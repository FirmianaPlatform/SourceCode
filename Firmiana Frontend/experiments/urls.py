from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

 
"""
urlpatterns = patterns('',
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
"""
urlpatterns = patterns('experiments.views',
    #(r'^experiments/sample/', sample),
    (r'^experiment/$', 'experiment'),
    (r'^reagent/$', 'reagent'),
    (r'^sample/$', 'sample'),
    (r'^form/reagent/$', 'reagent_form'),
    (r'^form/sample/$', 'sample_form'),
    (r'^form/experiment/$', 'experiment_form'),
    (r'^edit/reagent/$', 'reagent_edit'),
    (r'^edit/sample/$', 'sample_edit'),
    (r'^edit/experiment/$', 'experiment_edit'),
    (r'^load/reagent/$', 'reagent_load'),
    (r'^load/sample/$', 'sample_load'),
    (r'^load/experiment/$', 'experiment_load'),
    (r'^loadnew/experiment/$', 'experiment_loadnew'),
    (r'^data/reagent/$', 'reagent_data'),
    (r'^data/sample/$', 'sample_data'),
    (r'^data/experiment/$', 'experiment_data'),
    (r'^ajax/experiment_no/$', 'experiment_no'),
    (r'^ajax/sample_no/$', 'sample_no'),
    (r'^ajax/reagent_no/$', 'reagent_no'),
    (r'^save/reagent/$', 'reagent_save'),
    (r'^save/experiment/$', 'experiment_save'),
    (r'^save/sample/$', 'sample_save'),
    (r'^save/upload/$','fasta_upload'),
    (r'^save/new_modification/$','add_new_modifications'),
    (r'^editsave/reagent/$', 'reagent_edit_save'),
    (r'^editsave/experiment/$', 'experiment_edit_save'),
    (r'^editsave/sample/$', 'sample_edit_save'),
    (r'^delete/reagent/$', 'reagent_edit_delete'),
    (r'^delete/experiment/$', 'experiment_edit_delete'),
    (r'^delete/sample/$', 'sample_edit_delete'),
    (r'^data/sample_short/$', 'sample_short'),
    (r'^data/reagent_short/$', 'reagent_short'),
    (r'^ajax/display/(.*)/$', 'record_display'),
    (r'^ajax/display2/(.*)/$', 'record_display2'),
    (r'^ajax/experimenter/$', 'experimenter'),
    (r'^ajax/treatment_detail/$', 'treatment_detail'),
    (r'^ajax/unit_detail/$', 'unit_detail'),
    (r'^ajax/all_company/$', 'all_company'),
    (r'^ajax/all_lab/$', 'all_lab'),
    (r'^ajax/instrument_ms1/$', 'instrument_ms1'),
    (r'^ajax/instrument_ms2/$', 'instrument_ms2'),
    (r'^ajax/instrument_ms1_tol/$', 'instrument_ms1_tol'),
    (r'^ajax/instrument_ms2_tol/$', 'instrument_ms2_tol'),
    (r'^ajax/all_experimenter/$', 'all_experimenter'),
    (r'^ajax/Source_TissueTaxonID/$', 'source_tissueTaxonID'),
    (r'^ajax/Source_TissueTaxonName/$', 'source_tissueTaxonName'),
    (r'^ajax/Source_TissueTaxonAorM/$', 'source_tissueTaxonAorM'),
    (r'^ajax/Source_TissueTaxonStrain/$', 'source_tissueTaxonStrain'),
    (r'^ajax/Source_TissueSystem/$', 'sourcetissueSystem'),
    (r'^ajax/Source_TissueOrgan/$', 'sourcetissueOrgan'),
    (r'^ajax/ContainNoStore/$', 'ContainNoStore'),
    (r'^ajax/ContainBasketStore/$', 'ContainBasketStore'),
    (r'^ajax/ContainLayerStore/$', 'ContainLayerStore'),
    (r'^getPrideFileList/$', 'getPrideFileList'),
    
    (r'^manageChildAccount/$', 'manageChildAccount'),
    (r'^getAllChildAccountInfo/$', 'getAllChildAccountInfo'),
    (r'^getVisibleExpListByUserId/$', 'getVisibleExpListByUserId'),
    (r'^getRawFileListByExpName/$', 'getRawFileListByExpName'),
    (r'^downloadRawFileByExpNameAndFileName/$', 'downloadRawFileByExpNameAndFileName'),
    (r'^publicExperiments/$', 'gardener_publicExperiments'),
    
    
    
    
    
    
)
urlpatterns += patterns('display.views',
    (r'^data/spec/$', 'spec_data'),
    (r'^specview/$', 'spec_view'),
    (r'^figure/sensitivity/$', 'plot_sensitivity'),
    (r'^figure/model/$', 'plot_model'),
    (r'^quant_control/$', 'quant_control'),
)
