#!/usr/bin/env python
import sys, optparse, os, tempfile, subprocess, shutil, re,math,shlex
import zlib,base64,struct

ms_tools_path = os.path.join( os.path.dirname( __file__ ), '..')
GALAXY_ROOT = os.path.join( ms_tools_path, '..', '..' )

sys.path.insert(1, ms_tools_path)
from models.gardener_control import *

def stop_err(msg, ret=1):
    sys.stderr.write(msg)
    sys.exit(ret)

def update_search(conn, meta, file_data):
    search=Table('gardener_search',meta, autoload=True, autoload_with=engine)
    upd=search.update().where(search.c.id==file_data['search_id']).values({search.c.num_spectrum:file_data['num_spectrum'],
                                                                           search.c.stage:file_data['stage'],
                                                                           search.c.update_time:date_now(),
                                                                           search.c.rt_max:file_data['rt_max']})
    result=conn.execute(upd)
    return result

def update_experiment_spec(conn, meta, file_data):
    num_spec_exp = 0
    search=Table('gardener_search',meta, autoload=True, autoload_with=engine)
    exp=Table('gardener_experiment',meta, autoload=True, autoload_with=engine)
    s = select([search.c.num_spectrum]).where(and_(search.c.exp_id==file_data['exp_db_id'],search.c.rank==file_data['rank']))
    result = conn.execute(s)
    for row in result:
        num_spec_exp+=row[search.c.num_spectrum]
    print 'num_spec_exp',num_spec_exp
    upd=exp.update().where(exp.c.id==file_data['exp_db_id']).values({exp.c.num_spectrum:num_spec_exp,
                                                                     exp.c.stage:file_data['stage']})
    result=conn.execute(upd)
    return result

def mzxmlChecker(input):
    position = 0
    with open(input) as f:
        first = f.readline()
        i = 1
        while 1:
            line = f.readline()
            if not line:break
            if line == first:position=i
            i+=1
    return position


def index_mzXML(filename):
    print 'Write mzXML again...',str(datetime.datetime.now().strftime('%X'))
    
    mzxmlfile = ET.parse(filename)
    ''' Index problem '''
    mzxmlfile.write(filename, encoding="ISO-8859-1",xml_declaration=True)
    mzxmlfile = ET.parse(filename)
    
    root = mzxmlfile.getroot()
    
    offset_List = []
    offsetStart = 0
    offsetValue = 0
    with open(filename,'r') as f:
        for line in f:
            if '<scan ' in line:
                delta = line.index('<scan ')
                tmp = offsetValue + delta
                offset_List.append(tmp)
            elif '<index ' in line:
                delta = line.index('<index ')
                offsetStart = offsetValue + delta
                
            offsetValue += len(line)
            
    index = root.find('{http://sashimi.sourceforge.net/schema_revision/mzXML_3.2}index')
 
    i = 0
    for child in index.getchildren():
        child.text = str(offset_List[i])
        i += 1
            
    indexOffset = root.find('{http://sashimi.sourceforge.net/schema_revision/mzXML_3.2}indexOffset')
    indexOffset.text = str(offsetStart)

    mzxmlfile.write(filename, encoding="ISO-8859-1",xml_declaration=True)
                
def mzxmlParser(input, output, file_data): 
    exp_db_id = file_data['exp_db_id']
    f_num = file_data['f_num']
    r_num = file_data['r_num']
    file_name = file_data['name']
    search_id = file_data['search_id']
    """ Some wiff file contains more than one fraction due to mistake of experimenter"""
    position = mzxmlChecker(input)
    if position != 0:
        input_part = input + '_part'
        with open(input_part, 'w') as fout:
            with open(input, 'r') as f:
                part = f.readlines()[position:]
                for l in part:
                    fout.write(l)
        """ Correct index offset """ 
        index_mzXML(input_part)
        input = input_part
    #Copy mzxml to output file for next tool Mzxml2mgf
    shutil.copy(input, output)
            
    print 'Start(write ms1 ms2)!',str(datetime.datetime.now().strftime('%X'))  
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
    ms1_list=[]
    ms2_list=[]
    ms_scanlist = []
    ins_ms1_list = []
    ins_ms2_list = []
    num_pep = 0
    parsed1 = 1
    parsed2 = 1
    i = 0
    j = 0
    
    dir     = '%s/database/files/ms_peak/%s'%(GALAXY_ROOT, file_data['name'])
    dir_tmp = '%s/database/files/ms_peak_tmp/%s'%(GALAXY_ROOT, file_data['name'])
    
    if not os.path.exists(dir): 
        os.makedirs(dir)
          
    if not os.path.exists(dir_tmp): 
        os.makedirs(dir_tmp)
        
    MS1_txt_tmp = os.path.join(dir_tmp, 'MS1.txt')
    MS2_txt_tmp = os.path.join(dir_tmp, 'MS2.txt')
    
    MS1_txt = os.path.join(dir, 'MS1.txt')
    MS2_txt = os.path.join(dir, 'MS2.txt')
    
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
        precision = int(peaks.get('precision'))
        compress = peaks.get('compressionType')
        ###########  Write peaks into text files  ###########
        sum_int = 0.0
        fout_name = '%s/%s.txt'%(dir,num)
        fout_name_tmp = '%s/%s.txt'%(dir_tmp,num)
        fout = open(fout_name_tmp,'w')
        #ms_scanlist.append((num,fout_name))
        (mz,inten) = decode_spectrum(peak,compress,precision)
        #print(str(len(mz))+","+str(len(inten))+"\n\n")
        #=======================================================================
        # for i in range(len(mz)):
        #     #if inten[i]==0.0:continue
        #     row = '%s,%s,%s\n'%(str(num),str(mz[i]),str(inten[i]))
        #     sum_int += inten[i]
        #     if msLevel == '1':fout_allMS1.write(row)
        #     fout.write(row)
        # fout.close()
        # shutil.move(fout_name_tmp,fout_name)
        #=======================================================================
        
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
                
            ms2 = num
            preMz = scan.find('./{http://sashimi.sourceforge.net/schema_revision/mzXML_3.2}precursorMz')
            preScanNum = ms1#preMz.get('precursorScanNum')
            pre_mz = preMz.text
            ms2_list.append((ms2, preScanNum, pre_mz, rtTime))
            j+=1

    fout_allMS1.close()  
    fout_allMS2.close() 
    shutil.move(MS1_txt_tmp, MS1_txt)
    shutil.move(MS2_txt_tmp, MS2_txt)   
          
    rt_max = rtTime
    insertGeneral('gardener_ms1', ins_ms1_list)
    ins_ms1_list = []
    #insert_ms1(conn,meta,ins_ms1_list)
                
    for ms in ms2_list:
        ms1_id = get_ms1_id(conn,meta,ms[1],search_id)
        ins_ms2_list.append({'ms1_id':ms1_id,'search_id':search_id,'scan_num':ms[0],'pre_mz':ms[2],'rt':ms[3]})
    #===========================================================================
    #     """ Speed up DB writing """
    #     if (parsed2 % 1000) == 0:
    #         insert_ms2(conn,meta,ins_ms2_list)
    #         ins_ms2_list = []    
    #     parsed2 += 1                    
    # if len(ins_ms2_list) > 0:
    #     insert_ms2(conn,meta,ins_ms2_list)    
    #===========================================================================
    insertGeneral('gardener_ms2', ins_ms2_list)
    #insert_ms2(conn,meta,ins_ms2_list)
    print 'Mission over(write ms1 ms2)!',str(datetime.datetime.now().strftime('%X'))
        
    return num_scan,rt_max

def decode_spectrum(line,compress,precision):
    if line ==None:
        return [],[]
    decoded = base64.decodestring(line)
    decoded = zlib.decompress(decoded) if compress!='none' else decoded
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
        
    return mz_list,intensity_list

def sql_gardener_file(options,conn,meta):
    rank = options.rank
    file_data={}
    #file_data['job_id']=getJobId(conn,meta,options.job_track_id,options.user_id)
    cwd=os.getcwd()
    file_data['job_id']=getJobId(cwd)
    #options.label_name = 'CNHPP_HUVEC_DMSO_300ug_RP_17-22_3_E80574_F3_R3.raw'
    exp=get_exp_info("("+options.label_name+")")
    if exp['state']==1 :#and file_data['job_id']!=-1:
        file_data['name']  = exp['name']
        file_data['exp_id']= exp['exp_id']
        file_data['f_num'] = exp['nf']
        file_data['r_num'] = exp['nr']    
    else:
        stop_err('Error in file naming, please verify your file name before run reference pipeline.\n' )
    e_name = 'Exp' + file_data['exp_id']
    file_data['exp_db_id'] = get_exp_id(conn,meta,e_name)#ID of exp table!!!
    file_data['file_type'] = 'mzxml'
    file_data['type'] ='reference'
    file_data['path'] = options.output
    file_data['size'] = str(os.path.getsize(options.input)/1024)+'K'
    file_data['user'] = get_user_name(conn,meta,options.user_id)
    file_data['rank'],insertDB = isNewSearch(conn,meta,file_data)  #get_rank(conn,meta,file_data)
    file_data['date'] = date_now()#time.strftime("%Y-%m-%d %X", time.gmtime())
    '''
    print 'rank:',file_data['rank']
    if rank!=0:
        print 'rank = :',rank
        if rank > file_data['rank']:
            stop_err('Wrong rank number input.\n' )
        file_data['rank']  = rank
    '''
    insert_file(conn,meta,file_data)
    
    file_data['stage'] = 2
    file_data['log'] = 'Insert Successfully.'
    (f, r) = get_file_num(conn,meta,file_data['exp_db_id'])
    file_data['file_num'] = f * r
    
    if get_cache_exp_sid(conn,meta,file_data)==None:
        insert_cache_exp(conn,meta,file_data)
    
    if get_cache_rep_sid(conn,meta,file_data)==None:
        insert_cache_rep(conn,meta,file_data)
        
    if insertDB:
        insert_search(conn,meta,file_data)
    
    file_data['search_id'] = get_search_id(conn,meta,file_data)               
    return file_data

def storeDB(conn,meta,file_data,options):
    
    file_data['date'] = date_now()#time.strftime("%Y-%m-%d %X", time.gmtime())
    update_search(conn, meta, file_data)
    
    sid = get_cache_rep_sid(conn,meta,file_data)
    update_rep_stage(conn, meta, file_data,sid)
    
    updateExpStage(conn,meta,file_data)
    
    #cmd = 'cp '+ options.input + ' '+ options.output
    #runTool(cmd,file_data['search_id'])
    
def runTool(cmd,sid):
    try:
        print cmd,sid
        tmp_name = tempfile.NamedTemporaryFile(dir=".").name
        tmp_stderr = open(tmp_name, 'wb')
        #test = shlex.split(cmd)
        #print test
        proc = subprocess.Popen(args=cmd, shell=True, stderr=tmp_stderr.fileno())
        returncode = proc.wait()
        tmp_stderr.close()
        # Error checking.
        if returncode != 0:
            s = text('delete from gardener_search where id=%s'%sid)
            conn.execute(s)
            raise Exception, "return code = %i" % returncode
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
                
def __main__() :
     
    parser = optparse.OptionParser()
    parser.add_option('-i', '', dest='input', help=' ')
    parser.add_option('-o', '', dest='output', help='')
    parser.add_option('-u', '--user_id', dest='user_id', action='store', type="string", help='User id for galaxy runner.')
    parser.add_option('-a', '--label_name', dest='label_name', action='store', type="string", help='Label name for out file.')
    parser.add_option('', '--rank', dest='rank', action='store', type="int", help='Specify the rank.')
    (options, args) = parser.parse_args()
    print 'Processing mzxml:\n',options.input
    
    file_data = sql_gardener_file(options,conn,meta)
    
    (file_data['num_spectrum'],file_data['rt_max'])= mzxmlParser(options.input,options.output,file_data)
    
#     cp_to = os.path.join(GALAXY_ROOT,'database/files/mascot_result', 'Exp%s'%file_data['exp_id'],file_data['name'])
#     cp_to_file = os.path.join(cp_to, os.path.basename(options.input).replace('.dat','.mzXML'))
#     if not os.path.isdir(cp_to):
#         os.makedirs(cp_to)
#     shutil.copy(options.input, cp_to_file) 
    
    storeDB(conn,meta,file_data,options)
    
              
if __name__ == "__main__": __main__()
