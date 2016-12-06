from django.contrib import admin
from django.contrib.auth.models import *

from experiments.models import *

admin.site.register(Experimenter)
admin.site.register(Project)
#admin.site.register(Lab)
admin.site.register(All_Experimenter)

#----ajax-------
admin.site.register(Conjugate)
admin.site.register(Purification)
admin.site.register(React_species)
admin.site.register(Reagent_manufacturer)
admin.site.register(Affinity)
admin.site.register(Application)


admin.site.register(Rx_treatment)
admin.site.register(Ubi_subcell)
admin.site.register(Ubi_method)
admin.site.register(Ubi_detergent)
admin.site.register(Ubi_salt)
admin.site.register(Source_taxon)
admin.site.register(Genotype)
admin.site.register(Cell_type)
admin.site.register(Tissue_gender)
admin.site.register(Tissue_strain)
admin.site.register(Tissue_type)

admin.site.register(Instrument_administrator)
admin.site.register(Instrument_manufacturer)
admin.site.register(Digest_type)
admin.site.register(Digest_enzyme)
admin.site.register(Reagent_buffer)
admin.site.register(Reagent_method)
admin.site.register(Separation_method)
admin.site.register(Antigen_species)
admin.site.register(Antigen_clonal_type)
admin.site.register(Antigen_modification)

#-------------------------------------------

admin.site.unregister(Group)
