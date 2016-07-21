#!/usr/bin/env python
#sys.path.append("/opt/galaxy-dist/tools/ms_tools/")
#sys.path.insert(0,"C:\\\\Users\\\\us\\\\jmchilton-lwr-22ad7320bfc0")
import sys, optparse, os, tempfile, subprocess, shutil,shlex,math
#import zlib,base64,struct


def stop_err( msg ):
    sys.stderr.write( "%s\n" % msg )
    sys.exit()

def runTool(cmd):
    try:
        tmp_name = tempfile.NamedTemporaryFile( dir="." ).name
        tmp_stderr = open( tmp_name, 'wb' )
        proc = subprocess.Popen( args=cmd, shell=True, stderr=tmp_stderr.fileno() )
        returncode = proc.wait()
        tmp_stderr.close()
        
        # Error checking.
        if returncode != 0:
            raise Exception, "return code = %i" % returncode
        
        return returncode
            
    except Exception, e:
        # Read stderr so that it can be reported:
        tmp_stderr = open( tmp_name, 'rb' )
        stderr = ''
        buffsize = 1048576
        try:
            while True:
                stderr += tmp_stderr.read( buffsize )
                if not stderr or len( stderr ) % buffsize != 0:
                    break
        except OverflowError:
            pass
        tmp_stderr.close()
        
        stop_err( 'Error running msconvert(wiff).\n%s\n' % ( str( e ) ) )
  
def getCmd():
    # Parse Command Line
    parser = optparse.OptionParser()
    parser.add_option( '-i', '--input', dest='input', action='store', type="string", help='MS run wiff file.')
    parser.add_option( '', '--input_scan', dest='input_scan', action='store', type="string", help='MS run wiff scan file.')
    parser.add_option( '', '--outformat', dest='outformat', action='store', type="string", help='MS run converted file format.')
    parser.add_option( '-o', '--output', dest='output', action='store', type="string", help='MS run converted file.')
    parser.add_option('', '--store_to_db', dest='store_to_db', action='store', help='')
    parser.add_option('-j', '--job_track_id', dest='job_track_id', action='store', type="string", help='Job track ID for firmiana.')
    parser.add_option('-u', '--user_id', dest='user_id', action='store', type="string", help='User id for galaxy runner.')
    parser.add_option('-a', '--label_name', dest='label_name', action='store', type="string", help='Label name for out file.')
    (options, args) = parser.parse_args()
    #cmd = 'wine /usr/local/firmiana/external_tools/wine/ProteoWizard\ 3.0.4624/msconvert.exe $input --mzXML -o - > $output'
    '''
    wiffname = options.input.replace('.dat','.wiff')
    scanname = options.input.replace('.dat','.wiff.scan')
    
    cmd  = 'cp ' + options.input + ' ' + wiffname+';wait;'
    cmd += 'cp ' + options.input_scan + ' ' + scanname+';wait;'  
    cmd += 'wine /usr/local/firmiana/external_tools/wine/ProteoWizard\ 3.0.4624/msconvert.exe '
    cmd += wiffname

    if options.outformat == 'mzXML':
        cmd += " --mzXML"
        
    cmd += " -o " + options.output
    cmd += '; wait; rm ' + scanname + ' ' + wiffname
    '''
    # wine /usr/local/tpp/pwiz/msconvert.exe $input --mzXML -o - > $output
    scanname=options.input_scan.replace('.dat','.wiff.scan')
    wiffname=options.input_scan.replace('.dat','.wiff')

    cmd = 'copy %s %s>test'%(options.input,wiffname)
    #windows use '&&' and copy 
    cmd += '&& copy %s %s>test'%(options.input_scan,scanname)
    cmd += '&& msconvert %s'%wiffname
    if options.outformat=='mzXML':
        cmd += ' --mzXML -z'
    else:
        cmd += ' --mzML -z'
    #cmd += ' --32'
    cmd += ' --filter \"peakPicking true 1-\"'
    cmd += ' -o - > %s'%options.output  
    # Debugging.
    #print cmd
    #print options
    return cmd, options, args
                  
def __main__():
    
    (cmd, options, args) = getCmd() 
    if options.store_to_db=='yes':  
        #(storename,file_data)=sql_gardener_file(options,conn,meta)
        #cmd += '; wait; cp ' + options.output + ' ' + store_file_path+"/" +storename
        runTool(cmd)
        #storeDB(conn,meta,file_data,options)            
    else:
        runTool(cmd)         
    
if __name__=="__main__": __main__()
