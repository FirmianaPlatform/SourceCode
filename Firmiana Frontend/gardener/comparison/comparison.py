import gardener.models
from gardener.models import *
import pdb
import datetime
def newcmp_calc(id):
    # return 0
    t1 = datetime.datetime.now()
    def my_timer(t2, t1):
        return float((t2 - t1).seconds) + (t2 - t1).microseconds / 1000000.0
    
    def print_delta_time(t1, msg):
        msg = msg if msg else 'Till now'
        t2 = datetime.datetime.now()
        delta = my_timer(t2, t1)  # float((t2 - t1).seconds) + (t2 - t1).microseconds / 1000000.0
        print '%s used %.3f seconds' % (msg, delta)
    
    def set2str(tempset):
        tempstr = ''
        for aa in tempset:
            tempstr = tempstr + str(aa) + ';'
        tempstr = tempstr[:-1]
        return tempstr
    
    def get_coeRT(info, all_pep):           
        coeRT = []
        for exp1 in range(len(info)):
            temp = []
            rt1 = []
            rt2 = []
            for exp2 in range(len(info)):
                if exp1 != exp2:
                    for pep in range(len(all_pep)):
                        if info[exp1][pep][0] != 0 and info[exp2][pep][0] != 0:  # peptidearea
                            rt1.append(info[exp1][pep][2]) 
                            rt2.append(info[exp2][pep][2])
                    calc1 = polyfit(rt1, rt2, 1)
                    calc2 = polyfit(rt1, rt2, 2)
                    if calc1['determination'] >= calc2['determination']:
                        temp.append(calc1)
                    else:
                        temp.append(calc2)
                else:
                    temp.append('')
                    
            coeRT.append(temp)
        
        ''' fullfil RT '''
        for exp1 in range(len(info)):
            for pep_idx in range(len(all_pep)):
                # every peptide in exp
                if info[exp1][pep_idx] == [0, 0, 0, 0, 0, 0]:
                    # compare with any other exp
                    for exp2 in range(len(info)):
                        if exp1 == exp2:continue
                        if info[exp2][pep_idx] != [0, 0, 0, 0, 0, 0]:
                            temprt = np.polyval(coeRT[exp1][exp2]['polynomial'], info[exp2][pep_idx][2])
                            info[exp1][pep_idx] = [0, 0, temprt, info[exp2][pep_idx][3], info[exp2][pep_idx][4], info[exp2][pep_idx][5]]
                            # temp_list.append([tempPep.area, tempPep.fot, tempPep.rt_min, mz, tempPep.num_psms, tempPep.ion_score])
        
    pdb.set_trace()           
    t1 = datetime.datetime.now()
    csvname = id
    jobNow=XsearchTable.objects.get(id=int(csvname))
    pep_pro_gen =jobNow.ProGene
    repeatList = jobNow.searchs
    ion_score = float(jobNow.ionscore)
    dmz = float(jobNow.dmz)
    drt = float(jobNow.drt)
    qc = jobNow.qc
    compare = jobNow.compare
    
    repeatList = repeatList.split(';')[:-1]
    repeatLENGTH = len(repeatList)
    print 'Repeat Contains %d repeat' % repeatLENGTH
    
    proList = set()
    pepList = set()
    geneList = set()

    if 1:  # not qc:
        for repeat in repeatList:
            temp = repeat.split('_')
            (type, exp, rank, repe) = (temp[0], int(temp[1]), int(temp[2]), int (temp[3]))
            id = Search.objects.filter(exp_id=exp).filter(rank=rank).filter(repeat_id=repe).filter(type='rep')[0].id

            tempProList = Repeat_Protein.objects.filter(search_id=id).exclude(type=-1)
            for pro in tempProList:
                proList.add((pro.accession, pro.symbol, pro.description))
            tempPepList = Repeat_Peptide.objects.filter(search_id=id).filter(ion_score__gt=ion_score).exclude(type=-1)
            for pep in tempPepList:
                pepList.add((pep.sequence, pep.modification))

            tempGeneList = Repeat_Gene.objects.filter(search_id=id).exclude(type=-1)
            for gene in tempGeneList:
                geneList.add((gene.gene_id, gene.symbol, gene.description))

    else:  # After QC
        pass
    
    print_delta_time(t1, 'get list done!')
    pdb.set_trace()
    
    proList = list(proList)
    pepList = list(pepList)
    print 'len(pepList)=', len(pepList)
    geneList = list(geneList)

    
    ''' matrix '''
    proTable = []
    pepTable = []
    geneTable = []

    ''' For index '''
    proListForIndex = []
    geneListForIndex = []
    
    geneAnno = {}
    proAnno = {}
    
    pep2pro = []
    pep2gen = []
    
    for pro in proList:
        proListForIndex.append(pro[0])  # pro[0] = accession
    for gene in geneList:
        geneListForIndex.append(gene[1])  # gene[1] = symbol
        
    # LogFile=open(quant_dir+'logs/log.txt','w')
    if 1:  # not compare:
        ''' get geneTable '''
        for repeat in repeatList:
            temp = []
            tempList = repeat.split('_')
            (type, exp, rank, repe) = (tempList[0], int(tempList[1]), int(tempList[2]), int (tempList[3]))
            
            id = Search.objects.filter(exp_id=exp).filter(rank=rank).filter(repeat_id=repe).filter(type='rep')[0].id
            tempGenList = Repeat_Gene.objects.filter(search_id=id).exclude(type=-1)
            
            for gen in geneList:
                (gene_id, symbol, description) = list(gen)
                tmp_obj_gene = tempGenList.filter(symbol=symbol)
                if tmp_obj_gene:
                    tempGen = tmp_obj_gene[0]
                    temp.append([tempGen.area, tempGen.fot, tempGen.ibaq, 0])  # tempGen.num_psms now not available!
                    geneAnno[symbol] = tempGen.annotation
                else:
                    temp.append([-1, -1, -1, -1])
            geneTable.append(temp)
        # print len(geneTable)
        # peptidelist
        geneTable.append([])
        
        for gen in geneList:
            geneTable[-1].append(set()) 
            
        print_delta_time(t1, 'Gene done!')
        
        
        ''' get proTable '''
        repeat_idx = 0
        for repeat in repeatList:
            temp = []
            tempList = repeat.split('_')
            (type, exp, rank, repe) = (tempList[0], int(tempList[1]), int(tempList[2]), int (tempList[3]))
            id = Search.objects.filter(exp_id=exp).filter(rank=rank).filter(repeat_id=repe).filter(type='rep')[0].id
            # LogFile.write(str(id)+'\n')
            tempProList = Repeat_Protein.objects.filter(search_id=id).exclude(type=-1)
            for pro in proList:
                # if filter(pro):
                (acc, sym, des) = list(pro)
                
                tmp_obj_protein = tempProList.filter(accession=acc).filter(symbol=sym).filter(description=des)
                if tmp_obj_protein:
                    tempPro = tmp_obj_protein[0]
                    temp.append([tempPro.area, tempPro.fot, tempPro.ibaq, tempPro.num_psms])
                    # if acc=='gi|312922382':
                    #    print tempPro.annotation
                    proAnno[acc] = tempPro.annotation
                    try:
                        idx_geneList = geneListForIndex.index(sym)
                        geneTable[repeat_idx][idx_geneList][3] += tempPro.num_psms
                    except:
                        continue
                else:
                    temp.append([-1, -1, -1, -1])
            proTable.append(temp)
            repeat_idx += 1
        ''' proTable[-1] contains as many set()s as amount of proteins '''
        proTable.append([])
        for pro in proList:
            proTable[-1].append(set())
        
        
        print_delta_time(t1, 'proTable.append() done!')
        
        
        ''' get pepTable [exp by exp]'''
        for repeat in repeatList:
            temp = []
            tempList = repeat.split('_')
            (type, exp, rank, repe) = (tempList[0], int(tempList[1]), int(tempList[2]), int (tempList[3]))
            
            id = Search.objects.filter(exp_id=exp).filter(rank=rank).filter(repeat_id=repe).filter(type='rep')[0].id
            # LogFile.write(str(id)+'\n')
            tempPepList = Repeat_Peptide.objects.filter(search_id=id).exclude(type=-1)
            i = 0
            for pep in pepList:
                (seq, modi) = list(pep)
                if len(pep2pro) <= i:
                        pep2pro.append([])
                if len(pep2gen) <= i:
                        pep2gen.append(set())
                        
                tmp_obj_peptide = tempPepList.filter(sequence=seq).filter(modification=modi)
                if tmp_obj_peptide:
                    tempPep = tmp_obj_peptide[0]
                    temp.append([tempPep.area, tempPep.mh_da, tempPep.rt_min, tempPep.num_psms])
                    accessions = tempPep.protein_group_accessions.split(';')
                    pep2pro[i].extend(accessions)
                    for acc in accessions:
                        if acc in proListForIndex:
                            idx = proListForIndex.index(acc)
                            sym = proList[idx][1]
                            if sym:
                                pep2gen[i].add(sym)
                            ''' Record a protein has what peptides  '''
                            proTable[-1][idx].add(i)
                else:
                    temp.append([-1, -1, -1, -1])
                i = i + 1
            pepTable.append(temp)
        
        print_delta_time(t1, 'Peptide done!')
        
        i = 0
        for pro in proList:
            symbol = pro[1]
            if symbol != '':
                if symbol in geneListForIndex:
                    idx = geneListForIndex.index(symbol)
                    geneTable[-1][idx] = geneTable[-1][idx] | proTable[-1][i]
            i += 1
        
        print_delta_time(t1, 'geneListForIndex.index(symbol) done!')
        
        '''
        tempPepList=Repeat_Peptide.objects.filter(search_id=repeat).filter(ion_score__gt=ion_score).exclude(type=-1)
        for pep in peplist:
                #if  filter(pep):
                (seq,modi)=list(pep)
                if tempPepList.filter(sequence=seq).filter(modification=modi).count()>0:
                    tempPep=tempPepList.filter(sequence=seq).filter(modification=modi)[0]
                    
                    pep.add()
                else:
                    pep.add(-1)
            for gene in geneList:
                if filter(gene):
                    gene.add()
                else:
                    gene.add(-1)
        '''
    if compare:  # Start compare search !
        print_delta_time(t1, 'Start compare search !')
        
        repeat = repeatList[0]
        temp = repeat.split('_')
        (type, exp, rank, repe) = (temp[0], int(temp[1]), int(temp[2]), int (temp[3]))
        fraction = Search.objects.filter(exp_id=exp).filter(type='exp')[0].exp.num_fraction

        list_for_merge_fraction = []
        for frac in range(1, 1 + fraction):
            print 'frac=', frac
            # temp_pep_cont = []
            # temp_pep_all = [] #sequence and modification
            # get all pep for each fraction
            all_pep = set()
            
            for repeat in repeatList:
                temp = repeat.split('_')
                (type, exp, rank, repe) = (temp[0], int(temp[1]), int(temp[2]), int (temp[3]))
                
                #===============================================================
                # ''' I need to know a peptide has what proteins & genes  '''
                # cache_repeat_id = Search.objects.filter(exp_id=exp).filter(rank=rank).filter(repeat_id=repe).filter(type='rep')[0].id
                # cache_tempPepList_obj = Repeat_Peptide.objects.filter(search_id=cache_repeat_id).exclude(type=-1)
                # 
                # i=-1
                # for pep in pepList:
                #     i += 1
                #     (seq, modi) = list(pep)
                #     if len(pep2pro) <= i: pep2pro.append(set())
                #     if len(pep2gen) <= i: pep2gen.append(set())
                #             
                #     tmp_obj_peptide = cache_tempPepList_obj.filter(sequence=seq).filter(modification=modi)
                #     if tmp_obj_peptide:
                #         tempPep = tmp_obj_peptide[0]
                #         accessions = tempPep.protein_group_accessions.split(';')
                #   
                #         for acc in accessions:
                #             pep2pro[i].add(acc)
                #             idx = proListForIndex.index(acc)
                #             pep2gen[i].add(proList[idx][1])#symbol
                #===============================================================

                ''' get all_pep, which contains all non-redundant "peptide_modification_charge"  '''
                id = Search.objects.filter(exp_id=exp).filter(repeat_id=repe).filter(rank=rank).filter(fraction_id=frac)[0].id
                tempPepList = Peptide.objects.filter(search_id=id).exclude(type=-1)
                # tempPepList is a big list
                for pep in tempPepList:
                    pep_str = pep.sequence + '_' + pep.modification + '_' + str(pep.charge)
                    all_pep.add(pep_str)
                    
            all_pep = list(all_pep)
            print 'len(all_pep)=', len(all_pep)
            ''' 
            info[0] = [ [0,0,0,0,0,0],
                        [0,0,0,0,0,0],
                        [0,0,0,0,0,0],
                        .....,
                        [0,0,0,0,0,0] ] 
            '''
            info = []
            info_pep_without_area = []
            for repeat in repeatList:
                pep_without_area = []
                temp = repeat.split('_')
                (type, exp, rank, repe) = (temp[0], int(temp[1]), int(temp[2]), int (temp[3]))
                id = Search.objects.filter(exp_id=exp).filter(repeat_id=repe).filter(rank=rank).filter(fraction_id=frac)[0].id
                tempPepList = Peptide.objects.filter(search_id=id).exclude(type=-1)
                
                temp_list = []
                for pep in all_pep:
                    (seq, modi, charge) = pep.split('_')
                    tmp_obj_peptide = tempPepList.filter(sequence=seq).filter(modification=modi).filter(charge=charge).order_by('-ion_score')
                    if tmp_obj_peptide:
                        temp_pep = tmp_obj_peptide[0]
                        ms2_id = temp_pep.ms2_id
                        mz = MS2.objects.get(id=ms2_id).pre_mz
                        temp_list.append([temp_pep.area, temp_pep.fot, temp_pep.rt_min, mz, temp_pep.num_psms, temp_pep.ion_score])
                    else:
                        pep_without_area.append(seq + '_' + modi)
                        temp_list.append([0, 0, 0, 0, 0, 0])
                info.append(temp_list)
                info_pep_without_area.append(pep_without_area)
            
            ''' coefficient RT '''   
            get_coeRT(info, all_pep) 

            list_for_merge_exp = []
            for exp1 in range(len(info)):
                repeat = repeatList[exp1]
                temp = repeat.split('_')
                (type, exp, rank, repe) = (temp[0], int(temp[1]), int(temp[2]), int (temp[3]))
                obj_search = Search.objects.filter(exp_id=exp).filter(repeat_id=repe).filter(rank=rank).filter(fraction_id=frac)[0]
                id, filename = obj_search.id, obj_search.name
                ''' import from cal_area.py '''
                calcAreas(id, filename, 60, 10, info[exp1])
                
                list_for_merge_exp.append(info[exp1])
            ''' if we need compare 3 exps , list_for_merge_exp = [ [],[],[],all_pep ] '''    
            list_for_merge_exp.append(all_pep)
            ''' list_for_merge_fraction = [    [ [],[],[],all_pep ] , [ [],[],[],all_pep ] , [ [],[],[],all_pep ] ....... [ [],[],[],all_pep ]      ] '''
            list_for_merge_fraction.append(list_for_merge_exp)
            
            ''' Till now, one fraction finished '''
            
        print_delta_time(t1, 'Start merge every fraction per exp !')    
#                 proList = list(proList)
#                 pepList = list(pepList)
#                 geneList = list(geneList)
        
        
        list_peptide_dicts = []
        for exp in range(repeatLENGTH):
            protein_list_exp = proTable[exp]
            gene_list_exp = geneTable[exp]
            
            dict_peptide_table = {}
            not_in_dict_peptide_table = 0
            ''' pepList contains cached peptide list collected from all exps '''
            for pep_tuple in pepList:
                dict_peptide_table[  pep_tuple[0] + '_' + pep_tuple[1]  ] = []
                
            tmp_list_pep_attrib = []
            for frac in range(fraction):
                ''' list_for_merge_fraction = [    [ [],[],[],all_pep ] , [ [],[],[],all_pep ] , [ [],[],[],all_pep ] ....... [ [],[],[],all_pep ]      ] '''
                all_pep_exp_name = list_for_merge_fraction[frac][-1]
                list_exp_peptide = list_for_merge_fraction[frac][exp]
                for idx in range(len(all_pep_exp_name)):
                    # print 'all_pep_exp[idx]',all_pep_exp[idx]
                    (seq, mod, charge) = all_pep_exp_name[idx].split('_')
                    seq_mod = seq + '_' + mod
                    pep_attrib = list_exp_peptide[idx]
                    if seq_mod not in dict_peptide_table:
                        # print seq_mod,' not in dict_peptide_table'
                        not_in_dict_peptide_table += 1
                        continue
                    if dict_peptide_table[seq_mod]:
                        # area, fot, rt_min, mz, num_psms, ion_score = dict_peptide_table[seq_mod]
                        dict_peptide_table[seq_mod][4] += pep_attrib[4]
                        dict_peptide_table[seq_mod][0] += pep_attrib[0]
                    else:
                        dict_peptide_table[seq_mod] = pep_attrib

            #===================================================================
            # for pep_tuple in pepList:
            #     seq,mod = pep_tuple
            #     seq_mod = seq+'_'+mod
            #     if seq_mod in dict_peptide_table:
            #         print dict_peptide_table[seq_mod]
            #     else:
            #         print seq_mod ,'not in'
            #===================================================================
                        
            list_peptide_dicts.append(dict_peptide_table)
            print 'not_in_dict_peptide_table=', not_in_dict_peptide_table
            # print list_peptide_dicts  
            pep_without_area = set(info_pep_without_area[exp])
            i = -1    
            for pro in protein_list_exp:
                i += 1
                ''' Re-distribute area to proteins '''
                accession = proListForIndex[i]
                set_pep_of_pro = proTable[-1][i]  # set()
                # if pro[0] == -1:# pro[0] -> area
                for pep_idx in set_pep_of_pro:
                    if accession in pep2pro[pep_idx]:
                        seq_mod = '_'.join(list(pepList[pep_idx]))
                        if seq_mod in pep_without_area:
                            pro[0] += dict_peptide_table[seq_mod][0] / len(pep2pro[pep_idx])
                            
            i = -1    
            for gene in gene_list_exp:
                i += 1
                ''' Re-distribute area to genes '''
                sym = geneListForIndex[i]
                set_pep_of_gene = geneTable[-1][i]  # set()
                # if pro[0] == -1:# pro[0] -> area
                for pep_idx in set_pep_of_gene:
                    if sym in pep2gen[pep_idx]:
                        seq_mod = '_'.join(list(pepList[pep_idx]))
                        if seq_mod in pep_without_area:
                            gene[0] += dict_peptide_table[seq_mod][0] / len(pep2gen[pep_idx])
        # continue
                            
                        
        '''
        1.get all peptide, protein and gene
        2.get rttable
        3.get area per raw
        4.get all_table
        5.write table 
        '''
        # return
    print_delta_time(t1, 'Start write peptab !')  

    peptab = open(quant_dir + str(csvname) + '.peptab', 'w')
    # peptab = open('/tmp/' + str(csvname) + '.peptab', 'w')
    writer = csv.writer(peptab, delimiter='\t')
    title = ['Sequence', 'Modification', 'accessions', 'Symbol']
    for repeat in repeatList:
        title.append(repeat + '_area')
        title.append(repeat + '_mz')
        title.append(repeat + '_rt')
        title.append(repeat + '_psms')
    tempk = [str(item) for item in title]
    tempk.append('index')
    writer.writerow(tempk)
    

    if not compare:
        i = 0
        for pep in pepList:
            tempk = []
            (seq, modi) = list(pep)
            tempk.extend([seq, modi])
            pep2pro[i] = list(set(pep2pro[i]))
            tempk.append(set2str(pep2pro[i]))
            tempk.append(set2str(pep2gen[i]))
            for j in range(repeatLENGTH):
                (area, mz, rt, psms) = pepTable[j][i]
                tempk.extend([area, mz, rt, psms])
            tempk = [str(item) for item in tempk]
            tempk.append(str(i))
            writer.writerow(tempk)
            i = i + 1
    
    else:
        i = -1
        for pep in pepList:
            i += 1
            tempk = []
            (seq, modi) = list(pep)
            seq_mod = seq + '_' + modi
            tempk.extend([seq, modi])
            tempk.append(';'.join(sorted(set(pep2pro[i]))))
            tempk.append(';'.join(sorted(pep2gen[i])))
            for j in range(repeatLENGTH):
                (area, fot, rt, mz, psms, ionscore) = list_peptide_dicts[j][seq_mod]
                tempk.extend([area, mz, rt, psms])
            tempk = [str(item) for item in tempk]
            tempk.append(str(i))
            writer.writerow(tempk)
            # continue
    peptab.close()    
    
    print_delta_time(t1, 'Start write protab !')  
    
    protab = open(quant_dir + str(csvname) + '.protab', 'w')
    writer = csv.writer(protab, delimiter='\t')
    title = ['accessions', 'Symbol', 'Description', 'annotation']
    for repeat in repeatList:
        title.append(repeat + '_area')
        title.append(repeat + '_fot')
        title.append(repeat + '_ibaq')
        title.append(repeat + '_psms')
    title.append('peptide')
    tempk = [str(item) for item in title]
    writer.writerow(tempk)
    
    i = 0
    for pro in proList:
        
        tempk = []
        (acc, sym, des) = list(pro)
        if acc in proAnno:
            tempk.extend([acc, sym, des])
            tempk.append(proAnno[acc])
            for j in range(repeatLENGTH):
                (area, fot, ibaq, psms) = proTable[j][i]
                tempk.extend([area, fot, ibaq, psms])
            tempk.append(set2str(proTable[-1][i]))
            tempk = [str(item) for item in tempk]
            writer.writerow(tempk)
        i = i + 1
    
    print_delta_time(t1, 'Start write genetab !')  
    
    genetab = open(quant_dir + str(csvname) + '.genetab', 'w')
    writer = csv.writer(genetab, delimiter='\t')
    title = ['geneID', 'Symbol', 'Description', 'annotation']
    for repeat in repeatList:
        title.append(repeat + '_area')
        title.append(repeat + '_fot')
        title.append(repeat + '_ibaq')
        title.append(repeat + '_psms')
    title.append('peptide')
    tempk = [str(item) for item in title]
    writer.writerow(tempk)
    i = 0

    for gene in geneList:
        
        tempk = []
        (gene_id, symbol, description) = list(gene)
        if symbol in geneAnno:
            tempk.extend([gene_id, symbol, description])
            tempk.append(geneAnno[symbol])
            for j in range(repeatLENGTH):
                (area, fot, ibaq, psms) = geneTable[j][i]
                tempk.extend([area, fot, ibaq, psms])
            tempstr = ''
            for tempi in set(geneTable[-1][i]):
                tempstr = tempstr + str(tempi) + ';'
            tempk.append(tempstr[:-1])
            tempk = [str(item) for item in tempk]
            writer.writerow(tempk)
            i = i + 1
            # continue
    
    
    
    
    return 0