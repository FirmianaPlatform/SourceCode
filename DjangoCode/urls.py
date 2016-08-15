'''
Created on 2013-7-10

@author: garfield
'''
from django.conf.urls import patterns
urlpatterns = patterns('gardener.views',
                       (r'^$', 'gardener'),
                       # (r'^showdatabase/$', 'showdatabase'),
                       (r'^data/showdatabase/$', 'showdatabase_data'),
                       (r'^data/showsearch/$', 'showsearch_data'),
                       (r'^data/showjob/$', 'showjob'),

                       (r'^data/showpeptide/$', 'showpeptide_data'),
                       (r'^data/showprotein/$', 'showprotein_data'),
                       (r'^data/showgene/$', 'showgene_data'),

                       (r'^data/silacpeptide/$', 'silac_peptide'),
                       (r'^data/silacprotein/$', 'silac_protein'),
                       (r'^data/silacgene/$', 'silac_genes'),
                       (r'^data/silacpeptide_compare/$', 'silac_peptide_compare'),
                       (r'^data/silacprotein_compare/$', 'silac_protein_compare'),
                       (r'^data/silacgene_compare/$', 'silac_genes_compare'),

                       (r'^data/showms1_tic_data/$', 'showms1_tic_data'),
                       (r'^data/sum_pep_viewer/$', 'sum_pep_viewer'),
                       (r'^peptide_viwer/$', 'peptide_viwer'),
                       (r'^data/get_rank/$', 'get_rank'),
                       (r'^data/show_tic_fraction/$', 'show_tic_fraction'),

                       (r'^data/downdatabase/$', 'download_database'),
                       (r'^data/downgene/$', 'download_gene'),
                       (r'^data/downprotein/$', 'download_protein'),
                       (r'^data/downpeptide/$', 'download_peptide'),
                       (r'^genome/$', 'protein2Genome'),

                       (r'^rplot/$', 'rplot'),
                       (r'^venn_plot/$', 'venn_plot'),
                       (r'^kegg_statistic/$', 'kegg_statistic'),
                       (r'^system_state/$', 'system_state'),

                       (r'^mecompare/$', 'mecompare'),
                       (r'^mecompare_peptide/$', 'mecompare_peptide'),
                       (r'^newcompare/$', 'newcompare'),

                       (r'^newcmpprotein/$', 'newcmp_protein'),
                       (r'^newcmp_pcaAdjust/$', 'newcmp_pcaAdjust'),

                       (r'^newcmptree/$', 'newcmp_tree'),
                       (r'^newcmpcalc/$', 'newcmp_calc'),
                       (r'^newcmp_peptide/$', 'newcmp_peptide'),
                       (r'^com_getheaders/$', 'newcmp_getheader'),
                       (r'^ispec_output/$', 'ispec_output'),
                       (r'^help/$', 'help'),

                       (r'^sendtopublic/$', 'sendtopublic'),
                       (r'^userAnnotation/$', 'userAnnotation'),

                       (r'^PepLocation/$', 'PepLocation'),
                       (r'^coverage/$', 'coverage'),
                       (r'^firmiana_ppi/$', 'ppi_xiaotian'),
                       (r'^firmiana_ppi_analysis/$', 'ppi_xiaotian_analysis'),
                       (r'^tf/$', 'tf_ppi'),
                       
                       #20160808 for registration by zdd
                       (r'^addACompany/$', 'addACompany'), #http://www.firmiana.org/gardener/addACompany/
                       (r'^addALaboratory/$', 'addALaboratory'), #http://www.firmiana.org/gardener/addALaboratory/
                       )
