import math
import json
import datetime
import csv
import os
import zipfile
import tempfile
import numpy as np
import numpy
import random
import time
import commands
import sys
import re

from numpy.lib import recfunctions as rfn
from datetime import timedelta
from django.utils import timezone 
from django.core.servers.basehttp import FileWrapper
from django.db import connection
from django.db.models import Q
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.shortcuts import render
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.decorators import login_required
from django.conf import settings

from numpy import array, repeat, concatenate, ones, zeros, arange, reshape, put, add, dot, take, float32
from numpy.linalg import pinv
from scipy.signal.signaltools import lfilter
import multiprocessing
from multiprocessing import Process, Manager, Pool
from rpy2 import robjects as ro
from rpy2.robjects.packages import importr

from repository.models import *

from experiments.models import AuthChildUser, AuthParentChildAssociation

from experiments.views import isActive_ChildUser, isChildAccount, isGuest, isParentAccount, isValidatedUser



''' test function'''
def printHelloWorld(userId):
    if isGuest(userId):
        return 'Hello, world! Guest account.'
    elif isActive_ChildUser(userId):
        return 'Hello, world! Child account.'
    elif isParentAccount(userId):
        return 'Hello, world! Parent account.'
    else:
        return 'Hello, world!'
    

''' validate whether a project belongs to a user'''
def projectBelongsToUser(userId, pxdNo):
    allProjects = ProjectOverview.objects.all().filter(user_id = userId).filter(validated=True)
    allProjectsName = []
    for project in allProjects:
        allProjectsName.append(project.pxdNo)
    if pxdNo in allProjectsName:
        return True
    else:
        return False
        


''' add metadata of specific project '''
'''
parent permission
'''
def addMetadataForAProject(parametersDict):
    '''
    Insert a new record into ProjectDetail
    '''
    try:
        projects = ProjectOverview.objects.all()
        if projects.count()==0:
            newPxdNo = "FNO" + "000001"
        else:
            pxdNolist = []
            for project in projects:
                pxdNolist.append(project.pxdNo)
            pxdNolist.sort(cmp=None, key=None, reverse=True)
            currentPxdNo = pxdNolist[0].split("FNO")
            currentPxdNo_value = int(currentPxdNo[1])
            newPxdNo_value = str(currentPxdNo_value + 1)
            newPxdNo = "FNO" + "0"*(6-len(newPxdNo_value))+ newPxdNo_value
        pxdNo = newPxdNo
        
        projectName = parametersDict['projectName']
        keywords = parametersDict['keywords']
        projectDescription = parametersDict['projectDescription']
        sampleProtocol = parametersDict['sampleProtocol']
        dataProtocol = parametersDict['dataProtocol']
        
        
        
        experimentType = Miape_ExpType.objects.all().get(name=parametersDict['experimentType'])
        species = Miape_Species.objects.all().get(name=parametersDict['species'])
        tissue = Miape_Tissue.objects.all().get(name=parametersDict['tissue'])
        modification = Miape_Modification.objects.all().get(name=parametersDict['modification'])
        instrument = Miape_Instrument.objects.all().get(name=parametersDict['instrument'])
        cellType = Miape_CellType.objects.all().get(name=parametersDict['cellType'])
        disease = Miape_Disease.objects.all().get(name=parametersDict['disease'])
        quantMethods = Miape_QuantMethod.objects.all().get(name=parametersDict['quantMethods'])
        
        
        
        userName = parametersDict['userName']
        email = parametersDict['email']
        affiliation = parametersDict['affiliation']
        pubMedID = parametersDict['pubMedID']
        rePXaccession = parametersDict['rePXaccession']
        linkToOther = parametersDict['linkToOther']
        
        createTime = timezone.now()
        
        aNewProjectDetail = ProjectDetail(
                                          pxdNo = pxdNo,
                                          projectName = projectName,
                                          keywords = keywords,
                                          projectDescription = projectDescription,
                                          sampleProtocol = sampleProtocol,
                                          dataProtocol = dataProtocol,
                                          experimentType = experimentType,
                                          species = species,
                                          tissue = tissue,
                                          
                                          modification = modification,
                                          
                                          instrument = instrument,
                                          cellType = cellType,
                                          disease = disease,
                                          quantMethods = quantMethods,
                                          userName = userName,
                                          email = email,
                                          affiliation = affiliation,
                                          pubMedID = pubMedID,
                                          rePXaccession = rePXaccession,
                                          linkToOther = linkToOther,
                                          createTime = createTime,
                                          modifiedTime = createTime,
                                          validated = True
                                          )
        aNewProjectDetail.save()
    except:
        aProjectDetail = ProjectDetail.objects.all().get(id=aNewProjectDetail.id)
        aProjectDetail.delete()
        aNewProjectId = -1
        return aNewProjectId
        
    aNewProjectId = aNewProjectDetail.id
    return aNewProjectId
    

''' add a new project'''
'''
parent permission
'''
def addANewProject(aNewProjectId, parametersDict):
    '''
    Insert a new record into ProjectOverview
    '''
    pxdNo = ProjectDetail.objects.all().get(id=aNewProjectId).pxdNo
    status = parametersDict['status']
    projectStatus = ProjectStatus.objects.all().get(status=status)
    user = parametersDict['user']
    createTime = timezone.now()
    aProjectDetail = ProjectDetail.objects.all().get(id=aNewProjectId)
    aNewProjectOverview = ProjectOverview(id = aProjectDetail,
                                          pxdNo = pxdNo,
                                          status = projectStatus,
                                          user = user,
                                          createTime = timezone.now()
                                          )
    aNewProjectOverview.save()
    return pxdNo



''' show all projects under current user '''
def showAllProjects(userId):
    parentFlag = isParentAccount(userId)
    childFlag = isActive_ChildUser(userId)
    guestFlag = isGuest(userId)
    allProjects_detail = []
    if guestFlag:
        allProjects = ProjectOverview.objects.all().filter(status__status="Publicated").filter(validated=True)
        if allProjects:
            for project in allProjects:
                tmpDict = {}
                pxdNo = project.pxdNo
                tmpDict["pxdNo"] = project.pxdNo
                tmpDict["status"] = project.status.status
                projectDetail = ProjectDetail.objects.all().get(pxdNo=pxdNo)
                tmpDict["projectName"] = projectDetail.projectName
                tmpDict["species"] = projectDetail.species.name
                allProjects_detail.append(tmpDict)
    elif childFlag:
        projectStrList = ChildUserAndSharedProject.objects.all().filter(child_id=userId)
        if projectStrList:
            projectStrList = projectStrList[0].split(",")
            for projectStr in projectStrList:
                pxdNo = projectStr
                project = ProjectOverview.objects.all().get(pxdNo=pxdNo).filter(validated=True)
                tmpDict = {}
                tmpDict["pxdNo"] = project.pxdNo
                tmpDict["status"] = project.status.status
                projectDetail = ProjectDetail.objects.all().get(pxdNo=pxdNo)
                tmpDict["projectName"] = projectDetail.projectName
                tmpDict["species"] = projectDetail.species.name
                allProjects_detail.append(tmpDict)
    elif parentFlag:
        allProjects = ProjectOverview.objects.all().filter(user_id=userId).filter(validated=True)
        if allProjects:
            for project in allProjects:
                tmpDict = {}
                pxdNo = project.pxdNo
                tmpDict["pxdNo"] = project.pxdNo
                tmpDict["status"] = project.status.status
                projectDetail = ProjectDetail.objects.all().get(pxdNo=pxdNo)
                tmpDict["projectName"] = projectDetail.projectName
                tmpDict["species"] = projectDetail.species.name
                allProjects_detail.append(tmpDict)
    else:
        tmpDict = {}
        tmpDict["msg"] = "Current account is unkonwn."
        allProjects_detail.append(tmpDict)
    return allProjects_detail




def isPublicatedProject(pxdNo):
    aProject = ProjectOverview.objects.all().filter(pxdNo=pxdNo)[0]
    status = aProject.status.status
    if status=="Publicated":
        return True
    else:
        return False
    
def ownerIsGuest(pxdNo):
    aProject = PublicatedProject.objects.all().get(pxdNo=pxdNo)
    if aProject.newOwner == "Guest":
        return True
    else:
        return False

def changeProjectStatus(pxdNo, status):
    changeFlag = False
    if not isPublicatedProject(pxdNo):
        aProject = ProjectOverview.objects.all().filter(pxdNo=pxdNo)[0]
        statusInstance = ProjectStatus.objects.all().get(status=status)
        
        aProject.status = statusInstance
        aProject.save()
        changeFlag = True
        if aProject.status.status == "Publicated":
            newPublicatedProject = PublicatedProject(pxdNo = pxdNo,
                                                     oldOwner = aProject.user.username,
                                                     newOwner = "Guest",
                                                     isPublicated = True,
                                                     publicatedTime = timezone.now()
                                                     )
            newPublicatedProject.save() 
    return changeFlag


def showMetadataByPxdNo(pxdNo):
    try:
        aProjectMetadata = ProjectDetail.objects.all().get(pxdNo = pxdNo)
        parametersDict = {}
        parametersDict['pxdNo'] = pxdNo
        parametersDict['projectname'] = aProjectMetadata.projectName
        parametersDict['keywords'] = aProjectMetadata.keywords
        parametersDict['projectdescription'] = aProjectMetadata.projectDescription
        parametersDict['sampleprotocol'] = aProjectMetadata.sampleProtocol
        parametersDict['dataprotocol'] = aProjectMetadata.dataProtocol
        
        parametersDict['ExperimentType'] = aProjectMetadata.experimentType.name
        parametersDict['Species'] = aProjectMetadata.species.name
        parametersDict['Tissue'] = aProjectMetadata.tissue.name
        
        parametersDict['Modification'] = aProjectMetadata.modification.name
        
        parametersDict['Instrument'] = aProjectMetadata.instrument.name
        parametersDict['CellType'] = aProjectMetadata.cellType.name
        parametersDict['Disease'] = aProjectMetadata.disease.name
        parametersDict['QuantMethods'] = aProjectMetadata.quantMethods.name
        
        parametersDict['name'] = aProjectMetadata.userName
        parametersDict['email'] = aProjectMetadata.email
        parametersDict['affiliation'] = aProjectMetadata.affiliation
        parametersDict['pubmedID'] = aProjectMetadata.pubMedID
        parametersDict['rePXaccession'] = aProjectMetadata.rePXaccession
        parametersDict['linkToOther'] = aProjectMetadata.linkToOther
    except:
        parametersDict = {}
        parametersDict['error'] = "Errors occur while showing metadata of %s" % pxdNo
        return parametersDict
    return parametersDict


def updateMetadataForAProject(parametersDict):
    updateFlag = False
    pxdNo = parametersDict['pxdNo']
    aProject = ProjectOverview.objects.all().get(pxdNo = pxdNo)
    status = aProject.status.status
    if not isPublicatedProject(pxdNo):
        projectName = parametersDict['projectName']
        keywords = parametersDict['keywords']
        projectDescription = parametersDict['projectDescription']
        sampleProtocol = parametersDict['sampleProtocol']
        dataProtocol = parametersDict['dataProtocol']
        
        experimentType = Miape_ExpType.objects.all().get(name=parametersDict['experimentType'])
        species = Miape_Species.objects.all().get(name=parametersDict['species'])
        tissue = Miape_Tissue.objects.all().get(name=parametersDict['tissue'])
        
        modification = Miape_Modification.objects.all().get(name=parametersDict['modification'])
        
        instrument = Miape_Instrument.objects.all().get(name=parametersDict['instrument'])
        cellType = Miape_CellType.objects.all().get(name=parametersDict['cellType'])
        disease = Miape_Disease.objects.all().get(name=parametersDict['disease'])
        quantMethods = Miape_QuantMethod.objects.all().get(name=parametersDict['quantMethods'])
    
        userName = parametersDict['userName']
        email = parametersDict['email']
        affiliation = parametersDict['affiliation']
        pubMedID = parametersDict['pubMedID']
        rePXaccession = parametersDict['rePXaccession']
        linkToOther = parametersDict['linkToOther']
        
        aProjectDetail = ProjectDetail.objects.all().get(id=aProject.id.id)
        aProjectDetail.projectName = projectName
        aProjectDetail.keywords = keywords
        aProjectDetail.projectDescription = projectDescription
        aProjectDetail.sampleProtocol = sampleProtocol
        aProjectDetail.dataProtocol = dataProtocol
        aProjectDetail.experimentType = experimentType
        aProjectDetail.species = species
        aProjectDetail.tissue = tissue
        
        aProjectDetail.modification = modification
        
        aProjectDetail.cellType = cellType
        aProjectDetail.disease = disease
        aProjectDetail.quantMethods = quantMethods
        aProjectDetail.userName = userName
        aProjectDetail.email = email
        aProjectDetail.affiliation = affiliation,
        aProjectDetail.pubMedID = pubMedID
        aProjectDetail.rePXaccession = rePXaccession
        aProjectDetail.linkToOther = linkToOther
        aProjectDetail.modifiedTime = timezone.now()
        try:
            aProjectDetail.save()
            updateFlag = True
        except:
            updateFlag = True
            return updateFlag
    return updateFlag
    
    




'''
parent permission
'''
def showAllChildAccountInfo_inRepository(parentId): #return jsonResult
    '''
    Parent account gets own child account via parent id.
    '''
    parent = User.objects.all().get(id=parentId)
    childs = AuthParentChildAssociation.objects.all().filter(parent=parent)
    
    childs_username = []
    childs_isActive = []
    childs_annotation = []
    childs_sharedProjectList = []

    if childs:
        for child in childs:
            childs_username.append(child.child.child_username)
            childs_isActive.append(child.child.child_is_active)
            childs_annotation.append(child.child.child_annotation)
            
            childInstance = AuthChildUser.objects.all().get(id=child.child_id)
            child_sharedProhectList = ChildUserAndSharedProject.objects.all().filter(child=childInstance)
            if child_sharedProhectList:
                child_sharedProhectList = child_sharedProhectList[0]
                childs_sharedProjectList.append(child_sharedProhectList.sharedProject)
            else:
                childs_sharedProjectList.append("")
            
        success = 1
        prompt = "Load all child accounts belonging to the parent account in project level."
    else:
        success = 0
        prompt = "The parent account has no child accounts."
    
    
    childsCount = len(childs)
    tempDataList = []
    if childsCount>0:
        for i in range(0, childsCount):
            tempDataDict = {}
            tempDataDict['username'] = childs_username[i]
            tempDataDict['isActive'] = childs_isActive[i]
            tempDataDict['annotation'] = childs_annotation[i]
            tempDataDict['sharedProjectList'] = childs_sharedProjectList[i]
            tempDataList.append(tempDataDict)
    
    temp = {}
    temp['success'] = success
    temp['msg'] = prompt
    temp['data'] = tempDataList
    jsonResult = json.dumps(temp, cls=DjangoJSONEncoder)
    return jsonResult

'''
 Child user and shared project
'''
def addChildUserSharedProject(userId, childName, sharedProject):
    '''
    Parent account share specific experiments to child account.
    '''
    #shareProject = "FNO007407,FNO007408,FNO007409"
    addSharedProjectFlag = False
    allProjects = ProjectOverview.objects.all().filter(user_id = userId).filter(validated=True)
    allProjectsName = []
    for project in allProjects:
        allProjectsName.append(project.pxdNo)
    sharedProjectNameList = sharedProject.split(",")
    for sharedProjectName in sharedProjectNameList:
        if  sharedProjectName not in allProjectsName:
            return False
    
    try:
        child = AuthChildUser.objects.all().get(child_username=childName)
        childUserSharedProject = ChildUserAndSharedProject.objects.all().filter(child=child)
        if childUserSharedProject:
            childUserSharedProject = childUserSharedProject[0]
            childUserSharedProject.sharedProject = sharedProject
            childUserSharedProject.save()
        else:
            isActive = True
            newChildUserSharedProject = ChildUserAndSharedProject(child=child,
                                                              sharedProject=sharedProject,
                                                              isActive=isActive
                                                              )
            newChildUserSharedProject.save()
        addSharedProjectFlag = True
    except:
        addSharedProjectFlag = False
    return addSharedProjectFlag




''' update metadata of specific project '''
'''parent perimission'''
def updateChildAccountSharedProject(childName, sharedProject):
    '''
    Parent account updates experiments list for sharing to child account.
    '''
    updateSharedProjectFlag = False
    try:
        if child:
            child = child[0]
            childUserSharedProject = ChildUserAndSharedProject.objects.all().filter(child=child)
            if childUserSharedProject:
                childUserSharedProject = childUserSharedProject[0]
                childUserSharedProject.sharedProject = sharedProject
                childUserSharedProject.save()
                updateSharedProjectFlag = True
            else:
                updateSharedProjectFlag = False
        else:
            updateSharedProjectFlag = False
    except:
        updateSharedProjectFlag = False
    return updateSharedProjectFlag



def deleteAProject(userId, pxdNo):
    deleteFlag = False
    
    projectBelongsToUserFlag = projectBelongsToUser(userId, pxdNo)
    if not projectBelongsToUserFlag:
        return deleteFlag
    
    isPublicatedFlag = isPublicatedProject(pxdNo)
    if isPublicatedFlag:
        return deleteFlag
    else:
        aProject = ProjectOverview.objects.all().filter(pxdNo=pxdNo).filter(validated=True)
        if aProject:
            aProject = aProject[0]
            aProject.validated = False
        else:
            return deleteFlag
        



        
        
        

