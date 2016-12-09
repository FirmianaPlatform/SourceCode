from django.db import models

from django.contrib.auth.models import User
from experiments.models import AuthChildUser
from experiments.models import AuthParentChildAssociation

''' MIAPE Metadata '''
class Miape_ExpType(models.Model):
    '''Experimental type complying with MIAPE standard'''
    name = models.CharField(max_length=255, unique=True)
    validated = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name
        
class Miape_Species(models.Model):
    '''Species complying with MIAPE standard'''
    name = models.CharField(max_length=255, unique=True)
    validated = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name
        
class Miape_Tissue(models.Model):
    '''Tissues complying with MIAPE standard'''
    name = models.CharField(max_length=255, unique=True)
    validated = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name
        
class Miape_Modification(models.Model):
    '''Modifications complying with MIAPE standard'''
    name = models.CharField(max_length=255, unique=True)
    validated = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name
        
class Miape_Instrument(models.Model):
    '''Instrument name complying with MIAPE standard'''
    name = models.CharField(max_length=255, unique=True)
    validated = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name
        
class Miape_CellType(models.Model):
    '''Cell type complying with MIAPE standard'''
    name = models.CharField(max_length=255, unique=True)
    validated = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name
        
class Miape_Disease(models.Model):
    '''Disease name complying with MIAPE standard'''
    name = models.CharField(max_length=255, unique=True)
    validated = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name
        
class Miape_QuantMethod(models.Model):
    '''Quantification method complying with MIAPE standard'''
    name = models.CharField(max_length=255, unique=True)
    validated = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name

''' Project '''
class ProjectStatus(models.Model):
    '''Status of project in data repository of Fimiana'''
    status = models.CharField(max_length=90, unique=True)
    validated = models.BooleanField(default=True)
    def __unicode__(self):
        return self.status

class ProjectDetail(models.Model):
    '''Detail information of a project in data repository of Fimiana'''
    pxdNo = models.CharField(max_length=255, unique=True)
    projectName = models.TextField()
    keywords = models.TextField()
    projectDescription = models.TextField()
    sampleProtocol = models.TextField()
    dataProtocol = models.TextField()
    
    experimentType = models.TextField()
    species = models.TextField()
    tissue = models.TextField()
    modification = models.TextField()
    instrument = models.TextField()
    cellType = models.TextField()
    disease = models.TextField()
    quantMethods = models.TextField()
    
    userName = models.CharField(max_length=255, unique=False)
    email = models.CharField(max_length=255, unique=False)
    affiliation = models.TextField()
    pubMedID = models.TextField()
    rePXaccession = models.TextField()
    linkToOther = models.TextField()
    createTime = models.DateTimeField()
    modifiedTime = models.DateTimeField()
    
    validated = models.BooleanField(default=True)

    
class ProjectOverview(models.Model):
    '''Overview of a project in data repository of Fimiana'''
    id = models.OneToOneField(ProjectDetail, db_column='id', primary_key=True)
    pxdNo = models.CharField(max_length=255, unique=True)
    status = models.ForeignKey(ProjectStatus, unique=False)
    user = models.ForeignKey(User, unique=False)
    createTime = models.DateTimeField()
    
    validated = models.BooleanField(default=True)
    def __unicode__(self):
         return self.pxdNo

class ChildUserAndSharedProject(models.Model):
    '''The assotiation between sub-account and shared projects'''
    child = models.ForeignKey(AuthChildUser)
    sharedProject = models.TextField()
    isActive = models.BooleanField(default=True)
    def __unicode__(self):
        return self.sharedProject
     
class PublicatedProject(models.Model):
    '''The information of publicated project'''
    pxdNo = models.CharField(max_length=255, unique=True)
    oldOwner = models.CharField(max_length=255, unique=False)
    newOwner = models.CharField(max_length=255, unique=False, default="Guest")
    isPublicated = models.BooleanField(default=True)
    publicatedTime = models.DateTimeField()
    
    validated = models.BooleanField(default=True)
    def __unicode__(self):
        return self.id 
     
