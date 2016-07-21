#!/usr/bin/env python
import sys, optparse, os, tempfile, subprocess, shutil, re
ms_tools_path = os.path.join( os.path.dirname( __file__ ), '..')
GALAXY_ROOT = os.path.join( ms_tools_path, '..', '..' )

sys.path.insert(1, ms_tools_path)

from models.gardener_control import *
from config.firmianaConfig import *


def stop_err( msg ):
    sys.stderr.write( "%s\n" % msg )
    sys.exit()

def rerun(conn,meta,num_e):
    return 'no'

def getCmd():
    #runTool(cmd)         
    parser = optparse.OptionParser()
    parser.add_option('-u', '--user_id', dest='user_id', action='store', type="string", help='')
    parser.add_option('-e', '--exp_num', dest='exp_num', action='store', type="string", help='')
    parser.add_option('-o', '--output', dest='output', action='store', type="string", help='')
    
    (options, args) = parser.parse_args()
    return options
                
def __main__():
    
    options = getCmd()
    
    e_num_string = options.exp_num
    if e_num_string =='' or e_num_string == None:
        exit(0)
    #print e_num_string
    if ',' in e_num_string:
        e_num_list = e_num_string.split(',')
    else:
        e_num_list = e_num_string.split('X')#Because Galaxy trans ';' to 'X'.....
    print e_num_list
    
    xx = raw_input('Really go on???')
    if 'n' in xx:exit(0)
    #exit(0)
    for e_num in e_num_list:
        if e_num == '':
            continue
        e_name = 'Exp%s' %e_num
        exp_id = get_exp_id(conn, meta, e_name)
       
        t = 'UPDATE gardener_experiment set is_deleted=1 where id=%s' %exp_id
        conn.execute(t)
if __name__ == '__main__':
    __main__()
