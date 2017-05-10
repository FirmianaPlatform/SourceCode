'''
Created on 2015-01-22

@author: garfield
'''
from django.conf.urls import patterns
urlpatterns = patterns('api.views',
                       #(r'^$', 'api'),
                       
                       #metadata
                       (r'^meta/experiment/$', 'experimentMeta'),
                       (r'^meta/sample/$', 'sampleMeta'),
                       (r'^meta/reagent/$', 'reagentMeta'),
                       (r'^meta/experimentData/$', 'experimentDataMeta'),
                       
                       #gar_download
                       (r'^gar_download/download/$', 'downloadData'),
                       
                       #gardener
                       (r'^gardener/showDbData/$', 'showDbDataByFilterGardener'),
                       (r'^gardener/showGeneData/$', 'showGeneDataGardener'),
                       (r'^gardener/showPeptideData/$', 'showPeptideDataGardener'),
                       (r'^gardener/showProteinData/$', 'showProteinDataGardener'),
                       (r'^gardener/show3DplotData/$', 'show3DplotDataGardener'),
                       (r'^gardener/show3DplotDataDemo/$', 'show3DplotDataGardenerDemo'),
                       (r'^gardener/show3DplotDataDemoForSpecificSymbol/$', 'show3DplotDataGardenerDemoForSpecificSymbol'),
                       (r'^gardener/ppi_analysis/$', 'getPPIDataDemo'),

                       #showDbDataByFilterApi
                       )
