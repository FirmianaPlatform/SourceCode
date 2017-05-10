#!/usr/bin/env python
import optparse, os, shutil, subprocess, sys, tempfile, urllib2, urllib, re, base64
import httplib, mimetypes, mimetools, cookielib
import pycurl
import StringIO
from poster.encode import multipart_encode, MultipartParam
from poster.streaminghttp import register_openers, StreamingHTTPHandler, StreamingHTTPRedirectHandler, StreamingHTTPSHandler
#from binascii import b2a_base64
from HTMLParser import HTMLParser
from bs4 import BeautifulSoup

ms_tools_path = os.path.join( os.path.dirname( __file__ ), '..')
GALAXY_ROOT = os.path.join( ms_tools_path, '..', '..' )

sys.path.insert(1, ms_tools_path)
#from models.firmiana_models import *
from config.firmianaConfig import *
from models.gardener_control import *
MASCOT_CGI = os.path.join( ConfigSectionMap("Mascot")['address'], 'mascot/cgi' )
#session = Session()
#LIPENG = [116,119]
#LIPENG = ['Exp000080','Exp000083','Exp000085']
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

def update_search_param(conn,meta,pars,file_data):
    search=Table('gardener_search',meta, autoload=True, autoload_with=engine)
    upd=search.update().where(search.c.id==file_data['search_id']).values({search.c.parameter:pars,
                                                                           search.c.stage:file_data['stage'],
                                                                           search.c.update_time:date_now()})
    result=conn.execute(upd)
    return result



def update_experiment_pep(conn, meta, file_data):
    """
    num_pep_exp = 0
    search=Table('gardener_search',meta, autoload=True, autoload_with=engine)
    exp=Table('gardener_experiment',meta, autoload=True, autoload_with=engine)
    s = select([search.c.num_peptide]).where(and_(search.c.exp_id==file_data['exp_db_id'],search.c.rank==file_data['rank']))
    result = conn.execute(s)
    for row in result:
        num_pep_exp+=row[search.c.num_peptide]
    """
    t1 = text("select count(DISTINCT gardener_peptide.sequence) from gardener_peptide where search_id in(SELECT id from gardener_search where gardener_search.exp_id=%s and rank=%s and type=\'fraction\')"%(file_data['exp_db_id'],file_data['rank']))
    num_pep_exp = conn.execute(t1).scalar()
    print 'num_pep_exp',num_pep_exp
    
    t2 = text("select count(DISTINCT gardener_protein.accession) from gardener_protein where search_id in(SELECT id from gardener_search where gardener_search.exp_id=%s and rank=%s and type=\'fraction\')"%(file_data['exp_db_id'],file_data['rank']))
    num_pro_exp = conn.execute(t2).scalar()
    print 'num_pro_exp',num_pro_exp
    
    exp=Table('gardener_experiment',meta, autoload=True, autoload_with=engine)
    upd=exp.update().where(exp.c.id==file_data['exp_db_id']).values({exp.c.num_peptide:num_pep_exp,
                                                                     exp.c.num_isoform:num_pro_exp,
                                                                     exp.c.stage:file_data['stage']})
    result=conn.execute(upd)
    
    return result

  
def sql_gardener_file(options):
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
    
    file_data['exp_db_id'] = get_exp_id(conn,meta,'Exp%s'%exp['exp_id'])#ID of exp table!!!
    file_data['stage'] = 4
    file_data['size']  = 0
    file_data['file_type'] = 'mascotdat'
    file_data['type'] = 'reference'
    file_data['path'] = options.output
    file_data['user'] = get_user_name(conn,meta,options.user_id)
    file_data['rank'] = get_rank(conn,meta,file_data)
    file_data['search_id'] = get_search_id(conn,meta,file_data)
    file_data['date'] = date_now()#time.strftime("%Y-%m-%d %X", time.gmtime())
    file_data['file_num'] = get_file_num(conn,meta,file_data['exp_db_id'])
    
    insert_file(conn,meta,file_data)                 
    return ((file_data['name']+"_"+file_data['job_id']+"."+file_data['file_type']),file_data)  
        
def encode_multipart_formdata(fields, files):
    """
    fields is a sequence of (name, value) elements for regular form fields.
    files is a sequence of (name, filename, value) elements for data to be uploaded as files
    Return (content_type, body) ready for httplib.HTTP instance
    """
    BOUNDARY = mimetools.choose_boundary()
    CRLF = '\r\n'
    L = []
    for (key, value) in fields:
        #print key,value
        L.append('--' + BOUNDARY)
        L.append('Content-Disposition: form-data; name="%s"' % key)
        L.append('')
        L.append(value)
    for (key, filename, value) in files:
        #print key, filename
        L.append('--' + BOUNDARY)
        L.append('Content-Disposition: form-data; name="%s"; filename="%s"' % (key, filename))
        content_type = get_content_type(filename)
        #content_type='text/plain; charset=ascii'
        #content_type='application/octet-stream'
        L.append('Content-Type: %s' % content_type)
        L.append('')
        L.append(value)
    L.append('--' + BOUNDARY + '--')
    L.append('')
    body = CRLF.join(L)
    content_type = 'multipart/form-data; boundary=%s' % BOUNDARY
    return content_type, body
 
def get_content_type(filename):
    return mimetypes.guess_type(filename)[0] or 'application/octet-stream'

def register_openers(cookiejar=None):
    """Register the streaming http handlers in the global urllib2 default
    opener object.
    Returns the created OpenerDirector object."""
    handlers = [StreamingHTTPHandler, StreamingHTTPRedirectHandler]
    if hasattr(httplib, "HTTPS"):
        handlers.append(StreamingHTTPSHandler)
    if cookiejar:
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookiejar), *handlers)
    else:
        opener = urllib2.build_opener(*handlers)
    urllib2.install_opener(opener)
    return opener
    
def post_multipart(host, selector, fields, files):
    """
    Post fields and files to an http host as multipart/form-data.
    fields is a sequence of (name, value) elements for regular form fields.
    files is a sequence of (name, filename, value) elements for data to be uploaded as files
    Return the server's response page.
    """
    content_type, body = encode_multipart_formdata(fields, files)
    headers = {'Content-Type': content_type,
               'Content-Length': str(len(body))}

    #r = urllib2.Request("%s%s" % (host, selector), b2a_base64(body), headers)
    r = urllib2.Request("%s%s" % (host, selector), body, headers)
    #return urllib2.urlopen(r).read()
    return urllib2.urlopen(r)
    
def postFileRequest(url, paramName, fileObj, additionalHeaders={}, additionalParams={}):
    items = []
    #wrap post parameters
    for name, value in additionalParams.items():
        items.append(MultipartParam(name, value))
    #add file
    items.append(MultipartParam.from_file(paramName, fileObj))
    datagen, headers = multipart_encode(items)
    #add headers
    for item, value in additionalHeaders.iteritems():
        headers[item] = value
    return urllib2.Request(url, datagen, headers)    
    
def poster_multipart(url, additionalParams, filename):
    # Register the streaming http handlers with urllib2    
    #register_openers()
    username = ConfigSectionMap("Mascot")['username']
    password = ConfigSectionMap("Mascot")['password']
    login_url = MASCOT_CGI + '/login.pl'#ConfigSectionMap("Mascot")['login_url']
    #To include cookie handling
    #opener = register_openers()
    #opener.add_handler(urllib2.HTTPCookieProcessor(cookielib.CookieJar()))
    
    cookiejar = cookielib.CookieJar()
    loginOpener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookiejar))

    params = urllib.urlencode({'username':username, 'password':password, 'action':'login'})
   
    request = urllib2.Request(login_url, params)
    login = loginOpener.open(request)
    #print login.read()
    
    # Upload File
    # use the login cookie for file upload
    register_openers(cookiejar=cookiejar)
    # Start the multipart/form-data encoding of the file "DSC0001.jpg"
    # "image1" is the name of the parameter, which is normally set
    # via the "name" parameter of the HTML <input> tag.
    # headers contains the necessary Content-Type and Content-Length
    # datagen is a generator object that yields the encoded parameters
    items = []
    #wrap post parameters
    for name, value in additionalParams.items():
        items.append(MultipartParam(name, value))
    #add file
    #fileobj=open(filename, "rb")
    #MultipartParam(name, value=None, filename=None, filetype=None, filesize=None, fileobj=None, cb=None)
    items.append(MultipartParam.from_file('FILE', filename))
    #items.append(MultipartParam('infile', open(filename, "r"),filetype='text/plain; charset=utf8'))
    # Data for MS/MS ion searches must be supplied as an ASCII file   
    #items.append(MultipartParam('FILE',fileobj ,filetype='application/octet-stream'))
    
    datagen, headers = multipart_encode(items)
    user_agent = 'Mozilla/5.0'
    headers[ 'User-Agent'] = user_agent 
    #headers['Content-Transfer-Encoding']= 'base64'
    
    #s = "".join(datagen)
    # Create the Request object
    #request = urllib2.Request(url, b2a_base64(s), headers)
    request = urllib2.Request(url, datagen, headers)

    #To add basic authentication to the request
    #auth = base64.encodestring('%s:%s' % (username, password))[:-1] # This is just standard un/pw encoding  
    #request.add_header('Authorization', 'Basic %s' % auth ) # Add Auth header to request

    # Actually do the request, and get the response
    
    return urllib2.urlopen(request)

#return whether it is OK to run the tool
def checkDatabase(input, searchType, output, dbop_type):   
    try:
        """
        convertedRawfile=session.query(ConvertedRawfile).filter(ConvertedRawfile.filepath==inputfile).first()
        if not convertedRawfile:
            stop_err( 'Error adding records to DBSearchResult due to the lack of ConvertedRawfile record.\n' )
        convertedRawfileID=str(convertedRawfile.id)
        """
        #to avoid consistency problem, convertedRawfileID is set to that of mzxml file instead of mgf file
        convertedRawfile = session.query(ConvertedRawfile).filter(and_(ConvertedRawfile.filepath == input, ConvertedRawfile.fileType == 'mgf')).first()
        if not convertedRawfile:
            stop_err('Error adding records to DBSearchResult due to the lack of ConvertedRawfile record.\n')
        rawfileID = str(convertedRawfile.rawfileID)
        #get the corresponding mzxml file
        convertedRawfile = session.query(ConvertedRawfile).filter(and_(ConvertedRawfile.rawfileID == rawfileID, ConvertedRawfile.fileType == 'mzxml')).first()        
        convertedRawfileID = str(convertedRawfile.id)
        
        #dbsearchResult=session.query(DBSearchResult).filter(DBSearchResult.filepath==resultfilepath).first()
        #for each converted raw file, given the db search method (mascot, tandem), there should be only one DBSearchResult.
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
                 #by cascade, when deleting dbsearchResult, related parameter table will also be deleted  
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
        session.rollback()
        stop_err('Error checking records in DBSearchResult.\n%s' % (str(e)))      

     
#inputfile: the full name of input mzXML file
def storeDBSearchResult(convertedRawfileID, searchType, resultfilepath, options):                
    try:
        dbsearchResult = DBSearchResult(convertedRawfileID, searchType, resultfilepath, '')
        print dbsearchResult
        #store parameters at the same time
        mascotParam = MascotParam('', options.database, options.var_mods, options.fix_mods, options.enzyme, options.precursor_tolu, options.missed_cleavages, options.fragment_ion_tol, options.allowed_charges, options.instrument, options.precursor_search_type)
        dbsearchResult.mascotParams.append(mascotParam)
        session.add(dbsearchResult)
        session.commit()
    except Exception, e:
        session.rollback()
        stop_err('Error adding records to DBSearchResult.\n%s' % (str(e))) 


def checkMascotParam(filepath):
    try:
        dbsearchResult = session.query(DBSearchResult).filter(DBSearchResult.filepath == filepath).first()
        if not dbsearchResult:
            stop_err('Error adding records to MascotParam due to the lack of DBSearchResult.\n')
        dbsearchResultID = str(dbsearchResult.id)
        
        mascotParam = session.query(MascotParam).filter(MascotParam.dbsearchResultID == dbsearchResultID).first()
        #if mascotParam:
            #session.delete(mascotParam) 
        if mascotParam is not None:
             if dbop_type == 'update':       
                 session.delete(mascotParam)
                 return (True, dbsearchResultID)                                 
             elif dbop_type == 'delete':    
                 session.delete(mascotParam)
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
                stop_err('Error adding records to MascotParam.\n%s\n' % ''.join(errlist))
        else:
            #print 'experiment is None'
            if dbop_type == 'update' or dbop_type == 'delete':      
                err = 'There is no information about this analysis in the database.'
                stop_err('Error changing information for MascotParam in the database.\n%s\n' % err)       
            return (True, dbsearchResultID)    
    except Exception, e:
         stop_err('Error checking records in MascotParam.\n%s' % (str(e)))  


        
#database,var_mods,fix_mods,enzyme,precursor_tolu,missed_cleavages,fragment_ion_tol,allowed_charges,instrument,precursor_search_type
def storeMascotParam(dbsearchResultID, database, var_mods, fix_mods, enzyme, precursor_tolu, missed_cleavages, fragment_ion_tol, allowed_charges, instrument, precursor_search_type, dbop_type):                
    try:    
        mascotParam = MascotParam(dbsearchResultID, database, var_mods, fix_mods, enzyme, precursor_tolu, missed_cleavages, fragment_ion_tol, allowed_charges, instrument, precursor_search_type)
        #print mascotParam
        session.add(mascotParam)
        session.commit()
    except Exception, e:
         stop_err('Error adding records to MascotParam.\n%s' % (str(e))) 

#mascot_result = []

class MyHTMLParser(HTMLParser):
    def handle_data(self, data):
        #not contain 'Mascot search status page'
        if data.find('Mascot search status page') == -1:
            mascot_result.append(data)

def pycurl_download(url):#,post_file):
    #return 'test '
    #print pycurl.version_info()
    c = pycurl.Curl()
    b = StringIO.StringIO()
    c.setopt(pycurl.URL, url)
    c.setopt(pycurl.WRITEFUNCTION, b.write)
    c.setopt(pycurl.FOLLOWLOCATION, 1)
    c.setopt(pycurl.MAXREDIRS, 5)
    c.setopt(pycurl.CONNECTTIMEOUT, 60)
    c.setopt(pycurl.USERAGENT, "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.116 Safari/537.36")
    c.perform()
    print '===================================================='
    print "HTTP-code:", c.getinfo(c.HTTP_CODE) 
    print "Total-time:", c.getinfo(c.TOTAL_TIME)
    print "Download speed: %.2f bytes/second" % c.getinfo(c.SPEED_DOWNLOAD)
    print "Document size: %d bytes" % c.getinfo(c.SIZE_DOWNLOAD)
    print "Effective URL:", c.getinfo(c.EFFECTIVE_URL)
    print "Content-type:", c.getinfo(c.CONTENT_TYPE)
    print "Namelookup-time:", c.getinfo(c.NAMELOOKUP_TIME)
    print "Redirect-time:", c.getinfo(c.REDIRECT_TIME)
    print "Redirect-count:", c.getinfo(c.REDIRECT_COUNT)
    
    html = b.getvalue()
    
    b.close()
    c.close()
    
    return html
              
def getPureDat(html):
    content = ''
    if html:
        soup = BeautifulSoup(html)
        #print soup
        #content=soup.pre.contents[0] #truncated before xml tags
        content = ''
        pre = soup.find('pre')
        #print pre
        if pre:
            #content = pre[0].string  #will return none type, since there are more than one thing
            #soup = BeautifulSoup(str(pre))
            #A tag's children are available in a list called .contents
            for dat in pre.contents:
                content += str(dat)  #still have pre tag
            """ 
            #not feasible to replace the tags
            print content[0:100]            
            print content.find(r'<pre>')
            content.replace(r'<pre>', '')            
            print content[0:100]
            print content.find(r'</pre>')
            content.replace(r'</pre>', '')
            print content[-100:]
            """
            #content=str(soup.contents[0]) #get the whole html file
            
            #soup = BeautifulSoup(str(pre))
            #for string in soup.strings:
            #   content+=str(string) #delete xml tags, not right
                #content+=repr(string)   #repr() is meant to generate representations which can be read by the interpreter     
            #content=soup.get_text() #delete xml tags
        else:
            #print html
            print '===================================================='

    return content

def runTool(mascot_cgi, url, postdict, options):
    print 'start!(mascot)',str(datetime.datetime.now().strftime('%X'))
    try:
        # Run command.
        tmp_name = tempfile.NamedTemporaryFile(dir=".").name
        tmp_stderr = open(tmp_name, 'wb')
        
        """cj = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        urllib2.install_opener(opener)
        """
        #files is a sequence of (name, filename, value) elements for data to be uploaded as files
        #filevalue=open(infilename, "rb").read()
        #files=[('FILE',infilename,filevalue)]
        #fields=[(k, v) for k, v in postdict.iteritems()]
        
        #search_response=post_multipart(url,'',fields,files)       
        search_response = poster_multipart(url, postdict, options.input)        
        #search_response=urllib2.urlopen(url,  urllib.urlencode(postdict))
        response = search_response.read()
        print response
        #print search_response.geturl()
        # Look for an errorer if there is one
        #if re.match(r'error', str(search_response.read())):
        error_results = 'Sorry, your search could not be performed'
        if response.find(error_results) != -1:
            stop_err("Mascot search failed with response " + str(search_response.info()))
        else:
            ''' 
            Search for the location of the mascot data file in the response
            eg.http://192.168.151.142/mascot/cgi/master_results.pl?file=../data/20121207/F001245.dat            
            <A HREF="../cgi/master_results.pl?file=../data/20121209/F001376.dat">Click here to see Search Report</A>            
            results=re.search(r'master_results.pl\?file=\.*\/data\/(.*)\/(.+\.dat)',response)
            '''
            #for the newer version
        results = re.search(r'master_results.*.pl\?file=\.*\/data\/(.*)\/(.+\.dat)', response)
        if results:
            #print results.group(0)
            results_date = results.group(1)
            results_file = results.group(2)
                
            #results_date='20121209' 
            #results_file='F001376.dat' 
            # Download the results
            get_url = mascot_cgi + "/../x-cgi/ms-status.exe?Autorefresh=false&Show=RESULTFILE&DateDir=" + results_date + "&ResJob=" + results_file 
            #print 'URL = ', get_url
            #print 'Start download mascot dat...', str(datetime.datetime.now().strftime('%X'))
            #u = urllib2.urlopen(get_url, timeout=1000)
            #print 'Over download mascot dat : ', str(datetime.datetime.now().strftime('%X'))
                
            #html = u.read()
                
            html = pycurl_download(get_url)
            print '===================================================='
            if html:
                #print 'Below is .dat file content[0:200]:\n'
                #print html[0:200]
                content = html#getPureDat(html)
            else:
                print 'no content'
            #print content
            #<HTML><HEAD><TITLE>Mascot search status page</TITLE></HEAD><BODY bgcolor="#ffffff">
            #<PRE>...</PRE></BODY></HTML>
            #parser = MyHTMLParser()
            #parser.feed(content)
            #filename = 'test.html'
                
                
            f = open(options.output, 'wb')
            f.write(content.encode('utf-8'))
            f.close()
                
            print '\nComplete!(mascot)',str(datetime.datetime.now().strftime('%X'))
            return 0
        else:
            stop_err("Mascot search failed with no results. ")
                
        tmp_stderr.close()
        
        """ 
        seachType = 'mascot'
        #inputfile,searchType,resultfilepath
        print options.input, seachType, options.output
        storeDBSearchResult(options.input, seachType, options.output, options.dbop_type)
        #database,var_mods,fix_mods,enzyme,precursor_tolu,missed_cleavages,fragment_ion_tol,allowed_charges,instrument,precursor_search_type
        print options.output, options.database, var_mods, fix_mods, options.enzyme, options.precursor_tolu, options.missed_cleavages, options.fragment_ion_tol, options.instrument
        storeMascotParam(options.output, options.database, var_mods, fix_mods, options.enzyme, options.precursor_tolu, options.missed_cleavages, options.fragment_ion_tol, options.allowed_charges, options.instrument, options.precursor_search_type, options.dbop_type)
        """            
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
        
        stop_err('Error running Mascot.\n%s\n' % (str(e)))   

def get_search_param(file_data, postdict):
    def getEnzyme(conn, meta, id):
        e = Table('experiments_digest_enzyme', meta, autoload = True, autoload_with = engine)
        s = select([e.c.name]).where(e.c.id == id)
        res = conn.execute(s).scalar()
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
        return res
    def getITOL(conn, meta, id):
        e = Table('experiments_instrument_ms2_tol', meta, autoload = True, autoload_with = engine)
        s = select([e.c.name]).where(e.c.id == id)
        res = conn.execute(s).scalar()
        return res
    def getFixMods(conn, meta, eeid):
        tmp = ''
        A = Table('experiments_experiment_fixed_modifications', meta, autoload = True, autoload_with = engine)
        B = Table('experiments_fixed_modification', meta, autoload = True, autoload_with = engine)
        s = select([B.c.name]).select_from(A.join(B, B.c.id == A.c.fixed_modification_id)).where(A.c.experiment_id == eeid)
        res = conn.execute(s)
        if not res:return ''
        for row in res:
            tmp = tmp + row['name'] +','
        return tmp[:-1]
    def getVarMods(conn, meta, eeid):
        tmp = ''
        A = Table('experiments_experiment_dynamic_modifications', meta, autoload = True, autoload_with = engine)
        B = Table('experiments_dynamic_modification', meta, autoload = True, autoload_with = engine)
        s = select([B.c.name]).select_from(A.join(B, B.c.id == A.c.dynamic_modification_id)).where(A.c.experiment_id == eeid)
        res = conn.execute(s)
        if not res:return ''
        for row in res:
            tmp = tmp + row['name'] +','
        return tmp[:-1]
    def getSearchDB(conn, meta, id):
        e = Table('experiments_search_database', meta, autoload = True, autoload_with = engine)
        s = select([e.c.name]).where(e.c.id == id)
        res = conn.execute(s).scalar()
        return res
    
    eid = file_data['exp_db_id']
    eeid = file_data['exp_id']
    ee_name = 'Exp%s' %eeid
    #db = get_database(eid, ee_name)
    #if db : postdict['DB'] = db
    print 'ee_name=',ee_name
    
    e = Table('experiments_experiment', meta, autoload = True, autoload_with = engine)
    s = select([e.c.id,
                e.c.digest_enzyme_id,
                e.c.instrument_name_id,
                e.c.ms1_details_id,
                e.c.ms2_details_id,
                e.c.search_database_id]).where(e.c.name == ee_name)
    res = conn.execute(s).fetchone()
    if not res:
        exit(1)
    eeid = res['id']
    enzyme_id = res['digest_enzyme_id']
    instru_id = res['instrument_name_id']
    ms1_param_id = res['ms1_details_id']
    ms2_param_id = res['ms2_details_id']
    search_database_id = res['search_database_id']
    
    enzyme = getEnzyme(conn, meta, enzyme_id)
    instru = getInstru(conn, meta, instru_id)
    tol  = getTOL(conn, meta, ms1_param_id)
    itol = getITOL(conn, meta, ms2_param_id)
    fix_mods = getFixMods(conn, meta, eeid)
    var_mods = getVarMods(conn, meta, eeid)
    search_database = getSearchDB(conn, meta, search_database_id)
    #print enzyme,instru,tol,itol,'||',fix_mods,var_mods
    
    postdict['CLE'] = enzyme
    t = re.search(r'([^a-z^A-Z]*)(.*)', itol)
    postdict['ITOL'], postdict['ITOLU'] = t.group(1).strip(), t.group(2).strip()
    #postdict['ITOL'], postdict['ITOLU'] = '0.5', 'Da'
    t = re.search(r'([^a-z^A-Z]*)(.*)', tol)
    postdict['TOL'],  postdict['TOLU']  = t.group(1).strip(), t.group(2).strip()
    postdict['INSTRUMENT'] = 'Default'#instru
    postdict['IT_MODS'], postdict['MODS'] = var_mods, fix_mods
    postdict['DB'] = search_database

    pars = ','.join([ p +'=' + str(v) for p,v in postdict.items()])
    print pars
    
    return (pars, postdict)    

def getParam():
     #Parse Command Line
    parser = optparse.OptionParser()
    parser.add_option('-i', '', dest='input', help=' ')
    parser.add_option('-d', '', dest='database', help=' ')
    parser.add_option('-o', '', dest='output', help='')
    parser.add_option('-S', '', dest='server', help='')
    parser.add_option('', '--var-mods', dest='var_mods', help='')
    parser.add_option('', '--fix-mods', dest='fix_mods', help='')    
    parser.add_option('', '--enzyme', dest='enzyme', help='')
    parser.add_option('-f', '', dest='fragment_ion_tol', type="float", help='')
    parser.add_option('-p', '', dest='precursor_ion_tol', type="float", help='')
    parser.add_option('', '--precursor-search-type', dest='precursor_search_type', help='')
    parser.add_option('', '--precursor-ion-tol-units', dest='precursor_tolu', help='')
    parser.add_option('', '--fragment-ion-tol-units', dest='fragment_tolu', help='')
    parser.add_option('-v', '', dest='missed_cleavages', type="int", help='')
    parser.add_option('', '--instrument', dest='instrument', help='')
    parser.add_option('', '--allowed-charges', dest='allowed_charges', help='Keep X!Tandem parameter files')
    parser.add_option('', '--email', dest='email', help='Dont convert to pepXML after running the search') 
    parser.add_option('', '--username', dest='username', help='allow multi_isotope_search')
    #parser.add_option('', '--dbop_type', dest='dbop_type', action='store', help='')
    parser.add_option('', '--store_to_db', dest='store_to_db', action='store', help='')
    parser.add_option('-j', '--job_track_id', dest='job_track_id', action='store', type="string", help='Job track ID for firmiana.')
    parser.add_option('-u', '--user_id', dest='user_id', action='store', type="string", help='User id for galaxy runner.')
    parser.add_option('-a', '--label_name', dest='label_name', action='store', type="string", help='Label name for out file.')
    (options, args) = parser.parse_args()
    
    #print options.var_mods
    #print options.fix_mods
    #var_mods = [ mod.strip() for mod in options.var_mods.split(",") if not mod.isspace() ]
    #fix_mods =  [mod.strip() for mod in options.fix_mods.split(",") if not mod.isspace() ]
    var_mods = ''
    fix_mods = ''
    if options.var_mods:
        for mod in options.var_mods.split(","): 
            if not mod.isspace():
                var_mods += mod.strip() + ','
    if options.fix_mods:
        for mod in options.fix_mods.split(","): 
            if not mod.isspace():
                fix_mods += mod.strip() + ','    
    
    #contain None
    if options.var_mods.find('None') != -1:
        var_mods = ''
    if options.fix_mods.find('None') != -1:
        fix_mods = ''
        
    postdict = {}
    postdict['DECOY'] = 1
    # CHARGE
    postdict['CHARGE'] = options.allowed_charges
    # CLE
    postdict['CLE'] = options.enzyme
    # PFA
    postdict['PFA'] = str(options.missed_cleavages)
    # DB (Database)
    postdict['DB'] = options.database
    # INSTRUMENT
    postdict['INSTRUMENT'] = options.instrument
    # IT_MODS (Variable Modifications)
    postdict['IT_MODS'] = var_mods#getvar_mods()
    # ITOL (Fragment ion tolerance)
    postdict['ITOL'] = str(options.fragment_ion_tol)
    # ITOLU (Fragment ion tolerance units)
    postdict['ITOLU'] = options.fragment_tolu#'Da'
    # MASS (Monoisotopic and Average)
    postdict['MASS'] = options.precursor_search_type
    # MODS (Fixed modifications)
    postdict['MODS'] = fix_mods#get_fix_mods()
    # TOL (Precursor ion tolerance (Unit dependent))
    postdict['TOL'] = str(options.precursor_ion_tol)
    # TOLU (Tolerance Units)
    postdict['TOLU'] = options.precursor_tolu
    # Email
    postdict['USEREMAIL'] = options.email
    # Username
    postdict['USERNAME'] = options.username
    # COM (Search title)
    postdict['COM'] = "Test_qiunq"
     # REPORT (What to include in the search report. 
    #For command-line searches this is pretty much irrelevant because we retrieve the entire results file anyway)
    postdict['REPORT'] = 'AUTO'
    # TAXONOMY (Blank because we don't allow taxonomy)
    postdict['TAXONOMY'] = "All entries"
    # FILE
    postdict['FORMAT'] = "Mascot generic"
    
    postdict['FORMVER'] = '1.01'
    postdict['INTERMEDIATE'] = ''
    #SEARCH
    postdict['SEARCH'] = 'MIS'
    #print "Sending"+str(postdict)

    #for key in postdict:
        #print 'key=%s, value=%s' % (key, postdict[key])
    return (postdict,options,args)

def storeDB(file_data,options,pars):
    file_data['size']= str(os.path.getsize(options.output)/1024)+'K'
    update_file(conn,meta,file_data)
    #parserMascotdat(options.output,file_data)
    update_search_param(conn,meta,pars,file_data)
    
    #if isDone(conn, meta, file_data):#If all files converted
    #    update_experiment_pep(conn, meta, file_data)
    sid = get_cache_rep_sid(conn,meta,file_data)
    update_rep_stage(conn, meta, file_data,sid)
    
    updateExpStage(conn,meta,file_data)
 
def __main__():
    (postdict, options, args) = getParam()
    #print postdict
    #http://192.168.151.142/mascot/cgi/nph-mascot.exe?1
    mascot_cgi = MASCOT_CGI
    #mascot_cgi = options.server
    url = os.path.join( mascot_cgi, 'nph-mascot.exe?1' )
    searchType = 'mascot'
    print url
    
    if options.store_to_db == 'yes':
        
        (storename, file_data) = sql_gardener_file(options)
        (pars, postdict) = get_search_param(file_data, postdict)
        runTool(mascot_cgi, url, postdict, options)
        #=======================================================================
        # cp_to = os.path.join(GALAXY_ROOT,'database/files/mascot_result', 'Exp%s'%file_data['exp_id'],file_data['name'])
        # if not os.path.isdir(cp_to):
        #     os.makedirs(cp_to)
        # shutil.copy(options.output, cp_to)
        #=======================================================================
        storeDB(file_data, options, pars)
    else:
        runTool(mascot_cgi, url, postdict, options)
            
if __name__ == "__main__": __main__()
