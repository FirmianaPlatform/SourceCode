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
    cwd=os.getcwd()
    file_data['job_id']=getJobId(cwd)
    exp=get_exp_info("("+options.label_name+")")
    if exp['state']==1 and file_data['job_id']!=-1:
        file_data['name']=exp['name']
        file_data['exp_id']=exp['exp_id']
        file_data['f_num'] = exp['nf']
        file_data['r_num'] = exp['nr']    
    else:
        stop_err('Error in file naming, please verify your file name before run reference pipeline.\n' )
    file_data['stage']= 3
    file_data['user']= get_user_name(conn,meta,options.user_id)
    file_data['path']= options.output
    file_data['file_type']='mascotdat'
    file_data['type']='reference'
    file_data['size']= 0
    file_data['exp_db_id'] = get_exp_id(conn,meta,'Exp'+exp['exp_id'])#ID of every row in DB !!!
    insert_file(conn,meta,file_data)                 
    return ((file_data['name']+"_"+file_data['job_id']+"."+file_data['file_type']),file_data)

#return whether it is OK to run the tool
def checkDatabase(input, output, dbop_type):   
    try:
        dbSearchResult = session.query(DBSearchResult).filter(DBSearchResult.filepath == input).first()
        if not dbSearchResult:
            stop_err('Error updating records in DBSearchResult due to the lack of DBSearchResult record.\n')
        #if dbSearchResult.pepfilepath is not None :
        #it is strange that using only 'is not None', null pepepfilepath can not be detected
        if dbSearchResult.pepfilepath is not None and len(dbSearchResult.pepfilepath) > 0:
            if dbop_type == 'update':       
                return (True, dbSearchResult)                      
            elif dbop_type == 'delete':    
                dbSearchResult.pepfilepath = None
                session.commit()
                writePrompt(output)  
                return (False, None)
            else: 
                errlist = []         
                errlist.append('This raw file has been converted to type pepXML.\n')
                errlist.append('If you want to convert this file to type pepXML again,\n') 
                errlist.append('please choose "update" in the drop-down box "Change the information of the result for this analysis in the database".\n')
                errlist.append('Or else the original information in the database will be kept.')
                #print err
                stop_err('Error adding records to DBSearchResult.\n%s\n' % ''.join(errlist))           
        else:
            #print 'experiment is None'
            #if isUpdate == 'true' or isDelete == 'true':
            if dbop_type == 'update' or dbop_type == 'delete':      
                err = 'There is no information about this analysis in the database.'
                #print err
                stop_err('Error changing information for DBSearchResult in the database.\n%s\n' % err) 
            return (True, dbSearchResult)  
    except Exception, e:
        session.rollback()
        stop_err('Error checking records in DBSearchResult.\n%s\n' % (str(e)))  
    
def updateDBSearchResult(dbSearchResult, outputfile):        
    try:        
        dbSearchResult.pepfilepath = outputfile
        #print dbSearchResult
        session.commit()
    except Exception, e:
        session.rollback()
        stop_err('Error updating records in DBSearchResult.\n%s\n' % (str(e)))  

def runTool(cmd):               
    try:
        #
        # Run command.
        #
        tmp_name = tempfile.NamedTemporaryFile(dir=".").name
        tmp_stderr = open(tmp_name, 'wb')
        proc = subprocess.Popen(args=cmd, shell=True, stderr=tmp_stderr.fileno())
        returncode = proc.wait()
        tmp_stderr.close()
        
        # Error checking.
        if returncode != 0:
            raise Exception, "return code = %i" % returncode
        #else:
            #updateDBSearchResult(options.input, options.output, options.dbop_type)           
            #storefastaInfo(options.database,options.dbtype)
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
        
        stop_err('Error running Mascot2XML.\n%s\n' % (str(e)))
                  
def storefastaInfo(fafile, dbtype):
    try:
        for values in SimpleFastaParser(open(fafile, 'r')):
            (name, sequence) = values
            id_desc = name.split(' ', 1)
            #print id_desc
            id = id_desc[0]
            desc = id_desc[1]
            #print id
            #print desc            
            for instance in session.query(ProteinSequence).filter(ProteinSequence.sequence == sequence):
                if not instance:
                    protSeq = ProteinSequence(sequence)
                    print protSeq
                    session.add(protSeq) 
                   
                    protSeqInfo = ProteinSeqInfo(id, desc)
                    print protSeqInfo
                    session.add(protSeqInfo)
                                      
                    sequenceID = protSeq.id   
                    proteinSeqInfoID = protSeqInfo.id         
                    dbversion = dbtype  
                    dbname = fafile              
                    protSeqIDMap = ProteinSeqIDMap(sequenceID, dbtype, dbversion, dbname, proteinSeqInfoID)
                    print protSeqIDMap
                    session.add(protSeqIDMap)                                         
                else:
                    sequenceID = instance.id
                    for instance in session.query(ProteinSeqIDMap).filter(and_(ProteinSeqIDMap.sequenceID == sequenceID, ProteinSeqIDMap.dbtype == dbtype)):
                        if not instance:
                              protSeqInfo = ProteinSeqInfo(id, desc)
                              print protSeqInfo
                              session.add(protSeqInfo)
  
                              proteinSeqInfoID = protSeqInfo.id         
                              dbversion = dbtype  
                              dbname = fafile              
                              protSeqIDMap = ProteinSeqIDMap(sequenceID, dbtype, dbversion, dbname, proteinSeqInfoID)
                              print protSeqIDMap
                              session.add(protSeqIDMap) 
                session.commit()  
    except Exception, e:
         stop_err('Error updating records in PeptideIdentification.\n%s\n' % (str(e))) 
          
def SimpleFastaParser(handle):
    """Generator function to iterator over Fasta records (as string tuples).

    For each record a tuple of two strings is returned, the FASTA title
    line (without the leading '>' character), and the sequence (with any
    whitespace removed). The title line is not divided up into an
    identifier (the first word) and comment or description.

    >>> for values in SimpleFastaParser(open("Fasta/dups.fasta")):
    ...     print values
    ('alpha', 'ACGTA')
    ('beta', 'CGTC')
    ('gamma', 'CCGCC')
    ('alpha (again - this is a duplicate entry to test the indexing code)', 'ACGTA')
    ('delta', 'CGCGC')

    """
    #Skip any text before the first record (e.g. blank lines, comments)
    while True:
        line = handle.readline()
        if line == "":
            return  # Premature end of file, or just empty?
        if line[0] == ">":
            break

    while True:
        if line[0] != ">":
            raise ValueError(
                "Records in Fasta files should start with '>' character")
        title = line[1:].rstrip()
        lines = []
        line = handle.readline()
        while True:
            if not line:
                break
            if line[0] == ">":
                break
            lines.append(line.rstrip())
            line = handle.readline()

        #Remove trailing whitespace, and any internal spaces
        #(and any embedded \r which are possible in mangled files
        #when not opened in universal read lines mode)
        yield title, "".join(lines).replace(" ", "").replace("\r", "")

        if not line:
            return  # StopIteration

    assert False, "Should not reach this line"
    
#inputfile: the full name of input mzXML file

           
def getCmd():
    # Parse Command Line
    parser = optparse.OptionParser()
    parser.add_option('-i', '--input', dest='input', action='store', type="string", help='mascot result file.')
    parser.add_option('-o', '--output', dest='output', action='store', type="string", help='converted pepxml file.')
    parser.add_option('-d', '--database', dest='database', action='store', type="string", help='database.')
    parser.add_option('-e', '--enzyme', dest='enzyme', action='store', type="string", help='database.')
    parser.add_option('', '--semi', dest='semi', action='store', type="string", help='semi')
    parser.add_option('', '--pI', dest='pI', action='store', type="string", help='pI')
    parser.add_option('', '--nc', dest='nc', action='store', type="string", help='nc')
    parser.add_option('', '--po', dest='po', action='store', type="string", help='po')
    parser.add_option('', '--us', dest='us', action='store', type="string", help='us')
    #TO DO: find the appropriate metadata to retrieve db type
    parser.add_option('', '--dbtype', dest='dbtype', action='store', type="string", help='database.')
    #parser.add_option('', '--dbop_type', dest='dbop_type', action='store', help='')
    parser.add_option('', '--store_to_db', dest='store_to_db', action='store', help='')
    parser.add_option('-j', '--job_track_id', dest='job_track_id', action='store', type="string", help='Job track ID for firmiana.')
    parser.add_option('-u', '--user_id', dest='user_id', action='store', type="string", help='User id for galaxy runner.')
    parser.add_option('-a', '--label_name', dest='label_name', action='store', type="string", help='Label name for out file.')
    (options, args) = parser.parse_args()
    
    infilebase = os.path.splitext(os.path.basename(options.input))[0]  
    outfilename = os.path.join(os.path.dirname(options.input), ''.join([infilebase, '.pep.xml']))  
    
    # Mascot2XML <file.dat> (-D<database>) 
    #(-E<sample_enzyme>) (-html) (-pI) (-notgz) (-nodta) (-desc) (-shortid) (-verbose) (-t(!)<regression test>)'
    #will output a file with suffix .gz, 
    #no space between -D%s
    cmd = "%s/Mascot2XML %s -D%s" % (tpp, options.input, options.database)  

    if cmp(options.semi, 'true') == 0:
            cmd += ' -Esemi%s' % options.enzyme
    elif cmp(options.enzyme, 'default') != 0:
            cmd += ' -E%s' % options.enzyme
    if cmp(options.pI, 'true') == 0:
            cmd += ' -pI'
    if cmp(options.nc, 'true') == 0:
            cmd += ' notgz'
    if cmp(options.po, 'true') == 0:
            cmd += ' -desc'
    if cmp(options.us, 'true') == 0:
            cmd += ' -shortid'
    cmd += ';  wait; mv ' + outfilename + ' ' + options.output
    #os.rename(outfilename, options.output)
    # Debugging.
    print cmd
    return (cmd,options,args)

def storeDB(conn,meta,file_data,options,pars):
    file_data['date'] = time.strftime("%Y-%m-%d %X", time.gmtime())
    file_data['size']= str(os.path.getsize(options.output)/1024)+'K'
    update_file(conn,meta,file_data)
    file_data['search_id'] = get_search_id(conn,meta,file_data)
    file_data['num_peptide'] = parserMascotdat(options.output,file_data)
    update_search_param(conn,meta,pars,file_data)
    update_experiment(conn, meta, file_data)
    return file_data
    
def __main__():
    (cmd,options,args)=getCmd()
    #print status
    if options.store_to_db=='yes':   
        (storename,file_data,file)=sql_gardener_file(options,conn,meta)
        cmd += '; wait; cp ' + options.output + ' ' + store_file_path+"/" +storename
        runTool(cmd)
        file_data['size']= str(os.path.getsize(options.output)/1024)+'K'
        result=update_file(conn,meta,file_data,file)
    else:
        runTool(cmd)
    """
    (status, dbSearchResult) = checkDatabase(options.input, options.output, options.dbop_type)
    if status:
        #print 'go here'
        returncode = runTool(cmd)
        if returncode == 0:
            updateDBSearchResult(dbSearchResult, options.output)
     
    #updateDBSearchResult(options.input, options.output, options.dbop_type)
    """          
if __name__ == "__main__": __main__()
