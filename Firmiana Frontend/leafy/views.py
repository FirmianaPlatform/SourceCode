from django.template.loader import get_template
from django.template import Context
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.contrib.auth import logout, login, authenticate
import os,re
from hashlib import md5
from leafy.forms import *
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
import json

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.mail import send_mail
#from django.views.decorators.csrf import csrf_exempt
from  leafy.password_trans import new_secure_hash
from  leafy.password_trans import check_password
#from authority_trans import SecurityHelper
import subprocess

from experiments.models import *
from gardener.models import Search as gardener_search
from gardener.models import Experiment as gardener_experiment

import datetime,time
from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder

from Bio import SeqIO
from Bio import Entrez

import threading

from bioblend.galaxy import GalaxyInstance

import smtplib  
from email.mime.text import MIMEText 

'''Used for validating child account'''
from experiments.views import isChildAccount
from experiments.views import isActive_ChildUser
from experiments.views import isParentAccount
from experiments.views import isValidatedUser


NFS_path = '/usr/local/firmiana/galaxy-dist/database/files/'
import oss
from oss.oss_api import *
from lxml import etree as ET

AUTHTRANSPATH=os.path.join("/usr/local/bin/python ",settings._ROOT_PATH, 'authority_trans.py')
my_env = os.environ
my_env["PATH"] = settings._ROOT_PATH+":" + my_env["PATH"]

#online_num = 0
    
def main_page(request):
    ''' return HttpResponseRedirect('/gardener/') '''
    return HttpResponseRedirect(settings.LOGIN_PAGE)

#@login_required(login_url="/login/")
def logout_page(request):
    '''
    p = subprocess.Popen([AUTHTRANSPATH, request.COOKIES['galaxysession']], stdout=subprocess.PIPE,env=my_env)
 #   session_key = p.stdout.read().strip()

    #use the following code in the real server, because p will have other string with respect to django log
    gsession_key = p.stdout.read().strip()
    session_key = gsession_key.split('\n')[-1]

    galaxysession = Galaxy_session.objects.get(session_key=session_key)
    galaxysession.delete()
    #print 'before'
    '''
    logout(request)
    #print 'after'
    return HttpResponseRedirect(settings.LOGOUT_PAGE)

"""
def login_page(request):
    error = ''
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            username = cd['username']
            password = cd['password']
            user = authenticate(username=username, password=password)
            if user is not None and user.is_active:
                login(request, user)
                return HttpResponseRedirect('experiment/')
            else:
                error = "Your username and/or password were incorrect"
    else:
        form = LoginForm()
    variables = RequestContext(request, {'form': form , 'error':error})
    return render_to_response('login.html', variables)
    response["P3P"] = 'CP="IDC DSP COR ADM DEVi TAIi PSA PSD IVAi IVDi CONi HIS OUR IND CNT"'
"""

'''
def login_page(request):
    
    galaxyloginurl = settings.GALAXY_URL_LOGIN
    if 'galaxysession' in request.COOKIES:
        
        p = subprocess.Popen([AUTHTRANSPATH, request.COOKIES['galaxysession']], stdout=subprocess.PIPE,env=my_env)
#        session_key = p.stdout.read().strip()

        #use the following code in the real server, because p will have other string with respect to django log
        gsession_key = p.stdout.read().strip()
        session_key = gsession_key.split('\n')[-1]

        #session_key = SecurityHelper().decode_guid(request.COOKIES['galaxysession'])
        #sprint session_key
        try:
            galaxysession = Galaxy_session.objects.get(session_key=session_key)
            print galaxysession
            user_id = galaxysession.user_id
            user = User.objects.get(id=user_id)
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            subprocess.Popen(login(request, user))
            return HttpResponseRedirect(settings.DJANGO_DISPLAY)
        except:
            return HttpResponseRedirect(settings.LOGIN_PAGE)
    else:

        return HttpResponseRedirect(settings.LOGIN_PAGE)
'''

    
def logins(request):
    
    email= request.POST['email']
    one_month = request.POST['time'] if 'time' in request.POST else 0
    if '@' not in email:
        # username login
        email = email.replace(" ", "_")
        email = email + "@firmiana.org"
    #time.sleep(10000)
    if Experimenter.objects.filter(email=email):
        try:
            passwd_hashed=Experimenter.objects.filter(email=email)[0].password
        except Exception,e:
            temp = {}
            temp['success'] = 0
            temp['tex'] = 'Sorry, please check your email or password !'
            temp['type']=0    
            result = json.dumps(temp, cls=DjangoJSONEncoder)
            return HttpResponse(result)  
        if check_password(request.POST['password'],passwd_hashed):
            username = Experimenter.objects.filter(email=email)[0].username
            '''
            send mail to me if reviewer is online
            '''
            ip = ''
            if request.META.has_key('REMOTE_ADDR'):
                ip = request.META['REMOTE_ADDR']
            elif request.META.has_key('HTTP_X_FORWARDED_FOR'):
                ip = request.META['HTTP_X_FORWARDED_FOR']
            if username == 'Reviewer':
                mailto_list=['xiaotian_ni@icloud.com'] 
                mail_host="smtp.mxhichina.com"  
                mail_user="contact@firmiana.org"    
                mail_pass="Bprc_123"   
                mail_result = ''
                   
                def send_mail(to_list,sub,content):  
                    me= "<"+mail_user+">"
                    msg = MIMEText(content,_subtype='plain',_charset='gb2312')  
                    msg['Subject'] = sub  
                    msg['From'] = me  
                    msg['To'] = ";".join(to_list)  
                    try:  
                        server = smtplib.SMTP()  
                        server.connect(mail_host)  
                        server.login(mail_user,mail_pass)  
                        server.sendmail(me, to_list, msg.as_string())  
                        server.close()  
                        return True  
                    except Exception, e:  
                        print str(e)  
                        return False  
                send_mail(mailto_list, 'Online - ' + username, time.strftime('%Y-%m-%d %X',time.localtime(time.time())) + ' ' + ip)
                
            user=User.objects.get(username=username)
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            
            userId = user.id
            childFlag = isChildAccount(userId)
            childActive = isActive_ChildUser(userId)
                        
            login(request, user)
            #subprocess.Popen(login(request, user))
            #thread.start_new_thread(login,(request, user))
            
            if childFlag:
                if childActive:
                    temp = {}
                    m = md5()
                    m.update(username)
                    m.hexdigest() 
                    temp['success'] = 2 #child account
                    temp['name']= str(user.id)+'_'+m.hexdigest()
                    temp['tex'] = 'Child account logins successfully.'
                    temp['type']=1
                    result = json.dumps(temp, cls=DjangoJSONEncoder)
                    response = HttpResponse(result)
                    if one_month:
                        response.set_cookie('username',username,2592000)
                        #response.set_cookie('userId',userId,2592000)
                        response.set_cookie('promot',"This is a child account",2592000)
                    else:
                        response.set_cookie('username',username)
                        #response.set_cookie('userId',userId)
                        response.set_cookie('promot',"This is a child account")
                    return response
                else:
                    temp = {}
                    temp['success'] = 0
                    temp['tex'] = 'Sorry, you are a child account and are inactive.'
                    temp['type']=0  
                    result = json.dumps(temp, cls=DjangoJSONEncoder)
                    return HttpResponse(result) 
            
            
            temp = {}
            m = md5()
            m.update(username)
            m.hexdigest() 
            temp['success'] = 1 #parent account
            temp['name']= str(user.id)+'_'+m.hexdigest()
            temp['tex'] = 'Success Login.'
            temp['type']=1
            result = json.dumps(temp, cls=DjangoJSONEncoder)
            response = HttpResponse(result)
            if one_month:
                response.set_cookie('username',username,2592000)
                #response.set_cookie('userId',userId,2592000)
                response.set_cookie('promot',"This is a parent account",2592000)
            else:
                response.set_cookie('username',username)
                #response.set_cookie('userId',userId)
                response.set_cookie('promot',"This is a parent account")
            return response
                
        else:
            temp = {}
            temp['success'] = 0
            temp['tex'] = 'Sorry, please check your email or password !'
            temp['type']=0    
    else:
        temp = {}
        temp['success'] = 0
        temp['tex'] = 'Sorry, please check your email or password !'
        temp['type']=0    
    result = json.dumps(temp, cls=DjangoJSONEncoder)
    return HttpResponse(result)    
    #render_to_response( '/login_test', result)
    
def contact_post(request):
    name = request.POST['name']
    email = request.POST['email']
    text = request.POST['content']
    mailtext = email + ' ' +text  
    mailto_list=['contact@firmiana.org'] 
    mail_host="smtp.mxhichina.com"  
    mail_user="contact@firmiana.org"    
    mail_pass="Bprc_123"   
    mail_result = ''
       
    def send_mail(to_list,sub,content):  
        me= "<"+mail_user+">"
        msg = MIMEText(content,_subtype='plain',_charset='gb2312')  
        msg['Subject'] = sub  
        msg['From'] = me  
        msg['To'] = ";".join(to_list)  
        try:  
            server = smtplib.SMTP()  
            server.connect(mail_host)  
            server.login(mail_user,mail_pass)  
            server.sendmail(me, to_list, msg.as_string())  
            server.close()  
            return True  
        except Exception, e:  
            print str(e)  
            return False  
    
    if send_mail(mailto_list, 'Contact us - ' + name, mailtext):  
        return HttpResponse("Success.")
    else:  
        return HttpResponse("Failed.")
    

def register_valide(request, code):
    try:
        invitation = Invitation.objects.get(code=code)
        request.session['invitation'] = invitation.id
        return HttpResponseRedirect('/register/')
    except ObjectDoesNotExist:
        variables = RequestContext(request, {'error':'You have no permission to register'})
        return render_to_response(
                'registration/register_fail.html', variables)

def register_page(request):
    try:
#         if 'invitation' in request.session:
#             invitation = Invitation.objects.get(id=request.session['invitation'])
        if request.method == 'POST':
            
            form = RegistrationForm(request.POST)
#             print s
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password1']
                email = form.cleaned_data['email']
                company = request.POST['company']
                lab = request.POST['lab']
                lab_obj = All_Laboratory.objects.get(name=lab)
                ''' for Django register '''
                user = User.objects.create_user(
                        username=username,
                        password=password,
                        email=email
                )
                
                user_lab = User_Laboratory(
                        lab = lab_obj,
                        user_id = user.id,
                        validated = True
                )
                user_lab.save()   
                
                password = new_secure_hash(password)
                ''' for old galaxy register, we use another hash method '''
                galaxy_User = Experimenter(
                        id=user,
                        username=username,
                        email=email,
                        create_time=datetime.datetime.now(),
                        update_time=datetime.datetime.now(),
                        password=password
                        #company=company,
                        #lab=lab
                )
                galaxy_User.save()
                
#                     invitation.delete()
#                     del request.session['invitation']
                return HttpResponseRedirect(settings.LOGIN_PAGE)
            else:
                return HttpResponse("Username/Email has already been taken...")
        else:
            raise Http404
#             return render_to_response(
#                     'registration/register.html')
#         else:
#             variables = RequestContext(request, {'error':'You have no permission to register'})
#             return render_to_response(
#                     'registration/register_fail.html', variables)
    except ObjectDoesNotExist:
        raise Http404
#         try:
#             user.delete()
#         except:
#             pass
#         variables = RequestContext(request, {'error':'You have no permission to register'})
#         return HttpResponse("An error occurred, please try it later.")
        
def forgetpsd_valide(request, code):
    try:
        resetPsd = ResetPsd.objects.get(code=code)
    except ObjectDoesNotExist:
        return HttpResponse("Incorrect password reset code.")
    email = resetPsd.email
    user = Experimenter.objects.get(email=email)
    code=User.objects.make_random_password(10)
    new_password = new_secure_hash(code)
    user.password = new_password
    try:
        mailcontent = 'Your password has been reset.\nYour account ' + email + " 's new password is " + code +'. \nYou can change it after you log in to FIRMIANA. '
        send_mail('Password has been reset.', mailcontent, 'proteome.firmiana@gmail.com', [email], fail_silently=False)
    except:
        return HttpResponse("An error occurred, please try it later.")
    user.save()
    resetPsd.delete()
    return HttpResponse("Your password has been reset. Please check your mailbox.")
    
    
def forgetpsd(request):
    if request.method == 'POST':
        form = ResetPsdForm(request.POST)
        if form.is_valid():
            try:
                user = Experimenter.objects.get(email=form.cleaned_data['email'])
            except ObjectDoesNotExist:
                return HttpResponse("Your email doesn't exist.")
            resetPsd = ResetPsd(
                    email=form.cleaned_data['email'],
                    code=User.objects.make_random_password(20)
                    )
            resetPsd.save()
            resetPsd.send()
            return HttpResponse("Success! A password reset link has been send to your mailbox.")
        
#         email = request.POST['email']
#         try:
#             user = Experimenter.objects.get(email=email)
#         except ObjectDoesNotExist:
#             return HttpResponse("Your email doesn't exist.")
#         code=User.objects.make_random_password(20)
#         new_password = new_secure_hash(code)
#         user.password = new_password
#         user.save()
#         mailcontent = 'This mail is for reset your password.\nYour account ' + email + " 's new password is " + code +'.'
#         send_mail('Reset your password', mailcontent, 'proteome.firmiana@gmail.com', [email], fail_silently=False)
#         return HttpResponseRedirect(settings.LOGIN_PAGE)
    else:
        raise Http404

def register_success(request):
    return render_to_response(
        'registration/register_success.html', RequestContext(request)
    )


@login_required(login_url="/login/")
def invite(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            form = InvitationForm(request.POST)
            if form.is_valid():
                invitation = Invitation(
                        name=form.cleaned_data['name'],
                        email=form.cleaned_data['email'],
                        code=User.objects.make_random_password(20),
                        sender=request.user
                        )
                invitation.save()
                invitation.send()
                return HttpResponseRedirect('/invite/success/')
        else:
            form = InvitationForm()
        variables = RequestContext(request, {'form':form})
        return render_to_response('registration/invitation.html', variables)
    else:
        raise Http404

@login_required(login_url="/login/")
def invite_success(request):
    return render_to_response(
        'registration/invite_success.html', RequestContext(request)
    )


#@csrf_exempt
@login_required(login_url="/login/")
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data

            '''
            send_mail(subject, message, from_email, recipient_list, fail_silently=False,
            auth_user=None, auth_password=None, connection=None)
            '''
            email=ConfigSectionMap("Email")['address']
            send_mail(
                cd['subject'],
                cd['message'],
                cd.get('email', 'noreply@example.com'),
                [email],
            )

            return HttpResponseRedirect('/contact/thanks/')
    else:
        form = ContactForm(initial={'subject': 'I love your site!', 'message': 'I love your site!'})
    variables = RequestContext(request, {'form': form})
    return render_to_response('contact_form.html', variables)


def contact_success(request):
    #return HttpResponse("Thank you for your feedback!")
    return render_to_response(
        'contact_success.html', RequestContext(request))

@login_required(login_url=settings.LOGIN_PAGE)
def qiunq(request):
    if 'theme' in request.GET:
        theme = request.GET['theme'] if request.GET['theme'] in ['classic', 'access', 'gray', 'neptune'] else ''
    else:
        theme = ''
    return render_to_response('gardener/qiunq.html', {'theme':theme}) 

def entrez(request):
    return render_to_response('gardener/entrez.html',RequestContext(request))

def entrez_search(request):
    Entrez.email = "hzqnq@163.com"
    
    def Be_red(s):
        c1 = '<font color=\"#ff0000\">'
        c2 = '</font>'
        i=0
        flag = 0
        s = list(s)
        for i in range(len(s)):
            #if s[i]=='A' or s[i]=='T' or s[i]=='C' or s[i]=='G' or s[i]=='N':
            if s[i] in 'ATCGN':
                if not flag:
                    s[i] = c1 + s[i]
                    flag = 1
            else:
                if flag:
                    s[i] = c2 + s[i]
                    flag = 0
        s = ''.join(s)
        return s
        
    def myprint(seq,res,patterns):
        res += '<tt><table class=\"mytable\">'
        L = len(seq)
        c, m, i = L%120, L/120, 0
        flag = 0 if c==0 else 1
        while i < m:
            a, b = i*120, (i+1)*120
            #print '[%s]\t%s'%(a+1,seq[a:b])
            tmp =     '<tr><th>[%s]</th><td>%s</td><th>[%s]</th><td>%s</td></tr>'%(a+1, seq[a:a+60], a+61, seq[a+60:b])
            tmp = Be_red(tmp)
            res += tmp
            i+=1
        if flag:
            if c<=60:
                tmp = '<tr><th>[%s]</th><td>%s</td><th> %s </th><td>%s</td></tr>'%(i*120+1, seq[i*120:], '', '')
            else:
                tmp = '<tr><th>[%s]</th><td>%s</td><th>[%s]</th><td>%s</td></tr>'%(i*120+1, seq[i*120:i*120+60], i*120+61, seq[i*120+60:])
            tmp = Be_red(tmp)
            res += tmp
            #print '[%s]\t%s'%(i*60+1,seq[i*60:L])
        #print '======================'
        '''
        for pattern in patterns:
            tmp = pattern.upper()
            c1 = '<font color=\"#F00\">'
            c2 = '</font>'
            res = res.replace(tmp,c1 + tmp[0:1] + c2 + c1 + tmp[1:] + c2)
        '''
        res += '</table></tt>'
        return res
        
    def bigger(seq,st,ed):
        seq = list(seq)
        for i in range(0,23):
            seq[st-1+i] = seq[st-1+i].upper()
        return ''.join(seq)
    
    def get_location(regex,seq,exons,cds,res):
        patterns = set()
        nn = 0
        seq_tmp = seq
        for s in re.finditer(regex, seq):
            st = s.span()[0] + 1
            ed = s.span()[1] + 1
            if st<cds[0] or ed>cds[1]:
                continue
            if len(exons)==0:
                nn+=1
                #res += '.....' + s.group() + '(%s,%s)<br>'%(st,ed)
                #patterns.add(s.group())
                seq_tmp = bigger(seq_tmp,st,ed)
            for e in exons:
                if st>=e[0] and ed<=e[1]:
                    nn+=1
                    #patterns.add(s.group())
                    seq_tmp = bigger(seq_tmp,st,ed)
                    #res += '.....' + s.group() + '(%s,%s)<br>'%(st,ed)
                    break
        res += '<h5>##### Find %s matched patterns #####</h5>'%nn
        res = myprint(seq_tmp,res,patterns)
        
        return (res,nn)
    
    path_cache = '/usr/local/firmiana/incubator/Biopython/NCBI-nucleotide'
    
    res = "<!DOCTYPE html><html lang=\"en\"><head><meta charset=\"utf-8\">"
    #res+= "<link rel=\"stylesheet\" type=\"text/css\" href=\"/static/css/entrez_page.css\" />"
    res+= "</head><body>"
    
    db_name = 'Nucleotide'
    Orgn_name = ''#'Cypripedioideae'
    
    gene_name = request.POST['gene']#raw_input('Input Gene name:\n')#Acaca'#'matK'
    species   = request.POST['species']
    
    if species=='Mus musculus':
        txid = 10090
    elif species=='Homo sapiens':
        txid = 9606
    porgn = 'porgn:__txid%s'%txid
    
    regex1 = r'(g[\S]{20}gg)'
    regex2 = r'(cc[\S]{20}c)'
    
    num      = 10
    delta    = 0
    research = 0
    err      = 0
    seq_find = 0
    
    #html += "Term : %s[Orgn] AND %s[Gene]<br>" % (Orgn_name, gene_name)
    res += '<a id=\"top%s\"></a>'%(gene_name+species)
    
    species_tmp = '+'.join(species.split(' '))
    ncbi_url = 'http://www.ncbi.nlm.nih.gov/nuccore/?term=%s'%gene_name
    ncbi_url+= '%'+'5BGene%'+'5D+AND+%s'%species_tmp
    ncbi_url+= '%'+'5Bporgn%'+'3A__txid%s'%txid+'%5D'
        
    res += "<h3>Search Term : <a href=\"%s\" target=\"_blank\">%s[Gene] AND %s[%s]</a></h3>" % (ncbi_url, gene_name, species, porgn)
    #print 'Start search...'
    
    t1 = datetime.datetime.now()
    #exit(0)
    #handle = Entrez.esearch(db=db_name, term="%s[Orgn] AND %s[Gene]" % (Orgn_name, gene_name))
    try:
        handle = Entrez.esearch(db=db_name, term='%s[Gene] AND %s[%s]' % (gene_name, species, porgn))
    except Exception,e:
        res += '<br>URLError<br>'
        res += '</body></html>'
        #print "URLError"
        exit(0)
        HttpResponse(res)
    record = Entrez.read(handle)
    # print record["IdList"]                    
    handle.close()
    
    index = 0
    for id in record["IdList"]:
        if index >= num:
            break
        index += 1
        res += '<p>[%s]<a href=\"#%s\" target=\"_self\">\"GI|%s\"</a> (%s)</p>'%(index, id, id, gene_name)
        
    i = 0
    for id in record["IdList"]:
        if i >= num:
            break
        i += 1
        gi_ncbi_link = '<a href=\"%s\" target=\"_blank\"> \"GI|%s\" (%s)</a>'%(ncbi_url, id, gene_name)
        gotop = ' &nbsp;&nbsp;&nbsp;&nbsp;<a href=\"#top%s\" target=\"_self\">Go to top</a>'%(gene_name+species)
        res += '<br><a id=\"%s\"></a><h2>[%d] %s %s</h2>'%(id, i, gi_ncbi_link,gotop)
        
        filename = '%s/%s_%s.xml' %(path_cache, gene_name.lower(),id)
        if (not os.path.isfile(filename)) or research == 1:
            #print '\tDownloading...'
            net_handle = Entrez.efetch(db=db_name, id=id, rettype="gb", retmode="xml")
            out_handle = open(filename, "w")
            out_handle.write(net_handle.read())
            out_handle.close()
            net_handle.close()
        
        f = open(filename, "r")
        try:
            record = Entrez.read(f)
            f.close()
            #obj = Entrez.parse(record,validate=False)
            #print obj[0]
            seq = record[0]["GBSeq_sequence"]
        except Exception, e:
            f.close()
            res += '<br>.....Error when get Nucleotide sequence<br>.....continue.....<br><br>'
            err += 1
            continue
         
        flag = 1
        n=0
        key = record[0]['GBSeq_feature-table'][n]['GBFeature_key']
        while key!='CDS':
            n+=1
            try:
                key = record[0]['GBSeq_feature-table'][n]['GBFeature_key']
            except Exception,e:
                flag=-1
                break
        if flag==-1:
            res += '<br>.....Error when get CDS<br>.....continue.....<br><br>'
            continue
        #print key   
        st = record[0]['GBSeq_feature-table'][n]['GBFeature_intervals'][0]['GBInterval_from']
        ed = record[0]['GBSeq_feature-table'][n]['GBFeature_intervals'][0]['GBInterval_to']
        cds = [int(st), int(ed)]
        # seq = seq.split('\n')
        # seq = ''.join(seq)
        # print seq
        exons = []
        n = -1
        while 1:
            n+=1
            try:
                key = record[0]['GBSeq_feature-table'][n]['GBFeature_key']
            except Exception,e:
                flag = -1
                break
            if key!='exon':
                continue
            else:
                st = record[0]['GBSeq_feature-table'][n]['GBFeature_intervals'][0]['GBInterval_from']
                ed = record[0]['GBSeq_feature-table'][n]['GBFeature_intervals'][0]['GBInterval_to']
                exons.append( ( int(st), int(ed) ) )

        #exons = [ ( int(st), int(ed) ) ]
       
        exons.sort(key=lambda x:x[0])
        
        res += '<h4>CDS : %s</h4>'%cds
        
        tmp=''
        for e in exons:
            tmp += '(%s,%s),'%(e[0],e[1])
        res += '<h4>exons : %s</h4>'%tmp[:-1]
    
        res += '<h5>Pattern : [ G {N20} G G ]</h5>'
        (res,nn) = get_location(regex1,seq,exons,cds,res)
        seq_find += nn
        
        res += '<br><h5>Pattern : [ C C {N20} C ]</h5>'  
        (res,nn) = get_location(regex2,seq,exons,cds,res)
        seq_find += nn
        
    t2 = datetime.datetime.now()
    delta = float((t2 - t1).seconds) + (t2 - t1).microseconds / 1000000.0
    
    i = i - err
    tmp = 'Gene(GI)' if i<=1 else 'Genes(GI)'
    tmp2= 'Sequence' if seq_find<=1 else 'Sequences'
    res += '<h2>##### Searched %s %s and %s %s in %.3f seconds #####</h2>'%(i,tmp,seq_find,tmp2,delta)
    #tail = '<div style="width:100%; display:table; overflow:hidden; margin:0 auto; *position:relative;\">'+'<div style=\"display:table-cell; vertical-align: middle; *position:absolute; top:50%;\">'+'<div style=\"*position:relative; *top:-50%; text-align:center; width:90px; margin:0 auto;\">'+'<input id=\"uptop\" type=\"button\" value=\"Back to top\" onclick=\"scroTop()\"/></div></div></div>'
    #res += tail
    res += ' &nbsp;&nbsp;&nbsp;&nbsp;<a href=\"#top%s\" target=\"_self\">Go to top</a>'%(gene_name+species)
    res += '</body></html>'
    temp = {}
    temp['success'] = 1
    temp['text'] = res
    temp['type'] = 0    
    result = json.dumps(temp, cls=DjangoJSONEncoder)
    return HttpResponse(result)  
    
#===============================================================================
# def login_page(request):
#     '''
#     try:
#         ck = str(request.COOKIES['usercookie'])
#         id = ck.split('_')[0]
#         user = User.objects.filter(id=id)[0]
#         last_login = user.last_login
#         #logout(request)
#     except:
#         last_login = ''
#     '''
#     if "username" not in request.COOKIES :
#         logout(request)
#         return render_to_response('gardener/login_test.html')
#     
#     last_login = ''
#     ip = ''
#     
#     username = str(request.user)
#     if username=='AnonymousUser':
#         username=''
#     else:
#         last_login = request.user.last_login
#         if request.META.has_key('REMOTE_ADDR'):
#             ip = request.META['REMOTE_ADDR']
#         elif request.META.has_key('HTTP_X_FORWARDED_FOR'):
#             ip = request.META['HTTP_X_FORWARDED_FOR']
#     return render_to_response('gardener/login_test.html',RequestContext(request, {'username':username,'last_login':last_login,'ip':ip}) )
#===============================================================================

def login_page(request):
    total_exp = len( gardener_experiment.objects.filter(is_deleted = 0) )
    profiling_count = len( gardener_experiment.objects.filter(is_deleted = 0).filter(type = 'Profiling'))
    tfre_count      = len( gardener_experiment.objects.filter(is_deleted = 0).filter(bait__startswith = 'TFRE'))
    tio2_count      = len( gardener_experiment.objects.filter(is_deleted = 0).filter(bait__startswith = 'TiO2'))
    standard_count  = len( gardener_experiment.objects.filter(is_deleted = 0).filter(type = 'Standard'))
    
    human_count     = len( gardener_experiment.objects.filter(is_deleted = 0).filter(species__contains = 'Human'))
    mouse_count     = len( gardener_experiment.objects.filter(is_deleted = 0).filter(species__contains = 'Mouse'))
    frog_count      = len( gardener_experiment.objects.filter(is_deleted = 0).filter(species__contains = 'Xenopus laevis'))
    rat_count       = len( gardener_experiment.objects.filter(is_deleted = 0).filter(species__contains = 'Rat'))
    
    year2014_count       = len( gardener_experiment.objects.filter(is_deleted = 0).filter(index_date__contains = '2014'))
    year2015_count       = len( gardener_experiment.objects.filter(is_deleted = 0).filter(index_date__contains = '2015'))
    year2016_count       = len( gardener_experiment.objects.filter(is_deleted = 0).filter(index_date__contains = '2016'))
    
    qe_count        = len( gardener_experiment.objects.filter(is_deleted = 0).filter(instrument__contains = 'Q E'))
    fusion_count    = len( gardener_experiment.objects.filter(is_deleted = 0).filter(instrument__contains = 'Fusion'))
    velos_count     = len( gardener_experiment.objects.filter(is_deleted = 0).filter(instrument__contains = 'Velos'))
    ms56_count      = len( gardener_experiment.objects.filter(is_deleted = 0).filter(instrument__contains = 'Q-TOF'))
    
    if "username" not in request.COOKIES :
        logout(request)
        return render_to_response('gardener/homepageNxt/index.html',{'total_exp':total_exp,
                                                                     'profiling_count':profiling_count,
                                                                     'tfre_count':tfre_count,
                                                                     'tio2_count':tio2_count,
                                                                     'standard_count':standard_count,
                                                                     'human_count':human_count,
                                                                     'mouse_count':mouse_count,
                                                                     'frog_count':frog_count,
                                                                     'rat_count':rat_count,
                                                                     'qe_count':qe_count,
                                                                     'fusion_count':fusion_count,
                                                                     'velos_count':velos_count,
                                                                     'ms56_count':ms56_count,
                                                                     'year2014_count':year2014_count,
                                                                     'year2015_count':year2015_count,
                                                                     'year2016_count':year2016_count})

    last_login = ''
    ip = ''
    #total_exp = 0
    username = str(request.user)
    if username=='AnonymousUser':
        username=''
    else:
        last_login = request.user.last_login
        if request.META.has_key('REMOTE_ADDR'):
            ip = request.META['REMOTE_ADDR']
        elif request.META.has_key('HTTP_X_FORWARDED_FOR'):
            ip = request.META['HTTP_X_FORWARDED_FOR']
            
    '''
    send mail to me if reviewer is online
    '''
    if username == 'Reviewer':
        mailto_list=['xiaotian_ni@icloud.com'] 
        mail_host="smtp.mxhichina.com"  
        mail_user="contact@firmiana.org"    
        mail_pass="Bprc_123"   
        mail_result = ''
           
        def send_mail(to_list,sub,content):  
            me= "<"+mail_user+">"
            msg = MIMEText(content,_subtype='plain',_charset='gb2312')  
            msg['Subject'] = sub  
            msg['From'] = me  
            msg['To'] = ";".join(to_list)  
            try:  
                server = smtplib.SMTP()  
                server.connect(mail_host)  
                server.login(mail_user,mail_pass)  
                server.sendmail(me, to_list, msg.as_string())  
                server.close()  
                return True  
            except Exception, e:  
                print str(e)  
                return False  
        send_mail(mailto_list, 'Online - ' + username + ' ' + time.strftime('%Y-%m-%d %X',time.localtime(time.time())), time.strftime('%Y-%m-%d %X',time.localtime(time.time())) + ' ' + ip)
        
    return render_to_response('gardener/homepageNxt/index.html',RequestContext(request, {'total_exp':total_exp,
                                                                                         'profiling_count':profiling_count,
                                                                                         'tfre_count':tfre_count,
                                                                                         'tio2_count':tio2_count,
                                                                                         'standard_count':standard_count,
                                                                                         'human_count':human_count,
                                                                                         'mouse_count':mouse_count,
                                                                                         'frog_count':frog_count,
                                                                                         'rat_count':rat_count,
                                                                                         'qe_count':qe_count,
                                                                                         'fusion_count':fusion_count,
                                                                                         'velos_count':velos_count,
                                                                                         'ms56_count':ms56_count,
                                                                                         'year2014_count':year2014_count,
                                                                                         'year2015_count':year2015_count,
                                                                                         'year2016_count':year2016_count,
                                                                                         'username':username,
                                                                                         'last_login':last_login,
                                                                                         'ip':ip}))

def login_page_newDemo(request):
    total_exp = len( Experiment.objects.all() )    
    if "username" not in request.COOKIES :
        logout(request)
        return render_to_response('gardener/homepageQnq/index.html',{'total_exp':total_exp})
    
    last_login = ''
    ip = ''
    #total_exp = 0
    username = str(request.user)
    if username=='AnonymousUser':
        username=''
    else:
        last_login = request.user.last_login
        if request.META.has_key('REMOTE_ADDR'):
            ip = request.META['REMOTE_ADDR']
        elif request.META.has_key('HTTP_X_FORWARDED_FOR'):
            ip = request.META['HTTP_X_FORWARDED_FOR']
        
    return render_to_response('gardener/homepageQnq/index.html',RequestContext(request, {'total_exp':total_exp,'username':username,'last_login':last_login,'ip':ip}) )

class EmailThread(threading.Thread):
    def __init__(self, subject, body, from_email, recipient_list, fail_silently, html):
        self.subject = subject
        self.body = body
        self.recipient_list = recipient_list
        self.from_email = from_email
        self.fail_silently = fail_silently
        self.html = html
        threading.Thread.__init__(self)

    def run (self):
        '''
            send_mail(subject, message, from_email, recipient_list, fail_silently=False,
            auth_user=None, auth_password=None, connection=None)
        '''
        send_mail(self.subject, self.body, self.from_email, self.recipient_list, self.fail_silently)

def my_send_mail(subject, body, from_email, recipient_list, fail_silently=False, html=None, *args, **kwargs):
    EmailThread(subject, body, from_email, recipient_list, fail_silently, html).start()
    
def changepassword(request):
    username = str(request.user)
    user = Experimenter.objects.get(username=username)
    
    password_inDB = user.password
    if  check_password(request.POST['password0'],password_inDB):
        new_password = new_secure_hash(request.POST['password1'])
        user.password = new_password
        user.save()
        temp = {}
        temp['success'] = 1
        
        e_subject = 'Your password in Firmiana has changed.'
        e_message = 'New password is   ' + str(request.POST['password1'])
        my_send_mail( e_subject, e_message, settings.EMAIL_HOST_USER, [str(user.email)] ) 
        temp['tex'] = 'Successfully changed your password !'  
 
        result = json.dumps(temp, cls=DjangoJSONEncoder)    
        return HttpResponse(result)  
    #new_password = new_secure_hash(request.POST['password1'])
    temp = {}
    temp['success'] = 0
    temp['tex'] = 'Sorry, please check your password !'
    #temp['type'] = temp['tex'] = password_inDB+'_'+new_password   
    result = json.dumps(temp, cls=DjangoJSONEncoder)
    return HttpResponse(result)     

def galaxy_checkError(req):

    exp_name = req.GET['exp_name']
    instru = req.GET['instrument']
    file_name_list = []
    obj_search = gardener_search.objects.filter(exp__name=exp_name,type='fraction')
    
    for s in obj_search:
        file_name_list.append(s.name)
#     result = json.dumps(file_name_list, cls=DjangoJSONEncoder)
#     return HttpResponse(result) 
    
    if not file_name_list:
        return HttpResponse('No file names in %s'%exp_name) 
    #print file_name_list
    if '5600' in instru:
        hist_name_list = [ file_name + '.raw - QTOF5600' for file_name in file_name_list]
    else:
        hist_name_list = [ file_name + '.raw - General Workflow' for file_name in file_name_list]
        
    #print hist_name_list[:2]
    
    apikey='3c0ce871b56dbe1dd6b745144fd323bf'
    gi = GalaxyInstance(settings.GALAXY_URL, key=apikey)
    error_list = []
    for hname in hist_name_list:
        #print '# '+hname
        for history in gi.histories.get_histories(name=hname):
            hkey = history['id']
            hist = gi.histories.show_history(hkey)
            for error_key in hist['state_ids']['error']:
                error_list.append(error_key)
                #print '--error_key: '+error_key
                #tool_id = 'ms_identification_mascot'
                #res = gi.tools.run_tool(hid, tool_id, {'src':'hda','id':'c46c005a5dfa3261','store_to_db':'yes'})
                #print res
                #exit(0)
    if error_list:
        exp = gardener_experiment.objects.get(name=exp_name)
        exp.state = 'error'
        exp.save()
        return HttpResponse('Error detected in %s(count=%s)'%(exp_name,len(error_list)) )
    else:
        exp = gardener_experiment.objects.get(name=exp_name)
        exp.state = 'done'
        exp.save()
        return HttpResponse('No error in %s'%exp_name) 
            
    
def runtool(req):
    '''
    Exp000139 / tool_id = 'mascotdat_parser'
    http://61.50.134.132/runtool/?key=3c0ce871b56dbe1dd6b745144fd323bf&hid=142f6ba89946d90c&tid=mascotdat_parser
    '''
    apikey = '3c0ce871b56dbe1dd6b745144fd323bf'#req.POST['key']
    hid = req.POST['hid']
    tool_id =  req.POST['tid']
    
    gi = GalaxyInstance(settings.GALAXY_URL, key=apikey)
    res = gi.tools.run_tool(hid, tool_id, {'src':'hda','id':'c46c005a5dfa3261','store_to_db':'yes'})
    
    result = json.dumps(res, cls=DjangoJSONEncoder)
    return HttpResponse(result) 

def runworkflow(req):
    ''' 
    http://61.50.134.132/runworkflow/?key=3c0ce871b56dbe1dd6b745144fd323bf&wid=c6ef01d8a6d43836 
    Use hzqnq@163.com's api-key "3c0ce871b56dbe1dd6b745144fd323bf" 
    '''
    # wid = c6ef01d8a6d43836
    # ldda = d368c393b367e434 
    # hda = 3608c6e62163f50a
    wname = req.POST['wid']
    apikey = '3c0ce871b56dbe1dd6b745144fd323bf'#req.POST['key']
    try:
        gi = GalaxyInstance(settings.GALAXY_URL, key=apikey)
        workflows = gi.workflows.get_workflows(name=wname)
        wid = workflows[0]['id']
        wf = gi.workflows.show_workflow(wid)
        result = json.dumps(wf, cls=DjangoJSONEncoder)
        return HttpResponse(result) 

        datamap = {}
        for step_id in wf['inputs']: 
            datamap[step_id] = { 'src':'ld', 'id': 'd368c393b367e434'}
        res = gi.workflows.run_workflow(wid, datamap, history_name='New output history')

        result = json.dumps(res, cls=DjangoJSONEncoder)
        return HttpResponse(result)
    
    except:
         return HttpResponse([])

def showhistory(req):
    '''
    http://61.50.134.132/showhistory/?key=3c0ce871b56dbe1dd6b745144fd323bf&hid=142f6ba89946d90c
    '''
    result = []
    apikey = '3c0ce871b56dbe1dd6b745144fd323bf'#req.POST['key']
    hid = req.POST['hid']
    gi = GalaxyInstance(settings.GALAXY_URL, key=apikey)
    #history = gi.histories.show_history(hid)
    for history in gi.histories.get_histories(name=hid):
        hkey = history['id']
        hist = gi.histories.show_history(hkey)
        result = hist['state_ids']
        break
    
    
#     print h
#     print h['error']
#     print h['ok']
#     print h['paused']
#     print h['running']
    result = json.dumps(result, cls=DjangoJSONEncoder)
    return HttpResponse(result)  
    
def ForGalaxy(req):
    
    return render_to_response('gardener/ForGalaxy.html')

def visicount(request):
    #===========================================================================
    # try:
    #     f = open(os.path.join(settings._ROOT_PATH+'/visitor_count.txt'),'r')
    #     count = int(f.readline())
    #     f.close()
    # except:
    #     count = 0
    # count += 1
    # online_num +=1
    # if datetime.datetime.now().second == 1:
    #     f = open(os.path.join(settings._ROOT_PATH+'/visitor_count.txt'),'w')
    #     f.write(str(count))
    #     f.close()
    # data = {'v':str(count),'o':str(online_num)}    
    # result = json.dumps(data, cls=DjangoJSONEncoder)
    #===========================================================================
    return HttpResponse(1)
def developENV(req):
    return render_to_response('gardener/homepageQnq/index.html')
    return render_to_response('gardener/homepageDemo/index.html')
    return render_to_response('environment.html')

def developHomepageENV(req):
    return render_to_response('gardener/homepageDemo/indexLoginSuccess.html')
    return render_to_response('environment.html')

def continueErrWF(force, start_stage, exp_name):
    '''
    if wanna re-search mascot, use continueErrWF(2, 4, 'Exp002039')
    '''
    def _runworkflow(hid, dsid):
        ''' 
        http://61.50.134.132/runworkflow/?key=3c0ce871b56dbe1dd6b745144fd323bf&wid=c6ef01d8a6d43836 
        Use hzqnq@163.com's api-key "3c0ce871b56dbe1dd6b745144fd323bf" 
        '''
        # wid = c6ef01d8a6d43836
        # ldda = d368c393b367e434 
        # hda = 3608c6e62163f50a
        wname = wnameList[start_stage]

        try:
            gi = GalaxyInstance(settings.GALAXY_URL, key=apikey)
            workflows = gi.workflows.get_workflows(name=wname)
            wid = workflows[0]['id']
            wf = gi.workflows.show_workflow(wid)
            #result = json.dumps(wf, cls=DjangoJSONEncoder)
            #return HttpResponse(result) 
    
            datamap = {}
            for step_id in wf['inputs']: 
                datamap[step_id] = { 'src':'hda', 'id': dsid}
            res = gi.workflows.run_workflow(wid, datamap, history_id = hid)
            print res
        except:
            print 'error when _runworkflow'
            return 0
    
    # exp_name = 'Exp000973'
    # instru = 'Fusion'

    # exp_name = req.GET['exp_name']
    # instru = req.GET['instrument']
    #exp_name = 'Exp001608'
    wnameList = ['','','','start_from_mzxml','start_from_mgf']
    apikey = '3c0ce871b56dbe1dd6b745144fd323bf'#req.POST['key']
    STATE = 'error'
    stopped_stage = start_stage - 1
    
    if force==1:
        STATE = 'ok'
        start_stage = start_stage-1
    elif force==2:
        STATE = 'ok'
            
    file_name_list = []
    obj_search = gardener_search.objects.filter(exp__name=exp_name, type='fraction',stage = stopped_stage).order_by('repeat_id','fraction_id')
    
    if not obj_search:
        print 'not obj_search'
        return 0
    
    for s in obj_search:
        file_name_list.append(s.name)
    # print file_name_list
#     result = json.dumps(file_name_list, cls=DjangoJSONEncoder)
#     return HttpResponse(result) 
    
    if not file_name_list:
        return HttpResponse('No file names in %s' % exp_name) 
    # print file_name_list
        
    instru = gardener_experiment.objects.get(name=exp_name).instrument
    print 'instru=', instru
    
    if '5600' in instru:
        hist_name_list = [ file_name + '.wiff - QTOF5600' for file_name in file_name_list]
    elif '6600' in instru:
        hist_name_list = [ file_name + '.wiff - QTOF5600' for file_name in file_name_list]
    else:
        list_workflow_datasets = ['','','Raw to mzXML',        'mzXML to mgf',           'mascot_vs_',              'Mascotdat Parser']
        list_workflow_toolIDs  = ['','','ms_convert_raw2mzXML','ms_convert_mzXML2Search','ms_identification_mascot','mascotdat_parser']
        
        run_tool_name   = list_workflow_datasets[start_stage]#'mascotdat_parser' 
        input_tool_name = list_workflow_datasets[start_stage-1]
        
        run_tool_id   = list_workflow_toolIDs[start_stage]#'mascotdat_parser' 
        input_tool_id = list_workflow_toolIDs[start_stage-1]
        
        hist_name_list = [ file_name + '.raw - General Workflow' for file_name in file_name_list]
        

    gi = GalaxyInstance(settings.GALAXY_URL, key=apikey)

    #if cache==1:
    #    hist_name_list = [ hist_name_list[-1] ]
    
    #hist_name_list = ['HumanNoncodeProtein_E001608_F880_R1.raw - General Workflow']
        
    for hname in hist_name_list:
        dataset_rerun       = {}
        dataset_rerun_input = {}
        rerun_flag = 0
        print '# ' + hname
        for history in gi.histories.get_histories(name=hname):
            hid = history['id']
            print hid
            hist = gi.histories.show_history(hid, contents=True, deleted=None, visible=None, details=None, types=None)
            for dataset in hist:
                if dataset['name'].startswith(run_tool_name) and (not dataset['deleted']):
                    rerun_flag = 1 if dataset['state'] == STATE else 0
                    dataset_rerun = dataset
                if dataset['name'].startswith(input_tool_name) and (not dataset['deleted']) and dataset['state'] == 'ok':
                    dataset_rerun_input = dataset
            if rerun_flag and dataset_rerun and dataset_rerun_input:
                #print dataset_rerun
                #return 0
                
                rerun_input_datasetID = dataset_rerun_input['id']
                _runworkflow(hid, rerun_input_datasetID)
                
                #return 0
                
            else:
                print 'no need to rerun'#, hname
            # return 0
            
            
    
    
def rerunGalaxyTool(progress,cache,exp_name):
    if cache == 1:
        SINGLE = 'no'
        STATE = 'ok'
    elif cache == 2:
        SINGLE = 'yes'
        STATE = 'error'
    elif cache == 3:
        SINGLE = 'yes'
        STATE = 'ok'
    else:
        print "Wrong code"
        exit(1)
    # exp_name = 'Exp000973'
    # instru = 'Fusion'

    # exp_name = req.GET['exp_name']
    # instru = req.GET['instrument']
    file_name_list = []
    obj_search = gardener_search.objects.filter(exp__name=exp_name, type='fraction').order_by('repeat_id','fraction_id')
    
    if not obj_search:
        return 0
    
    
    for s in obj_search:
        file_name_list.append(s.name)
    # print file_name_list
#     result = json.dumps(file_name_list, cls=DjangoJSONEncoder)
#     return HttpResponse(result) 
    
    if not file_name_list:
        return HttpResponse('No file names in %s' % exp_name) 
    # print file_name_list
        
    instru = gardener_experiment.objects.get(name=exp_name).instrument
    print 'instru=', instru
    
    if '5600' in instru:
        hist_name_list = [ file_name + '.wiff - QTOF5600' for file_name in file_name_list]
    elif '6600' in instru:
        hist_name_list = [ file_name + '.wiff - QTOF5600' for file_name in file_name_list]
    else:
        list_workflow_datasets = ['','','Raw to mzXML','mzXML to mgf','mascot_vs_','Mascotdat Parser']
        list_workflow_toolIDs  = ['','','ms_convert_raw2mzXML','ms_convert_mzXML2Search','ms_identification_mascot','mascotdat_parser']
        run_tool_id   = list_workflow_toolIDs[progress]#'mascotdat_parser' 
        input_tool_id = list_workflow_toolIDs[progress-1]
        
        hist_name_list = [ file_name + '.raw - General Workflow' for file_name in file_name_list]
        
    # print hist_name_list[:2]
    #print hist_name_list
    #exit(0)
    apikey='3c0ce871b56dbe1dd6b745144fd323bf'
    gi = GalaxyInstance(settings.GALAXY_URL, key=apikey)

    if cache==1:
        hist_name_list = [ hist_name_list[-1] ]
    
    hist_name_list = ['HumanNoncodeProtein_E001608_F880_R1.raw - General Workflow']
        
    for hname in hist_name_list:
        dataset_rerun       = {}
        dataset_rerun_input = {}
        rerun_flag = 0
        print '# ' + hname
        for history in gi.histories.get_histories(name=hname):
            hid = history['id']
            print hid
            hist = gi.histories.show_history(hid, contents=True, deleted=None, visible=None, details=None, types=None)
            for dataset in hist:
                #print dataset
                #continue
            
                if dataset['name'].startswith(list_workflow_datasets[progress]) and (not dataset['deleted']):
                    rerun_flag = 1 if dataset['state'] == STATE else 0
                    dataset_rerun = dataset
                if dataset['name'].startswith(list_workflow_datasets[progress-1]) and (not dataset['deleted']) and dataset['state'] == 'ok':
                    dataset_rerun_input = dataset
            if rerun_flag and dataset_rerun and dataset_rerun_input:
                if progress == 3:
                    rerun_input_datasetID = dataset_rerun_input['id']
                    tool_inputs = {'src':'hda', 'id':rerun_input_datasetID, 'rerun_remap_job_id':'9a71f7c6b3805ca1'}       
                    res = gi.tools.run_tool(hid, run_tool_id, tool_inputs) 
                elif progress == 4:        
                    rerun_input_datasetID = dataset_rerun_input['id']
                    tool_inputs = {'src':'hda', 'id':rerun_input_datasetID, 'store_to_db':'yes'}       
                    res = gi.tools.run_tool(hid, run_tool_id, tool_inputs)
                elif progress == 5:        
                    rerun_input_datasetID = dataset_rerun_input['id']
                    tool_inputs = {'src':'hda', 'id':rerun_input_datasetID, 'store_to_db':SINGLE, 'min_ion':'0'}       
                    res = gi.tools.run_tool(hid, run_tool_id, tool_inputs)
                print res
            else:
                print 'no need to rerun'#, hname
            # return 0

def truncateExp(req):
    if not req.user.is_superuser:
        return HttpResponse('Not Superuser') 
        
    SINGLE = 'yes'
    STATE = 'error'
    exp_name = req.GET['expName']#'Exp'+exp_name
    #instru = 'Fusion'

    # exp_name = req.GET['exp_name']
    # instru = req.GET['instrument']
    file_name_list = []
    obj_search = gardener_search.objects.filter(exp__name=exp_name).order_by('repeat_id','fraction_id')
    
    if obj_search:
        for s in obj_search:
            if s.type == 'fraction':
                file_name_list.append(s.name)
                if s.num_spectrum == 0:
                    s.delete()

    # print file_name_list
    obj_exp = gardener_experiment.objects.get(name=exp_name)
        
    instru = obj_exp.instrument
    print 'instru=', instru
    
    if '5600' in instru:
        rawFileNumber = 2
        hist_name_list = [ file_name + '.wiff - QTOF5600' for file_name in file_name_list]
    elif '6600' in instru:
        rawFileNumber = 2
        hist_name_list = [ file_name + '.wiff - QTOF5600' for file_name in file_name_list]
    else:
        rawFileNumber = 1
        list_workflow_datasets = ['','','Raw to mzXML','mzXML to mgf','mascot_vs_','Mascotdat Parser']
        list_workflow_toolIDs = ['','','ms_convert_raw2mzXML','ms_convert_mzXML2Search','ms_identification_mascot','mascotdat_parser']
        #run_tool_id = list_workflow_toolIDs[progress]#'mascotdat_parser' 
        #input_tool_id = list_workflow_toolIDs[progress-1]
        
        hist_name_list = [ file_name + '.raw - General Workflow' for file_name in file_name_list]
        
    # print hist_name_list[:2]
    
    #obj_search.delete()
    #print 'Delete search table ',exp_name
    
    obj_exp.stage = 0
    obj_exp.started = 0
    obj_exp.save()
    print 'Deleted experiment table ',exp_name
    
    return HttpResponse('OK')

    apikey='3c0ce871b56dbe1dd6b745144fd323bf'
    gi = GalaxyInstance(settings.GALAXY_URL, key=apikey)

    for hname in hist_name_list:
        #print '# ' + hname
        for history in gi.histories.get_histories(name=hname):
            hid = history['id']
            #print hid
            gi.histories.delete_history(hid, purge=True)
            print hname,' deleted[',hid,']'
            #hist = gi.histories.show_history(hid, contents=True, deleted=None, visible=None, details=None, types=None)

                           
def getLocalFileList(req):
    exp_name = req.GET['exp_name']
    
    instru_full = req.GET['instru']

    format = 'raw'
    instru = 'none'
    
    if 'LTQ Orbitrap Velos' == instru_full :
        instru = "Velos"
    elif 'LTQ' == instru_full :
        instru = "LTQ"
    elif 'Fusion' == instru_full :
        instru = "Fusion"
    elif ('QExactive' == instru_full) or ('Q Exactive' == instru_full) :
        instru = "QExactive"
    elif ('Q Exactive Plus' == instru_full) or ('QExactive Plus' == instru_full) :
        instru = "QExactivePlus"
    elif '5600 Q-TOF' == instru_full :
        instru = "QTOF5600"
        format = 'wiff'
    elif '6600 Q-TOF' == instru_full:
        instru = "QTOF6600"
        format = 'wiff'
        
    file_path = os.path.join( NFS_path, 'raw_files/hzqnq@163.com',instru,exp_name[3:])
    mascot_file_path = os.path.join( NFS_path, 'mascot_result',exp_name)
    
    if not os.path.isdir(file_path):
        list_file=['no Folder in server']
    else:
        list_file = os.listdir(file_path)
    #print list_file
    if not list_file:
        list_file=['no files']
    
    data = {}
    record_list = []
    for file in list_file:
        mascotFileFolder = os.path.join(mascot_file_path, file.split(".")[0])
        mascot_file = os.listdir(mascotFileFolder) if os.path.isdir(mascotFileFolder) else []
        tmp_dict = {}
        tmp_dict['file'] = file
        tmp_dict['mascot_file'] = mascot_file[0] if mascot_file else 'None'
        record_list.append(tmp_dict)
    record_list.sort()
    data['fileList'] = record_list
    result = json.dumps(data)
    return HttpResponse(result)

    #return HttpResponse('OK')
    
def getCloudFileList(req):
    def parse_xml(input):
        list_file = []
        #print input
        try:
            #mzxmlfile = ET.parse(input)
            root = ET.fromstring(input)
        except Exception,e:
            #print e
            print 'error ET.parse(input)'
            return []
        
        #root = mzxmlfile.getroot()
        for content in root.iter('Contents'):
            #print '##############'
            filename = content.find('Key').text
            etag = content.find('ETag').text
            size = content.find('Size').text
            #print filename,etag,size
            list_file.append([filename,etag,size])
        
        return list_file
    
    exp_name = req.GET['exp_name']
    
    ID='0ulWD2N6RK5mrPAi'
    KEY = 'S1TQwAJIMyMTuzmIxI7meNoMD2iiXy'
    #oss = OssAPI("oss.aliyuncs.com", ID, KEY)
    oss = OssAPI("oss-cn-beijing.aliyuncs.com", ID, KEY)
    #bucket = 'bprc'
    bucket = 'china-data-bucket'
    #print exp_name
    res = oss.list_bucket(bucket, prefix = exp_name, marker = '', delimiter = '', maxkeys = '', headers = None)
    (status, result_xml) = res.status, res.read()
    #print result_xml
    if not result_xml:
        return HttpResponse( 'no result_xml')
    
    if status != 200:
        return HttpResponse( 'return code = %s'%status)
        
    list_file = parse_xml(result_xml)
    
    if not list_file:
        return HttpResponse( ['no files'])
    else:
        return HttpResponse( list_file )    
    
    return HttpResponse('OK')


def zddTestEntrance(request):
    '''
    try:
        ck = str(request.COOKIES['usercookie'])
        id = ck.split('_')[0]
        user = User.objects.filter(id=id)[0]
        last_login = user.last_login
        #logout(request)
    except:
        last_login = ''
    '''
    '''
    total_exp = len( Experiment.objects.all() )    
    if "username" not in request.COOKIES :
        logout(request)
        return render_to_response('gardener/homepageQnq/index.html',{'total_exp':total_exp})
    
    last_login = ''
    ip = ''
    #total_exp = 0
    username = str(request.user)
    if username=='AnonymousUser':
        username=''
    else:
        last_login = request.user.last_login
        if request.META.has_key('REMOTE_ADDR'):
            ip = request.META['REMOTE_ADDR']
        elif request.META.has_key('HTTP_X_FORWARDED_FOR'):
            ip = request.META['HTTP_X_FORWARDED_FOR']
        
    return render_to_response('gardener/homepageQnq/index.html',RequestContext(request, {'total_exp':total_exp,'username':username,'last_login':last_login,'ip':ip}) )
    '''
    
    #return render_to_response('gardener/homepageQnq/index.html')
    #return render_to_response('gardener/homepageZdd/a_frontend/index.html')
    return render_to_response('gardener/gardener.html')
    #
    #return render_to_response('api/extjsFolder/demo/index.html')

def zdd(request):
    return render_to_response('gardener/zdd.html')
