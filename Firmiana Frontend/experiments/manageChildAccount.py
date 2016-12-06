"""manageChildAccount.py -- this module is used for process the event that a parent account add an own child account """

from django.http import StreamingHttpResponse

from experiments.views import *
from gardener.views import *
#from leafy.views import *
from leafy.models import *

from django.utils import timezone

from gardener.models import Experiment as gard_experiment
from experiments.models import User_Laboratory as exp_User_Laboratory

import re

rawFilesPathInFirmiana = '/usr/local/firmiana/'


def promptJson(success, prompt):
    '''
    The funtion is used for outputing prompt in json format.
    '''
    temp = {}
    temp['success'] = success
    temp['text'] = prompt
    result = json.dumps(temp, cls=DjangoJSONEncoder)
    return result


def validateEmail(email):

    if len(email) > 7:
        if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) != None:
            return True
    return False


'''parent perimission'''
def addChildAccount(username, password, annotation):
    '''
    Register a child account.
    '''
    if validateEmail(username):
        email = username
    else:
        email = username.replace(" ", "_")
        email = email + '@firmiana.org'
    #insert record into auth_user
    user_child = User.objects.create_user(
                        username=username,
                        password=password,
                        email=email
                ) 
    
    #insert record into galaxy_user
    password = new_secure_hash(password)
    galaxy_user_child = Experimenter(
            id=user_child,
            username=username,
            email=email,
            create_time=timezone.now(),
            update_time=timezone.now(),
            password=password
    )
    galaxy_user_child.save()
    
    
    #insert record into auth_child_user
    child_username = username
    child_password = password
    child_email = email
    child_last_login = timezone.now() #datetime.datetime.strptime("2016-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")
    child_date_joined = timezone.now()
    child_is_active = True
    newChildUser = AuthChildUser(id = user_child,
                                 child_username=child_username,
                                 child_password=child_password,
                                 child_email = child_email,
                                 child_last_login=child_last_login,
                                 child_date_joined=child_date_joined,
                                 child_is_active=child_is_active,
                                 child_annotation=annotation
                                 )
    newChildUser.save()
    return newChildUser

def activateChildAccount(childName):
    '''
    Activate child account, make it be in active.
    c = a if a>b else b
    '''
    activateFlag = False
    try:
        child = AuthChildUser.objects.all().get(child_username=childName)
        child.child_is_active = True
        child.save()
        activateFlag = True
    except:
        activateFlag = False
    return activateFlag

def freezeChildAccount(childName):
    '''
    Freeze child account, make it be inactive.
    c = a if a>b else b
    '''
    freezeFlag = False
    try:
        child = AuthChildUser.objects.all().filter(child_username=childName)[0]
        child.child_is_active = False
        child.save()
        freezeFlag = True
    except:
        freezeFlag = False
    return freezeFlag

def deleteChildAccount(parentId, childName):
    ''''
    Delete child account.
    '''
    deleteFlag = False
    try:
        '''Child manager table'''
        parent = User.objects.all().get(id=parentId)
        auth_child = AuthChildUser.objects.all().get(child_username=childName)
        parentChildAssociation = AuthParentChildAssociation.objects.all().get(parent=parent,child=auth_child)
        childSharedExp = AuthChildUserAndSharedExp.objects.all().get(child=auth_child)
        parentChildAssociation.delete()
        childSharedExp.delete()
        auth_child.delete()
        
        '''System manager table'''
        galaxy_child = Experimenter.objects.all().get(username=childName)
        galaxy_child.delete()
        user_child = User.objects.all().get(username=childName)
        user_child.delete()
        
        deleteFlag = True

    except:
        deleteFlag = False
    return deleteFlag    
    
    
def addParentAndChildAssocitions(parentId, childUser):
    '''
    After creating child account, bulid parent and child account associations.
    '''
    #parent = AuthUser.objects.all().filter(email=email)[0]
    parent = User.objects.all().filter(id=parentId)[0]
    child = childUser
    parentChildAssociation = AuthParentChildAssociation(parent=parent,child=child)
    parentChildAssociation.save()
    return parentChildAssociation.id


def addChildUserSharedExp(childName, shareExp):
    '''
    Parent account share specific experiments to child account.
    '''
    #shareExp = "Exp007407,Exp0074078,Exp007409"
    addSharedExpFlag = False
    if shareExp == "":
        shareExp = ""
    else:
        shareExpList = shareExp.split(",")
        child = AuthChildUser.objects.all().get(child_username=childName)
        parentAndChild = AuthParentChildAssociation.objects.all().get(child=child)
        parentId = parentAndChild.parent.id
        user = User.objects.all().get(id=parentId)
        pass
    
    
    try:
        child = AuthChildUser.objects.all().get(child_username=childName)
        isActive = True
        newChildUserSharedExp = AuthChildUserAndSharedExp(child=child,
                                                          sharedExp=shareExp,
                                                          isActive=isActive
                                                          )
        newChildUserSharedExp.save()
        addSharedExpFlag = True
    except:
        addSharedExpFlag = False
    return addSharedExpFlag

def updateChildAccountSharedExp(childName, shareExp):
    '''
    Parent account updates experiments list for sharing to child account.
    '''
    updateSharedExpFlag = False
    try:
        child = AuthChildUser.objects.all().filter(child_username=childName, child_is_active=True)[0]
        childUserSharedExp = AuthChildUserAndSharedExp.objects.all().filter(child=child)
        if childUserSharedExp:
            childUserSharedExp = childUserSharedExp[0]
            childUserSharedExp.sharedExp = shareExp
            childUserSharedExp.save()
            updateSharedExpFlag = True
        else:
            updateSharedExpFlag = False
    except:
        updateSharedExpFlag = False
    return updateSharedExpFlag

def showAllChildAccountInfo(parentId): #return jsonResult
    '''
    Parent account gets own child account via parent id.
    '''
    parent = User.objects.all().get(id=parentId)
    childs = AuthParentChildAssociation.objects.all().filter(parent=parent)
    
    childs_username = []
    childs_isActive = []
    childs_annotation = []
    childs_sharedExpList = []

    tmpDataList = []
    if childs:
        for child in childs:
            childInstance = AuthChildUser.objects.all().filter(id=child.child_id)
            childInstance = childInstance[0]
            childs_username.append(childInstance.child_username)
            childs_isActive.append(childInstance.child_is_active)
            childs_annotation.append(childInstance.child_annotation)
            child_sharedExpList = AuthChildUserAndSharedExp.objects.all().get(child=childInstance)
            childs_sharedExpList.append(child_sharedExpList.sharedExp)
            tmpData = {}
            tmpData['childs_username'] = childInstance.child_username
            tmpData['childs_isActive'] = childInstance.child_is_active
            tmpData['childs_annotation'] = childInstance.child_annotation
            tmpData['childs_sharedExpList'] = child_sharedExpList.sharedExp
            tmpDataList.append(tmpData)
            
        success = 1
        prompt = "Load all sub-accounts belonging to the parent account."
    else:
        success = 0
        prompt = "The parent account has no sub-accounts."
    
    temp = {}
    temp['success'] = success
    temp['msg'] = prompt
    temp['data'] = tmpDataList
    jsonResult = json.dumps(temp)
    return jsonResult
'''parent perimission'''



'''validate account'''
def childHasExistedByID(userId):
    '''
    Verify whether that child user exists in the database.
    '''
    childUser = AuthChildUser.objects.all().filter(id=userId)
    if childUser:
        return True
    else:
        return False

def childHasExistedByName(childName):
    '''
    Verify whether that child user exists in the database.
    '''
    childUser = AuthChildUser.objects.all().filter(child_username=childName, child_is_active=True)
    if childUser:
        return True
    else:
        return False

# Child account verification 1
def isChildAccount(userId):
    '''
    Verify whether that child account exists in the database
    When the child account exists in the database, the function will return a 'True'
    Otherwisr, the retuen value is assigned 'False'
    '''
    childUser = AuthChildUser.objects.all().filter(id=userId)
    if childUser:
        return True
    else:
        return False
# Guest
def isGuest(userId):
    guest = User.objects.all().filter(id=userId)
    if guest:
        guest = guest[0]
        if guest.username == "Guest":
            return True
        else:
            return False
    else:
        return False

# Child account verification 2
def isActive_ChildUser(userId):
    '''
    Verify whether that parent account is active.
    When the child account is in active, the function will return a 'True'.
    Otherwisr, the retuen value is assigned 'False'.
    '''
    childUser = AuthChildUser.objects.all().filter(id=userId)
    if childUser:
        childUser = childUser[0]
        if childUser.child_is_active:
            return True
        else:
            return False
    else:
        return False
    

def isParentAccount(userId):
    '''
    Verify whether that parent account exists in the database.
    When the child account exists in the database, the function will return a 'True'.
    Otherwisr, the retuen value is assigned 'False'.
    '''
    childFlag = isChildAccount(userId)
    if childFlag:
        return False
    parent = User.objects.all().filter(id=userId)
    if parent:
        return True
    else:
        return False
    
def isValidatedUser(userId):
    '''
    Verify whether that the current account is validated.
    When the account is validated, the function will return a 'True'.
    Otherwisr, the retuen value is assigned 'False'.
    '''
    parentFlag = isParentAccount(userId)
    childFlag = isChildAccount(userId)
    childActive = isActive_ChildUser(userId)
    if parentFlag:
        return True
    elif childFlag and childActive:
        return True
    else:
        return False
'''validate account'''



def showVisibleExperiments_gardenerExperiment(userId): #return visibleExpList
    '''
    The function allows user who is authorized to view the corresponding experiments.
    '''
    childFlag = isChildAccount(userId)
    parentFlag = isParentAccount(userId)
    visibleExpList = []
    if childFlag:
        childId = userId
        #existedFlag = childHasExistedByID(childId)
        isActiveFlag = isActive_ChildUser(childId)
        if isActiveFlag:
            sharedExp = AuthChildUserAndSharedExp.objects.all().get(child_id=childId)
            sharedExpList = sharedExp.sharedExp.split(",")
            for expName in sharedExpList:
                expInstance = gard_experiment.objects.all().filter(name=expName)
                if expInstance:
                    visibleExpList.append(expInstance[0])
                else:
                    tmpStr = "%s is not found." % expName
                    visibleExpList.append(tmpStr)
            success = 1
            prompt = "Load visiable experiments list successfully." 
        else:
            success = 0 
            prompt = "The sub-account is inactive." 
    elif parentFlag:
        parentId = userId
        lab = User_Laboratory.objects.filter(user=parentId)
        lab = lab[0].lab.name if lab.count() else ''
        visibleExpList = gard_experiment.objects.filter(lab=lab).filter(is_deleted=0)
        success = 1
        prompt = "Load visiable experiments list successfully." 
    else:
        success = 0
        prompt = "The user does not exist."
    
    return visibleExpList

def showExperiments_ViewRawFiles(userId): #return jsonResult
    '''
    The function is used for viewing raw files list of a specific experiment.
    '''
    childFlag = isChildAccount(userId)
    parentFlag = isParentAccount(userId)
    visibleExpList = []
    if childFlag:
        childId = userId
        #existedFlag = childHasExistedByID(childId)
        isActiveFlag = isActive_ChildUser(childId)
        if isActiveFlag:
            sharedExp = AuthChildUserAndSharedExp.objects.all().get(child_id=childId)
            sharedExpList = sharedExp.sharedExp.split(",")
            visibleExpList = sharedExpList
            success = 1
            prompt = "Load visiable experiments name list successfully." 
        else:
            success = 0 
            prompt = "The sub-account is inactive." 
    elif parentFlag:
        parentId = userId
        lab = User_Laboratory.objects.filter(user=parentId)
        lab = lab[0].lab.name if lab.count() else ''
        experiments_list = gard_experiment.objects.filter(lab=lab).filter(is_deleted=0)
        for exp in experiments_list:
            visibleExpList.append(exp.name)
        success = 1
        prompt = "Load visiable experiments name list successfully." 
    else:
        success = 0
        prompt = "The user does not exist."
    
    tmpDataList = []
    if visibleExpList:
        for exp in visibleExpList:
            tmpDataDict = {}
            tmpDataDict["expName"] = exp
            tmpDataList.append(tmpDataDict)
    else:
        success = 1
        prompt = "The visiable experiments is null."
    
    temp = {}
    temp['success'] = success
    temp['text'] = prompt
    temp['visibleExpList'] = tmpDataList
    jsonResult = json.dumps(temp, cls=DjangoJSONEncoder)
    return jsonResult
    
    
def showRawFileListByExpName(expName):
    '''
    The function allows user to get raw files list of a specific experiment via its name.
    '''
    #expName = 'Exp001925'
    exp = gard_experiment.objects.all().filter(name=expName)
    list_file = []
    if exp:
        exp = exp[0]
        instrument = exp.instrument
    
        exp_name = expName
        instru_full = instrument

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
        elif 'Q Exactive HF' == instru_full :
            instru = "QExactiveHF"
        elif 'Fusion Lumos' == instru_full :
            instru = "FusionLumos"
        elif '5600 Q-TOF' == instru_full :
            instru = "QTOF5600"
            format = 'wiff'
        elif '6600 Q-TOF' == instru_full:
            instru = "QTOF6600"
            format = 'wiff'
            
        file_path = os.path.join(rawFilesPathInFirmiana, 'raw_files', instru, exp_name[3:])
        
        if not os.path.isdir(file_path):
            list_file=['no Folder in server']
        else:
            list_file = os.listdir(file_path)
        #print list_file
        if not list_file:
            list_file=['no files']

        list_file.sort()
    list_fileSize = []
    for fileName in list_file:
        tmpAbsPath = os.path.join(file_path, fileName)
        tmpFileSize = os.path.getsize(tmpAbsPath)*1.0/1024/1024
        tmpFileSizeMB = '%.2f MB' %(tmpFileSize) 
        list_fileSize.append(tmpFileSizeMB)
    
    tempData_file_list = []
    fileCount = len(list_file)
    if fileCount>0:
        for i in range(0,fileCount):
            tempData_file_dict = {}
            fileName = list_file[i]
            fileSize = list_fileSize[i]
            tempData_file_dict["fileName"] = fileName
            tempData_file_dict["fileSize"] = fileSize
            tempData_file_list.append(tempData_file_dict)
    

    
    tmp = {}
    tmp['success'] = 1
    tmp['expName'] = expName
    tmp["rawFiles"] = tempData_file_list
    jsonResult = json.dumps(tmp)
    return jsonResult

def showAbsPath_Exp_RawFile(expName, fileName):
    '''
    The function allows user to get the absolute path of a raw file via the corresponding experiment name and raw file name.
    '''
    #expName = 'Exp001925'
    #fileName = "81841_5ug_UHRF2_Ab_IP_2mg_MKN45_OE_NE_SDS_PAGE_band1_100per_loading_F1_R1.raw"
    exp = gard_experiment.objects.all().filter(name=expName)
    if exp:
        exp = exp[0]
        instrument = exp.instrument
    
        exp_name = expName
        instru_full = instrument

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
        elif 'Q Exactive HF' == instru_full :
            instru = "QExactiveHF"
        elif 'Fusion Lumos' == instru_full :
            instru = "FusionLumos"
        elif '5600 Q-TOF' == instru_full :
            instru = "QTOF5600"
            format = 'wiff'
        elif '6600 Q-TOF' == instru_full:
            instru = "QTOF6600"
            format = 'wiff'
        file_path = os.path.join(rawFilesPathInFirmiana, 'raw_files', instru, exp_name[3:])
        file_abs_path = os.path.join(file_path, fileName)
        if not os.path.isfile(file_abs_path):
            file_abs_path = "Not Found"
    return file_abs_path

def bigFileView(filePath):
    '''
    Download a big file via http protocol.
    '''
    def readFile(fn, buf_size=262144):
        f = open(fn, "rb")
        while True:
            c = f.read(buf_size)
            if c:
                yield c
            else:
                break
        f.close()
    #file_name = "big_file.txt"    
    HttpResponse(readFile(filePath))

def big_file_download(request):
    '''
    Download a big file via http protocol.
    '''
    def file_iterator(file_name, chunk_size=512):
        with open(file_name) as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break

    the_file_name = "big_file.pdf"
    response = StreamingHttpResponse(file_iterator(the_file_name))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(the_file_name)

    return response

def publicExperiments(userId, publicedExp):
    parentFlag = isParentAccount(userId)
    expNameList = publicedExp.split(",")
    try:
        if parentFlag:
            parent = User.objects.all().get(id=userId)
            username = parent.username
            for expName in expNameList:
                newPublicExperiment = PublicExperiments(expName=expName,
                                                         isPublic=True,
                                                         owner=username
                                                         )
                newPublicExperiment.save()
            success = 1 
            msg = "Your data are in public."
            data = {}
            data['success'] = success
            data['msg'] = msg
            result = json.dumps(data)    
        else:
            success = 0 
            msg = "You have no permission."
            data = {}
            data['success'] = success
            data['msg'] = msg
            result = json.dumps(data)
    except:
        success = 0 
        msg = "Exception occurs."
        data = {}
        data['success'] = success
        data['msg'] = msg
        result = json.dumps(data)
    return result


def __main__():
    
    '''
    Debug the correspongding  fucntions
    '''
    #user=request.user
    parentId = 14
    #childId = 77
    #shareExp = "Exp007407,Exp0074078,Exp007409"
    
    username = "Zhan Dongdong"
    password = "123456"
    annotation = "Reviewer"
    childUser = addChildAccount(username, password, annotation)
    parentChildAssociationId = addParentAndChildAssocitions(parentId, childUser)
    shareExp = "Exp007407,Exp007408,Exp007409"
    childName = username
    addChildUserSharedExp(childName, shareExp)
    
    username = "Zhang San"
    password = "1234567"
    annotation = "Student"
    childUser = addChildAccount(username, password, annotation)
    parentChildAssociationId = addParentAndChildAssocitions(parentId, childUser)
    shareExp = "Exp007407,Exp0074078,Exp007409,Exp007410,Exp007411"
    childName = username
    addChildUserSharedExp(childName, shareExp)
    
    username = "Li Si"
    password = "12345678"
    annotation = "Partner"
    childUser = addChildAccount(username, password, annotation)
    parentChildAssociationId = addParentAndChildAssocitions(parentId, childUser)
    shareExp = "Exp007407,Exp007410,Exp007411"
    childName = username
    addChildUserSharedExp(childName, shareExp)

    




