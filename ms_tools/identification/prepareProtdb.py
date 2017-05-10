#!/usr/bin/env python

import optparse, os, shutil, subprocess, sys, tempfile, re 
sys.path.append("/usr/local/firmiana/galaxy-dist/tools/ms_tools/")
from models.firmiana_models import *

session = Session()

def stop_err( msg ):
    sys.stderr.write( "%s\n" % msg )
    sys.exit()
    
def storefastaInfo(fafile,dbtype):
    try:
        for values in SimpleFastaParser(open(fafile,'r')):
            (names,sequence)=values
            id_desc=names.split(' ', 1)
            #print sequence
            #print id_desc
            name=id_desc[0]
            desc=id_desc[1]
            #print id
            #print desc 
            #if this sequence does not exist in the database 
            if not session.query(ProteinSequence).filter(ProteinSequence.sequence==sequence).first():          
                protSeq=ProteinSequence(sequence)
                #print protSeq
                session.add(protSeq)                    
                protSeqInfo=ProteinSeqInfo(name,desc)
                #print protSeqInfo
                session.add(protSeqInfo)                    
                session.commit()
                    
                protSeq=session.query(ProteinSequence).filter(ProteinSequence.sequence==sequence).first()              
                sequenceID=protSeq.id  
                #print  sequenceID
                protSeqInfo=session.query(ProteinSeqInfo).filter(and_(ProteinSeqInfo.name==name,ProteinSeqInfo.description==desc)).first()   
                proteinSeqInfoID=protSeqInfo.id 
                #print  proteinSeqInfoID       
                dbversion=dbtype  
                dbname=fafile              
                protSeqIDMap=ProteinSeqIDMap(sequenceID,dbtype,dbversion,dbname,proteinSeqInfoID)
                #print protSeqIDMap
                session.add(protSeqIDMap)               
            else:
                #the same sequence has different name and desc
                for instance in session.query(ProteinSequence).filter(ProteinSequence.sequence==sequence):
                    sequenceID=instance.id
                    #print sequenceID
                    #find if the detailed info of this sequence exist, or the info may be added or updated
                    if not session.query(ProteinSeqInfo).filter(and_(ProteinSeqInfo.name==name,ProteinSeqInfo.description==desc)).first():
                            protSeqInfo=ProteinSeqInfo(name,desc)
                            #print protSeqInfo
                            session.add(protSeqInfo)
                            session.commit()
                            
                            protSeqInfo=session.query(ProteinSeqInfo).filter(and_(ProteinSeqInfo.name==name,ProteinSeqInfo.description==desc)).first()   
                            proteinSeqInfoID=protSeqInfo.id          
                            dbversion=dbtype  
                            dbname=fafile              
                            protSeqIDMap=ProteinSeqIDMap(sequenceID,dbtype,dbversion,dbname,proteinSeqInfoID)
                            #print protSeqIDMap
                            session.add(protSeqIDMap) 
                    else:
                        #if the desciption of this sequence is not updated
                        for protSeqInfo in session.query(ProteinSeqInfo).filter(and_(ProteinSeqInfo.name==name,ProteinSeqInfo.description==desc)):
                            proteinSeqInfoID=protSeqInfo.id
                            if not session.query(ProteinSeqIDMap).filter(and_(ProteinSeqIDMap.sequenceID==sequenceID,ProteinSeqIDMap.proteinSeqInfoID==proteinSeqInfoID,ProteinSeqIDMap.dbtype==dbtype)).first():        
                                dbversion=dbtype  
                                dbname=fafile              
                                protSeqIDMap=ProteinSeqIDMap(sequenceID,dbtype,dbversion,dbname,proteinSeqInfoID)
                                #print protSeqIDMap
                                session.add(protSeqIDMap) 
            session.commit()  
    except Exception, e:
         stop_err( 'Error adding records in ProteinSequence, ProteinSeqInfo,ProteinSeqIDMap.\n%s\n' % ( str( e ) ) ) 
          
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

               
def __main__():
    #database='/usr/local/tpp/data/dbase/refSeqhuman20120320.fasta'
    database='/opt/galaxy-dist/database/sequence/refSeqhuman20120320/refSeqhuman20120320_Decoy.fasta'
    dbtype='RefSeq'
    storefastaInfo(database,dbtype)
    """  
    database='/opt/galaxy-dist/database/sequence/SwissProt/SwissProt_51.6.fasta'
    dbtype='SwissProt'
    storefastaInfo(database,dbtype) 
    """


if __name__=="__main__": __main__()
