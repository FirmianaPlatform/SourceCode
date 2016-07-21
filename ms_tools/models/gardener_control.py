import sys, os, re, time
from lxml import etree as ET

mstool_path = os.path.join( os.path.dirname( __file__ ), '..')
sys.path.insert(1, mstool_path)

from config.firmianaConfig import *
from sqlalchemy import *
from sqlalchemy.sql import select

''' For reading DB, like metadata and something about django '''
engine_name = ConfigSectionMap("Database_Django")['engine']
host = ConfigSectionMap("Database_Django")['host']
port = ConfigSectionMap("Database_Django")['port']
database = ConfigSectionMap("Database_Django")['database']
dbuser = ConfigSectionMap("Database_Django")['user']
password = ConfigSectionMap("Database_Django")['password']
store_file_path = ConfigSectionMap("Database")['store_file_path']
conn_str = "%s://%s:%s@%s:%s/%s" % (engine_name, dbuser, password, host, port , database)
engine = create_engine(conn_str)
conn = engine.connect()
meta = MetaData()

import datetime 
def time_now():
    return datetime.datetime.now().strftime('%X') 

def date_now():
    return datetime.datetime.now().strftime('%Y-%m-%d %X')

         
def getRepFra(conn,meta,e_name):
    e = Table('gardener_experiment',meta, autoload=True, autoload_with=engine)
    s = select([e.c.num_repeat,e.c.num_fraction]).where(e.c.name == e_name)
    #res = conn.execute(s)
    res = conn.execution_options(autocommit=True).execute(s).fetchone()
    fra = res[1]
    rep = res[0]
    
    return (rep, fra)

  
def getJobId(cwd):
    x = re.search(r'\/(\d+)\/(\d+)', cwd)
    if x:
        job_id = x.group(2)
    else:
        job_id = -1
    
    return job_id
    
         
def get_exp_info(lable):
    exp = {}
    #m = re.search(r'\(([^\(\)\.]*)\.[^\(\)\.]*\)', lable)  
    m = re.search(r'\(([^\(\)\.]*)\.[^\(\)]*\)', lable)   
    n = re.search(r'\_E(\d+)\_F(\d+)\_R(\d+)', lable)
    if m and n:
        exp['name'] = m.group(1)  #name of raw file!!!!!
        exp['exp_id'] = n.group(1)  #ID like 80574!!!!!!!!!!
        exp['nf'] = n.group(2)
        exp['nr'] = n.group(3)
        exp['state'] = 1
    else:
        exp['state'] = -1
    return exp 

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

def get_pro_len(conn, meta, acc, prefix):
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
    seq = seq.upper()
    for i in seq:
        try:
            mass += dict_aa_mass[i]
        except:
            continue
        
    return (mass, seq)

def get_file_num(conn, meta, exp_db_id):
    exp = Table('gardener_experiment', meta, autoload=True, autoload_with=engine)
    s = select([exp.c.num_fraction, exp.c.num_repeat]).where(exp.c.id == exp_db_id)
    res = conn.execution_options(autocommit=True).execute(s)
    for row in res:
        f_num = row[exp.c.num_fraction]
        r_num = row[exp.c.num_repeat]
    file_num = f_num * r_num
    print 'get_file_num():file_num=', file_num
    # user_name= user_name if ('user_name' in dir()) else 'Unknown'  
    return f_num, r_num

def getUserID(conn,meta,e_name):
    u = Table('experiments_experiment',meta, autoload=True, autoload_with=engine)
    s = select([u.c.experimenter_id]).where(u.c.name == e_name)
    user_id = conn.execution_options(autocommit=True).execute(s).scalar()
    return user_id

def getEmail(conn,meta,user_id):
    u = Table('galaxy_user',meta, autoload=True, autoload_with=engine)
    s = select([u.c.email]).where(u.c.id==user_id)
    email = conn.execution_options(autocommit=True).execute(s).scalar()
    #print 'Email:',email
    return email

def get_user_name(conn, meta, user_id):
    user = Table('galaxy_user', meta, autoload=True, autoload_with=engine)
    s = select([user.c.username]).where(user.c.id == user_id)
    user_name = conn.execution_options(autocommit=True).execute(s).scalar()  
    return user_name 

def get_exp_id(conn, meta, exp_name):
    t = Table('gardener_experiment', meta, autoload=True, autoload_with=engine)
    s = select([t.c.id]).where(t.c.name == exp_name)
    id = conn.execution_options(autocommit=True).execute(s).scalar()
    return id
"""
def get_scanNum_ms1(conn,meta,scanNum,file_name):
    scan=Table('gardener_ms1_ms2', meta, autoload=True, autoload_with=engine)
    s = select([scan.c.ms1]).where(and_(scan.c.ms2==scanNum,scan.c.file_name==file_name))
    result = conn.execution_options(autocommit=True).execute(s).scalar()
    #row=result.fetchone()
    scanNum_ms1=result#row['ms1'] 
    return scanNum_ms1
"""
def get_ms1_id(conn, meta, scanNum, search_id):
    scan = Table('gardener_ms1', meta, autoload=True, autoload_with=engine)
    s = select([scan.c.id]).where(and_(scan.c.scan_num == scanNum, scan.c.search_id == search_id))
    ms1_id = conn.execution_options(autocommit=True).execute(s).scalar()
    # row=result.fetchone()
    # ms1_id = row['id']   
    return ms1_id

def get_ms2_id(conn, meta, scanNum_ms2, search_id):
    # scan1=Table('gardener_ms1', meta, autoload=True, autoload_with=engine)
    scan2 = Table('gardener_ms2', meta, autoload=True, autoload_with=engine)
    # s = select([scan2.c.id]).where(and_(scan1.c.search_id==search_id,scan2.c.ms1_id==ms1_id)).select_from(scan2.outerjoin(scan1))
    s = select([scan2.c.id]).where(and_(scan2.c.scan_num == scanNum_ms2, scan2.c.search_id == search_id))
    ms2_id = conn.execution_options(autocommit=True).execute(s).scalar() 
    return ms2_id

def get_search_id(conn, meta, file_data):
    t = Table('gardener_search', meta, autoload=True, autoload_with=engine)
    s = select([t.c.id]).where(and_(t.c.exp_id == file_data['exp_db_id'],
                                    t.c.fraction_id == file_data['f_num'],
                                    t.c.repeat_id == file_data['r_num'],
                                    #t.c.user == file_data['user'],
                                    t.c.rank == file_data['rank'],
                                    t.c.type == 'fraction'))
    sid = conn.execution_options(autocommit=True).execute(s).scalar()   
    return sid

def get_cache_exp_sid(conn, meta, file_data):
    t = Table('gardener_search', meta, autoload=True, autoload_with=engine)
    s = select([t.c.id]).where(and_(t.c.exp_id == file_data['exp_db_id'],
                                       #t.c.user == file_data['user'],
                                       t.c.type == 'exp'))
    sid = conn.execution_options(autocommit=True).execute(s).scalar()   
    return sid

def get_cache_rep_sid(conn, meta, file_data):
    t = Table('gardener_search', meta, autoload=True, autoload_with=engine)
    s = select([t.c.id]).where(and_(t.c.exp_id == file_data['exp_db_id'],
                                    t.c.repeat_id == file_data['r_num'],
                                    t.c.rank == file_data['rank'],
                                    #t.c.user == file_data['user'],
                                    t.c.type == 'rep'))
    sid = conn.execution_options(autocommit=True).execute(s).scalar()   
    return sid

def insert_COPY(table_name, data_list):
    pass
    
def insertGeneral(table_name, data_list):
    t1 = datetime.datetime.now()
    print '#insert %s start :'%table_name,time_now()
    ll = len(data_list)
    step = 1000000
    m = ll / step
    if ll <= step:
        t = Table(table_name, meta, autoload=True, autoload_with=engine)
        conn.execution_options(autocommit=True).execute(t.insert(), data_list)
        print 'insertGeneral end (list len=%s) :'%ll,time_now()
        return
    for i in range(m):
        st = step*i
        ed = step*(i+1)
        tmp = data_list[st:ed]
        t = Table(table_name, meta, autoload=True, autoload_with=engine)
        conn.execution_options(autocommit=True).execute(t.insert(), tmp)
    tmp = data_list[ed:]
    #t = Table(table_name, meta, autoload=True, autoload_with=engine)
    if tmp:
        conn.execution_options(autocommit=True).execute(t.insert(), tmp)
    #print 'Inserted %s\n' %table_name
    t2 = datetime.datetime.now()
    print '#insertGeneral end :',time_now()
    print 'used:',t2-t1
    
    
def insert_cache_exp(conn, meta, file_data):
    t = Table('gardener_search', meta, autoload=True, autoload_with=engine)
    ins = t.insert()
    result = conn.execution_options(autocommit=True).execute(
                          ins,
                          repeat_id=0, fraction_id=0, rank=0, type='exp',
                          name=file_data['name'], exp_id=file_data['exp_db_id'],
                          num_spectrum=0, num_peptide=0, num_isoform=0, num_gene=0,
                          user=file_data['user'], stage=1, rt_max=0, log='Summary of Experiment Level.',
                          update_time=date_now(), create_time=date_now(),
                          parameter='unknown'
                          )
    return result

def insert_cache_rep(conn, meta, file_data):
    t = Table('gardener_search', meta, autoload=True, autoload_with=engine)
    ins = t.insert()
    result = conn.execution_options(autocommit=True).execute(
                          ins,
                          repeat_id=file_data['r_num'], fraction_id=0, rank=file_data['rank'], type='rep',
                          name=file_data['name'], exp_id=file_data['exp_db_id'],
                          num_spectrum=0, num_peptide=0, num_isoform=0, num_gene=0,
                          user=file_data['user'], stage=1, rt_max=0, log='Summary of Repeat Level.',
                          update_time=date_now(), create_time=date_now(),
                          parameter='unknown'
                          )
    return result

def update_cache_info(conn, meta, file_data, sid):
    search = Table('gardener_search', meta, autoload=True, autoload_with=engine)
    upd = search.update().where(search.c.id == sid).values({search.c.num_spectrum:file_data['num_spec'],
                                                          search.c.num_peptide:file_data['num_pep'],
                                                          search.c.num_isoform:file_data['num_pro'],
                                                          search.c.num_gene:file_data['num_gen'],
                                                          search.c.update_time:date_now(),
                                                          search.c.stage:file_data['stage']})
    result = conn.execution_options(autocommit=True).execute(upd)
    return result

def updateExpTable(conn, meta, file_data):
    exp = Table('gardener_experiment', meta, autoload=True, autoload_with=engine)
    upd = exp.update().where(exp.c.id == file_data['exp_db_id']).values({exp.c.num_spectrum:file_data['num_spec'],
                                                          exp.c.num_peptide:file_data['num_pep'],
                                                          exp.c.num_isoform:file_data['num_pro'],
                                                          exp.c.num_gene:file_data['num_gen'],
                                                          exp.c.update_date:date_now()})
    result = conn.execution_options(autocommit=True).execute(upd)
    return result

def update_rep_stage(conn, meta, file_data, sid):
    x = Table('gardener_search', meta, autoload=True, autoload_with=engine)
    s1 = select([func.min(x.c.stage)]).where(and_(x.c.exp_id == file_data['exp_db_id'],
                                                  x.c.rank == file_data['rank'],
                                                  x.c.repeat_id == file_data['r_num'],
                                                  x.c.type == 'fraction'))
    stage_min = conn.execution_options(autocommit=True).execute(s1).scalar()

    upd = x.update().where(x.c.id == sid).values({x.c.stage:stage_min,
                                                x.c.update_time:date_now()})
    result = conn.execution_options(autocommit=True).execute(upd)
    
def get_rank(conn, meta, file_data):
    scan = Table('gardener_search', meta, autoload=True, autoload_with=engine)
    s = select([func.max(scan.c.rank)]).where(and_(scan.c.name == file_data['name'],
                                                   scan.c.user == file_data['user'],
                                                   scan.c.type == 'fraction'))
    rank = conn.execution_options(autocommit=True).execute(s).scalar()   
    return rank

def get_protein_id(conn, meta, acc, search_id):
    pp = Table('gardener_protein', meta, autoload=True, autoload_with=engine)
    s = select([pp.c.id]).where(and_(pp.c.accession == acc, pp.c.search_id == search_id, pp.c.type == 1))
    result = conn.execution_options(autocommit=True).execute(s).scalar()
    # for row in result:
    #    protein_id = row['id']
    # protein_id=protein_id if ('protein_id' in dir()) else -1
    if result != None:
        return result
    else:
        return -1

def get_xenos_gene_from_db(acc_short,fileID):
    g = Table('gardener_fasta_data', meta, autoload=True, autoload_with=engine)
    
    s = select([g.c.symbol,g.c.description]).where(and_(g.c.protein_gi == acc_short, g.c.fasta_file_id == fileID))
    result = conn.execution_options(autocommit=True).execute(s).fetchone()
    
    if result:
        sym = result[g.c.symbol]
        des = result[g.c.description]
        return sym,des
    else:
        return '',''
    
def get_yeast_gene_from_db(acc_short):
    g = Table('gardener_fasta_data', meta, autoload=True, autoload_with=engine)
    fasta_file_id = 9
    s = select([g.c.symbol,g.c.description]).where(and_(g.c.accession == acc_short, g.c.fasta_file_id == fasta_file_id))
    result = conn.execution_options(autocommit=True).execute(s).fetchone()
    
    if result:
        sym = result[g.c.symbol]
        des = result[g.c.description]
        return sym,des
    else:
        return '',''
    
def get_zebrafish_gene_from_db(acc_short):
    g = Table('gardener_fasta_data', meta, autoload=True, autoload_with=engine)
    fasta_file_id = 14
    s = select([g.c.symbol,g.c.description]).where(and_(g.c.accession == acc_short, g.c.fasta_file_id == fasta_file_id))
    result = conn.execution_options(autocommit=True).execute(s).fetchone()
    
    if result:
        sym = result[g.c.symbol]
        des = result[g.c.description]
        return sym,des
    else:
        return '',''
    
#get_african_rice_gene_from_db  
def get_african_rice_gene_from_db(acc_short):
    g = Table('gardener_fasta_data', meta, autoload=True, autoload_with=engine)
    fasta_file_id = 16
    s = select([g.c.symbol,g.c.description]).where(and_(g.c.accession == acc_short, g.c.fasta_file_id == fasta_file_id))
    result = conn.execution_options(autocommit=True).execute(s).fetchone()
    
    if result:
        sym = result[g.c.symbol]
        des = result[g.c.description]
        return sym,des
    else:
        return '',''  

    
def get_xeno_gene_from_humandb(acc_short):
    g = Table('gardener_fasta_data', meta, autoload=True, autoload_with=engine)
    fasta_file_id = 13
    s = select([g.c.symbol,g.c.description]).where(and_(g.c.accession == acc_short, g.c.fasta_file_id == fasta_file_id))
    result = conn.execution_options(autocommit=True).execute(s).fetchone()
    
    if result:
        sym = result[g.c.symbol]
        des = result[g.c.description]
        return sym,des
    else:
        return '',''
        
def getGeneDescSymbol(conn, meta, gid):
    sym = ''
    des = ''
    g = Table('gardener_geneinfo', meta, autoload=True, autoload_with=engine)
    s = select([g.c.symbol, g.c.description]).where(g.c.gene_id == gid)
    res = conn.execution_options(autocommit=True).execute(s)
    row = res.fetchone()
    if row != None:
        sym = row[g.c.symbol]
        des = row[g.c.description]
    return sym, des

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
        #tmp = acc_short + '.'+'%'
        #s = select([g.c.geneid]).where(and_(g.c.protein_accession.like(tmp), g.c.tax_id == taxid))
    res = conn.execution_options(autocommit=True).execute(s).scalar()
    if res:
        gid = res
    return gid

def insert_file(conn, meta, file_data):
    t = Table('gardener_file', meta, autoload=True, autoload_with=engine)
    ins = t.insert()
    result = conn.execution_options(autocommit=True).execute(ins, name=file_data['name'], exp_id=file_data['exp_db_id'],
                        type=file_data['type'], file_type=file_data['file_type'],
                        jobid=file_data['job_id'], size=file_data['size'], path=file_data['path'],
                        rank=file_data['rank'], date=date_now()) 
    #return (result, file)

def update_file(conn, meta, file_data):
    file = Table('gardener_file', meta, autoload=True, autoload_with=engine)
    upd = file.update().where(file.c.jobid == file_data['job_id']).values(size=file_data['size'])
    result = conn.execution_options(autocommit=True).execute(upd) 
    return result

def updateFileReady(conn, meta, eid):
    e = Table('gardener_experiment',meta, autoload=True, autoload_with=engine)
    s = e.update().where(e.c.id==eid).values({ e.c.stage:0,e.c.state:'uploaded'})
    res = conn.execute(s)
    return res

def insert_search(conn, meta, file_data):
    search = Table('gardener_search', meta, autoload=True, autoload_with=engine)
    ins = search.insert()
    result = conn.execution_options(autocommit=True).execute(ins, repeat_id=file_data['r_num'], fraction_id=file_data['f_num'],
                        type='fraction', name=file_data['name'], exp_id=file_data['exp_db_id'],
                        num_spectrum=0, num_peptide=0, stage=1, user=file_data['user'],
                        num_isoform=0, num_gene=0, log=file_data['log'],
                        update_time=date_now(), create_time=date_now(),
                        rank=file_data['rank'], rt_max=0, parameter='unknown',state='running')
    return result

def insert_repeat(conn, meta, file_data):
    search = Table('gardener_search', meta, autoload=True, autoload_with=engine)
    
    ins = search.insert()
    result = conn.execution_options(autocommit=True).execute(ins, repeat_id=file_data['r_num'], fraction_id=0, rank=0,
                        type='repeat', name=file_data['name'], exp_id=file_data['exp_db_id'],
                        num_spectrum=0, num_peptide=0, num_isoform=0, num_gene=0,
                        user=file_data['user'], stage=5, log=file_data['log'],
                        update_time=date_now(), create_time=date_now(),
                        rt_max=0, parameter='unknown')
    return result

def insert_peptide(conn, meta, inserts):
    pep = Table('gardener_peptide', meta, autoload=True, autoload_with=engine)
    ins = pep.insert()
    result = conn.execution_options(autocommit=True).execute(ins, inserts) 
    return result

def insert_protein(conn, meta, inserts):
    pro = Table('gardener_protein', meta, autoload=True, autoload_with=engine)
    ins = pro.insert()
    result = conn.execution_options(autocommit=True).execute(ins, inserts) 
    return result

def insert_gene(conn, meta, inserts):
    g = Table('gardener_gene', meta, autoload=True, autoload_with=engine)
    s = g.insert()
    conn.execution_options(autocommit=True).execute(s, inserts)
    
def update_search_stage(conn, meta, file_data):
    search = Table('gardener_search', meta, autoload=True, autoload_with=engine)
    upd = search.update().where(search.c.id == file_data['search_id']).values({search.c.stage:file_data['stage'],
                                                                          search.c.update_time:date_now()})
    result = conn.execution_options(autocommit=True).execute(upd)
    return result

def delete_search(conn, meta, sid):
    s = text('delete from gardener_search where id=%s' % sid)
    conn.execution_options(autocommit=True).execute(s)
    print 'delete from gardener_search id=%s' % sid
'''    
def isDone(conn, meta, file_data):
    num=0
    x=Table('gardener_search', meta, autoload=True, autoload_with=engine)
    s=select([x.c.stage]).where(and_(x.c.exp_id==file_data['exp_db_id'],x.c.rank==file_data['rank']))
    result = conn.execution_options(autocommit=True).execute(s)
    #print 'count',result
    for row in result:
        num+=1
        if row[x.c.stage] < file_data['stage']:#Check every row to find if there's any uncompleted stage
            print 'Done?stage err: No'
            return 0
    if num<file_data['file_num']:#Make sure the num of converted rawfiles is right
        print 'Done?num err: No'
        return 0
    print 'Done?: Yes'
    return 1
'''
def isNewSearch(conn, meta, data):
    # rank = 1
    search = Table('gardener_search', meta, autoload=True, autoload_with=engine)
#     s = select([func.max(search.c.rank, type_=Integer)]).where(and_(search.c.exp_id == data['exp_db_id'],
#                                                                     search.c.fraction_id == data['f_num'],
#                                                                     search.c.repeat_id == data['r_num'], 
#                                                                     #search.c.user == data['user'],
#                                                                     search.c.type == 'fraction'))
    s = select([search.c.rank,search.c.num_spectrum]).where(and_(search.c.exp_id == data['exp_db_id'],
                                                                    search.c.fraction_id == data['f_num'],
                                                                    search.c.repeat_id == data['r_num'], 
                                                                    #search.c.user == data['user'],
                                                                    search.c.type == 'fraction'))
    
    res = conn.execute(s).fetchone()
    # print 'result',result
    if res :
        if res['num_spectrum']!=0:
            print 'Spectrum > 0'
            exit(1)
        else:
            print 'Spectrum == 0'
            rank = 1 
            insertDB = 0   
        #exit(1)
        #rank = res + 1
    else: 
        rank = 1 
        insertDB = 1   
    return (rank,insertDB)

def isRepDone(conn, meta, file_data):
    #user = file_data['user']
    stage_tool = file_data['stage']
    eid = file_data['exp_db_id']
    rank = file_data['rank']
    rep = file_data['r_num']
    x = Table('gardener_search', meta, autoload=True, autoload_with=engine)
    s1 = select([func.min(x.c.stage)]).where(and_(x.c.exp_id == eid, x.c.repeat_id == rep, x.c.rank == rank, x.c.type == 'fraction'))
    stage_min = conn.execution_options(autocommit=True).execute(s1).scalar()
    
    s2  = select([func.count(x.c.id)]).where(and_(x.c.exp_id == eid, x.c.repeat_id == rep, x.c.rank == rank, x.c.type == 'fraction'))
    num = conn.execution_options(autocommit=True).execute(s2).scalar()
    if num < file_data['fractionNum']:  # Make sure the num of converted rawfiles is right
        print 'Done?: No(err f_num of repeat)'
        return 0
 
    return stage_min

def isExpDone(conn, meta, file_data):
    #user = file_data['user']
    stage_tool = file_data['stage']
    eid = file_data['exp_db_id']
    rank = file_data['rank']
    x = Table('gardener_search', meta, autoload=True, autoload_with=engine)
    s1 = select([func.min(x.c.stage)]).where(and_(x.c.exp_id == eid, x.c.rank == rank, x.c.type == 'rep'))
    stage_min = conn.execution_options(autocommit=True).execute(s1).scalar()
    
    s2 = select([func.count(x.c.id)]).where(and_(x.c.exp_id == eid, x.c.rank == rank, x.c.type == 'fraction'))
    num = conn.execution_options(autocommit=True).execute(s2).scalar()
    if num < file_data['file_num']:  # Make sure the num of converted rawfiles is right
        print 'Done?: No(err total num of exp)'
        return 0

    return stage_min

def updateExpStage(conn, meta, file_data):
    stage_tool = file_data['stage']
    eid = file_data['exp_db_id']
    rank = file_data['rank']
    x = Table('gardener_search', meta, autoload=True, autoload_with=engine)
    s1 = select([func.min(x.c.stage)]).where(and_(x.c.exp_id == eid, x.c.type == 'rep'))
    stage_min = conn.execution_options(autocommit=True).execute(s1).scalar()
    s2 = select([func.count(x.c.id)]).where(and_(x.c.exp_id == eid, x.c.rank == rank, x.c.type == 'fraction'))
    num = conn.execution_options(autocommit=True).execute(s2).scalar()
    if num < file_data['file_num']:  # Make sure the num of converted rawfiles is right
        print 'Done?: No(num err)'
        # return 0
    if not stage_min:stage_min=1
    y = Table('gardener_experiment', meta, autoload=True, autoload_with=engine)
    upd = y.update().where(y.c.id == eid).values({y.c.stage:stage_min,
                                                y.c.update_date:date_now()})
    conn.execution_options(autocommit=True).execute(upd) 
    print 'stage of this tool:', stage_tool
    return stage_min
    # print 'Undefined stage???',stage_min
        
def rollBackAll(conn, meta, sid):
    s = 'delete from gardener_peptide where search_id=%s' % sid
    conn.execution_options(autocommit=True).execute(s)
    s = 'delete from gardener_protein where search_id=%s' % sid
    conn.execution_options(autocommit=True).execute(s)
    s = 'delete from gardener_gene where search_id=%s' % sid
    conn.execution_options(autocommit=True).execute(s)
    s = 'delete from gardener_ms2 where search_id=%s' % sid
    conn.execution_options(autocommit=True).execute(s)
    s = 'delete from gardener_ms1 where search_id=%s' % sid
    conn.execution_options(autocommit=True).execute(s)
    s = 'delete from gardener_search where id=%s' % sid
    conn.execution_options(autocommit=True).execute(s)

def rollBack(conn, meta, table, sid):
    s = 'delete from %s where search_id=%s' % (table, sid)
    conn.execution_options(autocommit=True).execute(s)
    
"""
       
# files = Table('gardener_file', meta, autoload=True, autoload_with=engine)
# s = select([files])
# result = conn.execution_options(autocommit=True).execute(s) 
# for row in result: 
#     print(row)

    if stage_min < stage_tool:
        print 'Done?: No(stage err)'
        return 0

    if stage_tool == 2:
        s   = select([func.sum(x.c.num_spectrum)]).where(and_(x.c.exp_id==eid,x.c.rank==rank))
        sum = conn.execution_options(autocommit=True).execute(s).scalar()
        y   = Table('gardener_experiment', meta, autoload=True, autoload_with=engine)
        upd = y.update().where(y.c.id==eid).values({y.c.stage:stage_tool,
                                                        y.c.num_spectrum:sum})
        conn.execution_options(autocommit=True).execute(upd)
        print 'Done?: Yes'
        print 'stage',stage_tool
        return stage_tool

    if stage_tool == 5:
        s   = select([func.sum(x.c.num_spectrum)]).where(and_(x.c.exp_id==eid,x.c.rank==rank,x.c.type=='fraction'))
        sum = conn.execution_options(autocommit=True).execute(s).scalar()
        
        t1 = text("select count(DISTINCT (sequence,modification)) from gardener_peptide where type=1 and search_id in(SELECT id from gardener_search where exp_id=%s and type=\'fraction\')"%eid)
        num_pep = conn.execution_options(autocommit=True).execute(t1).scalar()
        #print 'num_pep_exp',num_pep_exp
        t2 = text("select count(DISTINCT accession) from gardener_protein where type=1 and search_id in(SELECT id from gardener_search where exp_id=%s and type=\'fraction\')"%eid)
        num_pro = conn.execution_options(autocommit=True).execute(t2).scalar()
        #print 'num_pro_exp',num_pro_exp
        t3 = text("select count(DISTINCT gene_id) from gardener_gene where type=1 and search_id in(SELECT id from gardener_search where exp_id=%s and type=\'fraction\')"%eid)
        num_gen = conn.execution_options(autocommit=True).execute(t3).scalar()
        y = Table('gardener_experiment', meta, autoload=True, autoload_with=engine)
        upd = y.update().where(y.c.id==eid).values({y.c.stage:stage_tool,
                                                    y.c.num_spectrum:sum,
                                                    y.c.num_peptide:num_pep,
                                                    y.c.num_isoform:num_pro,
                                                    y.c.num_gene:num_gen})
        conn.execution_options(autocommit=True).execute(upd) 
        print 'stage',stage_tool
        return stage_tool,sum,num_pep,num_pro,num_gen
    



def getJobId(conn,meta,track_id,user_id):
   
    job=Table('job', meta, autoload=True, autoload_with=engine)
    s = select([job.c.command_line,job.c.id,job.c.history_id]).where(and_(job.c.user_id==user_id,job.c.state=="running"))
    result = conn.execution_options(autocommit=True).execute(s) 
    for row in result: 
        cmd=str(row[job.c.command_line])
        m=re.search(r'\-j\s(\d+)', cmd)
        if m:
           job_id=m.group(1)
           if job_id==track_id:
               job_id=str(row[job.c.id]) 
    job_id=job_id if ('job_id' in dir()) else -1 
      
    return job_id 
 
def insert_ms1data(conn,meta,inserts):
    ms1data=Table('gardener_ms1data', meta, autoload=True, autoload_with=engine)
    ins = ms1data.insert()
    result=conn.execution_options(autocommit=True).execute(ins, inserts) 
    return result
    
def insert_mascotdat(conn,meta,inserts):
    mascot=Table('gardener_mascotdat', meta, autoload=True, autoload_with=engine)
    ins = mascot.insert() 
    result=conn.execution_options(autocommit=True).execute(ins, inserts) 
    return result
"""    
