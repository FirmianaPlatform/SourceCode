#!/usr/bin/env python
import optparse, os, shutil, subprocess, sys, tempfile, urllib2, urllib, re, base64
import httplib, mimetypes, mimetools, cookielib
from poster.encode import multipart_encode, MultipartParam
from poster.streaminghttp import register_openers, StreamingHTTPHandler, StreamingHTTPRedirectHandler, StreamingHTTPSHandler
#from binascii import b2a_base64
from HTMLParser import HTMLParser
from bs4 import BeautifulSoup
sys.path.insert(1,"/usr/local/firmiana/galaxy-dist/tools/ms_tools/")
#from models.firmiana_models import *
from config.firmianaConfig import *
from models.gardener_control import *

def get_database(conn,meta,eid):
    
    res = get_species(conn,meta,eid)
    
    if res.find('Homo')!=-1:
        s='Human_refseq'
    elif res.find('Mouse')!=-1 or res.find('Mus musculus')!=-1 or res.find('Rattus')!=-1:
        s='Mouse_refseq'
    elif res.find('Arabidopsis')!=-1:
        s='Arabidopsis_lipeng'
        #s='Arabidopsis_refseq'
        #s='Arabidopsis_uniprot' 
    elif res.find('Pig')!=-1:
        #s='Pig_refseq'
        s='PIG_ensembl'
    else:
        return 0  
    return s

def get_search_param(conn, meta, e_name,postdict):
    def getEnzyme(conn, meta, id):
        e = Table('experiments_digest_enzyme', meta, autoload = True, autoload_with = engine)
        s = select([e.c.name]).where(e.c.id == id)
        res = conn.execute(s).scalar()
        if res == None:res = 0
        return res
    def getInstru(conn, meta, id):
        e = Table('experiments_instrument', meta, autoload = True, autoload_with = engine)
        s = select([e.c.name]).where(e.c.id == id)
        res = conn.execute(s).scalar()
        if res.find('trap')!=-1 or res.find('Velos')!=-1:
            tmp = 'ESI-TRAP'
        else:
            tmp = 'ESI-QUAD-TOF'
        return tmp
    def getTOL(conn, meta, id):
        e = Table('experiments_instrument_ms1_tol', meta, autoload = True, autoload_with = engine)
        s = select([e.c.name]).where(e.c.id == id)
        res = conn.execute(s).scalar()
        if res == None:res = '0 0'
        return res
    def getITOL(conn, meta, id):
        e = Table('experiments_instrument_ms2_tol', meta, autoload = True, autoload_with = engine)
        s = select([e.c.name]).where(e.c.id == id)
        res = conn.execute(s).scalar()
        if res == None:res = 0
        return res
    def getFixMods(conn, meta, eeid):
        tmp = ''
        A = Table('experiments_experiment_fixed_modifications', meta, autoload = True, autoload_with = engine)
        B = Table('experiments_fixed_modification', meta, autoload = True, autoload_with = engine)
        s = select([B.c.name]).select_from(A.join(B, B.c.id == A.c.fixed_modification_id)).where(A.c.experiment_id == eeid)
        res = conn.execute(s)
        if res == None:return 0
        for row in res:
            tmp = tmp + row['name'] +',' 
        if tmp == '':tmp = 0 
        return tmp
    def getVarMods(conn, meta, eeid):
        tmp = ''
        A = Table('experiments_experiment_dynamic_modifications', meta, autoload = True, autoload_with = engine)
        B = Table('experiments_dynamic_modification', meta, autoload = True, autoload_with = engine)
        s = select([B.c.name]).select_from(A.join(B, B.c.id == A.c.dynamic_modification_id)).where(A.c.experiment_id == eeid)
        res = conn.execute(s)
        if res == None:return 0
        for row in res:
            tmp = tmp + row['name'] +',' 
        if tmp == '':tmp = 0 
        return tmp
    
    d_param = {}
    e = Table('experiments_experiment', meta, autoload = True, autoload_with = engine)
    s = select([e]).where(e.c.name == e_name)
    res = conn.execute(s).fetchone()
    eeid = res['id']
    enzyme_id = res['digest_enzyme_id']
    instru_id = res['instrument_name_id']
    ms1_param_id = res['ms1_details_id']
    ms2_param_id = res['ms2_details_id']
    
    enzyme = getEnzyme(conn, meta, enzyme_id)
    instru = getInstru(conn, meta, instru_id)
    tol = getTOL(conn, meta, ms1_param_id)
    itol = getITOL(conn, meta, ms2_param_id)
    fix_mods = getFixMods(conn, meta, eeid)
    var_mods = getVarMods(conn, meta, eeid)
    print 'enzyme:',enzyme
    print 'instru:',instru,
    print 'tol:',tol,
    print 'itol:',itol,
    print 'fix_mods:',fix_mods
    print 'var_mods:',var_mods
    
    postdict['CLE'] = enzyme
    postdict['ITOL'] = itol.split(' ')[0]
    postdict['ITOLU'] = itol.split(' ')[1]
    postdict['TOL'] = tol.split(' ')[0]
    postdict['TOLU'] = tol.split(' ')[1]
    postdict['INSTRUMENT'] = instru
    postdict['IT_MODS'] = var_mods
    postdict['MODS'] = fix_mods

def get_param(postdict):
    enum = '000038'
    e_name = 'Exp%s'%enum
    eid = get_exp_id(conn, meta, e_name)
    db = get_database(conn,meta,34)
    print db
    postdict['DB'] = db
        
    get_search_param(conn,meta,e_name,postdict)
    
    
    par = []
    for p in postdict:
        t = p +'=' + str(postdict[p])
        par.append(t)
    pars = ','.join(par)
    print pars
    
    return postdict

postdict = {}
postdict['DECOY'] = 1    # CHARGE
postdict['CHARGE'] = 2    # CLE
postdict['CLE'] =   3  # PFA
postdict['PFA'] =  4   # DB (Database)
postdict['DB'] =  5   # INSTRUMENT
postdict['INSTRUMENT'] = 6    # IT_MODS (Variable Modifications)
postdict['IT_MODS'] = 7    # ITOL (Fragment ion tolerance)
postdict['ITOL'] =  8   # ITOLU (Fragment ion tolerance units)
postdict['ITOLU'] = 9   # MASS (Monoisotopic and Average)
postdict['MASS'] =  10  # MODS (Fixed modifications)
postdict['MODS'] =  11  # TOL (Precursor ion tolerance (Unit dependent))
postdict['TOL'] =  12  # TOLU (Tolerance Units)
postdict['TOLU'] = 13 # Email
postdict['USEREMAIL'] = 14# Username
postdict['USERNAME'] = 15 # COM (Search title)
postdict['COM'] = "Test_qiunq" # REPORT (What to include in the search report.   #For command-line searches this is pretty much irrelevant because we retrieve the entire results file anyway)
postdict['REPORT'] = "AUTO"   # TAXONOMY (Blank because we don't allow taxonomy)
postdict['TAXONOMY'] = "All entries"
postdict['FORMAT'] = "Mascot generic"   
postdict['FORMVER'] = '1.01'
postdict['INTERMEDIATE'] = ''
postdict['SEARCH'] = 'MIS'

get_param(postdict)