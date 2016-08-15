#!/usr/bin/env python
import msparser
import sys, optparse, os, tempfile, subprocess, shutil, re, math
import gc
from numpy import array, repeat, concatenate, ones, zeros, arange, reshape, put, add, dot, take, float32
from numpy.linalg import pinv
from scipy.signal.signaltools import lfilter
import numpy as np
import numpy

ms_tools_path = os.path.join( os.path.dirname( __file__ ), '..')
GALAXY_ROOT = os.path.join( ms_tools_path, '..', '..' )

sys.path.insert(1, ms_tools_path)
from models.gardener_control import *
from models.firmiana_sendmail import *
from config.firmianaConfig import *
#from models.firmiana_pepArea import *
#from models.firmiana_proAssemble import *
#from models.mascot_percolator import *

H_PLUS = 1.007276466#1.007825
LIPENG = 116
ANNO_STATUS = ['co_0','ki_0','li_0','re_0','pmm_0','pmh_0','tf_0','gbindxenopus_0']
MOD_ABBREV = ['Acetyl_','Methyl_','GlyGly_','Biotin_','PhosphoST_','PhosphoY_','#_','#_']
MOD_NAME = ['Acetyl','Methyl','GlyGly','Biotin','Phospho (ST)','Phospho (Y)','#','#']
LEN_MOD_NAME = len(MOD_NAME)
ANNOTATION = ','.join(ANNO_STATUS)
'''
Mono-isotopic mass, http://61.50.134.137/mascot/help/aa_help.html
'''
dict_aa_mass = {'A':71.037, 'B':114.535, 'C':103.009, 'D':115.027, 'E':129.043, 'F':147.068,
                    'G':57.021, 'H':137.059, 'I':113.084, 'J':113.084, 'K':128.095, 'L':113.084,
                    'M':131.040, 'N':114.043, 'O':237.148, 'P':97.053, 'Q':128.059, 'R':156.101,
                    'S':87.032, 'T':101.048, 'U':150.954, 'V':99.068, 'W':186.079, 'X':111.0,
                    'Y':163.063, 'Z':128.551}

WAIT_TIMES = 360

def stop_err(msg, ret=1):
    sys.stderr.write(msg)
    sys.exit(ret)

def update_time_used(conn, meta, sid, file_data):
    filename = 'F%s_R%s' %(file_data['f_num'], file_data['r_num'])
    search_id = file_data['search_id']
    t = "select parameter from gardener_search where id=%s" % search_id
    
    param = conn.execution_options(autocommit=True).execute(t).scalar()
    db = 'default'
    if param != None:
        tmp = re.search(r'DB=([^\,]+)\,', param)
        if tmp != None:
            db = tmp.group(1)
            
    t = 'select create_time from gardener_search where id=%s' % sid
    d_create = conn.execution_options(autocommit=True).execute(t).scalar()
    #t = 'select update_time from gardener_search where id=%s' % sid
    #d_update = conn.execution_options(autocommit=True).execute(t).scalar()
    d_update = date_now()
    
    d1 = str(d_create.strftime('%Y-%m-%d %X'))  
    #d2 = str(d_update.strftime('%Y-%m-%d %X')) 
    d2 = d_update
    d_create = time.mktime(time.strptime(d1, '%Y-%m-%d %H:%M:%S'))
    d_update = time.mktime(time.strptime(d2, '%Y-%m-%d %H:%M:%S'))
    delta = d_update - d_create
    hh = round(delta / 3600.0, 2)
    log_time = 'DB:%s/%s hours used. Last file is [%s]' % (db, hh, filename)
        
    sea = Table('gardener_search', meta, autoload=True, autoload_with=engine)    
    upd = sea.update().where(sea.c.id == sid).values({sea.c.log:log_time})
    conn.execution_options(autocommit=True).execute(upd)
    return hh
    
def outputfile(exp, Title):
    peptide = Peptide.objects.filter(search_id=exp)
    name = Search.objects.get(id=exp).name
    filename = '/usr/local/galaxyDATA01/galaxy-dist/database/files/IspecFiles/' + name + '.tab'
    if os.path.exists(filename):
        return filename
    f = open(filename, 'w')
    for title in Title:
        f.write('\t' + title)
    f.write('\n')
    for pep in peptide:
        f.write('NULL' + '\t')  # Confidence Level
        f.write('NULL' + 't')  # Search ID
        f.write('NULL' + '\t')  # Processing Node No
        f.write(pep.sequence + '\t')  # Sequence
        f.write('NULL' + '\t')  # Unique Sequence ID
        f.write('NULL' + '\t')  # PSM Ambiguity
        f.write('Protein Descriptions' + '\t')  # Protein Descriptions
        f.write('# Proteins' + '\t')  # Proteins
        f.write('# Protein Groups' + '\t')  # Protein Groups
        f.write(pep.protein_group_accessions + '\t')  # Protein Group Accessions
        f.write(pep.modification + '\t')  # Modifications
        f.write('Activation Type' + '\t')  # Activation Type
        f.write('DeltaScore' + '\t')  # DeltaScore
        f.write(str(pep.delta_cn) + '\t')  # DeltaCn
        f.write('Rank' + '\t')  # Rank
        f.write('Search Engine Rank' + '\t')  # Search Engine Rank
        f.write(str(pep.area) + '\t')  # Precursor Area
        f.write(str(pep.q_value) + '\t')  # q_value
        f.write(str(pep.pep) + '\t')  # pep
        f.write('Decoy Peptides Matched' + '\t')  # Decoy Peptides Matched
        f.write(str(pep.exp_value) + '\t')  # exp_value
        f.write('Homology Threshold' + '\t')  # Homology Threshold
        f.write('Identity High' + '\t')  # Identity High
        f.write('Identity Middle' + '\t')  # Identity Middle
        f.write(str(pep.ion_score) + '\t')  # ion_score
        f.write('Peptides Matched' + '\t')  # Peptides Matched
        f.write(str(pep.num_missed_cleavages) + '\t')  # Missed Cleavages
        f.write('Ion Inject Time _ms_' + '\t')  # Ion Inject Time _ms_
        f.write(str(pep.ms2.ms1.intensity) + '\t')  # Intensity
        f.write(str(pep.charge) + '\t')  # charge
        f.write(str(pep.ms2.pre_mz) + '\t')  # m_z _Da_
        f.write(str(pep.mh_da) + '\t')  # mh_da
        f.write('Delta Mass _Da_' + '\t')  # Delta Mass _Da_
        f.write(str(pep.delta_m_ppm) + '\t')  # delta_m_ppm
        f.write(str(pep.rt_min) + '\t')  # rt_min
        f.write('First Scan' + '\t')  # First Scan
        f.write('Last Scan' + '\t')  # Last Scan
        f.write('MS2' + '\t')  # MS Order
        f.write('Ions Matched' + '\t')  # Ions Matched
        f.write('Matched Ions' + '\t')  # Matched Ions
        f.write('Total Ions' + '\t')  # Total Ions
        f.write(name + '\t')  # Spectrum File
        f.write('' + '\n')  # anntotation
    f.close()
    return filename
    
def getMaxRepeat(conn, meta, eid):
    e = Table('gardener_experiment', meta, autoload=True, autoload_with=engine)
    s = select([e.c.num_repeat]).where(e.c.id == eid)
    result = conn.execution_options(autocommit=True).execute(s).scalar()
    return result

def getRepSpecNum(conn, meta, file_data):
    eid = file_data['exp_db_id']
    rank = file_data['rank']
    rid = file_data['r_num']
    x = Table('gardener_search', meta, autoload=True, autoload_with=engine)
    s = select([func.sum(x.c.num_spectrum)]).where(and_(x.c.exp_id == eid, x.c.repeat_id == rid, x.c.rank == rank, x.c.type == 'fraction'))
    sum = conn.execution_options(autocommit=True).execute(s).scalar()
    return sum  # ,num_pep, num_pro, num_gen

def getExpSpecNum(conn, meta, eid):
    x = Table('gardener_search', meta, autoload=True, autoload_with=engine)
    s = select([func.sum(x.c.num_spectrum)]).where(and_(x.c.exp_id == eid, x.c.type == 'fraction'))
    sum = conn.execution_options(autocommit=True).execute(s).scalar()
    return sum
        
def get_obj_MS1(conn, meta, sid, gt, lt):
    db = Table('gardener_ms1', meta, autoload=True, autoload_with=engine)
    mm = select([db.c.scan_num, db.c.rt, db.c.id]).where(and_(db.c.search_id == sid, db.c.rt < lt, db.c.rt > gt))
    result = conn.execution_options(autocommit=True).execute(mm)
    return result

def get_mz_rt(conn, meta, ms2_id):
    db = Table('gardener_ms2', meta, autoload=True, autoload_with=engine)
    mz, rt = conn.execution_options(autocommit=True).execute(select([db.c.pre_mz, db.c.rt]).where(db.c.id == ms2_id)).fetchone()
    # mz = conn.execution_options(autocommit=True).execute('select pre_mz from gardener_ms2 where id=%s'%ms2_id).scalar()
    if mz == None or rt == None:
        return 0,0
    return mz, rt

def update_search_fraction(conn, meta, file_data):
    sid = file_data['search_id']
    search = Table('gardener_search', meta, autoload=True, autoload_with=engine)
    
    t1 = ("select count(DISTINCT sequence) from gardener_peptide where search_id=%s and type=1" % sid)
    num_pep = conn.execution_options(autocommit=True).execute(t1).scalar()
    
    t2 = ("select count(DISTINCT accession) from gardener_protein where search_id=%s and type=1" % sid)
    num_iso = conn.execution_options(autocommit=True).execute(t2).scalar()
    
    t3 = ('select count(DISTINCT gene_id) from gardener_gene where search_id=%s and type=1' % sid)
    num_gene = conn.execution_options(autocommit=True).execute(t3).scalar()
    
    upd = search.update().where(search.c.id == sid).values({search.c.num_gene:num_gene,
                                                        search.c.num_peptide:num_pep,
                                                        search.c.num_isoform:num_iso,
                                                        search.c.stage:file_data['stage'],
                                                        search.c.update_time:file_data['date']})
    result = conn.execution_options(autocommit=True).execute(upd)
    return result

def mean_movement(input_data, window):
    if window % 2 != 1:
        raise Exception, "'mean_movement' function needs an odd window length"
    if window > (len(input_data)) + 2:
        raise Exception, "'mean_movement' function: input data too short"
    input_data = list(input_data)
    output_data = []
    length = len(input_data)
    n = (window - 1) / 2
    input_data2 = ([input_data[0]] * n) + list(input_data) + ([input_data[length - 1]] * (n + 1))
    _sum = 0.0
    for i in xrange(0, window):
        _sum += input_data2[i]
    w = float(window)
    for i in xrange(n, n + length):
        output_data.append(_sum / window)
        _sum -= input_data2[i - n]
        _sum += input_data2[i + n + 1]
    return output_data

def _mean_movement_only_python(data, m):
    if m > (2 * len(data)) + 2:
        return data
    input_array = list(data)
    output_array = list(data)
    mean_factor = (2 * m) + 1
    length = len(data)
    # Process data from the middle
    for i in xrange(m, length - m):
        _sum = 0
        for j in xrange(i - m, i + m):
            _sum += input_array[j]
        output_array[i] = _sum / mean_factor
    # Process data from the beginning
    window = 1
    for i in xrange(1, m):
        _sum = 0
        for j in xrange(i - window, i + window):
            _sum += input_array[j]
        output_array[i] = _sum / ((2 * window) + 1)
        window += 1
    output_array[0] = input_array[0]
        # Process data from the end
    window = 1
    for i in reversed(xrange(length - m, length - 1)):
        _sum = 0
        for j in xrange(i - window, i + window):
            _sum += input_array[j]
        output_array[i] = _sum / ((2 * window) + 1)
        window += 1
    output_array[length - 1] = input_array[length - 1]
    del input_array
    return output_array

def sgolay(p, n):
    if n % 2 != 1:
        raise Exception, "'sgolay' function needs an odd filter length n"
    elif p >= n:
        raise Exception, "'sgolay' function needs filter length n larger than polynomial order p"
    k = int(n / 2)
    F = zeros((n, n), float32)
    for row in range(1, k + 2):
        # A = pinv( ( [(1:n)-row]'*ones(1,p+1) ) .^ ( ones(n,1)*[0:p] ) );
        left = dot(reshape(arange(1, n + 1) - row, (-1, 1)), ones((1, p + 1)))
        right = repeat([range(0, p + 1)], n, 0)
        # A = generalized_inverse( left**right )
        A = pinv(left ** right)                
        # F(row,:) = A(1,:); 
        put(F.ravel(), add(arange(n), n * (row - 1)), A[0])
        
        # F(k+2:n,:) = F(k:-1:1,n:-1:1);
    for fila in range(k + 1, n):
        put (F.ravel(), add(arange(n), n * fila), F[n - 1 - fila][::-1])
    return F
    
def sgolayfilt(x, p, n):
    x = array(x, float32).ravel()   
    size = len(x)
    if size < n:
        raise Exception, "'sgolayfilt': insufficient data for filter"
    # # The first k rows of F are used to filter the first k points
    # # of the data set based on the first n points of the data set.
    # # The last k rows of F are used to filter the last k points
    # # of the data set based on the last n points of the dataset.
    # # The remaining data is filtered using the central row of F.
    F = sgolay(p, n)
    k = int(n / 2)
    # z = filter(F(k+1,:), 1, x);
    z = lfilter(F[k], 1, x)
    # y = [ F(1:k,:)*x(1:n,:) ; z(n:len,:) ; F(k+2:n,:)*x(len-n+1:len,:) ];    
    left = dot(take(F, arange(k), 0), take(x, arange(n), 0))  
    right = dot(take(F, arange(k + 1, n), 0), take(x, arange(size - n, size), 0))
    middle = take(z, arange(n - 1, size))
    return concatenate((left, middle, right))
    
def divfind(a, b):
    head = 0
    tail = len(a) - 1
    while head <= tail:
        mid = (head + tail) / 2
        if a[mid][1] < b:
            head = mid + 1
        else:
            tail = mid - 1
    return head

def calcAreas(file_data, options, dRT, dMZ, ins_pep):
    print 'Start(calculating areas)Reading txt......', time_now()
    # RtList = []
    result = []
    sid = file_data['search_id']
    DataBase = []
    filename = file_data['name']
    dir = '%s/database/files/ms_peak/%s/' % (GALAXY_ROOT, filename)  # Dir of .txt files of peaks
    dir_MS1 = '%s/database/files/ms_peak_tmp/%s/MS1.txt' % (GALAXY_ROOT, filename)  # Dir of .txt files of peaks
    #files = os.listdir(dir)
    filedict = {}
    i = -1
    ms_no_old = 0
    file_lines = []
    #fileLength = len(files)
    if os.path.isfile(dir_MS1):
        MS1_file = open(dir_MS1, 'r')
        for line in MS1_file:
            (ms_no, mz_temp, intensity_temp) = line.split(',')
            ms_no, mz_temp, intensity_temp = int(ms_no), float(mz_temp), float(intensity_temp)
            if ms_no != ms_no_old :
                i += 1
                filedict[ms_no] = i  # Record the order of every ms1 txt file appeared
                if i != 0:
                    DataBase.append(file_lines)
                    file_lines = []
            tmp_line = (ms_no, mz_temp, intensity_temp)
            file_lines.append(tmp_line)
            ms_no_old = ms_no
        MS1_file.close()
        DataBase.append(file_lines)
    ###############################################
    else:
        MS1_list = conn.execution_options(autocommit=True).execute('select scan_num from gardener_ms1 where search_id=%s ORDER BY id' % sid)
    
        for row in MS1_list :
            file_index = row['scan_num']
            peak_file = str(file_index) + '.txt'
            tt = []
            pp = int(file_index)  # MS1 scan num
            filedict[pp] = i  # Record the order of every txt file appeared
            i += 1
            f = open(dir + peak_file , 'r')
            for line in f:
                (ms_no, mz_temp, intensity_temp) = line.split(',')
                temp = (int(ms_no), float(mz_temp), float(intensity_temp))
                tt.append(temp)
            f.close()
            DataBase.append(tt)
    ################################################
    print 'Len(DataBase) = ', len(DataBase)
    print 'Complete reading txt!', time_now()
    # Allpep=Peptide.objects().filter(search_id==sid)
    print 'Initing obj_Pep......'
    pep_info = []
    PepNum = 0 
    
    '''This peptide list comes from msparser'''
    for row in ins_pep:
        PepNum += 1
        pep_info.append((row['ms2_id'], row['search_id'], row['sequence'], row['modification'], row['charge']))
        
    print 'for pep_index in range(PepNum)......'
    for pep_index in range(PepNum):
        # print 'pep_index',pep_index
        charge = pep_info[pep_index][4]
        QuantTable = []
        RTList = []
        IDTable = []
        ms2_id = pep_info[pep_index][0]
        # print 'pep_index=%s,ms2_id=%s'%(pep_index,ms2_id)
        # mz = allpep[pep_index]['mz']
        (mz, temp_rt) = get_mz_rt(conn, meta, ms2_id)  # conn.execution_options(autocommit=True).execute('select pre_mz,rt from gardener_ms2 where id=%s'%ms2_id).fetchone()

        lt, gt = temp_rt + dRT, temp_rt - dRT
        # print 'Initing obj_MS1......',pep_index
        pep_MS1 = []
        obj_MS1 = conn.execution_options(autocommit=True).execute('select * from gardener_ms1 where search_id=%s and rt>=%s and rt<=%s ORDER BY scan_num' % (sid, gt, lt))
        # obj_MS1 = get_obj_MS1(conn,meta,sid,gt,lt)
        tmp_id = 0
        for row in obj_MS1:
            tmp_id += 1
            pep_MS1.append((row['scan_num'], row['rt'], tmp_id))
        #print tempMS1
        
        for tMS1 in pep_MS1:
            best = 0
            RT = tMS1[1]
            interval = tMS1[2]
            try:
                id = filedict[int(tMS1[0])]
            except:
                continue
            less, more = mz * (1 - dMZ / 1e6), mz * (1 + dMZ / 1e6)
            '''Check If M/Z in right range'''
            if (DataBase[id][-1][1] < less) or (DataBase[id][0][1] > more):
                continue
            
            head = divfind(DataBase[id], less)
            tail = divfind(DataBase[id], more)
            best_intensity_list = [k[2] for k in DataBase[id][head:tail]]
            # p = DataBase[id][head:tail + 1]['intensity_temp']
            # p = [k['intensity_temp'] for k in DataBase[id] if k['mz_temp'] > mz * (1 - dMz / 1e6) and k['mz_temp'] < mz * (1 + dMz / 1e6)]
            if len(best_intensity_list) == 0:
                continue
            
            best = max(best, max(best_intensity_list))
            # print 'best',best
            if best == 0:
                # cmtable[exp][pep_index]['area'] = 0
                continue
            
            QuantTable.append(best)
            RTList.append(RT)
            IDTable.append(interval)
        # print 'len: '+str(len(QuantTable))
        """ Goto next peptide """
        if len(QuantTable) == 0:
            # cmtable[exp][pep_index]['area'] = 0
            continue
        
        index = QuantTable.index(max(QuantTable))
        length = len(QuantTable)
        
        left = 0
        for i in range(index, 0, -1):
            if IDTable[i] - IDTable[i - 1] > 3:
                left = i
                break
            
        right = length - 1
        for i in range(index + 1, length):
            if IDTable[i] - IDTable[i - 1] > 3:
                right = i - 1
                break
        # print ('right-left+1 '+str(right-left+1))
        QuantTable = QuantTable[left:right]
        RTList = RTList[left:right]
        
        length = len(QuantTable)
        if  length <= 3:
            areas = 0
        else:
            F = min(7, length - length % 2 - 1)
            #rt = str(QuantTable)
            #rm = str(RTList)
            SG_Processed_XIC = sgolayfilt(QuantTable, 2, F)
            # print 'SG_Processed_XIC',SG_Processed_XIC
            areas = numpy.trapz(SG_Processed_XIC, RTList)
            # to_db['%s'%pep_index] = areas
        ins_pep[pep_index]['area'] = areas
                    
        rr = 'sid=%s\t%s\t%s_%s\t%s\t%s\n' %(str(sid), pep_index, pep_info[pep_index][2], charge, areas, date_now()) 
        #rr = rr + ' qt=' + rt + ' rt=' + rm + '\n'
        result.append(rr)
    del DataBase 
    print 'Write peptide areas into output...'                         
    f = open(options.output, 'w')
    for r in result:
        f.write(r)
    f.close()
    print 'Complete calculating areas !', time_now()
    
    #gc.collect() 
    #exit(0)
    return ins_pep
    
def distributeAreas(ins_pep, ins_p, ins_g):    
    '''Get num_psms from all peptides list''' 
    i = 0
    s_pep = set()
    d_pep = {}
    for peptide in ins_pep:
        tt = peptide['sequence'] + peptide['modification']
        if tt in s_pep:
            d_pep[tt] += 1
        else:
            s_pep.add(tt)
            d_pep[tt] = 1
    for peptide in ins_pep:
        tt = peptide['sequence'] + peptide['modification']
        peptide['num_psms'] = d_pep[tt]
        # ins_pep[i]['num_psms'] = d_pep[tt]
        # i+=1
    
    '''Update protein areas'''   
    s_pro = set()  # set of protein accession, This set is larger than real protein set
    area_pro = {}  # For protein areas
    psms_pro = {}  # For num_psms of protein
    dict_p = {}  # For num_uni_pep
    for row in ins_pep:
        pro_gro_acc = row['protein_group_accessions']
        seq = row['sequence']
        num_pro = row['num_proteins']
        num_psms = row['num_psms']
        if num_pro == 0:continue
        area = row['area']
        pep_area = area / num_pro
        pga = pro_gro_acc.split(';')
        for pro in pga:
            if pro in s_pro:
                area_pro[pro] += pep_area
                psms_pro[pro] += num_psms
                dict_p[pro].append(seq)
            else:
                s_pro.add(pro)
                area_pro[pro] = pep_area
                psms_pro[pro] = num_psms
                dict_p[pro] = [seq]  # for getting num_uni_pep and num_pep
            
    '''Processing protein'''
    set_sym = set()
    area_g = {}  # For area of gene
    dict_g = {}  # For num_pep of gene
    proInGene = {}
    for pp in ins_p:
        if pp['type'] != 1:continue
        acc = pp['accession']
        if acc not in s_pro : continue
        sym = pp['symbol']
        num_pep = pp['num_peptides']
        pp['area'] = area_pro[acc]
        pp['num_psms'] = psms_pro[acc]
        pp['num_uni_peptides'] = len(set(dict_p[acc]))
        ''' Prepare gene '''  
        if sym in set_sym:
            area_g[sym] += pp['area']
            dict_g[sym].extend(dict_p[acc])
            proInGene[sym].append(acc)
        else:
            set_sym.add(sym)
            area_g[sym] = pp['area']
            dict_g[sym] = dict_p[acc]
            proInGene[sym] = [acc]
    ''' Processing gene  '''
    for gg in ins_g:
        if gg['type'] == -1:continue
        sym = gg['symbol']
        if not (sym in set_sym):continue
        protein_gi = '' 
        gg['area'] = area_g[sym]
        pros = proInGene[sym]
        for p in set(pros):
            protein_gi = protein_gi + p + ';'
        gg['protein_gi'] = protein_gi[:-1]
        gg['num_proteins'] = len(set(pros))
        gg['num_identified_proteins'] = len(set(pros))
        gg['num_uni_proteins'] = len(set(pros))
        gg['num_peptides'] = len(dict_g[sym])
        gg['num_uni_peptides'] = len(set(dict_g[sym]))

    # return ins_pep,ins_p,ins_g
                
def sql_gardener_file(options, conn, meta):
    rank = options.rank
    file_data = {}
    # file_data['job_id']=getJobId(conn,meta,options.job_track_id,options.user_id)
    # cwd=os.getcwd()
    # file_data['job_id']=getJobId(cwd)
    # options.label_name = 'CNHPP_HUVEC_DMSO_300ug_RP_17-22_3_E80574_F3_R3.raw'
    exp = get_exp_info("(" + options.label_name + ")")
    if exp['state'] == 1 :  # and file_data['job_id']!=-1:
        file_data['name'] = exp['name']
        file_data['exp_id'] = exp['exp_id']
        file_data['f_num'] = exp['nf']
        file_data['r_num'] = exp['nr']    
    else:
        stop_err('Error in file naming, please verify your file name before run reference pipeline.\n')
    e_name = 'Exp' + exp['exp_id']
    file_data['exp_db_id'] = get_exp_id(conn, meta, e_name)  #ID of exp table!!!
    (f, r) = get_file_num(conn, meta, file_data['exp_db_id'])
    file_data['file_num'] = f * r
    file_data['fractionNum'] = f
    file_data['repeatNum'] = r
    file_data['stage'] = 5
    file_data['user'] = get_user_name(conn, meta, options.user_id)
    file_data['email'] = getEmail(conn, meta, options.user_id)
    file_data['path'] = options.output
    file_data['file_type'] = 'txt'
    file_data['type'] = 'reference'
    file_data['size'] = 0
    file_data['rank'] = get_rank(conn, meta, file_data)
    print 'Max rank:', file_data['rank']
    if rank != 0:
        print 'rank!=0:', rank
        if rank > file_data['rank']:
            stop_err('Wrong rank number input.\n')
        file_data['rank'] = rank
        
    file_data['search_id'] = get_search_id(conn, meta, file_data)
    # insert_file(conn,meta,file_data)                 
    return file_data, rank

def timer(t2, t1):
    return float((t2 - t1).seconds) + (t2 - t1).microseconds / 1000000.0

def insertCache(stype, pep_pro_gene, data_list):
    table_name = 'gardener_%s_%s' %(stype, pep_pro_gene)
    insertGeneral(table_name, data_list)
    print '%s...Inserted %s\n' %(time_now(), table_name)

def get_pro_Length(peptide_list, qvalueThres, ionThres, pro_len_existed):
    dict_pro_length = {}
    tmp_set_pro = set()
    
    for peptide in peptide_list:
        
        sequence = peptide['sequence']
        if len(sequence) < 7:
            continue
        
        ionscore = peptide['ion_score']
        if ionscore < ionThres:
            continue
        
        qvalue = peptide['q_value']
        if qvalue > qvalueThres:
            continue

        pga_list = peptide['protein_group_accessions']
        for pro in pga_list.split(';'):
            if pro not in tmp_set_pro:     
                tmp_set_pro.add(pro)
                length = get_pro_len_Simple(conn, meta, pro) if pro not in pro_len_existed else pro_len_existed[pro]
                dict_pro_length[pro] = length

    return dict_pro_length

def pep_pro_association(peptide_list, qvalueThres, ionThres):
    tmp_set_pep = set()
    tmp_set_pro = set()
    dict_pep_has_pro = {}
    dict_pro_has_pep = {}
    pep_index = -1
    nonredundant_pep = 0
    for peptide in peptide_list:
        pep_index += 1
        type = peptide['type']
        
        sequence = peptide['sequence']
        if len(sequence) < 7:
            # print seq
            continue
        ionscore = peptide['ion_score']
        if ionscore < ionThres:
            continue
        qvalue = peptide['q_value']
        #=======================================================================
        # Round(ionscore)
        #=======================================================================
        # ionscore = round(ionscore)
        if qvalue > qvalueThres:
            continue
        nonredundant_pep += 1
        area = peptide['area']
        
        modification = peptide['modification']
        
        mod_status = [ 1 if MOD_NAME[i] in modification else 0 for i in range(LEN_MOD_NAME) ]
        
        charge = peptide['charge']
        # seq = seq + '_' + str(ionscore)
        # seq = seq + '_' + str(charge)
        seq = sequence.upper()
        if seq in tmp_set_pep:
            #===============================================================
            """ Maybe many peptides with same ionscore """
            #===============================================================
            dict_pep_has_pro[seq]['ionscore'] += ionscore
            dict_pep_has_pro[seq]['area'] += area
            dict_pep_has_pro[seq]['num_psms'] += 1
            i=-1
            for s in mod_status:
                i+=1
                dict_pep_has_pro[seq]['modification'][i] += s
            
        else:
            tmp_set_pep.add(seq)
            tmp = {}
            tmp['proteins'] = set()
            tmp['ionscore'] = ionscore
            tmp['charge'] = charge
            tmp['area'] = area
            tmp['type'] = type
            tmp['num_psms'] = 1
            tmp['modification'] = mod_status
            
            dict_pep_has_pro[seq] = tmp
        #=======================================================================
        """ Get every protein in which this peptide appears """
        #=======================================================================
        pga_list = peptide['protein_group_accessions']
        for pro in pga_list.split(';'):
            dict_pep_has_pro[seq]['proteins'].add(pro)
            
            if pro in tmp_set_pro:     
                dict_pro_has_pep[pro]['peptides'].add(seq)
                dict_pro_has_pep[pro]['pep_index'].add(pep_index)
                
            else:   
                symbol = ''  # getSymbol(pro)
                tmp_set_pro.add(pro)
                tmp = {}
                tmp['peptides'] = set([seq])
                tmp['pep_index'] = set([pep_index])
                tmp['sameset'] = set()
                tmp['symbol'] = symbol
                tmp['type'] = type
                
                dict_pro_has_pep[pro] = tmp
    
    return (dict_pep_has_pro, dict_pro_has_pep, nonredundant_pep)
    
def useParsimony(eid, type, qvalueThres, ionThres, peptide_list, flag, dict_pro_length):
    #flag = 1
    t1 = datetime.datetime.now()
    if flag != 0:
        print 'Grouping...[%s]' % type, t1.strftime('%X')
    
    (dict_pep_has_pro, dict_pro_has_pep,nonredundant_pep) = pep_pro_association(peptide_list, qvalueThres, ionThres)
    
    # f = open('outpep%s(%s).txt' % (eid, type), 'w')           
    set_uni_pep = set()
    for seq, info in dict_pep_has_pro.iteritems():
        # f.write(seq.split('_')[0] + '\n')
        # f.write(seq.split('_')[0].upper() + '\t'+';'.join(list(set(list_pro)))+'\n')
        if len(info['proteins']) == 1:# info['proteins'] is a set
            set_uni_pep.add(seq)
    # f.close()
    if flag != 0:
        print 'len(dict_pep_has_pro):', len(dict_pep_has_pro)
        print 'len(dict_pro_has_pep):', len(dict_pro_has_pep)
        print 'len(set_uni_pep):', len(set_uni_pep)

 
    #===============================================================================
    ''' Get distinct proteins identified by only discrete peptide(s)'''
    #===============================================================================
    j = k = 0
    dict_uni_pro      = {} # Proteins have unique peptides
    dict_none_uni_pro = {} # Proteins don't have unique peptides
    pro_onlyUniPep    = set()
    for pro, info in dict_pro_has_pep.iteritems():
        proscore = 0
        pep_psms = 0
        peptides = info['peptides']  # Is a set
        pepnum = len(peptides)
        pep_index_set = info['pep_index'] # Is a set
        symbol = info['symbol']
        # peps_other = list(peptides)
        uni_peps = []
        has_uni = 0
        # print pepnum
        tmp_mod_status = [ 0 for i in range(LEN_MOD_NAME)]
        for peptide in peptides:
            ''' Pro_score comes from ionscore '''
            proscore += dict_pep_has_pro[peptide]['ionscore']
            pep_psms += dict_pep_has_pro[peptide]['num_psms']
            if peptide in set_uni_pep:
                has_uni += 1
                uni_peps.append(peptide)
                # peps_other.remove(peptide)
            tmp_mod_status = [dict_pep_has_pro[peptide]['modification'][i]+tmp_mod_status[i] for i in range(LEN_MOD_NAME)]
        tmp_mod_status = ','.join([str(n) for n in tmp_mod_status])
        tmp = {}
        tmp['peptides'] = peptides  # Is a set
        tmp['pep_index'] = pep_index_set # Is a set
        tmp['sameset'] = set()
        tmp['uni'] = uni_peps
        tmp['symbol'] = symbol
        tmp['score'] = proscore
        tmp['pep_psms'] = pep_psms
        tmp['type'] = type
        tmp['score'] = proscore
        tmp['pep_psms'] = pep_psms  
        tmp['modification'] = tmp_mod_status
        if has_uni > 0:
            dict_uni_pro[pro] = tmp
            j += 1
            if has_uni == pepnum:
                pro_onlyUniPep.add(pro)
        else:
            #tmp['score'] = 0
            dict_none_uni_pro[pro] = tmp
            
    if flag != 0:
        print 'Finished getting dict_uni_pro...[%s]' % type, time_now()
    # exit(0)
    
    ''' Start to get sameset, and merge to dict_uni_pro '''
    sameset_find = total_sameset = 0
    searched = set()
    pro_sameset = set()
    dict_sameset_pro = {}

    for pro1, info1 in dict_none_uni_pro.items():
        if pro1 in searched : continue
        searched.add(pro1)
        master_pro = pro1
        #len_pro1 = get_pro_len_Simple(conn, meta, pro1)
        len_pro1 = dict_pro_length[pro1]
        min_len = len_pro1
        sameset_find = 0
        tmp = {}
        for pro2, info2 in dict_none_uni_pro.items():
            if pro2 in searched : continue
            if info1['peptides'] == info2['peptides']:  # Is a set
                #len_pro2 = get_pro_len_Simple(conn, meta, pro2)
                len_pro2 = dict_pro_length[pro2]
                if len_pro2 < min_len:
                    min_len, master_pro = len_pro2, pro2
                    
                symbol = info2['symbol']
                sameset_find += 1
                # print pro1, pro2
                if sameset_find == 1: 
                    del dict_none_uni_pro[pro1]
                    del dict_none_uni_pro[pro2]
                    searched.add(pro2)
                    tmp['peptides'] = info1['peptides']
                    tmp['pep_index'] = info1['pep_index']
                    tmp['sameset'] = set([pro1, pro2])
                    tmp['uni'] = []
                    tmp['symbol'] = symbol
                    tmp['score'] = info1['score']
                    tmp['pep_psms'] = info1['pep_psms']
                    tmp['modification'] = info1['modification']
                    tmp['type'] = type
                else:
                    # pro_sameset.add(pro2)
                    del dict_none_uni_pro[pro2]
                    searched.add(pro2)
                    tmp['sameset'].add(pro2)
                    tmp['pep_index'] = tmp['pep_index'] | info2['pep_index']
                # dict_uni_pro[pro_uni]['sameset'].append(pro)
        # print sameset_find,'====================='
        if sameset_find > 0:
            total_sameset += 1
            tmp['sameset'].remove(master_pro)
            dict_uni_pro[master_pro] = tmp
    
    """ Start to get remaining protein, and merge to dict_uni_pro """
    remaining = 0
    #print 'Remaining:\n'
    for pro, info in dict_none_uni_pro.items():
        equal_cover = 1
        pep_num = len(info['peptides'])
        for pep in info['peptides']:
            if equal_cover == 0:break
            for next_pro in dict_pep_has_pro[pep]['proteins']:
                if equal_cover == 0:break
                if next_pro == pro:continue
                pep_num_next_pro = len(dict_pro_has_pep[next_pro]['peptides'])
                if pep_num < pep_num_next_pro :
                    equal_cover = 0
        if equal_cover:
            #print pro
            remaining += 1
            dict_uni_pro[pro] = info
            del dict_none_uni_pro[pro]
              
    if flag != 0:
        print 'Pro has unipep:', j
        print 'Pro has Only unipep:', len(pro_onlyUniPep)
        print 'Pro has sameset:', total_sameset
        print 'Assigned Pro:', len(dict_uni_pro)
        print 'Remaining Pro:',remaining
        print 'Unassigned:', len(dict_none_uni_pro)-remaining
        print 'Finish useParsimony(%s,  %s)..................................' % (eid, type), time_now()
    
    if type == 1:
        return (dict_uni_pro, dict_none_uni_pro, dict_pep_has_pro, dict_pro_has_pep, nonredundant_pep)
    else:
        return (dict_uni_pro, nonredundant_pep)

def startProteinAssemble(eid, peptide_list, pep_list_decoy, fdrThres, ionThres):
    #dir = '/usr/local/galaxyDATA01/incubator/python/ms_parser'
    t1 = datetime.datetime.now()
    print '\nStart startProteinAssemble...eid =', eid
    #ionThres = 20
    step = 0.0001
    fdrThres = fdrThres + 0.0005
    pro_score_Thres = 20
    qvalueThres = 0.01
    if eid == LIPENG:
        qvalueThres = 0.003
    print '\n# # # # # Ionscore Threshold:', ionThres
    #===========================================================================
    # Start cycle to find FDR < 0.01
    #===========================================================================
    FDR = FDR_pep = FDR_psms = 1
    times = 1
    flag = 0
    dict_pro_length = {}
    dict_pro_length       = get_pro_Length(peptide_list,   qvalueThres, ionThres, dict_pro_length)
    dict_pro_length_decoy = get_pro_Length(pep_list_decoy, qvalueThres, ionThres, dict_pro_length)
    while 1:
        print '\n# # # # # Qvalue Threshold:', qvalueThres
        (dict_uni_pro_real, dict_none_uni_pro_real, dict_pep_has_pro_real, dict_pro_has_pep_real, total_pep_1) = useParsimony(eid, 1, qvalueThres, ionThres, peptide_list, flag, dict_pro_length)
        
        (dict_uni_pro_decoy, total_pep_0) = useParsimony(eid, -1, qvalueThres, ionThres, pep_list_decoy, flag, dict_pro_length_decoy)
    
        #===============================================================================
        # Calc FDR for every protein        
        #===============================================================================
        target_num = len(dict_uni_pro_real)
        if target_num == 0:
            FDR = 1
            break
        #FDR = float(decoy) / real
        decoy_num = len(dict_uni_pro_decoy)
        FDR     = float(decoy_num) / target_num
        
        
        if FDR>=fdrThres*2 and times==1: 
            qvalueThres = 0.003#step=step*2
        #=======================================================================
        # If FDR is good
        #=======================================================================
        print '# # # # # FDR:', FDR
        if FDR < fdrThres:
            if times == 1: break
            FDR_good = FDR
            flag += 1  # In case we leap 1 ionscore where FDR already < Threshold
            if flag == 2: break
            times += 1
            qvalueThres += step
        else:
            if flag == 1:
                times += 1
                qvalueThres = qvalueThres - step
            else:
                times += 1
                qvalueThres = qvalueThres - step*2
                if qvalueThres < 0:
                    qvalueThres += step*2
                    break
    
    FDR_pep = float(total_pep_0) / total_pep_1 if total_pep_1 !=0 else 1
    
    psms_fdr_real = psms_fdr_decoy = 0
    for xxx,yyy in dict_uni_pro_decoy.iteritems():
        psms_fdr_decoy += yyy['pep_psms']
        
    del peptide_list
    del pep_list_decoy
    t2 = datetime.datetime.now()
    delta = timer(t2, t1)  # float((t2 - t1).seconds) + (t2 - t1).microseconds / 1000000.0
    print '\nGroup Cycle used %.3f seconds' % delta
    #===============================================================================
    # Output proteins
    #===============================================================================
    print 'Protein group_result...' , time_now()
    
    tmp_set_pro = set()
    tmp_set_pep_index = set()
    tmp_set_pep_pga = set()
    set_pep_index = {}
    pga_peptide = {}
    group_result = []   
    total_FOT = 0.0
    for pro, info in dict_uni_pro_real.iteritems():
        #=======================================================================
        """ Using Pep_index to know which peptide used to assemble proteins """
        #=======================================================================
        pep_index_set = info['pep_index']
        tmp_set_pep_index = tmp_set_pep_index | pep_index_set

        #=======================================================================
        """ Below is getting Protein info """
        #=======================================================================
        
        modification = info['modification']
        proscore = info['score']
        symbol = info['symbol']
        pep_psms = info['pep_psms']
        psms_fdr_real += pep_psms
        
        sameset = ';'.join(sorted(info['sameset']))
        peps = sorted(info['peptides'])
        num_pep = len(peps)
        uni_peps = sorted(info['uni'])
        num_unipep = len(uni_peps)
        area_pro = 0.0
        #=======================================================================
        """ Distribute peptide area to Protein """
        #=======================================================================
        for peptide in peps:
            if peptide in tmp_set_pep_pga:
                pga_peptide[peptide].add(pro)
            else:
                tmp_set_pep_pga.add(peptide)
                pga_peptide[peptide] = set([pro])
                
            assembled = 0
            area_pep = dict_pep_has_pro_real[peptide]['area']
            pros_of_pep = dict_pep_has_pro_real[peptide]['proteins']
            for p in pros_of_pep:
                if p in dict_uni_pro_real: assembled += 1
            area_average = area_pep / assembled if assembled != 0 else 0
            area_pro += area_average
            
        tmp = {}
        tmp['accession'] = pro
        tmp['symbol'] = symbol
        tmp['score'] = proscore
        tmp['sameset'] = sameset
        tmp['num_pep'] = num_pep
        tmp['num_unipep'] = num_unipep
        tmp['pep_psms'] = pep_psms
        tmp['area'] = area_pro
        tmp['pep_index'] = pep_index_set
        tmp['modification'] = modification
        group_result.append(tmp)
        
    #===========================================================================
    # Print proteins with proper FDR        
    #===========================================================================
    
    output_nums = 0
    group_result.sort(key=lambda x:x['score'], reverse=1)
 
    output_nums = len(group_result)
    #===============================================================================
    # Unassigned proteins
    #===============================================================================
    print 'Unassigned proteins:',len(dict_none_uni_pro_real)
    
    FDR_psms = float(psms_fdr_decoy)/psms_fdr_real if psms_fdr_real !=0 else 1
    
    print 'FDR of psms =',FDR_psms
    print 'FDR of peptide =',FDR_pep
    print '\nFinal Qvalue Threshold = ', qvalueThres
    print 'After cycled %s times\nWrite %s proteins\nWith FDR = %f and ionscoreThreshold = %s......' % (times, output_nums, FDR, ionThres), time_now()
    #===============================================================================
    # Time used
    #===============================================================================
    t2 = datetime.datetime.now()
    delta = timer(t2, t1)  # float((t2 - t1).seconds) + (t2 - t1).microseconds / 1000000.0
    print 'Over...', str(t2.strftime('%X'))
    print 'Used %.3f seconds' % delta
    print 'EID:', eid
    print 
    
    return (group_result, qvalueThres, FDR, dict_uni_pro_real, tmp_set_pep_index, pga_peptide, dict_pro_length)

def getPepFromDB(eid, rid, rank, type, stype, ionThres):
    #===============================================================================
    # Get Real or Decoy psms  
    #===============================================================================
    if stype == 'exp':
        t = 'select * from gardener_peptide where ion_score>=%s and search_id in (select id from gardener_search where exp_id=%s and type=\'fraction\') and type=%s' % (ionThres, eid, type)
    elif stype == 'repeat':
        t = 'select * from gardener_peptide where ion_score>=%s and search_id in (select id from gardener_search where exp_id=%s and repeat_id=%s and rank=%s and type=\'fraction\') and type=%s' % (ionThres, eid, rid, rank, type)
    
    peptide_list = conn.execution_options(autocommit=True).execute(t)
    
    if peptide_list == None:
        print 'no peptides '
        peptide_list.close()
        return []
    pep_list = []

    for row in peptide_list:
        pep_d = {}
        pep_d['ms2_id'] = row['ms2_id']
        pep_d['search_id'] = row['search_id']
        pep_d['quality'] = row['quality']
        pep_d['sequence'] = row['sequence']
        pep_d['type'] = row['type']
        pep_d['num_psms'] = row['num_psms']
        pep_d['num_proteins'] = row['num_proteins']
        pep_d['num_protein_groups'] = row['num_protein_groups']
        pep_d['protein_group_accessions'] = row['protein_group_accessions']
        pep_d['modification'] = row['modification']
        pep_d['delta_cn'] = row['delta_cn']
        pep_d['area'] = row['area']
        pep_d['q_value'] = row['q_value']
        pep_d['pep'] = row['pep']
        pep_d['ion_score'] = row['ion_score']
        pep_d['exp_value'] = row['exp_value']
        pep_d['charge'] = row['charge']
        pep_d['mh_da'] = row['mh_da']
        pep_d['delta_m_ppm'] = row['delta_m_ppm']
        pep_d['rt_min'] = row['rt_min']
        pep_d['num_missed_cleavages'] = row['num_missed_cleavages']
        pep_d['fdr'] = row['fdr']
        pep_d['from_where'] = row['from_where']
        pep_d['fot'] = row['fot']
        pep_list.append(pep_d)
    
    #print 'peptide_list.append...[%s]' % type, time_now()
    return pep_list

def getPeptides(sid, filename, resfile, results, searchparams, NumQueries, min_ionscore, dict_percolator, maxRank):
    #===============================================================================
    # Get Real or Decoy psms  
    #===============================================================================
    ins_pep = []
    ms2_id_decoy = 0
    #print dict_percolator
    for query_rank in dict_percolator:  # range(1,1+NumQueries):
        query_index = int(query_rank.split(';')[0][6:])
        if not query_rank.endswith('rank:1'):
            continue
        
        peptides = resfile.getSectionValueStr(msparser.ms_mascotresfile.SEC_PEPTIDES, "q%s_p1" % query_index)
        if peptides == '-1' :
            continue
        intensity = resfile.getSectionValueStr(msparser.ms_mascotresfile.SEC_SUMMARY, "qintensity%s" % query_index)
        qexp = resfile.getSectionValueStr(msparser.ms_mascotresfile.SEC_SUMMARY, "qexp%s" % query_index)
        y = qexp.split(',')
        mz = y[0]
            
        query = msparser.ms_inputquery(resfile, query_index)
        rt_sec = query.getRetentionTimes()
        rt_min = round(float(rt_sec) / 60, 3)
        title = query.getStringTitle(-1)[:-8]
        scanNum_ms2 = int(title.split('.')[1])
            
        for j in range(1, 2):  # maxRank
            peptides = resfile.getSectionValueStr(msparser.ms_mascotresfile.SEC_PEPTIDES, "q%s_p%s" % (query_index, j))
            peptide = results.getPeptide(query_index, j)
            if not peptide: 
                break
            
            seq = peptide.getPeptideStr()
            sequence_list = list(seq)
            
            if len(sequence_list) < 7: 
                continue
            ionsScore = peptide.getIonsScore()
            if ionsScore < min_ionscore: 
                continue
            q_value = dict_percolator[query_rank]['qvalue']
            if q_value > 0.01:
                continue
            if q_value < 0.01:
                quality = 'High'
            elif q_value < 0.05:
                quality = 'Medium'
            else :
                quality = 'Low'
                    
            charge = peptide.getCharge()
            # mz = peptide.getObserved()
            # protein_id_list=[]    
            accession_list = []
            mod_list = []

            ########################## Modify sequence #######################
            varmod_list = list(peptide.getVarModsStr())
            if varmod_list[0] != '0':
                sequence_list[0] = sequence_list[0].lower()
                mod_left = searchparams.getVarModsName(int(varmod_list[0]))
                mod_list.append(mod_left) 
                       
            for position in range(1, len(varmod_list) - 1):
                if varmod_list[position] != '0':
                    n = searchparams.getVarModsName(int(varmod_list[position]))    
                    mod_name = n + '(' + str(position) + ')'  # sequence_list[position-1]+
                    mod_list.append(mod_name)
                    sequence_list[position - 1] = sequence_list[position - 1].lower()
                        
            if varmod_list[-1] != '0':
                sequence_list[-1] = sequence_list[-1].lower()
                mod_right = searchparams.getVarModsName(int(varmod_list[-1]))
                mod_list.append(mod_right)
                    
            sequence = ''.join(sequence_list)
            # mod_list.sort()
            modification = ';'.join(mod_list)  
          
            ################   store peptides in list  #######################
            # acc_from_hit=0
            acc_list = []
            
            getAccession = peptides.split(';') 
            tmp = getAccession[1]
            accs = tmp.split(',')
            for acc in accs:
                t = acc.split('"')[1]
                acc_list.append(t)
                    
            if len(acc_list) == 0:
                print 'peptide has no proteins:', sequence
                continue
                
            num_psms = 1  # peptide.getAnyMatch()
            num_proteins = len(acc_list)  # peptide.getNumProteins()  # 
            num_protein_groups = 0
            delta_cn = 0.0
            area = 0.0
            
            pep_value = dict_percolator[query_rank]['pepvalue']
            exp_value = results.getPeptideExpectationValue(ionsScore, query_index)
            mh_da = peptide.getMrCalc() + H_PLUS  # 1.0078251.007825  # peptide.getObserved() 
            delta_m_ppm = peptide.getDelta() / peptide.getMrCalc() * 1e6
            num_missed_cleavages = peptide.getMissedCleavages()  # tmp1.split(',')[0]#
           
            ms2_id = get_ms2_id(conn, meta, scanNum_ms2, sid)
            if ms2_id == None:
                continue
            ms2_id_decoy = ms2_id
                
            tmp = {}
            tmp['ms2_id'] = ms2_id
            tmp['search_id'] = sid
            tmp['quality'] = quality
            tmp['sequence'] = sequence
            tmp['num_psms'] = num_psms
            tmp['num_proteins'] = num_proteins
            tmp['num_protein_groups'] = num_protein_groups
            tmp['protein_group_accessions'] = ';'.join(acc_list)
            tmp['modification'] = modification
            tmp['delta_cn'] = delta_cn
            tmp['area'] = area
            tmp['q_value'] = q_value
            tmp['pep'] = pep_value
            tmp['ion_score'] = ionsScore
            tmp['exp_value'] = exp_value
            tmp['charge'] = charge
            tmp['mh_da'] = mh_da
            tmp['delta_m_ppm'] = delta_m_ppm
            tmp['rt_min'] = rt_sec
            tmp['num_missed_cleavages'] = num_missed_cleavages
            tmp['type'] = 1
            tmp['fdr'] = 0.0
            tmp['from_where'] = filename + '_q%s_p%s' % (query_index, j)
            tmp['fot'] = 0.0
            ins_pep.append(tmp)
    
    return ins_pep, ms2_id_decoy
    
def getDecoyPeps(sid, filename, resfile, results_decoy, searchparams, NumQueries, min_ionscore, dict_percolator_decoy, ms2_id_decoy, maxRank):

    print 'get MS2_id_decoy :', ms2_id_decoy
    if ms2_id_decoy == 0:
        return []
    ins_pep = []
    for query_rank in dict_percolator_decoy:  # range(1,1+NumQueries):
        query_index = int(query_rank.split(';')[0][6:])
        if query_rank[-1] != '1':
            continue    
    #for query_index in range(1, 1 + NumQueries):
        peptides = resfile.getSectionValueStr(msparser.ms_mascotresfile.SEC_DECOYPEPTIDES, "q%s_p1" % query_index)
        if peptides != '-1' :
            intensity = resfile.getSectionValueStr(msparser.ms_mascotresfile.SEC_DECOYSUMMARY, "qintensity%s" % query_index)
            for j in range (1, 2):  # (1,1+maxRank):#maxRank
                peptides = resfile.getSectionValueStr(msparser.ms_mascotresfile.SEC_DECOYPEPTIDES, "q%s_p%s" % (query_index, j))
                peptide = results_decoy.getPeptide(query_index, j)
                if not peptide: 
                    break
                sequence_list = list(peptide.getPeptideStr())
                if len(sequence_list) < 7: 
                    continue
                ionsScore = peptide.getIonsScore()
                if ionsScore < min_ionscore:
                    continue
                q_value = dict_percolator_decoy[query_rank]['qvalue']
                if q_value > 0.01:
                    continue
                if q_value < 0.01:
                    quality = 'High'
                elif q_value < 0.05:
                    quality = 'Medium'
                else :
                    quality = 'Low'
                    
                charge = peptide.getCharge()
                mz = peptide.getObserved()    
                accession_list = []
                mod_list = []
                ########################  Modify sequence  ######################
                varmod_list = list(peptide.getVarModsStr())
                if varmod_list[0] != '0':
                    sequence_list[0] = sequence_list[0].lower()
                    mod_left = searchparams.getVarModsName(int(varmod_list[0]))
                    mod_list.append(mod_left) 
                       
                for position in range(1, len(varmod_list) - 1):
                    if varmod_list[position] != '0':
                        n = searchparams.getVarModsName(int(varmod_list[position]))    
                        mod_name = n + '(' + str(position) + ')'  # sequence_list[position-1]+
                        mod_list.append(mod_name)
                        sequence_list[position - 1] = sequence_list[position - 1].lower()
                        
                if varmod_list[-1] != '0':
                    sequence_list[-1] = sequence_list[-1].lower()
                    mod_right = searchparams.getVarModsName(int(varmod_list[-1]))
                    mod_list.append(mod_right)
                    
                sequence = ''.join(sequence_list)
                mod_list.sort()
                modification = ';'.join(mod_list)  
                
                ################   store peptides in list  #######################
                # acc_from_hit=0
                acc_list = []
                
                getAccession = peptides.split(';')
                
                try:
                    tmp = getAccession[1]
                except:
                    print "q%s_p%s" % (query_index, j)
                    print getAccession
                    exit(0)
                accs = tmp.split(',')
                for acc in accs:
                    t = acc.split('"')[1]
                    acc_list.append(t)
                    
                if len(acc_list) == 0:
                    print 'peptide has no proteins:', sequence
                    continue
                
                mh_da = peptide.getMrCalc() + H_PLUS  # 1.007825  # peptide.getObserved() 
                delta_m_ppm = peptide.getDelta() / peptide.getMrCalc() * 1e6
                num_missed_cleavages = peptide.getMissedCleavages()  # tmp1.split(',')[0]#
                
                tmp = {}
                tmp['ms2_id'] = ms2_id_decoy
                tmp['search_id'] = sid
                tmp['quality'] = quality
                tmp['sequence'] = sequence
                tmp['num_psms'] = 0
                tmp['num_proteins'] = 0
                tmp['num_protein_groups'] = 0
                tmp['protein_group_accessions'] = ';'.join(acc_list)
                tmp['modification'] = modification
                tmp['delta_cn'] = 0.0
                tmp['area'] = 0.0
                tmp['q_value'] = q_value
                tmp['pep'] = dict_percolator_decoy[query_rank]['pepvalue']
                tmp['ion_score'] = ionsScore
                tmp['exp_value'] = 0.0
                tmp['charge'] = charge
                tmp['mh_da'] = mh_da
                tmp['delta_m_ppm'] = delta_m_ppm
                tmp['rt_min'] = 0.0
                tmp['num_missed_cleavages'] = num_missed_cleavages
                tmp['type'] = -1
                tmp['fdr'] = 1
                tmp['from_where'] = filename + '_q%s_p%s_decoy' % (query_index, j)
                tmp['fot'] = 0.0
                ins_pep.append(tmp)
    
    return ins_pep

def get_ibaq_num(pro_seq):
    length=len(pro_seq)
    tmp_len=0
    ans=0
    for i in range(length):
        tmp_len=tmp_len+1
        if pro_seq[i]=='K' or pro_seq[i]=='R':
            if i==length-1 or pro_seq[i+1]!='P':
                if tmp_len>=7 and tmp_len<=40:
                    ans=ans+1
            tmp_len=0
    
    if ans == 0 : ans = 1
    return ans

def get_pro_coverage(set_peps_of_pro,pro_seq,length):
    coverage = 0.0
    cover_set = set()
    for peptide in set_peps_of_pro:
        regex = r'%s'%peptide.upper()
        i = 0
        for s in re.finditer(regex, pro_seq):
            i += 1
            st = s.span()[0]
            ed = s.span()[1]
            tmp_list = range(st, ed)
            cover_set = cover_set.union(set(tmp_list))
        if i == 0:
            print 'Pep seq Not in fasta:',peptide
    coverage = float(len(cover_set)) / length if length != 0 else 0.0
    if coverage > 1: coverage = 1
    return coverage
"""
def getAnnotation(conn,meta,symbol):
    symbol = symbol.upper()
    anno = ['0' for i in range(6)]
    t = Table('gardener_fasta_data', meta, autoload=True, autoload_with=engine)
    s = select([t.c.annotation_id]).where(t.c.symbol == symbol)
    res = conn.execution_options(autocommit=True).execute(s).scalar()
    if res:
        res = res.split(';')
        for i in res:
            anno[int(i)-1] = '1'
    return ''.join(anno)
"""
def getAnnotation(conn,meta,anno_string, symbol,species):
    anno_list = anno_string.split(',')
    t = "select distinct(annotation_id),species from gardener_annotation where symbol=\'%s\'" %symbol.upper()
    res = conn.execution_options(autocommit=True).execute(t)
    for row in res:
        if row['species'] and species != row['species']:
            continue
        id = row['annotation_id']-1
        anno_list[id] = anno_list[id][:-1]+'1'
    
    return ','.join(anno_list)

def split_accession(accession):
    if '|' in accession:
        acc_short = accession.split('|')[1]
        prefix = accession.split('|')[0]
    else :
        acc_short = accession
        prefix = 'none'
        
    return (acc_short, prefix)
        
def getProGeneFromDB(dict_uni_pro, group_result, sid, eid, fdr, dict_pro_length):
    species = get_species(conn, meta, eid)
    taxid = get_taxid(conn, meta, eid)
    
    print 'Caching(get protein & gene).......', time_now()
    ins_p = []  # List of protein info
    ins_g = []  # List of gene info
    # parsed = 1
    total_FOT = total_FOT_gene = 0.0
    hit = 1
    count = 0
    acc_noGID = 0
    acc_noGID_list = []
    set_sym = set()
    #ibaq_num_dict = {}
    # print 'For pro in group_result...'
    for row in group_result:
        modif_num = row['modification'].split(',')
        modif_num = ['0' if i == '0' else '1' for i in modif_num]
        modif_status = ','.join([ MOD_ABBREV[i] + modif_num[i] for i in range(LEN_MOD_NAME)])
        score = row['score']
        accession = row['accession']
        pro_area = row['area']
        
        acc_short, prefix = split_accession(accession)
        
        others = row['sameset']
        num_proteins = 1 if others == '' else len(others.split(';')) + 1
        # mass = results.getProteinMass(accession)
        (mass, pro_seq) = get_pro_mass(conn, meta, acc_short, dict_aa_mass, prefix)        
       
        if mass != 0:
            #length = get_pro_len(conn, meta, acc_short, prefix)
            length = dict_pro_length[accession]
            
            if length == 0 : length = int(mass / 110)  # Must get length
            set_peps_of_pro = dict_uni_pro[accession]['peptides']
            coverage = get_pro_coverage(set_peps_of_pro,pro_seq,length)
        else:
            length = 0
            coverage = 0.0
            
        ibaq_num = get_ibaq_num(pro_seq)
        ibaq = pro_area / ibaq_num
        #ibaq_num_dict[accession] = ibaq_num
        symbol = desc = ''
        anno = ANNOTATION 

        '''Get Gene Info'''
        gid = getGeneID(conn, meta, acc_short, prefix, taxid) 
            
        ''''For other taxon '''
        if gid == -1 :
            acc_noGID += 1
            '''
            acc_noGID_list.append(accession)
            #print accession
            if 'Pig' in species or 'Sus scrofa' in species :
                gid = getPigGID(conn, meta, acc_short, prefix)
            '''    
            if 'Schizosaccharomyces pombe' == species:
                (symbol, desc) = get_yeast_gene_from_db(acc_short)
            elif int(taxid) == 8355:#xenopus, Lei Song
                (symbol, desc) = get_xenos_gene_from_db(acc_short)
            #elif int(taxid) == 7955:
                #(symbol, desc) = get_zebrafish_gene_from_db(acc_short)
            #elif int(taxid) == 8355:
            #    (symbol, desc) = get_xenos_gene_from_db(acc_short)
                
        if gid != -1:
            
            (symbol, desc) = getGeneDescSymbol(conn, meta, gid) if not desc else (symbol, desc)
            if symbol!='-':
                anno = getAnnotation(conn,meta,anno,symbol,species)
                # print hit,sid,symbol,desc
                tmp = {} 
                tmp['score'] = score
                tmp['search_id'] = sid
                tmp['symbol'] = symbol
                tmp['gene_id'] = gid
                tmp['protein_gi'] = accession if others=='' else accession + ';' + others
                tmp['num_proteins'] = num_proteins
                tmp['num_identified_proteins'] = num_proteins
                tmp['num_uni_proteins'] = num_proteins
                tmp['num_peptides'] = row['num_pep']
                tmp['num_uni_peptides'] = row['num_unipep']
                tmp['num_psms'] = row['pep_psms']
                tmp['area'] = pro_area
                tmp['fdr'] = fdr
                tmp['description'] = desc
                tmp['type'] = 1
                tmp['fot'] = 0.0   
                tmp['ibaq'] = ibaq
                tmp['annotation'] = anno
                tmp['modification'] = modif_status
            
                ins_g.append(tmp)
                total_FOT_gene += ibaq    
        
        ''''Protein Hit'''
        
        desc_pro = desc
        # desc_pro = results.getProteinDescription(accession)
        if not desc_pro :
            desc_pro = get_desc_pro(conn, meta, acc_short, prefix)
                
        tmp = {}    
        tmp['search_id'] = sid
        tmp['accession'] = accession
        tmp['other_members'] = others
        tmp['symbol'] = symbol if symbol!='-' else ''
        tmp['description'] = desc_pro
        tmp['score'] = score
        tmp['coverage'] = coverage
        tmp['num_proteins'] = num_proteins
        tmp['num_uni_peptides'] = row['num_unipep']
        tmp['num_peptides'] = row['num_pep']
        tmp['num_psms'] = row['pep_psms']
        tmp['area'] = pro_area
        tmp['length'] = length
        tmp['mw'] = mass
        tmp['calc_pi'] = 0.0
        tmp['type'] = 1
        tmp['fdr'] = fdr 
        tmp['fot'] = 0.0
        tmp['ibaq'] = ibaq
        tmp['annotation'] = anno
        tmp['modification'] = modif_status
        
        ins_p.append(tmp)
        # RMS_error = prot.getRMSDeltas(results)
        # numDisplayPeptides = prot.getNumDisplayPeptides()
        total_FOT += ibaq
        count += 1   
        hit += 1
    
    '''Calc Protein FOT'''
   
    for pp in ins_p:
        fot = pp['ibaq'] / total_FOT if total_FOT != 0 else 0.0
        pp['fot'] = fot * 1000000
        
    print 'Proteins with no GID = ', acc_noGID
    #print acc_noGID_list
    print '(iBAQ)Protein total_FOT = ', total_FOT
    print '(iBAQ)Gene total_FOT = ', total_FOT_gene
    # print 'Min_score=', min_proscore
    print 'Pro_Num = ', count
    
    '''Process Gene list '''
    set_sym = set()
    dict_gene = {}
    
    for gg in ins_g:
        sym = gg['symbol'] 
        protein_gi = gg['protein_gi']

        if sym in set_sym:
            dict_gene[sym]['score'] += gg['score']
            dict_gene[sym]['protein_gi'].extend(protein_gi.split(';'))
            dict_gene[sym]['num_proteins'] += gg['num_proteins']
            dict_gene[sym]['num_identified_proteins'] += gg['num_identified_proteins']
            dict_gene[sym]['num_uni_proteins'] += gg['num_uni_proteins']
            dict_gene[sym]['num_peptides'] += gg['num_peptides']
            dict_gene[sym]['num_uni_peptides'] += gg['num_uni_peptides']
            dict_gene[sym]['num_psms'] += gg['num_psms']
            dict_gene[sym]['area'] += gg['area']
            dict_gene[sym]['ibaq'] += gg['ibaq']
        else:
            set_sym.add(sym)
            tmp = {}
            tmp['score']        = gg['score']
            tmp['protein_gi']   = protein_gi.split(';')
            tmp['num_proteins'] = gg['num_proteins']
            tmp['num_identified_proteins'] = gg['num_identified_proteins']
            tmp['num_uni_proteins'] = gg['num_uni_proteins']
            tmp['num_peptides']     = gg['num_peptides']
            tmp['num_uni_peptides'] = gg['num_uni_peptides']
            tmp['num_psms'] = gg['num_psms']
            tmp['area']      = gg['area']
            tmp['search_id'] = gg['search_id']
            tmp['gene_id']   = gg['gene_id']
            tmp['symbol']    = sym
            tmp['fdr']       = gg['fdr']
            tmp['description'] = gg['description']
            tmp['type']        = gg['type']
            tmp['fot']         = gg['fot']
            tmp['ibaq']        = gg['ibaq']
            tmp['annotation']  = gg['annotation']
            tmp['modification'] = gg['modification']
            dict_gene[sym] = tmp
            
    gene_list = []        
    for sym, info in dict_gene.iteritems():
        fot = info['ibaq'] / total_FOT_gene if total_FOT_gene != 0 else 0.0
        info['fot'] = fot * 1000000
        info['protein_gi'] = ';'.join(sorted(info['protein_gi']))
        gene_list.append(info)
        
    print 'Complete Caching(append protein & gene)........', time_now()
    
    return (ins_p, gene_list)
                
def getProGeneFromFile(results, dict_uni_pro, group_result, sid, eid, fdr, dict_pro_length):
    
    species = get_species(conn, meta, eid)
    taxid = get_taxid(conn, meta, eid)
    
    print 'Start Single file(get protein & gene).......', time_now()
    ins_p = []  # List of protein info
    ins_g = []  # List of gene info
    # parsed = 1
    hit = 1
    count = 0
    acc_noGID = 0
    acc_noGID_list = []
    set_sym = set()
    
    #print 'For pro in group_result...'
    for row in group_result:
        
        accession = row['accession']
        
        if '|' in accession:
            acc_short = accession.split('|')[1]
            prefix = accession.split('|')[0]
        else :
            acc_short = accession
            prefix = 'none'
            
        
        score = row['score']
        
        others = row['sameset']
        num_proteins = 1 if others == '' else len(others.split(';')) + 1
        
        desc_pro = results.getProteinDescription(accession)
        if desc_pro == None or desc_pro == '':
            desc_pro = get_desc_pro(conn, meta, acc_short, prefix)
                
        length = 0
        coverage = 0.0
        (mass_my, pro_seq) = get_pro_mass(conn, meta, acc_short, dict_aa_mass, prefix)
        ibaq_num = 0#get_ibaq_num(pro_seq)
        mass = results.getProteinMass(accession)
        if mass == 0: mass = mass_my
        if mass != 0:
            #length = get_pro_len(conn, meta, acc_short, prefix)
            length = dict_pro_length[accession]
            if length == 0:
                length = int(mass / 110)  # Must get length
            # coverage = float(prot.getCoverage()) / length
                
        symbol = ''
        desc = ''
        #=======================================================================
        # Get Gene Info
        #=======================================================================
        gid = getGeneID(conn, meta, acc_short, prefix, taxid) 
            
        # For PIG only
        if gid == -1 :
            acc_noGID += 1
            acc_noGID_list.append(accession)
            #print accession
            if 'Pig' in species or 'Sus scrofa' in species :
                gid = getPigGID(conn, meta, acc_short, prefix)
               
        if gid != -1:
            
            (symbol, desc) = getGeneDescSymbol(conn, meta, gid)
            # print hit,sid,symbol,desc
            tmp = {} 
            tmp['score'] = score
            tmp['search_id'] = sid
            tmp['symbol'] = symbol
            tmp['gene_id'] = gid
            tmp['protein_gi'] = accession if others == '' else accession + ';' + others
            tmp['num_proteins'] = num_proteins
            tmp['num_identified_proteins'] = num_proteins
            tmp['num_uni_proteins'] = num_proteins
            tmp['num_peptides'] = row['num_pep']
            tmp['num_uni_peptides'] = row['num_unipep']
            tmp['num_psms'] = row['pep_psms']
            tmp['area'] = row['area']
            tmp['fdr'] = fdr
            tmp['description'] = desc
            tmp['type'] = 1
            tmp['fot'] = 0.0    
            tmp['ibaq'] = ibaq_num
            ins_g.append(tmp)
                
        #=======================================================================
        # Protein Hit
        #=======================================================================
        tmp = {}    
        tmp['search_id'] = sid
        tmp['accession'] = accession
        tmp['other_members'] = others
        tmp['symbol'] = symbol
        tmp['description'] = desc_pro
        tmp['score'] = score
        tmp['coverage'] = coverage
        tmp['num_proteins'] = num_proteins
        tmp['num_uni_peptides'] = row['num_unipep']
        tmp['num_peptides'] = row['num_pep']
        tmp['num_psms'] = row['pep_psms']
        tmp['area'] = row['area']
        tmp['length'] = length
        tmp['mw'] = mass
        tmp['calc_pi'] = 0.0
        tmp['type'] = 1
        tmp['fdr'] = fdr      
        tmp['fot'] = 0.0
        tmp['ibaq'] = ibaq_num   
        ins_p.append(tmp)
        # RMS_error = prot.getRMSDeltas(results)
        # numDisplayPeptides = prot.getNumDisplayPeptides()
        count += 1           
        hit += 1
    
    print 'Proteins with no GID = ', acc_noGID
    #print acc_noGID_list 
    # print 'Min_score=', min_proscore
    print 'Pro_Num = ', count
    #===========================================================================
    # Process Gene list    
    #===========================================================================
    set_sym = set()
    dict_gene = {}
    
    for gg in ins_g:
        sym = gg['symbol'] 
        protein_gi = gg['protein_gi']

        if sym in set_sym:
            dict_gene[sym]['score'] += gg['score']
            dict_gene[sym]['protein_gi'].extend(protein_gi.split(';'))
            dict_gene[sym]['num_proteins'] += gg['num_proteins']
            dict_gene[sym]['num_identified_proteins'] += gg['num_identified_proteins']
            dict_gene[sym]['num_uni_proteins'] += gg['num_uni_proteins']
            dict_gene[sym]['num_peptides'] += gg['num_peptides']
            dict_gene[sym]['num_uni_peptides'] += gg['num_uni_peptides']
            dict_gene[sym]['num_psms'] += gg['num_psms']
            dict_gene[sym]['area'] += gg['area']
        else:
            set_sym.add(sym)
            tmp = {}
            tmp['score']        = gg['score']
            tmp['protein_gi']   = protein_gi.split(';')
            tmp['num_proteins'] = gg['num_proteins']
            tmp['num_identified_proteins'] = gg['num_identified_proteins']
            tmp['num_uni_proteins'] = gg['num_uni_proteins']
            tmp['num_peptides']     = gg['num_peptides']
            tmp['num_uni_peptides'] = gg['num_uni_peptides']
            tmp['num_psms'] = gg['num_psms']
            tmp['area']      = gg['area']
            tmp['search_id'] = gg['search_id']
            tmp['gene_id']   = gg['gene_id'] 
            tmp['symbol']    = sym
            tmp['fdr']       = gg['fdr']
            tmp['description'] = gg['description']
            tmp['type']        = gg['type']
            tmp['fot']         = gg['fot']
            tmp['ibaq']        = gg['ibaq']
            dict_gene[sym]     = tmp
            
    gene_list = []        
    for sym, info in dict_gene.iteritems():
        info['protein_gi'] = ';'.join(sorted(info['protein_gi']))
        gene_list.append(info)
            
    print 'Complete Single file(append protein & gene)........', time_now()
        
    return (ins_p, gene_list)
    
def percolatorRun(cmd):
    try:
        
        tmp_name = tempfile.NamedTemporaryFile(dir=".").name
        tmp_stderr = open(tmp_name, 'wb')
        # test = shlex.split(cmd)
        # print test
        proc = subprocess.Popen(args=cmd, shell=True, stderr=tmp_stderr.fileno())
        returncode = proc.wait()
        tmp_stderr.close()
        # Error checking.
        # if returncode != 0:
        #    s = text('delete from gardener_search where id=%s'%sid)
        #    conn.execution_options(autocommit=True).execute(s)
        #    raise Exception, "return code = %i" % returncode
        # else:
        # it may be too late to check for records in database after finish running the tool
        # mzXML or mzML
       
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
        print str(e)
        stop_err('Error running percolator.\n%s\n' % (str(e)))

# exit(0)

def mergePercolatorFile(tab_file, fea_file, type):
    flag = 1
    dict_percolator = {}
    dict_query_rank = {}
    f_tab = open(tab_file, 'r')
    for line in f_tab:
        if flag == 1:
            flag += 1
            continue
        line = line.split('\t')
        query_rank = line[0]
        qvalue = float(line[2])
        pepvalue = float(line[3])
        
        dict_query_rank[query_rank] = (qvalue, pepvalue)
    f_tab.close()

    f_fea = open(fea_file, 'r')
    # f_out = open(out,'w')
    zz = 0
    for line in f_fea:
        if flag == 2:
            flag += 1
            continue
        line = line.split('\t')
        query_rank = line[0]
        if query_rank not in dict_query_rank :
            continue
        # if query_rank[-1] != '1':#Maybe there is rank 11?
        #    continue
        label = line[1]
        if label != str(type) :
            continue
        mScore = float(line[2])
        # mScore = float(line[4])#when using RT parameter
        
        # if mScore < 10.0 :
        #    continue
        
        mrCalc = float(line[4])
        # mrCalc = float(line[6])#when using RT parameter
        seq = line[46][2:-2]
        # seq = line[48][2:-2]#when using RT parameter
        pros = line[47]
        # pros = line[49]#when using RT parameter
        # if len(seq) < 7 :
        #    continue 
        
        (qvalue, pepvalue) = dict_query_rank[query_rank]
        
        # if qvalue >= 0.01 :
        #    continue
        
        varMods = line[13]
        # varMods = line[15]#when using RT parameter
        # print query,rank,label,seq,mScore,mrCalc
        query = query_rank.split(';')[0][6:]
        tmp = {}
        # tmp['query'] = int(query)
        tmp['qvalue'] = qvalue
        tmp['pepvalue'] = pepvalue
        tmp['seq'] = seq
        tmp['mScore'] = mScore
        tmp['mrCalc'] = mrCalc
        tmp['varMods'] = varMods
        # dict_percolator[int(query)] = tmp
        dict_percolator[query_rank] = tmp
        zz += 1
        # f_out.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\n'%(query,qvalue,seq,mScore,mrCalc,varMods,pros))
    f_fea.close() 
    # f_out.close()
    print 'non-redundant[type=%s] %s' %(type, zz)
    print 'len(dict_percolator)(has redundant):', len(dict_percolator)
    
    return dict_percolator

def percolatorPSMs(input, tmpname):
    dat_name = os.path.basename(input)
    temp_path = os.path.join(GALAXY_ROOT, 'database/files/mascot_percolator', tmpname)
    output_print = os.path.join(temp_path, '%s.print.txt'%dat_name)
    log_file = os.path.join(temp_path, '%s.log.txt'%dat_name)
    tab_file = os.path.join(temp_path, '%s.tab.txt'%dat_name)
    decoy_tab_file = os.path.join(temp_path, '%s_decoy.tab.txt'%dat_name)
    fea_file = os.path.join(temp_path, '%s.features.txt'%dat_name)
    out = os.path.join(temp_path, 'pep_out_%s.txt'%dat_name)
    
    MPercolatorPath = os.path.join(GALAXY_ROOT, '..', 'external_tools/MascotPercolator2.02')
    cmd = 'export LC_ALL=C;cd %s; ' %MPercolatorPath
    cmd += 'java -cp MascotPercolator.jar cli.MascotPercolator '
    cmd += '-features -chargefeature -rankdelta 1 -u '
    cmd += '-target %s ' %input
    cmd += '-decoy %s ' %input
    cmd += '-out %s' %os.path.join(temp_path, dat_name)
    cmd += ' > %s' %output_print
    print '='*20
    print cmd 
    print '='*20
    if not os.path.exists(temp_path): 
        print temp_path + ' doesn\'t exist!'
        os.makedirs(temp_path)
        
    if os.path.isfile(decoy_tab_file):
        print 'percolator file existed....\n'
    else:
        print 'start percolator....\n'
        if os.path.isfile(fea_file):os.remove(fea_file)
        if os.path.isfile(tab_file):os.remove(tab_file)
        if os.path.isfile(log_file):os.remove(log_file)
        if os.path.isfile(output_print):os.remove(output_print)
        percolatorRun(cmd)
        
    dict_percolator       = mergePercolatorFile(tab_file,       fea_file,  1)
    dict_percolator_decoy = mergePercolatorFile(decoy_tab_file, fea_file, -1)
    '''
    f = open(out, 'w')
    for query, pep in dict_percolator.items():
        f.write(str(query) + '\t' + pep['seq'] + '\t' + str(pep['qvalue']) + '\t' + str(pep['mScore']) + '\n')
    f.close()
    '''
    # exit(0)
    return (dict_percolator, dict_percolator_decoy)
'''
Below is the main function
'''    
def parseMascotDat(options, file_data):
    if options.store_to_db == 'no':
        print '\nStart cache directly.'
        return 0
    """ Now begin to parser .dat """
    print 'Start(parsing DAT)!', time_now()
    dRT = options.dRT
    dMZ = options.dMZ
    max_hit = options.max_hit
    msparser_min_ionscore = 7#
    ionThres = options.min_ion
    fdrThres = options.min_fdr 
    
    # print 'Parameters:',dRT,dMZ,min_ionscore,max_hit
    e_name = 'Exp%s' % file_data['exp_id']
    eid = file_data['exp_db_id']
    sid = file_data['search_id'] 
    e_num = file_data['exp_id']
    f_num = file_data['f_num']
    r_num = file_data['r_num']
    #species = get_species(conn, meta, eid)
    # job_id = file_data['job_id']

    (dict_percolator, dict_percolator_decoy) = percolatorPSMs(options.input, 'E%s_F%s_R%s' % (e_num, f_num, r_num))
    
    resfile = msparser.ms_mascotresfile(options.input)
    if not resfile.isValid() : 
        stop_err('Error: Invalid Mascotdat file.\n') 
    searchparams = msparser.ms_searchparams(resfile)
    msresFlags = msparser.ms_mascotresults.MSRES_MUDPIT_PROTEIN_SCORE | msparser.ms_mascotresults.MSRES_GROUP_PROTEINS | msparser.ms_mascotresults.MSRES_MAXHITS_OVERRIDES_MINPROB
    msresFlags_decoy = msparser.ms_mascotresults.MSRES_MUDPIT_PROTEIN_SCORE | msparser.ms_mascotresults.MSRES_GROUP_PROTEINS | msparser.ms_mascotresults.MSRES_MAXHITS_OVERRIDES_MINPROB | msparser.ms_mascotresults.MSRES_DECOY
    #===========================================================================
    """ Parse [.dat] using ms_parser """
    #===========================================================================
    results = msparser.ms_peptidesummary(
            resfile,
            msresFlags,
            0,  # minProteinProb
            max_hit,  # maxHits
            "",  # UniGeneFile
            msparser_min_ionscore,  # minIonsScore
            7  # minPepLenInPepSummary
           )
    
    results_decoy = msparser.ms_peptidesummary(
            resfile,
            msresFlags_decoy,
            0,  # minProteinProb
            max_hit,  # maxHits
            "",  # UniGeneFile
            msparser_min_ionscore,  # minIonsScore
            7  # minPepLenInPepSummary
           )
    
    filename = file_data['name'].split('_E%s_F' %e_num)[0]
    maxRank = results.getMaxRankValue()
    NumQueries = resfile.getNumQueries()
    #===========================================================================
    """ Get peptides from .dat file """
    #===========================================================================
    (peps_real, ms2_id_decoy) = getPeptides(sid, filename, resfile, results, searchparams, NumQueries, msparser_min_ionscore, dict_percolator, maxRank)
    del dict_percolator
    #===========================================================================
    """ Calculate area of every peptide(psms) """
    #===========================================================================
    peps_real = calcAreas(file_data, options, dRT, dMZ, peps_real)
    #exit(0)
    #===========================================================================
    """ Get decoy peptides from .dat file """
    #===========================================================================
    peps_decoy = getDecoyPeps(sid, filename, resfile, results_decoy, searchparams, NumQueries, msparser_min_ionscore, dict_percolator_decoy, ms2_id_decoy, maxRank)
    del dict_percolator_decoy
    #===========================================================================
    """ Assemble proteins """
    #===========================================================================
    (group_result, qvalueThres, FDR, dict_uni_pro, set_pep_index, pga_peptide, dict_pro_length) = startProteinAssemble(eid, peps_real, peps_decoy, fdrThres, ionThres)
    
    (proteins, genes) = getProGeneFromFile(results, dict_uni_pro, group_result, sid, eid, FDR, dict_pro_length)
    del dict_uni_pro
    del group_result
    # exit(0)
    # distributeAreas(ins_pep, ins_p, ins_g)

    #===========================================================================
    """ Clear old data """
    #===========================================================================
    s = 'delete from gardener_peptide where search_id=%s' % sid
    conn.execution_options(autocommit=True).execute(s)
    s = 'delete from gardener_protein where search_id=%s' % sid
    conn.execution_options(autocommit=True).execute(s)
    s = 'delete from gardener_gene where search_id=%s' % sid
    conn.execution_options(autocommit=True).execute(s)
    #===========================================================================
    """ Write DB """
    #===========================================================================
    print 'Start(write peptide,protein,gene)!', time_now()

    try:  
        if len(peps_real) != 0:
            peps_real.extend(peps_decoy)
            peps_real.sort(key=lambda x:x['ion_score'], reverse=1)
            insertGeneral('gardener_peptide', peps_real)
        del peps_real
        #print proteins[:100]
        if len(proteins) != 0:
            insertGeneral('gardener_protein', proteins)
        del proteins  
            
        if len(genes) != 0:
            insertGeneral('gardener_gene', genes)
    except Exception, e:
        s = 'delete from gardener_peptide where search_id=%s' % sid
        conn.execution_options(autocommit=True).execute(s)
        s = 'delete from gardener_protein where search_id=%s' % sid
        conn.execution_options(autocommit=True).execute(s)
        s = 'delete from gardener_gene where search_id=%s' % sid
        conn.execution_options(autocommit=True).execute(s)
        stop_err('Error writing peptide,protein,gene tables.\n%s\n' % (str(e)))  
    
    print 'Complete(write)!', time_now()        
    return 0 

def rep_to_exp(sid, data_list, pep_pro_gene, stype):           
    for tmp in data_list:
        tmp['search_id'] = sid
    s = 'delete from gardener_%s_%s where search_id=%s' % (stype, pep_pro_gene, sid)
    conn.execution_options(autocommit=True).execute(s)
    insertCache(stype, pep_pro_gene, data_list)
    
    return 0     
            
def cacheGene(file_data, genes, stype, sid):
    # updateExpStage(conn,meta,file_data)
    
    eid = file_data['exp_db_id']
    rid = file_data['r_num']
    rank = file_data['rank']
    print 'Exp ID %s Rep %s Rank %s Type %s' % (eid, rid, rank, stype)
    
    gene_num = len(genes)
    print 'All genes = %s' % gene_num 
    #===========================================================================
    """ Write DB """
    #===========================================================================
    s = 'delete from gardener_%s_gene where search_id=%s' % (stype, sid)
    conn.execution_options(autocommit=True).execute(s)
    # print genes
    if gene_num == 0:
        return 0
    insertCache(stype, 'gene', genes)
    
    return gene_num

def cacheProtein(file_data, stype, fdrThres, ionThres):
    # updateExpStage(conn,meta,file_data)
    #t1 = datetime.datetime.now()
    print '\nStart cacheProtein...ionThres=',ionThres
    
    eid = file_data['exp_db_id']
    rid = file_data['r_num']
    rank = file_data['rank']
    print '[Exp ID %s] [Rep %s] [Rank %s] [Type %s]' % (eid, rid, rank, stype)
    
    if stype == 'exp':
        sid = get_cache_exp_sid(conn, meta, file_data)

    elif stype == 'repeat':
        sid = get_cache_rep_sid(conn, meta, file_data)
    
    peptide_list   = getPepFromDB(eid, rid, rank,  1, stype, ionThres)
    pep_list_decoy = getPepFromDB(eid, rid, rank, -1, stype, ionThres)
    #peptide_list = []        
    (group_result, qvalueThres, fdr, dict_uni_pro, set_pep_index, pga_peptide, dict_pro_length) = startProteinAssemble(eid, peptide_list, pep_list_decoy, fdrThres, ionThres)
    
    (proteins, genes) = getProGeneFromDB(dict_uni_pro, group_result, sid, eid, fdr, dict_pro_length)
   
    num_pro = len(proteins)
    print 'proteins num = %s' % num_pro
    if num_pro == 0:
        return (sid, qvalueThres, [], peptide_list, set(), {}, 0, [])
    
    proteins.sort(key=lambda x:x['score'], reverse=True)
    #===========================================================================
    """ Write file """
    #===========================================================================
    #===========================================================================
    # out_file = '/usr/local/galaxyDATA01/galaxy-dist/database/files/%s_%s_ionscore_%s_fdr_%s.txt'%(stype,file_data['name'],ionThres,fdrThres)
    # with open(out_file, 'w') as f:
    #     f.write('\t'.join(['search_id','accession','other_members','symbol','description','score','coverage','num_proteins',
    #                        'num_uni_peptides','num_peptides','num_psms','area','length','mw','calc_pi','type',
    #                        'fdr','fot','ibaq','annotation','modification']) + '\n')
    #     for tmp in proteins:
    #         sid = tmp['search_id'] 
    #         accession = tmp['accession'] 
    #         others = tmp['other_members'] 
    #         symbol = tmp['symbol'] 
    #         desc_pro = tmp['description'] 
    #         score = tmp['score'] 
    #         coverage = tmp['coverage'] 
    #         num_proteins = tmp['num_proteins'] 
    #         n_u_pep = tmp['num_uni_peptides'] 
    #         n_pep = tmp['num_peptides'] 
    #         n_psms = tmp['num_psms'] 
    #         pro_area = tmp['area'] 
    #         length = tmp['length'] 
    #         mass = tmp['mw']  
    #         calc_pi = tmp['calc_pi'] 
    #         type = tmp['type'] 
    #         fdr = tmp['fdr'] 
    #         fot = tmp['fot'] 
    #         ibaq = tmp['ibaq'] 
    #         anno = tmp['annotation'] 
    #         modif_status = tmp['modification'] 
    #     
    #         line = '\t'.join([str(sid),accession,others,symbol,desc_pro,
    #                          str(score),str(coverage),str(num_proteins),str(n_u_pep),str(n_pep),
    #                          str(n_psms),str(pro_area),str(length),str(mass),str(calc_pi),str(type),
    #                          str(fdr),str(fot),str(ibaq),anno,modif_status])
    #         f.write(line + '\n')  
    # exit(0)
    #===========================================================================
    
    #===========================================================================
    """ Write DB """
    #===========================================================================

    
    s = 'delete from gardener_%s_protein where search_id=%s' % (stype, sid)
    conn.execution_options(autocommit=True).execute(s)
    
    insertCache(stype, 'protein', proteins)  
    

    # update_cache_info(conn,meta,file_data,temp['search_id'])       
    # return pro_list,area_pro,psms_pro,dict_p,s_pro
    return (sid, qvalueThres, proteins, peptide_list, set_pep_index, pga_peptide,num_pro, genes)
   
def cachePeptide(file_data, stype, qvalueThres, ionThres, sid, redundant_pep, set_pep_index, pga_peptide) :

    # updateExpStage(conn,meta,file_data)
    
    eid = file_data['exp_db_id']
    rid = file_data['r_num']
    rank = file_data['rank']
    print '[Exp ID %s] [Rep %s] [Rank %s] [Type %s]' % (eid, rid, rank, stype)
    
    #redundant_pep = getPepFromDB(eid, rid, rank, 1, stype, ionThres)
    a = []
    total_FOT = 0.0
    pep_has_pro = {}
    set_tmp = set()
    for i in set_pep_index:# set_pep_index is a set() !!!!!!
        peptide_dict = redundant_pep[i]
        area = peptide_dict['area']
        total_FOT += area
        seq = peptide_dict['sequence']
        mod = peptide_dict['modification']
        seq_mod = (seq, mod)
        ion_score = peptide_dict['ion_score']
        q_value = peptide_dict['q_value']
        flag = 0
        if seq_mod in set_tmp:
            pep_has_pro[seq_mod]['num_psms'] += 1
            pep_has_pro[seq_mod]['area'] += area
            if q_value < pep_has_pro[seq_mod]['q_value']:
                flag = 1
            elif q_value == pep_has_pro[seq_mod]['q_value'] and ion_score > pep_has_pro[seq_mod]['ion_score']:
                flag = 1
            if flag == 1:
                pep_has_pro[seq_mod]['ms2_id']    = peptide_dict['ms2_id']
                pep_has_pro[seq_mod]['quality']   = peptide_dict['quality']
                pep_has_pro[seq_mod]['type']      = peptide_dict['type']
                pep_has_pro[seq_mod]['delta_cn']  = peptide_dict['delta_cn']
                pep_has_pro[seq_mod]['q_value']   = q_value
                pep_has_pro[seq_mod]['pep']       = peptide_dict['pep']
                pep_has_pro[seq_mod]['ion_score'] = ion_score
                pep_has_pro[seq_mod]['exp_value'] = peptide_dict['exp_value']
                pep_has_pro[seq_mod]['charge']    = peptide_dict['charge']
                pep_has_pro[seq_mod]['mh_da']     = peptide_dict['mh_da']
                pep_has_pro[seq_mod]['delta_m_ppm'] = peptide_dict['delta_m_ppm']
                pep_has_pro[seq_mod]['rt_min']    = peptide_dict['rt_min']
                pep_has_pro[seq_mod]['num_missed_cleavages'] = peptide_dict['num_missed_cleavages']
                pep_has_pro[seq_mod]['type']      = peptide_dict['type']
                pep_has_pro[seq_mod]['from_where'] = peptide_dict['from_where']
            
        else:
            set_tmp.add(seq_mod)
            pga_set = pga_peptide[seq.upper()]
            num_proteins = len(pga_set)
            num_protein_groups= len(pga_set)
            pga = ';'.join(sorted(pga_set))
            pep_d = {}
            pep_d['ms2_id']    = peptide_dict['ms2_id']
            pep_d['search_id'] = sid
            pep_d['quality']   = peptide_dict['quality']
            pep_d['sequence']     = seq
            pep_d['modification'] = mod
            pep_d['type']         = peptide_dict['type']
            pep_d['num_proteins'] = num_proteins
            pep_d['num_protein_groups'] = num_protein_groups
            pep_d['protein_group_accessions'] = pga
            pep_d['delta_cn']  = peptide_dict['delta_cn']
            pep_d['q_value']   = peptide_dict['q_value']
            pep_d['pep']       = peptide_dict['pep']
            pep_d['ion_score'] = ion_score
            pep_d['exp_value'] = peptide_dict['exp_value']
            pep_d['charge']    = peptide_dict['charge']
            pep_d['mh_da']     = peptide_dict['mh_da']
            pep_d['delta_m_ppm'] = peptide_dict['delta_m_ppm']
            pep_d['rt_min']      = peptide_dict['rt_min']
            pep_d['num_missed_cleavages'] = peptide_dict['num_missed_cleavages']
            pep_d['type'] = peptide_dict['type']
            pep_d['from_where'] = peptide_dict['from_where']
            pep_d['num_psms'] = 1
            pep_d['area'] = area
            pep_d['fot'] = 0.0
            pep_d['fdr'] = 0.0
            pep_has_pro[seq_mod] = pep_d
            
    peptides_list = []        
    for seq_mod, dict_peplist in pep_has_pro.iteritems():
        area = dict_peplist['area']
        fot = area / total_FOT if total_FOT != 0 else 0.0
        fot = fot * 1000000
        dict_peplist['fot'] = fot
        peptides_list.append(dict_peplist)      
        
    print '\ntotal_FOT=',total_FOT

    #===========================================================================
    """ Calc FDR """
    #===========================================================================
    num_pep = len(peptides_list)
    print 'All peptides = ',num_pep
    #print 'Decoy=%s and All peptides=%s' % (delta, pep_all)
    #num_pep = pep_all - delta
    #if num_pep <= 0:
    if num_pep == 0:
        return (0, [])   
    
    #fdr = delta / num_pep
    peptides_list.sort(key=lambda x:x['ion_score'], reverse=True)
    #for x in peptides:
    #    x['fdr'] = fdr
    #print 'FDR_PEPTIDE=', fdr    
    #===========================================================================
    """ Write DB """
    #===========================================================================
    s = 'delete from gardener_%s_peptide where search_id=%s' % (stype, sid)
    conn.execution_options(autocommit=True).execute(s)
    
    insertCache(stype, 'peptide', peptides_list)
    # print peptides[0:10]
    # update_cache_info(conn,meta,file_data,temp['search_id'])
    # return pep_list

    return (num_pep, peptides_list)

def storeDB(conn, meta, file_data, options):
    fdrThres = options.min_fdr 
    ionThres = options.min_ion
    file_data['date'] = date_now()  # time.strftime("%Y-%m-%d %X", time.gmtime())
    
    update_search_fraction(conn, meta, file_data)
     
    # stage,file_data['num_spec']= updateExpStage(conn,meta,file_data)#,file_data['num_pep'],file_data['num_pro'],file_data['num_gen'] 
    
    """ Start cache Repeat """
    r_num = int(file_data['r_num'])
    f_num = int(file_data['f_num'])
    if f_num != file_data['fractionNum']:
        print 'Not the last fraction of repeat %s.' %r_num
        return 0
    
    stage_rep = isRepDone(conn, meta, file_data)
    
    wait_time = 1
    while stage_rep != 5:
        if options.forceCache:break
        if wait_time > WAIT_TIMES:
            stop_err('wait too long(rep).')
        time.sleep(100)
        wait_time += 1
        stage_rep = isRepDone(conn, meta, file_data)

    print '\nStart caching Rep[%s]...' % r_num, time_now()  
    stype = 'repeat'  
    file_data['num_spec'] = getRepSpecNum(conn, meta, file_data)  # ,file_data['num_pep'],file_data['num_pro'],file_data['num_gen']
            
    (sid, qvalueThres, proteins, redundant_pep, set_pep_index, pga_peptide, num_pro, genes) = cacheProtein(file_data, stype, fdrThres, ionThres)
    
    (num_pep, peptides) = cachePeptide(file_data, stype, qvalueThres, ionThres, sid, redundant_pep, set_pep_index, pga_peptide)      
    del redundant_pep
    del set_pep_index
    del pga_peptide
    
    num_gene = cacheGene(file_data, genes, stype, sid)
    
    file_data['num_pep'] = num_pep
    file_data['num_pro'] = num_pro
    file_data['num_gen'] = num_gene
       
    update_cache_info(conn, meta, file_data, sid)  # update_rep_stage(conn, meta, file_data,sid)
    total_time = update_time_used(conn, meta, sid, file_data)
    
    print 'Complete caching Rep[%s]...\n' % r_num, time_now()        
    #===========================================================================
    """ When Repeat == 1, no need to cache experiment """   
    #===========================================================================
    max_repeat = file_data['repeatNum']#getMaxRepeat(conn, meta, file_data['exp_db_id'])
    if max_repeat == 1:
        stype = 'exp'
        sid = get_cache_exp_sid(conn, meta, file_data) 
        
        if num_pep > 0:
            rep_to_exp(sid, peptides, 'peptide', stype)
        
        if num_pro > 0:
            rep_to_exp(sid, proteins, 'protein', stype)
        
        if num_gene > 0:
            rep_to_exp(sid, genes, 'gene', stype)
        
        update_cache_info(conn, meta, file_data, sid)
        updateExpTable(conn, meta, file_data)
        updateExpStage(conn, meta, file_data)
        send_complete_mail('jobs@firmiana.org','Exp'+file_data['exp_id']+' done','Congratulations,workflow completed in %s hours!'%total_time)
   
        print 'Complete caching Exp(from repeat=1)...', time_now() 
        return 0        
    #===========================================================================
    """ Start cache experiment """   
    #===========================================================================
    if r_num != max_repeat:
        print 'Not the last repeat.'
        return 0
    
    stage_exp = isExpDone(conn, meta, file_data)
    wait_time = 1
    while stage_exp != 5:
        if options.forceCache:break
        if wait_time > WAIT_TIMES:
            stop_err('wait too long(exp).')
        time.sleep(100)
        wait_time += 1
        stage_exp = isExpDone(conn, meta, file_data)
        
    print 'Start caching Exp...', time_now()    
    stype = 'exp'
    file_data['num_spec'] = getExpSpecNum(conn, meta, file_data['exp_db_id'])    
            
    (sid, qvalueThres, proteins, redundant_pep, set_pep_index, pga_peptide, num_pro, genes) = cacheProtein(file_data, stype, fdrThres, ionThres)
    
    (num_pep, peptides) = cachePeptide(file_data, stype, qvalueThres, ionThres, sid, redundant_pep, set_pep_index, pga_peptide)      
    del redundant_pep
    del set_pep_index
    del pga_peptide
    del peptides
    
    num_gene = cacheGene(file_data, genes, stype, sid)
    
    file_data['num_pep'] = num_pep
    file_data['num_pro'] = num_pro
    file_data['num_gen'] = num_gene
     
    update_cache_info(conn, meta, file_data, sid)
    updateExpTable(conn, meta, file_data)
    updateExpStage(conn, meta, file_data)
    
    #===========================================================================
    # send_complete_mail(file_data['email'],'Exp'+file_data['exp_id']+' done','Congratulations,workflow completed in %s hours!'%total_time)
    # 
    # print 'Complete caching Exp...', time_now()
    # 
    #===========================================================================
    return 0

def __main__() :
     
    parser = optparse.OptionParser()
    parser.add_option('-i', '', dest='input', help=' ')
    parser.add_option('-o', '', dest='output', help='')
    parser.add_option('-u', '--user_id', dest='user_id', action='store', type="string", help='User id for galaxy runner.')
    parser.add_option('-a', '--label_name', dest='label_name', action='store', type="string", help='Label name for out file.')
    parser.add_option('', '--rank', dest='rank', action='store', type="int", help='Specify the rank.')
    parser.add_option('', '--min_fdr', dest='min_fdr', action='store', type="float", help='')
    parser.add_option('', '--min_ion', dest='min_ion', action='store', type="int", help='')
    parser.add_option('', '--max_hit', dest='max_hit', action='store', type="int", help='')
    parser.add_option('', '--dMZ', dest='dMZ', action='store', type="int", help='')
    parser.add_option('', '--dRT', dest='dRT', action='store', type="int", help='')
    parser.add_option('', '--store_to_db', dest='store_to_db', action='store', help='')
    
    parser.add_option('', '--forceCache', dest='forceCache', action='store', type='int',help='')
    (options, args) = parser.parse_args()
    print 'Processing mascotdat:\n', options.input
    
    (file_data, rank) = sql_gardener_file(options, conn, meta)
    
    if rank == 0:
        parseMascotDat(options, file_data)
     
    storeDB(conn, meta, file_data, options)
    
if __name__ == "__main__": __main__()
