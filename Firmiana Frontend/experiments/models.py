from django.db import models
from django.contrib.auth.models import User, Group
from django.template.loader import get_template
from django.core.mail import EmailMessage
from django.template import Context
from password_trans import new_secure_hash
from leafy.config import *
from django.contrib.auth.models import AbstractUser
from django.template.defaultfilters import default
FIRMIANAURL = ConfigSectionMap("Firmiana")['firmianaurl']

class NewUser(AbstractUser):
    lab = models.CharField(max_length=100,null=True, blank=True)
    def __unicode__(self):
        return self.lab
        
class Invitation(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    code = models.CharField(max_length=20)
    sender = models.ForeignKey(User)
    def __unicode__(self):
        return '%s %s' % (self.sender.username, self.email)
    def send(self):
        subject = 'Inviation to join Firmiana System'
        link = FIRMIANAURL + '/register/%s/' % (self.code)
        template = get_template('invitation_email.txt')
        context = Context({
            'name': self.name,
            'link': link,
            })
        message = template.render(context)
        email = EmailMessage(subject, message, to=[self.email])
        email.send()
        
class ResetPsd(models.Model):
    email = models.EmailField()
    code = models.CharField(max_length=20)
    def __unicode__(self):
        return '%s' % (self.email)
    def send(self):
        subject = 'Reset your Firmiana password'
        link = FIRMIANAURL + '/forgetpsd/%s/' % (self.code)
        template = get_template('forgetpsd_email.txt')
        context = Context({
            'link': link,
            })
        message = template.render(context)
        email = EmailMessage(subject, message, to=[self.email])
        email.send()


class Experimenter(models.Model):
    id = models.OneToOneField(User, db_column='id', primary_key=True)
    create_time = models.DateTimeField(null=True, blank=True)
    update_time = models.DateTimeField(null=True, blank=True)
    email = models.CharField(max_length=765)
    password = models.CharField(max_length=120)
    external = models.IntegerField(null=True, blank=True)
    deleted = models.IntegerField(null=True, blank=True)
    purged = models.IntegerField(null=True, blank=True)
    username = models.CharField(max_length=765, blank=True)
    form_values_id = models.IntegerField(null=True, blank=True)
    disk_usage = models.DecimalField(null=True, max_digits=16, decimal_places=0, blank=True)

    def __unicode__(self):
        return self.username
    class Meta:
        db_table = 'galaxy_user'


class All_Company(models.Model):
    name = models.CharField(max_length=255, unique=True)
    validated = models.BooleanField(default=False)
    
    def __unicode__(self):
        return self.name 
class All_Laboratory(models.Model):
    name = models.CharField(max_length=255, unique=True)
    company = models.ManyToManyField(All_Company)
    validated = models.BooleanField(default=False)
    
    def __unicode__(self):
        return self.name 
''' For control what user can see '''
class User_Laboratory(models.Model):
    lab = models.ForeignKey(All_Laboratory)
    user = models.ForeignKey(User)
    validated = models.BooleanField(default=False)
    
    def __unicode__(self):
        return self.lab 
    
class All_Experimenter(models.Model):
    name = models.CharField(max_length=255, unique=False)
    lab = models.ForeignKey(All_Laboratory)
    validated = models.BooleanField(default=False)
    
    def __unicode__(self):
        return self.name 

class Experimenter_info(models.Model):
    company = models.ForeignKey(All_Company)
    lab = models.ForeignKey(All_Laboratory)
    experimenter = models.ForeignKey(All_Experimenter)
    def __unicode__(self):
        return self.experimenter 

class Container(models.Model):
    name = models.CharField(max_length=255, unique=True)
    validated = models.BooleanField(default=False)
   
    def __unicode__(self):
        return self.name
    
'''Refirgerator'''
class Refrigerator_No(models.Model):
    name = models.CharField(max_length=255, unique=True)
    validated = models.BooleanField(default=False)
    def __unicode__(self):
        return self.name

class Refrigerator_Temperature(models.Model):
    name = models.CharField(max_length=255, unique=True)
    validated = models.BooleanField(default=False)
    def __unicode__(self):
        return self.name

class Refrigerator_Layer(models.Model):
    name = models.CharField(max_length=255, unique=True)
    validated = models.BooleanField(default=False)
    def __unicode__(self):
        return self.name

'''Nitrogen'''
class Nitrogen_Container(models.Model):
    name = models.CharField(max_length=255, unique=True)
    validated = models.BooleanField(default=False)
    def __unicode__(self):
        return self.name

class Nitrogen_Basket(models.Model):
    name = models.CharField(max_length=255, unique=True)
    validated = models.BooleanField(default=False)
    def __unicode__(self):
        return self.name

class Nitrogen_Layer(models.Model):
    name = models.CharField(max_length=255, unique=True)
    validated = models.BooleanField(default=False)
    def __unicode__(self):
        return self.name

'''Others'''

class Others_Temperature(models.Model):
    name = models.CharField(max_length=255, unique=True)
    validated = models.BooleanField(default=False)
    def __unicode__(self):
        return self.name




class Container_No(models.Model):
    name = models.CharField(max_length=255)
    Container = models.ForeignKey(Container)
    validated = models.BooleanField(default=False)
   
    def __unicode__(self):
        return self.name
class Container_Basket(models.Model):
    name = models.CharField(max_length=255, unique=True)
    Container = models.ForeignKey(Container)
    validated = models.BooleanField(default=False)
   
    def __unicode__(self):
        return self.name
class Container_Layer(models.Model):
    name = models.CharField(max_length=255)
    Container = models.ForeignKey(Container)
    validated = models.BooleanField(default=False)
   
    def __unicode__(self):
        return self.name
class All_AgeUnit(models.Model):
    name = models.CharField(max_length=255, unique=True)
    validated = models.BooleanField(default=False)
   
    def __unicode__(self):
        return self.name
class Source_TissueTaxonAorM(models.Model):
    name = models.CharField(max_length=255, unique=True)
    validated = models.BooleanField(default=False)
   
    def __unicode__(self):
        return self.name
class Source_TissueTaxonID(models.Model):
    name = models.CharField(max_length=255, unique=True)
    pid = models.ForeignKey(Source_TissueTaxonAorM)
    validated = models.BooleanField(default=False)
   
    def __unicode__(self):
        return self.name

class Source_TissueTaxonStrain(models.Model):
    name = models.CharField(max_length=255)
    pid = models.ForeignKey(Source_TissueTaxonID)
    validated = models.BooleanField(default=False)
   
    def __unicode__(self):
        return self.name
class Source_TissueTaxonName(models.Model):
    name = models.CharField(max_length=255)
    abbrev=models.CharField(max_length=255)
    pid = models.ForeignKey(Source_TissueTaxonID)
    validated = models.BooleanField(default=False)
   
    def __unicode__(self):
        return self.name

class Source_TissueSystem(models.Model):
    name = models.CharField(max_length=255)
    pid = models.ForeignKey(Source_TissueTaxonAorM)
    validated = models.BooleanField(default=False)
   
    def __unicode__(self):
        return self.name

class Source_TissueOrgan(models.Model):
    name = models.CharField(max_length=255)
    pid = models.ForeignKey(Source_TissueSystem)
    validated = models.BooleanField(default=False)
   
    def __unicode__(self):
        return self.name

class Source_TissueStructure(models.Model):
    name = models.CharField(max_length=255)
    pid = models.ForeignKey(Source_TissueOrgan)
    validated = models.BooleanField(default=False)
   
    def __unicode__(self):
        return self.name
class Source_TissueType(models.Model):
    name = models.CharField(max_length=255)
    validated = models.BooleanField(default=False)
    def __unicode__(self):
        return self.name

class source_CellType(models.Model):
    name = models.CharField(max_length=255)
    validated = models.BooleanField(default=False)
    def __unicode__(self):
        return self.name

class Cell_Name(models.Model):
    name = models.CharField(max_length=255)
    pid = models.ForeignKey(source_CellType)
    abbrev=models.CharField(max_length=255)
    validated = models.BooleanField(default=False)
    def __unicode__(self):
        return self.name

class Fluid_name(models.Model):
    name = models.CharField(max_length=255)
    validated = models.BooleanField(default=False)
    def __unicode__(self):
        return self.name

class Experiment_group(models.Model):
    id = models.OneToOneField(Group, related_name='experiment_group', primary_key=True)
    create_time = models.DateTimeField(null=True, blank=True)
    update_time = models.DateTimeField(null=True, blank=True)
    name = models.CharField(max_length=255, unique=True, blank=True)
    deleted = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'galaxy_group'

    def __unicode__(self):
        return self.name

class Galaxy_session(models.Model):
    id = models.IntegerField(primary_key=True)
    create_time = models.DateTimeField(null=True, blank=True)
    update_time = models.DateTimeField(null=True, blank=True)
    user_id = models.IntegerField(null=True, blank=True)
    remote_host = models.CharField(max_length=255, blank=True)
    remote_addr = models.CharField(max_length=255, blank=True)
    referer = models.TextField(blank=True)
    current_history_id = models.IntegerField(null=True, blank=True)
    session_key = models.CharField(max_length=255, unique=True, blank=True)
    is_valid = models.IntegerField(null=True, blank=True)
    prev_session_id = models.IntegerField(null=True, blank=True)
    disk_usage = models.DecimalField(null=True, max_digits=16, decimal_places=0, blank=True)

    class Meta:
        db_table = 'galaxy_session'

class copartner(models.Model):
    from_experimenter = models.ForeignKey(Experimenter, related_name='from_experimenter_set')
    to_experimenter = models.ForeignKey(Experimenter, related_name='to_experimenter_set')

    class meta:
        unique_together = ('from_experimenter', 'to_experimenter')

class Project(models.Model):
    name = models.CharField(max_length=255, unique=True)
    validated = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name

################################################
#           Reagent   Model                    #
################################################

class Conjugate(models.Model):
    name = models.CharField(max_length=255, unique=True)
    validated = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name

class Purification(models.Model):
    name = models.CharField(max_length=255, unique=True)
    validated = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name

class React_species(models.Model):
    name = models.CharField(max_length=255, unique=True)
    validated = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name

class Reagent_manufacturer(models.Model):
    name = models.CharField(max_length=255, unique=True)
    validated = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name

class Affinity(models.Model):
    name = models.CharField(max_length=255, unique=True)
    validated = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name

class Application(models.Model):
    name = models.CharField(max_length=255, unique=True)
    validated = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name

#+++++++++++++++++++++++++++++ Reagent Type  Model++++++++++++++++++++++++
class Antigen_species(models.Model):
    name = models.CharField(max_length=255, unique=True)
    validated = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name

class Antigen_clonal_type(models.Model):
    name = models.CharField(max_length=255, unique=True)
    validated = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name

class Antigen_modification(models.Model):
    name = models.CharField(max_length=255, unique=True)
    validated = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name

class Antigen(models.Model):
    gene_id = models.CharField(max_length=1024)
    host_species = models.ForeignKey(Antigen_species)
    clonal_type = models.ForeignKey(Antigen_clonal_type)
    modification = models.ForeignKey(Antigen_modification)

    def __unicode__(self):
        return self.gene_id

class Dna_info(models.Model):
    sequence = models.TextField()

    def __unicode__(self):
        return self.sequence


class Domain_info(models.Model):
    domain = models.TextField()

    def __unicode__(self):
        return self.domain

class Chemical_info(models.Model):
    chemical = models.TextField()

    def __unicode__(self):
        return self.domain

class Remarks_info(models.Model):
    remarks = models.TextField()

    def __unicode__(self):
        return self.remarks

class Reagent(models.Model):
    experimenter = models.ForeignKey(Experimenter_info)
    date = models.DateField()
    type = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    manufacturer = models.ForeignKey(Reagent_manufacturer)
    catalog_no = models.CharField(max_length=255)
    # affinity = models.ForeignKey(Affinity)
    applications = models.ManyToManyField(Application)
    react_species_sources = models.ManyToManyField(React_species, related_name='reagent_source')
    react_species_targets = models.ManyToManyField(React_species, related_name='reagent_target')
    # purification = models.ForeignKey(Purification)
    conjugate = models.ForeignKey(Conjugate)
    antigen = models.ForeignKey(Antigen, null=True, blank=True)
    dna_info = models.ForeignKey(Dna_info, null=True, blank=True)
    domain_info = models.ForeignKey(Domain_info, null=True, blank=True)
    chemical_info=models.ForeignKey(Chemical_info, null=True, blank=True)
    remarks_info = models.ForeignKey(Remarks_info, null=True, blank=True)
    ispec_no = models.CharField(max_length=255, blank=True)
    
    #zdd add the field
    ext_comments = models.TextField(blank=True)
    def __unicode__(self):
        return self.name


################################################
#             Sample  Model                    #
################################################

#++++++++++++++++++++ Sample RX Model +++++++++++++++++++++++++++++

class Rx_treatment(models.Model):
    name = models.CharField(max_length=255, unique=True)
    validated = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name
class Rx_treatment_detail(models.Model):
    name = models.CharField(max_length=255, unique=True)
    type = models.ForeignKey(Rx_treatment)
    validated = models.BooleanField(default=False)
    abbrev=models.CharField(max_length=255)
    def __unicode__(self):
        return self.name
class Rx_treatment_detail_detail(models.Model):
    name = models.CharField(max_length=255, unique=True)
    type = models.ForeignKey(Rx_treatment_detail)
    validated = models.BooleanField(default=False)
    def __unicode__(self):
        return self.name
class Rx_unit(models.Model):
    name = models.CharField(max_length=255, unique=True)
    validated = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name
class Rx_unit_detail(models.Model):
    name = models.CharField(max_length=255)
    type = models.ForeignKey(Rx_unit)
    validated = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name
class Rx_duration(models.Model):
    name = models.CharField(max_length=255, unique=True)
    validated = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name
#++++++++++++++++++++ Sample UBI Model ++++++++++++++++++++++++++++

class Ubi_subcell(models.Model):
    name = models.CharField(max_length=255, unique=True)
    abbrev=models.CharField(max_length=255, unique=True)
    validated = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name

class Ubi_method(models.Model):
    name = models.CharField(max_length=255, unique=True)
    validated = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name
'''
class Ubi_detergent(models.Model):
    name = models.CharField(max_length=255, unique=True)
    validated = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name

class Ubi_salt(models.Model):
    name = models.CharField(max_length=255, unique=True)
    validated = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name
'''
#+++++++++++++++++++ Sample  Source  Model +++++++++++++++++++++++

class Source_taxon(models.Model):
    name = models.CharField(max_length=255, unique=True)
    validated = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name

class Genotype(models.Model):
    name = models.CharField(max_length=255, unique=True)
    abbrev=models.CharField(max_length=255)
    validated = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name


class Cell_type(models.Model):
    name = models.CharField(max_length=255, unique=True)
    validated = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name

class Tissue_gender(models.Model):
    name = models.CharField(max_length=255, unique=True)
    validated = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name

class Tissue_strain(models.Model):
    name = models.CharField(max_length=255, unique=True)
    validated = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name

class Tissue_type(models.Model):
    name = models.CharField(max_length=255, unique=True)
    validated = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name


class Source_tissue(models.Model):
    AorM = models.ForeignKey(Source_TissueTaxonAorM)
    tissueName = models.ForeignKey(Source_TissueTaxonName)
    tissueID = models.ForeignKey(Source_TissueTaxonID, related_name='+')
    tissueStrain = models.ForeignKey(Source_TissueTaxonStrain)
    age = models.CharField(max_length=255)
    age_unit = models.ForeignKey(All_AgeUnit)
    gender = models.ForeignKey(Tissue_gender)
    genotype = models.ForeignKey(Genotype)
    tissueSystem = models.ForeignKey(Source_TissueSystem)
    tissueOrgan = models.ForeignKey(Source_TissueOrgan)
    tissueStructure=models.CharField(max_length=255, blank=True)
    tissueType = models.ForeignKey(Source_TissueType)
    geneTaxon = models.ForeignKey(Source_TissueTaxonID, related_name='+', null=True, blank=True)
    geneSymbol = models.CharField(max_length=255, blank=True)
    geneID = models.CharField(max_length=255, blank=True)
    gene=models.TextField(blank=True)
    circ_time = models.CharField(max_length=255, blank=True)
    specific_ID = models.CharField(max_length=255, blank=True)

class Source_cell(models.Model):
    AorM = models.ForeignKey(Source_TissueTaxonAorM)
    tissueName = models.ForeignKey(Source_TissueTaxonName)
    tissueID = models.ForeignKey(Source_TissueTaxonID, related_name='+')
    tissueStrain = models.ForeignKey(Source_TissueTaxonStrain)
    genotype = models.ForeignKey(Genotype)
    cellType = models.ForeignKey(source_CellType, null=True, blank=True)
    cellName = models.ForeignKey(Cell_Name, null=True, blank=True)
    geneTaxon = models.ForeignKey(Source_TissueTaxonID, related_name='+', null=True, blank=True)
    geneSymbol = models.CharField(max_length=255, blank=True)
    geneID = models.CharField(max_length=255, blank=True)
    gene=models.TextField(blank=True)
    circ_time = models.CharField(max_length=255, blank=True)
    specific_ID = models.CharField(max_length=255, blank=True)

class Source_fluid(models.Model):
    AorM = models.ForeignKey(Source_TissueTaxonAorM)
    tissueName = models.ForeignKey(Source_TissueTaxonName)
    tissueID = models.ForeignKey(Source_TissueTaxonID, related_name='+')
    tissueStrain = models.ForeignKey(Source_TissueTaxonStrain)
    age = models.CharField(max_length=255)
    age_unit = models.ForeignKey(All_AgeUnit)
    gender = models.ForeignKey(Tissue_gender)
    genotype = models.ForeignKey(Genotype)
    fluid = models.ForeignKey(Fluid_name)
    geneTaxon = models.ForeignKey(Source_TissueTaxonID, related_name='+', null=True, blank=True)
    geneSymbol = models.CharField(max_length=255, blank=True)
    geneID = models.CharField(max_length=255, blank=True)
    gene=models.TextField(blank=True)
    circ_time = models.CharField(max_length=255, blank=True)
    specific_ID = models.CharField(max_length=255, blank=True)

class Source_others(models.Model):
    name = models.TextField()

class Location_Refrigerator(models.Model):
    no = models.ForeignKey(Refrigerator_No)
    temperature = models.ForeignKey(Refrigerator_Temperature)
    layer = models.ForeignKey(Refrigerator_Layer)

class Location_Nitrogen(models.Model):
    no = models.ForeignKey(Nitrogen_Container)
    basket = models.ForeignKey(Nitrogen_Basket)
    layer = models.ForeignKey(Nitrogen_Layer)
    
class Location_Others(models.Model):
    temperature = models.ForeignKey(Others_Temperature)
    location = models.CharField(max_length=255)

class Location(models.Model):
    refrigerator = models.ForeignKey(Location_Refrigerator, null=True, blank=True)
    nitrogen = models.ForeignKey(Location_Nitrogen , null=True, blank=True)
    others = models.ForeignKey(Location_Others , null=True, blank=True, related_name='+')
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


class Treatment(models.Model):
    rx_treatments = models.ForeignKey(Rx_treatment)
    rx_treatments_detail = models.ForeignKey(Rx_treatment_detail)
    rx_treatments_detail_detail = models.ForeignKey(Rx_treatment_detail_detail,null=True,blank=True )
    rx_amount = models.CharField(max_length=255, blank=True)
    rx_unit = models.ForeignKey(Rx_unit, null=True, blank=True)
    # detail some word wrong 
    rx_unit_deatil = models.ForeignKey(Rx_unit_detail, null=True, blank=True)
    rx_duration = models.CharField(max_length=255, blank=True)
    rx_duration_time = models.CharField(max_length=255, blank=True)
    geneTaxon = models.ForeignKey(Source_TissueTaxonID, null=True, blank=True)
    geneSymbol = models.CharField(max_length=255, blank=True)
    geneID = models.CharField(max_length=255, blank=True)

class Sample(models.Model):
    date = models.DateField()
    experimenter = models.ForeignKey(Experimenter_info)
    location = models.ForeignKey(Location)
    #cell_tissue = models.CharField(max_length=255, blank=True)
    source_tissue = models.ForeignKey(Source_tissue, null=True, blank=True)
    source_cell = models.ForeignKey(Source_cell, null=True, blank=True)
    source_fluid = models.ForeignKey(Source_fluid, null=True, blank=True)
    source_others = models.ForeignKey(Source_others, null=True, blank=True)
    rx_treatments = models.ForeignKey(Rx_treatment, null=True, blank=True)
    rx_treatments_detail = models.ForeignKey(Rx_treatment_detail, null=True, blank=True)
    rx_treatments_detail_detail = models.ForeignKey(Rx_treatment_detail_detail,null=True,blank=True )
    rx_amount = models.CharField(max_length=255, blank=True)
    rx_unit = models.ForeignKey(Rx_unit, null=True, blank=True)
    # detail some word wrong
    rx_unit_deatil = models.ForeignKey(Rx_unit_detail, null=True, blank=True)
    rx_duration = models.CharField(max_length=255, blank=True)
    rx_duration_time = models.CharField(max_length=255, blank=True)
    treatments = models.ManyToManyField(Treatment)

    ubi_subcells = models.ManyToManyField(Ubi_subcell)
    ubi_methods = models.ManyToManyField(Ubi_method)
    ubi_salt = models.CharField(max_length=255)
    ext_comments = models.TextField(blank=True)
    ispec_no = models.CharField(max_length=255, blank=True)


################################################
#            Experiment  Model                 #
################################################

#++++++++++++++++++++++++ Experiment Instrument Model ++++++++++++++++++++++
class Instrument_manufacturer(models.Model):
    name = models.CharField(max_length=255, unique=True)
    validated = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name

class Instrument(models.Model):
    name = models.CharField(max_length=255, unique=True)
    validated = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name
class Instrument_MS1(models.Model):
    name = models.CharField(max_length=255)
    type = models.ForeignKey(Instrument)
    validated = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name
    
class Instrument_MS1_tol(models.Model):
    name = models.CharField(max_length=255)
    type = models.ForeignKey(Instrument_MS1)
    validated = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name
    
class Instrument_MS2(models.Model):
    name = models.CharField(max_length=255)
    type = models.ForeignKey(Instrument)
    validated = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name
    
class Instrument_MS2_tol(models.Model):
    name = models.CharField(max_length=255)
    type = models.ForeignKey(Instrument_MS2)
    validated = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name
class Fixed_Modification(models.Model):
    #name = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255, blank=True)
    owner = models.CharField(max_length=255)
    validated = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name

class Dynamic_Modification(models.Model):
    #name = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255, blank=True)
    owner = models.CharField(max_length=255)
    validated = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name

#Fasta files
class Search_database(models.Model):
    name = models.CharField(max_length=255, unique=True)
    owner = models.CharField(max_length=255)
    validated = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name
#+++++++++++++++++++++++ Experiment Digest Model ++++++++++++++++++++++++++++

class Digest_type(models.Model):
    name = models.CharField(max_length=255, unique=True)
    validated = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name

class Digest_enzyme(models.Model):
    name = models.CharField(max_length=255, unique=True)
    validated = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name

#+++++++++++++++++++++++ Experiment Workflow Model ++++++++++++++++++++++++++++


#+++++++++++++++++++++++ Customized modifications ++++++++++++++++++++++++++++
#zdd
class Customized_Modifications(models.Model):
    experimentId = models.IntegerField()
    adder = models.CharField(max_length=255)
    new_modi_title = models.CharField(max_length=255)
    new_modi_fullname = models.TextField()
    new_modi_composition = models.TextField()
    new_modi_specificity = models.TextField() #new_modi_specificity_site,new_modi_specificity_position,new_modi_classification
    added_time = models.DateField()
    timeStamp = models.CharField(max_length=255, blank=True)
    def __unicode__(self):
        return self.experimentId

#+++++++++++++++++++++++ Customized modifications ++++++++++++++++++++++++++++


#+++++++++++++++++++++++ Customized fasta library ++++++++++++++++++++++++++++
#zdd
class Custom_FastaLib_copy(models.Model):
     #user=request.user
     timeStamp = models.CharField(max_length=255, blank=True)
     experimentId = models.IntegerField()
     upload_species = models.CharField(max_length=255, blank=True)
     upload_datasource = models.TextField()
     upload_date = models.DateField()
     upload_file = models.TextField()
     upload_user = models.CharField(max_length=255, blank=True)
     validated = models.BooleanField(default=False)
     def __unicode__(self):
         return self.experimentId
     
class Custom_FastaLib_withTimeStamp(models.Model):
     #user=request.user
     timeStamp = models.CharField(max_length=255, blank=True)
     experimentId = models.IntegerField()
     fastaLibName = models.CharField(max_length=255, blank=True)
     upload_species = models.CharField(max_length=255, blank=True)
     upload_datasource = models.TextField()
     upload_date = models.DateField()
     upload_file = models.TextField()
     upload_user = models.CharField(max_length=255, blank=True)
     validated = models.BooleanField(default=False)
     def __unicode__(self):
         return self.experimentId
     
     
class CustomFastaFile(models.Model):
    #user=request.user
    experimentId = models.IntegerField()
    upload_species = models.CharField(max_length=255, blank=False)
    upload_datasource = models.TextField()
    upload_date = models.DateField()
    upload_file = models.TextField()
    upload_user = models.CharField(max_length=255, blank=False)
    def __unicode__(self):
        return self.name


class CustomFile_ForDatabaseSearch(models.Model):
    experimentId = models.IntegerField()
    fileName = models.CharField(max_length=255, blank=True)
    fileAddressOnServer = models.CharField(max_length=255, blank=True)
    validated = models.BooleanField(default=False)


class ExpNo_TimeStamp(models.Model):
    experimentId = models.IntegerField()
    timeStamp = models.CharField(max_length=255, unique=False)
    validated = models.BooleanField(default=False)
    def __unicode__(self):
        return self.experimentId


#+++++++++++++++++++++++ Customized fasta library ++++++++++++++++++++++++++++

#+++++++++++++++++++++++  Quantification_Methods  ++++++++++++++++++++++++++++
#zdd
class Quantification_Methods(models.Model):
    name = models.CharField(max_length=255, unique=True)
    validated = models.BooleanField(default=False)
    def __unicode__(self):
        return self.name
#+++++++++++++++++++++++  Quantification_Methods  ++++++++++++++++++++++++++++


#+++++++++++++++++++++++ raw data source ++++++++++++++++++++++++++++
#zdd
class Workflow_mode(models.Model):
    name = models.CharField(max_length=255, unique=True)
    validated = models.BooleanField(default=False)
 
    def __unicode__(self):
        return self.name
#+++++++++++++++++++++++ raw data source ++++++++++++++++++++++++++++

#+++++++++++++++++++++++ alternatives search engine ++++++++++++++++++++++++++++
#zdd    
class searchEngine(models.Model):
    name = models.CharField(max_length=255, unique=True)
    validated = models.BooleanField(default=False)
 
    def __unicode__(self):
        return self.name


class Xtandem_mode(models.Model):
    experimentId = models.IntegerField()
    fragmentationMethod = models.CharField(max_length=255, blank=True)
    cysteineProtectingGroup = models.CharField(max_length=255, blank=True)
    protease = models.CharField(max_length=255, blank=True)
    numberOfAllowed13C = models.IntegerField()
    #parentMassTolerance = models.FloatField()
    #parentMassToleranceUnit = models.CharField(max_length=255, blank=True)
    #ionTolerance = models.FloatField()
    #ionToleranceUnit = models.CharField(max_length=255, blank=True)
    validated = models.BooleanField(default=False)

#     def __unicode__(self):
#         return self.id

class Pride_mode(models.Model):
    experimentId = models.IntegerField()
    pxdno = models.IntegerField()
    prideFileList = models.TextField()
    validated = models.BooleanField(default=False)
    
   
class Mascot_mode_missedCleavagesAllowed(models.Model):
    name = models.CharField(max_length=255)
    validated = models.BooleanField(default=False)
    def __unicode__(self):
        return self.name
    
class Mascot_mode_mascotEnzyme(models.Model):
    name = models.CharField(max_length=255)
    validated = models.BooleanField(default=False)
    def __unicode__(self):
        return self.name
    
class Mascot_mode_peptideCharge(models.Model):
    name = models.CharField(max_length=255)
    validated = models.BooleanField(default=False)
    def __unicode__(self):
        return self.name
    
class Mascot_mode_precursorSearchType(models.Model):
    name = models.CharField(max_length=255)
    validated = models.BooleanField(default=False)
    def __unicode__(self):
        return self.name
    
class Mascot_mode(models.Model):
    experimentId = models.IntegerField()
    missedCleavagesAllowed = models.ForeignKey(Mascot_mode_missedCleavagesAllowed)
    mascotEnzyme = models.ForeignKey(Mascot_mode_mascotEnzyme)
    peptideCharge = models.ForeignKey(Mascot_mode_peptideCharge)
    precursorSearchType = models.ForeignKey(Mascot_mode_precursorSearchType)   
    validated = models.BooleanField(default=False) 
    


class Experimentalfdr_info(models.Model):
    experimentId = models.IntegerField()
    experimentalFDR_level = models.CharField(max_length=255)
    experimentalFDR_value = models.FloatField()
    validated = models.BooleanField(default=False)
    def __unicode__(self):
        return self.id

#++++++++++++++++++++++  Separation Method Model +++++++++++++++++++++++++++++
class Reagent_buffer(models.Model):
    name = models.CharField(max_length=255, unique=True)
    validated = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name

class Reagent_method(models.Model):
    name = models.CharField(max_length=255, unique=True)
    validated = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name

#++++++++++++++++++++++  Separation Method Model +++++++++++++++++++++++++++++

class Separation_method(models.Model):
    name = models.CharField(max_length=255)
    source = models.CharField(max_length=255)
    size = models.CharField(max_length=255)
    buffer = models.CharField(max_length=255)
    others = models.CharField(max_length=255)
    validated = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name
    
class Separation_md(models.Model):
    name = models.CharField(max_length=255)
    validated = models.BooleanField(default=False)
    def __unicode__(self):
        return self.name

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class Experiment_type(models.Model):
    name = models.CharField(max_length=255, unique=True)
    validated = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name

class Experiment(models.Model):
    date = models.DateField()
    experimenter = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    lab = models.CharField(max_length=255)
    # room = models.CharField(max_length=255)
    # no = models.CharField(max_length=255)
    # Temperature = models.CharField(max_length=255)
    Funding = models.CharField(max_length=255)
    Project = models.CharField(max_length=255)
    PI = models.CharField(max_length=255)
    SubProject = models.CharField(max_length=255, blank=True)
    Subject = models.CharField(max_length=255, blank=True)
    Manager = models.CharField(max_length=255, blank=True)
    type = models.ForeignKey(Experiment_type)
    
    
    fraction = models.IntegerField()
    repeat = models.IntegerField()
    name = models.CharField(max_length=255, blank=True)
    samples = models.ManyToManyField(Sample, through='Experiment_sample')
    reagents = models.ManyToManyField(Reagent, through='Experiment_reagent')

    separation = models.CharField(max_length=255)
    separation_methods = models.ManyToManyField(Separation_method, through='Experiment_separation')
    separation_ajustments = models.TextField()
    
    digest_type = models.ForeignKey(Digest_type)
    digest_enzyme = models.ForeignKey(Digest_enzyme)
    
    ################add ForeignKey################
    quantificationMethod = models.ForeignKey(Quantification_Methods, default=1)#zdd
    workflowMode = models.ForeignKey(Workflow_mode, default=1)  #zdd
    searchEngine = models.ForeignKey(searchEngine, default=1)   #xiaotian
    #timestamp = models.ForeignKey(ExpNo_TimeStamp)                #xiaotian
    
    instrument_manufacturer = models.ForeignKey(Instrument_manufacturer)
    instrument_name = models.ForeignKey(Instrument)
    ms1 = models.ForeignKey(Instrument_MS1)
    ms1_details = models.ForeignKey(Instrument_MS1_tol)
    ms2 = models.ForeignKey(Instrument_MS2)
    ms2_details = models.ForeignKey(Instrument_MS2_tol)
    fixed_modifications = models.ManyToManyField(Fixed_Modification)
    dynamic_modifications = models.ManyToManyField(Dynamic_Modification)
    comments_conclusions = models.TextField()
    description = models.TextField()
    fm_no = models.CharField(max_length=255, blank=True)
    taxid = models.CharField(max_length=255, blank=True)
    search_database=models.ForeignKey(Search_database)
    
    #zdd add the field
    #pre_separation_methods: "Online", "Offline", "None"
    pre_separation_methods = models.CharField(max_length=255)
    
#     def __unicode__(self):
#         return self.id

#+++++++++++++++++++++++++ Experiment Separation Model ++++++++++++++++++++++++
class Experiment_pre_separation_methods(models.Model):
    name = models.CharField(max_length=255)
    validated = models.BooleanField(default=False)
    def __unicode__(self):
        return self.name
    

class Experiment_separation(models.Model):
    experiment = models.ForeignKey(Experiment)
    #methods = models.ForeignKey(Experiment_pre_separation_methods)
    separation_method = models.ForeignKey(Separation_method)
    method_order = models.IntegerField()
    separation_num = models.IntegerField()

    def __unicode__(self):
        return self.separation_method.name

#+++++++++++++++++++++++++ Experiment Reagent Model +++++++++++++++++++++++++++++

class Experiment_reagent(models.Model):
    experiment = models.ForeignKey(Experiment)
    reagent = models.ForeignKey(Reagent)
    amount = models.CharField(max_length=255)
    amount_unit=models.CharField(max_length=255)
    method = models.ForeignKey(Reagent_method)
    wash_buffer = models.ForeignKey(Reagent_buffer)
    ajustments = models.TextField()

#+++++++++++++++++++++++++ Experiment Sample  Model +++++++++++++++++++++++++++++

class Experiment_sample(models.Model):
    experiment = models.ForeignKey(Experiment)
    sample = models.ForeignKey(Sample)
    amount = models.CharField(max_length=255)
    amount_unit=models.CharField(max_length=255)
    ajustments = models.TextField()
    
############################add child user####################################
############################add child user####################################
#from django.contrib.auth.models import AuthUser
class AuthChildUser(models.Model):
    id = models.OneToOneField(User, db_column='id', primary_key=True)
    child_username = models.CharField(max_length=90, unique=True)
    child_password = models.CharField(max_length=384, unique=False)
    child_email= models.CharField(max_length=384, unique=False)
    child_last_login = models.DateTimeField()
    child_date_joined = models.DateTimeField()
    child_is_active = models.BooleanField(default=True)
    child_annotation = models.TextField()
    class Meta:
        db_table = u'auth_child_user'
    #first_name = models.CharField(max_length=90)
    #last_name = models.CharField(max_length=90)
    #email = models.CharField(max_length=225)
    #is_staff = models.IntegerField()
    #is_superuser = models.IntegerField()
    
class AuthParentChildAssociation(models.Model):
    parent = models.ForeignKey(User, unique=False)
    child = models.ForeignKey(AuthChildUser)
    class Meta:
        db_table = u'auth_parent_child_association'

class AuthChildUserAndSharedExp(models.Model):
    child = models.ForeignKey(AuthChildUser)
    sharedExp = models.TextField()
    isActive = models.BooleanField(default=True)
    class Meta:
        db_table = u'auth_child_user_and_shared_experiments'

class PublicExperiments(models.Model):
    expName = models.CharField(max_length=255, unique=False)
    isPublic = models.BooleanField(default=True)
    owner = models.CharField(max_length=255, unique=False)

# MIAPE Metadata

class Miape_ExpType(models.Model):
    name = models.CharField(max_length=255, unique=True)
    validated = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name
        
class Miape_Species(models.Model):
    name = models.CharField(max_length=255, unique=True)
    validated = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name
        
class Miape_Tissue(models.Model):
    name = models.CharField(max_length=255, unique=True)
    validated = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name
        
class Miape_Modification(models.Model):
    name = models.CharField(max_length=255, unique=True)
    validated = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name
        
class Miape_Instrument(models.Model):
    name = models.CharField(max_length=255, unique=True)
    validated = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name
        
class Miape_CellType(models.Model):
    name = models.CharField(max_length=255, unique=True)
    validated = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name
        
class Miape_Disease(models.Model):
    name = models.CharField(max_length=255, unique=True)
    validated = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name
        
class Miape_QuantMethod(models.Model):
    name = models.CharField(max_length=255, unique=True)
    validated = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name
        
        