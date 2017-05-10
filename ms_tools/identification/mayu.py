#!/usr/bin/env python

'''
Created on 2013-3-4

@author: garfield
revised by lubx
'''
import sys, optparse, os, tempfile, subprocess, shutil
sys.path.append("/usr/local/firmiana/galaxy-dist/tools/ms_tools/")
from models.firmiana_models import *

session = Session()

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

def getFileString(fpath, outpath):
    """
    format a nice file size string
    """
    size = ''
    fp = os.path.join(outpath, fpath)
    s = '? ?'
    if os.path.isfile(fp):
        n = float(os.path.getsize(fp))
        if n > 2**20:
            size = ' (%1.1f MB)' % (n/2**20)
        elif n > 2**10:
            size = ' (%1.1f KB)' % (n/2**10)
        elif n > 0:
            size = ' (%d B)' % (int(n))
        s = '%s %s' % (fpath, size) 
    return s

        
def getAllOutput(outputdir,rep=[],flist=[],runlog=[]):
        """ add some of our stuff to the html
        """
        bodyindex = len(rep) -1  # hope they don't change this
        footrow = bodyindex - 1 
        footer = rep[footrow]
        rep = rep[:footrow] + rep[footrow+1:]
        res = ['<div class="module"><h2>Files created by Mayu</h2><table cellspacing="2" cellpadding="2">\n']
        flist.sort()
        for i,f in enumerate(flist):
             if not(os.path.isdir(f)):
                 fn = os.path.split(f)[-1]
                 res.append('<tr><td><a href="%s">%s</a></td></tr>\n' % (fn,getFileString(fn, outputdir)))
        res.append('</table>\n') 
        res.append('<a href="http://tools.proteomecenter.org/wiki/index.php?title=Software:Mayu/">Mayu documentation and full attribution is here</a><br/><hr/>\n')
        res.append('Mayu was run by Galaxy\n</div>')
        res.append(footer)
        fixed = rep[:bodyindex] + res + rep[bodyindex:]
        return fixed # with our additions

        
def __main__():
    """
    #The subprocess module provides more powerful facilities for spawning new processes and retrieving their results. 
    #Using the subprocess module is preferable to using the commands module.


    outdir='/tmp'
    shutil.copy(sys.argv[1], os.path.dirname(sys.argv[1])+'/temp.iproph.pep.xml')
    
    mayucmd="bash /home/garfield/Mayu/mayu.sh" + " " +os.path.dirname(sys.argv[1])+ '/temp.iproph.pep.xml' + " " + outdir
    mayu_stat,mayu_out = commands.getstatusoutput(mayucmd) 
    
    if mayu_stat==0:
        file_mayucsv='/tmp/temp.iproph.pep.xml_psm_mFDR1_td_1.06.csv'
        if os.path.isfile(file_mayucsv):
            shutil.copy(file_mayucsv, sys.argv[2])
    """  
    parser = optparse.OptionParser()
    parser.add_option('-i', '--input', dest='input', help=' ')
    parser.add_option('', '--informat', dest='informat', help=' ')
    parser.add_option('-o', '--output', dest='output', action='store', help='write output to file')
    parser.add_option('', '--dbkey', dest='dbkey', action='store', help='')
    parser.add_option('', '--decoy_pre', dest='decoy_pre', action='store', help='')
    parser.add_option('', '--mFDR_step', dest='mFDR_step', action='store', help='')
    parser.add_option('', '--nr_missCle', dest='nr_missCle', action='store', help='')
    #parser.add_option('', '--nr_step', dest='nr_step', action='store', help='')
    parser.add_option('', '--maxMFDR', dest='maxMFDR', action='store', help='')
    parser.add_option('', '--pmFDR', dest='pmFDR', action='store', help='')
    parser.add_option('', '--verbose', dest='verbose', action='store', help='')
    parser.add_option('', '--idset', dest='idset', action='store', help='')
    parser.add_option('', '--filter', dest='filter', action='store', help='')
    #parser.add_option('', '--filebase', dest='filebase', action='store', help='')
    parser.add_option('', '--runR', dest='runR', action='store', help='')     
    parser.add_option('', '--minLen', dest='minLen', action='store', help='')
    parser.add_option('-d', '--outputdir', dest='outputdir', action='store', default="/tmp/")
    parser.add_option('', '--dbop_type', dest='dbop_type', action='store', help='')    
    (options, args) = parser.parse_args()    
    
    
    if not os.path.exists(options.outputdir): 
        os.makedirs(options.outputdir)

    inpath = os.path.dirname(options.input)
    infilebase = os.path.splitext(os.path.basename(options.input))[0]  
    
    outdir = options.outputdir
    #print outdir
    #output files in outdir with base as input file
    outfilebase = outdir + '/' + infilebase
    #$out_base . '_main_' . $version
    version = '1.06'
    outfilename = outfilebase + '_main_' + version + '.csv'
    #print outfilename
    
    # Mayu.pl must be invoked from the directory containing the script
    cmd = 'cd /usr/local/src/TPP-4.5.2/extern/Mayu'
    #required
    #input file must end in .xml or .csv
    if options.informat == 'pepxml':
        infilename=inpath+'/'+infilebase+'.interact.pep.xml'
        if not os.path.isfile(infilename):
            cmd += '; cp '+options.input+' '+infilename
        cmd +=' perl Mayu.pl'
        cmd += " -A " + infilename
    else: 
        infilename=inpath+'/'+infilebase+'.csv'
        if not os.path.isfile(infilename):
            cmd += '; cp '+options.input+' '+infilename
        cmd +='; wait; perl Mayu.pl'
        cmd += " -B " + infilename 
    
    #data has to be searched against one target decoy database (reversing recommended)         
    cmd += " -C " + options.dbkey
    #optional
    if options.minLen != '0':
        cmd += " -D " + options.minLen
    if options.decoy_pre != 'rev_':
        cmd += " -E " + options.decoy_pre
    if options.mFDR_step != '11':
        cmd += " -H " + options.mFDR_step
    if options.nr_missCle != '0':
        cmd += " -I " + options.nr_missCle
    #cmd +=" -O" + options.nr_step
    if options.maxMFDR != '0.01':
        cmd += " -G " + options.maxMFDR
    if options.idset != '0':
        cmd += " -N " + options.idset
    if options.filter != 'default':
        cmd += " -P " + options.filter
    if options.runR == 'true':
        cmd += " -runR" 
    if options.pmFDR == 'true':
        cmd += " -PmFDR"
    if options.verbose == 'true':
        cmd += " -verbose" 
    
    cmd += " -M " + outfilebase
    """
    if options.output.find('job_working_directory') != -1:
        outpath = options.output.replace('job_working_directory', 'files')
        outpath = outpath.replace('galaxy_dataset', 'dataset')
        #re.sub(pattern, repl, string, count=0, flags=0)
        #Return the string obtained by replacing the leftmost non-overlapping occurrences of pattern in string by the replacement repl
        pattern = r'(\/\d+)(\/\d+)'
        outpath = re.sub(pattern, '\g<1>', outpath)
    else:
        outpath = options.output
    
    #cp cannot deal with '*' in the filename, which mv can.
    cmd += ';  wait; cp ' + outfilename + ' ' + options.output     
    cmd += ';  wait; cp ' + outfilename + ' ' + outpath
    """
    print cmd
           
    try:
        #
        # Run command.
        #
        tmp_name = tempfile.NamedTemporaryFile(dir=".").name
        tmp_stderr = open(tmp_name, 'wb')
        proc = subprocess.Popen(args=cmd, shell=True, stderr=tmp_stderr.fileno(),cwd=options.outputdir)
        returncode = proc.wait()
        tmp_stderr.close()
      
        # Error checking.
        if returncode != 0:
            raise Exception, "return code = %i" % returncode
        else:
           flist = os.listdir(options.outputdir)
           runlog = open(tmp_name,'r').readlines() 
           """
            <!DOCTYPE html>
            <html>
            <body>
            <h1></h1>
            </body>
            </html> 
           """
           rep=['<!DOCTYPE html>\n','<html>\n','<body>\n','<h1>Mayu Report</h1>\n','</body>\n','</html>\n']
           #creat a html file listing all files in the output directory
           html=getAllOutput(options.outputdir,rep,flist,runlog)
           f = open(options.output, 'w')
           f.write(''.join(html))
           f.close()
           
    except Exception, e:
        # Read stderr so that it can be reported:
        tmp_stderr = open(tmp_name, 'rb')
        stderr = ''
        buffsize = 1048576
        try:
            while True:
                stderr += tmp_stderr.read(buffsize)
                if not stderr or len(stderr) % buffsize != 0:
                    break
        except OverflowError:
            pass
        tmp_stderr.close()
        
        stop_err('Error running Mayu.\n%s\n' % (str(e)))
             
    
    
if __name__ == "__main__": __main__()
