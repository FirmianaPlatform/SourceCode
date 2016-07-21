#!/usr/bin/env python
import sys, optparse, os, tempfile, subprocess, shutil,shlex,math
import zlib,base64,struct

ms_tools_path = os.path.join( os.path.dirname( __file__ ), '..')
GALAXY_ROOT = os.path.join( ms_tools_path, '..', '..' )

sys.path.insert(1, ms_tools_path)
from models.gardener_control import *
from config.firmianaConfig import *

pwz = ConfigSectionMap("Tool")['wine']

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

def getFilesForEID(eID):
    files = []
    return files

"""    
def is_ms1_ms2(conn,meta,file_name,search_id):
    flag = 1
    search=Table('gardener_ms1_ms2',meta, autoload=True, autoload_with=engine)
    s = select([search.c.id]).where(search.c.file_name==file_name)
    res = conn.execution_options(autocommit=True).execute(s)
    row=res.fetchone()
    #print 'row',row
    if row==None:flag =-1
    return flag

def isDone(conn, meta, file_data):
    flag=0
    x=Table('gardener_search', meta, autoload=True, autoload_with=engine)
    s=select([func.count(x.c.num_spectrum)]).where(and_(x.c.exp_id==file_data['exp_db_id'],x.c.rank==file_data['rank']))
    res = conn.execution_options(autocommit=True).execute(s).scalar()
    if res==file_data['file_num']:
        flag=1
    return flag
"""

"""
def insert_ms1_ms2(conn,meta,inserts):
    ms=Table('gardener_ms1_ms2', meta, autoload=True, autoload_with=engine)
    ins = ms.insert()
    result=conn.execution_options(autocommit=True).execute(ins, inserts) 
    return result
"""

def rollback_exp(conn,meta,file_data):
    exp=Table('gardener_experiment',meta, autoload=True, autoload_with=engine)
    s = select([exp.c.num_spectrum]).where(exp.c.id==file_data['exp_db_id'])
    num_spec_exp = conn.execution_options(autocommit=True).execute(s).scalar()
    
    search=Table('gardener_search',meta, autoload=True, autoload_with=engine)
    s = select([search.c.num_spectrum]).where(and_(search.c.name==file_data['name'],search.c.rank==file_data['rank']-1))
    num_spec = conn.execution_options(autocommit=True).execute(s).scalar()
    
    upd=exp.update().where(exp.c.id==file_data['exp_db_id']).values(num_spectrum=num_spec_exp-num_spec)
    result=conn.execution_options(autocommit=True).execute(upd)
    return result

def sql_gardener_file(options,conn,meta):
    
    file_data = {}
      
    #file_data['job_id']=getJobId(conn,meta,options.job_track_id,options.user_id)
    cwd = os.getcwd()
    file_data['job_id']=getJobId(cwd)
    exp = get_exp_info("("+options.label_name+")")
    if exp['state']==1 :#and file_data['job_id']!=-1:
        file_data['name']  =exp['name']
        file_data['exp_id']=exp['exp_id']
        file_data['f_num'] =exp['nf']
        file_data['r_num'] =exp['nr']        
    else:
        stop_err('Error in file naming, please verify your file name before run reference pipeline.\n' ) 
    e_name = 'Exp' + file_data['exp_id']
    file_data['exp_db_id'] = get_exp_id(conn, meta, e_name)#ID of every row in DB !!!
    file_data['file_type'] = 'mzxml'
    file_data['type'] ='reference' 
    file_data['path'] = options.output
    file_data['size'] = 0
    file_data['user'] = get_user_name(conn, meta, options.user_id)
    file_data['rank'],insertDB = isNewSearch(conn, meta, file_data)  
    file_data['date'] = date_now()#time.strftime("%Y-%m-%d %X", time.gmtime())
    
    insert_file(conn, meta, file_data)
    
    file_data['stage'] = 2
    file_data['log'] = 'Insert Successfully.'
    (f, r) = get_file_num(conn, meta, file_data['exp_db_id'])
    file_data['file_num'] = f * r
    
    if int(file_data['f_num'])==1:
        if get_cache_exp_sid(conn,meta,file_data)==None:
            insert_cache_exp(conn,meta,file_data)
    
        if get_cache_rep_sid(conn,meta,file_data)==None:
            insert_cache_rep(conn,meta,file_data)
        
    if insertDB:
        insert_search(conn,meta,file_data)
    
    file_data['search_id'] = get_search_id(conn,meta,file_data)
    
    return ((file_data['name']+"_"+str(file_data['job_id'])+"."+file_data['file_type']),file_data)

def mzxmlParser(input,zlib,file_data): 
    
    #ifWritePeakFile = 0 if 'Xenopus' in file_data['name'] else 1
    
    exp_db_id = file_data['exp_db_id']
    f_num = file_data['f_num']
    r_num = file_data['r_num']
    file_name = file_data['name']
    search_id = file_data['search_id']
    
    print 'Start mzxmlParser:',time_now()
    try:
        mzxmlfile = ET.parse(input)
    except Exception, e:
        delete_search(conn,meta,search_id)
        stop_err('Error running mzxmlParser.\n%s\n' % (str(e)))
        
    root = mzxmlfile.getroot()
    msRun = root.find('{http://sashimi.sourceforge.net/schema_revision/mzXML_3.2}msRun')
    num_scan = msRun.get('scanCount')
    
    #flag = is_ms1_ms2(conn,meta,file_name,search_id)
    #print 'flag',flag
    ms2_list=[]
    ms_scanlist = []
    ins_ms1_list = []
    ins_ms2_list = []
    num_pep = 0
    parsed1 = 1
    parsed2 = 1
    i=0
    j=0
    digit = 0
    dir_peak = os.path.join(GALAXY_ROOT, 'database/files/ms_peak',     file_data['name'])
    dir_tmp  = os.path.join(GALAXY_ROOT, 'database/files/ms_peak_tmp', file_data['name'])
    
    MS1_txt_tmp = os.path.join(dir_tmp, 'MS1.txt')
    MS2_txt_tmp = os.path.join(dir_tmp, 'MS2.txt')
    
    MS1_txt = os.path.join(dir_peak, 'MS1.txt')
    MS2_txt = os.path.join(dir_peak, 'MS2.txt')
    #'%s/database/files/ms_peak_tmp/%s'%(GALAXY_ROOT, file_data['name'])
    
    if not os.path.exists(dir_peak): 
        os.makedirs(dir_peak)
          
    if not os.path.exists(dir_tmp): 
        os.makedirs(dir_tmp)
        
    fout_allMS1 = open(MS1_txt_tmp,'w')      
    fout_allMS2 = open(MS2_txt_tmp,'w')    
    for scan in msRun.findall('{http://sashimi.sourceforge.net/schema_revision/mzXML_3.2}scan'):
        num = scan.get('num')
        msLevel = scan.get('msLevel')
        rt = scan.get('retentionTime')
        rtTime = float(rt[2:-1])
        #rt_min = round(rtTime/60,3)
        peaks = scan.find('./{http://sashimi.sourceforge.net/schema_revision/mzXML_3.2}peaks')
        peak = peaks.text
        digit += 1
        #print 'peak %s: \n%s'%(digit,peak)
        precision = int(peaks.get('precision'))
        compress = peaks.get('compressionType')
        (mz,inten) = decode_spectrum(peak,precision,zlib,search_id)
        ###########  Write peaks into text files  ###########
        sum_int = 0.0
        
        fout_name     = os.path.join(dir_peak, '%s.txt'%num)
        fout_name_tmp = os.path.join(dir_tmp,  '%s.txt'%num)
        #=======================================================================
        # if ifWritePeakFile:
        #     fout = open(fout_name,'w') 
        #     for i in range(len(mz)):
        #         #if inten[i]==0.0:continue
        #         row = '%s,%s,%s\n'%(str(num),str(mz[i]),str(inten[i]))
        #         sum_int += inten[i]
        #         fout.write(row)
        #     fout.close()
        #=======================================================================
            #shutil.move(fout_name_tmp,fout_name)
         
        if msLevel == '1':
            for i in range(len(mz)):
                #if inten[i]==0.0:continue
                row = '%s,%s,%s\n'%(str(num),str(mz[i]),str(inten[i]))
                sum_int += inten[i]
                fout_allMS1.write(row)
                
            ms1 = num
            ins_ms1_list.append({'search_id':search_id,'scan_num':ms1,'rt':rtTime,'intensity':sum_int})
            
            i+=1
        #######################################################    
        elif msLevel == '2':
            for i in range(len(mz)):
                #if inten[i]==0.0:continue
                row = '%s,%s,%s\n'%(str(num),str(mz[i]),str(inten[i]))
                sum_int += inten[i]
                fout_allMS2.write(row)
            #mz = 0
            #intensity = 0
            #charge = 0
            ms2 = num
            preMz = scan.find('./{http://sashimi.sourceforge.net/schema_revision/mzXML_3.2}precursorMz')
            preScanNum = preMz.get('precursorScanNum')
            pre_mz = preMz.text
            ms2_list.append((ms2, preScanNum, pre_mz, rtTime))
            j+=1
    #print dir_tmp
    fout_allMS1.close()  
    fout_allMS2.close() 
    shutil.move(MS1_txt_tmp, MS1_txt)
    shutil.move(MS2_txt_tmp, MS2_txt)      
    #exit(0)
    rt_max = rtTime
    
    insertGeneral('gardener_ms1', ins_ms1_list)
    ins_ms1_list = []
    #insert_ms1(conn,meta,ins_ms1_list)
                
    for ms in ms2_list:
        ms1_id = get_ms1_id(conn,meta,ms[1],search_id)
        ins_ms2_list.append({'ms1_id':ms1_id, 'search_id':search_id, 'scan_num':ms[0], 'pre_mz':ms[2], 'rt':ms[3]})
    #===========================================================================
    #     """ Speed up DB writing,reduce memory cost """
    #     if (parsed2 % 1000) == 0:
    #         insert_ms2(conn,meta,ins_ms2_list)
    #         ins_ms2_list = []    
    #     parsed2 += 1                    
    # if len(ins_ms2_list) > 0:
    #     insert_ms2(conn,meta,ins_ms2_list)
    #===========================================================================
    
    insertGeneral('gardener_ms2', ins_ms2_list)
    ins_ms2_list = []
    #insert_ms2(conn,meta,ins_ms2_list)        
    print 'Mission over(write ms1 ms2)!',time_now()
        
    return num_scan,rt_max
    #print 'Number of MS 1  :',i
    #print 'Number of MS 2  :',j      
    """
    mzXML = MzXML()
    mzXML.parse_file(input)

    sys.stderr.write("Write ms1.txt ... ")
    f_out = open('ms1_small.txt','w')
    for tmp_ms1 in mzXML.MS1_list:
        f_out.write("Scan\t%06d\t%06d\n"%(tmp_ms1.id, tmp_ms1.id))
        f_out.write("RT\tRetTime\t%.2f\n"%(tmp_ms1.retention_time))
        for i in range(0,10):#len(tmp_ms1.mz_list)):
            f_out.write("%f\t%.2f\n"%(tmp_ms1.mz_list[i],tmp_ms1.intensity_list[i]))
    f_out.close()
    sys.stderr.write("Done\n")    
    """

def decode_spectrum(line,precision,bzlib,sid):
    if line == None:
        return [],[]
    
    decoded = base64.decodestring(line)
    
    decoded = zlib.decompress(decoded) if bzlib=='z' else decoded
    tmp_size = len(decoded)/8 if precision==64 else len(decoded)/4
    unpack_format1 = ">%dd" % tmp_size if precision==64 else ">%dL" % tmp_size 
    #print(unpack_format1)
    idx = 0
    mz_list = []
    intensity_list = []
    for tmp in struct.unpack(unpack_format1,decoded):
        tmp_i = struct.pack("d",tmp) if precision==64 else struct.pack("I",tmp)
        tmp_f = struct.unpack("d",tmp_i)[0] if precision==64 else struct.unpack("f",tmp_i)[0]
        if( idx % 2 == 0 ):
            mz_list.append( float(tmp_f) )
        else:
            intensity_list.append( float(tmp_f) )
        idx += 1
    '''
    except Exception, e:
        delete_search(conn, meta, sid)
        stop_err('Error decoding base64 peaks.\n%s\n' % (str(e)))
    '''        
    return (mz_list,intensity_list)
"""
def insert_ms1(conn,meta,inserts):
    ms1 = Table('gardener_ms1', meta, autoload=True, autoload_with=engine)
    ins = ms1.insert()
    result = conn.execution_options(autocommit=True).execute(ins, inserts) 
    return result

def insert_ms2(conn,meta,inserts):
    ms2 = Table('gardener_ms2', meta, autoload=True, autoload_with=engine)
    ins = ms2.insert()
    result = conn.execution_options(autocommit=True).execute(ins, inserts) 
    return result
"""
def update_search(conn, meta, file_data):
    search = Table('gardener_search',meta, autoload=True, autoload_with=engine)
    upd = search.update().where(search.c.id==file_data['search_id']).values({search.c.num_spectrum:file_data['num_spectrum'],
                                                                           search.c.stage:file_data['stage'],
                                                                           search.c.update_time:date_now(),
                                                                           search.c.rt_max:file_data['rt_max']})
    result = conn.execution_options(autocommit=True).execute(upd)
    return result

def update_experiment_spec(conn, meta, file_data):
    num_spec_exp = 0
    search = Table('gardener_search',meta, autoload=True, autoload_with=engine)
    exp = Table('gardener_experiment',meta, autoload=True, autoload_with=engine)
    s = select([search.c.num_spectrum]).where(and_(search.c.exp_id==file_data['exp_db_id'],search.c.rank==file_data['rank']))
    result = conn.execution_options(autocommit=True).execute(s)
    for row in result:
        num_spec_exp += row[search.c.num_spectrum]
    print 'num_spec_exp',num_spec_exp
    upd = exp.update().where(exp.c.id==file_data['exp_db_id']).values({exp.c.num_spectrum:num_spec_exp,
                                                                     exp.c.stage:file_data['stage']})
    result = conn.execution_options(autocommit=True).execute(upd)
    return result

#return whether it is OK to run the tool
def checkDatabase(input, fileformat, output, dbop_type):   
    try:
        rawfile = session.query(MSRunRawfile).filter(MSRunRawfile.filepath == input).first()
        if not rawfile:
            stop_err('Error adding records to ConvertedRawfile due to the lack of MSRunRawfile record. \n Please run "Store Experiment Data" first to store your data  into database.\n')
        rawfileID = rawfile.id
        #for the same raw file, each time running file converting, the output will be different 
        """
        convertedRawfile=session.query(ConvertedRawfile).filter(ConvertedRawfile.filepath==output).first()
        if convertedRawfile:
            session.delete(convertedRawfile)
        """
        #for each raw file, with respect to a particular type, store the latest file
        convertedRawfile = session.query(ConvertedRawfile).filter(and_(ConvertedRawfile.rawfileID == rawfileID, ConvertedRawfile.fileType == fileformat)).first()
        #if this convertedRawfile has no related record in DBSearchResult, then delete it
        if convertedRawfile is not None:
             #if a workflow based on tandem has been run, 
             #then after running a workflow based on mascot, 
             #all the record related with the first run will be deleted on cascade  
             #solution: the workflow should begin with DBSearch
             if dbop_type == 'update':       
                 session.delete(convertedRawfile)  
                 return (True, rawfileID)           
                 """
                 #all the following analysis use filepath as an uniq identifier to get primary id in the database,
                 #so only if the original converted file is disconnected from table convertedRawfile, 
                 #all the following analysis result originated from this file will of no meaning.
                 #since to trace along all tables for comparison, there should be only one converted file with a specific format
                 #so the most convenient way is to delete original records and insert again.
                 """
                 #convertedRawfile.filepath = output
                 #return
                #writePrompt(f,'true','false',eid)             
             elif dbop_type == 'delete':    
                 session.delete(convertedRawfile)
                 session.commit()
                 writePrompt(output)  
                 return (False, None)
             else: 
                errlist = []         
                errlist.append('This raw file has been converted to type %s.\n' % fileformat)
                errlist.append('If you want to convert this file to type %s again,\n' % fileformat) 
                errlist.append('please choose "update" in the drop-down box "Change the information of the result for this analysis in the database".\n')
                errlist.append('Or else the original information in the database will be kept.')
                #print err
                stop_err('Error adding records to DBSearchResult.\n%s\n' % ''.join(errlist))           
        else:
            #print 'experiment is None'
            #if isUpdate == 'true' or isDelete == 'true':
            if  dbop_type == 'delete':      
                err = 'There is no information about this analysis in the database.'
                #print err
                stop_err('Error changing information for ConvertedRawfile in the database.\n%s\n' % err) 
            #if experiment is None and user chose 'insert'
            return  (True, rawfileID)      
    except Exception, e:
        session.rollback()
        stop_err('Error checking records in ConvertedRawfile.\n%s\n' % (str(e)))
    
#rawfileID, fileType, filepath          
def storeConvertedRawfile(rawfileID, fileformat, output):                
    try:
        convertedRawfile = ConvertedRawfile(rawfileID, fileformat, output)
        session.add(convertedRawfile)
        session.commit()
    except Exception, e:
        session.rollback()
        stop_err('Error adding records to ConvertedRawfile.\n%s\n' % (str(e)))


def runTool(cmd,sid):
    try:
        #
        # Run command.
        #
        print cmd,'\nsid:',sid
        print 'Start convert =',time_now()
        tmp_name = tempfile.NamedTemporaryFile(dir=".").name
        tmp_stderr = open(tmp_name, 'wb')
        #test = shlex.split(cmd)
        #print test
        proc = subprocess.Popen(args=cmd, shell=True, stderr=tmp_stderr.fileno())
        returncode = proc.wait()
        tmp_stderr.close()
        
        print 'Over convert =',time_now()
        # Error checking.
        if returncode != 0:
            delete_search(conn,meta,sid)
            
            raise Exception, "my return code = %i" % returncode
        #else:
        #it may be too late to check for records in database after finish running the tool
        #mzXML or mzML
       
        return returncode
        
    except Exception, e:
        
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
        stop_err('Error running msconvert(raw).\n%s\n' % (str(e)))

def getCmd():
     # Parse Command Line
    parser = optparse.OptionParser()
    parser.add_option('-i', '--input', dest='input', action='store', type="string", help='MS run raw file.')
    """ parser.add_option( '-f', '--fractionNo', dest='fractionNo', action='store', type="int", help='Fraction No.' )
    parser.add_option( '-r', '--replicatNo', dest='replicatNo', action='store', type="int", help='Replicate No.' )
    parser.add_option( '-p', '--phValue', dest='phValue', action='store', type="float", help='PH Value.' )
    parser.add_option( '-v', '--volumn', dest='volumn', action='store', type="float", help='"Volume(ml).')
    """
    parser.add_option('-b', '--binary', dest='binary', action='store', type="string", help='MS run converted file precision.')
    parser.add_option('-x', '--index', dest='index', action='store', type="string", help='MS run converted file with index')
    parser.add_option('-z', '--zlib', dest='zlib', action='store', type="string", help='MS run converted file with index')
    parser.add_option('-g', '--gzip', dest='gzip', action='store', type="string", help='MS run converted file with index')
    parser.add_option('-f', '--filter', dest='filter', action='store', type="string", help='MS run converted file with index')
    parser.add_option('-v', '--vendor', dest='vendor', action='store', type="string", help='MS run converted file with index')
    parser.add_option('-l', '--llevel', dest='llevel', action='store', type="int", help='MS run converted file with index')
    parser.add_option('', '--hlevel', dest='hlevel', action='store', type="int", help='MS run converted file with index')
    parser.add_option('-r', '--rmPrecur', dest='rmPrecur', action='store', type="string", help='MS run converted file with index')
    parser.add_option('-c', '--rmCharge', dest='rmCharge', action='store', type="string", help='MS run converted file with index')
    parser.add_option('-n', '--rmNeutr', dest='rmNeutr', action='store', type="string", help='MS run converted file with index')
    parser.add_option('-k', '--rmBlanket', dest='rmBlanket', action='store', type="string", help='MS run converted file with index')
    parser.add_option('', '--outformat', dest='outformat', action='store', type="string", help='MS run converted file format.')
    parser.add_option('-o', '--output', dest='output', action='store', type="string", help='MS run converted file.')
    #parser.add_option('', '--dbop_type', dest='dbop_type', action='store', help='')
    parser.add_option('', '--store_to_db', dest='store_to_db', action='store', help='')
    parser.add_option('-j', '--job_track_id', dest='job_track_id', action='store', type="string", help='Job track ID for firmiana.')
    parser.add_option('-u', '--user_id', dest='user_id', action='store', type="string", help='User id for galaxy runner.')
    parser.add_option('-a', '--label_name', dest='label_name', action='store', type="string", help='Label name for out file.')
    (options, args) = parser.parse_args()
    #print options.outformat,options.store_to_db,options.user_id,options.label_name
    #exit(0)   # wine /usr/local/tpp/pwiz/msconvert.exe $input --mzXML -o - > $output
    # -f [ --filelist ] arg    : specify text file containing filenames   
    cmd = "wine %s/msconvert.exe %s" % (pwz, options.input)

    # Add options.
    if cmp(options.outformat, 'mzXML') == 0:
        cmd += " --mzXML"
    if cmp(options.outformat, 'mzML') == 0:
        cmd += " --mzML"
    """
    # now only support mzXML and mzML
    if cmp(options.outformat,'mz5')==0:
        cmd += " --mz5"
    if cmp(options.outformat,'mgf')==0:
        cmd += " --mgf"
    if cmp(options.outformat,'text')==0:
        cmd += " --text"
    if cmp(options.outformat,'ms1')==0:
        cmd += " --ms1"
    if cmp(options.outformat,'cms1')==0:
        cmd += " --cms1"
    if cmp(options.outformat,'ms2')==0:
        cmd += " --ms2"
    if cmp(options.outformat,'cms2')==0:
        cmd += " --cms2"
    """
    if cmp(options.binary, '32') == 0:    
        cmd += " --32"
    #if cmp(options.binary,'64')==0:        #default
        #cmd +=" --mz64 --inten64"
    if cmp(options.index, 'noindex') == 0:
        cmd += ' --noindex'
    if cmp(options.zlib, 'z') == 0:
        cmd += ' -z'
    if cmp(options.gzip, 'g') == 0:
        cmd += ' -g'
    if cmp(options.filter, 'peakPicking') == 0:
        cmd += ' --filter '
        if (options.vendor == True):
            cmd += ' "peakPicking true'
        else :
            cmd += ' "peakPicking false'
        cmd += ' %d-%d"' % (options.llevel, options.hlevel)
    elif cmp(options.filter, 'ETDFilter') == 0:
        cmd += ' --filter ETDFilter'
        cmd += ' ' + str(options.rmPrecur).lower() + ' ' + str(options.rmCharge).lower() + ' ' + str(options.rmNeutr).lower() + ' ' + str(options.rmBlanket).lower()
  
    #By default, the name of output file is the same as the input file, with different suffix, such as '.mzXML' 
    type = '.' + options.outformat
    
    if options.input.endswith('.dat'):
        converted_filename = options.input.replace('.dat', type) 
    elif options.input.endswith('.raw'):
        converted_filename = options.input.replace('.raw', type) 
    else:
        converted_filename = options.input.replace('.wiff', type)
    #to avoid creating a directory named -
    #cmd += " -o - > "
    #cmd += options.output   
    cmd += ' -o /tmp' #+ os.path.dirname(options.input)
    """   
    #link creating will fail if options.output has already existed.
    if os.path.exists(options.output):
        cmd += "; wait; rm "+options.output
        cmd += "; wait; ln -s "+ outfilename+' '+options.output
    """
    #x=os.path.splitext(options.input)[0].split("dataset_")[2]
    #cmd += '; wait; mv ' + converted_filename + ' ' + options.output
    cmd += '; wait; mv ' + '/tmp/' + os.path.basename(converted_filename) + ' ' + options.output
    # Debugging.
    return (cmd, options, args)        

def storeDB(conn,meta,file_data,options):
    #file_data['date'] = date_now()#time.strftime("%Y-%m-%d %X", time.gmtime())
    file_data['size'] = str(os.path.getsize(options.output)/1024)+'K'
    update_file(conn,meta,file_data)
    
    #file_data['date'] = date_now()#time.strftime("%Y-%m-%d %X", time.gmtime())
    update_search(conn, meta, file_data)
    
    sid = get_cache_rep_sid(conn,meta,file_data)
    update_rep_stage(conn, meta, file_data,sid)
    
    updateExpStage(conn,meta,file_data)
    
def __main__():  
    (cmd, options, args) = getCmd() 
    """
        If there are already records in database, it is not necessary to run the tools,
        just check the option user chose.
        case insert: error without running the tool
        case update: delete and insert again and run the tool
        case delete: delele without running the tool
        If there is no record in database, 
        should still firstly check the option user chose.
        case insert: insert with running the tool
        case update: error without running the tool
        case delete: error without running the tool 
        
        In a word, running the tool and store record to db is about the same time,
        in other cases, there is no need to store record to db and run the tool.
        So if the tool run is success, then store record to db.      
    """  
    #print 'dbSwitch:', options.store_to_db
    #print 'CWD:', os.getcwd()
    if not os.path.isfile(options.input):
        print 'input error,nfs may disconnected'
        exit(1)
    if options.store_to_db=='yes':  
        (storename,file_data)=sql_gardener_file(options,conn,meta)
        #cmd += '; wait; cp ' + options.output + ' ' + store_file_path+"/" +storename
        
        
        
        runTool(cmd,file_data['search_id'])
        (file_data['num_spectrum'],file_data['rt_max']) = mzxmlParser(options.output,options.zlib,file_data)
    
        storeDB(conn,meta,file_data,options)
            #print file_data['num_spectrum'],file_data['num_peptide']
    else:
        runTool(cmd,0)
    
if __name__ == "__main__": __main__()
