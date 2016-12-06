import sys, os, re, time

from sqlalchemy import *
from sqlalchemy.sql import select

''' For reading DB, like metadata and something about django '''

engine_name = 'postgresql'
host = '192.168.99.201'
port = '6032'
database = 'galaxy'
dbuser = 'phoenix'
password = 'firmianaadmin'
conn_str = "%s://%s:%s@%s:%s/%s" % (engine_name, dbuser, password, host, port , database)
engine = create_engine(conn_str)
conn = engine.connect()
meta = MetaData()

import datetime 
def time_now():
    return datetime.datetime.now().strftime('%X') 

def get_pro_mass(conn, meta, acc, dict_aa_mass, prefix):
    mass = 0.0
    pro_seq = ''
    fas = Table('gardener_fasta_data', meta, autoload=True, autoload_with=engine)
    if prefix == 'none':
        #tmp = '%' + '|' + acc
        #s = select([fas.c.sequence]).where(fas.c.accession.like(tmp))
        s = select([fas.c.sequence]).where(fas.c.accession == acc)
    else:
        if prefix == 'gi':
            s = select([fas.c.sequence]).where(fas.c.protein_gi == acc)
        else:
            tmp = acc
            s = select([fas.c.sequence]).where(fas.c.accession == tmp)
            #tmp = acc + '%'
            #s = select([fas.c.length]).where(and_(fas.c.accession.like(tmp), fas.c.prefix == prefix))
    seq = conn.execution_options(autocommit=True).execute(s).scalar()
    if not seq:
        return (0.0, '')
    
    for i in list(seq):
        mass += dict_aa_mass[i]
        
    return (mass, seq)

def getGeneID(conn, meta, acc_short, prefix, taxid):
    gid = -1
    g = Table('gardener_gene2accession', meta, autoload=True, autoload_with=engine)
    if prefix == 'gi':
        if taxid != -1:
            s = select([g.c.geneid]).where(and_(g.c.protein_gi == acc_short, g.c.tax_id==taxid))
        else:
            s = select([g.c.geneid]).where(g.c.protein_gi == acc_short)
    else: 
        return gid 
        tmp = acc_short + '.'+'%'
        s = select([g.c.geneid]).where(and_(g.c.protein_accession.like(tmp), g.c.tax_id == taxid))
    res = conn.execution_options(autocommit=True).execute(s).scalar()
    if res != None:
        gid = res
    return gid


def getPigGID(conn, meta, acc_short, prefix):
    gid = -1
    g = Table('gardener_fasta_data', meta, autoload=True, autoload_with=engine)
    #tmp = prefix + '|' + acc_short
    if prefix == 'none':
    #    tmp = '%' + '|' + acc_short
        s = select([g.c.symbol]).where(and_(g.c.accession == acc_short, g.c.fasta_file_id == 7))
    else:
        tmp = acc_short
        s = select([g.c.length]).where(and_(g.c.accession == tmp, g.c.prefix == prefix, g.c.fasta_file_id == 7))
    
    sym = conn.execution_options(autocommit=True).execute(s).scalar()
    if sym == None:
        return gid
    g2 = Table('gardener_geneinfo', meta, autoload=True, autoload_with=engine)
    s = select([g2.c.gene_id]).where(and_(g2.c.symbol == sym, g2.c.tax_id == '9823'))
    res = conn.execution_options(autocommit=True).execute(s).scalar()
    if res != None:
        gid = res
    else:
        pass
        #print 'Acc: %s Sym: %s not in gardener_geneinfo' %(acc_short, sym)
    return gid


def getGeneDescSymbol(conn, meta, gid):
    sym = '-'
    des = '-'
    g = Table('gardener_geneinfo', meta, autoload=True, autoload_with=engine)
    s = select([g.c.symbol, g.c.description]).where(g.c.gene_id == gid)
    res = conn.execution_options(autocommit=True).execute(s)
    row = res.fetchone()
    if row != None:
        sym = row[g.c.symbol]
        des = row[g.c.description]
    return sym, des

def get_desc_pro(conn, meta, acc, prefix):
    fas = Table('gardener_fasta_data', meta, autoload=True, autoload_with=engine)
    if prefix == 'gi':
        s = select([fas.c.description]).where(fas.c.protein_gi == acc)
    else:
        s = select([fas.c.description]).where(fas.c.accession == acc)
    desc = conn.execution_options(autocommit=True).execute(s).scalar()
    if desc == None:
        return ''
    return desc


def get_pro_len_Simple(conn, meta, accession):
    if '|' in accession:
        acc = accession.split('|')[1]
        prefix = accession.split('|')[0]
    else :
        acc = accession
        prefix = 'none'
    fas = Table('gardener_fasta_data', meta, autoload=True, autoload_with=engine)
    if prefix == 'none':
        #tmp = '%' + '|' + acc
        #s = select([fas.c.length]).where(fas.c.accession.like(tmp))
        s = select([fas.c.length]).where(fas.c.accession == acc)
    else:
        if prefix == 'gi':
            s = select([fas.c.length]).where(fas.c.protein_gi == acc)
        else:
            tmp = acc
            s = select([fas.c.length]).where(fas.c.accession == tmp)
    
    ll = conn.execution_options(autocommit=True).execute(s).scalar()
    
    return 0 if ll == None else ll


def get_species(conn, meta, eid):
    exp = Table('gardener_experiment', meta, autoload=True, autoload_with=engine)
    s = select([exp.c.species]).where(exp.c.id == eid)
    spe = conn.execution_options(autocommit=True).execute(s).scalar()
    return spe

def get_taxid(conn, meta, eid):
    exp = Table('gardener_experiment', meta, autoload=True, autoload_with=engine)
    s = select([exp.c.taxid]).where(exp.c.id == eid)
    txid = conn.execution_options(autocommit=True).execute(s).scalar()
    if txid == '':
        return -1
    return txid
