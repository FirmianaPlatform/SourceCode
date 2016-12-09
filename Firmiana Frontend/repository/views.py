from repository.repositoryProcess import *

from django.contrib.auth.models import User

import os, sys
import getpass

# @login_required(login_url=settings.LOGIN_PAGE)
def repository(request):
    '''Jump to repository homepage.'''
    return render_to_response('repository/repository.html')

def printHelloWorld_test(request):
    '''A test function.'''
    userId = request.user.id
    data = {}
    data['msg'] = printHelloWorld(userId)
    result = json.dumps(data)
    return HttpResponse(result)


def promptJson(success, msg):
    '''Return values in JSON format'''
    data = {}
    data['success'] = success
    data['msg'] = msg
    result = json.dumps(data)
    return HttpResponse(result)

def isValidatedAccount(request):
    '''Validate whether a account accessing to Firmiana is a validated account.'''
    userId = request.user.id
    parentFlag = isParentAccount(userId)
    activeChildFlag = isActive_ChildUser(userId)
    guestFlag = isGuest(userId)
    if parentFlag or activeChildFlag or guestFlag:
        return True
    else:
        return False

def requestIsOwnerAndNotPublicated(pxdNo, request):
    '''Validate whether a project that the current account wants to access belongs to the current account
    or is in publicated status.
    '''
    aProject = ProjectOverview.objects.all().filter(pxdNo=pxdNo)
    if aProject:
        aProject = aProject[0]
        if isPublicatedProject(pxdNo):
            return False
        else:
            ownerId = aProject.user_id
            userId = request.user.id
            if ownerId==userId:
                return True
            else:
                return False
    else:
        return False
 
def parentAccess(userId, pxdNo):
    '''Validate whether a parent account wants to access to a prject not in publicated status.'''
    parentFlag = (not isGuest(userId)) and isParentAccount(userId)
    if parentFlag:
        aProject = ProjectOverview.objects.all().filter(pxdNo=pxdNo)
        if aProject:
            aProject = aProject[0]
            if isPublicatedProject(pxdNo):
                return False
            else:
                ownerId = aProject.user_id
                userId = userId
                if ownerId==userId:
                    return True
                else:
                    return False
        else:
            return False
        
    else:
        return False

def childAccess(userId, pxdNo):
    '''Validate whether a sub-account wants to access to a prject not in publicated status.'''
    childFlag = isChildAccount(userId)
    if childFlag:
        visiableProject = ChildUserAndSharedProject.objects.all().filter(child_id=userId)
        if visiableProject:
            visiableProject = visiableProject[0]
            visiableProjectNo = visiableProject.split(",")
            if pxdNo in visiableProjectNo:
                return True
            else:
                return False
        else:
            return False
    else:
        return False

def guestAccess(userId, pxdNo):
    '''Validate whether a guest account wants to access to a prject not in publicated status.'''
    if isGuest(userId) and isPublicatedProject(pxdNo):
        return True
    else:
        return False


def addAProjectRecord(request):
    '''Parent account privilege.
    Create a new project.'''
    if not isValidatedAccount(request):
        success = 0 
        msg = "You are not a validated account."
        return promptJson(success, msg)
        
    userId = request.user.id
    parentAccountFlag = isParentAccount(userId)
    if parentAccountFlag:
        parametersDict = {}
        parametersDict['projectName'] = request.GET['projectname']
        parametersDict['keywords'] = request.GET['keywords']
        parametersDict['projectDescription'] = request.GET['projectdescription']
        parametersDict['sampleProtocol'] = request.GET['sampleprotocol']
        parametersDict['dataProtocol'] = request.GET['dataprotocol']
        
        parametersDict['experimentType'] = request.GET['ExperimentType']
        parametersDict['species'] = request.GET['Species']
        parametersDict['tissue'] = request.GET['Tissue']
        parametersDict['modification'] = request.GET['Modification']
        parametersDict['instrument'] = request.GET['Instrument']
        parametersDict['cellType'] = request.GET['CellType']
        parametersDict['disease'] = request.GET['Disease']
        parametersDict['quantMethods'] = request.GET['QuantMethods']
        
        parametersDict['userName'] = request.GET['name']
        parametersDict['email'] = request.GET['email']
        parametersDict['affiliation'] = request.GET['affiliation']
        parametersDict['pubMedID'] = request.GET['pubmedID']
        parametersDict['rePXaccession'] = request.GET['rePXaccession']
        parametersDict['linkToOther'] = request.GET['linkToOther']
        try:
            aNewProjectId = addMetadataForAProject(parametersDict)
        except:
            success = 0 
            msg = "Exceptions: Add a new project metadata unsuccessfully (addMetadataForAProject)."
            return promptJson(success, msg)
        
        
        if aNewProjectId > -1:
            parametersDict['status'] = "Private"
            parametersDict['user'] = User.objects.all().get(id=userId)
            try:
                pxdNo = addANewProject(aNewProjectId, parametersDict)
                data = {}
                data['success'] = 1
                data['msg'] = "Add a new project successfully. Project Number: %s" % pxdNo
                data['pxdNo'] = pxdNo
                result = json.dumps(data)
                
                #create a folder in FTP
                currentSystemUser = getpass.getuser()
                ftpDir = "/usr/local/firmiana/firmianaFTP_userFolder"
                currentUser = User.objects.all().get(id=userId)
                email = currentUser.email
                folderName = pxdNo
                targetDir = os.path.join(ftpDir, email, folderName)
                os.mkdir(targetDir)
                os.chmod(targetDir, 0o777)
                
                return HttpResponse(result)
            except:
                aProjectDetail = ProjectDetail.objects.all().get(id=aNewProjectId)
                aProjectDetail.delete()
                aProjectOverview = ProjectOverview.objects.all().get(id=aNewProjectId)
                aProjectOverview.delete()
                success = 0 
                msg = "Exceptions: Add a new project unsuccessfully (addANewProject)."
                return promptJson(success, msg)
        else:
            success = 0 
            msg = "Add a new project metadata unsuccessfully (aNewProjectId > -1)."
            return promptJson(success, msg)        
    else:
        success = 0 
        msg = "You have no permission."
        return promptJson(success, msg)


def showAllProjectsByUserId(request):
    '''Parent account privilege.
    Show all projects under the current account.'''

    if not isValidatedAccount(request):
        success = 0 
        msg = "You are not a validated account."
        return promptJson(success, msg)
    userId = request.user.id
    allProjects_detail = showAllProjects(userId)
    if "msg" in allProjects_detail:
        success = 0
        msg = allProjects_detail["msg"]
        return promptJson(success, msg)
    else:
        data = {}
        data['success'] = 1
        data['msg'] = "show all projects of %s" % request.user.username
        data['data'] = allProjects_detail
        result = json.dumps(data)
        return HttpResponse(result)
    

def getProjectStatus(request):
    '''Get status of a project.'''
    if not isValidatedAccount(request):
        success = 0 
        msg = "You are not a validated account."
        return promptJson(success, msg)
    pxdNo = request.GET["pxdNo"]
    userId = request.user.id
    accessFlag = parentAccess(userId, pxdNo) or childAccess(userId, pxdNo) or guestAccess(userId, pxdNo)
    if not accessFlag:
        success = 0
        msg = "You have no permission."
        return promptJson(success, msg)
    try:
        aProject = ProjectOverview.objects.all().filter(pxdNo=pxdNo)[0]
        status = aProject.status.status
        data = {}
        data['success'] = 1
        data['msg'] = "%s status is %s" % (pxdNo, status)
        data['status'] = status
        result = json.dumps(data)
        return HttpResponse(result)
    except:
        success = 0
        msg = "Exception occurs in getProjectStatus."
        return promptJson(success, msg)

def changeProjectStatus_views(request):
    '''Parent account privilege.
    Change status of a project.'''
    if not isValidatedAccount(request):
        success = 0 
        msg = "You are not a validated account."
        return promptJson(success, msg)
    pxdNo = request.GET["pxdNo"]
    status = request.GET["status"]
    userId = request.user.id
    accessFlag = parentAccess(userId, pxdNo)
    if not accessFlag:
        success = 0 
        msg = "You have no permission."
        return promptJson(success, msg)
    changeFlag = changeProjectStatus(pxdNo, status)
    if changeFlag:
        success = 1
        msg = "The status of %s turn into %s." % (pxdNo, status)
        return promptJson(success, msg)
    else:
        success = 0
        msg = "The status of %s changed unsuccessfully." % (pxdNo)
        return promptJson(success, msg)
        
def showMetadataByPxdNo_views(request):
    '''Show metadata of a project.'''
    if not isValidatedAccount(request):
        success = 0 
        msg = "You are not a validated account."
        return promptJson(success, msg)
    pxdNo = request.GET["pxdNo"]
    
    userId = request.user.id
    accessFlag = parentAccess(userId, pxdNo) or childAccess(userId, pxdNo) or guestAccess(userId, pxdNo)
    if not accessFlag:
        success = 0
        msg = "You have no permission."
        return promptJson(success, msg)
    
    parametersDict = showMetadataByPxdNo(pxdNo)
    if "error" not in parametersDict:
        data = {}
        data['success'] = 1
        data['msg'] = "Show metadata of %s" % (pxdNo)
        data['data'] = parametersDict
        result = json.dumps(data)
        return HttpResponse(result)
    else:
        success = 0
        msg = "Error occurs"
        return promptJson(success, msg)

def updateMetadataForAProject_views(request):
    '''Update metadata of a project.'''
    if not isValidatedAccount(request):
        success = 0 
        msg = "You are not a validated account."
        return promptJson(success, msg)
    
    userId = request.user.id
    pxdNo = request.GET['pxdNo']
    accessFlag = parentAccess(userId, pxdNo)
    if not accessFlag:
        success = 0
        msg = "You have no permission."
        return promptJson(success, msg)
    if accessFlag:
        parametersDict = {}
        
        parametersDict['pxdNo'] = request.GET['pxdNo']
        
        parametersDict['projectName'] = request.GET['projectname']
        parametersDict['keywords'] = request.GET['keywords']
        parametersDict['projectDescription'] = request.GET['projectdescription']
        parametersDict['sampleProtocol'] = request.GET['sampleprotocol']
        parametersDict['dataProtocol'] = request.GET['dataprotocol']
        
        parametersDict['experimentType'] = request.GET['ExperimentType']
        parametersDict['species'] = request.GET['Species']
        parametersDict['tissue'] = request.GET['Tissue']
        parametersDict['modification'] = request.GET['Modification']
        parametersDict['instrument'] = request.GET['Instrument']
        parametersDict['cellType'] = request.GET['CellType']
        parametersDict['disease'] = request.GET['Disease']
        parametersDict['quantMethods'] = request.GET['QuantMethods']
        
        parametersDict['userName'] = request.GET['name']
        parametersDict['email'] = request.GET['email']
        parametersDict['affiliation'] = request.GET['affiliation']
        parametersDict['pubMedID'] = request.GET['pubmedID']
        parametersDict['rePXaccession'] = request.GET['rePXaccession']
        parametersDict['linkToOther'] = request.GET['linkToOther']
        updateFlag = updateMetadataForAProject(parametersDict)
        if updateFlag:
            success = 1
            msg = "Update metadata successfully."
            return promptJson(success, msg)
        else:
            success = 0
            msg = "You have no permission."
            return promptJson(success, msg)
    else:
        success = 0
        msg = "You have no permission."
        return promptJson(success, msg)

def showAllChildAccountInfo_inRepository_views(request):
    '''Parent account privilege.
    Show all sub-account information.
    '''
    if not isValidatedAccount(request):
        success = 0 
        msg = "You are not a validated account."
        return promptJson(success, msg)
    userId = request.user.id
    parentFlag = isParentAccount(userId)
    if parentFlag:
        parentId = userId
        jsonResult = showAllChildAccountInfo_inRepository(parentId)
        return HttpResponse(jsonResult)
    else:
        success = 0
        msg = "You have no permission."
        return promptJson(success, msg)

def addChildUserSharedProject_views(request):
    '''Parent account privilege.
    Share projects to sub-account.
    '''
    if not isValidatedAccount(request):
        success = 0 
        msg = "You are not a validated account."
        return promptJson(success, msg)
    userId = request.user.id
    parentFlag = isParentAccount(userId)
    if parentFlag:
        childName = request.GET['childName']
        sharedProject = request.GET['sharedProject']
        addSharedProjectFlag = addChildUserSharedProject(userId, childName, sharedProject)
        if addSharedProjectFlag:
            success = 1
            msg = "Share projects to child account successfully."
            return promptJson(success, msg)
        else:
            success = 0
            msg = "Having a project or more project does not belong to you or some exceptions occurs! "
            return promptJson(success, msg)
    else:
        success = 0
        msg = "You have no permission."
        return promptJson(success, msg)
        
def updateChildAccountSharedProject_views(request):
    '''Parent account privilege.
    Update shared projects with sub-account.
    '''
    if not isValidatedAccount(request):
        success = 0 
        msg = "You are not a validated account."
        return promptJson(success, msg)
    userId = request.user.id
    parentFlag = isParentAccount(userId)
    if parentFlag:
        childName = request.GET['childName']
        sharedProject = request.GET['sharedProject']
        updateSharedProjectFlag = updateChildAccountSharedProject(childName, sharedProject)
        if updateSharedProjectFlag:
            success = 1
            msg = "Update shared projects to child account successfully."
            return promptJson(success, msg)
        else:
            success = 0
            msg = "Update shared projects to child account unsuccessfully."
            return promptJson(success, msg)
    else:
        success = 0
        msg = "You have no permission."
        return promptJson(success, msg)

def deleteAProjectRecord(request):
    '''Parent account privilege.
    Delete a Project
    '''
    userId = request.user.id
    parentAccountFlag = isParentAccount(userId)
    if parentAccountFlag:
        parametersDict = {}
        pxdNo = request.GET['pxdNo']
        deleteFlag = deleteAProject(userId, pxdNo)
        if deleteFlag:
            success = 1
            msg = "Delete a project successfully."
            return promptJson(success, msg)
        else:
            success = 0 
            msg = "Delete a project unsuccessfully.."
            return promptJson(success, msg)
    else:
        success = 0 
        msg = "You have no permission."
        return promptJson(success, msg)



def record_display(request, model_name):
    '''Show information of a specific model according to model name'''
    
    data = {}
    model = eval(model_name)
    if model_name == "Miape_ExpType":
        common_records = model.objects.filter(validated=True)
    elif model_name == "Miape_Species":
        common_records = model.objects.filter(validated=True)
    elif model_name == "Miape_Tissue":
        common_records = model.objects.filter(validated=True)
    elif model_name == "Miape_Modification":
        common_records = model.objects.filter(validated=True)
    elif model_name == "Miape_Instrument":
        common_records = model.objects.filter(validated=True)
    elif model_name == "Miape_CellType":
        common_records = model.objects.filter(validated=True)
    elif model_name == "Miape_Disease":
        common_records = model.objects.filter(validated=True)
    elif model_name == "Miape_QuantMethod":
        common_records = model.objects.filter(validated=True)
    else:
        common_records = []
        
    record_list = []
    for record in common_records:
        tmp_dict = {}
        tmp_dict[model_name] = record.name
        record_list.append(tmp_dict)
    if model_name[0:5] != "Miape":
        record_list.sort()
    data[model_name + 's'] = record_list
    result = json.dumps(data)
    return HttpResponse(result)





