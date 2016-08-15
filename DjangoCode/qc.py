#!/usr/bin/env python
import sys, optparse, os, tempfile, subprocess, shutil, re, math
from sqlFunc import *
H_PLUS = 1.007276466#1.007825
LIPENG = 116
#ANNO_STATUS = ['co_0','ki_0','li_0','re_0','pmm_0','pmh_0','tf_0']
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

def stop_err(msg, ret=1):
    sys.stderr.write(msg)
    sys.exit(ret)

def time_now():
    return datetime.datetime.now().strftime('%X') 

def timer(t2, t1):
    return float((t2 - t1).seconds) + (t2 - t1).microseconds / 1000000.0


def getPepFromDB(eid_list, rid, rank, type, stype, ionThres):
    #===============================================================================
    # Get Real or Decoy psms  
    #===============================================================================
    pep_list = []
    for eid in eid_list:
        
        if stype == 'exp':
            t = 'select * from gardener_peptide where ion_score>=%s and search_id in (select id from gardener_search where exp_id=%s and type=\'fraction\') and type=%s' % (ionThres, eid, type)
        elif stype == 'repeat':
            t = 'select * from gardener_peptide where ion_score>=%s and search_id in (select id from gardener_search where exp_id=%s and repeat_id=%s and rank=%s and type=\'fraction\') and type=%s' % (ionThres, eid, rid, rank, type)
        
        peptide_list = conn.execution_options(autocommit=True).execute(t)

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
        
        if int(taxid) == 8355:#xenopus, Lei Song
            (symbol, desc) = get_xenos_gene_from_db(acc_short,12)
            gid = -1
        else:
            ''' Get Gene Info '''
            gid = getGeneID(conn, meta, acc_short, prefix, taxid) 
            
        ''' For other taxon '''
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

            #elif int(taxid) == 8355:
            #    (symbol, desc) = get_xenos_gene_from_db(acc_short)
                
        if gid != -1 or symbol != '':
            
            (symbol, desc) = getGeneDescSymbol(conn, meta, gid) if not desc else (symbol, desc)
            if symbol!='':
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
        tmp['symbol'] = symbol if symbol!='' else ''
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
            if pro == 'gi|357527351':
                print 'gi|357527351'
                print peptide
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

def useParsimony(eid,type, qvalueThres, ionThres, peptide_list, flag, dict_pro_length):
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
    searched    = set()
    #pro_sameset = set()
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
                    tmp['peptides']  = info1['peptides']
                    tmp['pep_index'] = info1['pep_index']
                    tmp['sameset']   = set([pro1, pro2])
                    tmp['uni'] = []
                    tmp['symbol'] = symbol
                    tmp['score']        = info1['score']
                    tmp['pep_psms']     = info1['pep_psms']
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
            dict_sameset_pro[master_pro] = tmp
    
    def isUniq(pro,pep):
        for key,info in dict_uni_pro.iteritems():
            if key == pro:continue
            if pep in info['peptides']:
                return False
            
        for key,info in dict_sameset_pro.iteritems():
            if key == pro:continue
            if pep in info['peptides']:
                return False
            
        for key,info in dict_none_uni_pro.iteritems():
            if key == pro:continue
            if pep in info['peptides']:
                return False
            
        return True
    
    for key,info in dict_sameset_pro.items():
        setPeptides = info['peptides']
        for p in setPeptides:
            if isUniq(key,p):
                info['uni'].append(p)
            
    #dict_uni_pro.update(dict_sameset_pro)
    dict_none_uni_pro.update(dict_sameset_pro)
    
    """ Imitate IDPicker, Start to get remaining protein, and merge to dict_uni_pro """
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
    
def startProAssemble(eid_list, peptide_list, pep_list_decoy, fdrThres, ionThres):
    #dir = '/usr/local/galaxyDATA01/incubator/python/ms_parser'
    eid = eid_list[0]
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


def cacheProtein( eid_list, file_data, stype, fdrThres, ionThres):
    # updateExpStage(conn,meta,file_data)
    #t1 = datetime.datetime.now()
    print '\nStart cacheProtein...ionThres=',ionThres

    rid = file_data['r_num']
    rank = file_data['rank']
    print '[Exp ID %s] [Rep %s] [Rank %s] [Type %s]' % (eid_list[0], rid, rank, stype)
    
    sid = 0
    
    peptide_list   = getPepFromDB(eid_list, rid, rank,  1, stype, ionThres)
    pep_list_decoy = getPepFromDB(eid_list, rid, rank, -1, stype, ionThres)
    #peptide_list = []        
    (group_result, qvalueThres, fdr, dict_uni_pro, set_pep_index, pga_peptide, dict_pro_length) = startProAssemble(eid_list, peptide_list, pep_list_decoy, fdrThres, ionThres)
    
    (proteins, genes) = getProGeneFromDB(dict_uni_pro, group_result, sid,  eid_list[0], fdr, dict_pro_length)
   
    num_pro = len(proteins)
    if num_pro == 0:
        return (sid, qvalueThres, [], peptide_list, set(), {}, 0, [])

    proteins.sort(key=lambda x:x['score'], reverse=True)
   
    return (sid, qvalueThres, proteins, peptide_list, set_pep_index, pga_peptide, genes)
   
def cachePeptide(file_data, stype, qvalueThres, ionThres, sid, redundant_pep, set_pep_index, pga_peptide) :
    
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

    if num_pep == 0:
        return (0, [])   
    
    peptides_list.sort(key=lambda x:x['ion_score'], reverse=True)

    return peptides_list

def my_QC(options):

    print 'Start caching Exp...', time_now()    
    
    file_data = {}
    file_data['r_num'] = 1
    file_data['rank'] = 1
    
    fdrThres = options['min_fdr']
    ionThres = options['min_ion']
    eid_list = options['exp_list']
    
    stype = options['stype']
    
    (sid, qvalueThres, proteins, redundant_pep, set_pep_index, pga_peptide, genes) = cacheProtein(eid_list, file_data, stype, fdrThres, ionThres)
    
    peptides = cachePeptide(file_data, stype, qvalueThres, ionThres, sid, redundant_pep, set_pep_index, pga_peptide)      
     
    print 'Complete caching Exp...', time_now()
    
    return (proteins, peptides, genes)

def __main__() :
    
    options = {}
    options['min_fdr'] = 0.01
    options['min_ion'] = 0
    options['max_hit'] = 10
    options['dMZ'] = 10
    options['dRT'] = 60
    
    options['exp_list'] = [429]#[484, 485, 391, 392, 428, 429]
    
    options['stype'] = 'exp'
    (proteins, peptides, genes) = my_QC(options)
    
    print 'Done'
#     print peptides[0]
#     print proteins[0]
#     print genes[0]
    print 'peptides=',len(peptides)
    print 'proteins=',len(proteins)
    print 'genes=',len(genes)
    
if __name__ == "__main__": __main__()
