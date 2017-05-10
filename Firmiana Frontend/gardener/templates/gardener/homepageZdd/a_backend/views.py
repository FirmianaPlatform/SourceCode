#!import
import experiments.views
#from experiments.models import *
import json
from django.http import HttpResponse, Http404, HttpResponseRedirect
import gardener.views

#from api
#Metadata
from api.apiSet.metadata.metadataExperimentApi import getExpMeta
from api.apiSet.metadata.metadataSampleApi import getSamMeta
from api.apiSet.metadata.metadataReagentApi import getReaMeta
from api.apiSet.metadata.metadataExperimentDataApi import getExpDataMeta

#gar_download
from api.apiSet.gar_download.downloadDataApi import getDownloadData


#Gardener
from api.apiSet.gardener.garShowDbDataByFilterApi import getDbDataByFilter
from api.apiSet.gardener.garShowGeneDataGardenerApi import getGeneDataGardener
from api.apiSet.gardener.garShowPeptideDataGardenerApi import getPeptideDataGardener
from api.apiSet.gardener.garShowProteinDataGardenerApi import getProteinDataGardener
from api.apiSet.gardener.garShow3DplotDataApi import get3DplotDataGardener
from api.apiSet.gardener.garShow3DplotDataApiDemo import get3DplotDataGardenerDemo

#three_dim_plot
from api.apiSet.three_dim_plot.garShow3DplotDataDemoForSpecificSymbol import get3DplotDataGardenerDemoForSpecificSymbol

#Account authenticate
from api.passwordAuthenticate.password_trans import check_password

#from ppi
from api.ppi.ppiApi import getPPIData

#!function

#Metadata
#experiment
def experimentMeta(request):
    email= request.GET['email']
    if experiments.models.Experimenter.objects.filter(email=email):
        try:
            passwd_hashed=experiments.models.Experimenter.objects.filter(email=email)[0].password
        except Exception,e:
            text = 'Sorry, please check your email or password !' 
            data = {'success': False, 'data': text}
            result = json.dumps(data)
            return HttpResponse(result)
        if check_password(request.GET['password'],passwd_hashed):
            return getExpMeta(request)
        else:
            text = 'Sorry, please check your password !'
    else:
        text = 'Sorry, please check your email!'
    data = {'success': False, 'data': text}
    result = json.dumps(data)
    return HttpResponse(result)

#sample
def sampleMeta(request):
    email= request.GET['email']
    if experiments.models.Experimenter.objects.filter(email=email):
        try:
            passwd_hashed=experiments.models.Experimenter.objects.filter(email=email)[0].password
        except Exception,e:
            text = 'Sorry, please check your email or password !' 
            data = {'success': False, 'data': text}
            result = json.dumps(data)
            return HttpResponse(result)
        if check_password(request.GET['password'],passwd_hashed):
            return getSamMeta(request)
        else:
            text = 'Sorry, please check your password !'
    else:
        text = 'Sorry, please check your email!'
    data = {'success': False, 'data': text}
    result = json.dumps(data)
    return HttpResponse(result)

#reagent
def reagentMeta(request):
    email= request.GET['email']
    if experiments.models.Experimenter.objects.filter(email=email):
        try:
            passwd_hashed=experiments.models.Experimenter.objects.filter(email=email)[0].password
        except Exception,e:
            text = 'Sorry, please check your email or password !' 
            data = {'success': False, 'data': text}
            result = json.dumps(data)
            return HttpResponse(result)
        if check_password(request.GET['password'],passwd_hashed):
            return getReaMeta(request)
        else:
            text = 'Sorry, please check your password !'
    else:
        text = 'Sorry, please check your email!'
    data = {'success': False, 'data': text}
    result = json.dumps(data)
    return HttpResponse(result)

#experimentDataMeta
def experimentDataMeta(request):
    email= request.GET['email']
    if experiments.models.Experimenter.objects.filter(email=email):
        try:
            passwd_hashed=experiments.models.Experimenter.objects.filter(email=email)[0].password
        except Exception,e:
            text = 'Sorry, please check your email or password !' 
            data = {'success': False, 'data': text}
            result = json.dumps(data)
            return HttpResponse(result)
        if check_password(request.GET['password'],passwd_hashed):
            #return getExpDataMeta(request)
            responseJson = getExpDataMeta(request)
            return responseJson
        else:
            text = 'Sorry, please check your password !'
    else:
        text = 'Sorry, please check your email!'
    data = {'success': False, 'data': text}
    result = json.dumps(data)
    return HttpResponse(result)

#Gardener
#dbData by filter in gardener
def showDbDataByFilterGardener(request):
    email= request.GET['email']
    if experiments.models.Experimenter.objects.filter(email=email):
        try:
            passwd_hashed=experiments.models.Experimenter.objects.filter(email=email)[0].password
        except Exception,e:
            text = 'Sorry, please check your email or password !' 
            data = {'success': False, 'data': text}
            result = json.dumps(data)
            return HttpResponse(result)
        if check_password(request.GET['password'],passwd_hashed):
            #return getExpDataMeta(request)
            responseJson = getDbDataByFilter(request)
            return responseJson
        else:
            text = 'Sorry, please check your password !'
    else:
        text = 'Sorry, please check your email!'
    data = {'success': False, 'data': text}
    result = json.dumps(data)
    return HttpResponse(result)

#geneData in gardener
def showGeneDataGardener(request):
    print "showGeneDataGardener" + "getGeneDataGardener(request)"
    email= request.GET['email']
    if experiments.models.Experimenter.objects.filter(email=email):
        try:
            passwd_hashed=experiments.models.Experimenter.objects.filter(email=email)[0].password
        except Exception,e:
            text = 'Sorry, please check your email or password !' 
            data = {'success': False, 'data': text}
            result = json.dumps(data)
            return HttpResponse(result)
        if check_password(request.GET['password'],passwd_hashed):
            #return getExpDataMeta(request)
            responseJson = getGeneDataGardener(request)
            return responseJson
        else:
            text = 'Sorry, please check your password !'
    else:
        text = 'Sorry, please check your email!'
    data = {'success': False, 'data': text}
    result = json.dumps(data)
    return HttpResponse(result)

#peptideData in gardener
def showPeptideDataGardener(request):
    print "showPeptideDataGardener" + "getPeptideDataGardener(request)"
    email= request.GET['email']
    if experiments.models.Experimenter.objects.filter(email=email):
        try:
            passwd_hashed=experiments.models.Experimenter.objects.filter(email=email)[0].password
        except Exception,e:
            text = 'Sorry, please check your email or password !' 
            data = {'success': False, 'data': text}
            result = json.dumps(data)
            return HttpResponse(result)
        if check_password(request.GET['password'],passwd_hashed):
            #return getExpDataMeta(request)
            responseJson = getPeptideDataGardener(request)
            return responseJson
        else:
            text = 'Sorry, please check your password !'
    else:
        text = 'Sorry, please check your email!'
    data = {'success': False, 'data': text}
    result = json.dumps(data)
    return HttpResponse(result)

#proteinData in gardener
def showProteinDataGardener(request):
    print "showProteinDataGardener" + "getProteinDataGardener(request)"
    email= request.GET['email']
    if experiments.models.Experimenter.objects.filter(email=email):
        try:
            passwd_hashed=experiments.models.Experimenter.objects.filter(email=email)[0].password
        except Exception,e:
            text = 'Sorry, please check your email or password !' 
            data = {'success': False, 'data': text}
            result = json.dumps(data)
            return HttpResponse(result)
        if check_password(request.GET['password'],passwd_hashed):
            #return getExpDataMeta(request)
            responseJson = getProteinDataGardener(request)
            return responseJson
        else:
            text = 'Sorry, please check your password !'
    else:
        text = 'Sorry, please check your email!'
    data = {'success': False, 'data': text}
    result = json.dumps(data)
    return HttpResponse(result)

#show3DplotData    
def show3DplotDataGardener(request):
    print "show3DplotGardener" + "get3DplotDataGardener(request)"
    email= request.GET['email']
    if experiments.models.Experimenter.objects.filter(email=email):
        try:
            passwd_hashed=experiments.models.Experimenter.objects.filter(email=email)[0].password
        except Exception,e:
            text = 'Sorry, please check your email or password !' 
            data = {'success': False, 'data': text}
            result = json.dumps(data)
            return HttpResponse(result)
        if check_password(request.GET['password'],passwd_hashed):
            #return getExpDataMeta(request)
            responseJson = get3DplotDataGardener(request)
            return responseJson
        else:
            text = 'Sorry, please check your password !'
    else:
        text = 'Sorry, please check your email!'
    data = {'success': False, 'data': text}
    result = json.dumps(data)
    return HttpResponse(result)


#show3DplotDataGardenerDemo
def show3DplotDataGardenerDemo(request):
    print "show3DplotGardener" + "get3DplotDataGardener(request)"
    responseJson = get3DplotDataGardenerDemo(request)
    return responseJson

#show3DplotDataGardenerDemoForSpecificSymbol
def show3DplotDataGardenerDemoForSpecificSymbol(request):
    print "show3DplotGardener" + "get3DplotDataGardener(request)"
    responseJson = get3DplotDataGardenerDemoForSpecificSymbol(request)
    return responseJson


def getPPIDataDemo(request):
    print "get ppiInfomation"
    responseJson = getPPIData(request)
    return responseJson


#gar_download
def downloadData(request):
    print 'download data'
    responseJson = getDownloadData(request)
    return responseJson




#