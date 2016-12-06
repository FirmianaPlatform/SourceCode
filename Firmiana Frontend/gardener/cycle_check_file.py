#!/usr/bin/env python
import sys, optparse, os, shutil, math, re, commands
import oss

from oss.oss_api import *

ms_tools_path = os.path.join( os.path.dirname( __file__ ), '..')
GALAXY_ROOT = os.path.join( ms_tools_path, '..', '..' )
api_path = os.path.join( GALAXY_ROOT, 'scripts/api' )
LOG_FILE_DIR = os.path.join(GALAXY_ROOT, 'one_key_download_log' )

sys.path.insert(1, ms_tools_path)
from models.gardener_control import *
from config.firmianaConfig import *

sys.path.insert(1, api_path )
from common import submit, display, delete as common_del
#GALAXY_ROOT = ConfigSectionMap("Galaxy")['root_path']
from aliyun_download import *

SPLIT_LINE = '================================'

def stop_err( msg ):
    sys.stderr.write( "%s\n" % msg )
    sys.exit(1)

def logPrint(line):
    YearMonth = str(datetime.datetime.now().strftime('%Y-%m-%d'))
    logfile = os.path.join(LOG_FILE_DIR, '%s.uploadlog' %YearMonth)
    f = open(logfile ,'a')
    line = line + '\n'
    f.write(line)
    f.close()

def fileReady(conn, meta, eid):
    e = Table('gardener_experiment',meta, autoload=True, autoload_with=engine)
    s = e.update().where(e.c.id==eid).values({ e.c.stage:0,e.c.state:'uploaded'})
    res = conn.execute(s)
    return res

def checkFormat(fname, format):
    if fname.lower().find('.' + format) == -1:
        return False
    else:
        return True

def expPrepare(base, exp_info):
    e_name = exp_info['e_name']
    eid = exp_info['eid']  
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
    #logPrint('Email: %s'%email)

    #logPrint('API_key: %s'%key)
    (species, instru, format, workflow_key) = get_instru_format_wf(conn, meta, eid)
            
    (num_rep, num_fra) = getRepFra(conn, meta, e_name)#options.rep    
     
    #===========================================================================
    #     
    # out_folder = '/usr/local/firmiana/data/rawfile_BPRC_bak/%s/%s' %(instru, exp_Num)
    # if not os.path.exists(out_folder): 
    #     os.makedirs(out_folder)
    #===========================================================================  
    exp_info['file_source'] = 'nas'
    exp_info['e_num']  = e_name[3:]
    exp_info['uid']   = user_id
    exp_info['user']  = user
    exp_info['email'] = email
    exp_info['num_rep'] = num_rep
    exp_info['num_fra'] = num_fra
    exp_info['instru'] = instru
    exp_info['species'] = species
    exp_info['format'] = format     
    exp_info['lib_folder_name'] = 'API imported %s' %e_name
    exp_info['num_files'] = int(num_rep)*int(num_fra) if format != 'wiff' else int(num_rep)*int(num_fra) * 2
    #lib_folder_name = 'New imported %s' %e_name
    log_line = 'Species: %s | Instrument: %s' %(species, instru)
   
    return (1, exp_info, log_line)
    #return (num_rep, num_fra, lib_folder_name) 

def get_instru_format_wf(conn, meta, eid):
    
    #exp = Table('experiments_experiment',meta, autoload=True, autoload_with=engine)
    #s = select([exp.c.instrument_name]).where(exp.c.name == e_name)
    exp = Table('gardener_experiment', meta, autoload=True, autoload_with=engine)
    s = select([exp.c.instrument]).where(exp.c.id == eid)
    instru_full = conn.execute(s).scalar()

    species = get_species(conn, meta, eid)

    format = 'raw'
    #workflow_key = ''
    instru = 'none'
    
    if 'LTQ Orbitrap Velos' == instru_full :
        instru = "Velos"
    elif 'LTQ' == instru_full :
        instru = "LTQ"
    elif 'Fusion' == instru_full :
        instru = "Fusion"
        #workflow_key = 'e46ebed6f2d8f086'
    elif ('QExactive' == instru_full) or ('Q Exactive' == instru_full) :
        instru = "QExactive"

    elif ('Q Exactive Plus' == instru_full) or ('QExactive Plus' == instru_full) :
        instru = "QExactivePlus"
            
    elif '5600 Q-TOF' == instru_full :
        instru = "QTOF5600"
        format = 'wiff'
    elif '6600 Q-TOF' == instru_full:
        instru = "QTOF6600"
        format = 'wiff'

    
        #stop_err('None instrument!') 
    
    #print 'Instrument:%s'%instru_full
    #print 'Workflow:%s'%workflow_key 
    return (species, instru, format)
 
def getNoFileExp(conn,meta):
    dividline = '----------------getNoFileExp----------------'
    exp_list = []
    exp = Table('gardener_experiment',meta, autoload=True, autoload_with=engine)
    sel = select([exp.c.id, exp.c.name, exp.c.priority]).where(and_(exp.c.stage==-1,exp.c.started==0,exp.c.is_deleted==0)).order_by(exp.c.id)
    res = conn.execution_options(autocommit=True).execute(sel)
    if res != None:
        for row in res:
            exp_list.append((row[exp.c.id], row[exp.c.name], row[exp.c.priority]))
    #print 'Undone exp list:',','.join(exp_list),'\n'
    if len(exp_list)!=0:
        exp_list.sort(key= lambda x:x[2],reverse=1)
        exp_line = [e[1] for e in exp_list]
        tmp = '%s\nTime : %s\nUndone exp : %s'%(dividline, date_now(),','.join(exp_line))
        logPrint(tmp)        
        #logPrint('Undone exp : %s'%(','.join(exp_list)))
    res.close()
    return exp_list      
         
def getRepFra(conn,meta,e_name):
    e = Table('gardener_experiment',meta, autoload=True, autoload_with=engine)
    s = select([e.c.num_repeat,e.c.num_fraction]).where(e.c.name == e_name)
    #res = conn.execute(s)
    res = conn.execution_options(autocommit=True).execute(s).fetchone()
    fra = res[1]
    rep = res[0]
    
    return (rep, fra)

 
def getFilePath(base, base_bprc, base_ftp_tmp, exp_info):
    email = exp_info['email']
    instru = exp_info['instru']
    exp_Num = exp_info['e_num']
    instru = exp_info['instru']
    
    exp_info['path'] = os.path.join(base, email, instru, exp_Num)
    exp_info['path_bprc'] = os.path.join(base_bprc, instru, exp_Num)
    exp_info['path_ftp_tmp'] = os.path.join(base_ftp_tmp, instru, exp_Num)
    '''
    if hand_input_path!='none':
        path = os.path.join(hand_input_path,str(r))
    '''
        
    #return (path, path_bprc, path_ftp_tmp)

def getRawFileNum(path, format):
    num = 0
    fra_rep_set = set()
    for file in os.listdir(path):
        if not checkFormat(file, format):
            continue
        res1 = re.search(r'\_E(\d+)\_F(\d+)\_R(\d+)\.', file)
        if res1:
            return -2
        res = re.search(r'\_F(\d+)\_R(\d+)\.', file)
        if not res:
            continue
        fra = res.group(1)
        rep = res.group(2)
        tmp = fra+'_'+rep
        fra_rep_set.add(tmp)
        num += 1
    real_num = len(fra_rep_set)
    if format == 'wiff': real_num = real_num*2
    if real_num != num:
        return -1
    #print format, 'Num', num
    return num

def checkFilePath(exp_info):
    def check_file_NAS(exp_info):
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
    #print 'Searching file in %s'%path
    #logPrint('Searching file in [%s]' %path)
    
    if not os.path.exists(path):
        if file_source == 'nas':
            return check_file_NAS(exp_info)
        elif file_source == 'aliyun':
            return check_file_aliyun(exp_info)
        elif file_source == 'amazon':
            return check_file_amazon(exp_info)


    else:
        logPrint('Find path in your email folder: [%s]' %path)
        total = getRawFileNum(path, format)
        #total = len(os.listdir(path))
        #if format == 'wiff': total = total/2
        if total == -2 or total == all_file:
            logPrint('Already copied before!') 
            fileReady(conn, meta, exp_info['eid'])
            return 'ok'
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
    
def copy_from_bprc(path_bprc,path, format):
    #print 'Now try copy files from NAS...'
    logPrint('start :%s...Now start copy files from NAS/FTP...'%date_now())
    for file_bprc in os.listdir(path_bprc):
        if not checkFormat(file_bprc, format):
            continue
        fullpath_src = os.path.join(path_bprc, file_bprc)
        fullpath_dst = os.path.join(path,      file_bprc)
        if os.path.isfile(fullpath_dst):
            logPrint('%s existed'%fullpath_dst)
            if os.path.getsize(fullpath_dst) == os.path.getsize(fullpath_src):
                continue
        #logPrint('%s existed'%fullpath_src)
        shutil.copy(fullpath_src, path)
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
                
def __main__():
    ''' Prevent this script from running again '''
    aa = commands.getoutput("ps aux|grep cycle_check_file|grep -v grep")
    iii = aa.count('cycle_check_file.py')
    if iii > 1:
        print 'cycle_check_file already running'
        exit(1)
        
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
            if not os.path.isfile('%s/database/files/NFS_192.168.12.89' %GALAXY_ROOT):
                stop_err('NFS folder error!') 
               
            eid = experiment[0]
            e_name = experiment[1]
            if not e_name.startswith('Exp'):
                logPrint('Error:e_name does not start with Exp!')
                #fileReady(conn, meta, eid)
                continue
            #eid = get_exp_id(conn, meta, e_name)
            """ all about this experiment """
            exp_info={}
            exp_info['eid']   = eid
            exp_info['e_name'] = e_name


            logLine = '' 
            dividline = '----------------------------------------'
            
            (ok, exp_info, log1) = expPrepare(base, exp_info)
            if not ok:
                continue
            
            ################    Rename & check file path  ###################
            #(path, path_bprc, path_ftp_tmp)
            getFilePath(base, base_bprc, base_ftp_tmp, exp_info)
            
            check_status = checkFilePath(exp_info)
            if check_status == 'err':
                print 'err'
            elif check_status == 'nas':
                copy_from_bprc(exp_info)
            elif check_status == 'aliyun':
                aliyun_download(exp_info)
            elif check_status == 'amazon':
                amazon_download(exp_info)
            
        time.sleep(10)  

if __name__ == '__main__':
    __main__()
