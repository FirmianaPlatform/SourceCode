#!/usr/bin/env python

import sys, optparse, os, tempfile, subprocess, shutil, re
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
    if len(qcResultID_list) == 2:
        qcResultID = qcResultID_list[1]
        qcResult = session.query(QCResult).filter(QCResult.id == qcResultID).first() 
        if qcResult.method == 'ProteinProphet':
            qcResultID = None
    elif len(qcResultID_list) == 3:
        qcResultID = qcResultID_list[1]
    elif len(qcResultID_list) > 3:
        print 'strange: qcResultID_list>3'
    '''
    for iqcResultID in qcResultID_list:
         qcResult = session.query(QCResult).filter(QCResult.id == iqcResultID).first() 
         if qcResult.method == 'InterProphet':
             qcResultID=iqcResultID
    return qcResultID     

def checkDatabase(inputfile_list, method, output, dbop_type):
    try:
        #method = 'InterProphet'        
        #each run will produce a new file, so the following code will not be executed 
        #qcResult=session.query(QCResult).filter(QCResult.filepath==resultfilepath).first() 
        #if qcResult:
        #     session.delete(qcResult)        
        """
        the input of InterProphet is the result of PeptideProphet, stored in QCResult
        so using 'DBSearchResult.pepfilepath==inputfile' cannot find any record 
        should first find the PeptideProphet record to get DBSearchResult_QCResult,
        and then find DBSearchResult record
        after InterProphet, there should be two records in DBSearchResult_QCResult for a DBSearchResult record
        """
        dbsearchResultID_list = []
        for input in inputfile_list:
            pep_qcResult = session.query(QCResult).filter(QCResult.filepath == input).first() 
            if pep_qcResult is None:
                stop_err('Error adding records to QCResult due to the lack of record for PeptideProphet.\n')
             
            pep_qcfile = pep_qcResult.filepath
            pep_qcResultID = pep_qcResult.id
            #one qcresult may correspond to several dbsearchResults
            dbsearchResult_QCResults = session.query(DBSearchResult_QCResult).filter(DBSearchResult_QCResult.qcResultID == pep_qcResultID)
            for dbsearchResult_QCResult in dbsearchResult_QCResults:
                dbsearchResultID = dbsearchResult_QCResult.dbsearchResultID
                dbsearchResultID_list.append(dbsearchResultID)
        #dbsearchResult = session.query(DBSearchResult).filter(DBSearchResult.id == dbsearchResultID).first()
        """ 
        there should be only one record for interprophet on one dbsearch result.
        for each dbsearchResult, there will be three QCResult: PeptideProphet, interprophet and proteinprophet.
        """
        qcResultID = getQCResultID(dbsearchResultID_list)
        dbsearchResult_QCResults = session.query(DBSearchResult_QCResult).filter(DBSearchResult_QCResult.qcResultID == qcResultID)
        """
        inter_qcResultID_list = []
        for dbsearchResultID in dbsearchResultID_list:
            dbsearchResult_QCResults = session.query(DBSearchResult_QCResult).filter(and_(DBSearchResult_QCResult.dbsearchResultID == dbsearchResultID, DBSearchResult_QCResult.qcResultID != pep_qcResultID))
            for dbsearchResult_QCResult in dbsearchResult_QCResults:
                qcResult = dbsearchResult_QCResult.qcResult
                if qcResult.method == 'InterProphet': 
                    inter_qcResultID = dbsearchResult_QCResult.qcResultID
                    inter_qcResultID_list.append(inter_qcResultID)
                    break
        """ 
        #if len(inter_qcResultID_list) > 0:        
        if qcResultID is not None:
            #when deleting dbsearchResult_QCResult, QCResult will be automatically deleted by cascade,
            #so are tables referring QCResult, like FDRParam and PeptideIdentification
             if dbop_type == 'update':  
                 #for qcResultID in  inter_qcResultID_list:                 
                     pepIdentifications = session.query(PeptideIdentification).filter(PeptideIdentification.qcResultID == qcResultID) 
                     for pepIdentification in pepIdentifications:
                         peptide_Protein_Identifications = session.query(Peptide_Protein_Identification).filter(Peptide_Protein_Identification.peptideIdentificationID == pepIdentification.id)
                         for peptide_Protein_Identifications in peptide_Protein_Identifications:
                             session.delete(peptide_Protein_Identifications)                        
                         session.delete(pepIdentification) 
                     fdrs = session.query(FDRParam).filter(FDRParam.qcResultID == qcResultID) 
                     for fdr in fdrs:
                        session.delete(fdr)
                     for dbsearchResult_QCResult in dbsearchResult_QCResults:
                         session.delete(dbsearchResult_QCResult)                   
                     return (True, dbsearchResultID_list)                                
             elif dbop_type == 'delete':                  
                 #for qcResultID in  inter_qcResultID_list:                 
                     pepIdentifications = session.query(PeptideIdentification).filter(PeptideIdentification.qcResultID == qcResultID) 
                     for pepIdentification in pepIdentifications:
                         peptide_Protein_Identifications = session.query(Peptide_Protein_Identification).filter(Peptide_Protein_Identification.peptideIdentificationID == pepIdentification.id)
                         for peptide_Protein_Identifications in peptide_Protein_Identifications:
                             session.delete(peptide_Protein_Identifications)                        
                         session.delete(pepIdentification) 
                     fdrs = session.query(FDRParam).filter(FDRParam.qcResultID == qcResultID) 
                     for fdr in fdrs:
                        session.delete(fdr)
                     #session.delete(dbsearchResult_QCResult)                   
                     for dbsearchResult_QCResult in dbsearchResult_QCResults:
                         session.delete(dbsearchResult_QCResult) 
                     #qcResultID=dbsearchResult_QCResult.qcResultID
                     #if qcResultID != pep_qcResultID:
                        #qcResult=session.query(QCResult).filter(QCResult.id==qcResultID).first()
                        #cascade delete FDRParam, PeptideIdentification,SearchScoreSummary, PeptideIdentification_ProteinSeqInfo
                        #session.delete(qcResult)                 
                     session.commit()
                     writePrompt(output)  
                     return (False, None)  
             else:   
                errlist = []         
                errlist.append('This file has been validated by %s.\n' % method)
                errlist.append('If you want to validate this file by %s again,\n' % method) 
                errlist.append('please choose "update" in the drop-down box "Change the information of the result for this analysis in the database".\n')
                errlist.append('Or else the original information in the database will be kept.')
                #print err
                stop_err('Error adding records to QCResult.\n%s\n' % ''.join(errlist))
        else:
            #print 'experiment is None'
            if dbop_type == 'update' or dbop_type == 'delete':      
                err = 'There is no information about this analysis in the database.'
                stop_err('Error changing information for QCResult in the database.\n%s\n' % err)       
            return (True, dbsearchResultID_list)       
    except Exception, e:
        session.rollback()
        stop_err('Error checking records in QCResult.\n%s' % (str(e))) 

   
#filepath,method
def storeQCResult(dbsearchResultID_list, resultfilepath, method):
    try:
        #method = 'InterProphet'
        qcResult = QCResult(resultfilepath, method)
        #print qcResult
        session.add(qcResult) #child
        #session.commit()
        
        #qcResult=session.query(QCResult).filter(QCResult.filepath==resultfilepath).first() 
        qcResult = session.query(QCResult).filter(QCResult.filepath == resultfilepath).first() 
        qcResultID = qcResult.id
        
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
         
#qcResultID, error, minProb, numCorr, numIncorr
def storeFDRParam(qcResultID, outputfile):
    try:
        """
        qcResult = session.query(QCResult).filter(QCResult.filepath == outputfile).first()        
        if not qcResult:
            stop_err('Error adding records to FDRParam due to the lack of QCResult.\n')
        qcResultID = qcResult.id
        
        fdrs = session.query(FDRParam).filter(FDRParam.qcResultID == qcResultID) 
        for fdr in fdrs:
             session.delete(fdr)
        """          
        pepfile = ET.parse(outputfile)
        root = pepfile.getroot()
        #print root
        """
        ./{http://regis-web.systemsbiology.net/pepXML}analysis_summary/
        #{http://regis-web.systemsbiology.net/pepXML}peptideprophet_summary/
        #{http://regis-web.systemsbiology.net/pepXML}roc_error_data/
        {http://regis-web.systemsbiology.net/pepXML}error_point')
        """
        search_hits = root.findall('./{http://regis-web.systemsbiology.net/pepXML}analysis_summary/{http://regis-web.systemsbiology.net/pepXML}error_point')
        if search_hits == None:
            stop_err('Error adding records to FDRParam due to the lack of error_point items in the pepxml file.\n')
        #for search_hit in root.iter('{http://regis-web.systemsbiology.net/pepXML}error_point'):
        for search_hit in search_hits:
            #analysis_summary/peptideprophet_summary/error_point
            error = search_hit.get('error')
            minProb = search_hit.get('min_prob')
            numCorr = search_hit.get('num_corr')
            numIncorr = search_hit.get('num_incorr')
            fdrParam = FDRParam(qcResultID, error, minProb, numCorr, numIncorr)
            #print fdrParam
            session.add(fdrParam)
        session.commit()
    except Exception, e:
        session.rollback()
        stop_err('Error adding records to FDRParam.\n%s' % (str(e))) 
         
#qcResultID, spectrum, startScan, endScan, precursorNeutralMass, assumedCharge,
#retentionTime, peptidePrevAa, peptideNextAa, calcNeutralPepMass, numMissedCleavages, probability, labelFreeQuant
def storePeptideIdentification(qcResultID, outputfile):
    try:
        #method = 'InterProphet'
        #</peptideprophet_result></analysis_result></search_hit></search_result></search_hit>
        """
        qcResult = session.query(QCResult).filter(QCResult.filepath == outputfile).first()        
        if not qcResult:
            stop_err('Error adding records to PeptideIdentification due to the lack of QCResult.\n')
        qcResultID = qcResult.id
        
        pepIdentifications = session.query(PeptideIdentification).filter(PeptideIdentification.qcResultID == qcResultID) 
        for pepIdentification in pepIdentifications:
             session.delete(pepIdentification) 
        """      
        pepfile = ET.parse(outputfile)
        root = pepfile.getroot()
        #spectrum_query = root.findall('./../{http://regis-web.systemsbiology.net/pepXML}spectrum_query')
        #print root
        for spectrum_query in root.iter('{http://regis-web.systemsbiology.net/pepXML}spectrum_query'):
            spectrum = spectrum_query.get('spectrum')
            startScan = spectrum_query.get('start_scan')
            endScan = spectrum_query.get('end_scan')
            precursorNeutralMass = spectrum_query.get('precursor_neutral_mass')
            assumedCharge = spectrum_query.get('assumed_charge')
            retentionTime = spectrum_query.get('retention_time_sec')
            
            search_hit = spectrum_query.find('./{http://regis-web.systemsbiology.net/pepXML}search_result/{http://regis-web.systemsbiology.net/pepXML}search_hit')
            if search_hit == None:
                stop_err('Error adding records to PeptideIdentification due to the lack of search_hits items in the pepxml file.\n')
            peptide_list = list(search_hit.get('peptide'))
            peptidePrevAa = search_hit.get('peptide_prev_aa')
            peptideNextAa = search_hit.get('peptide_next_aa')
            numTotProteins = search_hit.get('num_tot_proteins')
            numMatchedIons = search_hit.get('num_matched_ions')
            totNumIons = search_hit.get('tot_num_ions')
            calcNeutralPepMass = search_hit.get('calc_neutral_pep_mass')
            #massdiff = search_hit.get('massdiff')
            #num_tol_term = search_hit.get('num_tol_term')
            numMissedCleavages = search_hit.get('num_missed_cleavages')
            
            protein = search_hit.get('protein')
            protein_descr = search_hit.get('protein_descr')
            
            """ <modification_info modified_peptide="AETAAQDVQQK[136]">
            <mod_aminoacid_mass position="11" mass="136.1092"/>
            </modification_info>
            """
            modification = ''
            peptide = ''
            modification_info = search_hit.find('./{http://regis-web.systemsbiology.net/pepXML}modification_info')
            if modification_info != None:
                for mod_aminoacid_mass in modification_info.findall('{http://regis-web.systemsbiology.net/pepXML}mod_aminoacid_mass'):
                    position = mod_aminoacid_mass.get('position')
                    mass = mod_aminoacid_mass.get('mass')
                    modification += peptide_list[int(position) - 1] + '(' + str(mass) + '),'
                    peptide_list[int(position) - 1] = peptide_list[int(position) - 1].lower()
            peptide = ''.join(peptide_list)
                    
            peptideprophet_result = search_hit.find('./{http://regis-web.systemsbiology.net/pepXML}analysis_result/{http://regis-web.systemsbiology.net/pepXML}peptideprophet_result')
            probability = peptideprophet_result.get('probability')  
            
            peptideprophet_result = search_hit.find('./{http://regis-web.systemsbiology.net/pepXML}analysis_result/{http://regis-web.systemsbiology.net/pepXML}interprophet_result')
            iprobability = peptideprophet_result.get('probability') 
            
            """ <peptideprophet_result probability="0.8236" all_ntt_prob="(0.0000,0.0000,0.8236)">
                <search_score_summary>
                <parameter name="nss" value="0.0311"/>
                <parameter name="ntt" value="2"/>
                <parameter name="nmc" value="0"/>
                <parameter name="massd" value="0.005"/>
                <parameter name="isomassd" value="0"/>    isomassd may be empty
                </search_score_summary>
                </peptideprophet_result>
            """
            score_dict = {}
            score_summary = peptideprophet_result.find('./{http://regis-web.systemsbiology.net/pepXML}search_score_summary') 
            if score_summary != None:
                for parameter in score_summary.findall('{http://regis-web.systemsbiology.net/pepXML}parameter'):
                    name = parameter.get('name')
                    value = parameter.get('value')
                    score_dict[name] = value
                    #print name, value
                if 'isomassd' not in score_dict:
                    score_dict['isomassd'] = '-1'
                print score_dict      
            """ print '''qcResultID, spectrum,startScan,endScan, precursorNeutralMass, assumedCharge,retentionTime,
                                      peptide,peptidePrevAa, peptideNextAa, numTotProteins,numMatchedIons,totNumIons,calcNeutralPepMass,numMissedCleavages,modification,
                                      probability'''
            """                           
            pepIdentification = PeptideIdentification(qcResultID, spectrum, startScan, endScan, precursorNeutralMass, assumedCharge, retentionTime,
                                      peptide, peptidePrevAa, peptideNextAa, numTotProteins, numMatchedIons, totNumIons, calcNeutralPepMass, numMissedCleavages, modification,
                                      #protein,protein_descr,
                                      probability, iprobability, None, None)
            #print pepIdentification
            session.add(pepIdentification)
            #store protein information into table 
            protein_list = protein.split(';')
            print protein_list
            desc_list = protein_descr.split(';')
            proteinNum = len(protein_list)
            for i in range(proteinNum):
                protein = protein_list[i]
                protein_descr = desc_list[i]
                #it is strange that protein_descr retrieved from xml is 'proprotein convertase subtilisin\kexin type 4 precursor [Homo sapiens]'
                #while in fasta file and database protein_descr is 'proprotein convertase subtilisin/kexin type 4 precursor [Homo sapiens]'
                protein_descr = protein_descr.replace('\\', '/')
                #proteinSeqInfo=session.query(ProteinSeqInfo).filter(and_(ProteinSeqInfo.name==protein,ProteinSeqInfo.desc==protein_descr)).first()  
                proteinSeqInfo = session.query(ProteinSeqInfo).filter(ProteinSeqInfo.name == protein).first()
                """
                if proteinSeqInfo != None:
                    peptideIdentification_ProteinSeqInfo = PeptideIdentification_ProteinSeqInfo()              
                    peptideIdentification_ProteinSeqInfo.proteinSeqInfo = proteinSeqInfo
                    pepIdentification.proteinSeqInfos.append(peptideIdentification_ProteinSeqInfo)
                """
                if proteinSeqInfo is not None:
                        #it is strange that this will add a record with  ()
                        #peptideIdentification_ProteinSeqInfo=PeptideIdentification_ProteinSeqInfo() 
                        peptideIdentificationID = pepIdentification.id
                        proteinSeqInfoID = proteinSeqInfo.id  
                        peptideIdentification_ProteinSeqInfo = PeptideIdentification_ProteinSeqInfo(peptideIdentificationID=peptideIdentificationID, proteinSeqInfoID=proteinSeqInfoID)           
                        peptideIdentification_ProteinSeqInfo.proteinSeqInfo = proteinSeqInfo
                        pepIdentification.proteinSeqInfos.append(peptideIdentification_ProteinSeqInfo)
                else:
                    err = protein + ',' + protein_descr + ' are not stored in table ProteinSeqInfo!'
                    raise Exception(err)
        session.commit()
    except Exception, e:
        session.rollback()
        stop_err('Error adding records to PeptideIdentification.\n%s' % (str(e)))      

#add iprobability
def updatePeptideIdentification(inputfile, outputfile):
    try:
        #method = 'InterProphet'        
        pep_qcResult = session.query(QCResult).filter(QCResult.filepath == inputfile).first() 
        print pep_qcResult
        pep_qcfile = pep_qcResult.filepath
        pep_qcResultID = pep_qcResult.id
        
        #</peptideprophet_result></analysis_result></search_hit></search_result></search_hit>
        qcResult = session.query(QCResult).filter(QCResult.filepath == outputfile).first()        
        if not qcResult:
            stop_err('Error adding records to PeptideIdentification due to the lack of QCResult.\n')
        qcResultID = qcResult.id
              
        pepfile = ET.parse(outputfile)
        root = pepfile.getroot()
        #spectrum_query = root.findall('./../{http://regis-web.systemsbiology.net/pepXML}spectrum_query')
        #print root
        for spectrum_query in root.iter('{http://regis-web.systemsbiology.net/pepXML}spectrum_query'):
            spectrum = spectrum_query.get('spectrum')
            #startScan = spectrum_query.get('start_scan')
            #endScan = spectrum_query.get('end_scan')
            #precursorNeutralMass = spectrum_query.get('precursor_neutral_mass')
            #assumedCharge = spectrum_query.get('assumed_charge')
            
            pepIdentification = session.query(PeptideIdentification).filter(and_(PeptideIdentification.qcResultID == pep_qcResultID, PeptideIdentification.spectrum == spectrum))[0]
            #retentionTime = spectrum_query.get('retention_time_sec')
            pepIdentificationID = pepIdentification.id
            
            search_hit = spectrum_query.find('./{http://regis-web.systemsbiology.net/pepXML}search_result/{http://regis-web.systemsbiology.net/pepXML}search_hit')
            if search_hit == None:
                stop_err('Error adding records to PeptideIdentification due to the lack of search_hits items in the pepxml file.\n')
            
            interprophet_result = search_hit.find('./{http://regis-web.systemsbiology.net/pepXML}analysis_result/{http://regis-web.systemsbiology.net/pepXML}interprophet_result')
            iprobability = interprophet_result.get('probability') 
            pepIdentification.iprobability = iprobability
            pepIdentification.qcResultID = qcResultID
            
            """ <interprophet_result probability="0.998024" all_ntt_prob="(0,0,0.998024)">
            <search_score_summary>
            #the five names are different from peptide prophet, for now store in the same table
            <parameter name="nss" value="0"/>
            <parameter name="nrs" value="0.4998"/>
            <parameter name="nse" value="0"/>
            <parameter name="nsi" value="0"/>
            <parameter name="nsm" value="0"/>
            </search_score_summary>
            </interprophet_result>
            """
            score_dict = {}
            score_summary = interprophet_result.find('./{http://regis-web.systemsbiology.net/pepXML}search_score_summary') 
            if score_summary != None:
                for parameter in score_summary.findall('{http://regis-web.systemsbiology.net/pepXML}parameter'):
                    name = parameter.get('name')
                    value = parameter.get('value')
                    score_dict[name] = value
                    #print name, value
                if 'nsm' not in score_dict:
                    score_dict['nsm'] = '-1'
                print score_dict      
            """ print '''qcResultID, spectrum,startScan,endScan, precursorNeutralMass, assumedCharge,retentionTime,
                                      peptide,peptidePrevAa, peptideNextAa, numTotProteins,numMatchedIons,totNumIons,calcNeutralPepMass,numMissedCleavages,modification,
                                      probability'''
            """                           
            #pepIdentificationID,nss,ntt,nmc,massd,isomassd
            #searchScoreSummary=SearchScoreSummary('',score_dict['fval'],score_dict['ntt'],score_dict['nmc'],score_dict['massd'],score_dict['isomassd'])
            searchScoreSummaries = session.query(SearchScoreSummary).filter(SearchScoreSummary.pepIdentificationID == pepIdentificationID)
            if not searchScoreSummaries and len(searchScoreSummaries) > 0:
                searchScoreSummary = searchScoreSummaries[0]
                print searchScoreSummary
                searchScoreSummary.nss = score_dict['nss']
                searchScoreSummary.ntt = score_dict['nrs']
                searchScoreSummary.nmc = score_dict['nse']
                searchScoreSummary.massd = score_dict['nsi']
                searchScoreSummary.isomassd = score_dict['nsm']
            else:
                searchScoreSummary = SearchScoreSummary('', score_dict['nss'], score_dict['nrs'], score_dict['nse'], score_dict['nsi'], score_dict['nsm'])
                print searchScoreSummary
                pepIdentification.searchScoreSummary.append(searchScoreSummary)
        session.commit()
    except Exception, e:
         stop_err('Error updating records in PeptideIdentification.\n%s' % (str(e)))      
 
"""
xinteract  -N/usr/local/tpp/data/1percent_yeast20ul02.2012_08_24_15_03_37.t.tandem.interact.pep.xml -p0.05 -l7 
-OAP -d###RND### /usr/local/tpp/data/1percent_yeast20ul02.2012_08_24_15_03_37.t.tandem.pep.xml
"""
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
        """
        else:
            storeQCResult(options.input, outpath, options.dbop_type)
            storeFDRParam(outpath, options.dbop_type)
            #storePeptideIdentification(outpath)
            updatePeptideIdentification(options.input, outpath, options.dbop_type)
        """
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
        
        stop_err('Error running InterProphet.\n%s\n' % (str(e)))
             

    
def __main__():
    #Parse Command Line
    parser = optparse.OptionParser()
    parser.add_option('', '--input', dest='input', help=' ')
    parser.add_option('-S', '--nonss', dest='nonss', action='store', help='do not use numbe of sibling searches model')
    parser.add_option('-R', '--nonrs', dest='nonrs', action='store', help='do not use number replicate spectra model')
    parser.add_option('-E', '--nonse', dest='nonse', action='store', help='do not use number of sibling MS/MS runs model')
    parser.add_option('-I', '--nonsi', dest='nonsi', action='store', help='do not use number sibling ions model')
    parser.add_option('-M', '--nonsm', dest='nonsm', action='store', help='do not use number sibling mods model')   
    parser.add_option('-o', '--output', dest='output', action='store', help='write output to file')
    parser.add_option('-d', '--outputdir', dest='outputdir', action='store', default="/tmp/interProphet")
    parser.add_option('', '--dbop_type', dest='dbop_type', action='store', help='')
    (options, args) = parser.parse_args()    
   
    if not os.path.exists(options.outputdir): 
        os.makedirs(options.outputdir)
    #change ext from .dat to .pep.xml
    inputfile_list = []
    inputfile_list.append(options.input)
    for i, arg in enumerate(args):
        #print i, arg
        inputfile_list.append(arg)
        
    infilebase = os.path.splitext(os.path.basename(options.input))[0]  
    outfilename = os.path.join(options.outputdir, ''.join([infilebase, '.interact.iproph.pep.xml'])) 

    cmd = 'InterProphetParser '
    if options.nonss == 'true':
        cmd += ' NONSS'
    if options.nonrs == 'true':
        cmd += ' NONRS'
    if options.nonse == 'true':
        cmd += ' NONSE'
    if options.nonsi == 'true':
        cmd += ' NONSI'
    if options.nonsm == 'true':
        cmd += ' NONSM'
    #cmd += ' ' + infilename

    """
    for all pepxml input, name suffix needs be replaced
    """
    for inputfile in inputfile_list:
        inputfile_name = inputfile.replace('.dat', '.interact.pep.xml')
        if not os.path.isfile(inputfile_name):
            os.symlink(inputfile, inputfile_name)
            #shutil.copy2(inputfile, inputfile_name)
        cmd += " %s" % inputfile_name
        
    cmd += ' ' + outfilename   
    """
    cmd='xinteract '
    
    # Add options.
    cmd += ' -i'
    if options.nonss:
        cmd += 'S'
    if options.nonrs:
        cmd += 'R'
    if options.nonse:
        cmd += 'E'
    if options.nonsi:
        cmd += 'I'
    if options.nonsm:
        cmd += 'M'
    cmd +=' '+infilename
    """
    # Debugging.
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
    
    '''
    xinteract -Ndataset_1766.interact.pep.xml -O dataset_1766.pep.xml
    '''
    print cmd
    
    method = 'InterProphet' 
    (status, dbsearchResultID_list) = checkDatabase(inputfile_list, method, options.output, options.dbop_type)
    #print status
    if status:
        #print 'go here'
        returncode = runTool(cmd)
        if returncode == 0:
            qcResultID = storeQCResult(dbsearchResultID_list, outpath, method)    
            storePeptideIdentification(qcResultID, outpath)
            storeFDRParam(qcResultID, outpath) 

    
    
if __name__ == "__main__": __main__()
