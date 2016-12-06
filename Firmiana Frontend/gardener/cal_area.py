from sqlFunc import *

import sys, optparse, os, tempfile, subprocess, shutil, re, math
from numpy import array, repeat, concatenate, ones, zeros, arange, reshape, put, add, dot, take, float32
from numpy.linalg import pinv
from scipy.signal.signaltools import lfilter
import numpy as np
import numpy


NFS89_dir = os.path.join( os.path.dirname( __file__ ), '..','..','NFS_89')

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

def calcAreas(sid, filename, dRT, dMZ, ins_pep):
    if not os.path.isfile('%s/NFS_192.168.12.89' %NFS89_dir):
        print 'NFS folder error!'
        exit(1)
    print 'Start(calculating areas)Reading txt......', time_now()
    # RtList = []
    result = []
    #sid = file_data['search_id']
    DataBase = []
    #filename = file_data['name']
    dir = '%s/ms_peak/%s/' % (NFS89_dir, filename)  # Dir of .txt files of peaks
    dir_MS1 = '%s/ms_peak/%s/MS1.txt' % (NFS89_dir, filename)  # Dir of .txt files of peaks
    #files = os.listdir(dir)
    filedict = {}
    i = -1
    ms_no_old = 0
    file_lines = []
    #fileLength = len(files)
    ###############################################
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
            
            with open(dir + peak_file) as f:
                for line in f:
                    (ms_no, mz_temp, intensity_temp) = line.split(',')
                    temp = (int(ms_no), float(mz_temp), float(intensity_temp))
                    tt.append(temp)
            
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
        # from views.py   -->  temp_list.append([area, fot, rt, mz, num_psms, ion_score])
        # pep_info.append((rt, mz))
        pep_info.append((row[0], row[1],row[2], row[3]))
        
    print 'for pep_index in range(PepNum)......'
    for pep_index in range(PepNum):
        area_origin = pep_info[pep_index][0]
        fot = pep_info[pep_index][1]
        if area_origin !=0 :
            continue
        # print 'pep_index',pep_index
        #charge = pep_info[pep_index][5]
        rt_ms1 = pep_info[pep_index][2]
        mz_ms1 = pep_info[pep_index][3]
        
        QuantTable = []
        RTList = []
        IDTable = []
        #ms2_id = pep_info[pep_index][0]
        # print 'pep_index=%s,ms2_id=%s'%(pep_index,ms2_id)
        # mz_ms1 = allpep[pep_index]['mz_ms1']
        #(mz_ms1, rt_ms1) = get_mz_rt(conn, meta, ms2_id)  # conn.execution_options(autocommit=True).execute('select pre_mz,rt from gardener_ms2 where id=%s'%ms2_id).fetchone()

        lt, gt = rt_ms1 + dRT, rt_ms1 - dRT
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
            less, more = mz_ms1 * (1 - dMZ / 1e6), mz_ms1 * (1 + dMZ / 1e6)
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
        ins_pep[pep_index][0] = areas
                    
        #rr = 'sid=%s\t%s\t%s_%s\t%s\t%s\n' %(str(sid), pep_index, pep_info[pep_index][2], charge, areas, time_now()) 
        #rr = rr + ' qt=' + rt + ' rt=' + rm + '\n'
        #result.append(rr)
    del DataBase 
    #print 'Write peptide areas into output...'                         
    #f = open('area_out.txt', 'w')
    #for r in result:
    #    f.write(r)
    #f.close()
    #print 'Complete calculating areas !', time_now()
    
    #gc.collect() 
    #exit(0)
    return ins_pep

def __main__() :
    print time_now()
    dRT, dMZ = 60, 10
    #file_data = {}
    #file_data['search_id'] = 9141
    #file_data['name'] = '83329_Lung_cancer_T_25per_loading_F6_R1_E000712_F6_R1'
    
    '''
    This peptide list comes from msparser
    
    ms2_id -> ms2 RT & M/Z
    
    '''
    #===========================================================================
    # for row in ins_pep:
    #     PepNum += 1
    #     pep_info.append((row['ms2_id'], row['search_id'], row['sequence'], row['modification'], row['charge']))
    #===========================================================================
    search_id = 9141
    filename = '83329_Lung_cancer_T_25per_loading_F6_R1_E000712_F6_R1'
    
    ins_pep = []
    #[area, fot, rt, mz, num_psms, ion_score]
    #===========================================================================
    # tmp = {}
    # tmp['mz'] = 677.356014255044
    # tmp['rt'] = 2662.81
    # tmp['search_id'] = search_id
    # tmp['sequence'] = 'LIIWDSYTTNK'
    # tmp['modification'] = ''
    # tmp['charge'] = 2
    # ins_pep.append(tmp)
    # 
    # tmp = {}
    # tmp['mz'] = 515.607560591766
    # tmp['rt'] = 4120.01
    # tmp['search_id'] = search_id
    # tmp['sequence'] = 'SFLEEVLASGLHSR'
    # tmp['modification'] = ''
    # tmp['charge'] = 3
    # ins_pep.append(tmp)
    #===========================================================================
    tmp = [0,0,2662.81,677.356014255044,0,0]
    ins_pep.append(tmp)
    
    tmp = [0,0,4120.01,515.607560591766,0,0]
    ins_pep.append(tmp)
    
    
    ins_pep = calcAreas(search_id, filename, dRT, dMZ, ins_pep)
    
    print ins_pep
    
    print 'Done'
    print time_now()
    
if __name__ == "__main__": __main__()