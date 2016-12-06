from django.contrib import admin
from django.contrib.auth.models import *
from experiments.models import *

admin.site.register(Experimenter)
admin.site.register(All_Company)
admin.site.register(All_Laboratory)

'''
class User_LaboratoryAdmin(admin.ModelAdmin):
    list_display = ('lab', 'user', 'validated')
    raw_id_fields = ('lab', 'user', 'validated')
admin.site.register(User_Laboratory, User_LaboratoryAdmin)
'''

class All_ExperimenterAdmin(admin.ModelAdmin):
    list_display = ('name', 'lab', 'validated')
    #raw_id_fields = ('name', 'lab', 'validated')
admin.site.register(All_Experimenter, All_ExperimenterAdmin)

class Experimenter_infoAdmin(admin.ModelAdmin):
    list_display = ('company', 'lab', 'experimenter')
admin.site.register(Experimenter_info, Experimenter_infoAdmin)

#Refirgerator
admin.site.register(Refrigerator_No)
admin.site.register(Refrigerator_Temperature)
admin.site.register(Refrigerator_Layer)
#Nitrogen
admin.site.register(Nitrogen_Container)
admin.site.register(Nitrogen_Basket)
admin.site.register(Nitrogen_Layer)
#Others
admin.site.register(Others_Temperature)

#Container
admin.site.register(Container)
class Container_NoAdmin(admin.ModelAdmin):
    list_display = ('name', 'Container', 'validated')
    #raw_id_fields = ('name', 'Container', 'validated')
admin.site.register(Container_No, Container_NoAdmin)

class Container_BasketAdmin(admin.ModelAdmin):
    list_display = ('name', 'Container', 'validated')
    #raw_id_fields = ('name', 'Container', 'validated')
admin.site.register(Container_Basket, Container_BasketAdmin)

class Container_LayerAdmin(admin.ModelAdmin):
    list_display = ('name', 'Container', 'validated')
    #raw_id_fields = ('name', 'Container', 'validated')
admin.site.register(Container_Layer, Container_LayerAdmin)

admin.site.register(All_AgeUnit)

#Source
admin.site.register(Source_TissueTaxonAorM)

class Source_TissueSystemAdmin(admin.ModelAdmin):
    list_display = ('name', 'pid', 'validated')
    #raw_id_fields = ('name', 'pid', 'validated')
admin.site.register(Source_TissueSystem, Source_TissueSystemAdmin)

class Source_TissueOrganAdmin(admin.ModelAdmin):
    list_display = ('name', 'pid', 'validated')
    #raw_id_fields = ('name', 'pid', 'validated')
admin.site.register(Source_TissueOrgan, Source_TissueOrganAdmin)

class Source_TissueStructureAdmin(admin.ModelAdmin):
    list_display = ('name', 'pid', 'validated')
    #raw_id_fields = ('name', 'pid', 'validated')
admin.site.register(Source_TissueStructure, Source_TissueStructureAdmin)

class Source_TissueTaxonIDAdmin(admin.ModelAdmin):
    list_display = ('name', 'pid', 'validated')
    #raw_id_fields = ('name', 'pid', 'validated')
admin.site.register(Source_TissueTaxonID, Source_TissueTaxonIDAdmin)

class Source_TissueTaxonStrainAdmin(admin.ModelAdmin):
    list_display = ('name', 'pid', 'validated')
    #raw_id_fields = ('name', 'pid', 'validated')
admin.site.register(Source_TissueTaxonStrain, Source_TissueTaxonStrainAdmin)

class Source_TissueTaxonNameAdmin(admin.ModelAdmin):
    list_display = ('name', 'abbrev', 'pid', 'validated')
    #raw_id_fields = ('name', 'abbrev', 'pid', 'validated')
admin.site.register(Source_TissueTaxonName, Source_TissueTaxonNameAdmin)
admin.site.register(Source_TissueType)
admin.site.register(source_CellType)

class Cell_NameAdmin(admin.ModelAdmin):
    list_display = ('name', 'abbrev', 'pid', 'validated')
    #raw_id_fields = ('name', 'abbrev', 'pid', 'validated')
admin.site.register(Cell_Name, Cell_NameAdmin)

admin.site.register(Fluid_name)
admin.site.register(Experiment_group)
admin.site.register(Galaxy_session)


class copartnerAdmin(admin.ModelAdmin):
    list_display = ('from_experimenter', 'to_experimenter')
    #raw_id_fields = ('from_experimenter', 'to_experimenter')
admin.site.register(copartner, copartnerAdmin)


admin.site.register(Project)


#Reagent Model 
admin.site.register(Conjugate)
admin.site.register(Purification)
admin.site.register(React_species)
admin.site.register(Reagent_manufacturer)
admin.site.register(Affinity)
admin.site.register(Application)

#Reagent Type Model
admin.site.register(Antigen_species)
admin.site.register(Antigen_clonal_type)
admin.site.register(Antigen_modification)
class AntigenAdmin(admin.ModelAdmin):
    list_display = ('gene_id', 'host_species', 'clonal_type', 'modification')
    #raw_id_fields = ('gene_id', 'host_species', 'clonal_type', 'modification')
admin.site.register(Antigen, AntigenAdmin)

admin.site.register(Dna_info)
admin.site.register(Domain_info)
admin.site.register(Chemical_info)
admin.site.register(Remarks_info)
class ReagentAdmin(admin.ModelAdmin):
    list_display = ('experimenter', 'date', 'type', 'name', 'manufacturer', 'catalog_no', 'conjugate', 'antigen', 'dna_info', 'domain_info', 'chemical_info', 'remarks_info')
    #raw_id_fields = ('experimenter', 'date', 'type', 'name', 'manufacturer', 'catalog_no', 'applications', 'react_species_sources', 'react_species_targets', 'conjugate', 'antigen', 'dna_info', 'domain_info', 'chemical_info', 'remarks_info')
admin.site.register(Reagent, ReagentAdmin)






