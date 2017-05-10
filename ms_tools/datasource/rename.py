#!/usr/bin/env python
import sys, optparse, os, shutil, math, re, commands
import oss

from oss.oss_api import *

ms_tools_path = os.path.join( os.path.dirname( __file__ ), '..')
GALAXY_ROOT = os.path.join( ms_tools_path, '..', '..' )
api_path = os.path.join( GALAXY_ROOT, 'scripts/api' )
LOG_FILE_DIR = os.path.join(GALAXY_ROOT, 'one_key_run_log' )

sys.path.insert(1, ms_tools_path)
from models.gardener_control import *
from config.firmianaConfig import *

sys.path.insert(1, api_path )
from common import submit, display, delete as common_del
#GALAXY_ROOT = ConfigSectionMap("Galaxy")['root_path']
REGEX_FR  = re.compile(r'\_F(\d+)\_R(\d+)\.')
REGEX_EFR = re.compile(r'\_E(\d+)\_F(\d+)\_R(\d+)\.')
SPLIT_LINE = '='*10

def stop_err( msg ):
    sys.stderr.write( "%s\n" % msg )
    sys.exit(1)
    
def logPrint(line):
    YearMonth = str(datetime.datetime.now().strftime('%Y-%m-%d'))
    logfile = os.path.join(LOG_FILE_DIR, '%s.log' %YearMonth)
    f = open(logfile ,'a')
    line = line + '\n'
    f.write(line)
    f.close()
    
def rerun(conn,meta,e_name):
    return 'no'

def expStart(conn, meta, eid, flag):
    e = Table('gardener_experiment',meta, autoload=True, autoload_with=engine)
    s = e.update().where(e.c.id==eid).values({e.c.started:flag, e.c.stage:flag,e.c.state:'running'})
    res = conn.execute(s)
    return res

def checkFormat(fname, format):
    if fname.lower().find('.' + format) == -1:
        return False
    else:
        return True
    
def checkRunned(conn, meta, fname, user):
    tmp = {}
    n = REGEX_EFR.search(fname)
    e_name = 'Exp'+n.group(1)
    tmp['f_num'] = n.group(2)
    tmp['r_num'] = n.group(3)
    tmp['user'] = user
    tmp['rank'] = 1
    tmp['exp_db_id'] = get_exp_id(conn, meta, e_name)
    sid = get_search_id(conn, meta, tmp)
 
    return sid

def expPrepare(base, exp_info):
    e_name = exp_info['e_name']
    eid = exp_info['eid']  
    api_url = exp_info['api_url']  
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
    #logPrint('Email: %s'%email)
    api_key = getAPIkey(conn, meta, user_id)
    if api_key == None:
        return (0, '')
    #logPrint('API_key: %s'%key)
    (instru_folder, format, workflow_key) = get_instru_format_wf(conn, meta, exp_info)
    workflow_key = get_workflows(format, api_key, api_url)
    if workflow_key == '':
        logPrint('Error:No workflow_key found!')
        return (0, '')
            
    workflow = display(api_key, api_url + 'workflows/%s' % workflow_key, return_formatted = False)
    if not workflow:
        #print "Workflow [%s] not found."%workflow_key
        logPrint("Error:Workflow [%s] not found." %workflow_key)
        return (0, '')
            
    #===========================================================================
    #     
    # out_folder = '/usr/local/firmiana/data/rawfile_BPRC_bak/%s/%s' %(instru, exp_Num)
    # if not os.path.exists(out_folder): 
    #     os.makedirs(out_folder)
    #===========================================================================  
    exp_info['e_num'] = e_name[3:]
    exp_info['uid']   = user_id
    exp_info['user']  = user
    exp_info['email'] = email
    exp_info['api_key'] = api_key
    exp_info['instru_folder'] = instru_folder
    exp_info['workflow_key']  = workflow_key
    exp_info['workflow'] = workflow
    exp_info['format']   = format     
    exp_info['lib_folder_name'] = 'API imported %s' %e_name
    exp_info['num_files'] = int(num_rep)*int(num_fra) if format != 'wiff' else int(num_rep)*int(num_fra) * 2
    #lib_folder_name = 'New imported %s' %e_name
    log_line = 'Species: %s | Instrument: %s | Workflow_key: %s' %(exp_info['species'], exp_info['instru_full'], workflow_key)
   
    return (1, log_line)
    #return (num_rep, num_fra, lib_folder_name) 

def get_instru_format_wf(conn, meta, exp_info):
    
    instru_full = exp_info['instru_full']

    species = exp_info['species']
    #print 'Species:',species
    #logPrint('Species: %s' %species)

    workflow_key = 'xxx'
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
    elif 'Fusion Lumos' == instru_full :
        instru = "FusionLumos"
        
    elif ('QExactive' == instru_full) or ('Q Exactive' == instru_full) :
        instru = "QExactive"
    elif ('Q Exactive Plus' == instru_full) or ('QExactive Plus' == instru_full) :
        instru = "QExactivePlus"
    elif ('Q Exactive HF' == instru_full) or ('QExactive HF' == instru_full) :
        instru = "QExactiveHF"      
          
    elif '5600 Q-TOF' == instru_full :
        instru = "QTOF5600"
        format = 'wiff'
        workflow_key = 'xxx'
    elif '6600 Q-TOF' == instru_full:
        instru = "QTOF6600"
        format = 'wiff'
        workflow_key = 'xxx'
    else:
        workflow_key = ''
    
        #stop_err('None instrument!') 
    
    #print 'Instrument:%s'%instru_full
    #print 'Workflow:%s'%workflow_key 
    return (instru, format, workflow_key)
    
def getRunningJob(conn,meta):
    j = Table('job',meta, autoload=True, autoload_with=engine)
    s = select([func.count(j.c.state)]).where(j.c.state=='running')
    return conn.execution_options(autocommit=True).execute(s).scalar()
 
def getUndoneExp(conn,meta):
    dividline = '----------------getUndoneExp----------------'
    exp_list = []
    exp = Table('gardener_experiment',meta, autoload=True, autoload_with=engine)
    
    sel = select([exp.c.id, exp.c.name, exp.c.priority,exp.c.instrument,exp.c.species,exp.c.num_fraction,exp.c.num_repeat]).\
    where(and_(exp.c.stage==0,exp.c.started==0,exp.c.is_deleted==0)).order_by(exp.c.id)
    
    res = conn.execution_options(autocommit=True).execute(sel)
    if res != None:
        for row in res:
            exp_list.append((row[exp.c.id], row[exp.c.name], row[exp.c.priority],row[exp.c.instrument],
                            row[exp.c.species],row[exp.c.num_fraction],row[exp.c.num_repeat]))
    #print 'Undone exp list:',','.join(exp_list),'\n'
    if len(exp_list)!=0:
        exp_list.sort(key= lambda x:x[2],reverse=1)
        exp_line = [str(e[1]) for e in exp_list]
        tmp = '%s\nTime : %s\nUndone exp : %s'%(dividline, date_now(),','.join(exp_line))
        logPrint(tmp)        
        #logPrint('Undone exp : %s'%(','.join(exp_list)))
    res.close()
    return exp_list      
         
def getAPIkey(conn,meta,user_id):
    
    max_id = 0
    k = Table('api_keys',meta, autoload=True, autoload_with=engine)
    s = select([k.c.id,k.c.key]).where(k.c.user_id==user_id)
    res = conn.execute(s)
    if res==None:
        #print 'Please generate your API key first!'
        logPrint('Error:Please generate your API key first!')
        return res
        #stop_err( 'Please generate your API key first!' )
    for row in res:
        if row[k.c.id] > max_id:
            max_id = row[k.c.id]
            key = row[k.c.key]
    #print 'API_key:',key
    
    return key
 
def getFilePath(base, base_bprc, base_ftp_tmp, exp_info):
    email = exp_info['email']
    instru_folder = exp_info['instru_folder']
    exp_Num = exp_info['e_num']
    
    path      = os.path.join(base, email, instru_folder, exp_Num)
    path_bprc = os.path.join(base_bprc, instru_folder, exp_Num)
    path_ftp_tmp = os.path.join(base_ftp_tmp, instru_folder, exp_Num)
    '''
    if hand_input_path!='none':
        path = os.path.join(hand_input_path,str(r))
    '''
        
    return (path, path_bprc, path_ftp_tmp)

def getRawFileNum(path, format):
    num = 0
    fra_rep_set = set()
    for file in os.listdir(path):
        if not checkFormat(file, format):
            continue
        #=======================================================================
        # if file.endswith(format):
        #     fra_rep_set.add(file)
        #     num += 1
        #     continue
        #=======================================================================
        
        #res1 = REGEX_EFR.search(file)
        #if res1:
        #    return -2
        res = REGEX_FR.search(file)
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

def get_order_f_old(x): 
    a = re.search(r'([^A-Z^a-z]f|[^A-Z^a-z]F|band|BAND|fr|Fr)(\d+)',x)
    if a == None:
        return x 
    return int(a.group(2))

def get_order_r_old(x):
    a = re.search(r'(\d+)\.',x)
    if a == None:
        return x 
    return int(a.group(1))

def get_order_f(x): 
    a = re.search(r'_F(\d+)_R(\d+)\.',x)
    if a == None:
        a = re.search(r'_f(\d+)_r(\d+)\.',x)
        if a == None:
            return x 
    return int(a.group(1))

def get_order_r(x):
    a = re.search(r'_F(\d+)_R(\d+)\.',x)
    if a == None:
        a = re.search(r'_f(\d+)_r(\d+)\.',x)
        if a == None:
            return x 
    return int(a.group(2))

def old_rename(files, path, exp_Num, num_fra, num_rep, format):
    num_f = 1
    num_r = 1
    files.sort(key=lambda x:get_order_f_old(x))
    if num_rep != 1:
        files.sort(key=lambda x:get_order_r_old(x))
    log_line = ''        
    for file in files: 
        if not checkFormat(file, format): 
            continue
        fullpath = os.path.join(path, file)
        if '.scan' in file :
            num_f = num_f - 1
            newname = file.split(".")[0]+'_E'+str(exp_Num)+'_F'+str(num_f)+'_R'+str(num_r)+'.'+format+'.scan'
            if num_f == num_fra :
                num_f = 0
                num_r += 1
        else:
            newname = file.split(".")[0]+'_E'+str(exp_Num)+'_F'+str(num_f)+'_R'+str(num_r)+'.'+format
            
        newname = newname.replace('/', '_').replace(' ', '_').replace('(', '_').replace(')', '_')
        
        os.rename(fullpath, os.path.join(path, newname))
        
        exp = get_exp_info("("+newname+")")
        if exp['state']!=1:
            stop_err('Error in file naming[%s]'% newname ) 
            
        num_f += 1
        if format == 'raw' and num_f > num_fra:
            num_f = 1
            num_r += 1
        log_line += 'old name : %s\nnew name : %s\n' %(file, newname)
        if num_r > num_rep:break
        
    logPrint(log_line)
    
def renameFile(path, exp_info):
    exp_Num = exp_info['e_num']
    num_fra = exp_info['num_fra']
    num_rep = exp_info['num_rep']
    format = exp_info['format']
    old_name = 0
    #files = os.listdir(path)
    #===========================================================================
    # Check if the files have renamed, restore their names
    #===========================================================================
#     for file in files: 
#         if not checkFormat(file, format):
#             continue
#         fullpath = os.path.join(path, file)
#         if file.find('_E%s_F' %exp_Num) != -1:
#             if 'wiff.scan' in file :
#                 newname = file.split('_E%s_F' %exp_Num)[0]+'.'+format+'.scan'
#             else:
#                 newname = file.split('_E%s_F' %exp_Num)[0]+'.'+format
#             
#             os.rename(fullpath, os.path.join(path, newname))
    #===========================================================================
    # New name has _F1_R1. Sort them for rename
    #===========================================================================
    files = os.listdir(path)
    
    for file in files:
        if not checkFormat(file, format):
            continue
        res = REGEX_FR.search(file)
        if not res: 
            old_name = 1
            break
        
    if old_name:
        old_rename(files, path, exp_Num, num_fra, num_rep, format)
        #exit(0)
        return 1
    log_line = ''
    """ Be care of .wiff.scan """      
    for file in files: 
        if not checkFormat(file, format): 
            continue
        res = REGEX_FR.search(file)
        num_f, num_r = res.group(1), res.group(2)
        fullpath = os.path.join(path, file)
        ext_parts = file.split(".")
        
        EFR = '_E'+str(exp_Num)+'_F'+str(num_f)+'_R'+str(num_r)
        
        if len(ext_parts) > 2:
            newname = ext_parts[0]+ EFR +'.'+ext_parts[-2]+'.'+ext_parts[-1]
        else:
            newname = ext_parts[0]+ EFR +'.'+format
            
        newname = newname.replace('/', '_').replace(' ', '_').replace('(', '_').replace(')', '_')
        if file.find(EFR) == -1:
            os.rename(fullpath, os.path.join(path, newname))
        else:
            newname = file
        
        log_line += 'old name : %s\nnew name : %s\n' %(file, newname)
        exp = get_exp_info("("+newname+")")
        if exp['state']!=1:
            stop_err('Error in file naming[%s]'% newname ) 
    
        
    logPrint(log_line)
    #exit(0)    
    return 1

def getLibFolderID(exp_info):
    api_key = exp_info['api_key']
    api_url = exp_info['api_url']
    lib_folder_name = exp_info['lib_folder_name']
    library_id = lib_folder_id = -1
    try:
        libs = display(api_key, api_url + 'libraries', return_formatted=False)
    except:
        logPrint(api_url + 'libraries')
        logPrint("Error:Failure when libs = display")
        return (-1, -1, -1)
    
    library_id = None
    for library in libs:
        if library['name'] == lib_folder_name:
            if library['deleted']:
                continue
            library_id = library['id']
            lib_exist = 1
            #print 'Library [%s] existed!\n'%lib_folder_name
            logPrint('Library [%s] existed!'%lib_folder_name)
            #common_del(api_key, api_url + "libraries/%s" % library_id, {'purge':True}, return_formatted = False)
	    #print 'delete %s'%lib_folder_name, library_id
    if not library_id:
        lib_create_data = {'name':lib_folder_name}
        try:
            library = submit(api_key, api_url + 'libraries', lib_create_data, return_formatted=False)
        except:
            logPrint("Error:Failure when library = submit")
            return (-1, -1, -1)
        #print 'Library [%s] created!\n'%lib_folder_name
        logPrint('Library [%s] created!'%lib_folder_name)
        library_id = library['id']#library[0]['id']
        lib_exist = 0
        
    folders = display(api_key, api_url + "libraries/%s/contents" % library_id, return_formatted = False)
    for f in folders:
        if f['name'] == "/":
            lib_folder_id = f['id']
        
    if not library_id or not lib_folder_id:
        #print "Failure to configure library destination."
        logPrint("Error:Failure to configure library destination.")
        return (-1, -1, -1)
        #sys.exit(1)
        
    return (library_id, lib_folder_id, lib_exist) 

def get_LibDataList(exp_info, library_id):
    api_key = exp_info['api_key']
    api_url = exp_info['api_url']
    lib_folder_name = exp_info['lib_folder_name']
    
    dict_file = {}
    #print 'Delete lib [%s] and create it...'%lib_folder_name
    logPrint('Get file list from lib [%s]...' %lib_folder_name)
    '''
    logPrint('Delete lib [%s] and create it...' %lib_folder_name)
    data = {'purge':True}
    common_del(api_key, api_url + "libraries/%s" % library_id, data, return_formatted = False)
    (library_id,lib_folder_id,lib_exist) = getLibFolderID(api_key, api_url,lib_folder_name)
    '''
    libset = display(api_key, api_url + "libraries/%s/contents" % library_id, return_formatted = False)
    for lib in libset:
        if lib['type']=='folder':continue
        fn = lib['name'][1:] if lib['name'].startswith('/') else lib['name']
        dict_file[fn] = [lib]
    
    fname_count = 0
    for fname in dict_file:
        for tag in dict_file[fname]:
            if 'id' not in tag : continue
            fname_count += 1  
                  
    return ( dict_file, fname_count )
    
def uploadLibData(exp_info, library_id, lib_folder_id, path):
    format = exp_info['format']
    api_key = exp_info['api_key']
    api_url = exp_info['api_url']
    lib_folder_name = exp_info['lib_folder_name']
    #dict_file = {}
    #i = 0
    #libset = display(api_key, api_url + "libraries/%s/contents" % library_id, return_formatted = False)
    #for lib in libset:
    #    if lib['type']=='folder':continue
    #    i += 1
        
    #print 'Upload files to lib [%s]...\n'%lib_folder_name
    #logPrint('Upload files to lib [%s]...' %lib_folder_name)
    for fname in os.listdir(path):
        if not checkFormat(fname, format):
            continue
        res = REGEX_EFR.search(fname)
        if not res:
            continue
        fullpath = os.path.join(path, fname)
        if os.path.isfile(fullpath):    
            data = {}
            data['folder_id'] = lib_folder_id
            data['file_type'] = format
            data['dbkey'] = ''
            data['upload_option'] = 'upload_paths'
            data['filesystem_paths'] = fullpath
            data['create_type'] = 'file'
            #data['link_data_only'] = 'link_to_files'
            libset = submit(api_key, api_url + "libraries/%s/contents" % library_id, data, return_formatted = False)       
            #dict_file[fname] = libset
            logPrint('Uploading [%s]...' %fname)
            time.sleep(5)
    
    return 0
  
def get_workflows(format, api_key,api_url):
    workflow_id = ''
    wname = 'General Workflow'
    if format == 'wiff':
        wname = 'QTOF5600'
    #workflow_list = {}
    workflows = display(api_key,api_url + 'workflows',return_formatted = False)
    #i = 0
    for workflow in workflows:
        #i += 1
        if wname == workflow['name']:
            workflow_id = workflow['id']
            break
        #workflow_name = workflow['name']
        #workflow_info = display(api_key,api_url + 'workflows/%s' % workflow_id, return_formatted = False)
        #workflow_list[workflow_id] = [workflow_name,workflow_info,i]
    return workflow_id

def runWorkflow(dict_file, exp_info):
    
    def check_response(res,api_key,api_url,wf_data, runned):
        retry_num = 1
        while 'Error' in res:
            time.sleep(100)
            tmp = 'Error:%s\n[retry %s]%s' % (res, retry_num, wf_data['history'])
            logPrint(tmp)
            res = submit( api_key, api_url + 'workflows', wf_data, return_formatted=False)
            retry_num += 1
            if retry_num > 2 : 
                break
            
        if 'Error' in res:
            tmp = 'Error:[retry 10 times]%s' % wf_data['history']
            logPrint(tmp)
        else:
            #print res
            tmp = 'Running workflow : %s' %wf_data['history']
            logPrint(tmp)
            runned += 1
            #return 0
            time.sleep(10)
            # Successful workflow execution, safe to move dataset.
            #shutil.move(fullpath, os.path.join(out_folder, fname))
        return runned    
    
    user = exp_info['user']
    api_key = exp_info['api_key']
    api_url = exp_info['api_url']
    workflow = exp_info['workflow']
    num_files = exp_info['num_files']
    format = exp_info['format']    
    #print 'Workflow:\n', workflow 
    ddd = '='*30
    #print ddd
    #print 'dict_file:\n', dict_file
    #print ddd
    file_list = []
    runned = 0
    for fname in dict_file:
        for tag in dict_file[fname]:
            if 'id' in tag:
                file_list.append( (fname, tag['id']) )
                break
    if format == 'wiff':
        file_list.sort(key=lambda x:get_order_f(x[0]))
    else:
        file_list.sort(key=lambda x:get_order_f(x[0]))
    
    xxx = '\n'.join([xx[0] for xx in file_list])
    logPrint(xxx)
    ############## For wiff files ##############################################    
    if format == 'wiff':
        #print 'Wiff now..............\n'
        #print 'file_list:\n',file_list
        # Successful upload of dataset, we have the ldda now.  Run the workflow.
        #print file_list
        index = 0
        id = [0,0]
        while index < num_files:
            #print 'index:',index
            if 'wiff.scan' in file_list[index][0]:
                wiffname = file_list[index+1][0]
                id[1] = file_list[index][1]
                id[0] = file_list[index+1][1]
            else:
                wiffname = file_list[index][0]
                id[0] = file_list[index][1]
                id[1] = file_list[index+1][1]
            wf_data = {}
            wf_data['workflow_id'] = workflow['id']
            wf_data['history'] = "%s - %s" % (wiffname, workflow['name'])
            wf_data['ds_map'] = {}
            '''
                In wiff workflow, 'inputs 347' is .wiff, 'inputs 348' is .wiff.scan
                Be careful, dict is random access
            '''
            i = 0
                #print step_id, '|',ds_in
            for step_id in sorted(workflow['inputs'].keys()):
                wf_data['ds_map'][step_id] = {'src':'ld', 'id':id[i]}
                i += 1
                
            index += 2
            
            #print 'wf_data:\n',wf_data 
            #print ddd
            if checkRunned(conn, meta, wiffname, user) != None:
                logPrint('Error:[%s] runned before'%wiffname)
                continue
            res = submit( api_key, api_url + 'workflows', wf_data, return_formatted=False)
            
            runned = check_response(res,api_key,api_url,wf_data, runned)
            
        #exit(0)
        tmp = 'Runned workflows: %s' % runned
        logPrint(tmp)
        return 0
    ###############################################################################
    
    ############## For raw files ##################################################  
    for file in file_list:
        fname = file[0]
        file_id = file[1]
        """ Successful upload of dataset, we have the ldda now.  Run the workflow. """
        wf_data = {}
        wf_data['workflow_id'] = workflow['id']
        wf_data['history'] = "%s - %s" % (fname, workflow['name'])
        wf_data['ds_map'] = {}
        ''' In wiff workflow, 'inputs 347' is .wiff, 'inputs 348' is .wiff.scan '''
        for step_id, ds_in in workflow['inputs'].iteritems():
            wf_data['ds_map'][step_id] = {'src':'ld', 'id':file_id}
        #print 'wf_data:\n',wf_data 
        #print ddd
        if checkRunned(conn, meta, fname, user) != None:
            logPrint('Error:[%s] runned before'%fname)
            continue    
        res = submit( api_key, api_url + 'workflows', wf_data, return_formatted=False)
        
        runned = check_response(res,api_key,api_url,wf_data, runned)
                
    tmp = 'Runned workflows: %s' % runned
    logPrint(tmp)        
    return 0
    ###############################################################################

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

    api_url      = ConfigSectionMap("Firmiana")['address'] + 'api/'
    base         = os.path.join(GALAXY_ROOT, 'database/files/raw_files')
    base_bprc    =  ConfigSectionMap("Galaxy")['bprc_nas']#'/usr/local/galaxyDATA01/bprc_dingchen'
    base_ftp_tmp =  ConfigSectionMap("Galaxy")['ftp']#'/usr/local/galaxyDATA01/data/ftpdata'
    
    flag = 1
    
    while flag:
        NUM_CYCLE = 0
            
        exp_list = getUndoneExp(conn, meta)
        #exp_list.sort(reverse=0)
        for experiment in exp_list:
            if not os.path.isfile('%s/database/files/NFS_192.168.12.89' %GALAXY_ROOT):
                stop_err('NFS folder error!') 
                          
            eid    = experiment[0]
            e_name = experiment[1]
            
            #if e_name != 'Exp002169':
            #    continue
            
            
            """ all about this experiment """
            exp_info={}

            exp_info['api_url'] = api_url
            exp_info['eid']      = experiment[0]
            exp_info['e_name']   = experiment[1]
            exp_info['priority'] = experiment[2]
            exp_info['instru_full'] = experiment[3]
            exp_info['species'] = experiment[4]
            exp_info['num_fra'] = experiment[5]
            exp_info['num_rep'] = experiment[6]
            
            exp_info['check_flag'] = 0 
            
            if not e_name.startswith('Exp'):
                logPrint('Error:e_name does not start with Exp!')
                expStart(conn, meta, eid, 1)
                continue

            #Prevent exp being searched more than once
            #expStart(conn,meta,eid,1)
            
            while getRunningJob(conn, meta) > 10: 
                #print '%s has to wait 5 min.\n'%e_name
                #print 'Time:%s\n'%date_now()
                #logPrint('Time:%s\n%s has to wait 5 min.\n'%(date_now(),e_name))
                time.sleep(600)
            logLine = '' 
            dividline = '-'*30
            
            (ok, log1) = expPrepare(base, exp_info)
            if not ok:
                continue
            
            logLine += '%s\n*** Time: %s ***\n' %(dividline, date_now())
            logLine += 'Exp Name: %s | Email: %s | API_key: %s\n' %(e_name, exp_info['email'], exp_info['api_key'])
            logLine += log1
            logPrint(logLine)

            ##################################################################
            
            (library_id, lib_folder_id, lib_exist) = getLibFolderID(exp_info)
            if library_id == -1 or lib_folder_id == -1:
                continue
      
            status = 1
            path_list = []
            dict_file = {}
            #####################  Upload to libraries  #####################
            #===================================================================
            # Be care whether uploading to library is successful
            #===================================================================
            if lib_exist == 1:
                (dict_file, fname_count) = get_LibDataList(exp_info, library_id)
                print dict_file
                print len(dict_file)
                if fname_count != exp_info['num_files']:
                    common_del(exp_info['api_key'], api_url + "libraries/%s" % library_id, {'purge':True}, return_formatted = False)
                    (library_id, lib_folder_id, lib_exist) = getLibFolderID(exp_info)
                    if library_id == -1 or lib_folder_id == -1 : 
                        continue
                    logPrint('Already deleted lib [%s] and created it...' %exp_info['lib_folder_name'])
            #(dict_file, library_id, lib_folder_id, lib_exist) = uploadLibData(lib_exist, num_fra, api_key, api_url, library_id, lib_folder_id, path, format, lib_folder_name)
            if lib_exist != 1:
                ################    Rename & check file path  ###################
                (path, path_bprc, path_ftp_tmp) = getFilePath(base, base_bprc, base_ftp_tmp, exp_info)
                if e_name != 'Exp002084':
                    try:
                        
                        renameFile(path, exp_info)
                    except Exception,e:
                        #print str(e)
                        logPrint('Error:' + str(e)) 
                        continue
                
                #exit(0)
                
                uploadLibData(exp_info, library_id, lib_folder_id, path)
                
                fname_count = 0
                i = 0
                while fname_count != exp_info['num_files']:
                    i += 1
                    if i > 40:
                        logPrint('Checking LibDataList failed, file num error, useful file_count = %s!' % fname_count)
                        break
                    time.sleep(100)
                    (dict_file, fname_count) = get_LibDataList(exp_info, library_id)
                
            #################################################################
            ii = len(dict_file)
            
            if ii == exp_info['num_files']:
                expStart(conn, meta, eid, 1)
                #print 'Number of files in library [API imported %s]:%s\n'%(e_name,i)
                logPrint('Exp start now; Number of files in library [API imported %s]: %s' %(e_name, ii) )              
                #print 'dict_file:\n',dict_file        
                runWorkflow(dict_file, exp_info)
                
                NUM_CYCLE += 1  
                if NUM_CYCLE >1:
                    break
                #expStart(conn,meta,eid, 1)
            else:
                #print 'Wrong file amount in library [API imported %s]:%s\n'%(e_name,i)
                logPrint('Error:Wrong file amount in library [API imported %s]: %s\n' %(e_name, ii) )
            
            #exit(0) 
            #break 
        time.sleep(300)  

if __name__ == '__main__':
    __main__()
