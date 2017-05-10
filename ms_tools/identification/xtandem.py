#!/usr/bin/env python

import optparse, os, shutil, subprocess, sys, tempfile, re
from elementtree.ElementTree import XML
#import xml.etree.ElementTree as ET
from lxml import etree as ET
import re
sys.path.append("/usr/local/firmiana/galaxy-dist/tools/ms_tools/")
from models.firmiana_models import *
from config.firmianaConfig import *

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

tpp_bin = ConfigSectionMap("Tool")['tpp_bin'] 

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


def checkDatabase(input, searchType, output, dbop_type):
    try:
        convertedRawfile = session.query(ConvertedRawfile).filter(ConvertedRawfile.filepath == input).first()
        if not convertedRawfile:
            stop_err('Error adding records to DBSearchResult due to the lack of ConvertedRawfile record.\n')
        convertedRawfileID = str(convertedRawfile.id)
        
        #dbsearchResult=session.query(DBSearchResult).filter(DBSearchResult.filepath==resultfilepath).first()
        #for each converted raw file, given the db search method(mascot, tandem), there should be only one DBSearchResult.
        dbsearchResult = session.query(DBSearchResult).filter(and_(DBSearchResult.convertedRawfileID == convertedRawfileID, DBSearchResult.searchType == searchType)).first()
        #if dbsearchResult:
            #session.delete(dbsearchResult) 
        if dbsearchResult is not None:
             #if a workflow based on tandem has been run, 
             #then after running a workflow based on mascot, 
             #all the record related with the first run will be deleted on cascade  
             #solution: the workflow should begin with DBSearch
             if dbop_type == 'update':       
                 session.delete(dbsearchResult)
                 return (True, convertedRawfileID)                                
             elif dbop_type == 'delete':    
                 session.delete(dbsearchResult)
                 session.commit()
                 writePrompt(output)  
                 return (False, None)  
             else:   
                errlist = []         
                errlist.append('This file has been searched against database by %s.\n' % searchType)
                errlist.append('If you want to search this file against database by %s again,\n' % searchType) 
                errlist.append('please choose "update" in the drop-down box "Change the information of the result for this analysis in the database".\n')
                errlist.append('Or else the original information in the database will be kept.')
                #print err
                stop_err('Error adding records to DBSearchResult.\n%s\n' % ''.join(errlist))
        else:
            #print 'experiment is None'
            if dbop_type == 'update' or dbop_type == 'delete':      
                err = 'There is no information about this analysis in the database.'
                stop_err('Error changing information for DBSearchResult in the database.\n%s\n' % err)       
            return (True, convertedRawfileID)       
    except Exception, e:
         stop_err('Error checking records in DBSearchResult.\n%s' % (str(e))) 

def storeDBSearchResult(convertedRawfileID, searchType, resultfilepath, options, paramfile, taxonfile):                
    try:
        dbsearchResult = DBSearchResult(convertedRawfileID, searchType, resultfilepath, '')
        print dbsearchResult
        #store parameters at the same time
        xtandemParam = XtandemParam('', options.database, options.var_mods, options.fix_mods, options.enzyme, options.precursor_tolu, options.missed_cleavages, options.fragment_ion_tol, options.precursor_ion_tol, paramfile, taxonfile)
        dbsearchResult.xtandemParams.append(xtandemParam)
        session.add(dbsearchResult)
        session.commit()
    except Exception, e:
        session.rollback()
        stop_err('Error adding records to DBSearchResult.\n%s' % (str(e))) 
         
#database,var_mods,fix_mods,enzyme,precursor_tolu,missed_cleavages,fragment_ion_tol,precursor_ion_tol,tandem_params
def storeXtandemParam(filepath, database, var_mods, fix_mods, enzyme, precursor_tolu, missed_cleavages, fragment_ion_tol, precursor_ion_tol, paramfile, taxonfile):
    try:
        dbsearchResult = session.query(DBSearchResult).filter(DBSearchResult.filepath == filepath).first()
        if not dbsearchResult:
            stop_err('Error adding records to XtandemParam due to the lack of DBSearchResult.\n')
        dbsearchResultID = str(dbsearchResult.id)
        
        xtandemParam = session.query(XtandemParam).filter(XtandemParam.dbsearchResultID == dbsearchResultID).first()
        #if xtandemParam:
            #session.delete(xtandemParam) 
        if dbsearchResult is not None:
             #if a workflow based on tandem has been run, 
             #then after running a workflow based on mascot, 
             #all the record related with the first run will be deleted on cascade  
             #solution: the workflow should begin with DBSearch
             if dbop_type == 'update':       
                 session.delete(dbsearchResult)                             
             elif dbop_type == 'delete':    
                 session.delete(dbsearchResult)
                 session.commit()
                 writePrompt(output)  
                 return  
             else:   
                errlist = []         
                errlist.append('This file has been searched against database by %s.\n' % searchType)
                errlist.append('If you want to search this file against database by %s again,\n' % searchType) 
                errlist.append('please choose "update" in the drop-down box "Change the information of the result for this analysis in the database".\n')
                errlist.append('Or else the original information in the database will be kept.')
                #print err
                stop_err('Error adding records to XtandemParam.\n%s\n' % ''.join(errlist))
        else:
            #print 'experiment is None'
            if dbop_type == 'update' or dbop_type == 'delete':      
                err = 'There is no information about this analysis in the database.'
                stop_err('Error changing information for XtandemParam in the database.\n%s\n' % err)       
                
        xtandemParam = XtandemParam(dbsearchResultID, database, var_mods, fix_mods, enzyme, precursor_tolu, missed_cleavages, fragment_ion_tol, precursor_ion_tol, paramfile, taxonfile)
        #print xtandemParam
        session.add(xtandemParam)
        session.commit()
    except Exception, e:
         stop_err('Error adding records to XtandemParam.\n%s' % (str(e))) 
         
         
# Galaxy changes things like @ to __at__ we need to change it back
def decode_modification_string(mstring):
    re.sub("__at__", "@")
    re.sub("__oc__", "{")
    re.sub("__cc__", "}")
    re.sub("__ob__", "[")
    re.sub("__cb__", "]")

#ElementTree1.3 supports xpath, and python 2.7 is required
def generate_parameter_doc_py27(std_params, output_path, input_path, taxo_path, current_db, options, params_path):  
    # Set the input and output paths 
    input_notes = std_params.findall("./note[@type='input'][@label='spectrum, path']")
    if not len(input_notes) == 1:
        stop_err("Exactly one spectrum, path note is required in the parameter file")
    input_notes[0].text = input_path

    output_notes = std_params.findall("./note[@type='input'][@label='output, path']")
    if not len(output_notes) == 1:
        stop_err("Exactly one output, path note is required in the parameter file") 
    output_notes[0].text = output_path
  
    # Set the path to the scoring algorithm default params. We use one from ISB
    scoring_notes = std_params.findall("./note[@type='input'][@label='list path, default parameters']")
    if not len(scoring_notes) == 1:
        stop_err("Exactly one list path, default parameters note is required in the parameter file")
    scoring_notes[0].text = tpp_bin + "/isb_default_input_kscore.xml"

    # Taxonomy and Database
    db_notes = std_params.findall("./note[@type='input'][@label='protein, taxon']")
    if not len(db_notes) == 1:
        stop_err("Exactly one protein, taxon note is required in the parameter file") 
    db_notes[0].text = options.database.lower()

    taxo_notes = std_params.findall("./note[@type='input'][@label='list path, taxonomy information']")
    if not len(taxo_notes) == 1:
        stop_err("Exactly one list path, taxonomy information note is required in the parameter file") 
    taxo_notes[0].text = taxo_path
    
    #spectrum, fragment monoisotopic mass error
    fragment_tol = options.fragment_ion_tol  
    fmass = std_params.findall("./note[@type='input'][@label='spectrum, fragment monoisotopic mass error']")
    if not len(fmass) == 1:
        stop_err("Exactly one spectrum, fragment monoisotopic mass error note is required in the parameter file") 
    fmass[0].text = str(fragment_tol)
  
    ptol_plus = options.precursor_ion_tol * 0.5
    ptol_minus = options.precursor_ion_tol * 0.5
    # Precursor mass matching 
    pmass_minus = std_params.findall("./note[@type='input'][@label='spectrum, parent monoisotopic mass error minus']")
    if not len(pmass_minus) == 1:
        stop_err("Exactly one spectrum, parent monoisotopic mass error minus note is required in the parameter file") 
    pmass_minus[0].text = str(ptol_minus)
    pmass_plus = std_params.findall("./note[@type='input'][@label='spectrum, parent monoisotopic mass error plus']")
    if not len(pmass_plus) == 1:
        stop_err("Exactly one spectrum, parent monoisotopic mass error plus note is required in the parameter file") 
    pmass_plus[0].text = str(ptol_plus)

    pmass_err_units = std_params.findall("./note[@type='input'][@label='spectrum, parent monoisotopic mass error units']")
    if not len(pmass_err_units) == 1:
        stop_err("Exactly one spectrum, parent monoisotopic mass error units note is required in the parameter file. Got") + len(pmass_err_units) 
  
    pmass_err_units[0].text = options.precursor_tolu

    strict_monoisotopic_mass = False;
    if strict_monoisotopic_mass:
        isotopic_error = std_params.findall("./note[@type='input'][@label='spectrum, parent monoisotopic mass isotope error']")
        if not len(isotopic_error) == 1:
            stop_err("Exactly one spectrum, parent monoisotopic mass isotope error is required in the parameter file") 
        isotopic_error[0].text = "no"
   
    # Fixed and Variable Modifications
    carbamidomethyl = True;
    if not carbamidomethyl: 
        mods = std_params.findall("./note[@type='input'][@id='carbamidomethyl-fixed']")
        del mods
    
    glyco = True;
    if not glyco:
        mods = std_params.findall("./note[@type='input'][@id='glyco-variable']")
        del mods 
    
    methionine_oxidation = True;
    if not methionine_oxidation:
        mods = std_params.findall("./note[@type='input'][@id='methionine-oxidation-variable']")
        del mods
                
    #remove all leading and trailing whitespace of each mode in mods, and delete empty ones. 
    var_mods = [ mod.strip() for mod in options.var_mods.split(",") if mod.isspace() ]
    var_mods = [ decode_modification_string(mod)  for mod in var_mods ]
   
    fix_mods = [mod.strip() for mod in options.fix_mods.split(",") if mod.isspace() ]
    fix_mods = [ decode_modification_string(mod)  for mod in fix_mods ]
  
    root_bioml_node = std_params.findall('.')[0]
  
    mod_id = 1
    for mod in var_mods:
        mod_type = "potential modification mass"
        if (re.match('/[\[\]\(\)\{\}\!]/', mod)):
            mod_type = "potential modification motif"      
        mod_id_label = "custom-variable-mod-" + str(mod_id)
        mod_id = mod_id + 1
        mnode = ET.Element('node')
        mnode["id"] = mod_id_label
        mnode["type"] = "input"
        mnode["label"] = "residue, " + mod_type
        mnode.text = mod   
        ET.SubElement(root_bioml_node, mnode)
  
    mod_id = 1
    for mod in fix_mods:
        mod_type = "modification mass"
        if (re.match('/[\[\]\(\)\{\}\!]/', mod)): 
            mod_type = "modification motif"      
        mod_id_label = "custom-fixed-mod-" + str(mod_id)
        mod_id = mod_id + 1
        mnode = ET.Element('node')
        mnode["id"] = mod_id_label
        mnode["type"] = "input"
        mnode["label"] = "residue, " + mod_type
        mnode.text = mod  
        ET.SubElement(root_bioml_node, mnode)

    #p root_bioml_node
    std_params.write(params_path)

def generate_parameter_doc(std_params, output_path, input_path, taxo_path, current_db, options, params_path):  
    # Set the input and output paths 
    input_notes = std_params.findall("./note[@type='input'][@label='spectrum, path']")
    if not len(input_notes) == 1:
        stop_err("Exactly one spectrum, path note is required in the parameter file")
    input_notes[0].text = input_path

    output_notes = std_params.findall("./note[@type='input'][@label='output, path']")
    if not len(output_notes) == 1:
        stop_err("Exactly one output, path note is required in the parameter file") 
    output_notes[0].text = output_path
  
    # Set the path to the scoring algorithm default params. We use one from ISB
    scoring_notes = std_params.findall("./note[@type='input'][@label='list path, default parameters']")
    if not len(scoring_notes) == 1:
        stop_err("Exactly one list path, default parameters note is required in the parameter file")
    scoring_notes[0].text = tpp_bin + "/isb_default_input_kscore.xml"

    # Taxonomy and Database
    db_notes = std_params.findall("./note[@type='input'][@label='protein, taxon']")
    if not len(db_notes) == 1:
        stop_err("Exactly one protein, taxon note is required in the parameter file") 
    db_notes[0].text = options.database.lower()

    taxo_notes = std_params.findall("./note[@type='input'][@label='list path, taxonomy information']")
    if not len(taxo_notes) == 1:
        stop_err("Exactly one list path, taxonomy information note is required in the parameter file") 
    taxo_notes[0].text = taxo_path
    
    #spectrum, fragment monoisotopic mass error
    fragment_tol = options.fragment_ion_tol  
    fmass = std_params.findall("./note[@type='input'][@label='spectrum, fragment monoisotopic mass error']")
    if not len(fmass) == 1:
        stop_err("Exactly one spectrum, fragment monoisotopic mass error note is required in the parameter file") 
    fmass[0].text = str(fragment_tol)
  
    ptol_plus = options.precursor_ion_tol * 0.5
    ptol_minus = options.precursor_ion_tol * 0.5
    # Precursor mass matching 
    pmass_minus = std_params.findall("./note[@type='input'][@label='spectrum, parent monoisotopic mass error minus']")
    if not len(pmass_minus) == 1:
        stop_err("Exactly one spectrum, parent monoisotopic mass error minus note is required in the parameter file") 
    pmass_minus[0].text = str(ptol_minus)
    pmass_plus = std_params.findall("./note[@type='input'][@label='spectrum, parent monoisotopic mass error plus']")
    if not len(pmass_plus) == 1:
        stop_err("Exactly one spectrum, parent monoisotopic mass error plus note is required in the parameter file") 
    pmass_plus[0].text = str(ptol_plus)

    pmass_err_units = std_params.findall("./note[@type='input'][@label='spectrum, parent monoisotopic mass error units']")
    if not len(pmass_err_units) == 1:
        stop_err("Exactly one spectrum, parent monoisotopic mass error units note is required in the parameter file. Got") + len(pmass_err_units) 
  
    pmass_err_units[0].text = options.precursor_tolu

    strict_monoisotopic_mass = False;
    if strict_monoisotopic_mass:
        isotopic_error = std_params.findall("./note[@type='input'][@label='spectrum, parent monoisotopic mass isotope error']")
        if not len(isotopic_error) == 1:
            stop_err("Exactly one spectrum, parent monoisotopic mass isotope error is required in the parameter file") 
        isotopic_error[0].text = "no"
   
    # Fixed and Variable Modifications
    carbamidomethyl = True;
    if not carbamidomethyl: 
        mods = std_params.findall("./note[@type='input'][@id='carbamidomethyl-fixed']")
        del mods
    
    glyco = True;
    if not glyco:
        mods = std_params.findall("./note[@type='input'][@id='glyco-variable']")
        del mods 
    
    methionine_oxidation = True;
    if not methionine_oxidation:
        mods = std_params.findall("./note[@type='input'][@id='methionine-oxidation-variable']")
        del mods
                
    #remove all leading and trailing whitespace of each mode in mods, and delete empty ones. 
    var_mods = [ mod.strip() for mod in options.var_mods.split(",") if mod.isspace() ]
    var_mods = [ decode_modification_string(mod)  for mod in var_mods ]
   
    fix_mods = [mod.strip() for mod in options.fix_mods.split(",") if mod.isspace() ]
    fix_mods = [ decode_modification_string(mod)  for mod in fix_mods ]
  
    root_bioml_node = std_params.findall('.')[0]
  
    mod_id = 1
    for mod in var_mods:
        mod_type = "potential modification mass"
        if (re.match('/[\[\]\(\)\{\}\!]/', mod)):
            mod_type = "potential modification motif"      
        mod_id_label = "custom-variable-mod-" + str(mod_id)
        mod_id = mod_id + 1
        mnode = ET.Element('node')
        mnode["id"] = mod_id_label
        mnode["type"] = "input"
        mnode["label"] = "residue, " + mod_type
        mnode.text = mod   
        ET.SubElement(root_bioml_node, mnode)
  
    mod_id = 1
    for mod in fix_mods:
        mod_type = "modification mass"
        if (re.match('/[\[\]\(\)\{\}\!]/', mod)): 
            mod_type = "modification motif"      
        mod_id_label = "custom-fixed-mod-" + str(mod_id)
        mod_id = mod_id + 1
        mnode = ET.Element('node')
        mnode["id"] = mod_id_label
        mnode["type"] = "input"
        mnode["label"] = "residue, " + mod_type
        mnode.text = mod  
        ET.SubElement(root_bioml_node, mnode)

    #p root_bioml_node
    std_params.write(params_path)



def generate_taxonomy_doc(taxo_doc, current_db, options, taxo_path):

    taxon_label = taxo_doc.findall('./taxon')
    if not len(taxon_label) == 1:
        stop_err("Exactly one taxon label is required in the taxonomy_template file")
    taxon_label[0].set('label', options.database.lower())
    
    db_file = taxo_doc.findall('./taxon/file')
    if not len(db_file) == 1:
        stop_err("Exactly one database file is required in the taxonomy_template file") 
    db_file[0].set('URL', current_db)

    taxo_doc.write(taxo_path);
    
def replace_outpath(output_pre):
    if output_pre.find('job_working_directory') != -1:
        output_post = output_pre.replace('job_working_directory', 'files')
        output_post = output_post.replace('galaxy_dataset', 'dataset')
        #re.sub(pattern, repl, string, count=0, flags=0)
        #Return the string obtained by replacing the leftmost non-overlapping occurrences of pattern in string by the replacement repl
        pattern = r'(\/\d+)(\/\d+)'
        output_post = re.sub(pattern, '\g<1>', output_post)
    else:
        output_post = output_pre
    return output_post

def runTool(cmd):     
        #
        # Run command and handle output.
        #
        #tmp_name = tempfile.NamedTemporaryFile( dir="." ).name
        try:                              
            tmp_name = tempfile.NamedTemporaryFile(dir=".").name
            tmp_stderr = open(tmp_name, 'wb')
            proc = subprocess.Popen(args=cmd, shell=True, stderr=tmp_stderr.fileno())
            returncode = proc.wait()
            tmp_stderr.close()
        
            # Error checking.
            if returncode != 0:
                raise Exception, "return code = %i" % returncode
            #else:
                #seachType = 'tandem'
                #inputfile,searchType,resultfilepath
                #print options.input,seachType,options.output
                #storeDBSearchResult(options.input, seachType, options.output, options.dbop_type)
                #print options.output,options.database,options.var_mods,options.fix_mods,options.enzyme,options.precursor_tolu,options.missed_cleavages,options.fragment_ion_tol,options.precursor_ion_tol,params_path,taxo_path
                #storeXtandemParam(options.output, options.database, options.var_mods, options.fix_mods, options.enzyme, options.precursor_tolu, options.missed_cleavages, options.fragment_ion_tol, options.precursor_ion_tol, params_path, taxo_path, options.dbop_type)
                #too slow to store database information each time, since each fasta file may have tens of thousands of records, 
                #eg.33778 records for /usr/local/tpp/data/dbase/refSeqhuman20120320.fasta
                #one solution is to check whether this database has been stored, if yes, skip
                #the other solution is to store fasta info in advance
                #protSeqIDMap=session.query(ProteinSeqIDMap).filter(and_(ProteinSeqIDMap.dbname==options.database))
                #print options.database,options.dbtype
                #storefastaInfo(options.database,options.dbtype) 
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
        
             stop_err('Error running tandem.\n%s\n' % (str(e)))      
                         
def __main__():
    #Parse Command Line
    parser = optparse.OptionParser()
    parser.add_option('-i', '', dest='input', help=' ')
    parser.add_option('-d', '', dest='database', help=' ')
    parser.add_option('', '--dbtype', dest='dbtype', help=' ')
    parser.add_option('', '--var-mods', dest='var_mods', help='')
    parser.add_option('', '--fix-mods', dest='fix_mods', help='')
    parser.add_option('-o', '', dest='output', help='')
    parser.add_option('', '--enzyme', dest='enzyme', help='')
    parser.add_option('', '--precursor-ion-tol-units', dest='precursor_tolu', help='')
    parser.add_option('-v', '', dest='missed_cleavages', type="int", help='')
    parser.add_option('-f', '', dest='fragment_ion_tol', type="float", help='')
    parser.add_option('-p', '', dest='precursor_ion_tol', type="float", help='')
    parser.add_option('-K', '--keep-params-files', dest='keep_params_files', action='store_true', default=True, help='Keep X!Tandem parameter files')
    parser.add_option('-P', '--no-pepxml', dest='no_pepxml', action='store_true', default=True, help='Dont convert to pepXML after running the search') 
    parser.add_option('-a', '--allow_multi_isotope_search', action='store_false', dest='multi_isotope_searchl', default=False, help='allow multi_isotope_search')
    parser.add_option('', '--inparamfile', dest='tandem_params', help='XTandem parameters to use')
    parser.add_option('', '--intaxonfile', dest='intaxonfile', help='XTandem taxonomy file to use')
    parser.add_option('', '--outparamfile', dest='outparamfile', help='XTandem parameters used')
    parser.add_option('', '--outtaxonfile', dest='outtaxonfile', help='XTandem taxonomy file used')
    parser.add_option('', '--dbop_type', dest='dbop_type', action='store', help='')
    (options, args) = parser.parse_args()    
    
    infile = os.path.basename(options.input)
    infilepath = os.path.dirname(options.input)
    paramfilepath = ConfigSectionMap("Tandem")['paramfilepath']
    # Parse options from a parameter file (if provided), or from the default parameter file
    tandem_defaults = paramfilepath + "tandem_params.xml"
    """
    #users can select current parameter files
    if options.tandem_params:
        tandem_params=options.tandem_params
    else:
        tandem_params=tandem_defaults
    """
    tandem_params = tandem_defaults
    #Parses an XML section into an element tree
    std_params = ET.parse(tandem_params)

    # Parse taxonomy template file
    taxo_doc = ET.parse(paramfilepath + "taxonomy_template.xml")   
    
    # Run the search engine on each input file
    
    outbase = os.path.splitext(infile)[0]    
    #output_path=outbase+".tandem"
    output_path = options.output
    
    explicit_output = False;
    if not explicit_output:
        pepxml_path = infilepath + '/' + outbase + ".pep.xml"
    else:
        pepxml_path = explicit_output
  
    output_exists = False
    if  not options.no_pepxml and os.path.exists(pepxml_path):
        output_exists = True
    
    #query SearchdbResult, if resultfilepath is not null
    if  options.no_pepxml and os.path.exists(output_path):
        output_exists = True
        
    current_db = options.database
    
    over_write = True;
    # Only proceed if the output file is not present or we have opted to over-write it
    if (over_write or not output_exists):
        # Create the taxonomy file in the same directory as the params file
        #taxo_path=outbase+".taxonomy.xml"
        taxo_path = replace_outpath(options.outtaxonfile)
        #print options.outtaxonfile
        #print taxo_path
        mod_taxo_doc = generate_taxonomy_doc(taxo_doc, current_db, options, taxo_path)

        # Modify the default XML document to contain search specific details and save it so it can be used in the search  
       # params_path=outbase+".tandem.params"
        params_path = replace_outpath(options.outparamfile)
        mod_params = generate_parameter_doc(std_params, output_path, options.input, taxo_path, current_db, options, params_path)       
        
        cmd = "tandem " + params_path
        #in case that files cannot be written in the job working directory
        #cmd+= "; wait; cp " + params_path + " "+options.outtaxonfile
        #cmd+= "; wait; cp " + taxo_path + " "+options.outparamfile 
       
        # pepXML conversion and repair
        if not options.no_pepxml:                  
            #cmd += "; Tandem2XML "+output_path +" " +pepxml_path+"; "+repair_script+pepxml_path+"; rm "+output_path
            stop_err('Skipping pepXML conversion and repair')
                 
        # Add a cleanup command if not the user wants to keep params files
        if not options.keep_params_files: 
            cmd += "; rm " + params_path + "; rm " + taxo_path
        
        print cmd   
        
        searchType = 'tandem'
          
        (status, convertedRawfileID) = checkDatabase(options.input, searchType, options.output, options.dbop_type)
        if status:     
            returncode = runTool(cmd)
            if returncode == 0:
                storeDBSearchResult(convertedRawfileID, searchType, options.output, options, params_path, taxo_path)    
                #storeMascotParam(options.output, options.database, var_mods, fix_mods, options.enzyme, options.precursor_tolu, options.missed_cleavages, options.fragment_ion_tol, options.allowed_charges, options.instrument, options.precursor_search_type, options.dbop_type)
    else:
        stop_err('Skipping search on existing file %s' % output_path)  
   
if __name__ == "__main__": __main__()
