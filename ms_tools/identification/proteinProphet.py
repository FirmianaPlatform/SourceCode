#!/usr/bin/env python

import sys, optparse, os, tempfile, subprocess, shutil, re, math
#import xml.etree.ElementTree as ET
from lxml import etree as ET
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

"""   
        select * from DBSearchResult_QCResult 
        where qcResultID not in
        (select qcResultID from DBSearchResult_QCResult
        where dbsearchResultID not in (1,2))
        group by qcResultID having count(dbsearchResultID)=2;
"""
def getQCResultID(dbsearchResultID_list):
    dbsearchResultNum = len(dbsearchResultID_list)
    qcids_not = []
    for instance in session.query(DBSearchResult_QCResult).filter(~DBSearchResult_QCResult.dbsearchResultID.in_(dbsearchResultID_list)):
        #print instance.qcResultID, instance.dbsearchResultID
        qcid = instance.qcResultID
        qcids_not.append(qcid)
    #for instance in session.query(DBSearchResult_QCResult).filter(~DBSearchResult_QCResult.qcResultID.in_(cids_not)).group_by(DBSearchResult_QCResult.qcResultID).having(func.count(DBSearchResult_QCResult.dbsearchResultID) == dbsearchResultNum):
        #print instance.qcResultID, instance.dbsearchResultID
    qcResultID_list = []   
    dbsearchResult_QCResults = session.query(DBSearchResult_QCResult).filter(~DBSearchResult_QCResult.qcResultID.in_(qcids_not)).group_by(DBSearchResult_QCResult.qcResultID).having(func.count(DBSearchResult_QCResult.dbsearchResultID) == dbsearchResultNum)
    for dbsearchResult_QCResult in dbsearchResult_QCResults:
        qcResultID = dbsearchResult_QCResult.qcResultID
        qcResultID_list.append(qcResultID)
    #print qcResultID_list
    qcResultID = None
    '''
    here we need qcResultID for ProteinProphet
    the following logic assumes that :
    eg. for all dbsearch results for an experiment,
    there will be 3 qc results: PeptideProphet,InterProphet,ProteinProphet
    
    if len(qcResultID_list) == 2:
        qcResultID = qcResultID_list[1]
        qcResult = session.query(QCResult).filter(QCResult.id == qcResultID).first() 
        if qcResult.method == 'InterProphet':
            qcResultID = None
    elif len(qcResultID_list) == 3:
        qcResultID = qcResultID_list[2]
    elif len(qcResultID_list) > 3:
        print 'strange: qcResultID_list>3'
        
    sometimes, old ProteinProphet records may be not deleted completely from database,
    and the following code will always return the newest record for ProteinProphet
    '''
    for iqcResultID in qcResultID_list:
         qcResult = session.query(QCResult).filter(QCResult.id == iqcResultID).first() 
         if qcResult.method == 'ProteinProphet':
             qcResultID=iqcResultID
    return qcResultID    

def checkDatabase(inputfile_list, method, output, dbop_type):
    try:
        #according to inputfile, find DBSearchResult, then  DBSearchResult_QCResult, QCResult
        dbsearchResultID_list = []
        pep_qcResultID_list = []
        for input in inputfile_list:        
            pep_qcResult = session.query(QCResult).filter(QCResult.filepath == input).first() 
            #print pep_qcResult
            if pep_qcResult is None:
                stop_err('Error adding records to QCResult due to the lack of record for PeptideProphet or InterProphet.\n')
             
            pep_qcfile = pep_qcResult.filepath
            pep_qcResultID = pep_qcResult.id
            pep_qcResultID_list.append(pep_qcResultID)
            #dbsearchResult_QCResult = session.query(DBSearchResult_QCResult).filter(DBSearchResult_QCResult.qcResultID == pep_qcResultID).first()
            #one qcresult may correspond to several dbsearchResults
            dbsearchResult_QCResults = session.query(DBSearchResult_QCResult).filter(DBSearchResult_QCResult.qcResultID == pep_qcResultID)
            for dbsearchResult_QCResult in dbsearchResult_QCResults:
                dbsearchResultID = dbsearchResult_QCResult.dbsearchResultID
                dbsearchResultID_list.append(dbsearchResultID)
        #dbsearchResult = session.query(DBSearchResult).filter(DBSearchResult.id == dbsearchResultID).first()
        """
        the qcresult for ProteinProphet has the same dbsearchResult as PeptideProphet,
        each run of this produces only one qcResultID
        if deleting all prot_qcResultID connected with this dbsearchResult, it is not reasonable.
        here all the dbsearchResult_QCResults with the same dbsearchResult should have same prot_qcResultID
        such as, 
        1,1 1,2 1,3
        2,1 2,2 2,3
        1,2 in first column represent that there are two input peptideprophet xml files
        1,2,3 in second column represent the qcresultID of PeptideProphet, InterProphet,ProteinProphet respectively.
        there may also be records:
        1,4 2,5
        then: dbsearchResultID_list=[1,2];dbsearchResult_QCResult_list=[]
        so should select dbsearchResult_QCResults with 
        """
        qcResultID = getQCResultID(dbsearchResultID_list)
        print qcResultID
        #prot_qcResultID_list = []
        dbsearchResult_QCResults = session.query(DBSearchResult_QCResult).filter(DBSearchResult_QCResult.qcResultID == qcResultID)
        """
        dbsearchResult_QCResult_list=[]
        prot_qcResultID=None
        for dbsearchResultID in dbsearchResultID_list:
            dbsearchResult_QCResults = session.query(DBSearchResult_QCResult).filter(and_(DBSearchResult_QCResult.dbsearchResultID == dbsearchResultID, DBSearchResult_QCResult.qcResultID != pep_qcResultID))
            for dbsearchResult_QCResult in dbsearchResult_QCResults:
                qcResult = dbsearchResult_QCResult.qcResult
                if qcResult.method == 'ProteinProphet': 
                    prot_qcResultID = dbsearchResult_QCResult.qcResultID
                    #prot_qcResultID_list.append(prot_qcResultID)
                    dbsearchResult_QCResult_list.append(dbsearchResult_QCResult)
                    #break 
        """
        #if len(prot_qcResultID_list) > 0:
        if qcResultID is not None:
            #when deleting dbsearchResult_QCResult, QCResult will be automatically deleted by cascade,
            #so are tables referring QCResult, like FDRParam and PeptideIdentification
             if dbop_type == 'update':    
                 proteinIdentifications = session.query(ProteinIdentification).filter(ProteinIdentification.qcResultID == qcResultID) 
                 for proteinIdentification in proteinIdentifications:
                    session.delete(proteinIdentification)         
                 for dbsearchResult_QCResult in dbsearchResult_QCResults:                        
                     session.delete(dbsearchResult_QCResult)
                 return (True, dbsearchResultID_list, pep_qcResultID_list)                                
             elif dbop_type == 'delete': 
                 proteinIdentifications = session.query(ProteinIdentification).filter(ProteinIdentification.qcResultID == qcResultID) 
                 for proteinIdentification in proteinIdentifications:
                    session.delete(proteinIdentification) 
                 for dbsearchResult_QCResult in dbsearchResult_QCResults:                        
                     session.delete(dbsearchResult_QCResult)
                 session.commit()
                 writePrompt(output)  
                 return (False, None, None)  
             else:   
                errlist = []         
                errlist.append('This file has been validated by %s.\n' % method)
                errlist.append('If you want to validate this file by %s again,\n' % method) 
                errlist.append('please choose "update" in the drop-down box "Change the information of the result for this analysis in the database".\n')
                errlist.append('Or else the original information in the database will be kept.')
                #print err
                stop_err('Error checking records in QCResult.\n%s\n' % ''.join(errlist))
        else:
            #print 'experiment is None'
            if dbop_type == 'update' or dbop_type == 'delete':      
                err = 'There is no information about this analysis in the database.'
                stop_err('Error changing information for QCResult in the database.\n%s\n' % err)       
            return (True, dbsearchResultID_list, pep_qcResultID_list)       
    except Exception, e:
        session.rollback()
        stop_err('Error checking records in QCResult.\n%s' % (str(e))) 

'''
when processing pepxml file from combing several dbsearch results
'''
def storeQCResult(dbsearchResultID_list, resultfilepath, method):
    try:
        #method = 'InterProphet'
        qcResult = QCResult(resultfilepath, method)
        #print qcResult
        session.add(qcResult) #child
        #session.commit()
                
        qcResult = session.query(QCResult).filter(QCResult.filepath == resultfilepath).first() 
        qcResultID = qcResult.id
        #dbsearchResult=session.query(DBSearchResult).filter(DBSearchResult.pepfilepath==inputfile).first()
        #dbsearchResult_QCResult=DBSearchResult_QCResult()  #it is strange that this will add a record with  dbsearchResultID=0       
        for dbsearchResultID in dbsearchResultID_list:        
            dbsearchResult = session.query(DBSearchResult).filter(DBSearchResult.id == dbsearchResultID).first()  
            #dbsearchResult=session.query(DBSearchResult).filter(DBSearchResult.pepfilepath==inputfile).first()
            #dbsearchResult_QCResult=DBSearchResult_QCResult()  #it is strange that this will add a record with  dbsearchResultID=0       
            dbsearchResult_QCResult = DBSearchResult_QCResult(qcResultID=qcResultID, dbsearchResultID=dbsearchResultID)
            dbsearchResult_QCResult.qcResult = qcResult
            dbsearchResult.qcResults.append(dbsearchResult_QCResult)
        
        session.commit()
        return qcResultID 
    except Exception, e:
        session.rollback()
        stop_err('Error adding records to QCResult.\n%s' % (str(e))) 
        
def storeProteinIdentification(qcResultID, pep_qcResultID_list, outputfile):
    try:
        protfile = ET.parse(outputfile)
        root = protfile.getroot()
       
        for protein_group in root.iter('{http://regis-web.systemsbiology.net/protXML}protein_group'):
            protein = protein_group.find('./{http://regis-web.systemsbiology.net/protXML}protein')
            if protein is not None:
                protein_name = protein.get('protein_name')
                n_indistinguishable_proteins = protein.get('n_indistinguishable_proteins')
                probability = protein.get('probability')
                percent_coverage = protein.get('percent_coverage')
                unique_stripped_peptides = protein.get('unique_stripped_peptides')
                group_sibling_id = protein.get('group_sibling_id')
                total_number_peptides = protein.get('total_number_peptides')
                pct_spectrum_ids = protein.get('pct_spectrum_ids')
                confidence = protein.get('confidence')
                
                """
                41:      <protein protein_name="gi|10092601|ref|NP_003751.2|" n_indistinguishable_proteins="3" probability="1.0000" percent_coverage="1.6" unique_stripped_peptides="QVSGLTVDTEER+VDEGGWNTVQGAK" group_sibling_id="a" total_number_peptides="2" pct_spectrum_ids="0.05" confidence="1.00">
42-         <parameter name="prot_length" value="0"/>
43-         <annotation protein_description="eukaryotic translation initiation factor 4 gamma 3 isoform 3 [Homo sapiens]"/>
44-         <indistinguishable_protein protein_name="gi|311771714|ref|NP_001185730.1|">
45-            <annotation protein_description="eukaryotic translation initiation factor 4 gamma 3 isoform 1 [Homo sapiens]"/>
46-         </indistinguishable_protein>
47-         <indistinguishable_protein protein_name="gi|311771716|ref|NP_001185731.1|">
48-            <annotation protein_description="eukaryotic translation initiation factor 4 gamma 3 isoform 2 [Homo sapiens]"/>
49-         </indistinguishable_protein>
50-         <peptide peptide_sequence="VDEGGWNTVQGAK" charge="2" initial_probability="0.9973" nsp_adjusted_probability="0.9982" weight="1.00" is_nondegenerate_evidence="Y" n_enzymatic_termini="2" n_sibling_peptides="0.97" n_sibling_peptides_bin="5" n_instances="1" exp_tot_instances="1.00" is_contributing_evidence="Y" calc_neutral_pep_mass="1359.6497">
51-         </peptide>
52-         <peptide peptide_sequence="QVSGLTVDTEER" charge="2" initial_probability="0.9741" nsp_adjusted_probability="0.9828" weight="1.00" is_nondegenerate_evidence="Y" n_enzymatic_termini="2" n_sibling_peptides="1.00" n_sibling_peptides_bin="5" n_instances="1" exp_tot_instances="0.97" is_contributing_evidence="Y" calc_neutral_pep_mass="1332.6600">
53-         </peptide>
54-      </protein>
55-</protein_group>

                one group may have several proteins. 
                """
                indistinguishable_protein_name_list = []
                indistinguishable_proteins = protein.findall('./{http://regis-web.systemsbiology.net/protXML}indistinguishable_protein')
                for indistinguishable_protein in indistinguishable_proteins:
                    indistinguishable_protein_name_list.append(indistinguishable_protein.get('protein_name'))
                indistinguishable_protein_name = ','.join(indistinguishable_protein_name_list)
                
                protIdentification = ProteinIdentification(qcResultID, protein_name, n_indistinguishable_proteins, probability, percent_coverage, unique_stripped_peptides,
                                                            group_sibling_id, total_number_peptides, pct_spectrum_ids, confidence, indistinguishable_protein_name)
                #print pepIdentification
                session.add(protIdentification) 
                session.commit()
                protIdentification = session.query(ProteinIdentification).filter(and_(ProteinIdentification.qcResultID == qcResultID, ProteinIdentification.protein_name == protein_name)).first()               
                if protIdentification is None:
                    session.rollback()
                    stop_err('Error adding records to ProteinIdentification due to the failure of inserting one ProteinIdentification record.\n%s' % (str(e)))      
                proteinIdentificationID = protIdentification.id
                
                """
                <peptide peptide_sequence="ELPPDQAEYCIAR" charge="2" initial_probability="0.7549" nsp_adjusted_probability="0.8373" weight="0.50" is_nondegenerate_evidence="N" n_enzymatic_termini="2" n_sibling_peptides="5.02" n_sibling_peptides_bin="7" n_instances="2" exp_tot_instances="1.18" is_contributing_evidence="Y" calc_neutral_pep_mass="1560.7320">
539-<modification_info modified_peptide="ELPPDQAEYCIAR">
540-<mod_aminoacid_mass position="10" mass="160.030649"/>
541-</modification_info>
542:            <peptide_parent_protein protein_name="gi|194097350|ref|NP_001123476.1|"/>
543:            <peptide_parent_protein protein_name="gi|194097350|ref|NP_001123476.1|"/>
544:            <peptide_parent_protein protein_name="gi|194097352|ref|NP_001123477.1|"/>
545:            <peptide_parent_protein protein_name="gi|4501891|ref|NP_001093.1|"/>
546-         </peptide>

some peptides may have several parent proteins and modification

 <peptide peptide_sequence="TDCVMISTR" initial_probability="0.0861" nsp_adjusted_probability="0.0177" weight="0.50" is_nondegenerate_evidence="N" n_enzymatic_termini="2" n_sibling_peptides="0.00" n_sibling_peptides_bin="0" n_instances="1" exp_tot_instances="0.09" is_contributing_evidence="N">
            <peptide_parent_protein protein_name="sp|Q8TBR7-1|FA57A_HUMAN"/>
            <peptide_parent_protein protein_name="sp|Q8TBR7|FA57A_HUMAN"/>
            <peptide_parent_protein protein_name="tr|I3L0N4|I3L0N4_HUMAN"/>
             <indistinguishable_peptide peptide_sequence="2_TDC[160]VMISTR" charge="2" calc_neutral_pep_mass="1081.50">
             <modification_info modified_peptide="TDC[160]VMISTR"/>
             </indistinguishable_peptide>
         </peptide>

some peptides also have indistinguishable_peptides

                """
                peptides = protein.findall('./{http://regis-web.systemsbiology.net/protXML}peptide')
                if peptides is not None:
                    for peptide in peptides:
                        #peptide_sequence = peptide.get('peptide_sequence')
                        peptide_list = list(peptide.get('peptide_sequence'))
                        charge = peptide.get('charge')
                        initial_probability = peptide.get('initial_probability')
                        """ 
                        nsp_adjusted_probability = peptide.get('nsp_adjusted_probability')
                        peptide_group_designator = peptide.get('peptide_group_designator')
                        weight = peptide.get('weight')
                        is_nondegenerate_evidence = peptide.get('is_nondegenerate_evidence')
                        n_enzymatic_termini = peptide.get('n_enzymatic_termini')
                        n_sibling_peptides = peptide.get('n_sibling_peptides')
                        n_sibling_peptides_bin = peptide.get('n_sibling_peptides_bin')
                        n_instances = peptide.get('n_instances')
                        exp_tot_instances = peptide.get('exp_tot_instances')
                        is_contributing_evidence = peptide.get('is_contributing_evidence')
                        """
                        calc_neutral_pep_mass = peptide.get('calc_neutral_pep_mass')
                                                
                        """
                              <protein protein_name="gi|169646441|ref|NP_001108628.1|" n_indistinguishable_proteins="2" probability="1.0000" percent_coverage="10.8" unique_stripped_peptides="MTGSEFDFEEMK+TDDYLDQPCYETINR+TYDATTHFETTCDDIK" group_sibling_id="a" total_number_peptides="7" pct_spectrum_ids="0.17" confidence="1.00">
         <peptide peptide_sequence="MTGSEFDFEEMK" charge="2" initial_probability="0.9977" nsp_adjusted_probability="0.9986" weight="1.00" is_nondegenerate_evidence="Y" n_enzymatic_termini="2" n_sibling_peptides="3.61" n_sibling_peptides_bin="7" n_instances="1" exp_tot_instances="1.00" is_contributing_evidence="Y" calc_neutral_pep_mass="1465.5820">
         <peptide peptide_sequence="MTGSEFDFEEMK" charge="2" initial_probability="0.6318" nsp_adjusted_probability="0.7413" weight="1.00" is_nondegenerate_evidence="Y" n_enzymatic_termini="2" n_sibling_peptides="3.97" n_sibling_peptides_bin="7" n_instances="1" exp_tot_instances="0.63" is_contributing_evidence="Y" calc_neutral_pep_mass="1449.5870">
         <peptide peptide_sequence="MTGSEFDFEEMK" charge="2" initial_probability="0.0647" nsp_adjusted_probability="0.0647" weight="1.00" is_nondegenerate_evidence="Y" n_enzymatic_termini="2" n_sibling_peptides="4.61" n_sibling_peptides_bin="7" n_instances="1" exp_tot_instances="0.06" is_contributing_evidence="N" calc_neutral_pep_mass="1465.5820">
                        
                        if is strange that one protein has two peptide with the same sequence,charge,mass.
                        different fields:
                        initial_probability,nsp_adjusted_probability,n_sibling_peptides,exp_tot_instances,is_contributing_evidence
                        
peptideprophet_result for the first one:
<peptideprophet_result probability="0.9987" all_ntt_prob="(0.0000,0.0000,0.9987)">
69981-<search_score_summary>
69982-<parameter name="fval" value="4.6490"/>
69983-<parameter name="ntt" value="2"/>
69984-<parameter name="nmc" value="0"/>
69985-<parameter name="massd" value="0.002"/>
69986-</search_score_summary>
69987-</peptideprophet_result>

peptideprophet_result for the last one:
70005-<peptideprophet_result probability="0.0648" all_ntt_prob="(0.0000,0.0000,0.0648)">
70006-<search_score_summary>
70007-<parameter name="fval" value="-1.1979"/>
70008-<parameter name="ntt" value="2"/>
70009-<parameter name="nmc" value="0"/>
70010-<parameter name="massd" value="0.003"/>
70011-</search_score_summary>
70012-</peptideprophet_result>

so by comparing the probability, it is possible to distinguish the two peptides
but sometimes two peptides may have equal math.fabs(pepProbability - float(initial_probability)).
                        
                        | id    | qcResultID | spectrum                              | startScan | endScan | precursorNeutralMass | assumedCharge | retentionTime | peptide           | peptidePrevAa | peptideNextAa | numTotProteins | numMatchedIons | totNumIons | calcNeutralPepMass | numMissedCleavages | modification | probability | iprobability | labelFreeQuantArea | labelFreeQuantRT |
+-------+------------+---------------------------------------+-----------+---------+----------------------+---------------+---------------+-------------------+---------------+---------------+----------------+----------------+------------+--------------------+--------------------+--------------+-------------+--------------+--------------------+------------------+
| 81528 |         50 | dataset_1486.dat scan 11778 (charge 2 | 11778     | 11778   |            2015.8563 |             2 |       1656.93 | TDMDNQIVVSDYAQmDR | K             | V             |              2 |             19 |         32 |          2015.8564 |                  0 | M(147.0354), |      0.9995 |         NULL |        7.96998e+08 |          1804.99 |
| 81877 |         50 | dataset_1486.dat scan 12397 (charge 2 | 12397     | 12397   |            2015.8602 |             2 |       1721.57 | TDmDNQIVVSDYAQMDR | K             | V             |              2 |             22 |         32 |          2015.8564 |                  0 | M(147.0354), |      0.9998 |         NULL |               NULL |             NULL |

 <protein protein_name="gi|375477430|ref|NP_001243650.1|" n_indistinguishable_proteins="2" probability="1.0000" percent_coverage="8.1" unique_stripped_peptides="EDIEFICK+IDDVVNTR+LVIEEAER+TDMDNQIVVSDYAQMDR" group_sibling_id="a" total_number_peptides="18" pct_spectrum_ids="0.28" confidence="1.00">
9783-         <parameter name="prot_length" value="0"/>
9784-         <annotation protein_description="T-complex protein 1 subunit delta isoform b [Homo sapiens]"/>
9785:         <indistinguishable_protein protein_name="gi|38455427|ref|NP_006421.2|">
9786-            <annotation protein_description="T-complex protein 1 subunit delta isoform a [Homo sapiens]"/>
9787-         </indistinguishable_protein>
9788-         <peptide peptide_sequence="TDMDNQIVVSDYAQMDR" charge="2" initial_probability="0.9989" nsp_adjusted_probability="0.9996" weight="1.00" is_nondegenerate_evidence="Y" n_enzymatic_termini="2" n_sibling_peptides="4.83" n_sibling_peptides_bin="8" n_instances="10" exp_tot_instances="9.97" is_contributing_evidence="Y" calc_neutral_pep_mass="1999.8615">
9789-         </peptide>
9790-         <peptide peptide_sequence="TDMDNQIVVSDYAQMDR" charge="2" initial_probability="0.9988" nsp_adjusted_probability="0.9996" weight="1.00" is_nondegenerate_evidence="Y" n_enzymatic_termini="2" n_sibling_peptides="4.83" n_sibling_peptides_bin="8" n_instances="1" exp_tot_instances="1.00" is_contributing_evidence="Y" calc_neutral_pep_mass="2015.8564">
9791-<modification_info modified_peptide="TDM[147]DNQIVVSDYAQMDR">
9792-<mod_aminoacid_mass position="3" mass="147.035400"/>
9793-</modification_info>
9794-         </peptide>
9795-         <peptide peptide_sequence="TDMDNQIVVSDYAQMDR" charge="2" initial_probability="0.9985" nsp_adjusted_probability="0.9995" weight="1.00" is_nondegenerate_evidence="Y" n_enzymatic_termini="2" n_sibling_peptides="4.83" n_sibling_peptides_bin="8" n_instances="1" exp_tot_instances="1.00" is_contributing_evidence="Y" calc_neutral_pep_mass="2015.8564">
9796-<modification_info modified_peptide="TDMDNQIVVSDYAQM[147]DR">
9797-<mod_aminoacid_mass position="15" mass="147.035400"/>
9798-</modification_info>
9799-         </peptide>

here find two peptides: id 81528 and id 81877
0.9995-0.9985=0.001
0.9998-0.9988=0.001
Can not be distinguished.

so better use modification_info
                        """
                        modification = ''
                        peptide_sequence = ''
                        modification_info = peptide.find('./{http://regis-web.systemsbiology.net/protXML}modification_info')
                        if modification_info != None:
                            for mod_aminoacid_mass in modification_info.findall('./{http://regis-web.systemsbiology.net/protXML}mod_aminoacid_mass'):
                                position = mod_aminoacid_mass.get('position')
                                mass = mod_aminoacid_mass.get('mass')
                                modification += peptide_list[int(position) - 1] + '(' + str(mass) + '),'
                                peptide_list[int(position) - 1] = peptide_list[int(position) - 1].lower()
                        peptide_sequence = ''.join(peptide_list)  
                                                
                        for  pep_qcResultID in pep_qcResultID_list:     
                            peptideIdentifications = session.query(PeptideIdentification).filter(and_(PeptideIdentification.qcResultID == pep_qcResultID, PeptideIdentification.peptide == peptide_sequence, PeptideIdentification.assumedCharge == charge, PeptideIdentification.calcNeutralPepMass == calc_neutral_pep_mass))
                            if peptideIdentifications is None:
                                continue
                                #err = 'No record for qcResultID:%s %s charge:%s calc_neutral_pep_mass:%s' % (pep_qcResultID, peptide_sequence, charge, calc_neutral_pep_mass)
                                #stop_err('Error adding records to ProteinIdentification.\n%s' % err)  
                        #find the probability closest with initial_probability, the lowest delta

                            delta = 1                           
                            if len(peptideIdentifications.all()) > 1:
                                for ipeptideIdentification in peptideIdentifications:
                                    pepProbability = ipeptideIdentification.probability
                                    probDiff = math.fabs(pepProbability - float(initial_probability))
                                    if probDiff < delta:
                                        delta = probDiff
                                        peptideIdentification = ipeptideIdentification
                            else:
                                peptideIdentification = peptideIdentifications.first()
                                                                       
                            peptideIdentificationID = peptideIdentification.id
                            #print peptide_sequence, charge
                            #print peptideIdentificationID, proteinIdentificationID
                            peptide_Protein_Identification = Peptide_Protein_Identification(proteinIdentificationID=proteinIdentificationID, peptideIdentificationID=peptideIdentificationID)           
                            peptide_Protein_Identification.peptideIdentification = peptideIdentification
                            protIdentification.peptideIdentifications.append(peptide_Protein_Identification)
                        
        session.commit()
    except Exception, e:
         session.rollback()
         stop_err('Error adding records to ProteinIdentification.\n%s' % (str(e)))         
                        
 
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
            #storeQCResult(options.input,outpath)
            #storeFDRParam(outpath)
            #storePeptideIdentification(outpath)
            #updatePeptideIdentification(options.input,outpath)
        return returncode   
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
        
        stop_err('Error running ProteinProphet.\n%s\n' % (str(e))) 
     
def __main__():
    #Parse Command Line
    parser = optparse.OptionParser()
    parser.add_option('', '--input', dest='input', help=' ')
    parser.add_option('-o', '--output', dest='output', action='store', help='')
    parser.add_option('', '--iproph', dest='iproph', action='store', help='')
    parser.add_option('', '--nooccam', dest='nooccam', action='store', help='')
    parser.add_option('', '--groupwts', dest='groupwts', action='store', help='')
    parser.add_option('', '--normprotlen', dest='normprotlen', action='store', help='')
    parser.add_option('', '--logprobs', dest='logprobs', action='store', help='')
    parser.add_option('', '--confem', dest='confem', action='store', help='')
    parser.add_option('', '--allpeps', dest='allpeps', action='store', help='')
    parser.add_option('', '--unmapped', dest='unmapped', action='store', help='')
    parser.add_option('', '--instances', dest='instances', action='store', help='')
    parser.add_option('', '--delude', dest='delude', action='store', help='')
    parser.add_option('', '--minprob', dest='minprob', action='store', help='')
    parser.add_option('', '--minindep', dest='minindep', action='store', help='')
    parser.add_option('-d', '--outputdir', dest='outputdir', action='store', default="/tmp/")
    parser.add_option('', '--dbop_type', dest='dbop_type', action='store', help='')
    (options, args) = parser.parse_args()    
   
    if not os.path.exists(options.outputdir): 
        os.makedirs(options.outputdir)

    inputfile_list = []
    inputfile_list.append(options.input)
    for i, arg in enumerate(args):      
            inputfile_list.append(arg)
               
    infilebase = os.path.splitext(os.path.basename(options.input))[0]  
    outfilename = os.path.join(options.outputdir, ''.join([infilebase, '.interact.prot.xml'])) 
               
    cmd = 'ProteinProphet '
    for i, arg in enumerate(inputfile_list):
        add_file = arg.replace('.dat', '.interact.pep.xml')
        if not os.path.isfile(add_file):
            os.symlink(arg, add_file)
        cmd += " %s" % add_file 
    
    cmd += ' ' + outfilename   
    if options.iproph == 'true':
        cmd += ' IPROPHET'
    if options.nooccam == 'true':
        cmd += ' NOOCCAM'
    if options.groupwts == 'true':
        cmd += ' GROUPWTS' 
    if options.normprotlen == 'true':
        cmd += ' NOPROTLEN'
    if options.logprobs == 'true':
        cmd += ' LOGPROBS'
    if options.confem == 'true':
        cmd += ' CONFEM:'
    if options.allpeps == 'true':
        cmd += ' ALLPEPS'
    if options.unmapped == 'true':
        cmd += ' UNMAPPED'
    if options.instances == 'true':
        cmd += ' INSTANCES'
    if options.delude == 'true':
        cmd += ' DELUDE'
    if options.minprob != '0.05':
        cmd += ' MINPROB=' + options.minprob
    if options.minindep != '0':
        cmd += ' MININDEP=' + options.minindep
            
    if options.output.find('job_working_directory') != -1:
        outpath = options.output.replace('job_working_directory', 'files')
        outpath = outpath.replace('galaxy_dataset', 'dataset')
        #re.sub(pattern, repl, string, count=0, flags=0)
        #Return the string obtained by replacing the leftmost non-overlapping occurrences of pattern in string by the replacement repl
        pattern = r'(\/\d+)(\/\d+)'
        outpath = re.sub(pattern, '\g<1>', outpath)
    else:
        outpath = options.output
    
    cmd += ';  wait; cp ' + outfilename + ' ' + options.output     
    #galaxy will mv the output files from job_working_directory to files after finishing the run
    cmd += ';  wait; cp ' + outfilename + ' ' + outpath 
    
    print cmd
    
    method = 'ProteinProphet' 
    (status, dbsearchResultID_list, pep_qcResultID_list) = checkDatabase(inputfile_list, method, options.output, options.dbop_type)
    if status:
        returncode = runTool(cmd)
        if returncode == 0:
            qcResultID = storeQCResult(dbsearchResultID_list, outpath, method)    
            storeProteinIdentification(qcResultID, pep_qcResultID_list, outpath)


if __name__ == "__main__": __main__()
