#!/usr/bin/env python
import sys, optparse, os, tempfile, subprocess, shutil

ms_tools_path = os.path.join( os.path.dirname( __file__ ), '..')
GALAXY_ROOT = os.path.join( ms_tools_path, '..', '..' )

sys.path.insert(1, ms_tools_path)
from config.firmianaConfig import *
from models.gardener_control import *

tpp = ConfigSectionMap("Tool")['tpp_bin']

def stop_err(msg, ret=1):
    sys.stderr.write(msg)
    sys.exit(ret)   

def writePrompt(outfile):
    file = open(outfile, 'w')
    prompt = 'Information for this analysis has been deleted in the database.\n'
    prompt += 'Please note that other records connected with this analysis have also been deleted,\n'
    prompt += 'such as all the following analysis results.\n'
    file.write(prompt)
    file.close()
    
def sql_gardener_file(options,conn,meta):
    
    file_data={}
       
    #file_data['job_id']=getJobId(conn,meta,options.job_track_id,options.user_id)
    cwd = os.getcwd()
    file_data['job_id'] = getJobId(cwd)
    exp=get_exp_info("("+options.label_name+")")
    if exp['state']==1 and file_data['job_id']!=-1:
        file_data['name']  =exp['name']
        file_data['exp_id']=exp['exp_id']
        file_data['f_num'] =exp['nf']
        file_data['r_num'] =exp['nr']   
    else:
        stop_err('Error in file naming, please verify your file name before run reference pipeline.\n' ) 
    
    file_data['exp_db_id'] = get_exp_id(conn,meta,'Exp'+file_data['exp_id'])#ID of every row in DB !!!
    file_data['file_type'] = 'mgf'
    file_data['type'] ='reference'
    file_data['size'] = 0
    file_data['path'] = options.output
    file_data['user'] = get_user_name(conn,meta,options.user_id)
    file_data['rank'] = get_rank(conn,meta,file_data)
    file_data['date'] = date_now()#time.strftime("%Y-%m-%d %X", time.gmtime())
    file_data['stage'] = 3
    (f, r) = get_file_num(conn,meta,file_data['exp_db_id'])
    file_data['file_num']  = f * r
    file_data['search_id'] = get_search_id(conn,meta,file_data)
    
    insert_file(conn,meta,file_data)
    
    return ((file_data['name']+"_"+file_data['job_id']+"."+file_data['file_type']),file_data)
                    
def runTool(cmd):                
    try:
        #Run command.
        tmp_name = tempfile.NamedTemporaryFile(dir=".").name
        tmp_stderr = open(tmp_name, 'wb')
        proc = subprocess.Popen(args=cmd, shell=True, stderr=tmp_stderr.fileno())
        returncode = proc.wait()
        tmp_stderr.close()
        
        # Error checking.
        if returncode != 0:
            raise Exception, "return code = %i" % returncode
        """
        else:
            outformat = 'mgf'
            storeConvertedRawfile(options.input, outformat, options.output, options.dbop_type)
        """
        return returncode             
    except Exception, e:
        # Read stderr so that it can be reported:
        tmp_stderr = open(tmp_name, 'rb')
        stderr = ''
        buffsize = 3048576
        try:
            while True:
                stderr += tmp_stderr.read(buffsize)
                if not stderr or len(stderr) % buffsize != 0:
                    break
        except OverflowError:
            pass
        tmp_stderr.close()
        
        stop_err('Error running MzXML2Search.\n%s\n' % (str(e)))
             
def getCmd():
    # Parse Command Line
    parser = optparse.OptionParser()
    parser.add_option('-i', '--input', dest='input', action='store', type="string", help='tandem result file.')
    parser.add_option('-m', '--mslv1', dest='mslv1', action='store', type="int", help='MS level to export.')
    parser.add_option('-x', '--mslv2', dest='mslv2', action='store', type="int", help='range of MS levels to export.')
    parser.add_option('-v', '--pkct', dest='pkct', action='store', type="int", help='specifying minimum peak count.')
    parser.add_option('-Z', '--zcharge', dest='zcharge', action='store', type="int", help='Maximum reported charge state.')
    parser.add_option('-s', '--intens', dest='intens', action='store', type="float", help='specify intensity precision in peaklist')
    parser.add_option('-F', '--first', dest='first', action='store', type="int", help='specify the first scan.')
    parser.add_option('-L', '--last', dest='last', action='store', type="int", help='specify the last scan')
    parser.add_option('-B', '--min', dest='min', action='store', type="float", help='specify minimum MH+ mass')
    parser.add_option('-T', '--max', dest='max', action='store', type="float", help='specify maximum MH+ mass')
    parser.add_option('-N', '--ip', dest='ip', action='store', type="float", help='specify intensity precision in peaklist (set to zero to output all peaks)')
    parser.add_option('', '--pm', dest='pm', action='store', type="float", help='Output precision -- Mass')
    parser.add_option('', '--pi', dest='pi', action='store', type="float", help='Output precision -- Intensity')
    #parser.add_option('-A', '--yes', dest='yes', action='store', type="string", help='have precusor charge?')
    #parser.add_option('', '--c1', dest='c1', action='store', type="int", help='Precursor charge to analyze')
    #parser.add_option('', '--c2', dest='c2', action='store', type="int", help='Precursor range to analyze')
    parser.add_option('-o', '--output', dest='output', action='store', type="string", help='converted pepxml file.')
    #parser.add_option('', '--dbop_type', dest='dbop_type', action='store', help='')
    parser.add_option('', '--store_to_db', dest='store_to_db', action='store', help='')
    parser.add_option('-j', '--job_track_id', dest='job_track_id', action='store', type="string", help='Job track ID for firmiana.')
    parser.add_option('-u', '--user_id', dest='user_id', action='store', type="string", help='User id for galaxy runner.')
    parser.add_option('-a', '--label_name', dest='label_name', action='store', type="string", help='Label name for out file.')
    (options, args) = parser.parse_args()

    infilename = options.input.replace('.dat', '.mzXML')    
    if not os.path.isfile(infilename):
        os.symlink(options.input, infilename)
        
    #no space between -O%s   
    cmd = "%s/MzXML2Search" %tpp
    
    # Add options.     
    if options.mslv1 != 2 or options.mslv2 != 1:
            cmd += ' -M%d -%d' % (options.mslv1, options.mslv2)
    if options.pkct != 5:
            cmd += ' -P%d' % options.pkct
    if options.zcharge != 7:
            cmd += ' -Z%d' % options.zcharge
    if options.intens != 0.01:
            cmd += ' -I%f' % options.intens
    if options.first != 0:
            cmd += ' -F%d' % (options.first)
    if options.last != 0:
            cmd += ' -L%d' % (options.last)
    if options.ip != 0:
            cmd += ' -N%d' % options.ip
    if options.min != 600.00:
            cmd += ' -B%f' % options.min
    if options.max != 4200.00:
            cmd += ' -T%f' % options.max
    if options.pm != 4:
            cmd += ' -pm%d' % options.pm
    if options.pi != 0:
            cmd += ' -pi%d' % options.pi
    """
        if cmp(options.yes, 'yes') == 0:
            cmd += ' -c%f -%f' % (options.c1, options.c2)
    """ 
    cmd += " -O%s -mgf %s" % (options.output, infilename)
    
    return (cmd,options,args)

def storeDB(conn,meta,file_data,options):
    file_data['date'] = date_now()#time.strftime("%Y-%m-%d %X", time.gmtime())
    file_data['size']= str(os.path.getsize(options.output)/1024)+'K'
    update_file(conn,meta,file_data)
    update_search_stage(conn, meta, file_data)
    
    sid = get_cache_rep_sid(conn,meta,file_data)
    update_rep_stage(conn, meta, file_data,sid)
    
    updateExpStage(conn,meta,file_data)
               
def __main__():
    (cmd,options,args)=getCmd()
    # Debugging.
    print cmd
    #print 'CWD:', os.getcwd()
    if options.store_to_db=='yes':
        (storename,file_data)=sql_gardener_file(options,conn,meta)
        #cmd += '; wait; cp ' + options.output + ' ' + store_file_path+"/" +storename
        runTool(cmd)
        storeDB(conn,meta,file_data,options)
    else:
        runTool(cmd)
    
if __name__ == "__main__": __main__()
