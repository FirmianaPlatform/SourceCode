from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.loader import get_template
from django.contrib.auth.models import User
from django.contrib.auth import logout, login, authenticate
from django.http import StreamingHttpResponse
from django.contrib.auth import get_user
# from experiments.forms import *
from experiments.models import *
from gardener.models import Experiment as gard_experiment
# from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
import json
from datetime import date, datetime
import datetime
from lxml import etree
from ftplib import FTP
from urlparse import urlparse

import experiments_filters

# from experiments.manageChildAccount import * #manage sub-account
from experiments.manageChildAccount import addChildAccount
from experiments.manageChildAccount import activateChildAccount
from experiments.manageChildAccount import freezeChildAccount
from experiments.manageChildAccount import deleteChildAccount
from experiments.manageChildAccount import addParentAndChildAssocitions
from experiments.manageChildAccount import addChildUserSharedExp
from experiments.manageChildAccount import updateChildAccountSharedExp
from experiments.manageChildAccount import showAllChildAccountInfo
from experiments.manageChildAccount import childHasExistedByID
from experiments.manageChildAccount import childHasExistedByName
from experiments.manageChildAccount import isChildAccount
from experiments.manageChildAccount import isActive_ChildUser
from experiments.manageChildAccount import isParentAccount
from experiments.manageChildAccount import isGuest
from experiments.manageChildAccount import isValidatedUser
from experiments.manageChildAccount import showVisibleExperiments_gardenerExperiment
from experiments.manageChildAccount import showExperiments_ViewRawFiles
from experiments.manageChildAccount import showRawFileListByExpName
from experiments.manageChildAccount import promptJson
from experiments.manageChildAccount import showAbsPath_Exp_RawFile
from experiments.manageChildAccount import publicExperiments

rawFilesPathInFirmiana = '/usr/local/firmiana/'

#+++++++++++++++++++++++++++++++++++++++++++++++++++++

#+++++++++++++++++++++++++++++++++++++++++++++++++++++


#--------- experiment display and form view ------------------------
# @login_required(login_url="/login/")
def experiment(request):
    variables = RequestContext(request, {})
    return render_to_response('experiments/experiment.html', variables)
    response["P3P"] = 'CP="IDC DSP COR ADM DEVi TAIi PSA PSD IVAi IVDi CONi HIS OUR IND CNT"'

# @login_required(login_url="/login/")
def experiment_form(request):
    variables = RequestContext(request, {})
    return render_to_response('experiments/experiment_form.html', variables)
    response["P3P"] = 'CP="IDC DSP COR ADM DEVi TAIi PSA PSD IVAi IVDi CONi HIS OUR IND CNT"'

#-------- reagent display and form view
# @login_required(login_url="/login/")
def reagent(request):
    variables = RequestContext(request, {})
    return render_to_response('experiments/reagent.html', variables)
    response["P3P"] = 'CP="IDC DSP COR ADM DEVi TAIi PSA PSD IVAi IVDi CONi HIS OUR IND CNT"'

# @login_required(login_url="/login/")
def reagent_form(request):
    variables = RequestContext(request, {})
    return render_to_response('experiments/reagent_form.html', variables)
    response["P3P"] = 'CP="IDC DSP COR ADM DEVi TAIi PSA PSD IVAi IVDi CONi HIS OUR IND CNT"'

#-------- sample display and form view
# @login_required(login_url="/login/")
def sample(request):
    variables = RequestContext(request, {})
    return render_to_response('experiments/sample.html', variables)
    response["P3P"] = 'CP="IDC DSP COR ADM DEVi TAIi PSA PSD IVAi IVDi CONi HIS OUR IND CNT"'

# @login_required(login_url="/login/")
def sample_form(request):
    variables = RequestContext(request, {})
    return render_to_response('experiments/sample_form.html', variables)
    response["P3P"] = 'CP="IDC DSP COR ADM DEVi TAIi PSA PSD IVAi IVDi CONi HIS OUR IND CNT"'

#-------------------------------------------------------------------------------------#
# sample  reagent and experiment view for accepting and storing information submitted.#
#-------------------------------------------------------------------------------------#
# @login_required(login_url="/login/")
def sample_save(request):
    if request.method == 'POST':
        # user = User.objects.get(username=request.POST['experimenter'])
          # maybe some people will have same name..s
        company = All_Company.objects.get(name=request.POST['company'])
        lab = All_Laboratory.objects.get(name=request.POST['lab'])
        experimenter = All_Experimenter.objects.filter(name=request.POST['experimenter']).filter(lab=lab)[0]
        (exp_info, sign) = Experimenter_info.objects.get_or_create(
                                                         company=company,
                                                         lab=lab,
                                                         experimenter=experimenter
                                                         )
        (month, day, year) = request.POST['date'].split('/')
        sample_date = date(int(year), int(month), int(day))
        #print s
        (container, sign) = Container.objects.get_or_create(name=request.POST['location'])
        if request.POST['location'] == 'Refrigerator':
            container_No = Refrigerator_No.objects.get(name=request.POST['RefrigeratorNo'])
            container_basket = Refrigerator_Temperature.objects.get(name=request.POST['RefrigeratorTemper'])
            container_layer = Refrigerator_Layer.objects.get(name=request.POST['RefrigeratorLayer'])
            (refrigerator, sign) = Location_Refrigerator.objects.get_or_create(
                                               no=container_No,
                                               temperature=container_basket,
                                               layer=container_layer
                                               )
            (location, sign) = Location.objects.get_or_create(
                                                      refrigerator=refrigerator
                                                      )
        elif request.POST['location'] == 'Liquid Nitrogen':
            container_No = Nitrogen_Container.objects.filter(name=request.POST['Nitrogen_Container'])[0]
            container_basket = Nitrogen_Basket.objects.filter(name=request.POST['Nitrogen_Basket'])[0]
            container_layer = Nitrogen_Layer.objects.filter(name=request.POST['Nitrogen_Layer'])[0]
            (nitrogen, sign) = Location_Nitrogen.objects.get_or_create(
                                                             no=container_No,
                                                             basket=container_basket,
                                                             layer=container_layer,
                                                             )
            (location, sign) = Location.objects.get_or_create(
                                                      nitrogen=nitrogen
                                                      )
        elif request.POST['location'] == 'Others':
            temperature = Others_Temperature.objects.get(name=request.POST['Others_Temperature'])
            locations = request.POST['Others_location']
            (locationOthers, sign) = Location_Others.objects.get_or_create(
                                                                   temperature=temperature,
                                                                   location=locations  
                                                             )
            (location, sign) = Location.objects.get_or_create(
                                                      others=locationOthers
                                                      )
        # (ubi_detergent, sign) = Ubi_detergent.objects.get_or_create(name=request.POST['Ubi_detergent'])
        # (ubi_salt, sign) = Ubi_salt.objects.get_or_create(name=request.POST['Ubi_salt'])
        #=======================================================================
        # (rx_treatments, sign) = Rx_treatment.objects.get_or_create(name=request.POST['Rx_treatment'])
        # (rx_treatments_detail, sign) = Rx_treatment_detail.objects.get_or_create(name=request.POST['all_detail'], type=rx_treatments)
        #=======================================================================
        sample = Sample(date=sample_date,
                    experimenter=exp_info,
                    location=location,
                    # location=request.POST['location'],
                    # rx_treatments=rx_treatments,
                    # rx_treatments_detail=rx_treatments_detail,
                    # rx_amount=request.POST['amount'],
                    # rx_unit_deatil=rx_unit_deatil,
                    # rx_duration=request.POST['duration'],
                    # rx_duration_time=
                    # ubi_detergent=ubi_detergent,
                    # rx_unit=rx_unit,
                    ubi_salt=request.POST['Ubi_salt'],
                    ext_comments=request.POST['comments'],
                    ispec_no=request.POST['Ispec_num'])
        sample.save()
        #=======================================================================
        # if request.POST['Rx_treatment'] != 'None':
        #     (rx_unit, sign) = Rx_unit.objects.get_or_create(name=request.POST['Rx_unit'])
        #     try:
        #         if request.POST['Rx_unit'] != 'Concentration':
        #             (rx_unit_deatil, sign) = Rx_unit_detail.objects.get_or_create(name=request.POST['unit_detail'],
        #                                                                           type=rx_unit
        #                                                                           )
        #         else:
        #             (rx_unit_deatil, sign) = Rx_unit_detail.objects.get_or_create(name=request.POST['unit_detail2'] + '\\' + request.POST['unit_detail22'],
        #                                                                           type=rx_unit
        #                                                                           )
        #     except:
        #         (rx_unit_deatil, sign) = Rx_unit_detail.objects.get_or_create(name='None',
        #                                                             type=rx_unit
        #                                                             )
        #          
        #         sample.rx_amount = request.POST['amount']
        #         sample.rx_unit = rx_unit
        #         sample.rx_unit_deatil = rx_unit_deatil
        #         sample.rx_duration = request.POST['duration'],
        #         sample.rx_duration_time = request.POST['rx_dur_unit'],
        #=======================================================================
        treat_num = int(request.POST['treat_num'])
        for treat_order in range(1, treat_num + 1):
            if request.POST['Rx_treatment' + str(treat_order)] != 'None':
                if request.POST['Rx_treatment' + str(treat_order)] != 'Gene Engineering':
                    (rx_unit, sign) = Rx_unit.objects.get_or_create(name=request.POST['Rx_unit' + str(treat_order)])
                    # try:
                    if request.POST['Rx_unit' + str(treat_order)] != 'Concentration':
                        (rx_unit_deatil, sign) = Rx_unit_detail.objects.get_or_create(name=request.POST['unit_detail_' + str(treat_order)],
                                                                                      type=rx_unit
                                                                                      )
                    else:
                        (rx_unit_deatil, sign) = Rx_unit_detail.objects.get_or_create(name=request.POST['unit_detail2_' + str(treat_order)] + '/' + request.POST['unit_detail22_' + str(treat_order)],
                                                                                      type=rx_unit
                                                                                      )
                #===============================================================
                # except:
                #     (rx_unit_deatil, sign) = Rx_unit_detail.objects.get_or_create(name='None',
                #                                                         type=rx_unit
                #                                                         )
                #===============================================================
                 
                    rx_amount = request.POST['amount' + str(treat_order)]
                else:
                    rx_amount = ''
                    rx_unit = ''
                    rx_unit_deatil = ''
                rx_duration = request.POST['duration' + str(treat_order)]
                rx_duration_time = request.POST['rx_dur_unit' + str(treat_order)]
                (rx_treatments, sign) = Rx_treatment.objects.get_or_create(name=request.POST['Rx_treatment' + str(treat_order)])
                (rx_treatments_detail, sign) = Rx_treatment_detail.objects.get_or_create(name=request.POST['all_detail' + str(treat_order)], type=rx_treatments)
                treatment = Treatment(
                                    rx_treatments=rx_treatments,
                                    rx_treatments_detail=rx_treatments_detail,
                                    rx_duration=rx_duration,
                                    rx_duration_time=rx_duration_time,
                                    )
                treatment.save()
                if request.POST['Rx_treatment' + str(treat_order)] != 'Gene Engineering':
                    treatment.rx_amount = rx_amount
                    treatment.rx_unit = rx_unit
                    treatment.rx_unit_deatil = rx_unit_deatil
                    treatment.save()
                try:
                    geneTaxon = Source_TissueTaxonID.objects.filter(name=request.POST['newGeneTaxon' + str(treat_order)])[0]
                    geneSymbol = request.POST['newGeneSymbol' + str(treat_order)]
                    geneID = request.POST['newGeneID' + str(treat_order)]
                    treatment.geneTaxon = geneTaxon
                    treatment.geneSymbol = geneSymbol
                    treatment.geneID = geneID
                    treatment.save()
                except:
                    treatment.save()
            sample.treatments.add(treatment) 
        cell_tissue = request.POST['cell_tissue']
        #sample.cell_tissue = cell_tissue
        if cell_tissue == 'Tissue':
            (AorM, sign) = Source_TissueTaxonAorM.objects.get_or_create(name=request.POST['Source_TissueTaxonAorM'])
            (tissueName, sign) = Source_TissueTaxonName.objects.get_or_create(name=request.POST['tissueName'])
            (tissueID, sign) = Source_TissueTaxonID.objects.get_or_create(name=request.POST['tissueID'])
            tissueStrain = Source_TissueTaxonStrain.objects.filter(pid__name=request.POST['tissueID']).filter(name=request.POST['tissueStrain'])[0]
            
            # (taxon, sign) = Source_taxon.objects.get_or_create(name=request.POST['Source_taxon'])
            # (type, sign) = Tissue_type.objects.get_or_create(name=request.POST['Tissue_type'])
            (gender, sign) = Tissue_gender.objects.get_or_create(name=request.POST['Tissue_gender'])
            # (strain, sign) = Tissue_strain.objects.get_or_create(name=request.POST['Tissue_strain'])
            (genotype, sign) = Genotype.objects.get_or_create(name=request.POST['Genotype'])
            (tissueSystem, sign) = Source_TissueSystem.objects.get_or_create(name=request.POST['Source_TissueSystem'])
            (tissueOrgan, sign) = Source_TissueOrgan.objects.get_or_create(name=request.POST['Source_TissueOrgan'], pid=tissueSystem)
            tissueStructure = request.POST['Source_TissueStructure']
            (tissueType, sign) = Source_TissueType.objects.get_or_create(name=request.POST['Source_TissueType'])
            #===================================================================
            # if request.POST['geneTaxon'] != 'Gene Taxon':
            #     geneTaxon = Source_TissueTaxonID.objects.filter(name=request.POST['geneTaxon'])[0]
            #===================================================================
            # changes = request.POST['changes']
            age = request.POST['tissue_age']
            (age_unit, sign) = All_AgeUnit.objects.get_or_create(name=request.POST['All_AgeUnit'])
            try:
                circ_time = request.POST['circ_time']
            except:
                circ_time = ''
            gene_num = int(request.POST['Gene_num'])
            gene = ''
            for gene_order in range(1, gene_num + 1):
                gene = gene + request.POST['geneSymbol' + str(gene_order)] + '|' + request.POST['GeneID' + str(gene_order)] + '|' + request.POST['geneTaxon' + str(gene_order)] + ';'
            gene = gene[:-1]
            specific_ID = request.POST['Specific_ID']
            source_tissue = Source_tissue(AorM=AorM,
                                          tissueName=tissueName,
                                          tissueID=tissueID,
                                          tissueStrain=tissueStrain,
                                          gender=gender,
                                          tissueSystem=tissueSystem,
                                          tissueOrgan=tissueOrgan,
                                          tissueType=tissueType,
                                          genotype=genotype,
                                          gene=gene,
                                          tissueStructure=tissueStructure,
                                          # geneTaxon=geneTaxon,
                                          # geneSymbol=request.POST['geneSymbol'],
                                          # geneID=request.POST['GeneID'],
                                          age=age,
                                          age_unit=age_unit,
                                          circ_time=circ_time,
                                          specific_ID=specific_ID)
            source_tissue.save()
            #===================================================================
            # if request.POST['Genotype'] != 'Wild type':
            #     source_tissue.geneTaxon = geneTaxon
            #     source_tissue.geneSymbol = request.POST['geneSymbol']
            #     source_tissue.geneID = request.POST['GeneID']
            #===================================================================
            source_tissue.save()
            sample.source_tissue = source_tissue
            sample.save()
        
        elif cell_tissue == 'Cell':
            # (taxon, sign) = Tissue_source.objects.get_or_create(name=request.POST['Source_taxon'])
            (AorM, sign) = Source_TissueTaxonAorM.objects.get_or_create(name=request.POST['Source_TissueTaxonAorM'])
            tissueName = Source_TissueTaxonName.objects.filter(name=request.POST['tissueName'])[0]
            (tissueID, sign) = Source_TissueTaxonID.objects.get_or_create(name=request.POST['tissueID'])
            tissueStrain = Source_TissueTaxonStrain.objects.filter(pid__name=request.POST['tissueID']).filter(name=request.POST['tissueStrain'])[0]
            # (taxon, sign) = Source_taxon.objects.get_or_create(name=request.POST['Source_taxon'])
            # (type, sign) = Cell_type.objects.get_or_create(name=request.POST['Cell_type'])
            # (genotype, sign) = Genotype.objects.get_or_create(name=request.POST['Genotype'])
            # changes = request.POST['changes']
            # age is not available for cells
            try:
                circ_time = request.POST['circ_time']
            except:
                circ_time = ''
            (genotype, sign) = Genotype.objects.get_or_create(name=request.POST['Genotype'])
            try:
                circ_time = request.POST['circ_time']
            except:
                circ_time = ''
            gene_num = int(request.POST['Gene_num'])
            gene = ''
            for gene_order in range(1, gene_num + 1):
                gene = gene + request.POST['geneSymbol' + str(gene_order)] + '|' + request.POST['GeneID' + str(gene_order)] + '|' + request.POST['geneTaxon' + str(gene_order)] + ';'
            gene = gene[:-1]
            source_cell = Source_cell(AorM=AorM,
                                      tissueName=tissueName,
                                      tissueID=tissueID,
                                      tissueStrain=tissueStrain,
                                      genotype=genotype,
                                      gene=gene,
                                      circ_time=circ_time,
                                      specific_ID=request.POST['Specific_ID'])
            source_cell.save()
            if request.POST['Source_TissueTaxonAorM'] != 'Microorganism':
                (celltype, sign) = source_CellType.objects.get_or_create(name=request.POST['cellcelltype'])
                (cellName, sign) = Cell_Name.objects.get_or_create(name=request.POST['Cell_Name'], pid=celltype)
                source_cell.cellType = celltype
                source_cell.cellName = cellName
                source_cell.save()
            #===================================================================
            # if request.POST['geneTaxon'] != 'Gene Taxon':
            #     geneTaxon = Source_TissueTaxonID.objects.filter(name=request.POST['geneTaxon'])[0]
            #===================================================================
                
            #===================================================================
            # if request.POST['Genotype'] != 'Wild type':
            #     source_cell.geneTaxon = geneTaxon
            #     source_cell.geneSymbol = request.POST['geneSymbol']
            #     source_cell.geneID = request.POST['GeneID']
            #     source_cell.save()
            #===================================================================
            sample.source_cell = source_cell
            sample.save()
        elif cell_tissue == 'Fluid':
            (AorM, sign) = Source_TissueTaxonAorM.objects.get_or_create(name=request.POST['Source_TissueTaxonAorM'])
            tissueName = Source_TissueTaxonName.objects.filter(name=request.POST['tissueName'])[0]
            (tissueID, sign) = Source_TissueTaxonID.objects.get_or_create(name=request.POST['tissueID'])
            tissueStrain = Source_TissueTaxonStrain.objects.filter(pid__name=request.POST['tissueID']).filter(name=request.POST['tissueStrain'])[0]
            try:
                circ_time = request.POST['circ_time']
            except:
                circ_time = ''
            # (genotype, sign) = Genotype.objects.get_or_create(name=request.POST['Genotype'])
            (genotype, sign) = Genotype.objects.get_or_create(name=request.POST['Genotype'])
            try:
                circ_time = request.POST['circ_time']
            except:
                circ_time = ''
            age = request.POST['tissue_age']
            (age_unit, sign) = All_AgeUnit.objects.get_or_create(name=request.POST['All_AgeUnit'])
            (gender, sign) = Tissue_gender.objects.get_or_create(name=request.POST['Tissue_gender'])
            (fluid, sign) = Fluid_name.objects.get_or_create(name=request.POST['Fluid_name'])
            gene_num = int(request.POST['Gene_num'])
            gene = ''
            for gene_order in range(1, gene_num + 1):
                gene = gene + request.POST['geneSymbol' + str(gene_order)] + '|' + request.POST['GeneID' + str(gene_order)] + '|' + request.POST['geneTaxon' + str(gene_order)] + ';'
            gene = gene[:-1]
            source_fluid = Source_fluid(AorM=AorM,
                                      tissueName=tissueName,
                                      tissueID=tissueID,
                                      age=age,
                                      age_unit=age_unit,
                                      tissueStrain=tissueStrain,
                                      gene=gene,
                                      fluid=fluid,
                                      gender=gender,
                                      genotype=genotype,
                                      circ_time=circ_time,
                                      specific_ID=request.POST['Specific_ID'])
            source_fluid.save()
            
            #===================================================================
            # if request.POST['geneTaxon'] != 'Gene Taxon':
            #     geneTaxon = Source_TissueTaxonID.objects.filter(name=request.POST['geneTaxon'])[0]
            # if request.POST['Genotype'] != 'Wild type':
            #     source_fluid.geneTaxon = geneTaxon
            #     source_fluid.geneSymbol = request.POST['geneSymbol']
            #     source_fluid.geneID = request.POST['GeneID']
            #     source_fluid.save()
            #===================================================================
            sample.source_fluid = source_fluid
            sample.save()
        elif cell_tissue == 'Others':
            source_others = Source_others(name=request.POST['tissue_others'])
            source_others.save()
            sample.source_others = source_others
            sample.save()
        '''
        rx_treatment_list = request.POST.getlist('Rx_treatment')
        for treatment_name in rx_treatment_list:
            (rx_treatment, sign) = Rx_treatment.objects.get_or_create(name=treatment_name)
            sample.rx_treatments.add(rx_treatment)
        '''
        ubi_subcell_list = request.POST.getlist('Ubi_subcell')
        for subcell_name in ubi_subcell_list:
            (ubi_subcell, sign) = Ubi_subcell.objects.get_or_create(name=subcell_name)
            sample.ubi_subcells.add(ubi_subcell)

        ubi_method_list = request.POST.getlist('Ubi_method')
        for method_name in ubi_method_list:
            (ubi_method, sign) = Ubi_method.objects.get_or_create(name=method_name)
            sample.ubi_methods.add(ubi_method)
        sample.save()
        success = True
        msg = "Sample Added"
        data = {'success': success, 'msg':str(sample.id)}
        result = json.dumps(data)
        return HttpResponse(result)
        # return HttpResponseRedirect('/experiments/sample/')

    else:
        raise Http404()

# @login_required(login_url="/login/")
def reagent_save(request):
    if request.method == 'POST':
        #experimenter = All_Experimenter.objects.get(name=request.POST['experimenter'])  # maybe some people will have same name..s
        company = All_Company.objects.get(name=request.POST['company'])
        lab = All_Laboratory.objects.get(name=request.POST['lab'])
        experimenter = All_Experimenter.objects.filter(name=request.POST['experimenter']).filter(lab=lab)[0]
        (exp_info, sign) = Experimenter_info.objects.get_or_create(
                                                         company=company,
                                                         lab=lab,
                                                         experimenter=experimenter
                                                         )
        (month, day, year) = request.POST['date'].split('/')
        sample_date = date(int(year), int(month), int(day))
        name = request.POST['name']
        reagent_type = request.POST['reagent_type']
        (reagent_manufacturer, sign) = Reagent_manufacturer.objects.get_or_create(name=request.POST['Reagent_manufacturer'])
        catalog_no = request.POST['catalog_no']
        # (affinity, sign) = Affinity.objects.get_or_create(name=request.POST['Affinity'])
        # (purification, sign) = Purification.objects.get_or_create(name=request.POST['Purification'])
        (conjugate, sign) = Conjugate.objects.get_or_create(name=request.POST['Conjugate'])

        reagent = Reagent(experimenter=exp_info,
                          date=sample_date,
                          type=reagent_type,
                          name=name,
                          manufacturer=reagent_manufacturer,
                          catalog_no=catalog_no,
                          # affinity=affinity,
                          # purification=purification,
                          conjugate=conjugate,
                          ext_comments=request.POST['comments'],
                          ispec_no=request.POST['Ispec_num']
                          )
        reagent.save()

        react_species_list = request.POST.getlist('React_species_source')
        for react_species_name in react_species_list:
            (react_species, sign) = React_species.objects.get_or_create(name=react_species_name)
            reagent.react_species_sources.add(react_species)

        react_species_list = request.POST.getlist('React_species_target')
        for react_species_name in react_species_list:
            (react_species, sign) = React_species.objects.get_or_create(name=react_species_name)
            reagent.react_species_targets.add(react_species)
        
        application_list = request.POST.getlist('Application')
        for application_name in application_list:
            (application, sign) = Application.objects.get_or_create(name=application_name)
            reagent.applications.add(application)
        
        if reagent_type == 'Antigen':
            (host_species, sign) = Antigen_species.objects.get_or_create(name=request.POST['Antigen_species'])
            (clonal_type, sign) = Antigen_clonal_type.objects.get_or_create(name=request.POST['Antigen_clonal_type'])
            (modification, sign) = Antigen_modification.objects.get_or_create(name=request.POST['Antigen_modification'])
            antigen = Antigen(gene_id=request.POST['gene_id'],
                        host_species=host_species,
                        clonal_type=clonal_type,
                        modification=modification)
            antigen.save()
            reagent.antigen = antigen
        elif reagent_type == 'DNA':
            dna_info = Dna_info(sequence=request.POST['dna_sequence'])
            dna_info.save()
            reagent.dna_info = dna_info
        elif reagent_type == 'Protein':
            domain_info = Domain_info(domain=request.POST['domain'])
            domain_info.save()
            reagent.domain_info = domain_info
        elif reagent_type == 'other':
            remarks_info = Remarks_info(remarks=request.POST['remarks'])
            remarks_info.save()
            reagent.remarks_info = remarks_info
        elif reagent_type == 'chemical':
            chemical_info = Chemical_info(chemical=request.POST['cas_number'])
            chemical_info.save()
            reagent.chemical_info = chemical_info
        reagent.save()
        success = True
        msg = str(reagent.id)
        data = {'success': success, 'msg':msg}
        result = json.dumps(data)
        return HttpResponse(result)
        # return HttpResponseRedirect('/experiments/reagent/')
    else:
        raise Http404()
def reagent_short(request):
    sample_dict = {}
    sample_id = int(request.POST['id'])
    sample = Reagent.objects.get(id=sample_id)
    sample_dict['experimenter'] = str(sample.experimenter.lab.name) + '/' + str(sample.experimenter.experimenter.name)
    sample_dict['date'] = str(sample.date.month) + '/' + str(sample.date.day) + '/' + str(sample.date.year)
    sample_dict['name'] = str(sample.name) 
    sample_dict['manufacturer'] = str(sample.manufacturer.name) 
    sample_dict['catalog_no'] = str(sample.catalog_no)
    if sample.antigen:
        sample_dict['type'] = 'Antibodies'
        # sample_dict['cell_tissue'] = sample.source_tissue.type.name
    elif sample.domain_info:
        sample_dict['type'] = 'Proteins Motif'
    elif sample.dna_info:
        sample_dict['type'] = 'Nuclear Acid'
    elif sample.remarks_info:
        sample_dict['type'] = 'Others'
    result = json.dumps(sample_dict)
    return HttpResponse(result)

# @login_required(login_url="/login/")
def experiment_save(request):
    if request.method == 'POST':
        # (project, sign) = Project.objects.get_or_create(name=request.POST['Project'])
        (month, day, year) = request.POST['date'].split('/')
        experiment_date = date(int(year), int(month), int(day))
        # general_experimenter = All_Experimenter.objects.get(id=request.user)
        company = request.POST['company']
        lab = request.POST['lab']
        experimenter = request.POST['experimenter'] 
        
        ####################uploadFile########################
        #CustomFile_ForDatabaseSearch.objects.get_or_create(name=request.POST['Digest_type'])
        #fastaFileURL = request.FILES['addexperimentAdditionalsequenceFile']
        #file = fastaFileURL.read()
        #print s
        #fileAddressOnServer = request.POST['fastaFileURL']
        #fileName = request.request.POST['filename']
        ####################uploadFile########################
        
        # room = request.POST['Room']
        # No = request.POST['No']
        # Temperature = request.POST['Temperature']
        Funding = request.POST['Funding']
        Project = request.POST['Project']
        PI = request.POST['PI']
        SubProject = request.POST['SubProject']
        if SubProject == 'SubProject':
            SubProject = ''
        Subject = request.POST['Subject']
        if Subject == 'Subject':
            Subject = ''
        Manager = request.POST['Manager']
        if Manager == 'Manager Name':
            Manager = ''
        repeat = request.POST['repeat']
        fraction = request.POST['fraction']
        
        (experiment_type, sign) = Experiment_type.objects.get_or_create(name=request.POST['Experiment_type'])
        # separation_user = User.objects.get(username=request.POST['separation_experimenter'])
        # separation_experimenter = All_Experimenter.objects.get(id=separation_user)
        
        separation_ajustments = request.POST['separation_ajustments']

        # digest_user = User.objects.get(username=request.POST['digest_experimenter'])
        # digest_experimenter = All_Experimenter.objects.get(id=digest_user)
        (digest_type, sign) = Digest_type.objects.get_or_create(name=request.POST['Digest_type'])
        (digest_enzyme, sign) = Digest_enzyme.objects.get_or_create(name=request.POST['Digest_enzyme'])
        
        # (instrument_administrator, sign) = Instrument_administrator.objects.get_or_create(name=request.POST['Instrument_administrator'])
        
        #zdd instrument_MS: Separate value and unit
        #instrument_MS1_tol_unit
        instrument_MS1_tol_value = request.POST['instrument_MS1_tol']
        instrument_MS1_tol_unit = request.POST['instrument_MS1_tol_unit']
        instrument_MS1_tol_name = instrument_MS1_tol_value + " " + instrument_MS1_tol_unit
        #instrument_MS2_tol_unit
        instrument_MS2_tol_value = request.POST['instrument_MS2_tol']
        instrument_MS2_tol_unit = request.POST['instrument_MS2_tol_unit']
        instrument_MS2_tol_name = instrument_MS2_tol_value + " " + instrument_MS2_tol_unit
        
        
        
        (instrument_manufacturer, sign) = Instrument_manufacturer.objects.get_or_create(name=request.POST['Instrument_manufacturer'])
        instrument_name = Instrument.objects.get(name=request.POST['Instrument_name'])
        
        instrument_MS1 = Instrument_MS1.objects.get(name=request.POST['instrument_MS1'], type=instrument_name)
        instrument_MS1_tol = Instrument_MS1_tol.objects.get_or_create(name=instrument_MS1_tol_name, type=instrument_MS1)#get_or_create(name=request.POST['instrument_MS1_tol'], type=instrument_MS1)
        instrument_MS1_tol = instrument_MS1_tol[0]
        
        instrument_MS2 = Instrument_MS2.objects.get(name=request.POST['instrument_MS2'], type=instrument_name)
        instrument_MS2_tol = Instrument_MS2_tol.objects.get_or_create(name=instrument_MS2_tol_name, type=instrument_MS2)
        instrument_MS2_tol = instrument_MS2_tol[0]
        
        database = Search_database.objects.get(name=request.POST['Search_database'])
        comments_conclusions = request.POST['comments_conclusions']
        # description = request.POST['description']
        ispecno = request.POST['ispecno']
        taxid = ''
        
        ######################################################################
        #add mode of source by zdd
        (workflowMode, sign) = Workflow_mode.objects.get_or_create(name=request.POST['workflowMode'])
        #add search engine by xiaotian
        (search_Engine, sign) = searchEngine.objects.get_or_create(name=request.POST['searchEngine'])
        #add quantification method by zdd
        (quantification_methods, sign) = Quantification_Methods.objects.get_or_create(name=request.POST['quantificationMethods'])
        ######################################################################

        experiment = Experiment(date=experiment_date,
                experimenter=experimenter,
                company=company,
                lab=lab,
                # room=room,
                # no=No,
                # Temperature=Temperature,
                Funding=Funding,
                Project=Project,
                PI=PI,
                SubProject=SubProject,
                Subject=Subject,
                Manager=Manager,
                type=experiment_type,
                fraction=fraction,
                repeat=repeat,
                separation_ajustments=separation_ajustments,
                digest_type=digest_type,
                digest_enzyme=digest_enzyme,
                instrument_name=instrument_name,
                instrument_manufacturer=instrument_manufacturer,
                ms1=instrument_MS1,
                ms2=instrument_MS2,
                ms1_details=instrument_MS1_tol,
                ms2_details=instrument_MS2_tol,
                comments_conclusions=comments_conclusions,
                # description=description,
                fm_no=ispecno,
                search_database=database,
                
                #add workflow by zdd
                quantificationMethod = quantification_methods,
                workflowMode = workflowMode,
                searchEngine = search_Engine
                )
        experiment.save()
        no = experiment.id
        exp_name = str(experiment.id)
        while len(exp_name) < 6:
            exp_name = '0' + exp_name
        exp_name = 'Exp' + exp_name
        experiment.name = exp_name
        
        #print s
        ######################################################################
        #add workflow by zdd
        experimentId = no        
        #mode of source
        if experiment.workflowMode.name == "PRIDE" or experiment.workflowMode.name == "MassIVE":
            #query Pride_mode
            #if current expId exist
            #update pxdno, prideFileList
            pride_mode_detail = Pride_mode.objects.filter(experimentId=experimentId)
            pride_mode_detail_length = len(pride_mode_detail)
            if pride_mode_detail_length > 0:
                pride_mode_detail = pride_mode_detail[0]
                pride_mode_detail.pxdno = request.POST['pxdno']
                pride_mode_detail.prideFileList = request.POST['prideFileList']
                pride_mode_detail.save()
            #else insert a new record
            else:
                #add a record into Pride_mode
                prideMode = Pride_mode(
                    experimentId = experimentId,
                    pxdno = request.POST['pxdno'],
                    prideFileList = request.POST['prideFileList']
                )
                prideMode.save()
                #repeat = request.POST['repeat']
                #fraction = request.POST['fraction']
                
        
        #search engine
        if experiment.searchEngine.name == "X!Tandem":
            #add a record into Xtandem_mode
            xtandemMode = Xtandem_mode(
                experimentId = experimentId,
                fragmentationMethod = request.POST['fragmentationMethod'],
                cysteineProtectingGroup = request.POST['cysteineProtectingGroup'],
                protease = request.POST['protease'],
                numberOfAllowed13C = request.POST['numberOfAllowed13C'],
                #parentMassTolerance = request.POST['parentMassToleranceNumber'],
                #parentMassToleranceUnit = request.POST['parentMassToleranceUnit'],
                #ionTolerance = request.POST['ionToleranceNumber'],
                #ionToleranceUnit = request.POST['ionToleranceUnit']
            )
            xtandemMode.save()
            
        if experiment.searchEngine.name == "Mascot":
            #add a record into Mascot_mode
            (missedCleavagesAllowed, missedCleavagesAllowed_sign) = Mascot_mode_missedCleavagesAllowed.objects.get_or_create(name=request.POST['missedCleavagesAllowed'])
            (mascotEnzyme, mascotEnzyme_sign) = Mascot_mode_mascotEnzyme.objects.get_or_create(name=request.POST['mascotEnzyme'])
            (peptideCharge, peptideCharge_sign) = Mascot_mode_peptideCharge.objects.get_or_create(name=request.POST['peptideCharge'])
            (precursorSearchType, precursorSearchType_sign) = Mascot_mode_precursorSearchType.objects.get_or_create(name=request.POST['precursorSearchType'])
            mascotMode = Mascot_mode(
                experimentId = experimentId,
                missedCleavagesAllowed = missedCleavagesAllowed,
                mascotEnzyme = mascotEnzyme,
                peptideCharge = peptideCharge,
                precursorSearchType = precursorSearchType
            )
            mascotMode.save()
        
        ######################################################################
        
        ######################################################################
        #add experimentFdr by zdd
        experimentalFDR_level = request.POST['addexperimentFdr']
        #Spectrum Peptide Protein
        if "Spectrum" in experimentalFDR_level:
            Experimentalfdr_info(
                experimentId = experimentId,
                experimentalFDR_level = "Spectrum",
                experimentalFDR_value= request.POST['addexperimentSpectrumFdrValue']
            ).save()
        elif "Peptide" in experimentalFDR_level:
            Experimentalfdr_info(
                experimentId = experimentId,
                experimentalFDR_level = "Peptide",
                experimentalFDR_value= request.POST['addexperimentPeptideFdrValue']
            ).save()
        else:
            Experimentalfdr_info(
                experimentId = experimentId,
                experimentalFDR_level = "Protein",
                experimentalFDR_value= request.POST['addexperimentProteinFdrValue']
            ).save()
        
        ######################################################################
        
        bait = ''
        protocols = ''
        #pre_separation_methods
        experiment.pre_separation_methods = request.POST['separ_methods']
        #pre_separation_methods
        separation_method_num = int(request.POST['method_num'])
        experiment.separation = separation_method_num
        experiment.save()
        for method_order in  range(1, separation_method_num + 1):
            separation_method = request.POST['separation_method' + str(method_order)]
            separation_source = request.POST['separation_source' + str(method_order)]
            separation_size = request.POST['separation_size' + str(method_order)]
            separation_buffer = request.POST['separation_buffer' + str(method_order)]
            separation_others = request.POST['separation_others' + str(method_order)]
            separation_num = separation_method_num
            Sepeartion = Separation_method(
                                         name=separation_method,
                                         source=separation_source,
                                         size=separation_size,
                                         buffer=separation_buffer,
                                         others=separation_others,
                                         )
            Sepeartion.save()
            experiment_separation = Experiment_separation(experiment=experiment,
                    separation_method=Sepeartion,
                    method_order=method_order,
                    separation_num=separation_num)
            experiment_separation.save()


        sample_num = int(request.POST['sample_num'])
        for i in range(sample_num):
            sample = Sample.objects.get(id=request.POST['sample_no' + str(i + 1)])
            temp_sample = sample
            experiment_sample = Experiment_sample(sample=sample,
                                    experiment=experiment,
                                    amount=request.POST['sample_amount' + str(i + 1)],
                                    amount_unit=request.POST['sample_unit' + str(i + 1)],
                                    ajustments=request.POST['sample_ajustments' + str(i + 1)])
            experiment_sample.save()

        reagent_num = int(request.POST['reagent_num'])
        for i in range(reagent_num):
            reagent = Reagent.objects.get(id=request.POST['reagent_no' + str(i + 1)])
            bait = bait + str(reagent.name) + ';'
            amount = request.POST['reagent_amount' + str(i + 1)]
            amount_unit=request.POST['reagent_unit' + str(i + 1)]
            (method, sign) = Reagent_method.objects.get_or_create(name=request.POST['Reagent_method' + str(i + 1)])
            (wash_buffer, sign) = Reagent_buffer.objects.get_or_create(name=request.POST['Reagent_buffer' + str(i + 1)])
            ajustments = request.POST['reagent_ajustments' + str(i + 1)]
            experiment_reagent = Experiment_reagent(reagent=reagent,
                                    experiment=experiment,
                                    amount=amount,
                                    amount_unit=amount_unit,
                                    method=method,
                                    wash_buffer=wash_buffer,
                                    ajustments=ajustments)
            experiment_reagent.save()
        fixedModifications = request.POST.getlist('Fixed_Modification')
        for temp in fixedModifications:
            (fixedModification, sign) = Fixed_Modification.objects.get_or_create(name=temp)
            experiment.fixed_modifications.add(fixedModification) 
        dynamicModifications = request.POST.getlist('Dynamic_Modification')
        for temp in dynamicModifications:
            if temp != '':
                (dynamicModification, sign) = Dynamic_Modification.objects.get_or_create(name=temp)
                experiment.dynamic_modifications.add(dynamicModification)    
        
        cell = '-'
        organ = '-'
        tissue = '-'
        fluid = '-'
        description = ''
        sam_num=1
        for temp_sample in  experiment.samples.all().order_by('id'):
            if len(experiment.samples.all())>1:
                description=description+'#'+str(sam_num)+':'
                sam_num=sam_num+1
            if temp_sample.source_tissue:
                taxid = temp_sample.source_tissue.tissueID.name
                speci = temp_sample.source_tissue.tissueName.name
                tissue = temp_sample.source_tissue.tissueSystem.name
                organ = temp_sample.source_tissue.tissueOrgan.name 
                ts = temp_sample.source_tissue
                gene = ts.gene
                if ts.genotype.abbrev == 'WT': 
                    gstring = ts.genotype.abbrev
                else:
                    gstring = ''
                    genes = gene.split(';')
                    for gene in genes:
                        gstring = gstring + gene.split('|')[0] + '(' + ts.genotype.abbrev + ')' + '|' 
                        print gene
                    gstring=gstring[:-1]
                if ts.tissueStrain.name != 'None':                    
                    description += str(ts.tissueName.abbrev) + '_' + str(ts.tissueStrain.name) + '_' + gstring + '_' + str(ts.tissueOrgan.name)
                else:
                    description += str(ts.tissueName.abbrev) + '_' + gstring + '_' + str(ts.tissueOrgan.name)
                if ts.tissueStructure:
                    description=description+'_'+ts.tissueStructure
                if ts.tissueType:
                    if ts.tissueType.name == 'Tumor':
                        description = description + '(T)'
                    elif ts.tissueType.name == 'Tumor adjacent':
                        description = description + '(P)'
                    elif ts.tissueType.name == 'Normal' or  ts.tissueType.name == 'Tumor distant':
                        description = description + '(N)'
                    else:
                        description = description + '(' + ts.tissueType.name + ')'
            elif temp_sample.source_cell:
                taxid = temp_sample.source_cell.tissueID.name
                try:
                    speci = temp_sample.source_cell.tissueName.name
                except:
                    sepci = '-'
                try:
                    cell = temp_sample.source_cell.cellName.name
                except:
                    cell = '-'
                sc = temp_sample.source_cell
                gene = sc.gene
                if sc.genotype.abbrev == 'WT': 
                    gstring = sc.genotype.abbrev
                else:
                    gstring = ''
                    genes = gene.split(';')
                    for gene in genes:
                        gstring = gstring + gene.split('|')[0] + '(' + sc.genotype.abbrev + ')' + '|' 
                        
                    gstring=gstring[:-1]
                try:
                    if (sc.cellName.abbrev):
                        abbrev=sc.cellName.abbrev
                    else:
                        abbrev=sc.cellName.name
                except:
                        abbrev='None'
                if sc.tissueStrain.name != 'None':
                    description += str(sc.tissueName.abbrev) + '_' + str(sc.tissueStrain.name) + '_' + gstring + '_' + str(abbrev)
                else:
                    description += str(sc.tissueName.abbrev) + '_' + gstring + '_' + str(abbrev)
            elif temp_sample.source_fluid:
                taxid = temp_sample.source_fluid.tissueID.name
                speci = temp_sample.source_fluid.tissueName.name
                fluid = temp_sample.source_fluid.fluid.name
                sf = temp_sample.source_fluid
                gene = sf.gene
                if sf.genotype.abbrev == 'WT': 
                    gstring = sf.genotype.abbrev
                else:
                    gstring = ''
                    genes = gene.split(';')
                    for gene in genes:
                        gstring = gstring + gene.split('|')[0] + '(' + sf.genotype.abbrev + ')' + '|' 
                    gstring=gstring[:-1]
                if sf.tissueStrain.name != 'None':
                    description += str(sf.tissueName.abbrev) + '_' + str(sf.tissueStrain.name) + '_' + gstring+ '_' + str(sf.fluid.name) 
                else:
                    description += str(sf.tissueName.abbrev) + '_' + gstring+ '_' + str(sf.fluid.name) 
            elif temp_sample.source_others:
                taxid = ''
                speci = '-'
                tissue = '-'
            
            rx_treatment_string = ''
            for rx in temp_sample.treatments.all().order_by('id'):
                # rx_treatment_string=rx_treatment_string+str(rx.rx_treatments.name) + '|' + str(rx.rx_treatments_detail.name)
                if rx.geneTaxon:
                    rx_treatment_string = rx_treatment_string + rx.geneSymbol+'('+str(rx.rx_treatments_detail.abbrev)+')'
                else:
                    if rx.rx_treatments_detail.abbrev:
                        rx_treatment_string = rx_treatment_string + str(rx.rx_treatments_detail.abbrev) + '_'
                    else:
                        rx_treatment_string = rx_treatment_string + str(rx.rx_treatments_detail.name) + '_'
                    if rx.rx_unit_deatil:
                        if rx.rx_unit_deatil.name != 'None':
                            rx_treatment_string = rx_treatment_string + str(rx.rx_amount)  + str(rx.rx_unit_deatil.name)
                if rx_treatment_string[-1]=='_':
                    rx_treatment_string=rx_treatment_string[:-1]
                rx_treatment_string = rx_treatment_string + '_'+str(rx.rx_duration) + str(rx.rx_duration_time)
                
                rx_treatment_string = rx_treatment_string + '; '
            #=======================================================================
            # if (temp_sample.ubi_subcells.all() != 0):
            #     description = description + '-' + temp_sample.ubi_subcells.all()[0].abbrev
            #=======================================================================
            #=======================================================================
            # if temp_sample.rx_treatments.name != 'None':
            #     description = description + ';' + temp_sample.rx_treatments_detail.name
            # if temp_sample.rx_unit_deatil:
            #     description = description + '-' + temp_sample.rx_amount + temp_sample.rx_unit_deatil.name
            # if temp_sample.rx_duration_time:
            #     description = description + '-' + str(temp_sample.rx_duration) + str(temp_sample.rx_duration_time)        
            #=======================================================================
            for ubi in  temp_sample.ubi_subcells.all().order_by('id'):
                rx_treatment_string=rx_treatment_string+ubi.abbrev+'|'
            rx_treatment_string=rx_treatment_string[:-1]
            sample_amount=Experiment_sample.objects.filter(experiment=experiment).filter(sample=temp_sample)[0]
            if sample_amount.amount_unit!='None':
                rx_treatment_string=rx_treatment_string+'_'+sample_amount.amount+sample_amount.amount_unit
            else:
                rx_treatment_string=rx_treatment_string+'_'+sample_amount.amount
            description = description + '; ' + rx_treatment_string + '; '
        description=description.strip()[:-1]
        experiment.taxid = taxid
        experiment.save()
        if bait == '':
            bait = 'NA'
        # if experiment_type=='Affinity' experiment_type=reagent.type+reagent.name
        file_source = 'aliyun' if str(lab) == 'Dr.Minjia Tan Lab' else 'nas'
        exp_exp = gard_experiment(
                                  name=exp_name,
                                  bait=bait,
                                  type=experiment_type,
                                  description=description,
                                  species=speci,
                                  taxid=taxid,
                                  cell_type=cell,
                                  tissue=tissue,
                                  organ=organ,
                                  fluid=fluid,
                                  num_fraction=fraction,
                                  num_repeat=repeat,
                                  num_spectrum=0,
                                  num_peptide=0,
                                  num_isoform=0,
                                  num_gene=0,
                                  instrument=instrument_name,
                                  protocol='',
                                  lab=lab,
                                  operator=experimenter,
                                  experiment_date=experiment_date,
                                  index_date=datetime.date.today(),
                                  update_date=datetime.date.today(),
                                  stage=-1,
                                  started=0,
                                  is_public=0,
                                  is_deleted=0,
                                  priority = 0,
                                  file_source = file_source
                                 )

        '''
        exp_exp = gard_experiment.objects.create(name=exp_name,stage=0)
        '''
        exp_exp.save()    
        experiment.description = description
        experiment.save()
        experiment_flag = True
         
        #ExpNo_TimeStamp
        if experiment_flag:        
            experimentId = no 
            experiment_timeStamp = request.POST['timestamp']   
            #(expNo_timeStamp, sign) = ExpNo_TimeStamp.objects.get_or_create(experimentId=experimentId, timeStamp=experiment_timeStamp)
            #expNo_timeStamp.save()
            #compete Custom_FastaLib_withTimeStamp
            custom_fastaLib_withTimeStamp = Custom_FastaLib_withTimeStamp.objects.filter(timeStamp=experiment_timeStamp)
            if len(custom_fastaLib_withTimeStamp)>0:
                custom_fastaLib_withTimeStamp = custom_fastaLib_withTimeStamp[0]
                custom_fastaLib_withTimeStamp.experimentId = experimentId
                custom_fastaLib_withTimeStamp.save()
            
            custom_modifications = Customized_Modifications.objects.filter(timeStamp=experiment_timeStamp)
            if len(custom_modifications)>0:
                custom_modifications = custom_modifications[0]
                custom_modifications.experimentId = experimentId
                custom_modifications.save()
              
        success = True
        msg = "Experiment Added"
        data = {'success': success, 'msg':exp_name}
        result = json.dumps(data)
        return HttpResponse(result)
        # return HttpResponseRedirect('/experiments/experiment/')
    else:
        raise Http404()

#+++++++++++++++++++++++++++++++++++ Ajax +++++++++++++++++++++++++++++++++++
# @login_required(login_url="/login/")
def experimenter(request):
    data = {}
    experimenters = Experimenter.objects.all()
    experimenters_name = []
    for experimenter in experimenters:
        user_dict = {}
        try:
            user_dict['experimenter'] = experimenter.id.username
        except:
            continue
        # user_dict['experimenter'] = experimenter.username
        experimenters_name.append(user_dict)
    data['experimenters'] = experimenters_name
    result = json.dumps(data)
    return HttpResponse(result)

def all_experimenter(request):
    try:
        id = request.GET['id']
    except:
        id = ''
    data = {}
    experimenters = All_Experimenter.objects.all()
    experimenters = experimenters.filter(lab__name=id)
    experimenters_name = []
    for experimenter in experimenters:
        user_dict = {}
        try:
            user_dict['experimenter'] = experimenter.name
        except:
            continue
        # user_dict['experimenter'] = experimenter.username
        experimenters_name.append(user_dict)
    experimenters_name.sort()
    data['experimenters'] = experimenters_name
    result = json.dumps(data)
    return HttpResponse(result)

def all_company(request):
    data = {} 
    try:
        if  request.GET['share']:
            share=True
        else:
            share=False
    except:
        share=False
    if request.user.is_superuser or str(request.user) == 'AnonymousUser' or share:
        companys = All_Company.objects.all().filter(validated=True)
    else:
        lab_id = User_Laboratory.objects.filter(user=request.user)[0].lab.id
        companys = All_Laboratory.objects.get(id=lab_id).company.all()

    com_list = []
    for com in companys:
        user_dict = {}
        try:
            user_dict['company'] = com.name
        except:
            continue
        com_list.append(user_dict)
    com_list.sort()
    data['all_company'] = com_list
    result = json.dumps(data)
    return HttpResponse(result)

def all_lab(request):
    try:
        id = request.GET['id']
    except:
        id = ''
    data = {}
    lab_list = []
    try:
        if  request.GET['share']:
            share=True
        else:
            share=False
    except:
        share =False        
    if request.user.is_superuser or str(request.user) == 'AnonymousUser'or share :
        lab = All_Laboratory.objects.all()
        experimenters = lab.filter(company__name=id)
        
        for experimenter in experimenters:
            user_dict = {}
            try:
                user_dict['lab'] = experimenter.name
            except:
                continue
            lab_list.append(user_dict)
    else:
        lab_name = User_Laboratory.objects.filter(user=request.user)[0].lab.name
        lab_list.append({'lab':lab_name})
    data['all_lab'] = lab_list
    result = json.dumps(data)
    return HttpResponse(result)

def instrument_ms1(request):
    try:
        id = request.GET['id']
    except:
        id = ''
    data = {}
    lab = Instrument_MS1.objects.all()
    experimenters = lab.filter(type__name=id).filter(validated=True)
    experimenters_name = []
    for experimenter in experimenters:
        user_dict = {}
        try:
            user_dict['Instrument_MS1'] = experimenter.name
        except:
            continue
        experimenters_name.append(user_dict)
    data['Instrument_MS1'] = experimenters_name
    result = json.dumps(data)
    return HttpResponse(result)

def instrument_ms2(request):
    try:
        id = request.GET['id']
    except:
        id = ''
    data = {}
    lab = Instrument_MS2.objects.all()
    experimenters = lab.filter(type__name=id).filter(validated=True)
    # experimenters=lab
    experimenters_name = []
    for experimenter in experimenters:
        user_dict = {}
        try:
            user_dict['Instrument_MS2'] = experimenter.name
        except:
            continue
        experimenters_name.append(user_dict)
    data['Instrument_MS2'] = experimenters_name
    result = json.dumps(data)
    return HttpResponse(result)

def instrument_ms1_tol(request):
    try:
        id = request.GET['id']
    except:
        id = ''
    data = {}
    lab = Instrument_MS1_tol.objects.all()
    experimenters = lab.filter(type__name=id).filter(validated=True)
    experimenters_name = []
    for experimenter in experimenters:
        user_dict = {}
        try:
            #user_dict['Instrument_MS1_tol'] = experimenter.name
            #zdd instrument_MS: Separate value and unit
            user_dict['Instrument_MS1_tol'] = experimenter.name.split(" ")[0]
        except:
            continue
        if user_dict not in experimenters_name:
            experimenters_name.append(user_dict)
    data['Instrument_MS1_tol'] = experimenters_name
    result = json.dumps(data)
    return HttpResponse(result)

def instrument_ms2_tol(request):
    try:
        id = request.GET['id']
    except:
        id = ''
    data = {}
    lab = Instrument_MS2_tol.objects.all()
    experimenters = lab.filter(type__name=id).filter(validated=True)
    experimenters_name = []
    for experimenter in experimenters:
        user_dict = {}
        try:
            #user_dict['Instrument_MS2_tol'] = experimenter.name
            #zdd instrument_MS: Separate value and unit
            user_dict['Instrument_MS2_tol'] = experimenter.name.split(" ")[0]
        except:
            continue
        if user_dict not in experimenters_name:
            experimenters_name.append(user_dict)
    data['Instrument_MS2_tol'] = experimenters_name
    result = json.dumps(data)
    return HttpResponse(result)
def treatment_detail(request):
    try:
        id = request.GET['id']
    except:
        id = ''
    data = {}
    lab = Rx_treatment_detail.objects.all()
    experimenters = lab.filter(type__name=id)
    experimenters_name = []
    for experimenter in experimenters:
        user_dict = {}
        try:
            user_dict['all_detail'] = experimenter.name
        except:
            continue
        experimenters_name.append(user_dict)
    data['all_detail'] = experimenters_name
    result = json.dumps(data)
    return HttpResponse(result)

def unit_detail(request):
    try:
        id = request.GET['id']
    except:
        id = ''
    data = {}
    lab = Rx_unit_detail.objects.all()
    experimenters = lab.filter(type__name=id).filter(validated=True)
    experimenters_name = []
    for experimenter in experimenters:
        user_dict = {}
        try:
            user_dict['unit_detail'] = experimenter.name
        except:
            continue
        experimenters_name.append(user_dict)
    data['unit_detail'] = experimenters_name
    result = json.dumps(data)
    return HttpResponse(result)


def source_tissueTaxonAorM(request):
    data = {}
    lab = Source_TissueTaxonAorM.objects.all().filter(validated=True)
    experimenters_name = []
    for experimenter in lab:
        user_dict = {}
        try:
            user_dict['Source_TissueTaxonAorM'] = experimenter.name
        except:
            continue
        experimenters_name.append(user_dict)
    data['Source_TissueTaxonAorM'] = experimenters_name
    result = json.dumps(data)
    return HttpResponse(result)
def source_tissueTaxonID(request):
    try:
        id = request.GET['id']
    except:
        id = ''
    data = {}
    lab = Source_TissueTaxonName.objects.all().filter(validated=True)
    experimenters = lab.filter(name=id)
    experimenters_name = []
    for experimenter in experimenters:
        user_dict = {}
        try:
            user_dict['tissueID'] = experimenter.pid.name
        except:
            continue
        experimenters_name.append(user_dict)
    # experimenters_name.sort(lambda x:int(x['tissueID']))
    data['tissueID'] = experimenters_name
    result = json.dumps(data)
    return HttpResponse(result)


def source_tissueTaxonName(request):
    try:
        id = request.GET['id']
    except:
        id = ''
    data = {}
    lab = Source_TissueTaxonName.objects.all().filter(validated=True)
    experimenters = lab.filter(pid__pid__name=id)
    experimenters_name = []
    for experimenter in experimenters:
        user_dict = {}
        try:
            user_dict['tissueName'] = experimenter.name
        except:
            continue
        if user_dict not in experimenters_name:
            experimenters_name.append(user_dict)
    data['tissueName'] = experimenters_name
    result = json.dumps(data)
    return HttpResponse(result)
def source_tissueTaxonStrain(request):
    try:
        id = request.GET['id']
    except:
        id = ''
    data = {}
    lab = Source_TissueTaxonStrain.objects.all().filter(validated=True)
    experimenters = lab.filter(pid__name=id)
    experimenters_name = []
    for experimenter in experimenters:
        user_dict = {}
        try:
            user_dict['tissueStrain'] = experimenter.name
        except:
            continue
        experimenters_name.append(user_dict)
    data['tissueStrain'] = experimenters_name
    experimenters_name.sort()
    result = json.dumps(data)
    return HttpResponse(result)

def sourcetissueSystem(request):
    try:
        id = request.GET['id']
    except:
        id = ''
    data = {}
    lab = Source_TissueSystem.objects.all().filter(validated=True)
    experimenters = lab.filter(pid__name=id)
    experimenters_name = []
    for experimenter in experimenters:
        user_dict = {}
        try:
            user_dict['Source_TissueSystem'] = experimenter.name
        except:
            continue
        experimenters_name.append(user_dict)
    experimenters_name.sort()
    data['Source_TissueSystem'] = experimenters_name
    result = json.dumps(data)
    return HttpResponse(result)

def sourcetissueOrgan(request):
    try:
        id = request.GET['id']
    except:
        id = ''
    data = {}
    lab = Source_TissueOrgan.objects.all().filter(validated=True)
    experimenters = lab.filter(pid__name=id)
    experimenters_name = []
    for experimenter in experimenters:
        user_dict = {}
        try:
            user_dict['Source_TissueOrgan'] = experimenter.name
        except:
            continue
        experimenters_name.append(user_dict)
    experimenters_name.sort()
    data['Source_TissueOrgan'] = experimenters_name
    result = json.dumps(data)
    return HttpResponse(result)

# @login_required(login_url="/login/")
def record_display(request, model_name):
    
    ##############################################
    data = {}
    model = eval(model_name)
    if model_name == "Search_database":
        #model_name = u'Search_database'
        #for customized search database
        common_records = model.objects.filter(validated=True).filter(owner="admin")
        user = request.user.username
        custmon_records = model.objects.filter(validated=True).filter(owner=user)
        #union
        records = list(set(common_records).union(set(custmon_records)))
    elif model_name == "Fixed_Modification":
        #model_name = u'Fixed_Modification'
        #for customized fixed modification
        common_records = model.objects.filter(validated=True).filter(owner="admin")
        user = request.user.username
        custmon_records = model.objects.filter(validated=True).filter(owner=user)
        #union
        records = list(set(common_records).union(set(custmon_records)))
    elif model_name == "Dynamic_Modification":
        #model_name = u'Dynamic_Modification'
        #for customized dynamic modification
        common_records = model.objects.filter(validated=True).filter(owner="admin")
        user = request.user.username
        custmon_records = model.objects.filter(validated=True).filter(owner=user)
        #union
        records = list(set(common_records).union(set(custmon_records)))
    else:
        records = model.objects.filter(validated=True)

    ##############################################
    
    ##############################################    
    #data = {}
    #model = eval(model_name)
    #records = model.objects.filter(validated=True)
    ############################################## 
    
    record_list = []
    for record in records:
        tmp_dict = {}
        tmp_dict[model_name] = record.name
        record_list.append(tmp_dict)
    if model_name[0:5] != "Miape":
    	record_list.sort()
    data[model_name + 's'] = record_list
    result = json.dumps(data)
    return HttpResponse(result)

def record_display2(request, model_name):
    try:
        id = request.GET['id']
    except:
        id = ''
    data = {}
    model = eval(model_name)
    records = model.objects.filter(validated=True).filter(pid__name=id)
    record_list = []
    for record in records:
        tmp_dict = {}
        tmp_dict[model_name] = record.name
        record_list.append(tmp_dict)
    if len(record_list) == 0:
        tmp_dict = {}
        tmp_dict[model_name] = 'None'
        record_list.append(tmp_dict)
    record_list.sort()
    data[model_name] = record_list
    result = json.dumps(data)
    return HttpResponse(result)

# @login_required(login_url="/login/")
def experiment_no(request):
    ''' Experiment Authority '''
    lab = User_Laboratory.objects.filter(user=request.user)
    lab = lab[0].lab.name if lab.count() else ''
    
    if lab == 'Demo Lab':
        experiments = Experiment.objects.all().filter(lab='')
    elif request.user.is_superuser:
        experiments = Experiment.objects.all()
    else:
        experiments = Experiment.objects.all().filter(lab=lab)
    
    data = []
    try:
        experiments = experiments.order_by('-id')
        for experiment in experiments:
            experiment_dict = {}
            experiment_dict['experiment_no'] = experiment.id
            data.append(experiment_dict)
        result = json.dumps(data)
        return HttpResponse(result)
    except:
        raise Http404()

def sample_no(request):
    
    ''' Simple Authority '''
    lab = User_Laboratory.objects.filter(user=request.user)
    lab = lab[0].lab.name if lab.count() else ''
    
    if lab == 'Demo Lab':
        samples = Sample.objects.all().filter(experimenter__experimenter__lab__name='')
    elif request.user.is_superuser:
        samples = Sample.objects.all()
    else:
        samples = Sample.objects.filter(experimenter__lab__name=lab)
    
    data = []
    try:
        samples = samples.order_by('-id')
        for sample in samples:
            sample_dict = {}
            sample_dict['sample_no'] = sample.id
            data.append(sample_dict)
        result = json.dumps(data)
        return HttpResponse(result)
    except:
        raise Http404()

# @login_required(login_url="/loginsample_num/")
def reagent_no(request):
        
    ''' Simple Authority '''
    lab = User_Laboratory.objects.filter(user=request.user)
    lab = lab[0].lab.name if lab.count() else ''
    
    if lab == 'Demo Lab':
        reagents = Reagent.objects.all().filter(experimenter__experimenter__lab__name='')
    elif request.user.is_superuser:
        reagents = Reagent.objects.all()
    else:
        reagents = Reagent.objects.all().filter(experimenter__lab__name=lab)
    
    data = []
    try:
        reagents = reagents.order_by('-id')
        for reagent in reagents:
            reagent_dict = {}
            reagent_dict['reagent_no'] = reagent.id
            data.append(reagent_dict)
        result = json.dumps(data)
        return HttpResponse(result)
    except:
        raise Http404()

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# @login_required(login_url="/login/")
def sample_data(request):
    
    ''' Simple Authority '''
    lab = User_Laboratory.objects.filter(user=request.user)
    lab = lab[0].lab.name if lab.count() else ''
    
    if lab == 'Demo Lab':
        samples = Sample.objects.all().filter(experimenter__experimenter__lab__name='')
    elif request.user.is_superuser:
        samples = Sample.objects.all()
    else:
        samples = Sample.objects.all().filter(experimenter__lab__name=lab)
    
    
    #filter
    filters = []
    if 'filter' in request.GET:
        filters = json.loads(request.GET['filter'])
    else:
        filters = []
    
    #sort
    start = int(request.GET['start'])
    limit = int(request.GET['limit'])    
    count = samples.count()
    end = start + limit
    if end > count:
        end = count
    
    sort = request.GET['sort']   
    dir = request.GET['dir'] if 'dir' in request.GET else ''
    if dir == 'ASC':
        dir = ''
    elif dir == 'DESC':
        dir = '-' 
    if sort == 'sample_no':
        samples = samples.order_by(dir + 'id')[start:end]
    else:
        samples = samples.order_by(dir + sort)[start:end]
    
       
    sample_list = []
    for sample in samples:
        sample_dict = {}
        sample_dict['sample_no'] = sample.id
        sample_dict['experimenter'] = sample.experimenter.experimenter.name
        sample_dict['date'] = str(sample.date.month) + '/' + str(sample.date.day) + '/' + str(sample.date.year)
        if sample.source_tissue:
            sample_dict['txid'] = sample.source_tissue.tissueName.name
            sample_dict['genotype'] = sample.source_tissue.genotype.name
            sample_dict['cell_tissue'] = 'Tissue' + '-' + sample.source_tissue.gender.name + \
                    '-' + sample.source_tissue.tissueStrain.name
        elif sample.source_cell:
            # sample_dict['txid'] = sample.source_cell.taxon.name
            sample_dict['txid'] = sample.source_cell.tissueName.name
            sample_dict['genotype'] = sample.source_cell.genotype.name
            try:
                cellName = sample.source_cell.cellName.name
            except:
                cellName = ''
            sample_dict['cell_tissue'] = 'Cell' + '-' + cellName
        elif sample.source_fluid:
            # sample_dict['txid'] = sample.source_cell.taxon.name
            sample_dict['txid'] = sample.source_fluid.tissueName.name
            sample_dict['genotype'] = sample.source_fluid.genotype.name
            try:
                cellName = sample.source_fluid.fluid.name
            except:
                cellName = ''
            sample_dict['cell_tissue'] = 'Fluid-' + cellName 
        elif sample.source_others:
            sample_dict['cell_tissue'] = 'Others'

        sample_dict['methods'] = ''
        ubi_methods = sample.ubi_methods.all()
        for ubi_method in ubi_methods:
            sample_dict['methods'] += ' ' + ubi_method.name
        sample_dict['subcellular_organelle'] = ''
        ubi_subcells = sample.ubi_subcells.all()
        for ubi_subcell in ubi_subcells:
            sample_dict['subcellular_organelle'] += ' ' + ubi_subcell.name
        #=======================================================================
        # rx_treatment_string = str(sample.rx_treatments.name) + '\\' + str(sample.rx_treatments_detail.name) 
        # try:
        #     rx_unit_deatil = str(sample.rx_unit_deatil.name)
        # except:
        #     rx_unit_deatil = ''
        # sample_dict['rx'] = rx_treatment_string.strip() + ' ' + str(sample.rx_amount) + ' ' + rx_unit_deatil
        #=======================================================================
        rx_treatment_string = ''
        for rx in sample.treatments.all():
            rx_treatment_string = rx_treatment_string + str(rx.rx_treatments.name) + '|' + str(rx.rx_treatments_detail.name)
            try:
                rx_unit_deatil = str(rx.rx_unit_deatil.name)
            except:
                rx_unit_deatil = ''
            amount=rx.id
            rx_treatment_string = rx_treatment_string + ' ' + str(rx.rx_amount) + ' ' + rx_unit_deatil
            if rx.geneTaxon:
                rx_treatment_string = rx_treatment_string + ' ' + rx.geneTaxon.name + '|' + rx.geneSymbol + '|' + rx.geneID
            rx_treatment_string = rx_treatment_string + ';'
        sample_dict['rx'] = rx_treatment_string
        sample_list.append(sample_dict)

    data = {"samples":sample_list, 'total':count}
    result = json.dumps(data)
    return HttpResponse(result)

# @login_required(login_url="/login/")
def reagent_data(request):
    
    ''' Simple Authority '''
    lab = User_Laboratory.objects.filter(user=request.user)
    lab = lab[0].lab.name if lab.count() else ''
    
    if lab == 'Demo Lab':
        reagents = Reagent.objects.all().filter(experimenter__experimenter__lab__name='')
    elif request.user.is_superuser:
        reagents = Reagent.objects.all()
    else:
        reagents = Reagent.objects.all().filter(experimenter__lab__name=lab)
    
    start = int(request.GET['start'])
    limit = int(request.GET['limit'])
    sort = request.GET['sort']
    reagent_list = []
    count = reagents.count()
    end = start + limit
    
    dir = request.GET['dir'] if 'dir' in request.GET else ''
     
    if end > count:
        end = count
        dir = request.GET['dir'] if 'dir' in request.GET else ''
        
    if dir == 'ASC':
        dir = ''
    elif dir == 'DESC':
        dir = '-' 
    if sort == 'reagent_no':
        reagents = reagents.order_by(dir + 'id')[start:end]
    else:
        reagents = reagents.order_by('id')[start:end]
        
    for reagent in reagents:
        reagent_dict = {}
        reagent_dict['reagent_no'] = reagent.id
        reagent_dict['reagent_type'] = reagent.type
        reagent_dict['name'] = reagent.name
        reagent_dict['manufacturer'] = reagent.manufacturer.name
        reagent_dict['catalog_no'] = reagent.catalog_no
       # reagent_dict['affinity_type'] = reagent.affinity.name
        application_string = ''
        for application in reagent.applications.all():
            application_string += application.name + ' '
        reagent_dict['applications'] = application_string.strip()
        react_species_string = ''
        for react_species in reagent.react_species_sources.all():
            react_species_string += react_species.name + ' '
        reagent_dict['react_speciess'] = react_species_string.strip()
        # reagent_dict['purification'] = reagent.purification.name
        reagent_dict['conjugate'] = reagent.conjugate.name
        reagent_list.append(reagent_dict)
    data = {"reagents": reagent_list, 'total':count}
    result = json.dumps(data)
    return HttpResponse(result)

# @login_required(login_url="/login/")
def experiment_data(request):

    ''' Simple Authority '''
    lab = User_Laboratory.objects.filter(user=request.user)
    lab = lab[0].lab.name if lab.count() else ''
    
    if lab == 'Demo Lab':
        experiments = Experiment.objects.all().filter(lab='')
    elif request.user.is_superuser:
        experiments = Experiment.objects.all()
    else:
        experiments = Experiment.objects.all().filter(lab=lab)
        #add by zdd
        public_exps = gard_experiment.objects.filter(is_public=1)
        expNames = []
        for exp in public_exps:
            expNames.append(exp.name)
        for name in expNames:
            tmp = Experiment.objects.all().filter(name=name)
            experiments = experiments | tmp
        
    filters = []
    if 'filter' in request.GET:
        filters = json.loads(request.GET['filter'])
    else:
        filters = []
    
    start = int(request.GET['start'])
    limit = int(request.GET['limit'])
    sort = request.GET['sort']
    dir = request.GET['dir'] if 'dir' in request.GET else ''
    
    count = experiments.count()
    
    end = start + limit
    if end > count:
        end = count
        
    experiments = experiments_filters.experiments_filter(experiments, filters)
        
    if dir == 'ASC':
        dir = ''
    elif dir == 'DESC':
        dir = '-' 
    if sort == 'experiment_no':
        experiments = experiments.order_by(dir + 'id')[start:end]
    else:
        experiments = experiments.order_by('id')[start:end]
    
    experiment_list = []
    for experiment in experiments:
        experiment_dict = {}
        experiment_dict['experiment_no'] = experiment.id
        experiment_dict['experiment_name'] = experiment.name
        experiment_dict['experimenter'] = experiment.experimenter
        experiment_dict['date'] = str(experiment.date.month) + '/' + str(experiment.date.day) + '/' + str(experiment.date.year)
        experiment_dict['instrument'] = experiment.instrument_name.name
        experiment_dict['digest_enzyme'] = experiment.digest_enzyme.name
        experiment_dict['digest_type'] = experiment.digest_type.name
        experiment_samples = Experiment_sample.objects.filter(experiment=experiment)
        sample_string = ''
        for experiment_sample in experiment_samples:
            sample_string += str(experiment_sample.sample.id) + ' '
        experiment_dict['samples'] = sample_string.strip()
        experiment_reagents = Experiment_reagent.objects.filter(experiment=experiment)
        reagent_string = ''
        for experiment_reagent in experiment_reagents:
            reagent_string += str(experiment_reagent.reagent.id) + ' '
        experiment_dict['reagents'] = reagent_string.strip()
        experiment_separations = Experiment_separation.objects.filter(experiment=experiment)
        separation_string = ''
        for experiment_separation in experiment_separations:
            separation_string += experiment_separation.separation_method.name + ' '
        experiment_dict['separations'] = separation_string.strip()
        experiment_list.append(experiment_dict)

    data = {"experiments": experiment_list, "total":count}
    result = json.dumps(data)
    return HttpResponse(result)

# @login_required(login_url="/login/")
def sample_short(request):
    sample_dict = {}
    sample_id = int(request.POST['id'])
    sample = Sample.objects.get(id=sample_id)
    sample_dict['experimenter'] = str(sample.experimenter.lab.name) + '/' + str(sample.experimenter.experimenter.name)
    sample_dict['date'] = str(sample.date.month) + '/' + str(sample.date.day) + '/' + str(sample.date.year)
    if sample.source_tissue:
        sample_dict['txid'] = sample.source_tissue.tissueName.name
        sample_dict['source_type'] = 'Tissue''/' + str(sample.source_tissue.tissueSystem.name) + '/' + str(sample.source_tissue.tissueOrgan.name) + '/' + str(sample.source_tissue.tissueType.name)
        sample_dict['source_strain'] = sample.source_tissue.tissueStrain.name
        sample_dict['source_genotype'] = sample.source_tissue.genotype.name
        sample_dict['source_change'] = sample.source_tissue.geneSymbol
        # sample_dict['cell_tissue'] = sample.source_tissue.type.name
    elif sample.source_cell:
        sample_dict['txid'] = sample.source_cell.tissueName.name
        try:
            cellname = '/' + str(sample.source_cell.cellType.name) + '/' + str(sample.source_cell.cellName.name) 
        except:
            cellname = ''
        sample_dict['source_type'] = 'Cell \& MicroOrganism' + cellname
        sample_dict['source_strain'] = sample.source_cell.tissueStrain.name
        sample_dict['source_genotype'] = sample.source_cell.genotype.name
        sample_dict['source_change'] = sample.source_cell.geneSymbol
    elif sample.source_fluid:
        sample_dict['txid'] = sample.source_fluid.tissueName.name
        sample_dict['source_type'] = 'Fluid \& Excreta' + '/' + str(sample.source_fluid.fluid.name)
        sample_dict['source_strain'] = sample.source_fluid.tissueStrain.name
        sample_dict['source_genotype'] = sample.source_fluid.genotype.name
        sample_dict['source_change'] = sample.source_fluid.geneSymbol
    elif sample.source_others:
        sample_dict['source_type'] = 'Others'
    #===========================================================================
    # rx_treatment_string = str(sample.rx_treatments.name) + '/' + str(sample.rx_treatments_detail.name) 
    # try:
    #     rx_unit_deatil = str(sample.rx_unit_deatil.name)
    # except:
    #     rx_unit_deatil = ''
    #===========================================================================
    #===========================================================================
    # if sample.rx_treatments.name != 'None':
    #     sample_dict['rx'] = rx_treatment_string.strip() + ' ' + str(sample.rx_amount) + ' ' + str(rx_unit_deatil)
    # else:
    #     sample_dict['rx'] = rx_treatment_string.strip()
    #===========================================================================
    rx_treatment_string = ''
    for rx in sample.treatments.all():
        rx_treatment_string = rx_treatment_string + str(rx.rx_treatments.name) + '|' + str(rx.rx_treatments_detail.name)
        try:
            rx_unit_deatil = str(rx.rx_unit_deatil.name)
        except:
            rx_unit_deatil = ''
        rx_treatment_string = rx_treatment_string.strip() + ' ' + str(rx.rx_amount) + ' ' + rx_unit_deatil
        if rx.geneTaxon:
            rx_treatment_string = rx_treatment_string + ' ' + rx.geneTaxon.name + '|' + rx.geneSymbol + '|' + rx.geneID
        rx_treatment_string = rx_treatment_string + ';'
    sample_dict['rx'] = rx_treatment_string
    result = json.dumps(sample_dict)
    return HttpResponse(result)


# @login_required(login_url="/login/")
def sample_edit(request):
    no = request.GET['no']
    sample = Sample.objects.get(id=int(no))
    cell_tissue = ''
    if sample.source_tissue:
        cell_tissue = 'Tissue'
    elif sample.source_cell:
        cell_tissue = 'Cell'
    variables = RequestContext(request, {'no': no, 'cell_tissue':cell_tissue})
    return render_to_response('experiments/sample_edit.html', variables)
    response["P3P"] = 'CP="IDC DSP COR ADM DEVi TAIi PSA PSD IVAi IVDi CONi HIS OUR IND CNT"'

# @login_required(login_url="/login/")
def experiment_edit(request):
    no = request.GET['no']
    experiment = Experiment.objects.get(id=int(no))
    # print experiment
    experiment_samples = Experiment_sample.objects.filter(experiment=experiment)
    samplenum = len(experiment_samples)
    experiment_reagents = Experiment_reagent.objects.filter(experiment=experiment)
    reagentnum = len(experiment_reagents)
    variables = RequestContext(request, {'no': no, 'reagentnum':reagentnum, 'samplenum':samplenum})
    return render_to_response('experiments/experiment_edit.html', variables)
    response["P3P"] = 'CP="IDC DSP COR ADM DEVi TAIi PSA PSD IVAi IVDi CONi HIS OUR IND CNT"'


# @login_required(login_url="/login/")
def reagent_edit(request):
    no = request.GET['no']
    reagent = Reagent.objects.get(id=int(no))
    reagent_type = reagent.type
    variables = RequestContext(request, {'no': no, 'type':reagent_type})
    return render_to_response('experiments/reagent_edit.html', variables)
    response["P3P"] = 'CP="IDC DSP COR ADM DEVi TAIi PSA PSD IVAi IVDi CONi HIS OUR IND CNT"'
#+++++++++++++++++++++++++++++++++++ Load +++++++++++++++++++++++++++++++++++++++++++

# @login_required(login_url="/login/")
def reagent_load(request):
    reagent_dict = {}
    no = request.POST['reagent_no']
    reagent = Reagent.objects.get(id=int(no))
    reagent_dict['experimenter'] = reagent.experimenter.experimenter.name
    reagent_dict['lab'] = reagent.experimenter.lab.name
    reagent_dict['company'] = reagent.experimenter.company.name
    reagent_dict['date'] = str(reagent.date.month) + '/' + str(reagent.date.day) + '/' + str(reagent.date.year)
    reagent_dict['reagent_no'] = reagent.id
    reagent_dict['reagent_type'] = reagent.type
    reagent_dict['name'] = reagent.name
    reagent_dict['Reagent_name'] = reagent.id
    reagent_dict['Reagent_manufacturer'] = reagent.manufacturer.name
    reagent_dict['catalog_no'] = reagent.catalog_no
    # reagent_dict['Affinity'] = reagent.affinity.name
    reagent_dict['Application'] = []
    for application in reagent.applications.all():
        reagent_dict['Application'].append(application.name)

    reagent_dict['React_species_source'] = []
    for application in reagent.react_species_sources.all():
	       reagent_dict['React_species_source'].append(application.name)
    reagent_dict['React_species_target'] = []
    for application in reagent.react_species_targets.all():
         reagent_dict['React_species_target'].append(application.name)
    #reagent_dict['Purification'] = reagent.purification.name
    reagent_dict['Conjugate'] = reagent.conjugate.name
    reagent_dict['ispecno'] = reagent.conjugate.name
    if reagent.type == 'Antigen':
        antigen = reagent.antigen
        reagent_dict['gene_id'] = antigen.gene_id
        reagent_dict['Antigen_species'] = antigen.host_species.name
        reagent_dict['Antigen_clonal_type'] = antigen.clonal_type.name
        reagent_dict['Antigen_modification'] = antigen.modification.name
    elif reagent.type == 'Protein':
        domain_info = reagent.domain_info
        reagent_dict['domain'] = domain_info.domain
    elif reagent.type == 'DNA':
        dna_info = reagent.dna_info
        reagent_dict['dna_sequence'] = dna_info.sequence
    elif reagent.type == 'chemical':
        chemical_info = reagent.chemical_info
        if reagent.chemical_info:
            reagent_dict['cas_number'] = chemical_info.chemical
        else:
            reagent_dict['cas_number']=''
    elif reagent.type == 'other':
        remarks_info = reagent.remarks_info
        reagent_dict['remarks'] = remarks_info.remarks
        
    reagent_dict['Ispec_num'] = reagent.ispec_no

    data = {'success': True, 'data':reagent_dict}
    result = json.dumps(data)
    return HttpResponse(result)


# @login_required(login_url="/login/")
def sample_load(request):
    sample_dict = {}
    no = request.POST['sample_no']
    sample = Sample.objects.get(id=int(no))
    sample_dict['sample_no'] = sample.id
    sample_dict['Sample_name'] = sample.id
    sample_dict['date'] = str(sample.date.month) + '/' + str(sample.date.day) + '/' + str(sample.date.year)
    sample_dict['experimenter'] = sample.experimenter.experimenter.name
    sample_dict['lab'] = sample.experimenter.lab.name
    sample_dict['company'] = sample.experimenter.company.name
    detail_location=''
    if sample.location.refrigerator:
        sample_dict['RefrigeratorNo'] = sample.location.refrigerator.no.name
        sample_dict['RefrigeratorTemper'] = sample.location.refrigerator.temperature.name
        sample_dict['RefrigeratorLayer'] = sample.location.refrigerator.layer.name
        detail_location='Refrigerator'+sample.location.refrigerator.temperature.name+sample.location.refrigerator.no.name+'/'+sample.location.refrigerator.layer.name
    if sample.location.nitrogen:
        sample_dict['Nitrogen_Container'] = sample.location.nitrogen.no.name
        sample_dict['Nitrogen_Basket'] = sample.location.nitrogen.basket.name
        sample_dict['Nitrogen_Layer'] = sample.location.nitrogen.layer.name
        detail_location='Liquid Nitrogen'+sample.location.nitrogen.no.name+sample.location.nitrogen.basket.name+'/'+sample.location.nitrogen.layer.name
    if sample.location.others:
        sample_dict['Others_Temperature'] = sample.location.others.temperature.name
        sample_dict['Others_location'] = sample.location.others.location
        detail_location='Others'+sample.location.others.temperature.name+sample.location.others.location
    sample_dict['detail_location']=detail_location
    #sample_dict['location'] = sample.location
#===============================================================================
    #if sample.source_tissue:
    '''
     cell_tissue = request.POST['cell_tissue']
        sample.cell_tissue = cell_tissue
    '''
    if sample.source_tissue:
        '''
        sample_dict['cell_tissue'] = 'Tissue'
        
        sample_dict['Source_taxon'] = sample.source_tissue.tissueID.name
        sample_dict['Tissue_type'] = sample.source_tissue.tissueType.name
        sample_dict['Tissue_gender'] = sample.source_tissue.gender.name
        sample_dict['Tissue_strain'] = sample.source_tissue.tissueStrain.name
        sample_dict['Genotype'] = sample.source_tissue.genotype.name
        #sample_dict['changes'] = sample.source_tissue.changes
        sample_dict['age'] = sample.source_tissue.age
        sample_dict['circ_time'] = sample.source_tissue.circ_time
        '''
        sample_dict['cell_tissue'] = 'Tissue'
    
        sample_dict['Source_TissueTaxonAorM'] = sample.source_tissue.AorM.name
        sample_dict['tissueName'] = sample.source_tissue.tissueName.name
        sample_dict['tissueID'] = sample.source_tissue.tissueID.name
    
        sample_dict['tissueStrain'] = sample.source_tissue.tissueStrain.name
    
        sample_dict['tissue_age'] = sample.source_tissue.age
        sample_dict['All_AgeUnit'] = sample.source_tissue.age_unit.name
    
        sample_dict['Tissue_gender'] = sample.source_tissue.gender.name
    
        sample_dict['Genotype'] = sample.source_tissue.genotype.name
        
        #default sampleNum=1 geneSymbo + sampleNum
        if sample.source_tissue.gene:
            geneList = sample.source_tissue.gene.split(";")
        else:
            geneList = ""
        sample_dict['geneList'] = geneList
        geneNum = len(geneList)
        #sample_dict['Gene_num'] = geneNum
        #if geneNum>0:
            #for index in range(0, geneNum+1):
                #geneSmallList = geneList[index].split("|")
                #sample_dict['geneSymbol'+str(index)] = geneSmallList[0]
                #sample_dict['GeneID'+str(index)] = geneSmallList[1]
                #sample_dict['geneTaxon'+str(index)] = geneSmallList[2]

    
        sample_dict['Source_TissueSystem'] = sample.source_tissue.tissueSystem.name
        sample_dict['Source_TissueOrgan'] = sample.source_tissue.tissueOrgan.name
        sample_dict['Source_TissueStructure'] = sample.source_tissue.tissueStructure
        sample_dict['Source_TissueType'] = sample.source_tissue.tissueType.name
    
        sample_dict['circ_time'] = sample.source_tissue.circ_time
        sample_dict['Specific_ID'] = sample.source_tissue.specific_ID
# 
    elif sample.source_cell:
        '''
        sample_dict['cell_tissue'] = 'Cell'
        sample_dict['Source_taxon'] = sample.source_cell.tissueID.name
        sample_dict['Cell_type'] = sample.source_cell.cellType.name
        sample_dict['Genotype'] = sample.source_cell.genotype.name
#        sample_dict['changes'] = sample.source_cell.changes
#        sample_dict['age'] = sample.source_cell.age
        sample_dict['circ_time'] = sample.source_cell.circ_time
        '''
        sample_dict['cell_tissue'] = 'Cell'
    
        sample_dict['Source_TissueTaxonAorM'] = sample.source_cell.AorM.name
        sample_dict['tissueName'] = sample.source_cell.tissueName.name
        sample_dict['tissueID'] = sample.source_cell.tissueID.name
        
        sample_dict['tissueStrain'] = sample.source_cell.tissueStrain.name
    
        sample_dict['Genotype'] = sample.source_cell.genotype.name
    
        #sample_dict['Gene_num']
        #sample_dict['geneSymbol']
        #sample_dict['GeneID']
        #sample_dict['geneTaxon']
        if sample.source_cell.gene:
            geneList = sample.source_cell.gene.split(";")
        else:
            geneList = ""
        sample_dict['geneList'] = geneList
        geneNum = len(geneList)
        #sample_dict['Gene_num'] = geneNum
        '''
        if geneNum>0:
            sample_dict['Gene_num'] = geneNum
            for index in range(0, geneNum):
                geneSmallList = geneList[index].split("|")
                sample_dict['geneSmallList'] = geneSmallList
                sample_dict['geneSymbol'+str(index)] = geneSmallList[0]
                sample_dict['GeneID'+str(index)] = geneSmallList[1]
                sample_dict['geneTaxon'+str(index)] = geneSmallList[2]
        else:
            sample_dict['Gene_num'] = geneNum
        '''
                
        if sample.source_cell.AorM.name != 'Microorganism':
            sample_dict['cellcelltype'] = sample.source_cell.cellType.name
            sample_dict['Cell_Name'] = sample.source_cell.cellName.name
        
        sample_dict['circ_time'] = sample.source_cell.circ_time
        sample_dict['Specific_ID'] = sample.source_cell.specific_ID
        

    elif sample.source_fluid:
        sample_dict['cell_tissue'] = 'Fluid'
        
        sample_dict['Source_TissueTaxonAorM'] = sample.source_fluid.AorM.name
        sample_dict['tissueName'] = sample.source_fluid.tissueName.name
        sample_dict['tissueID'] = sample.source_fluid.tissueID.name
    
        sample_dict['tissueStrain'] = sample.source_fluid.tissueStrain.name
    
        sample_dict['tissue_age'] = sample.source_fluid.age
        sample_dict['All_AgeUnit'] = sample.source_fluid.age_unit.name
    
        sample_dict['Tissue_gender'] = sample.source_fluid.gender.name
    
        sample_dict['Genotype'] = sample.source_fluid.genotype.name
    
        #sample_dict['Gene_num'] = sample.source_fluid.
        #sample_dict['geneSymbol'] = sample.source_fluid.
        #sample_dict['GeneID'] = sample.source_fluid.
        #sample_dict['geneTaxon'] = sample.source_fluid.
        geneList = sample.source_fluid.gene.split(";")
        sample_dict['geneList'] = geneList
        geneNum = len(geneList)
        #sample_dict['Gene_num'] = geneNum
    
        sample_dict['Fluid_name'] = sample.source_fluid.fluid.name
        sample_dict['Specific_ID'] = sample.source_fluid.specific_ID
        
    else:
        sample_dict['tissue_others'] = sample.source_others.name
    
    
    '''   
    sample_dict['Rx_treatment'] = []
    for rx_treatment in sample.rx_treatments.all():
        sample_dict['Rx_treatment'].append(rx_treatment.name)
    sample_dict['Rx_unit'] = sample.rx_unit.name
    sample_dict['amount'] = sample.rx_amount
    sample_dict['duration'] = sample.rx_duration
    '''
 
    #Treatment ManyToMany: for in all
    sampleTreament = sample.treatments
    #sample_dict["treatmentsLen"] = len()
    count = 0;
    for sampleT in sampleTreament.all():
        count = count + 1
    sample_dict["treatmentsCount"] = count
    
    sample_dict["treatmentsSet"] = []
    
    #rx_treatments = 'Gene Engineering'
    sample_dict["rx_treatments"] = []
    sample_dict["rx_treatments_detail"] = []
    #rx_treatments = 'Gene Engineering'
    
    sample_dict["rx_treatments_detail_detail"] = []
    sample_dict["rx_amount"] = []
    sample_dict["rx_unit"] = []
    
    #rx_unit = 'Concentration'
    sample_dict["rx_unit_deatil1"] = []
    sample_dict["rx_unit_deatil2"] = []
    #rx_unit = 'Concentration'
    
    #rx_treatments = 'Gene Engineering'
    sample_dict["rx_duration"] = []
    sample_dict["rx_duration_time"] = []
    #rx_treatments = 'Gene Engineering'
        
    #rx_treatments = 'Gene Engineering'    
    sample_dict["rx_geneSymbol"] = []
    sample_dict["rx_geneID"] = []
    sample_dict["rx_geneTaxon"] = []
    #rx_treatments = 'Gene Engineering'
    
    for sampleT in sampleTreament.all():
        
        sample_dict["rx_treatments"].append(sampleT.rx_treatments.name)
        sample_dict["rx_treatments_detail"].append(sampleT.rx_treatments_detail.name)
        #sample_dict["rx_treatments_detail_detail"].append(sampleT.rx_treatments_detail_detail.name)
        
        if sampleT.rx_treatments.name == 'Gene Engineering':
            sample_dict["rx_geneSymbol"].append(sampleT.geneSymbol)
            sample_dict["rx_geneID"].append(sampleT.geneID)
            sampleT_geneTaxon = sampleT.geneTaxon
            if sampleT_geneTaxon:
                sample_dict["rx_geneTaxon"].append(sampleT_geneTaxon.name)
            else:
                sample_dict["rx_geneTaxon"].append("None")
        else:
            sample_dict["rx_amount"].append(sampleT.rx_amount)
            sample_dict["rx_unit"].append(sampleT.rx_unit.name)
            #sample_dict["rx_unit_deatil1"].append(sampleT.rx_unit_deatil.name)
            
            if sampleT.rx_unit.name != "Concentration":
                sample_dict["rx_unit_deatil1"].append(sampleT.rx_unit_deatil.name)    
            else:
                sample_dict["rx_unit_deatil2"].append(sampleT.rx_unit_deatil.name)
            

        sample_dict["rx_duration"].append(sampleT.rx_duration)
        sample_dict["rx_duration_time"].append(sampleT.rx_duration_time)
    
    sample_dict['Ubi_subcell'] = []
    for ubi_subcell in sample.ubi_subcells.all():
        sample_dict['Ubi_subcell'].append(ubi_subcell.name)
    sample_dict['Ubi_method'] = []
    for ubi_method in sample.ubi_methods.all():
        sample_dict['Ubi_method'].append(ubi_method.name)
#     sample_dict['Ubi_detergent'] = sample.ubi_detergent.name
    sample_dict['Ubi_salt'] = sample.ubi_salt
#===============================================================================
    sample_dict['comments'] = sample.ext_comments
    sample_dict['comments'] = sample.ext_comments
    sample_dict['Ispec_num'] = sample.ispec_no
    data = {'success': True, 'data':sample_dict}
    result = json.dumps(data)
    return HttpResponse(result)

# @login_required(login_url="/login/")
def experiment_loadnew(request):
    #General
    experiment_dict = {}
    no = request.POST['experiment_no']
    experiment = Experiment.objects.get(id=int(no))
    experimentId = int(no)
    
    #Experimenter
    experiment_dict['company'] = experiment.company
    experiment_dict['lab'] = experiment.lab
    experiment_dict['experimenter'] = experiment.experimenter
    
    #Date
    experiment_dict['date'] = str(experiment.date.month) + '/' + str(experiment.date.day) + '/' + str(experiment.date.year)
    
    #Funding
    experiment_dict['Funding'] = experiment.Funding
    experiment_dict['Project'] = experiment.Project
    experiment_dict['PI'] = experiment.PI
    
    #Execution
    experiment_dict['SubProject'] = experiment.SubProject
    experiment_dict['Subject'] = experiment.Subject
    experiment_dict['Manager'] = experiment.Manager
    
    #Experiment_type
    experiment_dict['Experiment_type'] = experiment.type.name
    
    #sample_num
    experiment_samples = experiment.samples.all()    #tuple
    #experiment_samples = Experiment_sample.objects.filter(experiment=experiment)
    samplenum = len(experiment_samples)
    experiment_dict['sample_num'] = samplenum
    
    #reagent_num
    experiment_reagents = Experiment_reagent.objects.filter(experiment=experiment)    #tuple
    reagentnum = len(experiment_reagents)
    experiment_dict['reagent_num'] = reagentnum
    
    #samples_Area
    #sample_no
    experiment_dict['sample_noSet'] = []
    for experiment_sample_noSet in experiment_samples.all():
        experiment_dict['sample_noSet'].append(experiment_sample_noSet.id)
        
    
    sample_count=1
    sampleNoList = []
    for sampleIndex in range(samplenum,0,-1):
        #sample_no
        experiment_dict['sample_no' + str(sample_count)] = experiment_samples[sampleIndex-1].id
        sampleNoList.append(experiment_samples[sampleIndex-1].id)  
        #index++
        sample_count = sample_count+1
    experiment_dict["sampleNoList"] = sampleNoList
    
    #amount and adjustments
    experimentSamples = Experiment_sample.objects.filter(experiment=experiment)
    experiment_dict['sampleAmountList'] = []
    experiment_dict['sampleUnitList'] = []
    experiment_dict['sampleAdjustmentsList'] = []
    sampleAmoutCount = 1
    for sampleIndex in range(samplenum,0,-1):
        experiment_dict['sample_amount' + str(sampleAmoutCount)] = experimentSamples[sampleIndex-1].amount
        experiment_dict['sampleAmountList'].append(experimentSamples[sampleIndex-1].amount)
        experiment_dict['sample_unit' + str(sampleAmoutCount)] = experimentSamples[sampleIndex-1].amount_unit
        experiment_dict['sampleUnitList'].append(experimentSamples[sampleIndex-1].amount_unit)
        experiment_dict['sample_adjustments' + str(sampleAmoutCount)] = experimentSamples[sampleIndex-1].ajustments
        experiment_dict['sampleAdjustmentsList'].append(experimentSamples[sampleIndex-1].ajustments)
        sampleAmoutCount = sampleAmoutCount+1
    
    #reagent_Area
    reagent_count=1
    reagentBufferList = []
    reagentNoList = []
    experiment_dict['reagentAmountList'] = []
    experiment_dict['reagentUnitList'] = []
    for reagentIndex in range(reagentnum,0,-1):
        #reagent_no
        experiment_dict['reagent_no' + str(reagent_count)] = experiment_reagents[reagentIndex-1].reagent.id
        reagentNoList.append(experiment_reagents[reagentIndex-1].reagent.id)
        #amount
        experiment_dict['reagent_amount' + str(reagent_count)] = experiment_reagents[reagentIndex-1].amount
        experiment_dict['reagentAmountList'].append(experiment_reagents[reagentIndex-1].amount)
        experiment_dict['reagent_unit' + str(reagent_count)] = experiment_reagents[reagentIndex-1].amount_unit
        experiment_dict['reagentUnitList'].append(experiment_reagents[reagentIndex-1].amount_unit)
        #method
        experiment_dict['Reagent_method' + str(reagent_count)] = experiment_reagents[reagentIndex-1].method.name
        #wash buffer
        experiment_dict['Reagent_buffer' + str(reagent_count)] = experiment_reagents[reagentIndex-1].wash_buffer.name
        reagentBufferList.append(experiment_reagents[reagentIndex-1].wash_buffer.name)
        #adjustments
        experiment_dict['reagent_ajustments' + str(reagent_count)] = experiment_reagents[reagentIndex-1].ajustments
        #index++
        reagent_count = reagent_count+1
    experiment_dict["reagentBufferList"] = reagentBufferList
    experiment_dict["reagentNoList"] = reagentNoList
    
    
    #Pre-Sepration
    experiment_separations = Experiment_separation.objects.filter(experiment=experiment)
    method_num = len(experiment_separations)
    experiment_dict['method_num'] = method_num
    
    experiment_dict['pre_separation_methods'] = experiment.pre_separation_methods
    
    experiment_dict['separationMethodList'] = []
    experiment_dict['separationSourceList'] = []
    experiment_dict['separationSizeList'] = []
    experiment_dict['separationBufferList'] = []
    experiment_dict['separationOthersList'] = []
    
    
    #if method_num > 0
    if method_num>0:
        experiment_separations = Experiment_separation.objects.filter(experiment=experiment)
        method_order = method_num
        #experiment_dict['separation_size'] = []
        for experiment_separation in experiment_separations:
            experiment_dict['separation_method' + str(method_order)] = experiment_separation.separation_method.name
            experiment_dict['separation_source' + str(method_order)] = experiment_separation.separation_method.source
            experiment_dict['separation_Size' + str(method_order)] = experiment_separation.separation_method.size
            #experiment_dict['separation_size'].append(experiment_separation.separation_method.size)
            experiment_dict['separation_buffer' + str(method_order)] = experiment_separation.separation_method.buffer
            experiment_dict['separation_others' + str(method_order)] = experiment_separation.separation_method.others
            
            experiment_dict['separationMethodList'].append(experiment_separation.separation_method.name)
            experiment_dict['separationSourceList'].append(experiment_separation.separation_method.source)
            experiment_dict['separationSizeList'].append(experiment_separation.separation_method.size)
            experiment_dict['separationBufferList'].append(experiment_separation.separation_method.buffer)
            experiment_dict['separationOthersList'].append(experiment_separation.separation_method.others)
            
            method_order = method_order-1
        #experiment_dict['separation_size'].reverse()
        experiment_dict['separationMethodList'].reverse()
        experiment_dict['separationSourceList'].reverse()
        experiment_dict['separationSizeList'].reverse()
        experiment_dict['separationBufferList'].reverse()
        experiment_dict['separationOthersList'].reverse()
    experiment_dict['separation_ajustments'] = experiment.separation_ajustments
    
    #Digsest
    experiment_dict['Digest_type'] = experiment.digest_type.name
    experiment_dict['Digest_enzyme'] = experiment.digest_enzyme.name
    
    #SearchDatabase-Parameter
#     custom_fastaLib_withTimeStamp = Custom_FastaLib_withTimeStamp.objects.filter(experimentId=experimentId)
#     if len(custom_fastaLib_withTimeStamp)>0:
#         custom_fastaLib_withTimeStamp = custom_fastaLib_withTimeStamp[0]
#         experiment_dict['Search_database'] = custom_fastaLib_withTimeStamp.fastaLibName
#     else:
#         experiment_dict['Search_database'] = experiment.search_database.name
    
    experiment_dict['Search_database'] = experiment.search_database.name
    experiment_dict['Instrument_manufacturer'] = experiment.instrument_manufacturer.name
    experiment_dict['Instrument_name'] = experiment.instrument_name.name
    experiment_dict['instrument_MS1'] = experiment.ms1.name
    #experiment_dict['instrument_MS1_tol'] = experiment.ms1_details.name
    experiment_dict['instrument_MS1_tol'] = experiment.ms1_details.name.split(" ")[0]
    experiment_dict['instrument_MS1_tol_unit'] = experiment.ms1_details.name.split(" ")[1]
    experiment_dict['instrument_MS2'] = experiment.ms2.name
    #experiment_dict['instrument_MS2_tol'] = experiment.ms2_details.name
    experiment_dict['instrument_MS2_tol'] = experiment.ms2_details.name.split(" ")[0]
    experiment_dict['instrument_MS2_tol_unit'] = experiment.ms2_details.name.split(" ")[1]
    
    #Modification
    experiment_dict['Fixed_Modification']=[]
    for fixed_modification in experiment.fixed_modifications.all():
        experiment_dict['Fixed_Modification'].append(fixed_modification.name)
    experiment_dict['Dynamic_Modification']=[]
    for dynamic_modification in experiment.dynamic_modifications.all():
        experiment_dict['Dynamic_Modification'].append(dynamic_modification.name)
    experiment_dict['fraction'] = experiment.fraction
    experiment_dict['repeat'] = experiment.repeat
    
    #comment
    experiment_dict['ispecno'] = experiment.fm_no
    experiment_dict['comments_conclusions'] = experiment.comments_conclusions
    
    #workflow_mode
    ######################################################################
    #add workflow by zdd
    workflowMode = experiment.workflowMode.name
    experiment_dict['workflowMode'] = workflowMode
    if workflowMode == "PRIDE" or workflowMode == "MassIVE":
        workflowMode_detail = Pride_mode.objects.all().filter(experimentId=experiment.id)[0]
        experiment_dict['pxdno'] = str(workflowMode_detail.pxdno)
        prideFileList = workflowMode_detail.prideFileList.split(",")
        fileNameList = []
        for fileURL in prideFileList:
            filename = fileURL.split("/")[-1]
            fileNameList.append(filename)
        experiment_dict['prideFileList'] = fileNameList
    
    
    searchEngine = experiment.searchEngine.name
    experiment_dict['searchEngine'] = searchEngine
    if searchEngine == "X!Tandem":
        searchEngine_detail = Xtandem_mode.objects.all().filter(experimentId=experiment.id)
        if len(searchEngine_detail)>0:
            searchEngine_detail = searchEngine_detail[0]
            experiment_dict['fragmentationMethod'] = searchEngine_detail.fragmentationMethod
            experiment_dict['cysteineProtectingGroup'] = searchEngine_detail.cysteineProtectingGroup
            experiment_dict['protease'] = searchEngine_detail.protease
            experiment_dict['numberOfAllowed13C'] = searchEngine_detail.numberOfAllowed13C
        #experiment_dict['parentMassToleranceNumber'] = workflowMode_detail.parentMassTolerance
        #experiment_dict['parentMassToleranceUnit'] = workflowMode_detail.parentMassToleranceUnit
        #experiment_dict['ionToleranceNumber'] = workflowMode_detail.ionTolerance
        #experiment_dict['ionToleranceUnit'] = workflowMode_detail.ionToleranceUnit
    if searchEngine == "Mascot": 
        searchEngine_detail = Mascot_mode.objects.all().filter(experimentId=experiment.id)
        if len(searchEngine_detail)>0:
            searchEngine_detail = searchEngine_detail[0]  
            experiment_dict['missedCleavagesAllowed'] = searchEngine_detail.missedCleavagesAllowed.name
            experiment_dict['mascotEnzyme'] = searchEngine_detail.mascotEnzyme.name
            experiment_dict['peptideCharge'] = searchEngine_detail.peptideCharge.name
            experiment_dict['precursorSearchType'] = searchEngine_detail.precursorSearchType.name
    ######################################################################
    
    ######################################################################
    #add experimentalFDR by zdd
    experimentalFDR_info = Experimentalfdr_info.objects.all().filter(experimentId=experiment.id)
    if len(experimentalFDR_info)>0:
        experimentalFDR_info = experimentalFDR_info[0]
        experimentalFDR_level = experimentalFDR_info.experimentalFDR_level
        if experimentalFDR_level == "Spectrum":
            experiment_dict['addexperimentFdr'] = "Spectrum-Level FDR"
            experiment_dict['addexperimentSpectrumFdrValue'] = experimentalFDR_info.experimentalFDR_value
        elif experimentalFDR_level == "Peptide":
            experiment_dict['addexperimentFdr'] = "Peptide-Level FDR"
            experiment_dict['addexperimentPeptideFdrValue'] = experimentalFDR_info.experimentalFDR_value
        else:
            experiment_dict['addexperimentFdr'] = "Protein-Level FDR"
            experiment_dict['addexperimentProteinFdrValue'] = experimentalFDR_info.experimentalFDR_value
    ######################################################################
 
    ######################################################################
    #add quantification methods
    experiment_dict['quantificationMethods'] = experiment.quantificationMethod.name
    ######################################################################
    
    
    #return result
    data = {'success': True, 'data':experiment_dict}
    result = json.dumps(data)
    return HttpResponse(result)





# @login_required(login_url="/login/")
def experiment_load(request):
    experiment_dict = {}
    no = request.POST['experiment_no']
    experiment = Experiment.objects.get(id=int(no))
    experiment_samples = experiment.samples.all()
    samplenum = len(experiment_samples)
    # experiment_reagents = experiment.reagents.all()
    experiment_reagents = Experiment_reagent.objects.filter(experiment=experiment)
    reagentnum = len(experiment_reagents)
    experiment_dict['expname'] = 'Exp' + no
    experiment_dict['experimenter'] = experiment.experimenter
    experiment_dict['company'] = experiment.company
    experiment_dict['lab'] = experiment.lab
    experiment_dict['Funding'] = experiment.Funding
    experiment_dict['Project'] = experiment.Project
    experiment_dict['PI'] = experiment.PI
    experiment_dict['SubProject'] = experiment.SubProject
    experiment_dict['Subject'] = experiment.Subject
    experiment_dict['Manager'] = experiment.Manager
    
    experiment_dict['fraction'] = experiment.fraction
    experiment_dict['repeat'] = experiment.repeat
    
    
    experiment_dict['experiment_no'] = experiment.id
    # experiment_dict['general_experimenter'] = experiment.experimenter.id.username
    experiment_dict['date'] = str(experiment.date.month) + '/' + str(experiment.date.day) + '/' + str(experiment.date.year)
    # experiment_dict['Project'] = experiment.Project
    # experiment_dict['location'] = experiment.location
    experiment_dict['Experiment_type'] = experiment.type.name
    experiment_dict['sample_num'] = samplenum
    experiment_dict['reagent_num'] = reagentnum

    # experiment_dict['separation_experimenter'] = experiment.separation_experimenter.id.username
    experiment_dict['separation_ajustments'] = experiment.separation_ajustments
    experiment_separations = Experiment_separation.objects.filter(experiment=experiment)
    experiment_dict['method_num'] = len(experiment_separations)
    for experiment_separation in experiment_separations:
        method_order = experiment_separation.method_order
        experiment_dict['Separation_method' + str(method_order)] = experiment_separation.separation_method.name
        # experiment_dict['separation_num' + str(method_order)] = experiment_separation.separation_num


    experiment_dict['Digest_type'] = experiment.digest_type.name
    experiment_dict['Digest_enzyme'] = experiment.digest_enzyme.name
    # experiment_dict['digest_experimenter'] = experiment.digest_experimenter.id.username

    experiment_dict['instrument_name'] = experiment.instrument_name.name
    # experiment_dict['instrument_type'] = experiment.instrument_type
    experiment_dict['search_database'] = experiment.search_database.name
    experiment_dict['instrument_name'] = experiment.instrument_name.name
    experiment_dict['ms1'] = experiment.ms1.name
    experiment_dict['ms1_details'] = experiment.ms1_details.name
    experiment_dict['ms2'] = experiment.ms2.name
    experiment_dict['ms2_details'] = experiment.ms2_details.name
    # experiment_dict['Instrument_administrator'] = experiment.instrument_administrator.name
    experiment_dict['description'] = experiment.description
    experiment_dict['ispec'] = experiment.fm_no
    experiment_dict['comments_conclusions'] = experiment.comments_conclusions
    sample_count = 1
    sample_id=''
    
    #sample_no
    experiment_dict['sample_noSet'] = []
    for experiment_sample_noSet in experiment_samples.all():
        experiment_dict['sample_noSet'].append(experiment_sample_noSet.id)
    
    experiment_dict['Fixed_Modification']=[]
    for fixed_modification in experiment.fixed_modifications.all():
        experiment_dict['Fixed_Modification'].append(fixed_modification.name)
    experiment_dict['Dynamic_Modification']=[]
    for dynamic_modification in experiment.dynamic_modifications.all():
        experiment_dict['Dynamic_Modification'].append(dynamic_modification.name)
    for experiment_sample in experiment_samples:
        experiment_dict['sample_no' + str(sample_count)] = experiment_sample.id
        tempstr=str(experiment_sample.id)
        while len(tempstr)<6:
            tempstr='0'+tempstr
        tempstr='Sam'+tempstr
        sample_id=sample_id+str(tempstr)+';'
        exp_sam = Experiment_sample.objects.filter(experiment=experiment).filter(sample=experiment_sample)
        if len(exp_sam) > 0:
            exp_sam = exp_sam[0]
        if exp_sam.amount:
            experiment_dict['sample_amount' + str(sample_count)] = str(exp_sam.amount)
        if exp_sam.amount_unit:
            experiment_dict['sample_amount' + str(sample_count)] = experiment_dict['sample_amount' + str(sample_count)] + str(exp_sam.amount_unit)
        experiment_dict['sample_ajustments' + str(sample_count)] = exp_sam.ajustments
        sample_count += 1
    sample_id=sample_id[:-1]
    experiment_dict['sample_id'] = sample_id
    reagent_count = 1
    reagent_id=''
    for experiment_reagent in experiment_reagents:
        experiment_dict['reagent_no' + str(reagent_count)] = experiment_reagent.reagent.id
        tempstr=str(experiment_reagent.reagent.id)
        while len(tempstr)<6:
            tempstr='0'+tempstr
        tempstr='Rea'+tempstr
        reagent_id=reagent_id+str(tempstr)+';'
        experiment_dict['reagent_amount' + str(reagent_count)] = experiment_reagent.amount
        experiment_dict['Reagent_method' + str(reagent_count)] = experiment_reagent.method.name
        experiment_dict['Reagent_buffer' + str(reagent_count)] = experiment_reagent.wash_buffer.name
        experiment_dict['reagent_ajustments' + str(reagent_count)] = experiment_reagent.ajustments
        reagent_count += 1
    reagent_id=reagent_id[:-1]
    experiment_dict['reagent_id'] = reagent_id
    if experiment_sample:
        temp_sample = experiment_sample
        description = ''
        if temp_sample.source_tissue:
            taxid = temp_sample.source_tissue.tissueID.name
            speci = temp_sample.source_tissue.tissueName.name
            tissue = temp_sample.source_tissue.tissueSystem.name
            organ = temp_sample.source_tissue.tissueOrgan.name 
            ts = temp_sample.source_tissue
            description = str(ts.AorM)[0].upper() + '-' + str(ts.tissueName.abbrev) + '-' + str(ts.tissueOrgan.name) + '-' + str(ts.genotype.name)
        elif temp_sample.source_cell:
            taxid = temp_sample.source_cell.tissueID.name
            try:
                speci = temp_sample.source_cell.tissueName.name
            except:
                sepci = '-'
            try:
                cell = temp_sample.source_cell.cellName.name
            except:
                cell = '-'
            sc = temp_sample.source_cell
            if sc.cellName:
                description = str(sc.AorM.name)[0].upper() + '-' + str(sc.tissueName.abbrev) + '-' + str(sc.cellName.name) + '-' + str(sc.genotype.name)
            else:
                description = str(sc.AorM.name)[0].upper() + '-' + str(sc.tissueName.abbrev) + '-' + '-' + str(sc.genotype.name)
        elif temp_sample.source_fluid:
            taxid = temp_sample.source_fluid.tissueID.name
            speci = temp_sample.source_fluid.tissueName.name
            fluid = temp_sample.source_fluid.fluid.name
            sf = temp_sample.source_fluid
            description = str(sf.AorM.name)[0].upper() + '-' + str(sf.tissueName.abbrev) + '-' + str(sf.fluid.name) + '-' + str(sf.genotype.name)
        elif temp_sample.source_others:
            taxid = ''
            speci = '-'
            tissue = '-'
        #=======================================================================
        # if temp_sample.rx_treatments.name != 'None':
        #     description = description + ';' + temp_sample.rx_treatments_detail.name
        # if temp_sample.rx_unit_deatil:
        #     description = description + '-' + temp_sample.rx_amount + temp_sample.rx_unit_deatil.name
        # if temp_sample.rx_duration_time:
        #     description = description + '-' + str(temp_sample.rx_duration) + str(temp_sample.rx_duration_time)
        #=======================================================================
        experiment_dict['description'] = experiment.description
    data = {'success': True, 'data':experiment_dict}
    result = json.dumps(data)
    return HttpResponse(result)

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# @login_required(login_url="/login/")
def reagent_edit_save(request):
    if request.method == 'POST':
        lab = User_Laboratory.objects.filter(user=request.user)
        lab = lab[0].lab.name if lab.count() else ''
        
        no = request.POST['reagent_no']
        reagent = Reagent.objects.get(id=int(no))
        if lab==reagent.experimenter.lab.name or request.user.is_superuser:
            #Experimenter
            #experimenter = All_Experimenter.objects.get(name=request.POST['experimenter'])
            experimenter = All_Experimenter.objects.filter(name=request.POST['experimenter'])#.filter(lab=lab)[0]
            company = All_Company.objects.get(name=request.POST['company'])
            lab = All_Laboratory.objects.get(name=request.POST['lab'])
            (exp_info, sign) = Experimenter_info.objects.get_or_create(company=company,
                                                                       lab=lab,
                                                                       experimenter=experimenter
                                                                       )
            reagent.experimenter = exp_info          
            
            #Reagent type
            reagent.type = request.POST['reagent_type']
           
            #Reagent Name
            reagent.name = request.POST['name']
           
            #Date
            (month, day, year) = request.POST['date'].split('/')
            reagent_date = date(int(year), int(month), int(day))
            reagent.date = reagent_date
           
            #Manufacturer
            (reagent_manufacturer, sign) = Reagent_manufacturer.objects.get_or_create(name=request.POST['Reagent_manufacturer'])
            reagent.manufacturer=reagent_manufacturer
           
            #Catalog No
            reagent.catalog_no = request.POST['catalog_no']
           
            #Conjugate Beads
            (conjugate, sign) = Conjugate.objects.get_or_create(name=request.POST['Conjugate'])
            reagent.conjugate = conjugate
            #UBI Info
            
            #Ispec No
            reagent.ispec_no=request.POST['Ispec_num']
            reagent.ext_comments = request.POST['comments'] 
           
            #Source Species
            react_species_list = []
            react_species_list = request.POST.getlist('React_species_source')
            for react_species_name in react_species_list:
                (react_species, sign) = React_species.objects.get_or_create(name=react_species_name)
                reagent.react_species_sources.add(react_species)
               
            react_species_list = request.POST.getlist('React_species_target')
            for react_species_name in react_species_list:
                (react_species, sign) = React_species.objects.get_or_create(name=react_species_name)
                reagent.react_species_targets.add(react_species)
            
            #Application
            application_list = []
            application_list = request.POST.getlist('Application')
            for application_name in application_list:
                (application, sign) = Application.objects.get_or_create(name=application_name)
                reagent.applications.add(application)
            
            if reagent.type == 'Antigen':
                (host_species, sign) = Antigen_species.objects.get_or_create(name=request.POST['Antigen_species'])
                (clonal_type, sign) = Antigen_clonal_type.objects.get_or_create(name=request.POST['Antigen_clonal_type'])
                (modification, sign) = Antigen_modification.objects.get_or_create(name=request.POST['Antigen_modification'])
                antigen = Antigen(gene_id=request.POST['gene_id'],
                                  host_species=host_species,
                                  clonal_type=clonal_type,
                                  modification=modification
                                  )
                antigen.save()
                reagent.antigen = antigen
               
            elif reagent.type == 'DNA':
                dna_info = Dna_info(sequence=request.POST['dna_sequence'])
                dna_info.save()
                reagent.dna_info = dna_info
            elif reagent.type == 'Protein':
                domain_info = Domain_info(domain=request.POST['domain'])
                domain_info.save()
                reagent.domain_info = domain_info
            elif reagent.type == 'other':
                remarks_info = Remarks_info(remarks=request.POST['remarks'])
                remarks_info.save()
                reagent.remarks_info = remarks_info
            elif reagent.type == 'chemical':
                chemical_info = Chemical_info(chemical=request.POST['cas_number'])
                chemical_info.save()
                reagent.chemical_info = chemical_info
            else:
                raise Http44()
            reagent.save()
            success = True
            msg = str(reagent.id)
            data = {'success': success, 'msg':msg}
            result = json.dumps(data)
            return HttpResponse(result)
        else:
            raise Http404()
    else:
        raise Http404()


'''
def reagent_edit_save(request):
    if request.method == 'POST':
        no = request.POST['reagent_no']
        reagent = Reagent.objects.get(id=int(no))
        if reagent.experimenter.id == request.user or request.user.is_superuser:
            name = request.POST['name']
            reagent_type = request.POST['reagent_type']
            (reagent_manufacturer, sign) = Reagent_manufacturer.objects.get_or_create(name=request.POST['Reagent_manufacturer'])
            catalog_no = request.POST['catalog_no']
            (affinity, sign) = Affinity.objects.get_or_create(name=request.POST['Affinity'])
            (purification, sign) = Purification.objects.get_or_create(name=request.POST['Purification'])
            (conjugate, sign) = Conjugate.objects.get_or_create(name=request.POST['Conjugate'])

            reagent.type = reagent_type
            reagent.name = name
            reagent.manufacturer = reagent_manufacturer
            reagent.catalog_no = catalog_no
            reagent.affinity = affinity
            reagent.purification = purification
            reagent.conjugate = conjugate

            reagent.applications.clear()
            application_list = request.POST.getlist('Application')
            for application_name in application_list:
                (application, sign) = Application.objects.get_or_create(name=application_name)
                reagent.applications.add(application)

            reagent.react_speciess.clear()
            react_species_list = request.POST.getlist('React_species')
            for react_species_name in react_species_list:
                (react_species, sign) = React_species.objects.get_or_create(name=react_species_name)
                reagent.react_speciess.add(react_species)

            if reagent_type == 'Antigen':
                antigen = reagent.antigen
                (host_species, sign) = Antigen_species.objects.get_or_create(name=request.POST['Antigen_species'])
                (clonal_type, sign) = Antigen_clonal_type.objects.get_or_create(name=request.POST['Antigen_clonal_type'])
                (modification, sign) = Antigen_modification.objects.get_or_create(name=request.POST['Antigen_modification'])
                antigen.gene_id = request.POST['gene_id']
                antigen.host_species = host_species
                antigen.clonal_type = clonal_type
                antigen.modification = modification
                antigen.save()
            elif reagent_type == 'DNA':
                dna_info = reagent.dna_info
                dna_info.sequence = request.POST['dna_sequence']
                dna_info.save()
            elif reagent_type == 'Protein':
                domain_info = reagent.domain_info
                domain_info.domain = request.POST['domain']
                domain_info.save()
            elif reagent_type == 'other':
                remarks_info = reagent.remarks_info
                remarks_info.remarks = request.POST['remarks']
                remarks_info.save()
            reagent.save()
            return HttpResponseRedirect('/experiments/reagent/')
        else:
            raise Http404()
    else:
        raise Http404()
'''
# @login_required(login_url="/login/")
def sample_edit_save(request):
    if request.method == 'POST':
        
        lab = User_Laboratory.objects.filter(user=request.user)
        lab = lab[0].lab.name if lab.count() else ''
        
        no = request.POST['sample_no']
        sample = Sample.objects.get(id=int(no))
        
        '''
        lab = experiments.models.User_Laboratory.objects.filter(user=request.user)
        lab = lab[0].lab.name if lab.count() else ''
        no = request.GET['sample_no']
        sample = experiments.models.Sample.objects.get(id=int(no))
    
        #ensure the current accout relate to the right lab
        if lab==sample.experimenter.lab.name:
        '''
        
        if lab==sample.experimenter.lab.name or request.user.is_superuser:
            
            #sample = None
            #Experimenter
            all_experimenter = All_Experimenter.objects.filter(name=request.POST['experimenter'])[0]
            #all_experimenter = All_Experimenter.objects.filter(name=request.POST['experimenter']).filter(lab=lab)
            #all_experimenter = All_Experimenter.objects.get(name=request.POST['experimenter'])  # maybe some people will have same name..s
            #all_experimenter = All_Experimenter.objects.filter(name=request.POST['experimenter']).filter(lab=lab)[0]
            #new
            #all_experimenter = All_Experimenter.objects.filter(name=request.POST['experimenter']).filter(lab=lab)[0]
            
            all_company = All_Company.objects.get(name=request.POST['company'])
            all_lab = All_Laboratory.objects.get(name=request.POST['lab'])
            (exp_info, sign) = Experimenter_info.objects.get_or_create(
                                                                       company=all_company,
                                                                       lab=all_lab,
                                                                       experimenter=all_experimenter
                                                                       )
            sample.experimenter = exp_info
            
            #Date
            (month, day, year) = request.POST['date'].split('/')
            sample_date = date(int(year), int(month), int(day))   
            sample.date = sample_date
            
            #Sample Location
            (container, sign) = Container.objects.get_or_create(name=request.POST['location'])
            if request.POST['location'] == 'Refrigerator':
                container_No = Refrigerator_No.objects.get(name=request.POST['RefrigeratorNo'])
                container_basket = Refrigerator_Temperature.objects.get(name=request.POST['RefrigeratorTemper'])
                container_layer = Refrigerator_Layer.objects.get(name=request.POST['RefrigeratorLayer'])
                (refrigerator, sign) = Location_Refrigerator.objects.get_or_create(
                                                                                   no=container_No,
                                                                                   temperature=container_basket,
                                                                                   layer=container_layer
                                                                                   )
                (location, sign) = Location.objects.get_or_create(refrigerator=refrigerator)
            elif request.POST['location'] == 'Liquid Nitrogen':
                container_No = Nitrogen_Container.objects.filter(name=request.POST['Nitrogen_Container'])[0]
                container_basket = Nitrogen_Basket.objects.filter(name=request.POST['Nitrogen_Basket'])[0]
                container_layer = Nitrogen_Layer.objects.filter(name=request.POST['Nitrogen_Layer'])[0]
                (nitrogen, sign) = Location_Nitrogen.objects.get_or_create(
                                                                           no=container_No,
                                                                           basket=container_basket,
                                                                           layer=container_layer
                                                                           )
                (location, sign) = Location.objects.get_or_create(nitrogen=nitrogen)
            elif request.POST['location'] == 'Others':
                temperature = Others_Temperature.objects.get(name=request.POST['Others_Temperature'])
                locations = request.POST['Others_location']
                (locationOthers, sign) = Location_Others.objects.get_or_create(
                                                                               temperature=temperature,
                                                                               location=locations
                                                                               )
                (location, sign) = Location.objects.get_or_create(others=locationOthers)
            else:
                raise Http404()
            sample.location=location

            #None Area                                
            sample.source_tissue = None
            sample.source_cell = None
            sample.source_fluid = None
            sample.source_others = None
            
            #Source Type 
            cell_tissue = request.POST['cell_tissue']
            #sample.cell_tissue = cell_tissue
            if cell_tissue == 'Tissue':               
                (AorM, sign) = Source_TissueTaxonAorM.objects.get_or_create(name=request.POST['Source_TissueTaxonAorM'])
                (tissueName, sign) = Source_TissueTaxonName.objects.get_or_create(name=request.POST['tissueName'])
                (tissueID, sign) = Source_TissueTaxonID.objects.get_or_create(name=request.POST['tissueID'])
                tissueStrain = Source_TissueTaxonStrain.objects.filter(pid__name=request.POST['tissueID']).filter(name=request.POST['tissueStrain'])[0]
                (gender, sign) = Tissue_gender.objects.get_or_create(name=request.POST['Tissue_gender'])
                (genotype, sign) = Genotype.objects.get_or_create(name=request.POST['Genotype'])
                (tissueSystem, sign) = Source_TissueSystem.objects.get_or_create(name=request.POST['Source_TissueSystem'])
                (tissueOrgan, sign) = Source_TissueOrgan.objects.get_or_create(name=request.POST['Source_TissueOrgan'], pid=tissueSystem)
                tissueStructure = request.POST['Source_TissueStructure']
                (tissueType, sign) = Source_TissueType.objects.get_or_create(name=request.POST['Source_TissueType'])
                age = request.POST['tissue_age']
                (age_unit, sign) = All_AgeUnit.objects.get_or_create(name=request.POST['All_AgeUnit'])
                try:
                    circ_time = request.POST['circ_time']
                except:
                    circ_time = ''
                gene_num = int(request.POST['Gene_num'])
                gene = ''
                for gene_order in range(1, gene_num + 1):
                    gene = gene + request.POST['geneSymbol' + str(gene_order)] + '|' + request.POST['GeneID' + str(gene_order)] + '|' + request.POST['geneTaxon' + str(gene_order)] + ';'
                gene = gene[:-1]
                specific_ID = request.POST['Specific_ID']
                source_tissue = Source_tissue(AorM=AorM,
                                              tissueName=tissueName,
                                              tissueID=tissueID,
                                              tissueStrain=tissueStrain,
                                              gender=gender,
                                              tissueSystem=tissueSystem,
                                              tissueOrgan=tissueOrgan,
                                              tissueType=tissueType,
                                              genotype=genotype,
                                              gene=gene,
                                              tissueStructure=tissueStructure,
                                              age=age,
                                              age_unit=age_unit,
                                              circ_time=circ_time,
                                              specific_ID=specific_ID
                                              )
                source_tissue.save()
                sample.source_tissue = source_tissue
                sample.save()
            
            #cell_tissue == 'Cell': 
            elif cell_tissue == 'Cell':
                (AorM, sign) = Source_TissueTaxonAorM.objects.get_or_create(name=request.POST['Source_TissueTaxonAorM'])
                tissueName = Source_TissueTaxonName.objects.filter(name=request.POST['tissueName'])[0]
                (tissueID, sign) = Source_TissueTaxonID.objects.get_or_create(name=request.POST['tissueID'])
                tissueStrain = Source_TissueTaxonStrain.objects.filter(pid__name=request.POST['tissueID']).filter(name=request.POST['tissueStrain'])[0]
                try:
                    circ_time = request.POST['circ_time']
                except:
                    circ_time = ''
                (genotype, sign) = Genotype.objects.get_or_create(name=request.POST['Genotype'])
                try:
                    circ_time = request.POST['circ_time']
                except:
                    circ_time = ''
                gene_num = int(request.POST['Gene_num'])
                gene = ''
                for gene_order in range(1, gene_num + 1):
                    gene = gene + request.POST['geneSymbol' + str(gene_order)] + '|' + request.POST['GeneID' + str(gene_order)] + '|' + request.POST['geneTaxon' + str(gene_order)] + ';'
                gene = gene[:-1]
                source_cell = Source_cell(AorM=AorM,
                                          tissueName=tissueName,
                                          tissueID=tissueID,
                                          tissueStrain=tissueStrain,
                                          genotype=genotype,
                                          gene=gene,
                                          circ_time=circ_time,
                                          specific_ID=request.POST['Specific_ID']
                                          )
                #source_cell.save()
                if request.POST['Source_TissueTaxonAorM'] != 'Microorganism':
                    (celltype, sign) = source_CellType.objects.get_or_create(name=request.POST['cellcelltype'])
                    (cellName, sign) = Cell_Name.objects.get_or_create(name=request.POST['Cell_Name'], pid=celltype)
                    source_cell.cellType = celltype
                    source_cell.cellName = cellName
                    #source_cell.save()
                source_cell.save()
                sample.source_cell = source_cell
                sample.save()
                
            elif cell_tissue == 'Fluid':
                (AorM, sign) = Source_TissueTaxonAorM.objects.get_or_create(name=request.POST['Source_TissueTaxonAorM'])
                tissueName = Source_TissueTaxonName.objects.filter(name=request.POST['tissueName'])[0]
                (tissueID, sign) = Source_TissueTaxonID.objects.get_or_create(name=request.POST['tissueID'])
                tissueStrain = Source_TissueTaxonStrain.objects.filter(pid__name=request.POST['tissueID']).filter(name=request.POST['tissueStrain'])[0]
                try:
                    circ_time = request.POST['circ_time']
                except:
                    circ_time = ''
                try:
                    circ_time = request.POST['circ_time']
                except:
                    circ_time = ''
                age = request.POST['tissue_age']
                (age_unit, sign) = All_AgeUnit.objects.get_or_create(name=request.POST['All_AgeUnit'])
                (gender, sign) = Tissue_gender.objects.get_or_create(name=request.POST['Tissue_gender'])
                (fluid, sign) = Fluid_name.objects.get_or_create(name=request.POST['Fluid_name'])
                (genotype, sign) = Genotype.objects.get_or_create(name=request.POST['Genotype'])
                gene_num = int(request.POST['Gene_num'])
                gene = ''
                for gene_order in range(1, gene_num + 1):
                    gene = gene + request.POST['geneSymbol' + str(gene_order)] + '|' + request.POST['GeneID' + str(gene_order)] + '|' + request.POST['geneTaxon' + str(gene_order)] + ';'
                gene = gene[:-1]
                source_fluid = Source_fluid(AorM=AorM,
                                            tissueName=tissueName,
                                            tissueID=tissueID,
                                            age=age,
                                            age_unit=age_unit,
                                            tissueStrain=tissueStrain,
                                            gene=gene,
                                            fluid=fluid,
                                            gender=gender,
                                            genotype=genotype,
                                            circ_time=circ_time,
                                            specific_ID=request.POST['Specific_ID']
                                            )
                source_fluid.save()
                sample.source_fluid = source_fluid
                sample.save()
            
            #cell_tissue == "Others"
            elif cell_tissue == 'Others':
                source_others = Source_others(name=request.POST['tissue_others'])
                source_others.save()
                sample.source_others = source_others
                sample.save()
            
            else:
                raise Http404()
            
            ##############################################
            
            #Total number of Treatment
            sample.treatments = []
            treat_num = int(request.POST['treat_num'])
            for treat_order in range(1, treat_num + 1):
                if request.POST['Rx_treatment' + str(treat_order)] != 'None':
                    if request.POST['Rx_treatment' + str(treat_order)] != 'Gene Engineering':
                        (rx_unit, sign) = Rx_unit.objects.get_or_create(name=request.POST['Rx_unit' + str(treat_order)])
                        if request.POST['Rx_unit' + str(treat_order)] != 'Concentration':
                            (rx_unit_deatil, sign) = Rx_unit_detail.objects.get_or_create(name=request.POST['unit_detail_' + str(treat_order)],
                                                                                          type=rx_unit
                                                                                          )
                        else:
                            (rx_unit_deatil, sign) = Rx_unit_detail.objects.get_or_create(name=request.POST['unit_detail2_' + str(treat_order)]
                                                                                          + '/' + request.POST['unit_detail22_' + str(treat_order)],
                                                                                          type=rx_unit
                                                                                          )
                        rx_amount = request.POST['amount' + str(treat_order)]
                    else:
                        rx_amount = ''
                        rx_unit = ''
                        rx_unit_deatil = ''
                    rx_duration = request.POST['duration' + str(treat_order)]
                    rx_duration_time = request.POST['rx_dur_unit' + str(treat_order)]
                    (rx_treatments, sign) = Rx_treatment.objects.get_or_create(name=request.POST['Rx_treatment' + str(treat_order)])
                    (rx_treatments_detail, sign) = Rx_treatment_detail.objects.get_or_create(name=request.POST['all_detail' + str(treat_order)], 
                                                                                             type=rx_treatments
                                                                                             )
                    treatment = Treatment(
                                          rx_treatments=rx_treatments,
                                          rx_treatments_detail=rx_treatments_detail,
                                          rx_duration=rx_duration,
                                          rx_duration_time=rx_duration_time,
                                          )
                    treatment.save()
                    if request.POST['Rx_treatment' + str(treat_order)] != 'Gene Engineering':
                        treatment.rx_amount = rx_amount
                        treatment.rx_unit = rx_unit
                        treatment.rx_unit_deatil = rx_unit_deatil
                        treatment.save()
                    try:
                        geneTaxon = Source_TissueTaxonID.objects.filter(name=request.POST['newGeneTaxon' + str(treat_order)])[0]
                        geneSymbol = request.POST['newGeneSymbol' + str(treat_order)]
                        geneID = request.POST['newGeneID' + str(treat_order)]
                        treatment.geneTaxon = geneTaxon
                        treatment.geneSymbol = geneSymbol
                        treatment.geneID = geneID
                        treatment.save()
                    except:
                        treatment.save()
                sample.treatments.add(treatment) 
            
            #Infomation
            
            ubi_subcell_list = request.POST.getlist('Ubi_subcell')
            ubi_subcell_list_old = sample.ubi_subcells.all()
            for temp in ubi_subcell_list_old:
                if temp not in ubi_subcell_list:
                    print "delete"
                    sample.ubi_subcells.remove(temp)
             
            for temp in ubi_subcell_list:
                if temp not in ubi_subcell_list_old:
                    print "add"
                    (ubi_subcell, sign) = Ubi_subcell.objects.get_or_create(name=temp)
                    sample.ubi_subcells.add(ubi_subcell)
            
            
#             for subcell_name in ubi_subcell_list:
#                 (ubi_subcell, sign) = Ubi_subcell.objects.get_or_create(name=subcell_name)
#                 sample.ubi_subcells.add(ubi_subcell)
                
                         
            ubi_method_list = request.POST.getlist('Ubi_method')
            ubi_method_list_old = sample.ubi_methods.all()
            for temp in ubi_method_list_old:
                if temp not in ubi_method_list:
                    print "delete"
                    sample.ubi_methods.remove(temp)
             
            for temp in ubi_method_list:
                if temp not in ubi_method_list_old:
                    print "add"
                    (ubi_method, sign) = Ubi_method.objects.get_or_create(name=temp)
                    sample.ubi_methods.add(ubi_method)
            
#             for method_name in ubi_method_list:
#                 (ubi_method, sign) = Ubi_method.objects.get_or_create(name=method_name)
#                 sample.ubi_methods.add(ubi_method)
            
            
            
            
            
            sample.ubi_salt=request.POST['Ubi_salt']
          
            #Comments
            sample.ext_comments = request.POST['comments']
            sample.ispec_no=request.POST['Ispec_num']
            sample.save()
            
            #send message of saving success
            success = True
            msg = "Sample motified"
            data = {'success': success, 'msg':str(sample.id)}
            result = json.dumps(data)
            return HttpResponse(result)
        else:
            raise Http404()
    else:
        raise Http404()
'''
def sample_edit_save(request):
    if request.method == "POST":
        no = request.POST["sample_no"]
        sample = Sample.objects.get(id=int(no))
        if sample.experimenter.id == request.user or request.user.is_superuser:
             
            #Experimenter
            experimenter = All_Experimenter.objects.get(name=request.POST['experimenter'])
            company = All_Company.objects.get(name=request.POST['company'])
            lab = All_Laboratory.objects.get(name=request.POST['lab'])
            (exp_info, sign) = Experimenter_info.objects.get_or_create(company=company,
                                                                        lab=lab,
                                                                        experimenter=experimenter)
             #Date
            (month, day, year) = request.POST['date'].split('/')
            sample_date = date(int(year), int(month), int(day))
             
             #Sample Location
            (container, sign) = Container.objects.get_or_create(name=request.POST['location'])
            if request.POST['location'] == 'Refrigerator':
                container_No = Refrigerator_No.objects.get(name=request.POST['RefrigeratorNo'])
                container_basket = Refrigerator_Temperature.objects.get(name=request.POST['RefrigeratorTemper'])
                container_layer = Refrigerator_Layer.objects.get(name=request.POST['RefrigeratorLayer'])
                (refrigerator, sign) = Location_Refrigerator.objects.get_or_create(no=container_No, 
                                                                                   temperature=container_basket,
                                                                                   layer=container_layer)
                (location, sign) = Location.objects.get_or_create(refrigerator=refrigerator)
            
            elif request.POST['location'] == 'Liquid Nitrogen':
                container_No = Nitrogen_Container.objects.filter(name=request.POST['Nitrogen_Container'])[0]
                container_basket = Nitrogen_Basket.objects.filter(name=request.POST['Nitrogen_Basket'])[0]
                container_layer = Nitrogen_Layer.objects.filter(name=request.POST['Nitrogen_Layer'])[0]
                (nitrogen, sign) = Location_Nitrogen.objects.get_or_create(no=container_No, basket=container_basket, layer=container_layer)
                (location, sign) = Location.objects.get_or_create(nitrogen=nitrogen)
            
            #request.POST['location'] == 'Others':            
            else: 
                temperature = Others_Temperature.objects.get(name=request.POST['Others_Temperature'])
                locations = request.POST['Others_location']
                (locationOthers, sign) = Location_Others.objects.get_or_create(temperature=temperature, location=locations)
                (location, sign) = Location.objects.get_or_create(others=locationOthers)
            
            #sample.save in fixed location
            sample = Sample(date=sample_date,
                            experimenter=exp_info,
                            location=location,
                            ubi_salt=request.POST['Ubi_salt'],
                            ext_comments=request.POST['comments'],
                            ispec_no=request.POST['Ispec_num'])
            
            
            sample.save()
            
            #Treatments
            sample.treatments.clear()
            treat_num = int(request.POST['treat_num'])
            for treat_order in range(1, treat_num + 1):
                if request.POST['Rx_treatment' + str(treat_order)] != 'None':
                    if request.POST['Rx_treatment' + str(treat_order)] != 'Gene Engineering':
                        (rx_unit, sign) = Rx_unit.objects.get_or_create(name=request.POST['Rx_unit' + str(treat_order)])
                        #try
                        if request.POST['Rx_unit' + str(treat_order)] != 'Concentration':
                            (rx_unit_deatil, sign) = Rx_unit_detail.objects.get_or_create(name=request.POST['unit_detail_' + str(treat_order)],
                                                                                          type=rx_unit)
                        else:
                            (rx_unit_deatil, sign) = Rx_unit_detail.objects.get_or_create(name=request.POST['unit_detail2_' + str(treat_order)]
                                                                                          + '/' + request.POST['unit_detail22_' + str(treat_order)],
                                                                                          type=rx_unit)
                        rx_amount = request.POST['amount' + str(treat_order)]
                    else:
                        rx_amount = ''
                        rx_unit = ''
                        rx_unit_deatil = ''
                            
                    rx_duration = request.POST['duration' + str(treat_order)]
                    rx_duration_time = request.POST['rx_dur_unit' + str(treat_order)]
                    
                    (rx_treatments, sign) = Rx_treatment.objects.get_or_create(name=request.POST['Rx_treatment' + str(treat_order)])
                    (rx_treatments_detail, sign) = Rx_treatment_detail.objects.get_or_create(name=request.POST['all_detail' + str(treat_order)], type=rx_treatments)
                    treatment = Treatment(rx_treatments=rx_treatments,
                                          rx_treatments_detail=rx_treatments_detail,
                                          rx_duration=rx_duration,
                                          rx_duration_time=rx_duration_time)
                    treatment.save()
                    
                    if request.POST['Rx_treatment' + str(treat_order)] != 'Gene Engineering':
                        treatment.rx_amount = rx_amount
                        treatment.rx_unit = rx_unit
                        treatment.rx_unit_deatil = rx_unit_deatil
                        treatment.save()
                    try:
                        geneTaxon = Source_TissueTaxonID.objects.filter(name=request.POST['newGeneTaxon' + str(treat_order)])[0]
                        geneSymbol = request.POST['newGeneSymbol' + str(treat_order)]
                        geneID = request.POST['newGeneID' + str(treat_order)]
                        treatment.geneTaxon = geneTaxon
                        treatment.geneSymbol = geneSymbol
                        treatment.geneID = geneID
                        treatment.save()
                    except:
                        treatment.save()
                sample.treatments.add(treatment)
                
                #Source Type
                cell_tissue = request.POST['cell_tissue']
                if cell_tissue == 'Tissue':
                    (AorM, sign) = Source_TissueTaxonAorM.objects.get_or_create(name=request.POST['Source_TissueTaxonAorM'])
                    (tissueName, sign) = Source_TissueTaxonName.objects.get_or_create(name=request.POST['tissueName'])
                    (tissueID, sign) = Source_TissueTaxonID.objects.get_or_create(name=request.POST['tissueID'])
                    tissueStrain = Source_TissueTaxonStrain.objects.filter(pid__name=request.POST['tissueID']).filter(name=request.POST['tissueStrain'])[0]
                    (gender, sign) = Tissue_gender.objects.get_or_create(name=request.POST['Tissue_gender'])
                    (genotype, sign) = Genotype.objects.get_or_create(name=request.POST['Genotype'])
                    (tissueSystem, sign) = Source_TissueSystem.objects.get_or_create(name=request.POST['Source_TissueSystem'])
                    (tissueOrgan, sign) = Source_TissueOrgan.objects.get_or_create(name=request.POST['Source_TissueOrgan'], pid=tissueSystem)
                    tissueStructure = request.POST['Source_TissueStructure']
                    (tissueType, sign) = Source_TissueType.objects.get_or_create(name=request.POST['Source_TissueType'])
                    age = request.POST['tissue_age']
                    (age_unit, sign) = All_AgeUnit.objects.get_or_create(name=request.POST['All_AgeUnit'])
                    try:
                        circ_time = request.POST['circ_time']
                    except:
                        circ_time = ''
                    gene_num = int(request.POST['Gene_num'])
                    gene = ''
                    for gene_order in range(1, gene_num + 1):
                        gene = gene + request.POST['geneSymbol' + str(gene_order)] + '|' + request.POST['GeneID' + str(gene_order)] + '|' + request.POST['geneTaxon' + str(gene_order)] + ';'
                    gene = gene[:-1]
                    specific_ID = request.POST['Specific_ID']
                    source_tissue = Source_tissue(AorM=AorM,
                                          tissueName=tissueName,
                                          tissueID=tissueID,
                                          tissueStrain=tissueStrain,
                                          gender=gender,
                                          tissueSystem=tissueSystem,
                                          tissueOrgan=tissueOrgan,
                                          tissueType=tissueType,
                                          genotype=genotype,
                                          gene=gene,
                                          tissueStructure=tissueStructure,
                                          # geneTaxon=geneTaxon,
                                          # geneSymbol=request.POST['geneSymbol'],
                                          # geneID=request.POST['GeneID'],
                                          age=age,
                                          age_unit=age_unit,
                                          circ_time=circ_time,
                                          specific_ID=specific_ID)
                    source_tissue.save()
                    sample.source_tissue = source_tissue
                    sample.save()
                
                elif cell_tissue == 'Cell':    
                    (AorM, sign) = Source_TissueTaxonAorM.objects.get_or_create(name=request.POST['Source_TissueTaxonAorM'])
                    tissueName = Source_TissueTaxonName.objects.filter(name=request.POST['tissueName'])[0]
                    (tissueID, sign) = Source_TissueTaxonID.objects.get_or_create(name=request.POST['tissueID'])
                    tissueStrain = Source_TissueTaxonStrain.objects.filter(pid__name=request.POST['tissueID']).filter(name=request.POST['tissueStrain'])[0]
                    try:
                        circ_time = request.POST['circ_time']
                    except:
                        circ_time = ''
                    (genotype, sign) = Genotype.objects.get_or_create(name=request.POST['Genotype'])
                    try:
                        circ_time = request.POST['circ_time']
                    except:
                        circ_time = ''    
                    gene_num = int(request.POST['Gene_num'])
                    gene = ''
                    for gene_order in range(1, gene_num + 1):
                        gene = gene + request.POST['geneSymbol' + str(gene_order)] + '|' + request.POST['GeneID' + str(gene_order)] + '|' + request.POST['geneTaxon' + str(gene_order)] + ';'
                    gene = gene[:-1]
                    source_cell = Source_cell(AorM=AorM,
                                      tissueName=tissueName,
                                      tissueID=tissueID,
                                      tissueStrain=tissueStrain,
                                      genotype=genotype,
                                      gene=gene,
                                      circ_time=circ_time,
                                      specific_ID=request.POST['Specific_ID'])
                    source_cell.save()
                    if request.POST['Source_TissueTaxonAorM'] != 'Microorganism':
                        (celltype, sign) = source_CellType.objects.get_or_create(name=request.POST['cellcelltype'])
                        (cellName, sign) = Cell_Name.objects.get_or_create(name=request.POST['Cell_Name'], pid=celltype)
                        source_cell.cellType = celltype
                        source_cell.cellName = cellName
                        source_cell.save()
                    sample.source_cell = source_cell
                    sample.save()
                
                elif cell_tissue == 'Fluid':
                    (AorM, sign) = Source_TissueTaxonAorM.objects.get_or_create(name=request.POST['Source_TissueTaxonAorM'])
                    tissueName = Source_TissueTaxonName.objects.filter(name=request.POST['tissueName'])[0]
                    (tissueID, sign) = Source_TissueTaxonID.objects.get_or_create(name=request.POST['tissueID'])
                    tissueStrain = Source_TissueTaxonStrain.objects.filter(pid__name=request.POST['tissueID']).filter(name=request.POST['tissueStrain'])[0]
                    try:
                        circ_time = request.POST['circ_time']
                    except:
                        circ_time = ''
                    # (genotype, sign) = Genotype.objects.get_or_create(name=request.POST['Genotype'])
                    try:
                        circ_time = request.POST['circ_time']
                    except:
                        circ_time = ''
                    age = request.POST['tissue_age']
                    (age_unit, sign) = All_AgeUnit.objects.get_or_create(name=request.POST['All_AgeUnit'])
                    (gender, sign) = Tissue_gender.objects.get_or_create(name=request.POST['Tissue_gender'])
                    (fluid, sign) = Fluid_name.objects.get_or_create(name=request.POST['Fluid_name'])
                    gene_num = int(request.POST['Gene_num'])
                    gene = ''
                    for gene_order in range(1, gene_num + 1):
                        gene = gene + request.POST['geneSymbol' + str(gene_order)] + '|' + request.POST['GeneID' + str(gene_order)] + '|' + request.POST['geneTaxon' + str(gene_order)] + ';'
                    gene = gene[:-1]
                    source_fluid = Source_fluid(AorM=AorM,
                                      tissueName=tissueName,
                                      tissueID=tissueID,
                                      age=age,
                                      age_unit=age_unit,
                                      tissueStrain=tissueStrain,
                                      gene=gene,
                                      fluid=fluid,
                                      gender=gender,
                                      genotype=genotype,
                                      circ_time=circ_time,
                                      specific_ID=request.POST['Specific_ID'])
                    source_fluid.save()
                    sample.source_fluid = source_fluid
                    sample.save() 
                
                elif cell_tissue == 'Others':
                    source_others = Source_others(name=request.POST['tissue_others'])
                    source_others.save()
                    sample.source_others = source_others
                    sample.save()
            
                sample.ubi_subcells.clear()
                ubi_subcell_list = request.POST.getlist('Ubi_subcell')
                for subcell_name in ubi_subcell_list:
                    (ubi_subcell, sign) = Ubi_subcell.objects.get_or_create(name=subcell_name)
                    sample.ubi_subcells.add(ubi_subcell)
                
                sample.ubi_methods.clear()
                ubi_method_list = request.POST.getlist('Ubi_method')
                for method_name in ubi_method_list:
                    (ubi_method, sign) = Ubi_method.objects.get_or_create(name=method_name)
                    sample.ubi_methods.add(ubi_method)
                
                sample.save()
                return HttpResponseRedirect('/experiments/sample/')
                #success = True
                #msg = "Sample Added"
                #data = {'success': success, 'msg':str(sample.id)}
                # = json.dumps(data)
                #return HttpResponse(result)
        else:
            raise Http404()
    else:
        raise Http404()
            
  '''          
            
def experiment_edit_save(request):
    if request.method == 'POST':
        lab = User_Laboratory.objects.filter(user=request.user)
        lab = lab[0].lab.name if lab.count() else ''
        no = request.POST['experiment_no']
        experiment = Experiment.objects.get(id=int(no))
        
        if lab==experiment.lab or request.user.is_superuser:
            #None Area
            
            #Experimenter
            company = request.POST['company']
            lab = request.POST['lab']
            experimenter = request.POST['experimenter']
            #Date
            (month, day, year) = request.POST['date'].split('/')
            experiment_date = date(int(year), int(month), int(day))
            #Funding
            Funding = request.POST['Funding']
            Project = request.POST['Project']
            PI = request.POST['PI']
            #Execution
            SubProject = request.POST['SubProject']
            if SubProject == 'SubProject':
                SubProject = ''
            Subject = request.POST['Subject']
            if Subject == 'Subject':
                Subject = ''
            Manager = request.POST['Manager']
            if Manager == 'Manager Name':
                Manager = ''
            #Experiment_tyoe
            (experiment_type, sign) = Experiment_type.objects.get_or_create(name=request.POST['Experiment_type'])
            
            #separation_ajustments
            separation_ajustments = request.POST['separation_ajustments']
            
            #Digest
            (digest_type, sign) = Digest_type.objects.get_or_create(name=request.POST['Digest_type'])
            (digest_enzyme, sign) = Digest_enzyme.objects.get_or_create(name=request.POST['Digest_enzyme'])
            
            #SearchDatabase-Parameter
            #zdd instrument_MS: Separate value and unit
            #instrument_MS1_tol_unit
            instrument_MS1_tol_value = request.POST['instrument_MS1_tol']
            instrument_MS1_tol_unit = request.POST['instrument_MS1_tol_unit']
            instrument_MS1_tol_name = instrument_MS1_tol_value + " " + instrument_MS1_tol_unit
            #instrument_MS2_tol_unit
            instrument_MS2_tol_value = request.POST['instrument_MS2_tol']
            instrument_MS2_tol_unit = request.POST['instrument_MS2_tol_unit']
            instrument_MS2_tol_name = instrument_MS2_tol_value + " " + instrument_MS2_tol_unit
            
            (instrument_manufacturer, sign) = Instrument_manufacturer.objects.get_or_create(name=request.POST['Instrument_manufacturer'])
            instrument_name = Instrument.objects.get(name=request.POST['Instrument_name'])
            
            instrument_MS1 = Instrument_MS1.objects.get(name=request.POST['instrument_MS1'], type=instrument_name)
            (instrument_MS1_tol, sign) = Instrument_MS1_tol.objects.get_or_create(name=instrument_MS1_tol_name, type=instrument_MS1)
            #instrument_MS1_tol = instrument_MS1_tol[0]
            
            instrument_MS2 = Instrument_MS2.objects.get(name=request.POST['instrument_MS2'], type=instrument_name)
            (instrument_MS2_tol, sign) = Instrument_MS2_tol.objects.get_or_create(name=instrument_MS2_tol_name, type=instrument_MS2)
            #instrument_MS2_tol = instrument_MS2_tol[0]
            
            database = Search_database.objects.get(name=request.POST['Search_database'])
            comments_conclusions = request.POST['comments_conclusions']
            
            #repeat
            repeat = request.POST['repeat']
            #fration
            fraction = request.POST['fraction']
            
            ispecno = request.POST['ispecno']
            taxid = ''
            
            
            ######################################################################
            #add workflow by zdd
            (workflowMode, sign) = Workflow_mode.objects.get_or_create(name=request.POST['workflowMode'])
            experiment.workflowMode = workflowMode
            experimentId = experiment.id
            if experiment.workflowMode.name == "PRIDE" or experiment.workflowMode.name == "MassIVE":
                workflowMode_detail = Pride_mode.objects.all().filter(experimentId=experiment.id)[0]
                workflowMode_detail.pxdno = request.POST['pxdno']
                workflowMode_detail.prideFileList = request.POST['prideFileList']
                workflowMode_detail.save()
            
            (search_Engine, sign) = searchEngine.objects.get_or_create(name=request.POST['searchEngine'])
            experiment.searchEngine = search_Engine
            if experiment.searchEngine.name == "X!Tandem":
                #add a record into Xtandem_mode
                searchEngine_detail = Xtandem_mode.objects.all().filter(experimentId=experiment.id)[0]
                searchEngine_detail.fragmentationMethod = request.POST['fragmentationMethod']
                searchEngine_detail.cysteineProtectingGroup = request.POST['cysteineProtectingGroup']
                searchEngine_detail.protease = request.POST['protease']
                searchEngine_detail.numberOfAllowed13C = request.POST['numberOfAllowed13C']
                #workflowMode_detail.parentMassTolerance = request.POST['parentMassToleranceNumber']
                #workflowMode_detail.parentMassToleranceUnit = request.POST['parentMassToleranceUnit']
                #workflowMode_detail.ionTolerance = request.POST['ionToleranceNumber']
                #workflowMode_detail.ionToleranceUnit = request.POST['ionToleranceUnit']
                searchEngine_detail.save()
                                
            if experiment.searchEngine.name == "Mascot":
                searchEngine_detail = Mascot_mode.objects.all().filter(experimentId=experiment.id)[0]
                (missedCleavagesAllowed, sign) = Mascot_mode_missedCleavagesAllowed.objects.get_or_create(name=request.POST['missedCleavagesAllowed'])
                (mascotEnzyme, sign) = Mascot_mode_mascotEnzyme.objects.get_or_create(name=request.POST['mascotEnzyme'])
                (peptideCharge, sign) = Mascot_mode_peptideCharge.objects.get_or_create(name=request.POST['peptideCharge'])
                (precursorSearchType, sign) = Mascot_mode_precursorSearchType.objects.get_or_create(name=request.POST['precursorSearchType'])
                searchEngine_detail.missedCleavagesAllowed = missedCleavagesAllowed
                searchEngine_detail.mascotEnzyme = mascotEnzyme
                searchEngine_detail.peptideCharge = peptideCharge
                searchEngine_detail.precursorSearchType = precursorSearchType
                searchEngine_detail.save()
            ######################################################################
            
            
            ######################################################################
            #add experimentalFDR by zdd
            experimentalFDR_info = Experimentalfdr_info.objects.all().filter(experimentId=experiment.id)[0]
            experimentalFDR_level = request.POST["addexperimentFdr"]
            if "Spectrum" in experimentalFDR_level:
                experimentalFDR_info.experimentalFDR_level = "Spectrum"
                experimentalFDR_info.experimentalFDR_value = request.POST['addexperimentSpectrumFdrValue']
            elif "Peptide" in experimentalFDR_level:
                experimentalFDR_info.experimentalFDR_level = "Peptide"
                experimentalFDR_info.experimentalFDR_value = request.POST['addexperimentPeptideFdrValue']
            else:
                experimentalFDR_info.experimentalFDR_level = "Protein"
                experimentalFDR_info.experimentalFDR_value = request.POST['addexperimentProteinFdrValue']
            experimentalFDR_info.save()
            ######################################################################
            
            ######################################################################
            #add quantification method by zdd
            (quantification_method, sign) = Quantification_Methods.objects.get_or_create(name=request.POST['quantificationMethods'])
            experiment.quantificationMethod = quantification_method
            ######################################################################
    
            
            experiment.experimenter=experimenter
            experiment.date = experiment_date
            experiment.company=company
            experiment.lab=lab
            experiment.Funding=Funding
            experiment.Project=Project
            experiment.PI=PI
            experiment.SubProject=SubProject
            experiment.Subject=Subject
            experiment.Manager=Manager             
            experiment.type=experiment_type
            experiment.fraction=fraction
            experiment.repeat=repeat
            experiment.separation_ajustments=separation_ajustments
            experiment.digest_type=digest_type             
            experiment.digest_enzyme=digest_enzyme
            experiment.instrument_name=instrument_name
            experiment.instrument_manufacturer=instrument_manufacturer
            
            experiment.ms1=instrument_MS1
            experiment.ms1_details=instrument_MS1_tol
            
            experiment.ms2=instrument_MS2
            experiment.ms2_details=instrument_MS2_tol
            
            experiment.comments_conclusions=comments_conclusions
            experiment.fm_no=ispecno
            
            #common lib and customized lib
            experiment.search_database=database
            
            
            experiment.save()
            
            no = experiment.id
            exp_name = str(experiment.id)
            while len(exp_name) < 6:
                exp_name = '0' + exp_name
            exp_name = 'Exp' + exp_name
            experiment.name = exp_name
            
            #experiment.separation_methods
            
            bait = ''
            protocols = ''
            #pre_separation_methods
            experiment.pre_separation_methods = request.POST['separ_methods']
            #pre_separation_methods
            separation_method_num = int(request.POST['method_num'])
            experiment.separation = separation_method_num
            #clear experiment.separation_methods
            experiment.separation_methods.clear()
            for method_order in  range(1, separation_method_num + 1):
                separation_method = request.POST['separation_method' + str(method_order)]
                separation_source = request.POST['separation_source' + str(method_order)]
                separation_size = request.POST['separation_Size' + str(method_order)]
                separation_buffer = request.POST['separation_buffer' + str(method_order)]
                separation_others = request.POST['separation_others' + str(method_order)]
                separation_num = separation_method_num
                Sepeartion = Separation_method(
                                               name=separation_method,
                                               source=separation_source,
                                               size=separation_size,
                                               buffer=separation_buffer,
                                               others=separation_others,
                                               )
                Sepeartion.save()
                experiment_separation = Experiment_separation(experiment=experiment,
                                                              separation_method=Sepeartion,
                                                              method_order=method_order,
                                                              separation_num=separation_num
                                                              )
                experiment_separation.save()
            #clear experiment.samples
            experiment.samples.clear()
            sample_num = int(request.POST['sample_num'])
            for i in range(sample_num):
                sample = Sample.objects.get(id=request.POST['sample_no' + str(i + 1)])
                temp_sample = sample               
                experiment_sample = Experiment_sample(sample=sample,
                                                      experiment=experiment,
                                                      amount=request.POST['sample_amount' + str(i + 1)],
                                                      amount_unit=request.POST['sample_unit' + str(i + 1)],
                                                      ajustments=request.POST['sample_ajustments' + str(i + 1)]
                                                      )
                
                experiment_sample.save()
            
            #clear experiment.reagents
            experiment.reagents.clear()
            reagent_num = int(request.POST['reagent_num'])
            for i in range(reagent_num):
                reagent = Reagent.objects.get(id=request.POST['reagent_no' + str(i + 1)])
                bait = bait + str(reagent.name) + ';'
                amount = request.POST['reagent_amount' + str(i + 1)]
                amount_unit=request.POST['reagent_unit' + str(i + 1)]
                (method, sign) = Reagent_method.objects.get_or_create(name=request.POST['Reagent_method' + str(i + 1)])
                (wash_buffer, sign) = Reagent_buffer.objects.get_or_create(name=request.POST['Reagent_buffer' + str(i + 1)])
                ajustments = request.POST['reagent_ajustments' + str(i + 1)]
                experiment_reagent = Experiment_reagent(reagent=reagent,
                                                        experiment=experiment,
                                                        amount=amount,
                                                        amount_unit=amount_unit,
                                                        method=method,
                                                        wash_buffer=wash_buffer,
                                                        ajustments=ajustments
                                                        )
                experiment_reagent.save()
            
            fixedModifications = request.POST.getlist('Fixed_Modification')
            fixedModifications_old = experiment.fixed_modifications.all()
           
#             for temp in fixedModifications:
#                 (fixedModification, sign) = Fixed_Modification.objects.get_or_create(name=temp)
#                 experiment.fixed_modifications.add(fixedModification)
            
            
            for temp in fixedModifications_old:
                if temp not in fixedModifications:
                    print "delete"
                    experiment.fixed_modifications.remove(temp)
             
            for temp in fixedModifications:
                if temp not in fixedModifications_old:
                    print "add"
                    (fixedModification, sign) = Fixed_Modification.objects.get_or_create(name=temp)
                    experiment.fixed_modifications.add(fixedModification)

                    
                
            
            
            
            dynamicModifications = request.POST.getlist('Dynamic_Modification')
            dynamicModifications_old = experiment.dynamic_modifications.all()
#             for temp in dynamicModifications:
#                 if temp != '':
#                     #delete
#                     (dynamicModification, sign) = Dynamic_Modification.objects.get_or_create(name=temp)
#                     experiment.dynamic_modifications.add(dynamicModification)
            for temp in dynamicModifications_old:
                if temp not in dynamicModifications:
                    print "delete"
                    experiment.dynamic_modifications.remove(temp)
             
            for temp in dynamicModifications:
                if temp not in dynamicModifications_old:
                    print "add"
                    (dynamicModification, sign) = Dynamic_Modification.objects.get_or_create(name=temp)
                    experiment.dynamic_modifications.add(dynamicModification)
            
            #Experiment.objects.get(id=int(no)).save()
            
            #description
            cell = '-'
            organ = '-'
            tissue = '-'
            fluid = '-'
            description = ''
            sam_num=1
            for temp_sample in  experiment.samples.all().order_by('id'):
                if len(experiment.samples.all())>1:
                    description=description+'#'+str(sam_num)+':'
                    sam_num=sam_num+1
                if temp_sample.source_tissue:
                    taxid = temp_sample.source_tissue.tissueID.name
                    speci = temp_sample.source_tissue.tissueName.name
                    tissue = temp_sample.source_tissue.tissueSystem.name
                    organ = temp_sample.source_tissue.tissueOrgan.name 
                    ts = temp_sample.source_tissue
                    gene = ts.gene
                    if ts.genotype.abbrev == 'WT': 
                        gstring = ts.genotype.abbrev
                    else:
                        gstring = ''
                        genes = gene.split(';')
                        for gene in genes:
                            gstring = gstring + gene.split('|')[0] + '(' + ts.genotype.abbrev + ')' + '|' 
                            print gene
                        gstring=gstring[:-1]
                    if ts.tissueStrain.name != 'None':                    
                        description += str(ts.tissueName.abbrev) + '_' + str(ts.tissueStrain.name) + '_' + gstring + '_' + str(ts.tissueOrgan.name)
                    else:
                        description += str(ts.tissueName.abbrev) + '_' + gstring + '_' + str(ts.tissueOrgan.name)
                    if ts.tissueStructure:
                        description=description+'_'+ts.tissueStructure
                    if ts.tissueType:
                        if ts.tissueType.name == 'Tumor':
                            description = description + '(T)'
                        elif ts.tissueType.name == 'Tumor adjacent':
                            description = description + '(P)'
                        elif ts.tissueType.name == 'Normal' or  ts.tissueType.name == 'Tumor distant':
                            description = description + '(N)'
                        else:
                            description = description + '(' + ts.tissueType.name + ')'
                elif temp_sample.source_cell: 
                    taxid = temp_sample.source_cell.tissueID.name
                    try:
                        speci = temp_sample.source_cell.tissueName.name
                    except:
                        sepci = '-'
                    try:
                        cell = temp_sample.source_cell.cellName.name
                    except:
                        cell = '-'       
                    sc = temp_sample.source_cell
                    gene = sc.gene
                    if sc.genotype.abbrev == 'WT': 
                        gstring = sc.genotype.abbrev
                    else:
                        gstring = ''
                        genes = gene.split(';')
                        for gene in genes:
                            gstring = gstring + gene.split('|')[0] + '(' + sc.genotype.abbrev + ')' + '|' 
                        gstring=gstring[:-1]
                    try:
                        if (sc.cellName.abbrev):
                            abbrev=sc.cellName.abbrev
                        else:
                            abbrev=sc.cellName.name
                    except:
                        abbrev='None'
                    if sc.tissueStrain.name != 'None':
                        description += str(sc.tissueName.abbrev) + '_' + str(sc.tissueStrain.name) + '_' + gstring + '_' + str(abbrev)
                    else:
                        description += str(sc.tissueName.abbrev) + '_' + gstring + '_' + str(abbrev)
                elif temp_sample.source_fluid:
                    taxid = temp_sample.source_fluid.tissueID.name
                    speci = temp_sample.source_fluid.tissueName.name
                    fluid = temp_sample.source_fluid.fluid.name
                    sf = temp_sample.source_fluid
                    gene = sf.gene
                    if sf.genotype.abbrev == 'WT': 
                        gstring = sf.genotype.abbrev
                    else:
                        gstring = ''
                        genes = gene.split(';')
                        for gene in genes:
                            gstring = gstring + gene.split('|')[0] + '(' + sf.genotype.abbrev + ')' + '|' 
                        gstring=gstring[:-1]
                    if sf.tissueStrain.name != 'None':
                        description += str(sf.tissueName.abbrev) + '_' + str(sf.tissueStrain.name) + '_' + gstring+ '_' + str(sf.fluid.name) 
                    else:
                        description += str(sf.tissueName.abbrev) + '_' + gstring+ '_' + str(sf.fluid.name)
                elif temp_sample.source_others:
                    taxid = ''
                    speci = '-'
                    tissue = '-'
                    
                rx_treatment_string = ''
                for rx in temp_sample.treatments.all().order_by('id'):
                    if rx.geneTaxon:
                        rx_treatment_string = rx_treatment_string + rx.geneSymbol+'('+str(rx.rx_treatments_detail.abbrev)+')'
                    else:
                        if rx.rx_treatments_detail.abbrev:
                            rx_treatment_string = rx_treatment_string + str(rx.rx_treatments_detail.abbrev) + '_'
                        else:
                            rx_treatment_string = rx_treatment_string + str(rx.rx_treatments_detail.name) + '_'
                        if rx.rx_unit_deatil:
                            if rx.rx_unit_deatil.name != 'None':
                                rx_treatment_string = rx_treatment_string + str(rx.rx_amount)  + str(rx.rx_unit_deatil.name)
                                
                    if rx_treatment_string[-1]=='_':
                        rx_treatment_string=rx_treatment_string[:-1]
                    rx_treatment_string = rx_treatment_string + '_'+str(rx.rx_duration) + str(rx.rx_duration_time)
                
                    rx_treatment_string = rx_treatment_string + '; '
                    
                for ubi in  temp_sample.ubi_subcells.all().order_by('id'):
                    rx_treatment_string=rx_treatment_string+ubi.abbrev+'|'
                rx_treatment_string=rx_treatment_string[:-1]
                sample_amount=Experiment_sample.objects.filter(experiment=experiment).filter(sample=temp_sample)[0]
                if sample_amount.amount_unit!='None':
                    rx_treatment_string=rx_treatment_string+'_'+sample_amount.amount+sample_amount.amount_unit
                else:
                    rx_treatment_string=rx_treatment_string+'_'+sample_amount.amount
                description = description + '; ' + rx_treatment_string + '; '
            description=description.strip()[:-1]
            experiment.taxid = taxid
            experiment.save()
            if bait == '':
                bait = 'NA'
            
            #experiment = Experiment.objects.get(id=int(no))
            gardenerExp = gard_experiment.objects.get(name=exp_name);           
            gardenerExp.bait=bait
            gardenerExp.type=experiment_type.name
            gardenerExp.description=description
            gardenerExp.species=speci
            gardenerExp.taxid=taxid
            gardenerExp.cell_type=cell
            gardenerExp.tissue=tissue
            gardenerExp.organ=organ
            gardenerExp.fluid=fluid
            gardenerExp.num_fraction=fraction
            gardenerExp.num_repeat=repeat
            #gardenerExp.num_spectrum=0
            #gardenerExp.num_peptide=0
            #gardenerExp.num_isoform=0
            #gardenerExp.num_gene=0
            gardenerExp.instrument=instrument_name.name
            gardenerExp.protocol=''
            gardenerExp.lab=lab
            gardenerExp.operator=experimenter
            gardenerExp.experiment_date=experiment_date
            gardenerExp.index_date=datetime.date.today()
            gardenerExp.update_date=datetime.date.today()
            #gardenerExp.stage=-1
            #gardenerExp.started=0
            #gardenerExp.is_public=0
            #gardenerExp.is_deleted=0
            #gardenerExp.priority = 0
            #gardenerExp.file_source = 'nas'
            gardenerExp.save()
            
            experiment.description = description
            experiment.save()    
            success = True
            msg = "Experiment Added"
            data = {'success': success, 'msg':exp_name}
            result = json.dumps(data)
            return HttpResponse(result)     
        else:
            return HttpResponse('wtf')
    else:
        print "false"
        data = {'success': False, 'data':"Error"}
        result = json.dumps(data)
        return HttpResponse(result)
                  
            
            
            
            
            
            
            
            
            
            
            
               



#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# @login_required(login_url="/login/")
'''
def experiment_edit_save(request):
    if request.method == 'POST':
        no = request.POST['experiment_no']
        experiment = Experiment.objects.get(id=int(no))
        if experiment.experimenter.id == request.user:
            (project, sign) = Project.objects.get_or_create(name=request.POST['Project'])
            (month, day, year) = request.POST['date'].split('/')
            experiment_date = date(int(year), int(month), int(day))
            general_user = User.objects.get(username=request.user.username)
            general_experimenter = All_Experimenter.objects.get(id=general_user)
            location = request.POST['location']
            (experiment_type, sign) = Experiment_type.objects.get_or_create(name=request.POST['Experiment_type'])
            separation_user = User.objects.get(username=request.POST['separation_experimenter'])
            separation_experimenter = All_Experimenter.objects.get(id=separation_user)
            separation_ajustments = request.POST['separation_ajustments']

            digest_user = User.objects.get(username=request.POST['digest_experimenter'])
            digest_experimenter = All_Experimenter.objects.get(id=digest_user)
            (digest_type, sign) = Digest_type.objects.get_or_create(name=request.POST['Digest_type'])
            (digest_enzyme, sign) = Digest_enzyme.objects.get_or_create(name=request.POST['Digest_enzyme'])

            (instrument_administrator, sign) = Instrument_administrator.objects.get_or_create(name=request.POST['Instrument_administrator'])
            (instrument_manufacturer, sign) = Instrument_manufacturer.objects.get_or_create(name=request.POST['Instrument_manufacturer'])
            instrument_name = request.POST['instrument_name']
            instrument_type = request.POST['instrument_type']

            comments_conclusions = request.POST['comments_conclusions']
            description = request.POST['description']

            experiment.date = experiment_date
            experiment.experimenter = general_experimenter
            experiment.project = project
            experiment.separation_experimenter = separation_experimenter
            experiment.separation_ajustments = separation_ajustments
            experiment.digest_type = digest_type
            experiment.digest_enzyme = digest_enzyme
            experiment.digest_experimenter = digest_experimenter
            experiment.instrument_name = instrument_name
            experiment.instrument_type = instrument_type
            experiment.instrument_manufacturer = instrument_manufacturer
            experiment.instrument_administrator = instrument_administrator
            experiment.comments_conclusions = comments_conclusions
            experiment.description = description

            Experiment_separation.objects.filter(experiment=experiment).delete()
            separation_method_num = int(request.POST['method_num'])
            for method_order in  range(1, separation_method_num + 1):
                (separation_method, sign) = Separation_method.objects.get_or_create(name=request.POST['Separation_method' + str(method_order)])
                separation_num = request.POST['separation_num' + str(method_order)]
                experiment_separation = Experiment_separation(experiment=experiment,
                        separation_method=separation_method,
                        method_order=method_order,
                        separation_num=separation_num)
                experiment_separation.save()

            Experiment_sample.objects.filter(experiment=experiment).delete()
            sample_num = int(request.POST['sample_num'])
            for i in range(sample_num):
                sample = Sample.objects.get(id=request.POST['sample_no' + str(i + 1)])
                experiment_sample = Experiment_sample(sample=sample,
                                        experiment=experiment,
                                        amount=request.POST['sample_amount' + str(i + 1)],
                                        ajustments=request.POST['sample_ajustments' + str(i + 1)])
                experiment_sample.save()

            Experiment_reagent.objects.filter(experiment=experiment).delete()
            reagent_num = int(request.POST['reagent_num'])
            for i in range(reagent_num):
                reagent = Reagent.objects.get(id=request.POST['reagent_no' + str(i + 1)])
                amount = request.POST['reagent_amount' + str(i + 1)]
                (method, sign) = Reagent_method.objects.get_or_create(name=request.POST['Reagent_method' + str(i + 1)])
                (wash_buffer, sign) = Reagent_buffer.objects.get_or_create(name=request.POST['Reagent_buffer' + str(i + 1)])
                ajustments = request.POST['reagent_ajustments' + str(i + 1)]
                experiment_reagent = Experiment_reagent(reagent=reagent,
                                        experiment=experiment,
                                        amount=amount,
                                        method=method,
                                        wash_buffer=wash_buffer,
                                        ajustments=ajustments)
                experiment_reagent.save()
            experiment.save()
            return HttpResponseRedirect('/experiments/experiment/')
        else:
            raise Http404()
    else:
        raise Http404()
'''

# @login_required(login_url="/login/")
def reagent_edit_delete(request):
    data = {}
    error = ''  # record error information
    success = 'False'
    no = request.GET['no']
    reagent = Reagent.objects.get(id=int(no))
    if reagent.experimenter.id == request.user or request.user.is_superuser:
        experiment_reagents = Experiment_reagent.objects.filter(reagent=reagent)
        if len(experiment_reagents) != 0:
            error = 'There are experiments used this reagent, you cannot delete it now!'
        else:
            if reagent.type == 'Antigen':
                antigen = reagent.antigen
                antigen.delete()
            elif reagent.type == 'Protein':
                domain_info = reagent.domain_info
                domain_info.delete()
            elif reagent.type == 'DNA':
                dna_info = reagent.dna_info
                dna_info.delete()
            elif reagent.type == 'other':
                remarks_info = reagent.remarks_info
                remarks_info.delete()
            reagent.delete()
            success = "True"
    else:
        error = 'Sorry, You have no permission to do this!'
    data = {'success': success, 'error':error}
    result = json.dumps(data)
    return HttpResponse(result)

# @login_required(login_url="/login/")
def sample_edit_delete(request):
    data = {}
    error = ''
    success = 'False'
    no = request.GET['no']
    sample = Sample.objects.get(id=int(no))
    if sample.experimenter.id == request.user or request.user.is_superuser:
        experiment_samples = Experiment_sample.objects.filter(sample=sample)
        if len(experiment_samples) != 0:
            error = 'There are experiments used this sample,you cannot delete it now!'
        else:
            source_tissue = sample.source_tissue
            source_cell = sample.source_cell
            if source_tissue:
                source_tissue.delete()
            if source_cell:
                source_cell.delete()
            sample.delete()
            success = 'True'
    else:
        error = "Sorry, you have no permssions to do this!"
    data = {'success': success, 'error':error}
    result = json.dumps(data)
    return HttpResponse(result)

# @login_required(login_url="/login/")
def experiment_edit_delete(request):
    data = {}
    error = ''  # record error information
    success = 'False'
    no = request.GET['no']
    username = str(request.user)
    experiment = Experiment.objects.get(id=int(no))
    e_name = experiment.name
    # if experiment.experimenter.id == request.user:
    if 'qiunq' == username:
        experiment_samples = Experiment_sample.objects.filter(experiment=experiment)
        experiment_samples.delete()
        experiment_reagents = Experiment_reagent.objects.filter(experiment=experiment)
        experiment_reagents.delete()
        experiment_separations = Experiment_separation.objects.filter(experiment=experiment)
        experiment_separations.delete()
        experiment.delete()
        ''' change to deleted status '''
        try:
            gard_exp = gard_experiment.objects.get(name=e_name)
            gard_exp.is_deleted = 1
            gard_exp.save()
        except:
            pass
        success = 'True'
        error = 'User %s deleted %s' % (username, no)
    else:
        error = 'Sorry, User \"%s\" has no permission to do this!' % username
    data = {'success': success, 'error':error}
    result = json.dumps(data)
    return HttpResponse(result)

def ContainNoStore(request):
    try:
        id = request.GET['id']
    except:
        id = ''
    data = {}
    lab = Container_No.objects.all()
    experimenters = lab.filter(Container__name=id)
    experimenters_name = []
    for experimenter in experimenters:
        user_dict = {}
        try:
            user_dict['ContainNo'] = experimenter.name
        except:
            continue
        experimenters_name.append(user_dict)
    data['ContainNo'] = experimenters_name
    result = json.dumps(data)
    return HttpResponse(result)
def ContainBasketStore(request):
    try:
        id = request.GET['id']
    except:
        id = ''
    data = {}
    lab = Container_Basket.objects.all()
    experimenters = lab.filter(Container__name=id)
    experimenters_name = []
    for experimenter in experimenters:
        user_dict = {}
        try:
            user_dict['ContainBasket'] = experimenter.name
        except:
            continue
        experimenters_name.append(user_dict)
    data['ContainBasket'] = experimenters_name
    result = json.dumps(data)
    return HttpResponse(result)
def ContainLayerStore(request):
    try:
        id = request.GET['id']
    except:
        id = ''
    data = {}
    lab = Container_Layer.objects.all()
    experimenters = lab.filter(Container__name=id)
    experimenters_name = []
    for experimenter in experimenters:
        user_dict = {}
        try:
            user_dict['ContainLayer'] = experimenter.name
        except:
            continue
        experimenters_name.append(user_dict)
    data['ContainLayer'] = experimenters_name
    result = json.dumps(data)
    return HttpResponse(result)


def correct(id):
    experiment = Experiment.objects.get(id=id)
    description = ''
    # print exp
    # exp.comments_conclusions = exp.description + exp.comments_conclusions
    if len(experiment.samples.all()) != 0:
        for temp_sample in experiment.samples.all().order_by('id'):
            if len(experiment.samples.all())>1:
                description=description+'#'+str(sam_num)+':'
                sam_num=sam_num+1
            if temp_sample.source_tissue:
                taxid = temp_sample.source_tissue.tissueID.name
                speci = temp_sample.source_tissue.tissueName.name
                tissue = temp_sample.source_tissue.tissueSystem.name
                organ = temp_sample.source_tissue.tissueOrgan.name 
                ts = temp_sample.source_tissue
                gene = ts.gene
                if ts.genotype.abbrev == 'WT': 
                    gstring = ts.genotype.abbrev
                else:
                    gstring = ''
                    genes = gene.split(';')
                    for gene in genes:
                        gstring = gstring + gene.split('|')[0] + '(' + ts.genotype.abbrev + ')' + '|' 
                        print gene
                    gstring=gstring[:-1]
                if ts.tissueStrain.name != 'None':                    
                    description += str(ts.tissueName.abbrev) + '_' + str(ts.tissueStrain.name) + '_' + gstring + '_' + str(ts.tissueOrgan.name)
                else:
                    description += str(ts.tissueName.abbrev) + '_' + gstring + '_' + str(ts.tissueOrgan.name)
                if ts.tissueStructure:
                    description=description+'_'+ts.tissueStructure
                if ts.tissueType:
                    if ts.tissueType.name == 'Tumor':
                        description = description + '(T)'
                    elif ts.tissueType.name == 'Tumor adjacent':
                        description = description + '(P)'
                    elif ts.tissueType.name == 'Normal' or  ts.tissueType.name == 'Tumor distant':
                        description = description + '(N)'
                    else:
                        description = description + '(' + ts.tissueType.name + ')'
            elif temp_sample.source_cell:
                taxid = temp_sample.source_cell.tissueID.name
                try:
                    speci = temp_sample.source_cell.tissueName.name
                except:
                    sepci = '-'
                try:
                    cell = temp_sample.source_cell.cellName.name
                except:
                    cell = '-'
                sc = temp_sample.source_cell
                gene = sc.gene
                if sc.genotype.abbrev == 'WT': 
                    gstring = sc.genotype.abbrev
                else:
                    gstring = ''
                    genes = gene.split(';')
                    for gene in genes:
                        gstring = gstring + gene.split('|')[0] + '(' + sc.genotype.abbrev + ')' + '|' 
                        
                    gstring=gstring[:-1]
                try:
                    if (sc.cellName.abbrev):
                        abbrev=sc.cellName.abbrev
                    else:
                        abbrev=sc.cellName.name
                except:
                        abbrev='None'
                if sc.tissueStrain.name != 'None':
                    description += str(sc.tissueName.abbrev) + '_' + str(sc.tissueStrain.name) + '_' + gstring + '_' + str(abbrev)
                else:
                    description += str(sc.tissueName.abbrev) + '_' + gstring + '_' + str(abbrev)
            elif temp_sample.source_fluid:
                taxid = temp_sample.source_fluid.tissueID.name
                speci = temp_sample.source_fluid.tissueName.name
                fluid = temp_sample.source_fluid.fluid.name
                sf = temp_sample.source_fluid
                gene = sf.gene
                if sf.genotype.abbrev == 'WT': 
                    gstring = sf.genotype.abbrev
                else:
                    gstring = ''
                    genes = gene.split(';')
                    for gene in genes:
                        gstring = gstring + gene.split('|')[0] + '(' + sf.genotype.abbrev + ')' + '|' 
                    gstring=gstring[:-1]
                if sf.tissueStrain.name != 'None':
                    description += str(sf.tissueName.abbrev) + '_' + str(sf.tissueStrain.name) + '_' + gstring+ '_' + str(sf.fluid.name) 
                else:
                    description += str(sf.tissueName.abbrev) + '_' + gstring+ '_' + str(sf.fluid.name) 
            elif temp_sample.source_others:
                taxid = ''
                speci = '-'
                tissue = '-'
            
            rx_treatment_string = ''
            for rx in temp_sample.treatments.all().order_by('id'):
                # rx_treatment_string=rx_treatment_string+str(rx.rx_treatments.name) + '|' + str(rx.rx_treatments_detail.name)
                if rx.geneTaxon:
                    rx_treatment_string = rx_treatment_string + rx.geneSymbol+'('+str(rx.rx_treatments_detail.abbrev)+')'
                else:
                    if rx.rx_treatments_detail.abbrev:
                        rx_treatment_string = rx_treatment_string + str(rx.rx_treatments_detail.abbrev) + '_'
                    else:
                        rx_treatment_string = rx_treatment_string + str(rx.rx_treatments_detail.name) + '_'
                    if rx.rx_unit_deatil:
                        if rx.rx_unit_deatil.name != 'None':
                            rx_treatment_string = rx_treatment_string + str(rx.rx_amount)  + str(rx.rx_unit_deatil.name)
                if rx_treatment_string[-1]=='_':
                    rx_treatment_string=rx_treatment_string[:-1]
                rx_treatment_string = rx_treatment_string + '_'+str(rx.rx_duration) + str(rx.rx_duration_time)
                
                rx_treatment_string = rx_treatment_string + '; '
            #=======================================================================
            # if (temp_sample.ubi_subcells.all() != 0):
            #     description = description + '-' + temp_sample.ubi_subcells.all()[0].abbrev
            #=======================================================================
            #=======================================================================
            # if temp_sample.rx_treatments.name != 'None':
            #     description = description + ';' + temp_sample.rx_treatments_detail.name
            # if temp_sample.rx_unit_deatil:
            #     description = description + '-' + temp_sample.rx_amount + temp_sample.rx_unit_deatil.name
            # if temp_sample.rx_duration_time:
            #     description = description + '-' + str(temp_sample.rx_duration) + str(temp_sample.rx_duration_time)        
            #=======================================================================
            for ubi in  temp_sample.ubi_subcells.all().order_by('id'):
                rx_treatment_string=rx_treatment_string+ubi.abbrev+'|'
            rx_treatment_string=rx_treatment_string[:-1]
            sample_amount=Experiment_sample.objects.filter(experiment=experiment).filter(sample=temp_sample)[0]
            rx_treatment_string=rx_treatment_string+'_'+sample_amount.amount+sample_amount.amount_unit
            description = description + '; ' + rx_treatment_string + '; '
        description=description.strip()[:-1]
    experiment.description = description
    experiment.save()
    gar_exp = gard_experiment.objects.get(name=experiment.name)
    gar_exp.description = description
    gar_exp.save()

def getPrideFileList(request):
    if request.method == 'GET':
        pxdNo = request.GET['pxdNo']
        address = ''
        url = 'http://proteomecentral.proteomexchange.org/cgi/GetDataset?ID=%s&outputMode=XML&test=no' % str(
            pxdNo)
        print url
        tree = etree.parse(url)
        root = tree.getroot()
        # print root.tag, root.attrib
        # for child in root:
            # print child.tag, child.attrib
        hostingRepository = root.find('DatasetSummary').get('hostingRepository')
        # print hostingRepository
        if hostingRepository == 'PRIDE':
            DatasetFileList = root.find('DatasetFileList')
            for DatasetFile in DatasetFileList.findall('DatasetFile'):
                names = DatasetFile.get('name')
                addr = DatasetFile.find('cvParam').get('value')
                address += names + ',' + addr + ';'
        elif hostingRepository == 'MassIVE':
            FullDatasetLinkList = root.find('FullDatasetLinkList')
            for DatasetFile in FullDatasetLinkList.findall('FullDatasetLink'):
                if DatasetFile.find('cvParam').get('cvRef') == 'PRIDE':
                    ftpAddress = DatasetFile.find('cvParam').get('value')
                    print ftpAddress
                    o = urlparse(ftpAddress)
    
                    ftp = FTP(o.netloc)
                    ftp.login()
                    ftp.cwd(o.path)
                    ftp.cwd('raw')
                    listing = []
                    ftp.retrlines('LIST', listing.append)
                    listing = [pp.split(None, 8)[-1].lstrip() for pp in listing]
                    # print listing
                    for files in listing:
                        address += files + ',' + ftpAddress + '/raw/' + files + ';'
        address = address.strip(';')
        return HttpResponse(address)


def fasta_upload(request):
    customFastaLibrary = "/usr/local/firmiana/leafy/experiments/customFastaLibrary"
    if request.method == 'POST':
        addFastaFlag = False
        success = False
        ######################################################################
        #Custom_FastaLib_withTimeStamp
        #upload customized fasta file
        #experimentId = no
        upload_timestamp = request.POST['upload_timestamp']
        upload_species = request.POST['upload_species']
        upload_datasource = request.POST['upload_datasource']
        
        upload_date = request.POST['upload_date']
        (month, day, year) = upload_date.split('/')
        upload_date = date(int(year), int(month), int(day))
        #upload_file = request.POST['upload_file']
        upload_user = request.user.username
        #print upload_user
        fastaFileURL = request.FILES['upload_file']
        file = fastaFileURL.read()
        
        #validate file name in Custom_FastaLib_withTimeStamp
        #validate folder
        fastaLibFolder = upload_user
        fastaLibPath_parent = os.path.join(customFastaLibrary, fastaLibFolder)
        if not os.path.exists(fastaLibPath_parent):
            os.mkdir(fastaLibPath_parent)
            os.chmod(fastaLibPath_parent, 0777)
        #validate filename
        fastaLibName = upload_species + "_" + upload_datasource + "_" + year + month + day
        fastaLibName_suffix = fastaLibName + ".fasta"
        fastaLibPath = os.path.join(fastaLibPath_parent, fastaLibName_suffix)
        if not os.path.isfile(fastaLibPath):
            os.mknod(fastaLibPath)
#         else:#cover
#             success = False
#             msg = "The libary has existed the file wiht the same name, please confirm it or rename it!"
#             data = {'success': success, 'msg':msg, "fastaLibName":fastaLibName}
#             result = json.dumps(data)
#             return HttpResponse(result)
        #write file into server
        with open(fastaLibPath, "w") as f:
            os.chmod(fastaLibPath, 0777)
            f.write(file)
            addFastaFlag = True
            ################################################# 
            #once uploaded successfully, send a email to Admin
            #
            #
            #
            #
            #
            #
            #################################################  
        #print ssss
        #####################write Custom_FastaLib_withTimeStamp###############################
        if addFastaFlag:
            newFastaLib = Custom_FastaLib_withTimeStamp(
                            timeStamp = upload_timestamp,
                            experimentId = 0,
                            fastaLibName = fastaLibName,
                            upload_species = upload_species,
                            upload_datasource = upload_datasource,
                            upload_date = upload_date,
                            upload_file = fastaLibPath,
                            upload_user = upload_user
                            #validated = 
                        )
            newFastaLib.save()
            success = True
            
        #####################write Custom_FastaLib_withTimeStamp###############################
        
        #Search_database.objects.filter()
        if success:
            (newSearchDatabase, sign) = Search_database.objects.get_or_create(name=fastaLibName, validated=True, owner=upload_user)
            newSearchDatabase.save()
            #Search_database.objects.filter()
        
        #print sssss
        ######################################################################
        if success:
            msg = "Customized database has been added!"
        else:
            msg = "Customized database was added unsuccessfully!"
        data = {'success': success, 'msg':msg, "fastaLibName":fastaLibName}
        result = json.dumps(data)
        return HttpResponse(result)
        
        
        #return HttpResponse('UPLOAD OK')
    
    
def add_new_modifications(request):
    success = False
    experimentId = 0
    adder = request.user.username
    if request.method == 'POST':
        
        new_modi_title = request.POST['new_modi_title']
        new_modi_fullname = request.POST['new_modi_fullname']
        new_modi_composition = request.POST['new_modi_composition']
        new_modi_specificity = request.POST['new_modi_specificity'] #new_modi_specificity_site,new_modi_specificity_position,new_modi_classification
        added_time = request.POST['new_modi_addtime'] #15/07/2016
        #added_time = datetime.datetime.now().strftime("%m/%d/%y")
        (day, month, year) = added_time.split('/')
        added_time = date(int(year), int(month), int(day))
        timeStamp = request.POST['upload_timestamp']
        
        #add a new record to Customized_Modifications
        (custom_modifications, custom_modifications_sign) = Customized_Modifications.objects.get_or_create(
                                                            experimentId = experimentId,
                                                            adder = adder,
                                                            new_modi_title = new_modi_title,
                                                            new_modi_fullname = new_modi_fullname,
                                                            new_modi_composition = new_modi_composition,
                                                            new_modi_specificity = new_modi_specificity,
                                                            added_time = added_time,
                                                            timeStamp = timeStamp
                                                        )
        
        #custom_modifications_sign = False : found
        #custom_modifications_sign = True : not found, create
        if custom_modifications_sign:
            #add a new record to     Fixed_Modification
            (new_Fixed_Modification, sign) = Fixed_Modification.objects.get_or_create(name=new_modi_title, validated=True, owner=adder)
            
            #add a new record to Dynamic_Modification
            (new_Dynamic_Modification, sign) = Dynamic_Modification.objects.get_or_create(name=new_modi_title, validated=True, owner=adder)
            success = True
    
    if success:
        msg = "Customized modification has been added!"
    else:
        msg = "Customized modification may have been added!!"
    data = {'success': success, 'msg':msg, "new_modi_title":new_modi_title}
    result = json.dumps(data)
    return HttpResponse(result)
    
    
#parent account    
def manageChildAccount(request):
    '''
    The function is used for managing sub-account, including adding, deleting, 
    activate, freeze a sub-account and updating the shared experiments from
    parent account that the child can view.
    Parameters: 
    Add: action, childName, childPassword, annotation, sharedExp
    Delete: action, childName
    Activate: action, childName
    Freeze: action, childName
    Update shared experiments: action, childName, sharedExp
    '''
#     username = request.COOKIES['username']
#     user = User.objects.all().filter(username=username)
#     if user:
#         user = user[0]
#         userId = user.id
#     else:
#         userId = ""
    userId = request.user.id
    parentId = userId
    action = request.GET['action']
    if 'childName' in request.GET:
        childName = request.GET['childName']
        childNameFlag = True
    else:
        childName = ""
        childNameFlag = False
    
    if 'childPassword' in request.GET:
        childPassword = request.GET['childPassword']
        childPasswordFlag = True
    else:
        childPassword = ""
        childPasswordFlag = False

    if 'annotation' in request.GET:
        annotation = request.GET['annotation']
        annotationFlag = True
    else:
        annotation = ""
        annotationFlag = False
        
    if 'sharedExp' in request.GET:
        sharedExp = request.GET['sharedExp']
        sharedExpFlag = True
    else:
        sharedExp = ""
        sharedExpFlag = False
    
    
    if isParentAccount(userId): # validate parent account
        '''
        Add a new sub-account
        Parameters: childName, password, annotation, sharedExp
        '''
        passParameterRight = False
        if action=="add": 
            if childNameFlag and childPasswordFlag and annotationFlag and sharedExpFlag:
                passParameterRight = True
                if not childHasExistedByName(childName): # validate sub-account
                    try:
                        username = childName                        
                        childUser = addChildAccount(username, childPassword, annotation) # register a new sub-account
                        parentChildAssociationId = addParentAndChildAssocitions(parentId, childUser) # connect child to parent 
                        addSharedExpFlag = addChildUserSharedExp(childName, sharedExp) # connect child to shared experiments from parent
                        success = 1
                        prompt = 'Add a sub-account successfully!'
                        result = promptJson(success, prompt)
                        return HttpResponse(result)
                    except:
                        success = 0
                        prompt = 'The add-action has an exception, please contact administrator!'
                        result = promptJson(success, prompt)
                        return HttpResponse(result)
                else:
                    success = 0
                    prompt = 'Sorry, child user name has been used!'
                    result = promptJson(success, prompt)
                    return HttpResponse(result)
            else:
                success = 0
                prompt = 'Sub-account Name/Sub-account password/annotation/shared experiments can not be null.'
                result = promptJson(success, prompt)
                return HttpResponse(result)

        '''
        Delete a sub-account
        Parameter: childName
        '''
        if action=="delete" and childNameFlag:
            passParameterRight = True
            if childHasExistedByName(childName): # validate sub-account
                try:
                    deleteFlag = deleteChildAccount(parentId, childName)
                    if deleteFlag:
                        success = 1
                        prompt = 'Delete a sub-account successfully!'
                        result = promptJson(success, prompt)
                        return HttpResponse(result)
                    else:
                        success = 0
                        prompt = 'Delete a sub-account abortively!'
                        result = promptJson(success, prompt)
                        return HttpResponse(result)
                except:
                    success = 0
                    prompt = 'The delete-action has an exception, please contact administrator!'
                    result = promptJson(success, prompt)
                    return HttpResponse(result)
            else:
                success = 0
                prompt = 'Sorry, sub-user name does not exist!'
                result = promptJson(success, prompt)
                return HttpResponse(result)
        
        '''
        Activate a sub-account
        Parameter: childName
        '''
        if action=="activate":
            passParameterRight = True
            try:
                activeFlag = activateChildAccount(childName)
                if activeFlag:
                    success = 1
                    prompt = 'Activate a sub-account successfully!'
                    result = promptJson(success, prompt)
                    return HttpResponse(result)
                else:
                    success = 0
                    prompt = 'Activate a sub-account abortively!'
                    result = promptJson(success, prompt)
                    return HttpResponse(result)
            except:
                success = 0
                prompt = 'The activate-action has an exception, please contact administrator!'
                result = promptJson(success, prompt)
                return HttpResponse(result)
        
        '''
        Freeze a sub-account
        Parameters: childName
        '''
        if action=="freeze" and childNameFlag:
            passParameterRight = True
            #childName = "Zhan Dongdong"
            try:
                freezeFlag = freezeChildAccount(childName)
                if freezeFlag:
                    success = 1
                    prompt = 'Freeze a sub-account successfully!'
                    result = promptJson(success, prompt)
                    return HttpResponse(result)
                else:
                    success = 0
                    prompt = 'Freeze a sub-account abortively!'
                    result = promptJson(success, prompt)
                    return HttpResponse(result)
            except:
                success = 0
                prompt = 'The freeze-action has an exception, please contact administrator!'
                result = promptJson(success,prompt)
                return HttpResponse(result)
        
        '''
        update shared experiments from parent
        Parameters: childName, sharedExp
        '''
        if action=="update" and childNameFlag and sharedExpFlag:
            passParameterRight = True
            try:
                #shareExp = request.POST['shareExp']
                
                updateSharedExpFlag = updateChildAccountSharedExp(childName, sharedExp)
                if updateSharedExpFlag:
                    success = 1
                    prompt = 'Update shared experiments of the sub-account successfully!'
                    result = promptJson(success, prompt)
                    return HttpResponse(result)
                else:
                    success = 0
                    prompt = 'Update shared experiments of the sub-account abortively!'
                    result = promptJson(success, prompt)
                    return HttpResponse(result)
            except:
                success = 0
                prompt = 'The update-shared-experiemnts-action has an exception, please contact administrator!'
                result = promptJson(success,prompt)
                return HttpResponse(result)
        '''
        Validate whether that parameter passing is right.
        '''    
        if not passParameterRight:
            success = 0
            prompt = 'Sorry, the parameter passing is wrong!'
            result = promptJson(success,prompt)
            return HttpResponse(result)  
    else:
        success = 0
        prompt = 'Sorry, you are not a parent user and have no permission to do this operation!'
        result = promptJson(success,prompt)
        return HttpResponse(result)  


def getAllChildAccountInfo(request):
    '''
    The function is used for achiving information all sub-accounts whose belongs to the current parent.
    '''
#     username = request.COOKIES['username']
#     user = User.objects.all().filter(username=username)
#     #user = request.user    
#     if user:
#         user = user[0]
#         userId = user.id
#     else:
#         userId = -1
    userId = request.user.id
    parentFlag = isParentAccount(userId)
    if parentFlag:
        parentId = userId
        result = showAllChildAccountInfo(parentId)
    else:
        success = 0 
        msg = "You have no permission."
        data = {}
        data['success'] = success
        data['msg'] = msg
        result = json.dumps(data)
    return HttpResponse(result)

def getVisibleExpListByUserId(request):
    '''
    The function is used for viewing experiments whose access is granted to the current user.
    '''
    #userId = request.user
#     username = request.COOKIES['username']
#     user = User.objects.all().filter(username=username)
#     if user:
#         user = user[0]
#         userId = user.id
#     else:
#         userId = ""
    
    userId = request.user.id
    userFlag = isValidatedUser(userId)
    if userFlag:
        result = showExperiments_ViewRawFiles(userId)
        return HttpResponse(result)
    else:
        success = 0 
        msg = "You have no permission."
        data = {}
        data['success'] = success
        data['msg'] = msg
        result = json.dumps(data)
        return HttpResponse(result)
    
def getRawFileListByExpName(request):
    '''
    The function is used for getting raw files list of a specific experiemnt.
    Parameter: expName
    '''
#     username = request.COOKIES['username']
#     user = User.objects.all().filter(username=username)
#     if user:
#         user = user[0]
#         userId = user.id
#     else:
#         userId = ""
    
    userId = request.user.id
    userFlag = isValidatedUser(userId)
    if userFlag:
        expName = request.GET['expName']
        result = showRawFileListByExpName(expName)
        return HttpResponse(result)
    else:
        success = 0 
        msg = "You have no permission."
        data = {}
        data['success'] = success
        data['msg'] = msg
        result = json.dumps(data)
        return HttpResponse(result)

def downloadRawFileByExpNameAndFileName(request):
    '''
    The function is used for download a specific raw file.
    Parameter: expName, fileName
    '''
#     username = request.COOKIES['username']
#     user = User.objects.all().filter(username=username)
#     if user:
#         user = user[0]
#         userId = user.id
#     else:
#         userId = ""
    userId = request.user.id
    userFlag = isValidatedUser(userId)
    if not userFlag:
        success = 0 
        msg = "You have no permission."
        data = {}
        data['success'] = success
        data['msg'] = msg
        result = json.dumps(data)
        return HttpResponse(result)
    
    expName = request.GET['expName']
    fileName = request.GET['fileName']
    file_abs_path = showAbsPath_Exp_RawFile(expName, fileName)
    
    if file_abs_path == "Not Found":
        success = 0
        prompt = 'The file is not found!'
        result = promptJson(success, prompt)
        return HttpResponse(result)
    else:
        def file_iterator(file_name, chunk_size=512):
            with open(file_name) as f:
                while True:
                    c = f.read(chunk_size)
                    if c:
                        yield c
                    else:
                        break
        the_file_name = file_abs_path
        response = StreamingHttpResponse(file_iterator(the_file_name))
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="{0}"'.format(fileName)
        return response

    
def gardener_publicExperiments(request):
    userId = request.user.id
    publicedExp = request.GET['publicedExp']
    result = publicExperiments(userId, publicedExp)
    return HttpResponse(result)
    
    
    
    
    
    
    