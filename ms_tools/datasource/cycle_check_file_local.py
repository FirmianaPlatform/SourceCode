#!/usr/bin/env python
import sys, optparse, os, shutil, math, re, commands
from aliyun_download import *
from rename import getRawFileNum,checkFormat,get_instru_format_wf,stop_err
from rename import SPLIT_LINE

ms_tools_path = os.path.join( os.path.dirname( __file__ ), '..')
GALAXY_ROOT = os.path.join( ms_tools_path, '..', '..' )
api_path = os.path.join( GALAXY_ROOT, 'scripts/api' )
LOG_FILE_DIR = os.path.join(os.path.dirname( __file__ ), 'one_key_download_log' )

sys.path.insert(1, ms_tools_path)
from models.gardener_control import *
from config.firmianaConfig import *

sys.path.insert(1, api_path )
from common import submit, display, delete as common_del
#GALAXY_ROOT = ConfigSectionMap("Galaxy")['root_path']

def logPrint(line):
    YearMonth = str(datetime.datetime.now().strftime('%Y-%m-%d'))
    logfile = os.path.join(LOG_FILE_DIR, '%s.uploadlog' %YearMonth)
    f = open(logfile ,'a')
    line = line + '\n'
    f.write(line)
    f.close()

def expPrepare(base, exp_info):
    e_name = exp_info['e_name']
    eid = exp_info['eid']
    (num_fra,num_rep) = exp_info['num_fra'],exp_info['num_rep']  
    '''
    user_id = getUserID(conn,meta,e_name)
    if user_id == None:
        #print 'No user_id found!\n'
        logPrint('No user_id found!')
        continue
    '''
    user_id = 2#hzqnq@163.com
    user = 'qiunq'
    email = getEmail(conn, meta, user_id)
    email_folder = os.path.join(base, email)
    if not os.path.exists(email_folder): 
        os.makedirs(email_folder)

    (instru_folder, format, workflow_key) = get_instru_format_wf(conn, meta, exp_info)

    exp_info['e_num'] = e_name[3:]
    exp_info['uid']   = user_id
    exp_info['user']  = user
    exp_info['email'] = email
    exp_info['instru_folder'] = instru_folder
    exp_info['format']   = format
    exp_info['num_files'] = int(num_rep)*int(num_fra) if format != 'wiff' else int(num_rep)*int(num_fra) * 2
    #lib_folder_name = 'New imported %s' %e_name
    log_line = 'Species: %s | Instrument: %s' %(exp_info['species'], exp_info['instru_full'])
   
    return (1, log_line)
 
def getNoFileExp(conn,meta):
    dividline = '----------------getNoFileExp----------------'
    exp_list = []
    exp = Table('gardener_experiment',meta, autoload=True, autoload_with=engine)
    
    sel = select([exp.c.id, exp.c.name, exp.c.priority,exp.c.instrument,exp.c.species,exp.c.num_fraction,exp.c.num_repeat,exp.c.file_source]).\
    where(and_(exp.c.stage==-1,exp.c.started==0,exp.c.is_deleted==0,exp.c.file_source=='nas')).order_by(exp.c.id)
    
    res = conn.execution_options(autocommit=True).execute(sel)
    if res != None:
        for row in res:
            exp_list.append((row[exp.c.id], row[exp.c.name], row[exp.c.priority],row[exp.c.instrument],
                            row[exp.c.species],row[exp.c.num_fraction],row[exp.c.num_repeat],row[exp.c.file_source]))
    #print 'Undone exp list:',','.join(exp_list),'\n'
    if len(exp_list)!=0:
        exp_list.sort(key= lambda x:x[2],reverse=1)
        exp_line = [str(e[1]) for e in exp_list]
        tmp = '%s\nTime : %s\nNoFile exp : %s'%(dividline, date_now(),','.join(exp_line))
        #print tmp
        logPrint(tmp)        
        #logPrint('Undone exp : %s'%(','.join(exp_list)))
    res.close()
    return exp_list     
         
def getFilePath(base, base_bprc, base_ftp_tmp, exp_info):
    email = exp_info['email']
    instru_folder = exp_info['instru_folder']
    exp_Num = exp_info['e_num']
    
    instru_folder_dir = os.path.join(base, email, instru_folder)
    exp_info['path'] = os.path.join(instru_folder_dir, exp_Num)
    exp_info['path_bprc'] = os.path.join(base_bprc, instru_folder, exp_Num)
    exp_info['path_ftp_tmp'] = os.path.join(base_ftp_tmp, instru_folder, exp_Num)
    
    if not os.path.isdir(instru_folder_dir):
        os.makedirs(instru_folder_dir)

def check_file_md5(exp_info):
    exp_info['check_flag'] = 1
    res = copy_from_bprc(exp_info)
    exp_info['check_flag'] = 0   
    return res

def checkFilePath(exp_info):

    def check_file_NAS(exp_info):
        if not os.path.exists(exp_info['path_bprc']):
            logPrint('Error:No path:[%s]\n%s'%(exp_info['path_bprc'],SPLIT_LINE))
            return 'err'
        total = getRawFileNum(exp_info['path_bprc'], exp_info['format'])
        if total == all_file:
            return 'nas'
        else:#print 'Not enough files in NAS path:%s(%s/%s)'%(path_bprc,total,num_fra)
            logPrint('Error:Not enough files in outer path:[%s](%s/%s)\n%s'%(exp_info['path_bprc'],total,all_file,SPLIT_LINE))
            return 'err' 
    def check_file_aliyun(exp_info):
        return 'aliyun'
        return 'err'
    
    def  check_file_amazon(exp_info):
        return 'amazon'
        return 'err'
     
    file_source = exp_info['file_source']   
    path = exp_info['path']
    num_fra = exp_info['num_fra']
    num_rep = exp_info['num_rep']
    format = exp_info['format']
    all_file = exp_info['num_files']
    # have not uploaded before '''
    if not os.path.isdir(path):
        if file_source == 'nas':
            return check_file_NAS(exp_info)
        elif file_source == 'aliyun':
            return check_file_aliyun(exp_info)
        elif file_source == 'amazon':
            return check_file_amazon(exp_info)

    # Folder existed in Galaxy files 
    else:
        logPrint('Find path in your email folder: [%s]' %path)
        total = getRawFileNum(path, format)
        #total = len(os.listdir(path))
        #if format == 'wiff': total = total/2
        if total == -2 or total == all_file:
            check_result = check_file_md5(exp_info)
            if check_result == 1:
                logPrint('Already copied before!')
                updateFileReady(conn, meta, exp_info['eid'])
                return 'ok'
            else:
                return file_source
        if total == -1:
            logPrint('Error:check raw file names')
            return 'err'
        if total < all_file:
            return file_source
        elif total > all_file:
            logPrint('Error:Too many files!(%s/%s)'%(total,all_file))
            return 'err'    
    return 'err'   


def amazon_download(exp_info):
    pass      
    
def copy_from_bprc(exp_info):
    #print 'Now try copy files from NAS...'
    path_bprc = exp_info['path_bprc']
    path = exp_info['path']
    format = exp_info['format']
    logPrint('start :%s...Now start copy files from NAS...'%date_now())
    if not os.path.isdir(path):
        os.makedirs(path)
    for file_bprc in os.listdir(path_bprc):
        if not checkFormat(file_bprc, format):
            continue
        fullpath_src = os.path.join(path_bprc, file_bprc)
        fullpath_dst = os.path.join(path,      file_bprc)

        if os.path.isfile(fullpath_dst):
            logPrint('%s existed'%fullpath_dst)
            if os.path.getsize(fullpath_dst) == os.path.getsize(fullpath_src):
                continue
            elif exp_info['check_flag']:
                return 'undone'
        #logPrint('%s existed'%fullpath_src)
        os.symlink(fullpath_src, fullpath_dst)
        #shutil.copy(fullpath_src, path)
    #print 'Complete copying files from NAS\n'
    logPrint('end   :%s...Complete copying files from %s...'%(date_now(),path_bprc))
    return 1


def getCmd():
           
    parser = optparse.OptionParser()
    parser.add_option('-u', '--user_id', dest='user_id', action='store', type="string", help='')
    parser.add_option('-o', '--output', dest='output', action='store', type="string", help='')
    #parser.add_option('-w', '--workflow', dest='workflow_key', action='store', type="string", help='')
    parser.add_option('', '--hp', dest='own_path', action='store', type="string", help='')
    
    (options, args) = parser.parse_args()
    return options

def check_self_running():
    self_name = os.path.basename(__file__)
    aa = commands.getoutput("ps aux|grep %s|grep -v grep" %self_name)
    iii = aa.count(self_name)
    if iii > 1:
        print self_name,' already running'
        exit(1)
                        
def __main__():
    ''' Prevent this script from running again '''
    check_self_running()
        
    options = getCmd()

    base         = os.path.join(GALAXY_ROOT, 'database/files/raw_files')
    base_bprc    =  ConfigSectionMap("Galaxy")['bprc_nas']#'/usr/local/galaxyDATA01/bprc_dingchen'
    base_ftp_tmp =  ConfigSectionMap("Galaxy")['ftp']#'/usr/local/galaxyDATA01/data/ftpdata'
    
    flag = 1
    
    while flag:
        NUM_CYCLE = 0
            
        exp_list = getNoFileExp(conn, meta)
        #exp_list.sort(reverse=0)
        for experiment in exp_list:
            while not os.path.isfile('xxx'):
                print 'NAS disconnected.'
                cmd = 'xxx'
                output = os.popen(cmd)
                time.sleep(30) 
            if not os.path.isfile('xxx' %GALAXY_ROOT):
                stop_err('NFS folder error!') 
               
            """ all about this experiment """
            exp_info={}
              
            eid    = experiment[0]
            e_name = experiment[1]
            
            exp_info['eid']      = experiment[0]
            exp_info['e_name']   = experiment[1]
            exp_info['priority'] = experiment[2]
            exp_info['instru_full'] = experiment[3]
            exp_info['species'] = experiment[4]
            exp_info['num_fra'] = experiment[5]
            exp_info['num_rep'] = experiment[6]
            exp_info['file_source'] = experiment[7]
            
            exp_info['check_flag'] = 0 
            
            if not e_name.startswith('Exp'):
                logPrint('Error:e_name does not start with Exp!')
                #updateFileReady(conn, meta, eid)
                continue
            #eid = get_exp_id(conn, meta, e_name)

            logLine = '' 
            dividline = '-'*40
            
            (ok, log1) = expPrepare(base, exp_info)
            if not ok:
                continue
            
            ''' log experiment info '''          
            logLine += '%s\n*** Time: %s ***\n' %(dividline, date_now())
            logLine += 'Exp Name: %s | Email: %s \n' %(exp_info['e_name'], exp_info['email'])
            logLine += log1
            logPrint(logLine)
            
            ################    Rename & check file path  ###################
            #(path, path_bprc, path_ftp_tmp)
            getFilePath(base, base_bprc, base_ftp_tmp, exp_info)
            
            check_status = checkFilePath(exp_info)
            if check_status == 'err':
                pass
                #print 'err'
            elif check_status == 'nas':
                copy_from_bprc(exp_info)
            elif check_status == 'aliyun':
                aliyun_download(exp_info)
            elif check_status == 'amazon':
                amazon_download(exp_info)
            
        time.sleep(300)  

if __name__ == '__main__':
    __main__()
