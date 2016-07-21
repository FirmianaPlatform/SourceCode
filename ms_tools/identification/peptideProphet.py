#!/usr/bin/env python
"""
usage: peptideProphet.py ${output} ${input_file}  
    -r $glyco $useicat $phospho $usepi $usert $accurate_mass $no_ntt $no_nmc 
    $use_gamma $use_only_expect $force_fit $allow_alt_instruments $maldi
    
    Run PeptideProphet on a set of pep.xml input files.\n\nUsage: peptide_prophet.rb [options] file1.pep.xml file2.pep.xml ..."
"""

import sys, optparse, os, tempfile, subprocess, shutil, re
#import xml.etree.ElementTree as ET
from lxml import etree as ET
#from django.db import models
sys.path.append("/usr/local/firmiana/galaxy-dist/tools/ms_tools/")
from models.firmiana_models import *
from models.gardener_control import *

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
        select * from firmiana_DBSearchResult_QCResult 
        where qcResultID not in
        (select qcResultID from firmiana_DBSearchResult_QCResult
        where dbsearchResultID not in (1,2))
        group by qcResultID having count(dbsearchResultID)=2;
        
        /usr/local/lib/python2.7/dist-packages/sqlalchemy/sql/expression.py:1925: 
        SAWarning: The IN-predicate on "firmiana_DBSearchResult_QCResult.qcResultID" was invoked with an empty sequence. 
        This results in a contradiction, which nonetheless can be expensive to evaluate.  
        Consider alternative strategies for improved performance.
  return self._in_impl(operators.in_op, operators.notin_op, other)
"""

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

def getQCResultID(dbsearchResult_list):
    dbsearchResultID_list = []
    for dbsearchResult in dbsearchResult_list:
        dbsearchResultID_list.append(dbsearchResult.id)
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
    print qcResultID_list
    return qcResultID_list    

#choose qcResultID corresponding to method
def getQCResultIDForMethod(qcResultID_list, method):
    rval = []
    for qcResultID in qcResultID_list:
        qcResult = session.query(QCResult).filter(QCResult.id == qcResultID).first()
        if qcResult.method == method:
            rval.append(qcResultID)  
    return rval
               

def getExperimentIDs(external_experimentID_list):
    experimentID_list = []
    for externalExperimentID in external_experimentID_list:
        experiment = session.query(Experiment).filter(Experiment.externalExperimentID == externalExperimentID).first()        
        experimentID = experiment.id
        experimentID_list.append(experimentID)
    return experimentID_list


def getFilesPerExp(experimentID_list, dbsearch_type):
    #pepxml_files_dict={}
    #mzxml_files_dict={}
    pepxml_files = []
    mzxml_files = []
    for experimentID in experimentID_list:
        for rawfile in session.query(MSRunRawfile).filter(and_(MSRunRawfile.experimentID == experimentID)):            
            #print rawfile
            #file=instance.filepath
            rawfileID = rawfile.id
            fileType = 'mzxml'
            converted_rawfile = session.query(ConvertedRawfile).filter(and_(ConvertedRawfile.rawfileID == rawfileID, ConvertedRawfile.fileType == fileType)).first()
            if converted_rawfile:
                #print converted_rawfile
                convertedRawfileID = converted_rawfile.id
                #print convertedRawfileID
                #one mzxml file can be searched several times???
                #dbsearchResult=session.query(DBSearchResult).filter(DBSearchResult.convertedRawfileID==convertedRawfileID).first()
                dbsearchResult = session.query(DBSearchResult).filter(and_(DBSearchResult.convertedRawfileID == convertedRawfileID, DBSearchResult.searchType == dbsearch_type)).first()
                #print dbsearchResult
                #qcResult=dbsearchResult.qcResults[0]
                if dbsearchResult is None:
                    stop_err('The experiment(s) may not have been searched using %s, please check again.' % dbsearch_type)    
                pepxml_file = dbsearchResult.pepfilepath        
                pepxml_files.append(pepxml_file)
            else:
                 stop_err('no converted mzxml files for this experiment.')
                 
    return pepxml_files

'''
inputfile_list: converted database search result
method: QC type, such as  PeptideProphet
output: file to write prompt
'''
def checkDatabase(inputfile_list, method, output, dbop_type):
    try:
        #to avoid repeatedly store PeptideProphet result for the same DBSearchResult
        #qcResult=session.query(QCResult).filter(QCResult.filepath==resultfilepath).first() 
        #if qcResult:
             #session.delete(qcResult)
             #session.commit()
        #according to inputfile, find DBSearchResult, then  DBSearchResult_QCResult, QCResult
        """
        here only checked the first input,
        actually one qcresult may correspond to several dbsearchResults
        when rerunning this tool, all related dbsearchResult_QCResults should be updated
        one pepxml file from peptideprophet may invovle in several QC runs
        """
        dbsearchResult_list = []
        qcResultID_list = []
        for input in inputfile_list:
            dbsearchResult = session.query(DBSearchResult).filter(DBSearchResult.pepfilepath == input).first()
            if dbsearchResult is None:
                stop_err('Error adding records to QCResult due to the lack of pepxml filepath in DBSearchResult record.\n')
            dbsearchResult_list.append(dbsearchResult)
            dbsearchResultID = dbsearchResult.id
            """
            dbsearchResult_QCResults = session.query(DBSearchResult_QCResult).filter(DBSearchResult_QCResult.dbsearchResultID == dbsearchResultID)           
            qcResultID = None               
            for dbsearchResult_QCResult in dbsearchResult_QCResults:
                qcResult = dbsearchResult_QCResult.qcResult
                #if qcResult.method == 'PeptideProphet': 
                #all other qcresults rely on peptideprophet, so qcResultID_list must contain all qcresults
                qcResultID = dbsearchResult_QCResult.qcResultID
                qcResultID_list.append(qcResultID)
                    #break
            """
        qcResultID_list = getQCResultID(dbsearchResult_list)
        pep_qcResultID_list = getQCResultIDForMethod(qcResultID_list, method) 
        #f = open('/home/ice/firout/firtest', 'w')
        #here should find only one qcResultID corresponding to last run 
        if pep_qcResultID_list is not None and len(pep_qcResultID_list) > 0:            
             #for dbsearchResult_QCResult in dbsearchResult_QCResults:
                 #qcResultID_list.append(dbsearchResult_QCResult.qcResultID)            
             #when deleting dbsearchResult_QCResult, QCResult will be automatically deleted by cascade,
             #so are tables referring QCResult, like FDRParam and PeptideIdentification
             if dbop_type == 'update':  
                 #qcResultID=dbsearchResult_QCResult.qcResultID  
                 for  qcResultID in pep_qcResultID_list:
                     #f.write(str(qcResultID))
                     pepIdentifications = session.query(PeptideIdentification).filter(PeptideIdentification.qcResultID == qcResultID) 
                     for pepIdentification in pepIdentifications:
                         #should first delete Peptide_Protein_Identification
                         peptide_Protein_Identifications = session.query(Peptide_Protein_Identification).filter(Peptide_Protein_Identification.peptideIdentificationID == pepIdentification.id)
                         for peptide_Protein_Identifications in peptide_Protein_Identifications:
                             session.delete(peptide_Protein_Identifications)
                         session.delete(pepIdentification) 
                     fdrs = session.query(FDRParam).filter(FDRParam.qcResultID == qcResultID) 
                     for fdr in fdrs:
                         session.delete(fdr)
                     """
                     delete all dbsearchResult_QCResults corresponding to the same QCResult
                     """
                     dbsearchResult_QCResults = session.query(DBSearchResult_QCResult).filter(DBSearchResult_QCResult.qcResultID == qcResultID).all()
                     for dbsearchResult_QCResult in dbsearchResult_QCResults:
                         #f.write(':' + str(dbsearchResult_QCResult.dbsearchResultID))                         
                         session.delete(dbsearchResult_QCResult) 
                     #f.close()                                                     
                 return (True, dbsearchResult_list)                                
             elif dbop_type == 'delete': 
                 #qcResultID=dbsearchResult_QCResult.qcResultID   
                 #del dbsearchResult_QCResult.qcResult
                 #session.delete(dbsearchResult_QCResult)
                 for qcResultID in pep_qcResultID_list:  
                    pepIdentifications = session.query(PeptideIdentification).filter(PeptideIdentification.qcResultID == qcResultID) 
                    for pepIdentification in pepIdentifications:
                         peptide_Protein_Identifications = session.query(Peptide_Protein_Identification).filter(Peptide_Protein_Identification.peptideIdentificationID == pepIdentification.id)
                         for peptide_Protein_Identifications in peptide_Protein_Identifications:
                             session.delete(peptide_Protein_Identifications)                        
                         session.delete(pepIdentification) 
                    fdrs = session.query(FDRParam).filter(FDRParam.qcResultID == qcResultID) 
                    for fdr in fdrs:
                        session.delete(fdr)
                    dbsearchResult_QCResult = session.query(DBSearchResult_QCResult).filter(DBSearchResult_QCResult.qcResultID == qcResultID).first()
                    session.delete(dbsearchResult_QCResult)                                               
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
                stop_err('Error checking records in QCResult.\n%s\n' % ''.join(errlist))
        else:
            #print 'dbsearchResult is None'
            if dbop_type == 'update' or dbop_type == 'delete':      
                err = 'There is no information about this analysis in the database.'
                stop_err('Error changing information for QCResult in the database.\n%s\n' % err)       
            return (True, dbsearchResult_list)       
    except Exception, e:
        session.rollback()
        stop_err('Error checking records in QCResult.\n%s' % (str(e))) 

#filepath,method and DBSearchResult_QCResult
def storeQCResult(dbsearchResults, resultfilepath, method):
    try:
        #method = 'PeptideProphet'      
        qcResult = QCResult(resultfilepath, method)
        #print qcResult
        session.add(qcResult) #child
        #session.commit()
        """
        # create parent, append a child via association
        p = Parent()
        a = Association(extra_data="some data")
        a.child = Child()
        p.children.append(a)
        """
        #to return qcResultID, have to first query, or else the return value will be NULL
        qcResult = session.query(QCResult).filter(QCResult.filepath == resultfilepath).first() 
        qcResultID = qcResult.id
        #dbsearchResult=session.query(DBSearchResult).filter(DBSearchResult.pepfilepath==inputfile).first()
        #dbsearchResult_QCResult=DBSearchResult_QCResult()  #it is strange that this will add a record with  dbsearchResultID=0
        for dbsearchResult in dbsearchResults:       
            dbsearchResult_QCResult = DBSearchResult_QCResult(qcResultID=qcResultID, dbsearchResultID=dbsearchResult.id)
            dbsearchResult_QCResult.qcResult = qcResult
            dbsearchResult.qcResults.append(dbsearchResult_QCResult)
        
        session.commit()
        return qcResultID
    except Exception, e:
        session.rollback()
        stop_err('Error adding records to QCResult.\n%s' % (str(e))) 
 
         
#qcResultID, error, minProb, numCorr, numIncorr
#def storeFDRParam(outputfile):
def storeFDRParam(qcResultID, outputfile):
    try:
        """
        qcResult = session.query(QCResult).filter(QCResult.filepath == outputfile).first()        
        if not qcResult:
            stop_err('Error adding records to FDRParam due to the lack of QCResult.\n')
        qcResultID = qcResult.id
        
        fdrs = session.query(FDRParam).filter(FDRParam.qcResultID == qcResultID).first() 
        if fdrs:
             session.delete(fdrs)     
        """     
            #print instance
        #print outputfile
        pepfile = ET.parse(outputfile)
        root = pepfile.getroot()
        #print root
        search_hits = root.findall('./{http://regis-web.systemsbiology.net/pepXML}analysis_summary/{http://regis-web.systemsbiology.net/pepXML}peptideprophet_summary/{http://regis-web.systemsbiology.net/pepXML}roc_error_data/{http://regis-web.systemsbiology.net/pepXML}error_point')
        #for search_hit in root.iter('{http://regis-web.systemsbiology.net/pepXML}error_point'):
        if search_hits == None:
            stop_err('Error adding records to FDRParam due to the lack of error_point items in the pepxml file.\n')
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
         
#qcResultID,spectrum,startScan,endScan, precursorNeutralMass, assumedCharge,retentionTime, 
#peptide,peptidePrevAa, peptideNextAa, numTotProteins,numMatchedIons,totNumIons,calcNeutralPepMass,numMissedCleavages,
#probability,labelFreeQuant
#def storePeptideIdentification(outputfile, method):
def storePeptideIdentification(qcResultID, outputfile):
    try:
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
            #print instance
        pepfile = ET.parse(outputfile)
        root = pepfile.getroot()
       
        #spectrum_query = root.findall('./../{http://regis-web.systemsbiology.net/pepXML}spectrum_query')
        #print root
        for spectrum_query in root.iter('{http://regis-web.systemsbiology.net/pepXML}spectrum_query'):
            #print spectrum_query
            spectrum = spectrum_query.get('spectrum')
            startScan = spectrum_query.get('start_scan')
            endScan = spectrum_query.get('end_scan')
            precursorNeutralMass = spectrum_query.get('precursor_neutral_mass')
            assumedCharge = spectrum_query.get('assumed_charge')
            retentionTime = spectrum_query.get('retention_time_sec')
            #print 'retentionTime:',retentionTime
            
            """
            <search_hit hit_rank="1" peptide="VAINGFGR" peptide_prev_aa="R" peptide_next_aa="I" 
            protein="YGR192C" protein_descr="TDH3 SGDID:S000003424, Chr VII from 883815-882817, reverse complement,
             Verified ORF, Glyceraldehyde-3-phosphate dehydrogenase, isozyme 3, involved in glycolysis and gluconeogenesis; 
             tetramer that catalyzes the reaction of glyceraldehyde-3-phosphate to 1,3 bis-phosphoglycerate; 
             detected in the cytoplasm and cell-wall " num_tot_proteins="2" num_matched_ions="12" tot_num_ions="14" 
            calc_neutral_pep_mass="832.4555" massdiff="0.006" num_tol_term="2" num_missed_cleavages="0" is_rejected="0">
            """
            search_hit = spectrum_query.find('./{http://regis-web.systemsbiology.net/pepXML}search_result/{http://regis-web.systemsbiology.net/pepXML}search_hit')
            if search_hit != None:
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
            
                #one peptide may correspond to several proteins
                """
                <search_hit hit_rank="1" peptide="NVKEEETVAK" peptide_prev_aa="K" peptide_next_aa="S" protein="YBL072C" protein_descr="RPS8A SGDID:S000000168, Chr II from 89123-88521, reverse complement, Verified ORF, Protein component of the small (40S) ribosomal subunit; identical to Rps8Ap and has similarity to rat S8 ribosomal protein" num_tot_proteins="2" num_matched_ions="9" tot_num_ions="18" calc_neutral_pep_mass="1161.6212" massdiff="0.000" num_tol_term="2" num_missed_cleavages="1" is_rejected="0">
                <alternative_protein protein="YER102W" protein_descr="RPS8B SGDID:S000000904, Chr V from 363096-363698, Verified ORF, Protein component of the small (40S) ribosomal subunit; identical to Rps8Bp and has similarity to rat S8 ribosomal protein" num_tol_term="2" peptide_prev_aa="K" peptide_next_aa="S"/>
                <modification_info modified_peptide="NVK[136]EEETVAK[136]">
                """
                protein = search_hit.get('protein')
                protein_descr = search_hit.get('protein_descr')           
                alternative_proteins = search_hit.findall('./{http://regis-web.systemsbiology.net/pepXML}alternative_protein')
                if alternative_proteins != None:
                    for alternative_protein in alternative_proteins:
                        alternative_protein_name = alternative_protein.get('protein')
                        alternative_protein_descr = alternative_protein.get('protein_descr')
                        protein += ';' + alternative_protein_name
                        protein_descr += ';' + alternative_protein_descr
             
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
                
                """ <peptideprophet_result probability="0.8236" all_ntt_prob="(0.0000,0.0000,0.8236)">
                <search_score_summary>
                <parameter name="fval" value="0.0311"/>
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
                #print score_dict        
                """ print '''qcResultID, spectrum,startScan,endScan, precursorNeutralMass, assumedCharge,retentionTime,
                                      peptide,peptidePrevAa, peptideNextAa, numTotProteins,numMatchedIons,totNumIons,calcNeutralPepMass,numMissedCleavages,modification,
                                      probability'''
                """                        
                pepIdentification = PeptideIdentification(qcResultID, spectrum, startScan, endScan, precursorNeutralMass, assumedCharge, retentionTime,
                                      peptide, peptidePrevAa, peptideNextAa, numTotProteins, numMatchedIons, totNumIons, calcNeutralPepMass, numMissedCleavages, modification,
                                      probability, None, None, None)
                #print pepIdentification
                session.add(pepIdentification)
                
                #pepIdentificationID,fval,ntt,nmc,massd,isomassd
                searchScoreSummary = SearchScoreSummary('', score_dict['fval'], score_dict['ntt'], score_dict['nmc'], score_dict['massd'], score_dict['isomassd'])
                #print searchScoreSummary
                pepIdentification.searchScoreSummary.append(searchScoreSummary)
                #store protein information into table 
                protein_list = protein.split(';')
                #print protein_list
                desc_list = protein_descr.split(';')
                proteinNum = len(protein_list)
                #del pepIdentification.proteinSeqInfos
                for i in range(proteinNum):
                    protein = protein_list[i]
                    protein_descr = desc_list[i]
                    #print protein_descr
                    #it is strange that protein_descr retrieved from xml is 'proprotein convertase subtilisin\kexin type 4 precursor [Homo sapiens]'
                    #while in fasta file and database protein_descr is 'proprotein convertase subtilisin/kexin type 4 precursor [Homo sapiens]'
                    protein_descr = protein_descr.replace('\\', '/')
                    """strange isssue: ###RND###gi|81158224|ref|NP_005001.3|_UNMAPPED,
                    originally identified as ###RND###gi|81158224|ref|NP_005001.3| 
                    in database /opt/galaxy-dist/database/sequence/SwissProt/SwissProt_51.6.fasta 
                    causes: mascot to pepxml, selecting wrong database
                    """
                    #print protein_descr
                    #proteinSeqInfo=session.query(ProteinSeqInfo).filter(and_(ProteinSeqInfo.name==protein,ProteinSeqInfo.desc==protein_descr)).first()  
                    proteinSeqInfo = session.query(ProteinSeqInfo).filter(ProteinSeqInfo.name == protein).first()
                    #print proteinSeqInfo
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
                        
def runTool(cmd):          
    try:
        #Run command.
        tmp_name = tempfile.NamedTemporaryFile(dir=".").name
        tmp_stderr = open(tmp_name, 'wb')
        #OK to use multiple job handlers
        proc = subprocess.Popen(args=cmd, shell=True, stderr=tmp_stderr.fileno())
        #This will deadlock when using stdout=PIPE and/or stderr=PIPE and 
        #the child process generates enough output to a pipe 
        #such that it blocks waiting for the OS pipe buffer to accept more data. Use communicate() to avoid that
        returncode = proc.wait()
        #returncode = subprocess.call( args=cmd, shell=True )
        #streamdata = proc.communicate()
        #print streamdata
        #returncode = proc.returncode
        tmp_stderr.close()
        
        # Error checking.
        if returncode != 0:
            raise Exception, "return code = %i" % returncode
        #else:
            #storeQCResult(options.input,outpath, options.dbop_type)
            #storeFDRParam(outpath, options.dbop_type)
            #storePeptideIdentification(outpath, options.dbop_type)
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
        
        stop_err('Error running PeptideProphet.\n%s\n' % (str(e)))
             
        
def getCmd():
    #Parse Command Line
    parser = optparse.OptionParser()
    parser.add_option('', '--input', dest='input', help=' ')
    parser.add_option('-g', '--glyco', dest='glyco', action='store', help='Expect true positives to have a glycocapture motif')
    parser.add_option('-i', '--useicat', dest='useicat', action='store', help='Use icat information')
    parser.add_option('-f', '--no-useicat', dest='no_useicat', action='store', help='Do not use icat information')
    parser.add_option('-H', '--phospho', dest='phospho', action='store', help='Use phospho information')
    parser.add_option('-I', '--usepi', dest='usepi', action='store', help='Use pI information')
    parser.add_option('-R', '--usert', dest='usert', action='store', help='Use hydrophobicity / RT information')
    parser.add_option('-A', '--accurate-mass', dest='accurate_mass', action='store', help='Use accurate mass binning')
    parser.add_option('-N', '--no-ntt', dest='no_ntt', action='store', help='Do not use NTT model')
    parser.add_option('-M', '--no-nmc', dest='no_nmc', action='store', help='Do not use NMC model')
    parser.add_option('-G', '--use-gamma', dest='use_gamma', action='store', help='use Gamma Distribution to model the Negatives (applies only to X!Tandem data)')
    parser.add_option('-E', '--use-only-expect', dest='use_only_expect', action='store', help='only use Expect Score as the Discriminant(applies only to X!Tandem data, helpful for data with homologous top hits e.g. phospho or glyco)')
    parser.add_option('-F', '--force-fit', dest='force_fit', action='store', help='force the fitting of the mixture model, bypass automatic mixture model checks')
    parser.add_option('-w', '--allow-alt-instruments', dest='allow_alt_instruments', action='store', help='warning instead of exit with error if instrument types between runs is different')
    parser.add_option('-m', '--maldi', dest='maldi', action='store', help='maldi data')
    parser.add_option('-t', '', dest='no_png', action='store', help='do not create png data plot')
    parser.add_option('-o', '', dest='output', action='store', help='write output to file')
    parser.add_option('-p', '', dest='prob_cutoff', type="float", action='store', help='do not discard search results with PeptideProphet probabilities below 0.05')
    parser.add_option('', '--min-peptide-len', dest='min_peptide_len', type="int", action='store', help='minimum peptide length considered in the analysis (default 7)')
    parser.add_option('-d', '--outputdir', dest='outputdir', action='store', default="/tmp/peptideProphet")
    #parser.add_option('', '--dbop_type', dest='dbop_type', action='store', help='')
    parser.add_option('', '--dbsearch_type', dest='dbsearch_type', action='store', type="string", help='')
    parser.add_option('', '--source_select', dest='source_select', action='store', type="string", help='')
    parser.add_option('', '--store_to_db', dest='store_to_db', action='store', help='')
    parser.add_option('-j', '--job_track_id', dest='job_track_id', action='store', type="string", help='Job track ID for firmiana.')
    parser.add_option('-u', '--user_id', dest='user_id', action='store', type="string", help='User id for galaxy runner.')
    parser.add_option('-a', '--label_name', dest='label_name', action='store', type="string", help='Label name for out file.')
    (options, args) = parser.parse_args()

    #such as: dataset_769_files
    if not os.path.exists(options.outputdir): 
        os.makedirs(options.outputdir)

    #change ext from .dat to .pep.xml, or else xinteract could not be executed
    inputfile_list = []
    outfilename = ''
    
    if options.source_select == 'experimentID':
        infilebase = ''.join(['Experiment', str(options.input)])
    else:
        infilebase = os.path.splitext(os.path.basename(options.input))[0]  
        #output file ext should be .interact.pep.xmls
    outfilename = os.path.join(options.outputdir, ''.join([infilebase, '.interact.pep.xml'])) 
    
    # Add options.
    cmd = '/usr/local/firmiana/external_tools/tpp_4.6.2/bin/xinteract -N%s' % outfilename

    if options.prob_cutoff:
        cmd += ' -p' + str(options.prob_cutoff)
    if options.min_peptide_len:
        cmd += ' -l' + str(options.min_peptide_len)
    cmd += ' -O'
    if options.glyco == 'true':
        cmd += 'g'
    if options.useicat == 'true':
        cmd += 'i'
    if options.no_useicat == 'true':
        cmd += 'f'
    if options.phospho == 'true':
        cmd += 'H'
    if options.usepi == 'true':
        cmd += 'I'
    if options.usert == 'true':
        cmd += 'R'
    if options.accurate_mass == 'true':
        cmd += 'A'
    if options.no_ntt == 'true':
        cmd += 'N'
    if options.no_nmc == 'true':
        cmd += 'M'
    if options.use_gamma == 'true':
        cmd += 'G'
    if options.use_only_expect == 'true':
        cmd += 'E'
    if options.force_fit == 'true':
        cmd += 'F'
    if options.allow_alt_instruments == 'true':
        cmd += 'w'
    if options.maldi == 'true':
        cmd += 'm'
    #dataset_325.interact.pep_FVAL_1.png,...dataset_325.interact.pep_FVAL_7.png,dataset_325.interact.pep_IPPROB.png,dataset_325.interact.pep_PPPROB.png
    if options.no_png == 'true':
        cmd += 't '
    
    if options.source_select == 'experimentID': 
        eid1 = options.input        
        external_experimentID_list = [eid1] 
        experimentID_list = getExperimentIDs(external_experimentID_list)
        inputfile_list = getFilesPerExp(experimentID_list, options.dbsearch_type)
    else:
        inputfile_list.append(options.input)
        for i, arg in enumerate(args):      
            inputfile_list.append(arg)
            
    for i, arg in enumerate(inputfile_list):
        add_file = arg.replace('.dat', '.pep.xml')
        if not os.path.isfile(add_file):
            os.symlink(arg, add_file)
            #shutil.copy2(arg, add_file)
        cmd += " %s" % add_file 
           
    # Debugging.
    #mv can overide current files with the same name
    #Moved /opt/galaxy-dist/database/job_working_directory/000/331/galaxy_dataset_554.dat to /opt/galaxy-dist/database/files/000/dataset_554.dat
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
    method = 'PeptideProphet' 
    
    if options.store_to_db=='yes':   
        (storename,file_data,file)=sql_gardener_file(options,conn,meta)
        cmd += '; wait; cp ' + options.output + ' ' + store_file_path+"/" +storename
        runTool(cmd)
        file_data['size']= str(os.path.getsize(options.output)/1024)+'K'
        result=update_file(conn,meta,file_data,file)
    else:
        runTool(cmd)
    """
    (status, dbsearchResults) = checkDatabase(inputfile_list, method, options.output, options.dbop_type)
    #print status
    if status:
        #print 'go here'
        returncode = runTool(cmd)
        if returncode == 0:
            qcResultID = storeQCResult(dbsearchResults, outpath, method)    
            storePeptideIdentification(qcResultID, outpath)
            storeFDRParam(qcResultID, outpath)
    """
    
if __name__ == "__main__": __main__()
