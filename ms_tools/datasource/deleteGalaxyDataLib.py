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
        print 'no such exp'
        exit(0)
        
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

def logPrint(line):
    print line
    print

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

    api_url      = ConfigSectionMap("Firmiana")['address'] + 'api/'
    base         = os.path.join(GALAXY_ROOT, 'database/files/raw_files')
    base_bprc    =  ConfigSectionMap("Galaxy")['bprc_nas']#'/usr/local/galaxyDATA01/bprc_dingchen'
    base_ftp_tmp =  ConfigSectionMap("Galaxy")['ftp']#'/usr/local/galaxyDATA01/data/ftpdata'
    
    exp_info={}
    enum = raw_input('Input exp num like [002333,000123]:\n')
    e_name = 'Exp'+enum
    exp_info['api_url'] = api_url
    exp_info['api_key'] = getAPIkey(conn,meta,2)
    exp_info['lib_folder_name'] = 'API imported %s' %e_name
    
    print exp_info
    
    (library_id, lib_folder_id, lib_exist)  = getLibFolderID(exp_info)
    
    print 'library_id:' + str(library_id)
    print 'lib_folder_id:' + str(lib_folder_id)
    print 'lib_exist:' + str(lib_exist)
    
    res = common_del(exp_info['api_key'], api_url + "libraries/%s" % library_id, {'purge':True}, return_formatted = False)
    print res

if __name__ == '__main__':
    __main__()
