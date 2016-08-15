import math
import json
import datetime
import csv
import os
import zipfile
import tempfile
import numpy as np
from numpy.lib import recfunctions as rfn
import numpy

from datetime import timedelta

import random
import time
from django.core.servers.basehttp import FileWrapper
from django.db import connection
from django.db.models import Q
from django.template import RequestContext
from django.shortcuts import render_to_response
# from django.http import HttpResponse
from gardener.models import *
import experiments.models
from django.core.serializers.json import DjangoJSONEncoder
import commands
import sys
import re
from django.http import HttpResponse
from numpy import array, repeat, concatenate, ones, zeros, arange, reshape, put, add, dot, take, float32
from numpy.linalg import pinv
from scipy.signal.signaltools import lfilter
from django.shortcuts import render
import multiprocessing
from multiprocessing import Process, Manager, Pool
from rpy2 import robjects as ro
from rpy2.robjects.packages import importr
from django.contrib.auth.decorators import login_required
from django.conf import settings
from qc import my_QC
from cal_area import calcAreas
import pathway
import genome
import signif
from operator import attrgetter
import newfuncTest
# standarlib by Garfiled
import firmianaLib
tmpdir = pathway.tmpdir


#ms_dir = '/usr/local/firmiana/galaxy-dist/database/files/ms_peak/'
ms_dir = '/usr/local/firmiana/NFS_89/ms_peak/'
quant_dir = '/usr/local/firmiana/data/QuantTable/'


NEW = 'new'
RUNNING = 'running'
DONE = 'done'
ERROR = 'error'
''' When httpd restart, all running jobs are killed  '''
for runningJob in XsearchTable.objects.filter(status=RUNNING):
    runningJob.status = ERROR
    runningJob.save()


@login_required(login_url=settings.LOGIN_PAGE)
def showdatabase_data(request):
    ''' Simple Authority '''
    lab = experiments.models.User_Laboratory.objects.filter(user=request.user)
    lab = lab[0].lab.name if lab.count() else ''

    if lab == 'Demo Lab':
        experiment_list = Experiment.objects.filter(
            is_public=1).filter(is_deleted=0)
    elif request.user.is_superuser:
        experiment_list = Experiment.objects.filter(is_deleted=0)
    else:
        experiment_list = Experiment.objects.filter(
            lab=lab).filter(is_deleted=0)
        Extra_Exp = Share_Exp.objects.filter(lab=lab)
        for extra in Extra_Exp:
            experiment_list = experiment_list | Experiment.objects.filter(
                id=extra.exp.id)
        public_exp = Experiment.objects.filter(is_public=1)
        experiment_list = experiment_list | public_exp
    '''
    multi-sort is done below
    '''
    filters = []
    if 'filter' in request.GET:
        filters = json.loads(request.GET['filter'])
    else:
        filters = []
    property = 'name'
    direction = ''
    if 'sort' in request.GET:
        sort = json.loads(str(request.GET['sort'])[1:-1])
        property = sort['property']
        if sort['direction'] == 'DESC':
            direction = '-'
    else:
        property = "name"
        direction = '-'

    start = int(request.GET['start'])
    limit = int(request.GET['limit'])
    end = start + limit

    experiment_list = firmianaLib.result_filter(experiment_list, filters)

    count = experiment_list.count()
    if end > count or limit == -1:
        end = count
    if property !='name':
        experiment_list = experiment_list.order_by(direction + property,'-name')[start:end]
    else:
        experiment_list = experiment_list.order_by(direction + property)[start:end]
    expInfo_list = []
    for experiment in experiment_list:
        temp = {}
        temp['id'] = experiment.id
        temp['name'] = experiment.name
        temp['type'] = experiment.type
        temp['description'] = experiment.description
        temp['species'] = experiment.species
        temp['cell_type'] = experiment.cell_type
        temp['tissue'] = experiment.tissue
        temp['organ'] = experiment.organ
        temp['fluid'] = experiment.fluid
        temp['num_fraction'] = experiment.num_fraction
        temp['num_repeat'] = experiment.num_repeat
        temp['num_spectrum'] = experiment.num_spectrum
        temp['num_peptide'] = experiment.num_peptide
        temp['num_isoform'] = experiment.num_isoform
        temp['num_gene'] = experiment.num_gene
        temp['instrument'] = experiment.instrument
        temp['protocol'] = experiment.protocol
        temp['lab'] = experiment.lab
        temp['operator'] = experiment.operator
        temp['experiment_date'] = experiment.experiment_date
        temp['index_date'] = experiment.index_date
        temp['update_date'] = experiment.update_date
        temp['stage'] = experiment.stage
        temp['state'] = experiment.state
        temp['bait'] = experiment.bait
        try:
            temp['ispec'] = experiments.models.Experiment.objects.get(
                id=int(experiment.name.split('Exp')[1])).fm_no
        except:
            temp['ispec'] = ''
        specific = ''
        try:
            for sample in experiments.models.Experiment.objects.get(id=int(experiment.name.split('Exp')[1])).samples.all():
                if sample.source_tissue:
                    specific = specific + sample.source_tissue.specific_ID + ';'
                if sample.source_cell:
                    specific = specific + sample.source_cell.specific_ID + ';'
                if sample.source_fluid:
                    specific = specific + sample.source_fluid.specific_ID + ';'
        except:
            specific = ''
        temp['specific'] = specific
        expInfo_list.append(temp)
    data = {"data": expInfo_list, "total": count}
    result = json.dumps(data, cls=DjangoJSONEncoder)

    return HttpResponse(result)


def showsearch_data(request):
    sid = int(request.GET['id'])
    Searchs = Search.objects.filter(exp_id=sid).filter(type='rep')
    SearchList = []
    for search in Searchs:
        temp = {}
        temp['repeat_id'] = search.repeat_id
        temp['fraction_id'] = search.fraction_id
        temp['num_fraction'] = Experiment.objects.get(id=search.exp_id).num_fraction
        temp['search_id'] = search.id
        temp['type'] = search.type
        temp['name'] = search.name
        temp['exp_id'] = search.exp_id
        temp['rank'] = search.rank
        temp['num_spectrum'] = search.num_spectrum
        temp['num_peptide'] = search.num_peptide
        temp['num_isoform'] = search.num_isoform
        temp['num_gene'] = search.num_gene
        temp['log'] = search.log
        temp['create_time'] = search.create_time
        temp['date'] = search.update_time
        temp['user'] = search.user
        temp['stage'] = search.stage
        temp['rt_max'] = search.rt_max
        temp['parameter'] = search.parameter
        SearchList.append(temp)

    data = {"data": SearchList, "total": len(SearchList)}
    result = json.dumps(data, cls=DjangoJSONEncoder)
    return HttpResponse(result)


def showjob(request):
    ''' Simple Authority '''
    uname = str(request.user)
    if request.user.is_superuser:
        job_list = XsearchTable.objects.all()
    else:
        job_list = XsearchTable.objects.filter(user=uname)

    '''
    multi-sort is done below
    '''
    filters = []
    if 'filter' in request.GET:
        filters = json.loads(request.GET['filter'])
    else:
        filters = []
    property = '?'
    direction = ''
    
    if 'sort' in request.GET:
        sort = json.loads(str(request.GET['sort'])[1:-1])
        property = sort['property']
        if sort['direction'] == 'DESC':
            direction = '-'
    else:
        property = "id"
        direction = '-'

    property = 'exp_num' if property == 'explist_length' else property
    start = int(request.GET['start'])
    limit = int(request.GET['limit'])
    end = start + limit

    job_list = firmianaLib.result_filter(job_list, filters)

    count = job_list.count()
    if end > count or limit == -1:
        end = count

    job_list = job_list.order_by(direction + property)[start:end]
    jobs = []
    for job in job_list:
        temp = {}
        temp['csv_name'] = job.id
        temp['dmz'] = job.dmz
        temp['drt'] = job.drt
        temp['ionscore'] = job.ionscore
        temp['searchs'] = job.searchs
        temp['compare'] = job.compare
        temp['qc'] = job.qc
        temp['done'] = job.done
        temp['ProGene'] = job.ProGene
        temp['create_time'] = job.create_time
        temp['update_time'] = job.update_time
        temp['user'] = job.user
        temp['status'] = job.status
        temp['explist'] = job.exp_name
        temp['exp_name'] = '*'.join([Experiment.objects.get(
            id=exp_str.split('_')[1]).name for exp_str in job.exp_name.split(",")])
        temp['explist_length'] = job.exp_num
        temp['description'] = job.description
        jobs.append(temp)

    data = {"data": jobs, "total": count}
    result = json.dumps(data, cls=DjangoJSONEncoder)
    return HttpResponse(result)


def help(request):
    return render_to_response('gardener/help.html')


@login_required(login_url=settings.LOGIN_PAGE)
def gardener(request):
    if 'theme' in request.GET:
        theme = request.GET['theme'] if request.GET['theme'] in [
            'classic', 'access', 'gray', 'neptune'] else ''
    else:
        theme = ''
    return render_to_response('gardener/gardener.html', {'theme': theme})


@login_required(login_url=settings.LOGIN_PAGE)
def showpeptide_data(request):
    if 'sid' in request.GET:
        sid = int(request.GET['sid'])
    else:
        sid = 0
    try:
        search_id = int(request.GET['search_id'])
    except:
        search_id = 0
    try:
        accession = str(request.GET['accession'])
    except:
        accession = 0
    try:
        exp_id = int(request.GET['exp_id'])
    except:
        exp_id = 0
    try:
        stype = str(request.GET['stype'])
    except:
        stype = ''
    try:
        rankid = int(request.GET['rankid'])
    except:
        rankid = 0
    try:
        symbol = str(request.GET['symbol'])
    except:
        symbol = 0
    start = int(request.GET['start'])
    limit = int(request.GET['limit'])
    end = start + limit
    '''
    multi-sort is done below
    '''
    filters = []
    try:
        filters = json.loads(request.GET['filter'])
    except:
        filters = []
    property = '?'
    direction = ''
    try:
        sort = json.loads(str(request.GET['sort'])[1:-1])
        property = sort['property']
        if sort['direction'] == 'DESC':
            direction = '-'
        if property == 'exp_name':
            property = 'search'
    except:
        property = "ion_score"
        direction = '-'

    if stype == 'protein':
        tp = Search.objects.filter(id=search_id)[0].type
        if tp == 'exp':
            peptide_list = Exp_Peptide.objects.all()
        elif tp == 'rep':
            peptide_list = Repeat_Peptide.objects.all()
    elif stype == 'exper' or stype == 'anywhere':
        if sid!=6954:
            peptide_list = Exp_Peptide.objects.all()
        else:
            peptide_list = Exp_Peptide_200.objects.all()
#         peptide_list = Exp_Peptide.objects.all()
    elif stype == 'search':
        peptide_list = Repeat_Peptide.objects.all()
    elif stype == 'gene':
        tp = Search.objects.filter(id=search_id)[0].type
        if tp == 'exp':
            protein_list = Exp_Protein.objects.all()
            peptide_list = Exp_Peptide.objects.all()
        elif tp == 'rep':
            protein_list = Repeat_Protein.objects.all()
            peptide_list = Repeat_Peptide.objects.all()
    if len(filters) != 0:
        for filter in filters:
            if filter['type'] == 'string':
                if filter['field'] == 'exp_description':
                    peptide_list = peptide_list.filter(
                        search__exp__description__icontains=str(filter['value']))
                else:
                    kwargs = {str(filter['field']) +
                              '__icontains': str(filter['value'])}
                    peptide_list = peptide_list.filter(**kwargs)
            if filter['type'] == 'numeric':
                if filter['comparison'] == 'lt' or filter['comparison'] == 'gt':
                    kwargs = {
                        str(filter['field']) + '__' + str(filter['comparison']): str(filter['value'])}
                else:
                    kwargs = {str(filter['field']) +
                              '__exact': str(filter['value'])}
                peptide_list = peptide_list.filter(**kwargs)
            if filter['type'] == 'date':
                ptime = str(filter['value']).split('/')

                if filter['comparison'] == 'lt' or filter['comparison'] == 'gt':
                    today = str(datetime.datetime(
                        int(ptime[2]), int(ptime[0]), int(ptime[1])))
                    kwargs = {str(filter['field']) + '__' +
                              str(filter['comparison']): today}
                    peptide_list = peptide_list.filter(**kwargs)
                else:
                    today = datetime.datetime(int(ptime[2]), int(
                        ptime[0]), int(ptime[1])) - timedelta(days=1)
                    tomorrow = today + timedelta(days=2)
                    kwargs = {str(filter['field']) + '__gt': str(today)}
                    protein_list = protein_list.filter(**kwargs)
                    kwargs = {str(filter['field']) + '__lt': str(tomorrow)}
                    peptide_list = peptide_list.filter(**kwargs)
    if stype == 'protein':
        peptide_list = peptide_list.filter(protein_group_accessions__contains=accession).filter(
            search__id=search_id).exclude(type=-1)
        # return HttpResponse(str(accession)+''+str(search_id))
    elif stype == 'exper':
        sid = Search.objects.filter(exp_id=sid).filter(type='exp')[0].id
        peptide_list = peptide_list.filter(search__id=sid).order_by(
            direction + property).exclude(type=-1)
    elif stype == 'search':
        peptide_list = peptide_list.filter(search__id=search_id).order_by(
            direction + property).exclude(type=-1)
    elif stype == 'gene':
        protein_list = protein_list.filter(symbol=symbol).filter(
            search__id=search_id).exclude(type=-1).values('accession')
        acc_list = []
        for tt in protein_list:
            acc_list.append(str(tt['accession']))
        temp_list = []
        for acc in acc_list:
            tt_list = peptide_list.filter(search__id=search_id).filter(
                protein_group_accessions__contains=acc).order_by(direction + property).exclude(type=-1)
            temp_list.extend(tt_list)
        peptide_list = list(set(temp_list))
    elif stype == 'anywhere':
        peptide_list = peptide_list.filter(Q(sequence__icontains=symbol) | Q(
            modification__icontains=symbol)).order_by(direction + property).exclude(type=-1)
    # only_list = peptide_list.values('sequence', 'modification')
    if stype != 'gene':
        count = peptide_list.count()
    else:
        count = len(peptide_list)

    # huge = peptide_list.aggregate(Max('area'))['area__max']
    if end > count or limit == -1:
        end = count
    peptide_list = peptide_list[start:end]
    # only_list = only_list[start:end]
    peptides = []
    for peptide in peptide_list:
        temp = {}
        temp['id'] = peptide.id
        temp['ms2'] = peptide.ms2_id
        temp['exp_description'] = peptide.search.exp.description
        temp['search_id'] = peptide.search_id
        temp['sequence'] = peptide.sequence
        temp['type'] = peptide.type
        temp['quality'] = peptide.quality
        temp['num_psms'] = peptide.num_psms
        temp['num_proteins'] = peptide.num_proteins
        temp['num_protein_groups'] = peptide.num_protein_groups
        temp['protein_group_accessions'] = peptide.protein_group_accessions
        temp['modification'] = peptide.modification
        temp['delta_cn'] = peptide.delta_cn
        temp['area'] = peptide.area
        temp['fot'] = peptide.fot
        temp['q_value'] = peptide.q_value
        temp['pep'] = peptide.pep
        temp['ion_score'] = peptide.ion_score
        temp['exp_value'] = peptide.exp_value
        temp['charge'] = peptide.charge
        temp['mh_da'] = peptide.mh_da
        temp['delta_m_ppm'] = peptide.delta_m_ppm
        temp['rt_min'] = round(float(peptide.rt_min), 2)
        temp['num_missed_cleavages'] = peptide.num_missed_cleavages
        if stype == 'anywhere':
            temp['exp_name'] = peptide.search.exp.name
        temp['fdr'] = peptide.fdr
        temp['from_where'] = peptide.from_where
        peptides.append(temp)
    data = {"data": peptides, "total": count}
    result = json.dumps(data, cls=DjangoJSONEncoder)
    return HttpResponse(result)


@login_required(login_url=settings.LOGIN_PAGE)
def showgene_data(request):
    sid = int(request.GET['sid']) if 'sid' in request.GET else 0
    stype = str(request.GET['stype']) if 'stype' in request.GET else ''
    symbol = str(request.GET['symbol']) if'symbol' in request.GET else ''
    start = int(request.GET['start']) if 'start' in request.GET else 0
    limit = int(request.GET['limit']) if 'limit' in request.GET else -1
    end = start + limit
    '''
    multi-sort is done below
    '''
    filters = []
    try:
        filters = json.loads(request.GET['filter'])
    except:
        filters = []
    property = '?'
    direction = ''
    try:
        sort = json.loads(str(request.GET['sort'])[1:-1])
        property = sort['property']
        if property == 'exp_name':
            property = 'search'
        if sort['direction'] == 'DESC':
            direction = '-'
    except:
        property = "area"
        direction = '-'

    if stype == 'exper' or stype == 'anywhere':
        gene_list = Exp_Gene.objects.all()
    if stype == 'search':
        gene_list = Repeat_Gene.objects.all()
    if len(filters) != 0:
        for filter in filters:
            if filter['field'] == 'user_specified':
                anno_protein = user_defined.objects.filter(
                    user=request.user.id).filter(annotation__icontains=filter['value'])
                if stype != 'anywhere':
                    if stype == 'exper':
                        species = Search.objects.get(id=Search.objects.filter(
                            exp_id=sid).filter(type='exp')[0].id).exp.species
                    else:
                        species = Search.objects.get(id=sid).exp.species
                    anno_protein = anno_protein.filter(species=species)
                anno_proteins = anno_protein.values_list('symbol', flat=True)
                gene_list = gene_list.filter(symbol__in=anno_proteins)
                continue
            if filter['type'] == 'list':
                for anno in filter['value']:
                    kwargs = {str(filter['field']) + '__icontains': anno}
                    gene_list = gene_list.filter(**kwargs)
            if filter['type'] == 'string':
                if filter['field'] == 'exp_description':
                    gene_list = gene_list.filter(
                        search__exp__description__icontains=str(filter['value']))
                else:
                    kwargs = {str(filter['field']) +
                              '__icontains': str(filter['value'])}
                    gene_list = gene_list.filter(**kwargs)
            if filter['type'] == 'numeric':
                if filter['comparison'] == 'lt' or filter['comparison'] == 'gt':
                    kwargs = {
                        str(filter['field']) + '__' + str(filter['comparison']): str(filter['value'])}
                else:
                    kwargs = {str(filter['field']) +
                              '__exact': str(filter['value'])}
                gene_list = gene_list.filter(**kwargs)
            if filter['type'] == 'date':
                ptime = str(filter['value']).split('/')

                if filter['comparison'] == 'lt' or filter['comparison'] == 'gt':
                    today = str(datetime.datetime(
                        int(ptime[2]), int(ptime[0]), int(ptime[1])))
                    kwargs = {str(filter['field']) + '__' +
                              str(filter['comparison']): today}
                    gene_list = gene_list.filter(**kwargs)
                else:
                    today = datetime.datetime(int(ptime[2]), int(
                        ptime[0]), int(ptime[1])) - timedelta(days=1)
                    tomorrow = today + timedelta(days=2)
                    kwargs = {str(filter['field']) + '__gt': str(today)}
                    gene_list = gene_list.filter(**kwargs)
                    kwargs = {str(filter['field']) + '__lt': str(tomorrow)}
                    gene_list = gene_list.filter(**kwargs)
    if stype == 'exper':
        gene_list = gene_list.filter(search__exp_id=sid).exclude(type=-1)
    if stype == 'search':
        gene_list = gene_list.filter(search__id=sid).exclude(type=-1)
    if stype == 'anywhere':
        if property != 'search':
            gene_list = gene_list.filter(
                symbol__icontains=symbol).exclude(type=-1)
        else:
            gene_list = gene_list.filter(
                symbol__icontains=symbol).exclude(type=-1)
    if property == 'search':
        gene_list = gene_list.order_by(direction + 'search__exp__id')
    elif property == 'user_specified':  # some problems I don't know
        for gen in range(len(gene_list)):
            gene = gene_list[gen]
            anno = user_defined.objects.filter(
                user=request.user.id, species=gene.search.exp.species, symbol=gene.symbol)
            gene_list[gen].user_specified = anno[0].annotation if anno else ""
        sorted(gene_list, key=lambda x: x.user_specified)
    else:
        gene_list = gene_list.order_by(direction + property)
    count = gene_list.count()
    if end > count or limit == -1:
        end = count
    gene_list = gene_list[start:end]
    genes = []
    for gene in gene_list:
        temp = {}
        temp['id'] = gene.id
        temp['exp_description'] = gene.search.exp.description
        temp['search_id'] = gene.search_id
        temp['symbol'] = gene.symbol
        temp['gene_id'] = gene.gene_id
        temp['protein_gi'] = gene.protein_gi
        temp['num_proteins'] = gene.num_proteins
        temp['num_identified_proteins'] = gene.num_identified_proteins
        temp['num_uni_proteins'] = gene.num_uni_proteins
        temp['num_peptides'] = gene.num_peptides
        temp['num_uni_peptides'] = gene.num_uni_peptides
        anno = user_defined.objects.filter(
            user=request.user.id, species=gene.search.exp.species, symbol=gene.symbol)
        temp['user_specified'] = anno[0].annotation if anno else ""
        temp['area'] = gene.area
        temp['fot'] = gene.fot
        temp['ibaq'] = gene.ibaq
        temp['fdr'] = gene.fdr
        temp['description'] = gene.description
        temp['annotation'] = gene.annotation
        temp['modification'] = gene.modification
        if stype == 'anywhere':
            temp['exp_name'] = gene.search.exp.name
        temp['fdr'] = gene.fdr
        genes.append(temp)

    data = {"data": genes, "total": count}
    result = json.dumps(data, cls=DjangoJSONEncoder)

    return HttpResponse(result)


def download_database(request):
    '''
    multi-sort is done below
    '''
    reload(sys)
    sys.setdefaultencoding('utf-8')
    filters = []
    try:
        filters = json.loads(request.GET['filter'])
    except:
        filters = []
    '''
    sort is done below
    '''
    property = '?'
    direction = ''
    try:
        sort = json.loads(str(request.GET['sort'])[1:-1])
        property = sort['property']
        if sort['direction'] == 'DESC':
            direction = '-'
    except:
        property = "id"
        direction = ''

    ''' Simple Authority '''
    lab = experiments.models.User_Laboratory.objects.filter(user=request.user)
    lab = lab[0].lab if lab.count() else ''

    if lab == 'Demo Lab':
        experiment_list = Experiment.objects.all().filter(
            is_public=1).filter(is_deleted=0)
    elif request.user.is_superuser:
        experiment_list = Experiment.objects.all().filter(is_deleted=0)
    else:
        experiment_list = Experiment.objects.all().filter(lab=lab).filter(is_deleted=0)
        Extra_Exp = Share_Exp.objects.filter(lab=lab)
        for extra in Extra_Exp:
            experiment_list = experiment_list | Experiment.objects.filter(
                id=extra.exp.id)

    if len(filters) != 0:
        for filter in filters:
            if filter['type'] == 'string':
                '''
                need to be update:?a a? a
                '''
                kwargs = {str(filter['field']) +
                          '__icontains': str(filter['value'])}
                experiment_list = experiment_list.filter(**kwargs)
            if filter['type'] == 'numeric':
                if filter['comparison'] == 'lt' or filter['comparison'] == 'gt':
                    kwargs = {
                        str(filter['field']) + '__' + str(filter['comparison']): str(filter['value'])}
                else:
                    kwargs = {str(filter['field']) +
                              '__exact': str(filter['value'])}
                experiment_list = experiment_list.filter(**kwargs)

    count = experiment_list.count()
    experiment_list = experiment_list.order_by(direction + property)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="experiment.txt"'
    writer = csv.writer(response, delimiter='\t')
    writer.writerow(['', 'Name', 'Type', 'Description', 'Species', 'Cell Type', 'Tissue', 'Organ', 'Fraction Num', 'Repeat Num', 'Spectrum Num',
                     'Peptide Num', 'Isoform Num', 'Gene Num', 'Instrument', 'Protocol', 'Lab', 'Operator', 'Experiment Date', 'Index Date', 'Update Date', 'Stage'])
    i = 1
    for experiment in experiment_list:
        temp = []
        temp.append(str(i))
        # temp.append(experiment.id)
        temp.append(experiment.name)
        temp.append(experiment.type)
        temp.append(experiment.description)
        temp.append(experiment.species)
        temp.append(experiment.cell_type)
        temp.append(experiment.tissue)
        temp.append(experiment.organ)
        temp.append(experiment.num_fraction)
        temp.append(experiment.num_repeat)
        temp.append(experiment.num_spectrum)
        temp.append(experiment.num_peptide)
        temp.append(experiment.num_isoform)
        temp.append(experiment.num_gene)
        temp.append(experiment.instrument)
        temp.append(experiment.protocol)
        temp.append(experiment.lab)
        temp.append(experiment.operator)
        temp.append(experiment.experiment_date)
        temp.append(experiment.index_date)
        temp.append(experiment.update_date)
        temp.append(experiment.stage)
        temp = [str(item) for item in temp]
        writer.writerow(temp)
        i += 1
    return response


def download_protein(request):
    '''
    multi-sort is done below
    '''

    reload(sys)
    sys.setdefaultencoding('utf-8')
    try:
        sid = int(request.GET['sid'])
    except:
        sid = 0
    try:
        stype = str(request.GET['stype'])
    except:
        stype = ''
    filters = []
    try:
        filters = json.loads(request.GET['filter'])
    except:
        filters = []
    try:
        exp_name = str(request.GET['exp_name'])
    except:
        exp_name = ''
    symbol = str(request.GET['symbol']) if 'symbol' in request.GET else ''
    '''
    sort is done below
    '''
    property = '?'
    direction = ''
    try:
        sort = json.loads(str(request.GET['sort'])[1:-1])
        property = sort['property']
        if sort['direction'] == 'DESC':
            direction = '-'
    except:
        property = "id"
        direction = ''
    if stype == 'exper':
        if exp_name == '':
            exp_name = Experiment.objects.get(id=sid).name
            protein_list = Exp_Protein.objects.filter(
                search__exp__id=sid).filter(search__type='exp').filter(type=1)
        else:
            #exp_name = Experiment.objects.get(id=sid).name
            protein_list = Exp_Protein.objects.all().filter(
                search__exp__name=exp_name).filter(search__type='exp').filter(type=1)
    if stype == 'search':
        protein_list = []  # Repeat_Protein.objects.all().filter(search_id=sid)
    if stype == 'anywhere' or stype == 'anno':
        protein_list = Exp_Protein.objects.all()
    if stype == 'anywhere':
        exp_name = symbol
        protein_list = protein_list.filter(Q(other_members__icontains=symbol) | Q(accession__icontains=symbol) | Q(
            symbol__icontains=symbol) | Q(description__icontains=symbol)).order_by(direction + property).exclude(type=-1)
    # protein_list = Protein.objects.all()
    if len(filters) != 0:
        for filter in filters:
            if filter['type'] == 'list':
                for anno in filter['value']:
                    kwargs = {str(filter['field']) + '__icontains': anno}
                    protein_list = protein_list.filter(**kwargs)
            if filter['type'] == 'string':
                kwargs = {str(filter['field']) +
                          '__icontains': str(filter['value'])}
                protein_list = protein_list.filter(**kwargs)
            if filter['type'] == 'numeric':
                if filter['comparison'] == 'lt' or filter['comparison'] == 'gt':
                    kwargs = {
                        str(filter['field']) + '__' + str(filter['comparison']): str(filter['value'])}
                else:
                    kwargs = {str(filter['field']) +
                              '__exact': str(filter['value'])}
                protein_list = protein_list.filter(**kwargs)

    count = protein_list.count()
    protein_list = protein_list.order_by(direction + property)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=' + \
        exp_name + '_protein.txt'
    writer = csv.writer(response, delimiter='\t')
    title = ['Accession', 'Annotation', 'Modification', 'Same set', 'Symbol', 'Description', 'Score',
             'Coverage', '# Proteins', '# Unqiue Peptides', '# Peptides',
             '# PSMs', 'Area', 'FoT(1e-6)', 'iBAQ', 'Length', 'MW', 'calc. pI']
    if stype == 'anywhere':
        title = ['ExpName', 'Exp Description'] + title
    writer.writerow(title)
    i = 1
    for protein in protein_list:
        temp = []
        # temp.append(str(i))
        # temp.append(protein.id)
        if stype == 'anywhere':
            temp.append(protein.search.exp.name)
            temp.append(protein.search.exp.description)
        temp.append(protein.accession)
        temp.append(protein.annotation)
        temp.append(protein.modification)
        temp.append(protein.other_members)
        temp.append(protein.symbol)
        temp.append(protein.description)
        temp.append(protein.score)
        temp.append(protein.coverage)
        temp.append(protein.num_proteins)
        temp.append(protein.num_uni_peptides)
        temp.append(protein.num_peptides)
        temp.append(protein.num_psms)
        temp.append(protein.area)
        temp.append(protein.fot)
        temp.append(protein.ibaq)
        temp.append(protein.length)
        temp.append(protein.mw)
        temp.append(protein.calc_pi)
        temp = [str(item) for item in temp]
        writer.writerow(temp)
        i += 1
    return response


def download_peptide(request):
    reload(sys)
    sys.setdefaultencoding('utf-8')
    try:
        sid = int(request.GET['sid'])
    except:
        sid = 0
    try:
        stype = str(request.GET['stype'])
    except:
        stype = ''
    try:
        exp_name = str(request.GET['exp_name'])
    except:
        exp_name = ''
    filters = []
    try:
        filters = json.loads(request.GET['filter'])
    except:
        filters = []
    '''
    sort is done below
    '''
    property = '?'
    direction = ''
    try:
        sort = json.loads(str(request.GET['sort'])[1:-1])
        property = sort['property']
        if sort['direction'] == 'DESC':
            direction = '-'
    except:
        property = "id"
        direction = ''
    if stype == 'exper':
        if sid != 0:
            exp_name = Experiment.objects.get(id=sid).name
            peptide_list = Exp_Peptide.objects.all().filter(
                search__exp__id=sid).filter(search__type='exp').filter(type=1)
        else:
            #exp_name = Experiment.objects.get(name=exp_name).name
            peptide_list = Exp_Peptide.objects.all().filter(
                search__exp__name=exp_name).filter(search__type='exp').filter(type=1)
    if stype == 'search':
        peptide_list = []  # Repeat_Peptide.objects.all().filter(search_id=sid)
    # peptide_list = Peptide.objects.all()
    if len(filters) != 0:
        for filter in filters:
            if filter['type'] == 'string':
                kwargs = {str(filter['field']) +
                          '__icontains': str(filter['value'])}
                peptide_list = peptide_list.filter(**kwargs)
            if filter['type'] == 'numeric':
                if filter['comparison'] == 'lt' or filter['comparison'] == 'gt':
                    kwargs = {
                        str(filter['field']) + '__' + str(filter['comparison']): str(filter['value'])}
                else:
                    kwargs = {str(filter['field']) +
                              '__exact': str(filter['value'])}
                peptide_list = peptide_list.filter(**kwargs)

    count = peptide_list.count()
    peptide_list = peptide_list.order_by(direction + property)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=' + \
        exp_name + "_peptide.txt"
    writer = csv.writer(response, delimiter='\t')
    writer.writerow(['Sequence', 'Modification', 'Ion score', 'Retetion Time(minute)',
                     'Area', 'FoT(1e-6)', 'Charge', '# Missed Cleavages', '# PSMs', '# Proteins',
                     '# Protein Groups', 'Protein Group Accessions', 'Delta Cn', 'Q Value',
                     'PEP', 'Exp Score', 'MH+ [Da]', 'Delta M [ppm]', 'Quality', 'File Name', 'FDR'])
    i = 1
    for peptide in peptide_list:
        temp = []
        temp.append(peptide.sequence)
        temp.append(peptide.modification)
        temp.append(peptide.ion_score)
        temp.append(round(float(peptide.rt_min) / 60, 2))
        temp.append(peptide.area)
        temp.append(peptide.fot)
        temp.append(peptide.charge)
        temp.append(peptide.num_missed_cleavages)
        temp.append(peptide.num_psms)
        temp.append(peptide.num_proteins)
        temp.append(peptide.num_protein_groups)
        temp.append(peptide.protein_group_accessions)
        temp.append(peptide.delta_cn)
        temp.append(peptide.q_value)
        temp.append(peptide.pep)
        temp.append(peptide.exp_value)
        temp.append(peptide.mh_da)
        temp.append(peptide.delta_m_ppm)
        temp.append(peptide.quality)
        temp.append(peptide.from_where)
        temp.append(peptide.fdr)
        temp = [str(item) for item in temp]
        writer.writerow(temp)
        i += 1
    return response


def download_gene(request):

    reload(sys)
    sys.setdefaultencoding('utf-8')
    try:
        sid = int(request.GET['sid'])
    except:
        sid = 0
    try:
        stype = str(request.GET['stype'])
    except:
        stype = ''
    filters = []
    try:
        filters = json.loads(request.GET['filter'])
    except:
        filters = []
    try:
        exp_name = str(request.GET['exp_name'])
    except:
        exp_name = ''
    '''
    sort is done below
    '''
    property = '?'
    direction = ''
    try:
        sort = json.loads(str(request.GET['sort'])[1:-1])
        property = sort['property']
        if sort['direction'] == 'DESC':
            direction = '-'
    except:
        property = "id"
        direction = ''
    if stype == 'exper':
        if sid != 0:
            exp_name = Experiment.objects.get(id=sid).name
            gene_list = Exp_Gene.objects.all().filter(
                search__exp__id=sid).filter(search__type='exp').filter(type=1)
        else:
            gene_list = Exp_Gene.objects.all().filter(
                search__exp__name=exp_name).filter(search__type='exp').filter(type=1)
    if stype == 'search':
        gene_list = []  # Repeat_Peptide.objects.all().filter(search_id=sid)
    # gene_list = Peptide.objects.all()
    if len(filters) != 0:
        for filter in filters:
            if filter['type'] == 'list':
                for anno in filter['value']:
                    kwargs = {str(filter['field']) + '__icontains': anno}
                    gene_list = gene_list.filter(**kwargs)
            if filter['type'] == 'string':
                kwargs = {str(filter['field']) +
                          '__icontains': str(filter['value'])}
                gene_list = gene_list.filter(**kwargs)
            if filter['type'] == 'numeric':
                if filter['comparison'] == 'lt' or filter['comparison'] == 'gt':
                    kwargs = {
                        str(filter['field']) + '__' + str(filter['comparison']): str(filter['value'])}
                else:
                    kwargs = {str(filter['field']) +
                              '__exact': str(filter['value'])}
                gene_list = gene_list.filter(**kwargs)

    count = gene_list.count()
    gene_list = gene_list.order_by(direction + property)
    response = HttpResponse(content_type='text/csv')

    content = 'attachment; filename=' + exp_name + '_gene' + ".txt"
    response['Content-Disposition'] = content
    writer = csv.writer(response, delimiter='\t')
    writer.writerow(['Gene ID', 'Symbol', 'Description', 'Proteins', 'Protein Num',
                     'Peptide Num', 'Unique Peptide Num', 'Area', 'FoT(1e-6)', 'iBAQ', 'PSMs'])
    i = 1
    for gene in gene_list:
        temp = []
        # temp.append(str(i))
        # temp.append(gene.id)
        temp.append(gene.gene_id)
        temp.append(gene.symbol)
        temp.append(gene.description)
        temp.append(gene.protein_gi)
        temp.append(gene.num_proteins)
        temp.append(gene.num_peptides)
        temp.append(gene.num_uni_peptides)
        temp.append(gene.area)
        temp.append(gene.fot)
        temp.append(gene.ibaq)
        temp.append(gene.num_psms)
        temp = [str(item) for item in temp]
        writer.writerow(temp)
        i += 1
    return response

def showprotein_data_test(request):
    
    return(HttpResponse(result))
@login_required(login_url=settings.LOGIN_PAGE)
def showprotein_data(request):

    sid = int(request.GET['sid']) if 'sid' in request.GET else 0

    rankid = int(request.GET['rankid']) if 'rankid' in request.GET else 0

    stype = str(request.GET['stype']) if 'stype' in request.GET else ''

    symbol = str(request.GET['symbol']) if 'symbol' in request.GET else ''

    search_id = int(request.GET['search_id']
                    ) if 'search_id' in request.GET else 0

    protein_group_accessions = str(request.GET[
                                   'protein_group_accessions']) if 'protein_group_accessions' in request.GET else ''

    '''
    multi-sort is done below
    '''
    filters = []
    try:
        filters = json.loads(request.GET['filter'])
    except:
        filters = []
    property = '?'
    direction = ''
    try:
        sort = json.loads(str(request.GET['sort'])[1:-1])
        property = sort['property']
        if sort['direction'] == 'DESC':
            direction = '-'
    except:
        property = "coverage"
        direction = '-'

    if stype == 'exper' or stype == 'anywhere' or stype == 'anno':
        if sid!=6954:
            protein_list = Exp_Protein.objects.all()
        else:
            protein_list = Exp_Protein_200.objects.all()
    elif stype == 'search':
        protein_list = Repeat_Protein.objects.all()
    elif stype == 'gene' or stype == 'peptide':
        tp = Search.objects.filter(id=search_id)[0].type
        if tp == 'exp':
            protein_list = Exp_Protein.objects.all()
        elif tp == 'rep':
            protein_list = Repeat_Protein.objects.all()
    
#     ref_score_dict = {}
#     for protein in protein_list:
#         peptideListWCE = Best_Responders_WCE.objects.all().filter(protein_gi = protein.accession)
#         if len(peptideListWCE) != 0:
#             tmpList = []
#             for peptide in peptideListWCE:
#                 tmpList.append(peptide.ref_score)
#             tmpList.sort(reverse = True)
#             if len(tmpList) > 3:
#                 avg = (tmpList[0] + tmpList[1] + tmpList[2]) / 3
#             else:
#                 avg = sum(tmpList) / len(tmpList)
#             ref_score_dict[protein.accession] = avg
#         else:
#             peptideListTFRE = Best_Responders_TFRE.objects.all().filter(protein_gi = protein.accession)
#             if len(peptideListTFRE) != 0:
#                 tmpList = []
#                 for peptide in peptideListTFRE:
#                     tmpList.append(peptide.ref_score)
#                 tmpList.sort(reverse = True)
#                 if len(tmpList) > 3:
#                     avg = (tmpList[0] + tmpList[1] + tmpList[2]) / 3
#                 else:
#                     avg = sum(tmpList) / len(tmpList)
#                 ref_score_dict[protein.accession] = avg
#             else:
#                 ref_score_dict[protein.accession] = -1
                
    if len(filters) != 0:
        for filter in filters:
            if filter['field'] == 'user_specified':
                anno_protein = user_defined.objects.filter(
                    user=request.user.id).filter(annotation__icontains=filter['value'])
                if stype != 'anywhere':
                    if stype == 'exper':
                        species = Search.objects.get(id=Search.objects.filter(
                            exp_id=sid).filter(type='exp')[0].id).exp.species
                    else:
                        species = Search.objects.get(id=sid).exp.species
                    anno_protein = anno_protein.filter(species=species)
                anno_proteins = anno_protein.values_list('symbol', flat=True)
                protein_list = protein_list.filter(symbol__in=anno_proteins)
                continue
            if filter['type'] == 'list':
                for anno in filter['value']:
                    kwargs = {str(filter['field']) + '__icontains': anno}
                    protein_list = protein_list.filter(**kwargs)
            elif filter['type'] == 'string':
                if filter['field'] == 'exp_description':
                    protein_list = protein_list.filter(
                        search__exp__description__icontains=str(filter['value']))
                else:
                    kwargs = {str(filter['field']) +
                              '__icontains': str(filter['value'])}
                    protein_list = protein_list.filter(**kwargs)

            elif filter['type'] == 'numeric':
                if filter['comparison'] == 'lt' or filter['comparison'] == 'gt':
                    kwargs = {
                        str(filter['field']) + '__' + str(filter['comparison']): str(filter['value'])}
                else:
                    kwargs = {str(filter['field']) +
                              '__exact': str(filter['value'])}
                protein_list = protein_list.filter(**kwargs)

    if stype == 'exper':
        ExpID = sid
        sid = Search.objects.filter(exp_id=sid).filter(type='exp')[0].id
        print 'sid',sid
        protein_list = protein_list.filter(search__id=sid).exclude(type=-1)
    if stype == 'search':
        protein_list = protein_list.filter(
            search__id=search_id).exclude(type=-1)
    if stype == 'gene':
        protein_list = protein_list.filter(symbol=symbol).filter(
            search__id=search_id).exclude(type=-1)
    if stype == 'peptide':
        protein_list = protein_list.filter(accession__in=protein_group_accessions.split(
            ';')).filter(search__id=search_id).exclude(type=-1)
    if stype == 'anywhere':
        protein_list = protein_list.filter(Q(other_members__icontains=symbol) | Q(accession__icontains=symbol) | Q(
            symbol__icontains=symbol) | Q(description__icontains=symbol)).exclude(type=-1)
    count = protein_list.count()

    if 'toGenome' in request.GET:
        gi = []
        for pro in protein_list:
            gi.append(pro.accession)
        # sid = Search.objects.filter(exp_id=sid).filter(type='exp')[0].id
        ExpID = Experiment.objects.get(id=ExpID).name
        result = genome.Protein2Genome_new(ExpID, gi)
        data = {'success': True, 'species': result[
            0], 'file': result[1], 'chr': result[2]}
        result = json.dumps(data, cls=DjangoJSONEncoder)
        return HttpResponse(result)

    start = int(request.GET['start'])if 'start' in request.GET else 0
    limit = int(request.GET['limit'])if 'limit' in request.GET else -1
    end = start + limit
    if end > count or limit == -1:
        end = count
    if property == 'exp_name':
        protein_list = protein_list.order_by(direction + 'search__exp__name')
    elif property == 'exp_description':
        protein_list = protein_list.order_by(
            direction + 'search__exp__description')
    elif property == 'user_specified':  # some problems I don't know
        for pro in range(len(protein_list)):
            protein = protein_list[pro]
            anno = user_defined.objects.filter(
                user=request.user.id, species=protein.search.exp.species, symbol=protein.symbol)
            protein_list[pro].user_specified = anno[
                0].annotation if anno else ""
        sorted(protein_list, key=attrgetter('user_specified'))
    else:
        protein_list = protein_list.order_by(direction + property)
    protein_list = protein_list[start:end]
    proteins = []

    for protein in protein_list:
        temp = {}
        temp['id'] = protein.id
        anno = user_defined.objects.filter(
            user=request.user.id, species=protein.search.exp.species, symbol=protein.symbol)
        temp['user_specified'] = anno[0].annotation if anno else ""
        temp['search_id'] = protein.search_id
        temp['exp_description'] = protein.search.exp.description
        temp['other_members'] = protein.other_members
        temp['accession'] = protein.accession
        temp['symbol'] = protein.symbol
        temp['description'] = protein.description
        temp['score'] = protein.score
        temp['coverage'] = protein.coverage
        temp['num_proteins'] = protein.num_proteins
        temp['num_uni_peptides'] = protein.num_uni_peptides
        temp['num_peptides'] = protein.num_peptides
        temp['num_psms'] = protein.num_psms
        temp['area'] = protein.area
        temp['length'] = protein.length
        temp['mw'] = protein.mw
        temp['fot'] = protein.fot
        temp['ibaq'] = protein.ibaq
        temp['fdr'] = protein.fdr
        temp['annotation'] = protein.annotation
        temp['modification'] = protein.modification
        temp['exp_name'] = protein.search.exp.name
#         temp['ref_score'] = ref_score_dict[protein.accession]
        proteins.append(temp)
    data = {"data": proteins, "total": count}
    result = json.dumps(data, cls=DjangoJSONEncoder)

    return HttpResponse(result)


def showms1_tic_data(request):
    if not request.GET.has_key('search_id'):
        exp_id = request.GET['exp_id']
        repeat_id = request.GET['repeat_id']
        rank = request.GET['rank']
        fraction_id = request.GET[
            'fraction_id'] if request.GET.has_key('fraction_id') else 1
        searchid = Search.objects.filter(exp_id=exp_id).filter(repeat_id=repeat_id).filter(
            rank=rank).filter(fraction_id=fraction_id).filter(type='fraction')[0].id
    else:
        searchid = request.GET['search_id']
    tic_ms1List = []
    tic_ms1s = MS1.objects.filter(search_id=searchid).order_by('rt')
    count = tic_ms1s.count()
    for tic_ms1 in tic_ms1s:
        temp = {}
        temp['rt'] = tic_ms1.rt
        temp['intensity'] = tic_ms1.intensity
        tic_ms1List.append(temp)
    data = {"data": tic_ms1List, "total": count}
    result = json.dumps(data, cls=DjangoJSONEncoder)
    return HttpResponse(result)


def show_tic_fraction(request):
    exp_id = request.GET['exp_id']
    repeat_id = request.GET['repeat_id']
    rank = request.GET['rank']
    searchs = Search.objects.filter(exp_id=exp_id).filter(repeat_id=repeat_id).filter(
        rank=rank).filter(type='fraction').order_by('fraction_id')
    searchList = []
    count = searchs.count()
    for search in searchs:
        temp = {}
        temp['fraction'] = 'Fraction:' + str(search.fraction_id)
        temp['search_id'] = search.id
        searchList.append(temp)
    data = {"data": searchList, "total": count}
    result = json.dumps(data, cls=DjangoJSONEncoder)
    return HttpResponse(result)


def get_rank(request):
    if request.GET.has_key('search_id'):
        search_id = request.GET['search_id']
    elif request.GET.has_key('protein_id'):
        search_id = Protein.objects.filter(
            id=request.GET['protein_id'])[0].search_id
    elif request.GET.has_key('exp_id'):
        temp = request.GET['exp_id'].split('_')
        (type, exp_id, rank, repe) = (temp[0], int(
            temp[1]), int(temp[2]), int(temp[3]))
        search_id = Search.objects.filter(exp_id=exp_id).filter(
            rank=rank).filter(repeat_id=repe).filter(type='rep')[0].id
    type = Search.objects.filter(id=search_id)[0].type
    exp_id = Search.objects.filter(id=search_id)[0].exp_id
    first_rank = Search.objects.filter(id=search_id)[0].rank if type == 'rep' else Search.objects.filter(
        exp_id=exp_id).filter(type='fraction')[0].rank
    searchs = Search.objects.filter(exp_id=exp_id).filter(
        type='fraction').exclude(rank=first_rank)
    searchList = []
    searchList.append(
        {'rank': 'Batch:' + str(first_rank), 'rank_id': first_rank})
    ranks = set()
    for search in searchs:
        temp = {}
        if search.rank not in ranks:
            temp['rank'] = 'Batch:' + str(search.rank)
            temp['rank_id'] = search.rank
            searchList.append(temp)
            ranks.add(search.rank)
    data = {"data": searchList, "total": len(searchList)}
    result = json.dumps(data, cls=DjangoJSONEncoder)
    return HttpResponse(result)


def sum_pep_viewer(request):
    if request.GET.has_key('search_id'):
        search_id = request.GET['search_id']
    elif request.GET.has_key('protein_id'):
        search_id = Protein.objects.filter(
            id=request.GET['protein_id'])[0].search_id
    elif request.GET.has_key('exp_id'):
        temp = request.GET['exp_id'].split('_')
        (type, exp_id, rank, repe) = (temp[0], int(
            temp[1]), int(temp[2]), int(temp[3]))
        search_id = Search.objects.filter(exp_id=exp_id).filter(
            rank=rank).filter(repeat_id=repe).filter(type='rep')[0].id
        # search_id = Protein.objects.filter(id=request.GET['protein_id'])[0].search_id
    type = Search.objects.filter(id=search_id)[0].type
    exp_id = Search.objects.filter(id=search_id)[0].exp_id
    if type == 'exp':
        rank = request.GET['rank'] if request.GET.has_key(
            'rank') else Search.objects.filter(exp_id=exp_id).filter(type='fraction')[0].rank
    elif type == 'rep':
        rank = request.GET['rank'] if request.GET.has_key(
            'rank') else Search.objects.filter(id=search_id)[0].rank
    pep = request.GET['pep_sequence']
    modi = request.GET['modification']
    searchs = Search.objects.filter(exp_id=exp_id).filter(
        rank=rank).filter(type='fraction').values('id')
    peps = Peptide.objects.filter(search_id__in=searchs).filter(
        sequence=pep).filter(modification=modi)
    pepList = []
    sre = set()
    sfr = set()
    inten = 0
    maxar = 0.000000000000000000000000001
    count = peps.count()
    for pep in peps:
        temp = {}
        ms2 = MS2.objects.filter(id=pep.ms2_id)[0]
        temp['id'] = ms2.id
        temp['rt'] = ms2.rt
        temp['pre_mz'] = ms2.pre_mz
        temp['ms2_scan'] = ms2.scan_num
        temp['search_id'] = ms2.search_id
        ms1 = MS1.objects.filter(ms2=ms2.id)[0]
        temp['ms1_scan'] = ms1.scan_num
        temp['ms1_rt'] = ms1.rt
        temp['intensity'] = ms1.intensity
        temp['area'] = pep.area
        temp['charge'] = pep.charge
        temp['sequence'] = pep.sequence
        temp['modification'] = pep.modification
        search = Search.objects.filter(id=ms2.search_id)[0]
        temp['rank'] = search.rank
        temp['repeat_id'] = search.repeat_id
        temp['fraction_id'] = search.fraction_id
        temp['rt_max'] = search.rt_max
        temp['filename'] = search.name
        if search.repeat_id not in sre:
            sre.add(search.repeat_id)
        if search.fraction_id not in sfr:
            sfr.add(search.fraction_id)
        if ms1.intensity > inten:
            inten = ms1.intensity
        if pep.area > maxar:
            maxar = pep.area
        pepList.append(temp)
    lre = list(sre)
    lre.sort()
    lfr = list(sfr)
    lfr.sort()
    plotList = []
    for out in pepList:
        out['xplot'] = out['rt'] / out['rt_max'] * \
            0.95 + lre.index(out['repeat_id'])
        out['yplot'] = out['intensity'] / inten * \
            0.95 + lfr.index(out['fraction_id'])
        out['rarea'] = out['area']
        out['area'] = out['rarea'] / maxar
        plotList.append(out)
    data = {"data": plotList, "total": count}
    result = json.dumps(data, cls=DjangoJSONEncoder)
    return HttpResponse(result)


def peptide_viwer(request):
    '''
    def peakCheck(peakFile,msLevel):
        if not os.path.isfile(peakFile):
            msAllFile       = ms_dir + '/' + request.GET['filename'] + '/' + 'MS%s.txt'%msLevel
            msAllFilePickle = ms_dir + '/' + request.GET['filename'] + '/' + 'MS%s.pkl'%msLevel
            if not os.path.isfile(msAllFilePickle):
                a1 = {}
                with open(msAllFile) as f:
                    for line in f:
                        line = line.strip().split(',')
                        ms_no, mz_temp, intensity_temp = int(line[0]), line[1],line[2]
                        if ms_no in a1:
                            a1[ms_no].append(mz_temp + ',' + intensity_temp)
                        else:
                            a1[ms_no] = [mz_temp + ',' + intensity_temp]

                f1 = file(msAllFilePickle, 'wb')  
                pickle.dump(a1, f1, True)
                f1.close()

            f2 = file(msAllFilePickle, 'rb')  
            a2 = pickle.load(f2)  
            f2.close()
            scan = request.GET['ms%s_scan'%msLevel] 

            peaks = a2[ int(scan) ]

            toWrite = ''
            for p in peaks:
                tmp = scan + ',' + p + '\n'
                toWrite += tmp


            fout=open(peakFile,'w')
            fout.write(toWrite)
            fout.close()

    '''
    def peakCheck(peakFile, peakFile_tmp, msLevel):
        if not os.path.isfile(peakFile):
            workingFile = peakFile_tmp
            if os.path.isfile(workingFile):
                return 0

            f = open(workingFile, 'w')
            f.close()

            scan = request.GET[
                'ms1_scan'] if msLevel == 1 else request.GET['ms2_scan']
            msAllFile = ms_dir + '/' + \
                request.GET['filename'] + '/' + 'MS%s.txt' % msLevel
            tmp = ''
            with open(msAllFile) as f:
                flag = 0
                for line in f:
                    if line.startswith(scan + ','):
                        tmp += line
                        flag = 1
                    elif flag:
                        break
            fout = open(peakFile, 'w')
            fout.write(tmp)
            fout.close()

            os.remove(workingFile)
            return 1
        else:
            return 1

    # ms_dir = '/usr/local/firmiana/galaxy-dist/database/files'
    fms1 = ms_dir + '/' + request.GET['filename'] + \
        '/' + request.GET['ms1_scan'] + '.txt'
    fms2 = ms_dir + '/' + request.GET['filename'] + \
        '/' + request.GET['ms2_scan'] + '.txt'

    fms1_tmp = '/tmp/' + request.GET['filename'] + \
        '_' + request.GET['ms1_scan'] + '.tmpeak'
    fms2_tmp = '/tmp/' + request.GET['filename'] + \
        '_' + request.GET['ms2_scan'] + '.tmpeak'

    if not peakCheck(fms1, fms1_tmp, 1):
        return HttpResponse('Still caching Spectrum Data ,Try later.')
    if not peakCheck(fms2, fms2_tmp, 2):
        return HttpResponse('Still caching Spectrum Data ,Try later.')
    sms1 = ""
    ms1list = {}
    for line in open(fms1):
        tr = line.strip().split(',')
        sms1 = sms1 + ',[' + tr[1] + ',' + tr[2] + ']'
        ms1list[tr[1]] = tr[2]
    sms1 = '[' + sms1[1:] + ']'
    sms2 = ""
    for line in open(fms2):
        tr = line.strip().split(',')
        sms2 = sms2 + ',[' + tr[1] + ',' + tr[2] + ']'
    sms2 = '[' + sms2[1:] + ']'
    # ms1_id = MS2.objects.filter(id=request.GET['id'])[0].ms1_id
    # ms2s = MS2.objects.filter(ms1_id=ms1_id)
    pre_mz = MS2.objects.get(id=request.GET['id']).pre_mz
    prms = ""
    for key, value in ms1list.iteritems():
        if (float(key) >= pre_mz * (1 - 10 / 1e6) and float(key) <= pre_mz * (1 + 10 / 1e6)):
            prms = prms + ',[' + str(key) + ',' + str(value) + ']'
    prms = '[' + prms[1:] + ']'
    context = {
        'charge': request.GET['charge'],
        'scanNum': request.GET['ms2_scan'],
        'sequence': request.GET['sequence'],
        'precursorMz': request.GET['pre_mz'],
        'ms1scanLabel': request.GET['ms1_scan'] + ' RT: ' + request.GET['ms1_rt'],
        'filename': request.GET['filename'],
        'precursorPeaks': prms,
        'ms1peaks': sms1,
        'ms2peaks': sms2,
        'staticMods': '[]'
    }
    return render(request, 'gardener/msviewer.html', context)


def venn_plot(request):
    def trans_pro(prolist):
        pros = set()
        for pro in prolist:
            pros.add(pro.accession)
        return pros

    def trans_pep(peplist):
        peps = set()
        for pep in peplist:
            peps.add(str(pep.sequence) + "_" + str(pep.modification))
        return peps

    type = request.GET['type']
    data = request.GET['data']
    inputs = data.split(',')
    out = ""
    if len(inputs) == 2:
        if type == 'repeat':
            paras = inputs[0].split('_')
            search1 = Search.objects.filter(repeat_id=paras[0]).filter(
                exp_id=paras[1]).filter(type='rep').values('id')
            name1 = Experiment.objects.filter(id=paras[1]).values('name')[0][
                'name'] + '_' + str(paras[0])
            pro1 = trans_pro(Repeat_Protein.objects.filter(
                search_id__in=search1).exclude(type=-1).distinct('accession'))
            pep1 = trans_pep(Repeat_Peptide.objects.filter(search_id__in=search1).exclude(
                type=-1).distinct('sequence', 'modification'))
            paras = inputs[1].split('_')
            search2 = Search.objects.filter(repeat_id=paras[0]).filter(
                exp_id=paras[1]).filter(type='rep').values('id')
            name2 = Experiment.objects.filter(id=paras[1]).values('name')[0][
                'name'] + '_' + str(paras[0])
            pro2 = trans_pro(Repeat_Protein.objects.filter(
                search_id__in=search2).exclude(type=-1).distinct('accession'))
            pep2 = trans_pep(Repeat_Peptide.objects.filter(search_id__in=search2).exclude(
                type=-1).distinct('sequence', 'modification'))
        else:
            search1 = Search.objects.filter(
                exp_id=inputs[0]).filter(type='exp').values('id')
            name1 = Experiment.objects.filter(
                id=inputs[0]).values('name')[0]['name']
            pro1 = trans_pro(Exp_Protein.objects.filter(
                search_id=search1).exclude(type=-1).distinct('accession'))
            pep1 = trans_pep(Exp_Peptide.objects.filter(search_id=search1).exclude(
                type=-1).distinct('sequence', 'modification'))
            search2 = Search.objects.filter(
                exp_id=inputs[1]).filter(type='exp').values('id')
            name2 = Experiment.objects.filter(
                id=inputs[1]).values('name')[0]['name']
            pro2 = trans_pro(Exp_Protein.objects.filter(
                search_id=search2).exclude(type=-1).distinct('accession'))
            pep2 = trans_pep(Exp_Peptide.objects.filter(search_id=search2).exclude(
                type=-1).distinct('sequence', 'modification'))

        venng = importr('VennDiagram')
        venn2 = ro.r['draw.pairwise.venn']
        grid_draw = ro.r['grid.draw']
        dev_off = ro.r['dev.off']
        ro.r.setwd(tmpdir)
        prooutfile = 'venn_pro' + str(time.time()) + '.png'
        ro.r.png(filename=prooutfile, bg="transparent")
        grid_draw(venn2(
            area1=len(pro1),
            area2=len(pro2),
            cross_area=len(pro1 & pro2),
            category=ro.StrVector(['pro_' + name1, 'pro_' + name2]),
            fill=ro.StrVector(['#FF6342', '#ADDE63']),
            cat_col=ro.StrVector(['#FF6342', '#ADDE63']),
            lty='blank',
            cex=2,
            cat_cex=2,
            cat_pos=ro.IntVector([-20, 20]),
            cat_dist=0.05,
            ext_pos=30,
            ext_dist=-0.05,
            ext_length=0.85,
            ext_line_lwd=2,
            ext_line_lty="dashed"
        ))
        dev_off()
        out = '/static/images/tmp/{}'.format(
            prooutfile)
        pepoutfile = 'venn_pep' + str(time.time()) + '.png'
        ro.r.png(filename=pepoutfile, bg="transparent")
        grid_draw(venn2(
            area1=len(pep1),
            area2=len(pep2),
            cross_area=len(pep1 & pep2),
            category=ro.StrVector(['pep_' + name1, 'pep_' + name2]),
            fill=ro.StrVector(['#FF6342', '#ADDE63']),
            cat_col=ro.StrVector(['#FF6342', '#ADDE63']),
            lty='blank',
            cex=2,
            cat_pos=ro.IntVector([-20, 20]),
            cat_cex=2,
            cat_dist=0.05,
            ext_pos=30,
            ext_dist=-0.05,
            ext_length=0.85,
            ext_line_lwd=2,
            ext_line_lty="dashed"
        ))
        dev_off()
        out = out + ',' + '/static/images/tmp/{}'.format(pepoutfile)
    elif len(inputs) == 3:
        if type == 'repeat':
            paras = inputs[0].split('_')
            search1 = Search.objects.filter(repeat_id=paras[0]).filter(
                exp_id=paras[1]).filter(type='rep').values('id')
            name1 = Experiment.objects.filter(id=paras[1]).values('name')[0][
                'name'] + '_' + str(paras[0])
            pro1 = trans_pro(Repeat_Protein.objects.filter(
                search_id__in=search1).exclude(type=-1).distinct('accession'))
            pep1 = trans_pep(Repeat_Peptide.objects.filter(search_id__in=search1).exclude(
                type=-1).distinct('sequence', 'modification'))
            paras = inputs[1].split('_')
            search2 = Search.objects.filter(repeat_id=paras[0]).filter(
                exp_id=paras[1]).filter(type='rep').values('id')
            name2 = Experiment.objects.filter(id=paras[1]).values('name')[0][
                'name'] + '_' + str(paras[0])
            pro2 = trans_pro(Repeat_Protein.objects.filter(
                search_id__in=search2).exclude(type=-1).distinct('accession'))
            pep2 = trans_pep(Repeat_Peptide.objects.filter(search_id__in=search2).exclude(
                type=-1).distinct('sequence', 'modification'))
            paras = inputs[2].split('_')
            search3 = Search.objects.filter(repeat_id=paras[0]).filter(
                exp_id=paras[1]).filter(type='rep').values('id')
            name3 = Experiment.objects.filter(id=paras[1]).values('name')[0][
                'name'] + '_' + str(paras[0])
            pro3 = trans_pro(Repeat_Protein.objects.filter(
                search_id__in=search3).exclude(type=-1).distinct('accession'))
            pep3 = trans_pep(Repeat_Peptide.objects.filter(search_id__in=search3).exclude(
                type=-1).distinct('sequence', 'modification'))
        else:
            search1 = Search.objects.filter(
                exp_id=inputs[0]).filter(type='exp').values('id')
            name1 = Experiment.objects.filter(
                id=inputs[0]).values('name')[0]['name']
            pro1 = trans_pro(Exp_Protein.objects.filter(
                search_id=search1).exclude(type=-1).distinct('accession'))
            pep1 = trans_pep(Exp_Peptide.objects.filter(search_id=search1).exclude(
                type=-1).distinct('sequence', 'modification'))
            search2 = Search.objects.filter(
                exp_id=inputs[1]).filter(type='exp').values('id')
            name2 = Experiment.objects.filter(
                id=inputs[1]).values('name')[0]['name']
            pro2 = trans_pro(Exp_Protein.objects.filter(
                search_id=search2).exclude(type=-1).distinct('accession'))
            pep2 = trans_pep(Exp_Peptide.objects.filter(search_id=search2).exclude(
                type=-1).distinct('sequence', 'modification'))
            search3 = Search.objects.filter(
                exp_id=inputs[2]).filter(type='exp').values('id')
            name3 = Experiment.objects.filter(
                id=inputs[2]).values('name')[0]['name']
            pro3 = trans_pro(Exp_Protein.objects.filter(
                search_id=search3).exclude(type=-1).distinct('accession'))
            pep3 = trans_pep(Exp_Peptide.objects.filter(search_id=search3).exclude(
                type=-1).distinct('sequence', 'modification'))
        venng = importr('VennDiagram')
        venn3 = ro.r['draw.triple.venn']
        grid_draw = ro.r['grid.draw']
        dev_off = ro.r['dev.off']
        ro.r.setwd(tmpdir)
        prooutfile = 'venn_pro' + str(time.time()) + '.png'
        ro.r.png(filename=prooutfile, bg="transparent")
        grid_draw(venn3(
            area1=len(pro1),
            area2=len(pro2),
            area3=len(pro3),
            n12=len(pro1 & pro2),
            n23=len(pro2 & pro3),
            n13=len(pro1 & pro3),
            n123=len(pro1 & pro2 & pro3),
            category=ro.StrVector(
                ['pro_' + name1, 'pro_' + name2, 'pro_' + name3]),
            fill=ro.StrVector(['#FF6342', '#ADDE63', '#63C6DE']),
            cat_col=ro.StrVector(['#FF6342', '#ADDE63', '#63C6DE']),
            lty='blank',
            cex=2,
            cat_pos=ro.IntVector([-20, 20, 180]),
            cat_cex=2,
            cat_dist=0.05,
            ext_pos=30,
            ext_dist=-0.05,
            ext_length=0.85,
            ext_line_lwd=2,
            ext_line_lty="dashed"
        ))
        dev_off()
        out = '/static/images/tmp/{}'.format(
            prooutfile)
        pepoutfile = 'venn_pep' + str(time.time()) + '.png'
        ro.r.png(filename=pepoutfile, bg="transparent")
        grid_draw(venn3(
            area1=len(pep1),
            area2=len(pep2),
            area3=len(pep3),
            n12=len(pep1 & pep2),
            n23=len(pep2 & pep3),
            n13=len(pep1 & pep3),
            n123=len(pep1 & pep2 & pep3),
            category=ro.StrVector(
                ['pep_' + name1, 'pep_' + name2, 'pep_' + name3]),
            fill=ro.StrVector(['#FF6342', '#ADDE63', '#63C6DE']),
            cat_col=ro.StrVector(['#FF6342', '#ADDE63', '#63C6DE']),
            lty='blank',
            cex=2,
            cat_pos=ro.IntVector([-20, 20, 180]),
            cat_cex=2,
            cat_dist=0.05,
            ext_pos=30,
            ext_dist=-0.05,
            ext_length=0.85,
            ext_line_lwd=2,
            ext_line_lty="dashed"
        ))
        dev_off()
        out = out + ',' + '/static/images/tmp/{}'.format(pepoutfile)
    elif len(inputs) == 4:
        if type == 'repeat':
            paras = inputs[0].split('_')
            search1 = Search.objects.filter(repeat_id=paras[0]).filter(
                exp_id=paras[1]).filter(type='rep').values('id')
            name1 = Experiment.objects.filter(id=paras[1]).values('name')[0][
                'name'] + '_' + str(paras[0])
            pro1 = trans_pro(Repeat_Protein.objects.filter(
                search_id__in=search1).exclude(type=-1).distinct('accession'))
            pep1 = trans_pep(Repeat_Peptide.objects.filter(search_id__in=search1).exclude(
                type=-1).distinct('sequence', 'modification'))

            paras = inputs[1].split('_')
            search2 = Search.objects.filter(repeat_id=paras[0]).filter(
                exp_id=paras[1]).filter(type='rep').values('id')
            name2 = Experiment.objects.filter(id=paras[1]).values('name')[0][
                'name'] + '_' + str(paras[0])
            pro2 = trans_pro(Repeat_Protein.objects.filter(
                search_id__in=search2).exclude(type=-1).distinct('accession'))
            pep2 = trans_pep(Repeat_Peptide.objects.filter(search_id__in=search2).exclude(
                type=-1).distinct('sequence', 'modification'))

            paras = inputs[2].split('_')
            search3 = Search.objects.filter(repeat_id=paras[0]).filter(
                exp_id=paras[1]).filter(type='rep').values('id')
            name3 = Experiment.objects.filter(id=paras[1]).values('name')[0][
                'name'] + '_' + str(paras[0])
            pro3 = trans_pro(Repeat_Protein.objects.filter(
                search_id__in=search3).exclude(type=-1).distinct('accession'))
            pep3 = trans_pep(Repeat_Peptide.objects.filter(search_id__in=search3).exclude(
                type=-1).distinct('sequence', 'modification'))

            paras = inputs[3].split('_')
            search4 = Search.objects.filter(repeat_id=paras[0]).filter(
                exp_id=paras[1]).filter(type='rep').values('id')
            name4 = Experiment.objects.filter(id=paras[1]).values('name')[0][
                'name'] + '_' + str(paras[0])
            pro4 = trans_pro(Repeat_Protein.objects.filter(
                search_id__in=search4).exclude(type=-1).distinct('accession'))
            pep4 = trans_pep(Repeat_Peptide.objects.filter(search_id__in=search4).exclude(
                type=-1).distinct('sequence', 'modification'))

        else:
            search1 = Search.objects.filter(
                exp_id=inputs[0]).filter(type='exp').values('id')
            name1 = Experiment.objects.filter(
                id=inputs[0]).values('name')[0]['name']
            pro1 = trans_pro(Exp_Protein.objects.filter(
                search_id=search1).exclude(type=-1).distinct('accession'))
            pep1 = trans_pep(Exp_Peptide.objects.filter(search_id=search1).exclude(
                type=-1).distinct('sequence', 'modification'))

            search2 = Search.objects.filter(
                exp_id=inputs[1]).filter(type='exp').values('id')
            name2 = Experiment.objects.filter(
                id=inputs[1]).values('name')[0]['name']
            pro2 = trans_pro(Exp_Protein.objects.filter(
                search_id=search2).exclude(type=-1).distinct('accession'))
            pep2 = trans_pep(Exp_Peptide.objects.filter(search_id=search2).exclude(
                type=-1).distinct('sequence', 'modification'))

            search3 = Search.objects.filter(
                exp_id=inputs[2]).filter(type='exp').values('id')
            name3 = Experiment.objects.filter(
                id=inputs[2]).values('name')[0]['name']
            pro3 = trans_pro(Exp_Protein.objects.filter(
                search_id=search3).exclude(type=-1).distinct('accession'))
            pep3 = trans_pep(Exp_Peptide.objects.filter(search_id=search3).exclude(
                type=-1).distinct('sequence', 'modification'))

            search4 = Search.objects.filter(
                exp_id=inputs[3]).filter(type='exp').values('id')
            name4 = Experiment.objects.filter(
                id=inputs[3]).values('name')[0]['name']
            pro4 = trans_pro(Exp_Protein.objects.filter(
                search_id=search4).exclude(type=-1).distinct('accession'))
            pep4 = trans_pep(Exp_Peptide.objects.filter(search_id=search4).exclude(
                type=-1).distinct('sequence', 'modification'))

        venng = importr('VennDiagram')
        venn4 = ro.r['draw.quad.venn']
        grid_draw = ro.r['grid.draw']
        dev_off = ro.r['dev.off']
        ro.r.setwd(tmpdir)
        prooutfile = 'venn_pro' + str(time.time()) + '.png'
        ro.r.png(filename=prooutfile, bg="transparent")
        grid_draw(venn4(
            area1=len(pro1),
            area2=len(pro2),
            area3=len(pro3),
            area4=len(pro4),
            n12=len(pro1 & pro2),
            n13=len(pro1 & pro3),
            n14=len(pro1 & pro4),
            n23=len(pro2 & pro3),
            n24=len(pro2 & pro4),
            n34=len(pro3 & pro4),
            n123=len(pro1 & pro2 & pro3),
            n124=len(pro1 & pro2 & pro4),
            n134=len(pro1 & pro3 & pro4),
            n234=len(pro2 & pro3 & pro4),
            n1234=len(pro1 & pro2 & pro3 & pro4),
            category=ro.StrVector([name1, name2, name3, name4]),
            fill=ro.StrVector(['#FF6342', '#00FF63', '#63C6DE', '#FFFF00']),
            cat_col=ro.StrVector(['#000000', '#000000', '#000000', '#000000']),
            lty='blank',
            cex=1.3,
            # cat_pos=ro.IntVector([-45, -20, 20, 45]),
            cat_cex=1.5,
            cat_dist=ro.FloatVector([0.2, 0.2, 0.1, 0.1]),
            ext_pos=30,
            ext_dist=-0.05,
            ext_length=0.85,
            ext_line_lwd=2,
            ext_line_lty="dashed"
        ))
        dev_off()
        out = '/static/images/tmp/{}'.format(
            prooutfile)
        pepoutfile = 'venn_pep' + str(time.time()) + '.png'
        ro.r.png(filename=pepoutfile, bg="transparent")
        grid_draw(venn4(
            area1=len(pep1),
            area2=len(pep2),
            area3=len(pep3),
            area4=len(pep4),
            n12=len(pep1 & pep2),
            n13=len(pep1 & pep3),
            n14=len(pep1 & pep4),
            n23=len(pep2 & pep3),
            n24=len(pep2 & pep4),
            n34=len(pep3 & pep4),
            n123=len(pep1 & pep2 & pep3),
            n124=len(pep1 & pep2 & pep4),
            n134=len(pep1 & pep3 & pep4),
            n234=len(pep2 & pep3 & pep4),
            n1234=len(pep1 & pep2 & pep3 & pep4),
            category=ro.StrVector([name1, name2, name3, name4]),
            fill=ro.StrVector(['#FF6342', '#00FF63', '#63C6DE', '#FFFF00']),
            cat_col=ro.StrVector(['#000000', '#000000', '#000000', '#000000']),
            lty='blank',
            cex=1.3,
            # cat_pos=ro.IntVector([-30, 30, -20, 20]),
            cat_cex=1.5,
            cat_dist=ro.FloatVector([0.2, 0.2, 0.1, 0.1]),
            ext_pos=30,
            ext_dist=-0.05,
            ext_length=0.85,
            ext_line_lwd=2,
            ext_line_lty="dashed"
        ))
        dev_off()
        out = out + ',' + '/static/images/tmp/{}'.format(pepoutfile)

    return HttpResponse(out)


def rplot(request):
    outtest = "Hello World!"
    variables = RequestContext(request, {'outtest': outtest})

    def report_state():
        yield "Start Data initialization:"
        para = request.GET.get('paras')
        yield "OK!<br/>Run Statistics:<br/>"
        cmd = "Rscript "
        script = '/usr/local/firmiana/leafy/gardener/scripts/R/pca.R '
        outputfile = str(time.time()) + 'pca'
        paras = '--args output=' + outputfile
        code = str(cmd + script + paras)
        yield code + '<br/>'
        (status, output) = commands.getstatusoutput(code)
        if status != 0:
            yield "Output:<br/>" + str(output)
            yield '<br/><img src="/static/images/tmp/1374933054.35pcaline1.png" height="500" width="500" alt="PCA-plot"/>'
            yield '<br/><br/><img src="/static/images/tmp/1374933054.35pcaline2.png" height="500" width="500" alt="PCA-plot"/>'
            yield '<br/><br/><img src="/static/images/tmp/1374933054.35pcaline3.png" height="500" width="500" alt="PCA-plot"/>'
        else:
            yield '<br/><img src="/static/images/tmp/pca_tmp/' + outputfile + ' line1.png"  alt="PCA-plot"/>'
    return HttpResponse(report_state())


def polyfit(x, y, degree):  # calc r-square
    results = {}
    coeffs = numpy.polyfit(x, y, degree)
    # Polynomial Coefficients
    results['polynomial'] = coeffs.tolist()
    results['degree'] = degree
    # r-squared
    p = numpy.poly1d(coeffs)
    # fit values, and mean
    yhat = p(x)  # or [p(z) for z in x]
    ybar = numpy.sum(y) / len(y)  # or sum(y)/len(y)
    # or sum([ (yihat - ybar)**2 for yihat in yhat])
    ssreg = numpy.sum((yhat - ybar) ** 2)
    sstot = numpy.sum((y - ybar) ** 2)  # or sum([ (yi - ybar)**2 for yi in y])
    results['determination'] = ssreg / sstot
    return results


def mean_movement(input_data, window):
    if window % 2 != 1:
        raise Exception, "'mean_movement' function needs an odd window length"
    if window > (len(input_data)) + 2:
        raise Exception, "'mean_movement' function: input data too short"
    input_data = list(input_data)
    output_data = []
    length = len(input_data)
    n = (window - 1) / 2
    input_data2 = ([input_data[0]] * n) + list(input_data) + \
        ([input_data[length - 1]] * (n + 1))
    _sum = 0.0
    for i in xrange(0, window):
        _sum += input_data2[i]
    w = float(window)
    for i in xrange(n, n + length):
        output_data.append(_sum / window)
        _sum -= input_data2[i - n]
        _sum += input_data2[i + n + 1]
    return output_data


def _mean_movement_only_python(data, m):
    if m > (2 * len(data)) + 2:
        return data
    input_array = list(data)
    output_array = list(data)
    mean_factor = (2 * m) + 1
    length = len(data)
    # Process data from the middle
    for i in xrange(m, length - m):
        _sum = 0
        for j in xrange(i - m, i + m):
            _sum += input_array[j]
        output_array[i] = _sum / mean_factor
    # Process data from the beginning
    window = 1
    for i in xrange(1, m):
        _sum = 0
        for j in xrange(i - window, i + window):
            _sum += input_array[j]
        output_array[i] = _sum / ((2 * window) + 1)
        window += 1
    output_array[0] = input_array[0]
    # Process data from the end
    window = 1
    for i in reversed(xrange(length - m, length - 1)):
        _sum = 0
        for j in xrange(i - window, i + window):
            _sum += input_array[j]
        output_array[i] = _sum / ((2 * window) + 1)
        window += 1
    output_array[length - 1] = input_array[length - 1]
    del input_array
    return output_array


def sgolay(p, n):
    if n % 2 != 1:
        raise Exception, "'sgolay' function needs an odd filter length n"
    elif p >= n:
        raise Exception, "'sgolay' function needs filter length n larger than polynomial order p"
    k = int(n / 2)
    F = zeros((n, n), float32)
    for row in range(1, k + 2):
        # A = pinv( ( [(1:n)-row]'*ones(1,p+1) ) .^ ( ones(n,1)*[0:p] ) );
        left = dot(reshape(arange(1, n + 1) - row, (-1, 1)), ones((1, p + 1)))
        right = repeat([range(0, p + 1)], n, 0)
        # A = generalized_inverse( left**right )
        A = pinv(left ** right)
        # F(row,:) = A(1,:);
        put(F.ravel(), add(arange(n), n * (row - 1)), A[0])

        # F(k+2:n,:) = F(k:-1:1,n:-1:1);
    for fila in range(k + 1, n):
        put(F.ravel(), add(arange(n), n * fila), F[n - 1 - fila][::-1])
    return F


def sgolayfilt(x, p, n):
    x = array(x, float32).ravel()
    size = len(x)
    if size < n:
        raise Exception, "'sgolayfilt': insufficient data for filter"
    # # The first k rows of F are used to filter the first k points
    # # of the data set based on the first n points of the data set.
    # # The last k rows of F are used to filter the last k points
    # # of the data set based on the last n points of the dataset.
    # # The remaining data is filtered using the central row of F.
    F = sgolay(p, n)
    k = int(n / 2)
    # z = filter(F(k+1,:), 1, x);
    z = lfilter(F[k], 1, x)
    # y = [ F(1:k,:)*x(1:n,:) ; z(n:len,:) ; F(k+2:n,:)*x(len-n+1:len,:) ];
    left = dot(take(F, arange(k), 0), take(x, arange(n), 0))
    right = dot(take(F, arange(k + 1, n), 0),
                take(x, arange(size - n, size), 0))
    middle = take(z, arange(n - 1, size))
    return concatenate((left, middle, right))


def divfind(a, b):
    head = 0
    tail = len(a) - 1
    while head <= tail:
        mid = (head + tail) / 2
        if a[mid]['mz_temp'] < b:
            head = mid + 1
        else:
            tail = mid - 1
    return head


def calc(exp, expList, cmtable, pepFraction, FID, PepNum, allpep, dRT, dMz, ProTable, proListForIndex):
    connection.close()
    RtList = []
    DataBase = []
    filename = Search.objects.get(id=expList[exp]).name
    dir = ms_dir + '/' + filename + '/'
    files = os.listdir(dir)
    filedict = {}
    i = 0
    fileLength = len(files)
    tmp_ms1files = MS1.objects.filter(search__id=expList[exp])
    ms1files = []
    for ms1file in tmp_ms1files:
        ms1files.append(ms1file.scan_num)
    for file in files:
        tt = []
        ms1name = int(file.split('.')[0])
        if ms1name not in ms1files:
            continue
        filedict[ms1name] = i
        i = i + 1
        f = open(dir + file, 'r')
        for line in f:
            (ms_no, mz_temp, intensity_temp) = line.split(',')
            temp = {}
            temp['ms_id'] = int(ms_no)
            temp['mz_temp'] = float(mz_temp)
            temp['intensity_temp'] = float(intensity_temp)
            tt.append(temp)
        f.close()
        DataBase.append(tt)
    for pep in range(PepNum):
        if cmtable[pep] == '':
            continue
        if cmtable[pep]['complete'] == False or (pep not in pepFraction[FID[expList[exp]]]):
            if pep not in pepFraction[FID[expList[exp]]]:
                cmtable[pep]['area'] = 'None'
            continue
        QuantTable = []
        RTList = []
        IDTable = []
        mz = allpep[pep]['mz']
        tempMS1 = MS1.objects.filter(search_id=expList[exp]).filter(rt__lt=cmtable[pep][
            'rt'] + dRT).filter(rt__gt=cmtable[pep]['rt'] - dRT).order_by('rt')
        if len(tempMS1) == 0:
            cmtable[pep]['area'] = 0
        else:
            temp_num = 0
            for tMS1 in tempMS1:
                temp_num = temp_num + 1
                best = 0
                id = filedict[int(tMS1.scan_num)]
                if (mz * (1 - dMz / 1e6) > DataBase[id][len(DataBase[id]) - 1]['mz_temp'] or mz * (1 + dMz / 1e6) < DataBase[id][0]['mz_temp']):
                    p = []
                else:
                    head = divfind(DataBase[id], mz * (1 - dMz / 1e6))
                    tail = divfind(DataBase[id], mz * (1 + dMz / 1e6))
                    p = [k['intensity_temp'] for k in DataBase[id][head:tail]]
                    # p = DataBase[id][head:tail + 1]['intensity_temp']
                # p = [k['intensity_temp'] for k in DataBase[id] if k['mz_temp'] > mz * (1 - dMz / 1e6) and k['mz_temp'] < mz * (1 + dMz / 1e6)]
                if len(p) == 0:
                    cmtable[pep]['area'] = 0
                    continue
                else:
                    best = max(best, max(p))
                    if best == 0:
                        cmtable[pep]['area'] = 0
                        continue
                    else:
                        QuantTable.append(best)
                        RTList.append(tMS1.rt)
                        IDTable.append(temp_num)
            if len(QuantTable) == 0:
                cmtable[pep]['area'] = 0
                continue
            else:
                index = QuantTable.index(max(QuantTable))
                length = len(QuantTable)
                left = 0
                for i in range(index, 0, -1):
                    if IDTable[i] - IDTable[i - 1] > 3:
                        left = i
                right = length - 1
                for i in range(index + 1, length):
                    if IDTable[i] - IDTable[i - 1] > 3:
                        right = i
                QuantTable = QuantTable[left:right]
                RTList = RTList[left:right]
                length = len(QuantTable)
                if length <= 3:
                    area = 0
                else:
                    F = min(7, length - length % 2 - 1)
                    SG_Processed_XIC = sgolayfilt(QuantTable, 2, F)
                    area = numpy.trapz(SG_Processed_XIC, RTList)
                    # area=numpy.trapz(SG_Processed_XIC,rtlist)
                cmtable[pep]['area'] = area
                cmtable[pep]['mz'] = mz
    for pep in cmtable:
        if pep != '':
            temp = len(pep['protein_group_accessions'])
            for accession in pep['protein_group_accessions']:
                ProTable[exp][proListForIndex[accession]] += pep['area'] / temp
    ans = (cmtable, ProTable[exp])
    connection.close()
    f = open('/usr/local/firmiana/leafy/gardener/test/test1.txt', 'a')
    f.write(str(datetime.datetime.now().strftime(
        '%Y-%m-%d %H:%M:%S')) + 'exp_ca=' + str(exp) + '\n')
    f.close()
    return ans


def mecompare(request):
    # expList= json.load(request.GET['expList'])
    def getParam():
        try:
            expList = request.GET['sid']
        except:
            expList = ''
        try:
            start = int(request.GET['start'])
        except:
            start = ''
        try:
            limit = int(request.GET['limit'])
        except:
            limit = ''
        try:
            dRT = float(request.GET['dRT'])
        except:
            dRT = 60
        try:
            dMz = float(request.GET['dMz'])
        except:
            dMz = 10
        try:
            ionscore = float(request.GET['ionscore'])
        except:
            ionscore = 30
        try:
            compare = request.GET['compare']
            if compare == 'true':
                compare = True
            else:
                compare = False
        except:
            compare = False
        try:
            ppt = request.GET['pp']
        except:
            ppt = '2'
        try:
            tree = request.GET['tree']
        except:
            tree = 2
        try:  # direciton means reverse or not
            sort = json.loads(str(request.GET['sort'])[1:-1])
            property = sort['property']
            if sort['direction'] == 'DESC':
                direction = True
            else:
                direction = False
        except:
            property = "accessions"
            direction = False
        try:
            filters = json.loads(request.GET['filter'])
        except:
            filters = []
        return (expList, dRT, dMz, ionscore, compare, start, limit, ppt, property, direction, tree, filters)

    def getExpList(expList, Search2Exp):
        expList = expList.split(',')[:-1]
        f = open('/usr/local/firmiana/leafy/gardener/test/test1.txt', 'a')
        f.write(str(datetime.datetime.now().strftime(
            '%Y-%m-%d %H:%M:%S')) + str(expList) + 'begin \n')
        f.close()
        templist = []
        i = 0
        j = 0
        allexp = []
        delList = []
        for exp in expList:
            temp = exp.split('_')
            (type, exp_id, rank, repe) = (temp[0], int(
                temp[1]), int(temp[2]), int(temp[3]))
            if type == 'exp':
                delList.append(exp)
                Rep = Search.objects.filter(exp_id=exp_id).filter(type='rep')
                for rr in Rep:
                    tempstring = str('repeat') + '_' + str(rr.exp_id) + \
                        '_' + str(rr.rank) + '_' + str(rr.repeat_id)
                    expList.append(tempstring)
        for dd in delList:
            expList.remove(dd)
        expList = list(set(expList))
        ansList = expList
        f = open('/usr/local/firmiana/leafy/gardener/test/test1.txt', 'a')
        f.write(str(datetime.datetime.now().strftime(
            '%Y-%m-%d %H:%M:%S')) + str(expList) + 'begin \n')
        f.close()
        for exp in expList:
            temp = exp.split('_')
            (type, exp_id, rank, repe) = (temp[0], int(
                temp[1]), int(temp[2]), int(temp[3]))
            ExpName = Experiment.objects.get(id=exp_id).name
            allexp.append(ExpName)
            if type == 'repeat':
                SearchList = Search.objects.filter(exp_id=exp_id).filter(
                    repeat_id=repe).filter(rank=rank).filter(type='fraction')
            elif type == 'exp':
                SearchList = Search.objects.filter(
                    exp_id=exp_id).filter(type='fraction')
            for search in SearchList:
                templist.append(search.id)
                Search2Exp[j] = i
                j = j + 1
            i = i + 1
        allexp = list(set(allexp))
        allrep = [[]for row in range(len(allexp))]
        for exp in expList:
            temp = exp.split('_')
            (exp1, rank, repe) = (temp[1], temp[2], temp[3])
            ExpName = Experiment.objects.get(id=exp1).name
            idx = allexp.index(ExpName)
            allrep[idx].append(exp)
        return (templist, Search2Exp, allexp, allrep, ansList)

    def getCsvName(expList, dRT, dMz, ionscore, compare):
        CsvName = ''
        expList.sort()
        for exp in expList:
            CsvName = CsvName + str(exp) + '_'
        # CsvName = CsvName + '&dRT=' + str(dRT) + '&dMz=' + str(dMz) + '&compare=' + str(compare)
        (xtable, sign) = XsearchTable.objects.get_or_create(dmz=dMz,
                                                            drt=dRT,
                                                            ionscore=ionscore,
                                                            searchs=CsvName,
                                                            ProGene='protein',
                                                            compare=compare,
                                                            user='hzqnq'
                                                            )
        xtable.save()
        CsvName = str(xtable.id)
        ProFileName = quant_dir + CsvName + '.protab'
        CsvName = quant_dir + CsvName + '.tab'
        return (CsvName, ProFileName)

    def getPep(expList):
        for exp in expList:
            peplist = Peptide.objects.filter(ms2__search__id=exp).filter(
                ion_score__gt=10).exclude(type=-1)
            for pep in peplist:
                dic[pep.sequence] = pep.ms2.pre_mz
        for key, value in dic.iteritems():
            temp = {}
            temp['pep'] = key
            temp['mz'] = value
            allpep.append(temp)
        Pep2Num = {}
        i = 0
        for pep in allpep:
            Pep2Num[pep['pep']] = i
            i = i + 1

        pepFraction = [[] for row in range(MaxFraction + 1)]
        for exp in expList:
            temp = Search.objects.get(id=exp).fraction_id
            peplist = Peptide.objects.filter(ms2__search__id=exp).filter(
                ion_score__gt=10).exclude(type=-1)
            for pep in peplist:
                pepFraction[temp].append(Pep2Num[pep.sequence])
            pepFraction[temp] = list(set(pepFraction[temp]))
        return (allpep, Pep2Num, pepFraction)

    def getCmtable(ExpNum, expList, Pep2Num):
        allProtein = []
        cmtable = [['' for col in range(PepNum)] for row in range(
            ExpNum + 1)]  # compare all peptide information
        for exp in range(ExpNum):
            pp = []
            peplist = Peptide.objects.filter(ms2__search__id=expList[exp]).filter(
                ion_score__gt=10).exclude(type=-1)
            for pep in peplist:
                num = Pep2Num[pep.sequence]
                if cmtable[exp][num] == '' or cmtable[exp][num]['ionscore'] < pep.ion_score:
                    temp = {}
                    temp['rt'] = pep.ms2.rt
                    temp['complete'] = False
                    temp['ionscore'] = pep.ion_score
                    temp['pep'] = pep.sequence
                    temp['area'] = pep.area
                    temp['num_psms'] = pep.num_psms
                    temp['num_proteins'] = pep.num_proteins
                    temp['protein_group_accessions'] = pep.protein_group_accessions.split(
                        ';')
                    for kk in pep.protein_group_accessions.split(';'):
                        if kk not in allProtein:
                            allProtein.append(kk)
                    cmtable[exp][num] = temp
        Symbol = []
        Description = []
        for pp in allProtein:
            pro = Protein.objects.filter(accession=pp).exclude(type=-1)
            if len(pro) != 0:
                pro = pro[0]
                Symbol.append(pro.symbol)
                Description.append(pro.description)
            else:
                Symbol.append('')
                Description.append('')
        return (cmtable, allProtein, Symbol, Description)

    def getRTtable(stdtable):
        rttable = []
        f = open('/usr/local/firmiana/leafy/gardener/test/test1.txt', 'a')
        f.write(str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    ) + str(ExpNum) + '\t' + str(PepNum) + 'rttable is \n')
        f.close()
        for exp1 in range(ExpNum):
            ep = []
            for exp2 in range(ExpNum):
                rt1 = []
                rt2 = []
                if exp1 != exp2:
                    for pep in range(PepNum):
                        if stdtable[exp1][pep] != '' and stdtable[exp2][pep] != '':
                            rt1.append(stdtable[exp1][pep]['rt'])
                            rt2.append(stdtable[exp2][pep]['rt'])
                    if len(rt1) != 0:
                        calc1 = polyfit(rt1, rt2, 1)
                        calc2 = polyfit(rt1, rt2, 2)
                        if calc1['determination'] > calc2['determination']:
                            ep.append(calc1)
                        else:
                            ep.append(calc2)
                    else:
                        ep.append('')

                else:
                    ep.append('')
            rttable.append(ep)
        return rttable

    def getStdtable(cmtable):
        stdtable = []  # Create a standard for rt reg
        for exp in cmtable:
            pp = []
            for pep in exp:
                if pep == '' or pep['ionscore'] < 10:
                    pp.append('')
                else:
                    pp.append(pep)
            stdtable.append(pp)
        return stdtable

    def RTComplete(cmtable):
        for exp in range(ExpNum):
            for pep in range(PepNum):
                if cmtable[exp][pep] == '':
                    for exp2 in range(ExpNum):
                        if exp != exp2 and FID[expList[exp]] == FID[expList[exp2]] and rttable[exp][exp2] != '' and cmtable[exp2][pep] != '' and cmtable[exp2][pep]['rt'] != '':
                            # temprt=np.polyval([1,2,3],cmtable[exp2][pep]['rt'])
                            temprt = np.polyval(rttable[exp][exp2][
                                                'polynomial'], cmtable[exp2][pep]['rt'])
                            temp = {}
                            temp['rt'] = temprt
                            temp['complete'] = True
                            temp['ionscore'] = cmtable[exp2][pep]['ionscore']
                            temp['pep'] = cmtable[exp2][pep]['pep']
                            temp['num_psms'] = cmtable[exp2][pep]['num_psms']
                            temp['num_proteins'] = cmtable[
                                exp2][pep]['num_proteins']
                            temp['protein_group_accessions'] = cmtable[
                                exp2][pep]['protein_group_accessions']
                            cmtable[exp][pep] = temp
                            break
        return cmtable

    def GroupFraction(expList):
        xList = []
        MaxFraction = 0
        for exp in expList:
            tempSearch = Search.objects.get(id=exp)
            if tempSearch.fraction_id > MaxFraction:
                MaxFraction = tempSearch.fraction_id
            temp = {}
            temp['ID'] = exp
            temp['exp_id'] = tempSearch.exp_id
            temp['reaeat_id'] = tempSearch.repeat_id
            temp['type'] = tempSearch.type
            temp['rank'] = tempSearch.rank
            temp['fraction_id'] = tempSearch.fraction_id
            FID[exp] = tempSearch.fraction_id
            xList.append(temp)
        GroupE = [[]for row in range(MaxFraction + 1)]
        for exp in expList:
            GroupE[FID[exp]].append(exp)
        return (xList, GroupE, MaxFraction)

    def change(a, b):
        lista = a
        listb = b
        lista.extend(b)
        lista = list(set(a))
        return lista

    f = open('/usr/local/firmiana/leafy/gardener/test/test1.txt', 'w')
    f.write(str(datetime.datetime.now().strftime(
        '%Y-%m-%d %H:%M:%S')) + 'begin \n')
    f.close()
    # return HttpResponse('12345')
    expList = ''
    dRT = 60
    dMz = 10
    compare = False
    (expList, dRT, dMz, ionscore, compare, start, limit,
     ppt, property, direction, tree, filters) = getParam()

    Search2Exp = {}
    (expList, Search2Exp, allexp, allrep, ansList) = getExpList(expList, Search2Exp)
    newExpNum = len(ansList)
    CsvName = ''
    (CsvName, ProFileName) = getCsvName(expList, dRT, dMz, ionscore, compare)
    f = open('/usr/local/firmiana/leafy/gardener/test/test1.txt', 'a')
    f.write(str(datetime.datetime.now().strftime(
        '%Y-%m-%d %H:%M:%S')) + str(ProFileName) + 'begin \n')
    f.close()
    FID = {}
    GroupE = []
    MaxFraction = 0
    xList = []
    if compare and int(ppt) != 1 and int(tree) != 1:
        if not os.path.exists(CsvName):
            (xList, GroupE, MaxFraction) = GroupFraction(expList)
            f = open('/usr/local/firmiana/leafy/gardener/test/test1.txt', 'a')
            f.write(str(datetime.datetime.now().strftime(
                '%Y-%m-%d %H:%M:%S')) + 'GroupFaction done\n')
            f.close()
            allpep = []
            dic = {}

            (allpep, Pep2Num, pepFraction) = getPep(expList)
            # allpep = list(set(allpep))  # Get unique_pep
            f = open('/usr/local/firmiana/leafy/gardener/test/test1.txt', 'a')
            f.write(str(datetime.datetime.now().strftime(
                '%Y-%m-%d %H:%M:%S')) + 'pep done\n')
            f.close()

            PepNum = len(allpep)
            ExpNum = len(expList)
            cmtable = []
            allProtein = []
            (cmtable, allProtein, Symbol, Description) = getCmtable(
                ExpNum, expList, Pep2Num)
            # allProtein = list(set(allProtein))
            ProNum = len(allProtein)
            proListForIndex = {}
            ProTable = [[0 for col in range(ProNum)]
                        for row in range(ExpNum + 1)]
            i = 0
            for protein in allProtein:
                proListForIndex[protein] = i
                i = i + 1
                # f.write(str(exp)+'\n')
            # f.close()
            # return HttpResponse(cmtable[0][0]['pep'])
            f = open('/usr/local/firmiana/leafy/gardener/test/test1.txt', 'a')
            f.write(str(datetime.datetime.now().strftime(
                '%Y-%m-%d %H:%M:%S')) + 'cmtable done\n')
            f.close()

            stdtable = getStdtable(cmtable)
            f = open('/usr/local/firmiana/leafy/gardener/test/test1.txt', 'a')
            f.write(str(datetime.datetime.now().strftime(
                '%Y-%m-%d %H:%M:%S')) + 'stdtable done\n')
            f.close()

            rttable = getRTtable(stdtable)
            f = open('/usr/local/firmiana/leafy/gardener/test/test1.txt', 'a')
            f.write(str(datetime.datetime.now().strftime(
                '%Y-%m-%d %H:%M:%S')) + 'rttable done \n')
            f.close()

            cmtable = RTComplete(cmtable)
            f = open('/usr/local/firmiana/leafy/gardener/test/test1.txt', 'a')
            f.write(str(datetime.datetime.now().strftime(
                '%Y-%m-%d %H:%M:%S')) + 'cmtable=' + str(ExpNum) + 'rt complete\n')
            f.close()
            pool = multiprocessing.Pool(processes=20)
            result = []
            # ExpNum = 10
            # for exp in range(ExpNum):
            for exp in range(ExpNum):
                f = open('/usr/local/firmiana/leafy/gardener/test/test1.txt', 'a')
                f.write(str(datetime.datetime.now().strftime(
                    '%Y-%m-%d %H:%M:%S')) + 'exp=' + str(exp) + '\n')
                f.close()
                connection.close()
                # (cmtable[exp], ProTable[exp]) = calc(exp, expList, cmtable[exp], pepFraction, FID, PepNum, allpep, dRT, dMz, ProTable, proListForIndex)
                result.append(pool.apply_async(calc, (exp, expList, cmtable[
                              exp], pepFraction, FID, PepNum, allpep, dRT, dMz, ProTable, proListForIndex)))
                connection.close()
                # cmtable[exp] = calc(exp)q
                # f = open('/usr/local/firmiana/leafy/gardener/test/test1.txt', 'a')
                # f.write(str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')) + 'exp=' + str(exp) + 't=' + str(t) + '\n')
                # f.close()
            i = 0
            for res in result:
                (cmtable[i], ProTable[i]) = res.get()
                i = i + 1
            pool.close()
            pool.join()
            f = open('/usr/local/firmiana/leafy/gardener/test/test1.txt', 'a')
            f.write(str(datetime.datetime.now().strftime(
                '%Y-%m-%d %H:%M:%S')) + 'areas complete\n')
            f.close()
            newcmtable = [[{} for col in range(PepNum)]
                          for row in range(newExpNum)]
            newProTable = [[{}
                            for col in range(ProNum)] for row in range(newExpNum)]

            i = 0
            for exp in range(ExpNum):
                for pep in range(PepNum):
                    if cmtable[exp][pep] != '':
                        if 'ionscore' not in cmtable[exp][pep] or 'protein_group_accessions' not in cmtable[exp][pep] or'area' not in cmtable[exp][pep]:
                            continue
                        if newcmtable[Search2Exp[i]][pep] == []:
                            newcmtable[Search2Exp[i]][pep] = cmtable[exp][pep]
                        elif 'ionscore'not in newcmtable[Search2Exp[i]][pep] or cmtable[exp][pep]['ionscore'] > newcmtable[Search2Exp[i]][pep]['ionscore']:
                            newcmtable[Search2Exp[i]][pep][
                                'ionscore'] = cmtable[exp][pep]['ionscore']
                            newcmtable[Search2Exp[i]][pep][
                                'area'] = cmtable[exp][pep]['area']
                            newcmtable[Search2Exp[i]][pep][
                                'num_proteins'] = cmtable[exp][pep]['num_proteins']
                            newcmtable[Search2Exp[i]][pep][
                                'num_psms'] = cmtable[exp][pep]['num_psms']
                            newcmtable[Search2Exp[i]][pep][
                                'rt'] = cmtable[exp][pep]['rt']
                            newcmtable[Search2Exp[i]][pep][
                                'mz'] = allpep[pep]['mz']
                            if 'protein_group_accessions' not in newcmtable[Search2Exp[i]][pep]:
                                newcmtable[Search2Exp[i]][pep][
                                    'protein_group_accessions'] = ''
                            else:
                                newcmtable[Search2Exp[i]][pep]['protein_group_accessions'] = change(cmtable[exp][pep][
                                                                                                    'protein_group_accessions'], newcmtable[Search2Exp[i]][pep]['protein_group_accessions'])

                i = i + 1
            '''
            i = 0
            for exp in range(ExpNum):
                for Proteins in range(ProNum):
                    newProTable[Search2Exp[i]][Proteins] = newProTable[Search2Exp[i]][Proteins] + ProTable[exp][Proteins]
                i = i + 1
            '''
            i = 0
            for exp in range(newExpNum):
                j = 0
                for pep in newcmtable[exp]:
                    # if pep != ''and 'ionscore' in pep and
                    # 'protein_group_accessions' in pep and 'area' in pep:
                    if 'protein_group_accessions' in pep and 'area' in pep:
                        temp = len(pep['protein_group_accessions'])
                        for accession in pep['protein_group_accessions']:
                            if newProTable[exp][proListForIndex[accession]] == [] or 'area' not in newProTable[exp][proListForIndex[accession]]:
                                newProTable[exp][proListForIndex[accession]][
                                    'area'] = pep['area'] / temp
                                newProTable[exp][proListForIndex[
                                    accession]]['peptide'] = str(j)
                            else:
                                newProTable[exp][proListForIndex[accession]][
                                    'area'] += pep['area'] / temp
                                newProTable[exp][proListForIndex[accession]][
                                    'peptide'] += ';' + str(j)
                    j = j + 1
            f = open('/usr/local/firmiana/leafy/gardener/test/test1.txt', 'a')
            f.write(str(datetime.datetime.now().strftime(
                '%Y-%m-%d %H:%M:%S')) + 'done=' + str(exp) + '\n')
            f.close()
            # csv_name =  csv_name

            f = open(CsvName, 'w')
            f.write('Sequence\tModification\t')
            for templ in ansList:
                f.write(str(templ) + '_area\t')
                f.write(str(templ) + '_rt\t')
                f.write(str(templ) + '_mz\t')
            f.write('\n')
            for pep in range(PepNum):
                f.write(allpep[pep]['pep'] + '\t')
                f.write('\t')
                for exp in range(newExpNum):
                    f.write(str(newcmtable[exp][pep]['area']) + '\t')
                    f.write(str(newcmtable[exp][pep]['rt']) + '\t')
                    f.write(str(newcmtable[exp][pep]['mz']) + '\t')
                f.write('\n')
            f.close()
            f = open(ProFileName, 'w')
            f.write('accessions\tSymbol\tDescription\t')
            for templ in ansList:
                f.write(str(templ) + 'area' + '\t')
            f.write('peptide')
            f.write('\n')
            for Proteins in range(ProNum):
                f.write(allProtein[Proteins] + '\t')
                f.write(Symbol[Proteins] + '\t')
                f.write(Description[Proteins] + '\t')
                for exp in range(newExpNum):
                    if 'area' in newProTable[exp][Proteins]:
                        f.write(str(newProTable[exp][Proteins]['area']) + '\t')
                    else:
                        f.write('0' + '\t')
                # Proteins of all!qiuqiuqiuqiu!
                if 'peptide' in newProTable[exp][Proteins]:
                    f.write(newProTable[exp][Proteins]['peptide'])
                else:
                    f.write('')
                f.write('\n')
            f.close()
    elif int(ppt) != 1 and int(tree) != 1:
        if not os.path.exists(CsvName):
            expList = request.GET['sid']
            expList = expList.split(',')[:-1]
            templist = []
            allexp = []
            delList = []
            for exp in expList:
                temp = exp.split('_')
                (type, exp_id, rank, repe) = (temp[0], int(
                    temp[1]), int(temp[2]), int(temp[3]))
                if type == 'exp':
                    delList.append(exp)
                    Rep = Search.objects.filter(
                        exp_id=exp_id).filter(type='rep')
                    for rr in Rep:
                        tempstring = str(
                            'repeat') + '_' + str(rr.exp_id) + '_' + str(rr.rank) + '_' + str(rr.repeat_id)
                        expList.append(tempstring)
            for dd in delList:
                expList.remove(dd)
            expList = list(set(expList))
            expList.sort()
            allList = []
            for exp in expList:
                temp = exp.split('_')
                (type, exp_id, rank, repe) = (temp[0], int(
                    temp[1]), int(temp[2]), int(temp[3]))
                SearchList = Search.objects.filter(exp_id=exp_id).filter(
                    repeat_id=repe).filter(rank=rank).filter(type='rep')
                allList.append(SearchList[0].id)
            expList = list(set(allList))
            proList = []
            proListForIndex = []

            for exp in expList:
                Pro = Repeat_Protein.objects.filter(
                    search_id=exp).exclude(type=-1)
                for pro in Pro:
                    if (pro.accession, pro.symbol, pro.description) not in proList:
                        proList.append(
                            (pro.accession, pro.symbol, pro.description))
                        proListForIndex.append(pro.accession)
            ProNum = len(proList)
            peptides = ['' for col in range(ProNum)]
            pepList = []
            for exp in expList:
                Pep = Repeat_Peptide.objects.filter(search_id=exp).filter(
                    ion_score__gt=10).exclude(type=-1)
                for pep in Pep:
                    if (pep.sequence, pep.modification) not in pepList:
                        pepList.append((pep.sequence, pep.modification))
                        j = len(pepList) - 1
                        protein_group_accessions = pep.protein_group_accessions.split(
                            ';')
                        for pp in protein_group_accessions:
                            if pp in proListForIndex:
                                k = proListForIndex.index(pp)
                                peptides[k] += str(j) + ';'
            PepNum = len(pepList)
            newExpNum = len(expList)
            newcmtable = [[{} for col in range(PepNum)]
                          for row in range(newExpNum)]
            newProTable = [[{}
                            for col in range(ProNum)] for row in range(newExpNum)]
            for exp in expList:
                i = expList.index(exp)
                Pro = Repeat_Protein.objects.filter(
                    search_id=exp).exclude(type=-1)
                for pro in Pro:
                    j = proList.index(
                        (pro.accession, pro.symbol, pro.description))
                    temp = {}
                    temp['area'] = pro.area
                    temp['score'] = pro.score
                    temp['num_peptides'] = pro.num_peptides
                    temp['peptide'] = ''
                    newProTable[i][j] = temp
                Pep = Repeat_Peptide.objects.filter(search_id=exp).filter(
                    ion_score__gt=10).exclude(type=-1)
                for pep in Pep:
                    j = pepList.index((pep.sequence, pep.modification))
                    temp = {}
                    temp['num_psms'] = pep.num_psms
                    temp['num_proteins'] = pep.num_proteins
                    temp['charge'] = pep.charge
                    ms2 = pep.ms2_id
                    temp['mz'] = MS2.objects.get(id=ms2).pre_mz
                    temp['rt'] = pep.rt_min
                    temp['area'] = pep.area
                    newcmtable[i][j] = temp
            f = open(ProFileName, 'w')
            f.write('accessions\tSymbol\tDescription\t')
            for exp in expList:
                rr = Search.objects.get(id=exp)
                s = str('repeat') + '_' + str(rr.exp_id) + '_' + \
                    str(rr.rank) + '_' + str(rr.repeat_id)
                f.write(str(s) + 'area' + '\t')
            f.write('peptide\n')
            for pro in proList:
                for temp in pro:
                    f.write(str(temp) + '\t')
                for exp in expList:
                    if 'area' in newProTable[expList.index(exp)][proList.index(pro)]:
                        f.write(str(newProTable[expList.index(exp)][
                                proList.index(pro)]['area']) + '\t')
                    else:
                        f.write('0\t')
                f.write(peptides[proList.index(pro)] + '\n')
            f.close()
            f = open(CsvName, 'w')
            f.write('Sequence\tModification\t')
            for exp in expList:
                rr = Search.objects.get(id=exp)
                s = str('repeat') + '_' + str(rr.exp_id) + '_' + \
                    str(rr.rank) + '_' + str(rr.repeat_id)
                f.write(str(s) + '_area\t')
                f.write(str(s) + '_rt\t')
                f.write(str(s) + '_mz\t')
            f.write('\n')
            for pep in pepList:
                for temp in pep:
                    f.write(str(temp) + '\t')
                for exp in expList:
                    if 'area' in newcmtable[expList.index(exp)][pepList.index(pep)]:
                        f.write(str(newcmtable[expList.index(exp)][
                                pepList.index(pep)]['area']) + '\t')
                    else:
                        f.write('0\t')
                    if 'rt' in newcmtable[expList.index(exp)][pepList.index(pep)]:
                        f.write(str(newcmtable[expList.index(exp)][
                                pepList.index(pep)]['rt']) + '\t')
                    else:
                        f.write('0\t')
                    if 'mz' in newcmtable[expList.index(exp)][pepList.index(pep)]:
                        f.write(str(newcmtable[expList.index(exp)][
                                pepList.index(pep)]['mz']) + '\t')
                    else:
                        f.write('0\t')
                    if 'protein_group_accessions' in newcmtable[expList.index(exp)][pepList.index(pep)]:
                        f.write(str(newcmtable[expList.index(exp)][pepList.index(pep)][
                                'protein_group_accessions']) + '\t')
                    else:
                        f.write('0\t')
                f.write('\n')
            f.close()
    if int(tree) == 1:
        columns = []
        i = 0
        for temp1 in allexp:
            all = []
            a = {}
            a['text'] = 'Root'
            a['expanded'] = True
            for rep in allrep[i]:
                pp = {}
                pp["text"] = temp1 + '_' + rep
                # pp['id'] = temp1 + '_' + rep
                pp['leaf'] = True
                pp['checked'] = False
                columns.append(pp)
            i = i + 1
        a['children'] = columns
        all.append(a)
        result = json.dumps(all)
        return HttpResponse(result)

    if int(ppt) == 1:
        columns = [
            {'text': 'Accession', 'dataIndex': 'accessions', 'width': 90,
                'sortable': True, 'filter': {'type': 'string', 'encode': True}},
            {'text': 'Symbol', 'dataIndex': 'Symbol', 'width': 70,
                'sortable': True, 'filter': {'type': 'string', 'encode': True}},
            {'text': 'Description', 'dataIndex': 'Description', 'width': 70,
                'sortable': True, 'filter': {'type': 'string', 'encode': True}},
            {'text': 'Annotation', 'width': 70},
            {'text': 'Relation', 'width': 70, }
        ]
        i = 0
        for temp1 in allexp:
            tempDicExp = {}
            tempDicExp['text'] = temp1
            col = []
            for rep in allrep[i]:
                pp = {}
                pp['text'] = rep
                ff = []
                kk = {}
                kk['text'] = 'Area'
                kk['dataIndex'] = rep + 'area'
                kk['sortable'] = True
                kk['filter'] = {'type': 'float', 'encode': True}
                ff.append(kk)
                kk = {}
                kk['text'] = 'Ratio'
                kk['dataIndex'] = rep + 'ratio'
                # kk['sortable'] = True
                # kk['filter'] = {'type' : 'float', 'encode' : True}
                ff.append(kk)
                pp['columns'] = ff

                col.append(pp)
            tempDicExp['columns'] = col
            i = i + 1
            columns.append(tempDicExp)
        data = {}
        data['columns'] = columns
        result = json.dumps(data)
        return HttpResponse(result)

    f = open(ProFileName, 'r')
    fields = []
    fields.append({'name': 'id', 'type': 'int'})
    fields.append({'name': 'accessions', 'type': 'string'})
    fields.append({'name': 'Symbol', 'type': 'string'})
    fields.append({'name': 'Description', 'type': 'string'})
    fields.append({'name': 'test1_1', 'type': 'int'})
    fields.append({'name': 'test1_2', 'type': 'int'})
    fields.append({'name': 'test1_3', 'type': 'int'})
    fields.append({'name': 'test1_4', 'type': 'int'})
    fields.append({'name': 'test1_5', 'type': 'int'})
    fields.append({'name': 'test1_6', 'type': 'int'})
    fields.append({'name': 'test1_7', 'type': 'int'})
    fields.append({'name': 'test2_1', 'type': 'int'})
    fields.append({'name': 'test2_2', 'type': 'int'})
    fields.append({'name': 'test2_3', 'type': 'int'})
    fields.append({'name': 'test2_4', 'type': 'int'})
    fields.append({'name': 'test2_5', 'type': 'int'})
    fields.append({'name': 'test2_6', 'type': 'int'})
    fields.append({'name': 'test2_7', 'type': 'int'})
    fields.append({'name': 'annotation', 'type': 'string'})
    fields.append({'name': 'relation', 'type': 'string'})
    fields.append({'name': 'peptide', 'type': 'string'})
    for templ in ansList:
        temp = {}
        temp['name'] = templ + 'ratio'
        temp['type'] = 'float'
        fields.append(temp)
        temp = {}
        temp['name'] = templ + 'area'
        temp['type'] = 'float'
        fields.append(temp)
    data = []

    i = 0
    tfile = []
    title = []
    for line in f:
        if i == 0:
            i = i + 1
            title = line.split('\t')
        else:
            tfile.append(line.split('\t'))
    if len(filters) != 0:
        for filter in filters:
            if filter['type'] == 'string':
                field = title.index(filter['field'])
                tfile = [pp for pp in tfile if filter['value'] in pp[field]]
            if filter['type'] == 'numeric':
                field = title.index(filter['field'])
                if filter['comparison'] == 'lt':
                    tfile = [pp for pp in tfile if filter[
                        'value'] > float(pp[field])]
                if filter['comparison'] == 'gt':
                    tfile = [pp for pp in tfile if filter[
                        'value'] < float(pp[field])]
                if filter['comparison'] == 'lt':
                    tfile = [pp for pp in tfile if filter[
                        'value'] == float(pp[field])]
    '''
    def sortcmp(a, b):
        x = property
        if property in title:
            property = title.index(property)
        d = type(a[property])
        if type(a[property]) == type(1):
            return (a[property] - b[property]) * direction
        if type(a[property]) == type('s'):
            if direction == 1:
                return a[property] < b[property]
            else:
                return a[property] > b[property]
    '''
    if property in title:
        property = title.index(property)
    else:
        property = 0
    tfile = sorted(tfile, key=lambda lines: lines[
                   property] if property <= 2 else float(lines[property]), reverse=direction)
    count = len(tfile)
    end = start + limit
    if count < end or limit == -1:
        end = count
    tfile = tfile[start:end]
    for p in tfile:
        temp = {}
        #======================================================================
        # temp['test1_1'] = random.randint(0, 1)
        # temp['test1_2'] = random.randint(0, 1)
        # temp['test1_3'] = random.randint(0, 1)
        # temp['test1_4'] = random.randint(0, 1)
        # temp['test1_5'] = random.randint(0, 1)
        # temp['test1_6'] = random.randint(0, 1)
        # temp['test1_7'] = random.randint(0, 1)
        # temp['test2_1'] = random.randint(0, 1)
        # temp['test2_2'] = random.randint(0, 1)
        # temp['test2_3'] = random.randint(0, 1)
        # temp['test2_4'] = random.randint(0, 1)
        # temp['test2_5'] = random.randint(0, 1)
        # temp['test2_6'] = random.randint(0, 1)
        # temp['test2_7'] = random.randint(0, 1)
        #======================================================================
        temp['accessions'] = p[0]
        temp['Symbol'] = p[1]
        temp['Description'] = p[2]
        temp['id'] = i
        # p = p[3:]
        j = 3
        ok = False
        for templ in ansList:
            temp[title[j]] = float(p[j])
            if float(p[j]) != 0:
                ok = True
            j = j + 1
        temp['peptide'] = p[-1]
        i = i + 1
        # if not ok:
        #    continue
        data.append(temp)
    metaData = {}
    metaData['fields'] = fields
    # metaData['columns'] = columns
    metaData['root'] = 'data'
    data = {"data": data, "metaData": metaData,
            'total': count, 'allrep': allrep}
    result = json.dumps(data)
    return HttpResponse(result)


def mecompare_peptide(request):
    def getParam():
        try:
            expList = request.GET['sid']
        except:
            expList = ''
        try:
            start = int(request.GET['start'])
        except:
            start = ''
        try:
            limit = int(request.GET['limit'])
        except:
            limit = ''
        try:
            dRT = float(request.GET['dRT'])
        except:
            dRT = 60
        try:
            dMz = float(request.GET['dMz'])
        except:
            dMz = 10
        try:
            compare = request.GET['compare']
            if compare == 'true':
                compare = True
            else:
                compare = False
        except:
            compare = False
        try:
            ionscore = float(request.GET['ionscore'])
        except:
            ionscore = 30
        try:
            peptide = request.GET['peptide']
        except:
            peptide = ''
        return (peptide, expList, dRT, dMz, ionscore, compare, start, limit)

    def getExpList(expList, Search2Exp):
        expList = expList.split(',')[:-1]
        templist = []
        i = 0
        j = 0
        allexp = []
        delList = []
        for exp in expList:
            temp = exp.split('_')
            (type, exp_id, rank, repe) = (temp[0], int(
                temp[1]), int(temp[2]), int(temp[3]))
            if type == 'exp':
                delList.append(exp)
                Rep = Search.objects.filter(exp_id=exp_id).filter(type='rep')
                for rr in Rep:
                    tempstring = str('repeat') + '_' + str(rr.exp_id) + \
                        '_' + str(rr.rank) + '_' + str(rr.repeat_id)
                    expList.append(tempstring)
        for dd in delList:
            expList.remove(dd)
        f = open('/usr/local/firmiana/leafy/gardener/test/test1.txt', 'w')
        f.write(str(datetime.datetime.now().strftime(
            '%Y-%m-%d %H:%M:%S')) + str(expList) + 'begin \n')
        f.close()
        expList = list(set(expList))
        expList.sort()
        f = open('/usr/local/firmiana/leafy/gardener/test/test1.txt', 'a')
        f.write(str(datetime.datetime.now().strftime(
            '%Y-%m-%d %H:%M:%S')) + str(expList) + 'begin \n')
        f.close()
        ansList = expList
        for exp in expList:
            temp = exp.split('_')
            (type, exp_id, rank, repe) = (temp[0], int(
                temp[1]), int(temp[2]), int(temp[3]))
            ExpName = Experiment.objects.get(id=exp_id).name
            allexp.append(ExpName)
            if type == 'repeat':
                SearchList = Search.objects.filter(exp_id=exp_id).filter(
                    repeat_id=repe).filter(rank=rank).filter(type='fraction')
            elif type == 'exp':
                SearchList = Search.objects.filter(
                    exp_id=exp_id).filter(type='fraction')
            for search in SearchList:
                templist.append(search.id)
                Search2Exp[j] = i
                j = j + 1
            i = i + 1
        allexp = list(set(allexp))
        allrep = [[]for row in range(len(allexp))]
        for exp in expList:
            temp = exp.split('_')
            (exp1, rank, repe) = (temp[1], temp[2], temp[3])
            ExpName = Experiment.objects.get(id=exp1).name
            idx = allexp.index(ExpName)
            allrep[idx].append(exp)
        return (templist, Search2Exp, allexp, allrep, ansList)

    def getCsvName(expList, dRT, dMz, compare, ionscore):
        CsvName = ''
        expList.sort()
        for exp in expList:
            CsvName = CsvName + str(exp) + '_'
        (xtable, sign) = XsearchTable.objects.get_or_create(dmz=dMz,
                                                            drt=dRT,
                                                            ionscore=ionscore,
                                                            searchs=CsvName,
                                                            ProGene='protein',
                                                            compare=compare,
                                                            user='hzqnq'
                                                            )
        CsvName = str(xtable.id)
        # CsvName = CsvName + '&dRT=' + str(dRT) + '&dMz=' + str(dMz) + '&compare=' + str(compare)
        ProFileName = quant_dir + CsvName + '.protab'
        CsvName = quant_dir + CsvName + '.tab'
        return (CsvName, ProFileName)

    expList = ''
    dRT = 60
    dMz = 10
    compare = False
    peptide = ''
    (peptide, expList, dRT, dMz, ionscore, compare, start, limit) = getParam()
    # f = open('/usr/local/firmiana/leafy/gardener/test/test1.txt', 'w')
    # f.write(str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')) + str(expList) + '\n')
    # f.close()
    Search2Exp = {}
    (expList, Search2Exp, allexp, allrep, ansList) = getExpList(expList, Search2Exp)
    newExpNum = len(ansList)
    CsvName = ''
    (CsvName, ProFileName) = getCsvName(expList, dRT, dMz, compare, ionscore)
    FID = {}
    GroupE = []
    MaxFraction = 0
    xList = []

    f = open(CsvName, 'r')
    fields = []
    fields.append({'name': 'id', 'type': 'int'})
    fields.append({'name': 'num_psms', 'type': 'int'})
    fields.append({'name': 'num_proteins', 'type': 'int'})
    fields.append({'name': 'Sequence', 'type': 'string'})
    for templ in ansList:
        temp = {}
        temp['name'] = templ + '_ratio'
        temp['type'] = 'float'
        fields.append(temp)
        temp = {}
        temp['name'] = templ + '_area'
        temp['type'] = 'float'
        fields.append(temp)
        temp = {}
        temp['name'] = templ + '_mz'
        temp['type'] = 'float'
        fields.append(temp)
        temp = {}
        temp['name'] = templ + '_rt'
        temp['type'] = 'float'
        fields.append(temp)
    data = []

    i = 0
    pep = []
    title = []
    for line in f:
        if i == 0:
            i = i + 1
            title = line.split('\t')
            continue
        pep.append(line.split('\t'))
    # f = open('/usr/local/firmiana/leafy/gardener/test/test1.txt', 'w')
    # f.write(str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')) + str(peptide.split(';')) + '\n')
    # f.close()
    if peptide == '\n':
        newpep = []
    else:
        newpep = [pep[int(i)] for i in peptide.split(';')[:-1]]
    pep = newpep
    count = len(pep)
    for p in pep:
        temp = {}
        for i in range(len(p)):  # must be corrected
            temp[title[i]] = p[i]
        data.append(temp)
    columns = [
        {'text': 'Sequeunce', 'dataIndex': 'Sequence', 'width': 130},
        {'text': 'PSM Num', 'dataIndex': 'num_psms', 'width': 120},
        {'text': 'Protein Num', 'dataIndex': 'num_proteins', 'width': 120}
    ]
    i = 0
    for temp1 in allexp:
        # tempDicExp = {}
        # col = []
        for rep in allrep[i]:
            kk = {}
            kk['text'] = 'Area'
            kk['dataIndex'] = rep + '_area'
            columns.append(kk)
            kk = {}
            kk['text'] = 'Ratio'
            kk['dataIndex'] = rep + '_ratio'
            columns.append(kk)
        # tempDicExp['columns'] = col
        i = i + 1
        # columns.append(tempDicExp)
    metaData = {}
    metaData['fields'] = fields
    metaData['columns'] = columns
    metaData['root'] = 'data'
    data = {"data": data, "metaData": metaData,
            'total': count, 'allrep': allrep}
    result = json.dumps(data)
    return HttpResponse(result)


def kegg_statistic(request):
    if request.GET.has_key('search_id'):
        search_id = request.GET['search_id']
    elif request.GET.has_key('protein_id'):
        search_id = Protein.objects.filter(
            id=request.GET['protein_id'])[0].search_id
    pre = '{0}kegg_tmp/firkegg_{1}/'.format(tmpdir, time.time())
    os.mkdir(pre)
    ro.r.setwd(pre)  # create tempfile

    gage = importr('gage')
    gagedata = importr('gageData')
    pathview = importr('pathview')
    # = importr('Cairo')####

    data_env = gage. __rdata__.fetch('gse16873')  # Load data
    kegg_env = gage. __rdata__.fetch('kegg.gs')
    egsymb_env = gage. __rdata__.fetch('egSymb')

    gse = data_env['gse16873']
    kegg_gs = kegg_env['kegg.gs']

    ro.globalenv['egSymb'] = egsymb_env['egSymb']
    ro.globalenv['gse16873'] = data_env['gse16873']  #
    ro.globalenv['kegg.gs'] = kegg_env['kegg.gs']

    is_na = ro.r['is.na']
    as_num = ro.r['as.numeric']
    colnames = ro.r['colnames']
    rownames = ro.r['rownames']
    wtable = ro.r['write.table']
    esset_grp = ro.r['esset.grp']
    not_is_na = ro.r('function(x) !is.na(x)')

    options = 'options(bitmapType=cairo)'

    def pathview(pid):
        ro.r.pathview(gene_data=d_pro.rx(True, ro.r.seq(1, 2)),
                      pathway_id=pid, species="hsa")  # species

    gp1 = ro.IntVector([1, 3, 5, 7, 9, 11])  #
    gp2 = ro.IntVector([2, 4, 6, 8, 10, 12])  #
    exp_kegg = ro.r.gage(gse, gsets=kegg_gs, ref=gp1, samp=gp2)
    # exp_kegg_2d = ro.r.gage(gse, gsets = kegg_gs,ref = gp1, samp = gp2,same_dir = False)
    # exp_kegg_2d_sig=ro.r.sigGeneSet(exp_kegg_2d,outname="sig_kegg_2d")
    # exp_kegg = ro.r.gage(gse, gsets = kegg_gs,ref = gp1, samp = gp2)
    # exp_kegg_up_sig=ro.r.sigGeneSet(exp_kegg.rx('greater'),outname="sig_kegg")
    esg_kegg_up_sig = esset_grp(exp_kegg.rx('greater')[
                                0], gse, gsets=kegg_gs, ref=gp1, samp=gp2, test4up=True, output=True, outname='{}_up_pathway'.format(pre), make_plot=False)
    esg_kegg_down_sig = esset_grp(exp_kegg.rx('less')[0], gse, gsets=kegg_gs, ref=gp1, samp=gp2,
                                  test4up=False, output=True, outname='{}_down_pathway'.format(pre), make_plot=False)
    out_kegg = []
    col = []
    i = 0
    wantStop = int(request.GET['kegg_num'])
    if os.path.isfile('{}_up_pathway.esgp.txt'.format(pre)):
        for line in open('{}_up_pathway.esgp.txt'.format(pre), 'r'):
            i += 1
            if i > wantStop:
                break
            cls = line.replace('"', '').strip().split('\t')
            if cls[0] == 'essentialSets':
                if len(col) == 0:
                    for i in range(len(cls)):
                        cls[i] = cls[i].replace('.', '_')
                        col.append(cls[i])
            else:
                temp = {}
                for i in range(len(cls)):
                    cls[i] = float(cls[i]) if re.match(
                        '((\d+(\.\d*)?)|(\.\d+))', cls[i]) else cls[i]
                    temp[col[i]] = cls[i]
                temp['type'] = 'up'
                temp['genes'] = ','.join(gage.eg2sym(
                    esg_kegg_up_sig.rx('coreGeneSets')[0].rx(cls[0])[0]))
                temp['img'] = '{0}{1}.pathview.multi.png'.format(
                    pre, cls[0][0:8]).replace('/usr/local/firmiana/leafy', '')
                out_kegg.append(temp)
        gs = ro.r.unique(ro.r.unlist(kegg_gs.rx(
            rownames(exp_kegg.rx('greater')[0]).rx(ro.r.seq(1, 3)))))
        essData = ro.r.essGene(gs, gse, ref=gp1, samp=gp2)
    i = 0
    if os.path.isfile('{}_down_pathway.esgp.txt'.format(pre)):
        for line in open('{}_down_pathway.esgp.txt'.format(pre), 'r'):
            i += 1
            if i > wantStop:
                break
            cls = line.replace('"', '').strip().split('\t')
            if cls[0] == 'essentialSets':
                if len(col) == 0:
                    for i in range(len(cls)):
                        cls[i] = cls[i].replace('.', '_')
                        col.append(cls[i])
            else:
                temp = {}
                for i in range(len(cls)):
                    cls[i] = float(cls[i]) if re.match(
                        r'((\d+(\.\d*)?)|(\.\d+))', cls[i]) else cls[i]
                    temp[col[i]] = cls[i]
                temp['type'] = 'down'
                temp['genes'] = ','.join(gage.eg2sym(
                    esg_kegg_down_sig.rx('coreGeneSets')[0].rx(cls[0])[0]))
                temp['img'] = '{0}{1}.pathview.multi.png'.format(
                    pre, cls[0][0:8]).replace('/usr/local/firmiana/leafy', '')
                out_kegg.append(temp)
    field = []
    column = []
    if len(out_kegg) > 0:
        d_pro = gse.rx(True, gp2).ro - gse.rx(True, gp1)
        for kegg in out_kegg:
            pathview(kegg['essentialSets'][0:8])
        col.append('type')
        col.append('genes')
        col.append('img')
        for cl in col:
            temp = {}
            col_temp = {}
            if cl in ('essentialSets', 'setGroup', 'type', 'genes', 'img'):
                temp['name'] = cl
                temp['type'] = 'string'
                col_temp['text'] = cl
                col_temp['dataIndex'] = cl
                col_temp['align'] = 'left'
                if cl == 'essentialSets':
                    col_temp['flex'] = 1
                else:
                    col_temp['width'] = 70
                if cl in ('img', 'setGroup'):
                    col_temp['hidden'] = True
                col_temp['sortable'] = True
            else:
                temp['name'] = cl
                temp['type'] = 'float'
                col_temp['text'] = cl
                col_temp['dataIndex'] = cl
                col_temp['align'] = 'left'
                col_temp['width'] = 70
                col_temp['sortable'] = True
            field.append(temp)
            column.append(col_temp)
    metaData = {}
    metaData['fields'] = field
    metaData['columns'] = column
    data = {"data": out_kegg, "metaData": metaData, 'total': len(out_kegg)}
    result = json.dumps(data, cls=DjangoJSONEncoder)
    return HttpResponse(result)


def system_state(request):
    state = open(
        '/usr/local/firmiana/admin/log/system').readlines()[-1].strip().split(',')
    data = {"cpu": state[0], "mem": state[1], "task": state[2]}
    result = json.dumps(data, cls=DjangoJSONEncoder)
    return HttpResponse(result)


def ispec_output(request):

    def getExpList(expList):
        expList = expList.split(',')[:-1]
        templist = []
        i = 0
        j = 0
        allexp = []
        delList = []
        Search2Exp = {}
        for exp in expList:
            temp = exp.split('_')
            (type, exp_id, rank, repe) = (temp[0], int(
                temp[1]), int(temp[2]), int(temp[3]))
            if type == 'exp':
                delList.append(exp)
                Rep = Search.objects.filter(exp_id=exp_id).filter(type='rep')
                for rr in Rep:
                    tempstring = str('repeat') + '_' + str(rr.exp_id) + \
                        '_' + str(rr.rank) + '_' + str(rr.repeat_id)
                    expList.append(tempstring)
        for dd in delList:
            expList.remove(dd)
        expList = list(set(expList))
        ansList = expList
        f = open('/usr/local/firmiana/leafy/gardener/test/test1.txt', 'a')
        f.write(str(datetime.datetime.now().strftime(
            '%Y-%m-%d %H:%M:%S')) + str(expList) + 'begin \n')
        f.close()
        for exp in expList:
            temp = exp.split('_')
            (type, exp_id, rank, repe) = (temp[0], int(
                temp[1]), int(temp[2]), int(temp[3]))
            ExpName = Experiment.objects.get(id=exp_id).name
            allexp.append(ExpName)
            if type == 'repeat':
                SearchList = Search.objects.filter(exp_id=exp_id).filter(
                    repeat_id=repe).filter(rank=rank).filter(type='fraction')
            elif type == 'exp':
                SearchList = Search.objects.filter(
                    exp_id=exp_id).filter(type='fraction')
            for search in SearchList:
                templist.append(search.id)
                Search2Exp[j] = i
                j = j + 1
            i = i + 1
        allexp = list(set(allexp))
        allrep = [[]for row in range(len(allexp))]
        for exp in expList:
            temp = exp.split('_')
            (exp1, rank, repe) = (temp[1], temp[2], temp[3])
            ExpName = Experiment.objects.get(id=exp1).name
            idx = allexp.index(ExpName)
            allrep[idx].append(exp)
        return (templist, Search2Exp, allexp, allrep, ansList)

    def outputfile(exp, Title):
        peptide = Peptide.objects.filter(search_id=exp)
        name = Search.objects.get(id=exp).name
        filename = '/usr/local/firmiana/galaxy-dist/database/files/IspecFiles/' + name + '.tab'
        if os.path.exists(filename):
            return filename
        f = open(filename, 'w')
        i = 0
        for title in Title:
            if i != len(Title) - 1:
                f.write(title + '\t')
                i = i + 1
            else:
                f.write(title)
        f.write('\n')
        for pep in peptide:
            f.write(pep.quality + '\t')  # Confidence Level
            f.write('' + '\t')  # Search ID
            f.write('' + '\t')  # Processing Node No
            f.write(pep.sequence + '\t')  # Sequence
            f.write('' + '\t')  # Unique Sequence ID
            f.write('' + '\t')  # PSM Ambiguity
            f.write('' + '\t')  # Protein Descriptions
            f.write('' + '\t')  # Proteins
            f.write('' + '\t')  # Protein Groups
            # Protein Group Accessions
            f.write(pep.protein_group_accessions + '\t')
            f.write(pep.modification + '\t')  # Modifications
            f.write('' + '\t')  # Activation Type
            f.write('' + '\t')  # DeltaScore
            f.write(str(pep.delta_cn) + '\t')  # DeltaCn
            f.write('' + '\t')  # Rank
            f.write('' + '\t')  # Search Engine Rank
            f.write(str(pep.area) + '\t')  # Precursor Area
            f.write(str(pep.q_value) + '\t')  # q_value
            f.write(str(pep.pep) + '\t')  # pep
            f.write('' + '\t')  # Decoy Peptides Matched
            f.write(str(pep.exp_value) + '\t')  # exp_value
            f.write('' + '\t')  # Homology Threshold
            f.write('' + '\t')  # Identity High
            f.write('' + '\t')  # Identity Middle
            f.write(str(pep.ion_score) + '\t')  # ion_score
            f.write('' + '\t')  # Peptides Matched
            f.write(str(pep.num_missed_cleavages) + '\t')  # Missed Cleavages
            f.write('' + '\t')  # Isolation Interference _%_
            f.write('' + '\t')  # Ion Inject Time _ms_
            f.write(str(pep.ms2.ms1.intensity) + '\t')  # Intensity
            f.write(str(pep.charge) + '\t')  # charge
            f.write(str(pep.ms2.pre_mz) + '\t')  # m_z _Da_
            f.write(str(pep.mh_da) + '\t')  # mh_da
            f.write('' + '\t')  # Delta Mass _Da_
            f.write(str(pep.delta_m_ppm) + '\t')  # delta_m_ppm
            f.write(str(pep.rt_min) + '\t')  # rt_min
            f.write('' + '\t')  # First Scan
            f.write('' + '\t')  # Last Scan
            f.write('MS2' + '\t')  # MS Order
            f.write('' + '\t')  # Ions Matched
            f.write('' + '\t')  # Matched Ions
            f.write('' + '\t')  # Total Ions
            f.write(name + '\t')  # Spectrum File
            f.write('' + '\n')  # anntotation
        f.close()
        return filename

    def readFile(fn, buf_size=262144):
        f = open(fn, "rb")
        while True:
            c = f.read(buf_size)
            if c:
                yield c
            else:
                break
        f.close()

    # file_name = "big_file.txt"
    # response = HttpResponse(readFile(file_name))

    # return response
    try:
        expList = request.GET['sid']
    except:
        expList = ''
    try:
        _dc = request.GET['_dc']
    except:
        _dc = '1'
    (expList, Search2Exp, allexp, allrep, ansList) = getExpList(expList)
    Title = ['Confidence Level', 'Search ID', 'Processing Node No', 'Sequence', 'Unique Sequence ID', 'PSM Ambiguity', 'Protein Descriptions', '# Proteins', '# Protein Groups', 'Protein Group Accessions', 'Modifications', 'Activation Type', 'DeltaScore', 'DeltaCn', 'Rank', 'Search Engine Rank', 'Precursor Area', 'q_Value', 'PEP', 'Decoy Peptides Matched', 'Exp Value',
             'Homology Threshold', 'Identity High', 'Identity Middle', 'IonScore', 'Peptides Matched', '# Missed Cleavages', 'Isolation Interference _%_', 'Ion Inject Time _ms_', 'Intensity', 'Charge', 'm_z _Da_', 'MH_ _Da_', 'Delta Mass _Da_', 'Delta Mass _PPM_', 'RT _min_', 'First Scan', 'Last Scan', 'MS Order', 'Ions Matched', 'Matched Ions', 'Total Ions', 'Spectrum File', 'Annotation']
    temp = tempfile.TemporaryFile()
    zipFile = zipfile.ZipFile(temp, 'w', zipfile.ZIP_DEFLATED)
    for exp in expList:
        name = outputfile(exp, Title)
        zipFile.write(name, os.path.basename(name))
    zipFile.close()
    wrapper = FileWrapper(temp)
    response = HttpResponse(wrapper, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename=test.zip'
    response['Content-Length'] = temp.tell()
    temp.seek(0)
    return response


def mspaint(request):
    return null


def newcompare(request):
    # get params
    expList = request.POST['explist']
    try:
        dRT = float(request.POST['dRT'])
    except:
        dRT = 60
    try:
        dMz = float(request.POST['dMz'])
    except:
        dMz = 10
    try:
        ionscore = float(requset.POST['ionscore'])
    except:
        ionscore = 30
    views = request.POST['Views']
    try:
        cross = request.POST['cross_search']
        if cross == 'Yes':
            cross = True
        else:
            cross = False
    except:
        cross = False
    try:
        qc = request.POST['QC']
        if qc == 'Yes':
            qc = True
        else:
            qc = False
    except:
        qc = False

    desc = request.POST['description']
    if not desc:
        desc = '-'

    user = request.user

    # get explist
    expList = expList.split(',')[:-1]
    # templist = []
    # allexp = []
    delList = []
    for exp in expList:
        temp = exp.split('_')
        (type, exp_id, rank, repe) = (temp[0], int(
            temp[1]), int(temp[2]), int(temp[3]))
        if type == 'exp':
            delList.append(exp)
            Rep = Search.objects.filter(exp_id=exp_id).filter(type='rep')
            for rr in Rep:
                tempstring = str('repeat') + '_' + str(rr.exp_id) + \
                    '_' + str(rr.rank) + '_' + str(rr.repeat_id)
                expList.append(tempstring)
    for dd in delList:
        expList.remove(dd)
    expList.sort()
    CsvName = ''
    for exp in expList:
        CsvName = CsvName + str(exp) + ';'
    if views == 'Protein':
        views = 'protein'
    elif views == 'Gene':
        views = 'gene'
    else:
        views = 'peptide'
    table = XsearchTable.objects.filter(dmz=dMz, drt=dRT, ionscore=ionscore, searchs=CsvName,
                                        ProGene=views, compare=cross, qc=qc, user=user)

    #=========================================================================
    # if table.count() >= 1:
    #     CsvName = table[0].id
    # else:
    #=========================================================================
    xtable = XsearchTable(dmz=dMz,
                          drt=dRT,
                          ionscore=ionscore,
                          searchs=CsvName,
                          ProGene=views,
                          compare=cross,
                          qc=qc,
                          user=user,
                          status='new',
                          exp_name=request.POST['explist'][:-1],
                          exp_num=len(request.POST['explist'][:-1].split(',')),
                          description=desc
                          )
    xtable.save()
    CsvName = str(xtable.id)
    data = {'success': True, 'msg': str(CsvName)}
    result = json.dumps(data)
    return HttpResponse(result)
    # CsvName = CsvName + '&dRT=' + str(dRT) + '&dMz=' + str(dMz) + '&compare=' + str(compare)


def newcmp_getheader(request):
    csvname = int(request.GET['id'])
    cont = XsearchTable.objects.get(id=csvname)
    expList = cont.exp_name
    expList = expList.split(',')
    if expList[-1] == '':
        expList = expList[:-1]
    gridType = request.GET[
        'gridType'] if 'gridType' in request.GET else cont.ProGene
    # print gridType
    t1 = datetime.datetime.now()

    def my_timer(t1):
        t2 = datetime.datetime.now()
        return float((t2 - t1).seconds) + (t2 - t1).microseconds / 1000000.0
    if gridType == 'protein':
        columns = [
            {'xtype': 'rownumberer', 'width': 50, 'text': 'No.'},
            {'text': 'Accession', 'dataIndex': 'accessions', 'width': 90,
                'sortable': True, 'filter': {'type': 'string', 'encode': True}},
            {'text': 'Symbol', 'dataIndex': 'Symbol', 'width': 70,
                'sortable': True, 'filter': {'type': 'string', 'encode': True}},
            {'text': 'Description', 'dataIndex': 'Description', 'width': 70,
                'sortable': True, 'filter': {'type': 'string', 'encode': True}},
            {'text': 'Annotation', 'width': 70, 'sortable': True},
            {'text': 'Modification', 'dataIndex': 'modification',
                'width': 70, 'sortable': True},
            {'text': 'User Defined', 'dataIndex': 'user_defined', 'width': 70,
                'sortable': True, 'editor': {'allowBlank': True}},
        ]
    elif gridType == 'gene':
        columns = [
            {'xtype': 'rownumberer', 'width': 50, 'text': 'No.'},
            {'text': 'geneID', 'dataIndex': 'geneID', 'width': 90,
                'sortable': True, 'filter': {'type': 'string', 'encode': True}},
            {'text': 'Symbol', 'dataIndex': 'Symbol', 'width': 70,
                'sortable': True, 'filter': {'type': 'string', 'encode': True}},
            {'text': 'Description', 'dataIndex': 'Description', 'width': 70,
                'sortable': True, 'filter': {'type': 'string', 'encode': True}},
            {'text': 'Annotation', 'width': 70, 'sortable': True},
            {'text': 'Modification', 'dataIndex': 'modification',
                'width': 70, 'sortable': True},
            {'text': 'User Defined', 'dataIndex': 'user_defined', 'width': 70,
                'sortable': True, 'editor': {'allowBlank': True}},
        ]
    else:
        columns = [
            {'xtype': 'rownumberer', 'width': 50, 'text': 'No.'},
            {'text': 'Sequence', 'dataIndex': 'Sequence', 'width': 90,
                'sortable': True, 'filter': {'type': 'string', 'encode': True}},
            {'text': 'Protein Accession', 'dataIndex': 'accessions', 'width': 70,
                'sortable': True, 'filter': {'type': 'string', 'encode': True}},
            {'text': 'GeneSymbol', 'dataIndex': 'Symbol', 'width': 70,
                'sortable': True, 'filter': {'type': 'string', 'encode': True}},
            {'text': 'Modification', 'dataIndex': 'Modification', 'width': 70,
                'sortable': True, 'filter': {'type': 'string', 'encode': True}},
        ]
    # print 'init'
    # print my_timer(t1)
    alist = []  # explist
    blist = []  # replist
    cacheB = []
    for exp in expList:
        temp = exp.split('_')
        (type, exp_id, rank, repe) = (temp[0], int(
            temp[1]), int(temp[2]), int(temp[3]))
        ExpName = Experiment.objects.get(id=exp_id).name
        Description = Experiment.objects.get(id=exp_id).description
        alist.append(ExpName)
        if type == 'exp':
            RepeatList = Search.objects.filter(
                exp_id=exp_id).filter(rank=rank).filter(type='rep')
            for rep in RepeatList:
                blist.append('repeat_' + str(rep.exp_id) + '_' +
                             str(rep.rank) + '_' + str(rep.repeat_id))
                cacheB.append(rep.exp_id)
        else:
            blist.append(exp)
            cacheB.append(exp_id)
    alist = list(set(alist))
    alist.sort()
    blist = list(set(blist))
    blist.sort()
    # print 'sort'
    # print my_timer(t1)
    max_length = 0
    cacheExperimentA = Experiment.objects.filter(name__in=alist)
    des = {}
    for exp in cacheExperimentA:
        des[exp.name] = exp.description
    names = {}
    cacheExperimentB = Experiment.objects.filter(id__in=cacheB).all()
    for exp in cacheExperimentB:
        names[exp.id] = exp.name
    for exp in alist:
        tempDicExp = {}
        tempDicExp['text'] = exp
        # tempDicExp['cls'] = 'multiline'
        Description = des[exp]
        # Description = Experiment.objects.get(name=exp).description
        for description in Description.split(';'):
            if len(description) > 20:
                tempDicExp['text'] = tempDicExp[
                    'text'] + '<br>' + description[:20]
                tempDicExp['text'] = tempDicExp[
                    'text'] + '<br>' + description[20:]
            else:
                tempDicExp['text'] = tempDicExp['text'] + '<br>' + description
        # print 'muhaha'
        # print my_timer(t1)
        max_length = len(tempDicExp['text'].split('<br>')) if (
            len(tempDicExp['text'].split('<br>')) > max_length) else max_length
        col = []
        for temp1 in blist:
            temp = temp1.split('_')
            (type, exp_id, rank, repe) = (temp[0], int(
                temp[1]), int(temp[2]), int(temp[3]))
            name = names[exp_id]
            # name=Experiment.objects.get(id=exp_id).name
            if name == exp:
                pp = {}
                pp['text'] = type + '_' + str(rank) + '_' + str(repe)
                ff = []
                kk = {}
                kk['text'] = 'Area'
                kk['dataIndex'] = temp1 + '_area'
                kk['sortable'] = True
                kk['width'] = 80
                kk['align'] = 'right'
                kk['filter'] = {'type': 'float', 'encode': True}
                ff.append(kk)
                kk = {}
                kk['text'] = 'PSM'
                kk['dataIndex'] = temp1 + '_psms'
                kk['sortable'] = True
                kk['width'] = 65
                kk['align'] = 'right'
                kk['filter'] = {'type': 'float', 'encode': True}
                ff.append(kk)
                kk = {}
                kk['text'] = 'Ratio'
                kk['dataIndex'] = temp1 + '_ratio'
                kk['sortable'] = True
                kk['width'] = 65
                kk['align'] = 'right'
                kk['filter'] = {'type': 'float', 'encode': True}
                ff.append(kk)
                pp['columns'] = ff
                col.append(pp)
        tempDicExp['columns'] = col
        # print 'wulala'
        # print my_timer(t1)
        columns.append(tempDicExp)
    # print 'dbdone'
    # print my_timer(t1)
    for i in range(len(columns)):
        if 'text' not in columns[i]:
            continue
        if 'Exp' in columns[i]['text']:
            while(len(columns[i]['text'].split('<br>')) <= max_length):
                columns[i]['text'] = columns[i]['text'] + '<br>'
    # print 'yoyo'
    # print my_timer(t1)
    data = {}
    data['columns'] = columns

    result = json.dumps(data)
    return HttpResponse(result)


def newcmp_calc(id):
    # return 0
    t1 = datetime.datetime.now()

    def my_timer(t2, t1):
        return float((t2 - t1).seconds) + (t2 - t1).microseconds / 1000000.0

    def print_delta_time(t1, msg):
        msg = msg if msg else 'Till now'
        t2 = datetime.datetime.now()
        # float((t2 - t1).seconds) + (t2 - t1).microseconds / 1000000.0
        delta = my_timer(t2, t1)
        print '%s used %.3f seconds' % (msg, delta)

    def set2str(tempset):
        tempstr = ''
        for aa in tempset:
            tempstr = tempstr + str(aa) + ';'
        tempstr = tempstr[:-1]
        return tempstr

    def get_coeRT(info, all_pep):
        coeRT = []
        for exp1 in range(len(info)):
            temp = []
            rt1 = []
            rt2 = []
            for exp2 in range(len(info)):
                if exp1 != exp2:
                    for pep in range(len(all_pep)):
                        if info[exp1][pep][0] != 0 and info[exp2][pep][0] != 0:  # peptidearea
                            rt1.append(info[exp1][pep][2])
                            rt2.append(info[exp2][pep][2])
                    calc1 = polyfit(rt1, rt2, 1)
                    calc2 = polyfit(rt1, rt2, 2)
                    if calc1['determination'] >= calc2['determination']:
                        temp.append(calc1)
                    else:
                        temp.append(calc2)
                else:
                    temp.append('')

            coeRT.append(temp)

        ''' fullfil RT '''
        for exp1 in range(len(info)):
            for pep_idx in range(len(all_pep)):
                # every peptide in exp
                if info[exp1][pep_idx] == [0, 0, 0, 0, 0, 0]:
                    # compare with any other exp
                    for exp2 in range(len(info)):
                        if exp1 == exp2:
                            continue
                        if info[exp2][pep_idx] != [0, 0, 0, 0, 0, 0]:
                            temprt = np.polyval(
                                coeRT[exp1][exp2]['polynomial'], info[exp2][pep_idx][2])
                            info[exp1][pep_idx] = [0, 0, temprt, info[exp2][pep_idx][
                                3], info[exp2][pep_idx][4], info[exp2][pep_idx][5]]
                            # temp_list.append([tempPep.area, tempPep.fot, tempPep.rt_min, mz, tempPep.num_psms, tempPep.ion_score])

    t1 = datetime.datetime.now()
    csvname = id

    pep_pro_gen = XsearchTable.objects.get(id=int(csvname)).ProGene

    repeatList = XsearchTable.objects.get(id=int(csvname)).searchs
    ion_score = float(XsearchTable.objects.get(id=int(csvname)).ionscore)
    dmz = float(XsearchTable.objects.get(id=int(csvname)).dmz)
    drt = float(XsearchTable.objects.get(id=int(csvname)).drt)
    qc = XsearchTable.objects.get(id=int(csvname)).qc
    compare = XsearchTable.objects.get(id=int(csvname)).compare

    repeatList = repeatList.split(';')[:-1]
    repeatLENGTH = len(repeatList)
    print 'Repeat Contains %d repeat' % repeatLENGTH
    proList = set()
    pepList = set()
    geneList = []
    tmp_geneList = set()

    if not qc:
        for repeat in repeatList:
            temp = repeat.split('_')
            (type, exp_id, rank, repe) = (temp[0], int(
                temp[1]), int(temp[2]), int(temp[3]))
            id = Search.objects.filter(exp_id=exp_id).filter(
                rank=rank).filter(repeat_id=repe).filter(type='rep')[0].id

            tempProList = Repeat_Protein.objects.filter(
                search_id=id).exclude(type=-1)
            for pro in tempProList:
                proList.add((pro.accession, pro.symbol, pro.description))

            tempPepList = Repeat_Peptide.objects.filter(search_id=id).filter(
                ion_score__gt=ion_score).exclude(type=-1)
            for pep in tempPepList:
                pepList.add((pep.sequence, pep.modification))

            tempGeneList = Repeat_Gene.objects.filter(
                search_id=id).exclude(type=-1)
            for gene in tempGeneList:
                sym = gene.symbol
                if sym not in tmp_geneList:
                    tmp_geneList.add(sym)
                    geneList.append((gene.gene_id, sym, gene.description))

    else:  # After QC
        tmpExpList = []
        for repeat in repeatList:
            temp = repeat.split('_')
            (type, exp_id, rank, repe) = (temp[0], int(
                temp[1]), int(temp[2]), int(temp[3]))
            # // exp_id is from TABLE gardener_experiment
            tmpExpList.append(exp_id)

        options = {}
        options['min_fdr'] = 1
        options['min_ion'] = 0
        options['max_hit'] = 10
        options['dMZ'] = 10
        options['dRT'] = 60

        options['exp_list'] = tmpExpList  # [484, 485, 391, 392, 428, 429]

        options['stype'] = 'exp'
        (proteins, peptides, genes) = my_QC(options)

        for pro in proteins:
            proList.add((pro['accession'], pro['symbol'], pro['description']))

        for pep in peptides:
            pepList.add((pep['sequence'], pep['modification']))

        for gene in genes:
            sym = gene['symbol']
            if sym not in tmp_geneList:
                tmp_geneList.add(sym)
                geneList.append((gene['gene_id'], sym, gene['description']))

        print 'Done'

        print 'peptides=', len(peptides)
        print 'proteins=', len(proteins)
        print 'genes=', len(genes)

    print_delta_time(t1, 'get list done!')

    proList = list(proList)
    pepList = list(pepList)
    print 'len(pepList)=', len(pepList)
    # geneList = list(geneList)

    ''' matrix '''
    proTable = []
    pepTable = []
    geneTable = []

    ''' For index '''
    proListForIndex = []
    geneListForIndex = []

    geneAnno = {}
    proAnno = {}

    pep2pro = []
    pep2gen = []

    for pro in proList:
        proListForIndex.append(pro[0])  # pro[0] = accession
    for gene in geneList:
        geneListForIndex.append(gene[1])  # gene[1] = symbol

    # LogFile=open(quant_dir+'logs/log.txt','w')
    # if 1:  # not compare:
    ''' get geneTable '''
    for repeat in repeatList:
        temp = []
        tempList = repeat.split('_')
        (type, exp, rank, repe) = (tempList[0], int(
            tempList[1]), int(tempList[2]), int(tempList[3]))

        id = Search.objects.filter(exp_id=exp).filter(
            rank=rank).filter(repeat_id=repe).filter(type='rep')[0].id
        tempGenList = Repeat_Gene.objects.filter(search_id=id).exclude(type=-1)

        for gen in geneList:
            (gene_id, symbol, description) = list(gen)
            tmp_obj_gene = tempGenList.filter(symbol=symbol)
            if tmp_obj_gene:
                tempGen = tmp_obj_gene[0]
                # tempGen.num_psms now not available!
                temp.append([tempGen.area, tempGen.fot,
                             tempGen.ibaq, tempGen.num_psms])
                geneAnno[symbol] = tempGen.annotation
            else:
                temp.append([-1, -1, -1, -1])
        geneTable.append(temp)
    # print len(geneTable)
    # peptidelist
    geneTable.append([])

    for gen in geneList:
        geneTable[-1].append(set())

    print_delta_time(t1, 'geneTable.append done!')

    ''' get proTable '''
    repeat_idx = 0
    for repeat in repeatList:
        temp = []
        tempList = repeat.split('_')
        (type, exp, rank, repe) = (tempList[0], int(
            tempList[1]), int(tempList[2]), int(tempList[3]))
        id = Search.objects.filter(exp_id=exp).filter(
            rank=rank).filter(repeat_id=repe).filter(type='rep')[0].id
        # LogFile.write(str(id)+'\n')
        tempProList = Repeat_Protein.objects.filter(
            search_id=id).exclude(type=-1)
        for pro in proList:
            # if filter(pro):
            (acc, sym, des) = list(pro)

            tmp_obj_protein = tempProList.filter(accession=acc).filter(
                symbol=sym).filter(description=des)
            if tmp_obj_protein:
                tempPro = tmp_obj_protein[0]
                temp.append([tempPro.area, tempPro.fot,
                             tempPro.ibaq, tempPro.num_psms])
                # if acc=='gi|312922382':
                #    print tempPro.annotation
                proAnno[acc] = tempPro.annotation
                try:
                    idx_geneList = geneListForIndex.index(sym)
                    geneTable[repeat_idx][idx_geneList][3] += tempPro.num_psms
                except:
                    continue
            else:
                temp.append([-1, -1, -1, -1])
        proTable.append(temp)
        repeat_idx += 1
    ''' proTable[-1] contains as many set()s as amount of proteins '''
    proTable.append([])
    for pro in proList:
        proTable[-1].append(set())

    print_delta_time(t1, 'proTable.append() done!')

    ''' get pepTable [exp by exp]'''
    for repeat in repeatList:
        temp = []
        tempList = repeat.split('_')
        (type, exp, rank, repe) = (tempList[0], int(
            tempList[1]), int(tempList[2]), int(tempList[3]))

        id = Search.objects.filter(exp_id=exp).filter(
            rank=rank).filter(repeat_id=repe).filter(type='rep')[0].id
        # LogFile.write(str(id)+'\n')
        tempPepList = Repeat_Peptide.objects.filter(
            search_id=id).exclude(type=-1)
        i = 0
        for pep in pepList:
            (seq, modi) = list(pep)
            if len(pep2pro) <= i:
                pep2pro.append([])
            if len(pep2gen) <= i:
                pep2gen.append(set())

            tmp_obj_peptide = tempPepList.filter(
                sequence=seq).filter(modification=modi)
            if tmp_obj_peptide:
                tempPep = tmp_obj_peptide[0]
                temp.append([tempPep.area, tempPep.mh_da,
                             tempPep.rt_min, tempPep.num_psms])
                accessions = tempPep.protein_group_accessions.split(';')
                pep2pro[i].extend(accessions)
                for acc in accessions:
                    if acc in proListForIndex:
                        idx = proListForIndex.index(acc)
                        sym = proList[idx][1]
                        if sym:
                            pep2gen[i].add(sym)
                        ''' Record a protein has what peptides  '''
                        proTable[-1][idx].add(i)
            else:
                temp.append([-1, -1, -1, -1])
            i = i + 1
        pepTable.append(temp)

    print_delta_time(t1, 'Peptide done!')

    i = 0
    for pro in proList:
        symbol = pro[1]
        if symbol != '':
            if symbol in geneListForIndex:
                idx = geneListForIndex.index(symbol)
                geneTable[-1][idx] = geneTable[-1][idx] | proTable[-1][i]
        i += 1

    print_delta_time(t1, 'geneListForIndex.index(symbol) done!')

    '''
    tempPepList=Repeat_Peptide.objects.filter(search_id=repeat).filter(ion_score__gt=ion_score).exclude(type=-1)
    for pep in peplist:
            #if  filter(pep):
            (seq,modi)=list(pep)
            if tempPepList.filter(sequence=seq).filter(modification=modi).count()>0:
                tempPep=tempPepList.filter(sequence=seq).filter(modification=modi)[0]
                
                pep.add()
            else:
                pep.add(-1)
        for gene in geneList:
            if filter(gene):
                gene.add()
            else:
                gene.add(-1)
    '''
    if compare:  # Start compare search !
        print_delta_time(t1, 'Start compare search !')

        repeat = repeatList[0]
        temp = repeat.split('_')
        (type, exp, rank, repe) = (temp[0], int(
            temp[1]), int(temp[2]), int(temp[3]))
        fraction = Search.objects.filter(exp_id=exp).filter(type='exp')[
            0].exp.num_fraction

        list_for_merge_fraction = []
        for frac in range(1, 1 + fraction):
            print 'frac=', frac
            # temp_pep_cont = []
            # temp_pep_all = [] #sequence and modification
            # get all pep for each fraction
            all_pep = set()

            for repeat in repeatList:
                temp = repeat.split('_')
                (type, exp, rank, repe) = (temp[0], int(
                    temp[1]), int(temp[2]), int(temp[3]))

                #==============================================================
                # ''' I need to know a peptide has what proteins & genes  '''
                # cache_repeat_id = Search.objects.filter(exp_id=exp).filter(rank=rank).filter(repeat_id=repe).filter(type='rep')[0].id
                # cache_tempPepList_obj = Repeat_Peptide.objects.filter(search_id=cache_repeat_id).exclude(type=-1)
                #
                # i=-1
                # for pep in pepList:
                #     i += 1
                #     (seq, modi) = list(pep)
                #     if len(pep2pro) <= i: pep2pro.append(set())
                #     if len(pep2gen) <= i: pep2gen.append(set())
                #
                #     tmp_obj_peptide = cache_tempPepList_obj.filter(sequence=seq).filter(modification=modi)
                #     if tmp_obj_peptide:
                #         tempPep = tmp_obj_peptide[0]
                #         accessions = tempPep.protein_group_accessions.split(';')
                #
                #         for acc in accessions:
                #             pep2pro[i].add(acc)
                #             idx = proListForIndex.index(acc)
                #             pep2gen[i].add(proList[idx][1])#symbol
                #==============================================================

                ''' get all_pep, which contains all non-redundant "peptide_modification_charge"  '''
                id = Search.objects.filter(exp_id=exp).filter(
                    repeat_id=repe).filter(rank=rank).filter(fraction_id=frac)[0].id
                tempPepList = Peptide.objects.filter(
                    search_id=id).exclude(type=-1)
                # tempPepList is a big list
                for pep in tempPepList:
                    pep_str = pep.sequence + '_' + \
                        pep.modification + '_' + str(pep.charge)
                    all_pep.add(pep_str)

            all_pep = list(all_pep)
            print 'len(all_pep)=', len(all_pep)
            ''' 
            info[0] = [ [0,0,0,0,0,0],
                        [0,0,0,0,0,0],
                        [0,0,0,0,0,0],
                        .....,
                        [0,0,0,0,0,0] ] 
            '''
            info = []
            info_pep_without_area = []
            for repeat in repeatList:
                pep_without_area = []
                temp = repeat.split('_')
                (type, exp, rank, repe) = (temp[0], int(
                    temp[1]), int(temp[2]), int(temp[3]))
                id = Search.objects.filter(exp_id=exp).filter(
                    repeat_id=repe).filter(rank=rank).filter(fraction_id=frac)[0].id
                tempPepList = Peptide.objects.filter(
                    search_id=id).exclude(type=-1)

                temp_list = []
                for pep in all_pep:
                    (seq, modi, charge) = pep.split('_')
                    tmp_obj_peptide = tempPepList.filter(sequence=seq).filter(
                        modification=modi).filter(charge=charge).order_by('-ion_score')
                    if tmp_obj_peptide:
                        temp_pep = tmp_obj_peptide[0]
                        ms2_id = temp_pep.ms2_id
                        mz = MS2.objects.get(id=ms2_id).pre_mz
                        temp_list.append(
                            [temp_pep.area, temp_pep.fot, temp_pep.rt_min, mz, temp_pep.num_psms, temp_pep.ion_score])
                    else:
                        pep_without_area.append(seq + '_' + modi)
                        temp_list.append([0, 0, 0, 0, 0, 0])
                info.append(temp_list)
                info_pep_without_area.append(pep_without_area)

            ''' coefficient RT '''
            get_coeRT(info, all_pep)

            list_for_merge_exp = []
            for exp1 in range(len(info)):
                repeat = repeatList[exp1]
                temp = repeat.split('_')
                (type, exp, rank, repe) = (temp[0], int(
                    temp[1]), int(temp[2]), int(temp[3]))
                obj_search = Search.objects.filter(exp_id=exp).filter(
                    repeat_id=repe).filter(rank=rank).filter(fraction_id=frac)[0]
                id, filename = obj_search.id, obj_search.name
                ''' import from cal_area.py '''
                calcAreas(id, filename, 60, 10, info[exp1])

                list_for_merge_exp.append(info[exp1])
            ''' if we need compare 3 exps , list_for_merge_exp = [ [],[],[],all_pep ] '''
            list_for_merge_exp.append(all_pep)
            ''' list_for_merge_fraction = [    [ [],[],[],all_pep ] , [ [],[],[],all_pep ] , [ [],[],[],all_pep ] ....... [ [],[],[],all_pep ]      ] '''
            list_for_merge_fraction.append(list_for_merge_exp)

            ''' Till now, one fraction finished '''

        print_delta_time(t1, 'Start merge every fraction per exp !')
#                 proList = list(proList)
#                 pepList = list(pepList)
#                 geneList = list(geneList)

        list_peptide_dicts = []
        for exp in range(repeatLENGTH):
            protein_list_exp = proTable[exp]
            gene_list_exp = geneTable[exp]

            dict_peptide_table = {}
            not_in_dict_peptide_table = 0
            ''' pepList contains cached peptide list collected from all exps '''
            for pep_tuple in pepList:
                dict_peptide_table[pep_tuple[0] + '_' + pep_tuple[1]] = []

            tmp_list_pep_attrib = []
            for frac in range(fraction):
                ''' list_for_merge_fraction = [    [ [],[],[],all_pep ] , [ [],[],[],all_pep ] , [ [],[],[],all_pep ] ....... [ [],[],[],all_pep ]      ] '''
                all_pep_exp_name = list_for_merge_fraction[frac][-1]
                list_exp_peptide = list_for_merge_fraction[frac][exp]
                for idx in range(len(all_pep_exp_name)):
                    # print 'all_pep_exp[idx]',all_pep_exp[idx]
                    (seq, mod, charge) = all_pep_exp_name[idx].split('_')
                    seq_mod = seq + '_' + mod
                    pep_attrib = list_exp_peptide[idx]
                    if seq_mod not in dict_peptide_table:
                        # print seq_mod,' not in dict_peptide_table'
                        not_in_dict_peptide_table += 1
                        continue
                    if dict_peptide_table[seq_mod]:
                        # area, fot, rt_min, mz, num_psms, ion_score = dict_peptide_table[seq_mod]
                        dict_peptide_table[seq_mod][4] += pep_attrib[4]
                        dict_peptide_table[seq_mod][0] += pep_attrib[0]
                    else:
                        dict_peptide_table[seq_mod] = pep_attrib

            #==================================================================
            # for pep_tuple in pepList:
            #     seq,mod = pep_tuple
            #     seq_mod = seq+'_'+mod
            #     if seq_mod in dict_peptide_table:
            #         print dict_peptide_table[seq_mod]
            #     else:
            #         print seq_mod ,'not in'
            #==================================================================

            list_peptide_dicts.append(dict_peptide_table)
            print 'not_in_dict_peptide_table=', not_in_dict_peptide_table
            # print list_peptide_dicts
            pep_without_area = set(info_pep_without_area[exp])
            i = -1
            for pro in protein_list_exp:
                i += 1
                ''' Re-distribute area to proteins '''
                accession = proListForIndex[i]
                set_pep_of_pro = proTable[-1][i]  # set()
                # if pro[0] == -1:# pro[0] -> area
                for pep_idx in set_pep_of_pro:
                    if accession in pep2pro[pep_idx]:
                        seq_mod = '_'.join(list(pepList[pep_idx]))
                        if seq_mod in pep_without_area:
                            pro[0] += dict_peptide_table[seq_mod][0] / \
                                len(pep2pro[pep_idx])

            i = -1
            for gene in gene_list_exp:
                i += 1
                ''' Re-distribute area to genes '''
                sym = geneListForIndex[i]
                set_pep_of_gene = geneTable[-1][i]  # set()
                # if pro[0] == -1:# pro[0] -> area
                for pep_idx in set_pep_of_gene:
                    if sym in pep2gen[pep_idx]:
                        seq_mod = '_'.join(list(pepList[pep_idx]))
                        if seq_mod in pep_without_area:
                            gene[0] += dict_peptide_table[seq_mod][0] / \
                                len(pep2gen[pep_idx])
        # continue

        '''
        1.get all peptide, protein and gene
        2.get rttable
        3.get area per raw
        4.get all_table
        5.write table 
        '''
        # return
    print_delta_time(t1, 'Start write peptab !')

    peptab = open(quant_dir + str(csvname) + '.peptab', 'w')
    # peptab = open('/tmp/' + str(csvname) + '.peptab', 'w')
    writer = csv.writer(peptab, delimiter='\t')
    title = ['Sequence', 'Modification', 'accessions', 'Symbol']
    for repeat in repeatList:
        title.append(repeat + '_area')
        title.append(repeat + '_mz')
        title.append(repeat + '_rt')
        title.append(repeat + '_psms')
    tempk = [str(item) for item in title]
    tempk.append('index')
    writer.writerow(tempk)

    if not compare:
        i = 0
        for pep in pepList:
            tempk = []
            (seq, modi) = list(pep)
            tempk.extend([seq, modi])
            pep2pro[i] = list(set(pep2pro[i]))
            tempk.append(set2str(pep2pro[i]))
            tempk.append(set2str(pep2gen[i]))
            for j in range(repeatLENGTH):
                (area, mz, rt, psms) = pepTable[j][i]
                tempk.extend([area, mz, rt, psms])
            tempk = [str(item) for item in tempk]
            tempk.append(str(i))
            writer.writerow(tempk)
            i = i + 1

    else:
        i = -1
        for pep in pepList:
            i += 1
            tempk = []
            (seq, modi) = list(pep)
            seq_mod = seq + '_' + modi
            tempk.extend([seq, modi])
            tempk.append(';'.join(sorted(set(pep2pro[i]))))
            tempk.append(';'.join(sorted(pep2gen[i])))
            for j in range(repeatLENGTH):
                (area, fot, rt, mz, psms,
                 ionscore) = list_peptide_dicts[j][seq_mod]
                tempk.extend([area, mz, rt, psms])
            tempk = [str(item) for item in tempk]
            tempk.append(str(i))
            writer.writerow(tempk)
            # continue
    peptab.close()

    print_delta_time(t1, 'Start write protab !')

    protab = open(quant_dir + str(csvname) + '.protab', 'w')
    writer = csv.writer(protab, delimiter='\t')
    title = ['accessions', 'Symbol', 'Description', 'annotation']
    for repeat in repeatList:
        title.append(repeat + '_area')
        title.append(repeat + '_fot')
        title.append(repeat + '_ibaq')
        title.append(repeat + '_psms')
    title.append('peptide')
    tempk = [str(item) for item in title]
    writer.writerow(tempk)

    i = 0
    for pro in proList:

        tempk = []
        (acc, sym, des) = list(pro)
        if acc in proAnno:
            tempk.extend([acc, sym, des])
            tempk.append(proAnno[acc])
            for j in range(repeatLENGTH):
                (area, fot, ibaq, psms) = proTable[j][i]
                tempk.extend([area, fot, ibaq, psms])
            tempk.append(set2str(proTable[-1][i]))
            tempk = [str(item) for item in tempk]
            writer.writerow(tempk)
        i = i + 1

    print_delta_time(t1, 'Start write genetab !')

    genetab = open(quant_dir + str(csvname) + '.genetab', 'w')
    writer = csv.writer(genetab, delimiter='\t')
    title = ['geneID', 'Symbol', 'Description', 'annotation']
    for repeat in repeatList:
        title.append(repeat + '_area')
        title.append(repeat + '_fot')
        title.append(repeat + '_ibaq')
        title.append(repeat + '_psms')
    title.append('peptide')
    tempk = [str(item) for item in title]
    writer.writerow(tempk)
    i = 0

    for gene in geneList:

        tempk = []
        (gene_id, symbol, description) = list(gene)
        if symbol in geneAnno:
            tempk.extend([gene_id, symbol, description])
            tempk.append(geneAnno[symbol])
            for j in range(repeatLENGTH):
                (area, fot, ibaq, psms) = geneTable[j][i]
                tempk.extend([area, fot, ibaq, psms])
            tempstr = ''
            for tempi in set(geneTable[-1][i]):
                tempstr = tempstr + str(tempi) + ';'
            tempk.append(tempstr[:-1])
            tempk = [str(item) for item in tempk]
            writer.writerow(tempk)
        i = i + 1
        # continue

    return 0


def getPcaMetadata(data_source, parameters, ncol_ds):
    conditionLevels = parameters['conditionLevels']
    dict_repeat2expname = parameters['repeat2expname']
    cLDict = {}
    for cond_exp in conditionLevels:
        cond, exp = cond_exp.split('|')
        cond = cond.replace('#', '"#"')
        for e in exp.split(';'):
            expName = dict_repeat2expname[e]
            cLDict[expName] = cond

    metadata_matrix = []
    ''' species;dateOfExperiment;dateOfOperation;instrument;method;separation;sex;age;reagent;sample;genotype;strain '''
    metadata_matrix.append(['expName', 'condition', 'species', 'instrument', 'dateOfExperiment',
                            'dateOfOperation', 'method', 'separation', 'sex', 'age',
                            'reagent', 'sample', 'tissueType', 'strain', 'circ_time'])
    for colNumber in range(1, ncol_ds):
        expName = data_source[0][colNumber]

        if not expName.startswith('Exp'):
            return (metadata_matrix, [])
            # tmp = [ expName ] + [''] * (len(metadata_matrix[0]) - 1)

        else:
            obj_sample = experiments.models.Experiment.objects.get(
                name=expName).samples.all()[0]
            sample = obj_sample.id
            try:
                obj_reagent = experiments.models.Experiment.objects.get(
                    name=expName).reagents.all()[0]
                reagent = obj_reagent.id
            except:
                reagent = 'NA'

            taxID = experiments.models.Experiment.objects.get(
                name=expName).taxid
            instru = experiments.models.Experiment.objects.get(
                name=expName).instrument_name_id
            dateOfExp = experiments.models.Experiment.objects.get(
                name=expName).date
            dateOfOper = obj_sample.date
            method = obj_sample.ubi_methods.all()[0].id
            separation = experiments.models.Experiment.objects.get(
                name=expName).separation

            '''
            source_tissue
            system = sample.source_tissue.tissueSystem.name
            organ = sample.source_tissue.tissueOrgan.name
            status = sample.source_tissue.tissueType.name
            circ_time = sample.source_tissue.circ_time
            
            source_cell
            cell_type = sample.source_cell.cellType.name
            cell_name = sample.source_cell.cellName.name
            circ_time = sample.source_cell.circ_time
            
            source_fluid
            fluid_or_excreta = sample.source_fluid.fluid.name
            
            source_others
            others = sample.source_others.name
 
            '''
            sex = ''
            age = ''
            tissueType = ''
            strain = ''
            circ_time = ''

            if obj_sample.source_tissue:
                sex = obj_sample.source_tissue.gender.name
                age = obj_sample.source_tissue.age
                tissueType = obj_sample.source_tissue.tissueType.name
                strain = obj_sample.source_tissue.tissueStrain.name
                circ_time = obj_sample.source_tissue.circ_time
            elif obj_sample.source_cell:
                sex = ''
                age = ''
                tissueType = obj_sample.source_cell.cellType.name
                strain = obj_sample.source_cell.tissueStrain.name
                circ_time = obj_sample.source_cell.circ_time
            elif obj_sample.source_fluid:
                pass
            else:
                pass

            tmp = []
            tmp.append(expName)
            if conditionLevels:
                tmp.append(cLDict[expName])
            else:
                tmp.append('Condition_1')
            tmp.append(str(taxID))
            tmp.append(str(instru))
            tmp.append(str(dateOfExp))
            tmp.append(str(dateOfOper))
            tmp.append(str(method))
            tmp.append(str(separation))
            tmp.append(str(sex))
            tmp.append(str(age))
            tmp.append(str(reagent))
            tmp.append(str(sample))
            tmp.append(str(tissueType))
            tmp.append(str(strain))
            tmp.append(str(circ_time))

        for i in range(len(tmp)):
            if not tmp[i]:
                tmp[i] = 'NA'
        metadata_matrix.append(tmp)

    ''' For json back to front '''
    dataMeta = []

    colNames = metadata_matrix[0]
    for idx in range(1, len(metadata_matrix)):
        tmp = {}
        for i in range(len(colNames)):
            tmp[colNames[i]] = metadata_matrix[idx][i]
        dataMeta.append(tmp)

    return (metadata_matrix, dataMeta)


def newcmp_protein(request):

    def getGOtxtSymbol(goTxt):
        ds = [['Symbol']]
        goTxt = goTxt[:-1] if goTxt.endswith(';') else goTxt
        geneList = goTxt.split(';')
        for g in geneList:
            ds.append([g])
        return ds

    def getGOtxtArea(goTxt, data_source):
        ds = set()
        goTxt = goTxt[:-1] if goTxt.endswith(';') else goTxt
        geneList = goTxt.split(';')
        for g in geneList:
            ds.add(g)

        tmpDS = [data_source[0]]
        for d in data_source[1:]:
            if d[0] in ds:
                tmpDS.append(d)

        return tmpDS

    if 'id' in request.POST:
        httpParamDict = request.POST

    else:
        httpParamDict = request.GET

    csvname = httpParamDict['id']
    cont = XsearchTable.objects.get(id=csvname)

    temp_name = httpParamDict[
        'temp_name'] if 'temp_name' in httpParamDict else ''

    if 'gridType' not in httpParamDict:
        gridType = cont.ProGene
    else:
        gridType = httpParamDict['gridType'] if httpParamDict[
            'gridType'] in ['protein', 'gene', 'peptide'] else cont.ProGene
    # expNum = httpParamDict['expNum'] if 'expNum' in httpParamDict else 4
    print gridType
    if gridType == 'protein':
        ProFileName = quant_dir + csvname + temp_name + '.protab'
    elif gridType == 'gene':
        ProFileName = quant_dir + csvname + temp_name + '.genetab'
    else:
        ProFileName = quant_dir + csvname + temp_name + '.peptab'

    """ If the server has to restart and some calculation stopped, just switch 'running' to 'new' """
    type = httpParamDict['type'] if 'type' in httpParamDict else 0
    if type:  # type=1 means this request is from menu button
        # return HttpResponse('Job done')
        job_status = cont.status

        if 'rerun' in httpParamDict:
            tempFileName = ProFileName.replace(quant_dir, '/dev/shm/') + '.npy'
            if os.path.isfile(tempFileName):
                os.remove(tempFileName)
            job_status = NEW

        if job_status == DONE:
            if not os.path.exists(ProFileName):
                # cont.status = ERROR
                cont.save()
                return HttpResponse('Error,no file')
            else:
                return HttpResponse('Job done')

        elif job_status == NEW:
            cont.status = RUNNING
            cont.save()
            newcmp_calc(csvname)
            cont = XsearchTable.objects.get(id=int(csvname))
            if not os.path.exists(ProFileName):
                cont.status = ERROR
                cont.save()
                return HttpResponse('Job failed')
            else:
                cont.status = DONE
                cont.save()
                return HttpResponse('Job done')

        elif job_status == RUNNING:
            return HttpResponse('Job is running')

        else:
            return HttpResponse('Job failed')
    # type=0 means this request is from store of Notice.js
    if not os.path.exists(ProFileName):
        cont.status = ERROR
        cont.save()
        return HttpResponse('Error,no file')
    tempFileName = ProFileName.replace(quant_dir, '/dev/shm/') + '.npy'
    if not os.path.isfile(tempFileName):
        prodata = np.genfromtxt(ProFileName, delimiter='\t', names=True, dtype=None)
        np.save(tempFileName, prodata)

    prodata = np.load(tempFileName)
    print prodata.dtype.names
    # print my_timer(t1)
    titles = list(prodata.dtype.names)
    fields = []
    fields.append({'name': 'id', 'type': 'int'})
    fields.append({'name': 'co', 'type': 'int'})
    fields.append({'name': 'ki', 'type': 'int'})
    fields.append({'name': 'li', 'type': 'int'})
    fields.append({'name': 're', 'type': 'int'})
    fields.append({'name': 'pmm', 'type': 'int'})
    fields.append({'name': 'pmh', 'type': 'int'})
    fields.append({'name': 'tf', 'type': 'int'})
    fields.append({'name': 'Acetyl', 'type': 'int'})
    fields.append({'name': 'Methyl', 'type': 'int'})
    fields.append({'name': 'GlyGly', 'type': 'int'})
    fields.append({'name': 'Biotin', 'type': 'int'})
    fields.append({'name': 'PhosphoST', 'type': 'int'})
    fields.append({'name': 'PhosphoY', 'type': 'int'})
    #=========================================================================
    # fields.append({'name': 'average', 'type': 'float'})
    # fields.append({'name': 'median', 'type': 'float'})
    # fields.append({'name': 'var', 'type': 'float'})
    #=========================================================================
    for title in titles:
        temp = {}
        temp['name'] = title
        if title in ['accessions', 'Symbol', 'Description', 'peptide', 'annotation', 'Sequence', 'Modification']:
            temp['type'] = 'string'
        else:
            temp['type'] = 'float'

        fields.append(temp)
        if 'area' in title:
            temp = {}
            temp['type'] = 'float'
            temp['name'] = title.replace('area', 'ratio')
            fields.append(temp)
    data = []
    try:  # direciton means reverse or not
        sort = json.loads(str(httpParamDict['sort'])[1:-1])
        property = str(sort['property'])
        direction = True if sort['direction'] == 'DESC' else False

    except:
        property = "accessions"
        direction = False

    try:
        # print str(httpParamDict['columns'])+'123'
        columns = httpParamDict.getlist('columns')
        # print columns
        if '^' in columns[0]:
            columns = columns[0]
            columns = columns.split('^')
    except:
        columns = []
    # print columns
    Normalize = False
    if 'Normalize' in httpParamDict:
        Normalize = httpParamDict['Normalize']
        if Normalize == 'true':
            Normalize = True
        else:
            Normalize = False
        print Normalize

    normalizationLevel = 'none_none'
    if 'normalizationLevel' in httpParamDict:
        normalizationLevel = httpParamDict['normalizationLevel']
        if normalizationLevel == '':
            normalizationLevel = 'none_none'
        # print normalizationLevel

    #=========================================================================
    # temp_name = 'area'
    # for mm in prodata.dtype.names:
    #     if temp_name in mm:
    #         temp_namelist.append(mm)
    # for i in range(len(list(prodata[temp_namelist[0]]))):
    #     temp_list = []
    #     for mm in temp_namelist:
    #         if prodata[mm][i] != -1:
    #             temp_list.append(prodata[mm][i])
    #         else:
    #             temp_list.append(0)
    #     average.append(np.mean(temp_list))
    #     medium.append(np.median(temp_list))
    #     var.append(np.var(temp_list))
    # prodata = rfn.append_fields(prodata, 'average', data=np.array(average), usemask=False)
    #     # prodata=np.concatenate((prodata,pvalue_list.T),axis=1)
    # titles.append('average')
    # prodata = rfn.append_fields(prodata, 'medium', data=np.array(medium), usemask=False)
    #     # prodata=np.concatenate((prodata,pvalue_list.T),axis=1)
    # titles.append('medium')
    # prodata = rfn.append_fields(prodata, 'var', data=np.array(var), usemask=False)
    #     # prodata=np.concatenate((prodata,pvalue_list.T),axis=1)
    # titles.append('var')
    #=========================================================================
    for column in columns:
        average = []
        median = []
        var = []
        temp_namelist = []
        if ';' in column and 'VS' not in column:
            column_data = column.split(';')
            if column_data[0] not in titles:
                continue
            if 'area' in column or 'fot' in column or 'ibaq' in column:
                statisticalMethod = httpParamDict['statistical']
                temp_namelist = column_data
                for i in range(len(list(prodata[temp_namelist[0]]))):
                    temp_list = []
                    for mm in temp_namelist:
                        if prodata[mm][i] != -1:
                            temp_list.append(prodata[mm][i])
                        else:
                            temp_list.append(0)
                    if statisticalMethod == 'avg':
                        average.append(np.mean(temp_list))
                    else:
                        average.append(np.median(temp_list))
                prodata = rfn.append_fields(prodata, str(
                    column), data=np.array(average), usemask=False)
                titles.append(column)
                fields.append({'name': column, 'type': 'float'})
            else:
                temp_namelist = column_data
                for i in range(len(list(prodata[temp_namelist[0]]))):
                    temp_list = []
                    for mm in temp_namelist:
                        if prodata[mm][i] != -1:
                            temp_list.append(prodata[mm][i])
                        else:
                            temp_list.append(0)
                    average.append(np.sum(temp_list))
                prodata = rfn.append_fields(prodata, str(
                    column), data=np.array(average), usemask=False)
                titles.append(column)
                fields.append({'name': column, 'type': 'float'})

    for column in columns:
        if '_vs_' in column:
            (a, b) = column.split('_vs_')
            ctrl_list = list(prodata[b])
            expr_list = list(prodata[a])
            ratio_list, inten_list = signif.refine_data(ctrl_list, expr_list)
            pvalue_list = signif.signif(ratio_list, inten_list)

            # pvalue_list=np.array(pvalue_list)
            prodata = rfn.append_fields(prodata, str(
                column), data=np.array(pvalue_list), usemask=False)
            # prodata=np.concatenate((prodata,pvalue_list.T),axis=1)
            titles.append(column)
            fields.append({'name': column, 'type': 'float'})
        elif 'VS' in column:
            # return HttpResponse(column)
            (a, b) = column.split('VS')
            ctrl_list = list(prodata[b])
            expr_list = list(prodata[a])
#             ratio_list, inten_list = signif.refine_data(ctrl_list,expr_list)
#             pvalue_list = signif.signif(ratio_list, inten_list)
            ratio_list = []
            for i in range(len(ctrl_list)):
                if float(ctrl_list[i]) == float(expr_list[i]):
                    ans = 1
                elif float(ctrl_list[i]) == 0 or float(ctrl_list[i]) == -1:
                    ans = 1e9
                elif float(expr_list[i]) == -1:
                    ans = 0
                else:
                    ans = expr_list[i] / ctrl_list[i]
                ratio_list.append(ans)

            # pvalue_list=np.array(pvalue_list)
            prodata = rfn.append_fields(prodata, str(
                column), data=np.array(ratio_list), usemask=False)
            # prodata=np.concatenate((prodata,pvalue_list.T),axis=1)
            titles.append(column)
            fields.append({'name': column, 'type': 'float'})

    try:
        filters = json.loads(httpParamDict['filter'])
    except:
        filters = []
    oldFieldName = ''
    secondFilter = 0
    temp = np.ones(prodata.size)
    temp1 = np.ones(prodata.size)
    if len(filters) != 0:
        for filter_num1 in range(len(filters)):
            for filter_num2 in range(filter_num1, len(filters)):
                if filters[filter_num1]['field'] < filters[filter_num2]['field']:
                    temp_num = filters[filter_num1]
                    filters[filter_num1] = filters[filter_num2]
                    filters[filter_num2] = temp_num

        for filter in filters:
            if filter['field'] != oldFieldName:
                if secondFilter == 3:
                    for i in range(len(temp)):
                        if temp1[i] == 1:
                            temp[i] = 1
                elif secondFilter == 2:
                    temp = temp1
                # print temp
                # print prodata
                prodata = prodata[temp == 1]
                # print prodata
                oldFieldName = filter['field']
                temp = np.ones(prodata.size)
                temp1 = np.ones(prodata.size)
                secondFilter = 0
            if filter['type'] == 'list':
                for anno in filter['value']:
                    # temp = np.zeros(prodata.size)
                    i = 0
                    for line in prodata:
                        if anno not in line['annotation']:
                            temp[i] = 0
                        i = i + 1
                    # prodata=prodata[temp==1]
            if filter['type'] == 'string':
                field = titles.index(filter['field'])
                # temp = np.zeros(prodata.size)
                i = 0
                for line in prodata:
                    if filter['value'].upper() not in line[filter['field']].upper():
                        temp[i] = 0
                    i = i + 1
                # prodata = prodata[temp == 1]

            if filter['type'] == 'numeric':
                # field = titles.index(filter['field'])
                if filter['comparison'] == 'lt' or filter['comparison'] == 'lt2':
                    # temp = np.zeros(prodata.size)
                    i = 0
                    for line in prodata:
                        if filter['field'] in titles:
                            if filter['value'] <= line[filter['field']]:
                                if filter['comparison'] == 'lt':
                                    temp[i] = 0
                                    secondFilter = secondFilter | 1
                                elif filter['comparison'] == 'lt2':
                                    temp1[i] = 0
                                    secondFilter = secondFilter | 2
                        else:
                            [case, control] = str(filter['field']).split('VS')
                            if line[control] == 0 or line[control] == -1:
                                if filter['comparison'] == 'lt':
                                    temp[i] = 0
                                    secondFilter = secondFilter | 1
                                elif filter['comparison'] == 'lt2':
                                    temp1[i] = 0
                                    secondFilter = secondFilter | 2
                            elif filter['value'] <= line[case] / line[control]:
                                if filter['comparison'] == 'lt':
                                    temp[i] = 0
                                    secondFilter = secondFilter | 1
                                elif filter['comparison'] == 'lt2':
                                    temp1[i] = 0
                                    secondFilter = secondFilter | 2
                        i = i + 1
                    # prodata = prodata[temp == 1]
                if filter['comparison'] == 'eq' or filter['comparison'] == 'eq2':
                    # temp = np.zeros(prodata.size)
                    i = 0
                    for line in prodata:
                        if filter['field'] in titles:
                            if filter['value'] != line[filter['field']]:
                                if filter['comparison'] == 'eq':
                                    temp[i] = 0
                                    secondFilter = secondFilter | 1
                                elif filter['comparison'] == 'eq2':
                                    temp1[i] = 0
                                    secondFilter = secondFilter | 2
                        else:
                            [case, control] = str(filter['field']).split('VS')
                            # a=line[case]
                            # b=line[control]
                            if line[control] == 0 or line[control] == -1:
                                if filter['comparison'] == 'eq':
                                    temp[i] = 0
                                    secondFilter = secondFilter | 1
                                elif filter['comparison'] == 'eq2':
                                    temp1[i] = 0
                                    secondFilter = secondFilter | 2
                            elif line[case] == 0 or line[case] == -1:
                                if filter['comparison'] == 'eq':
                                    temp[i] = 0
                                    secondFilter = secondFilter | 1
                                elif filter['comparison'] == 'eq2':
                                    temp1[i] = 0
                                    secondFilter = secondFilter | 2
                            elif filter['value'] != line[case] / line[control]:
                                if filter['comparison'] == 'eq':
                                    temp[i] = 0
                                    secondFilter = secondFilter | 1
                                elif filter['comparison'] == 'eq2':
                                    temp1[i] = 0
                                    secondFilter = secondFilter | 2
                        i = i + 1
                    # prodata = prodata[temp == 1]
                if filter['comparison'] == 'gt'or filter['comparison'] == 'gt2':
                    # temp = np.zeros(prodata.size)
                    i = 0
                    for line in prodata:
                        if filter['field'] in titles:
                            if filter['value'] >= line[filter['field']]:
                                if filter['comparison'] == 'gt':
                                    temp[i] = 1
                                    secondFilter = secondFilter | 1
                                elif filter['comparison'] == 'gt2':
                                    temp1[i] = 1
                                    secondFilter = secondFilter | 2
                        else:
                            [case, control] = str(filter['field']).split('VS')
                            a = line[case]
                            b = line[control]
                            if line[case] == 0 or line[case] == -1:
                                if filter['comparison'] == 'gt':
                                    temp[i] = 0
                                    secondFilter = secondFilter | 1
                                elif filter['comparison'] == 'gt2':
                                    temp1[i] = 0
                                    secondFilter = secondFilter | 2
                            elif line[control] == 0 or line[control] == -1:
                                if filter['comparison'] == 'gt':
                                    temp[i] = 0
                                    secondFilter = secondFilter | 1
                                elif filter['comparison'] == 'gt2':
                                    temp1[i] = 0
                                    secondFilter = secondFilter | 2
                            elif filter['value'] >= line[case] / line[control]:
                                if filter['comparison'] == 'gt':
                                    temp[i] = 0
                                    secondFilter = secondFilter | 1
                                elif filter['comparison'] == 'gt2':
                                    temp1[i] = 0
                                    secondFilter = secondFilter | 2
                        i = i + 1
                    # prodata = prodata[temp == 1]
        # print secondFilter
        if secondFilter == 3:
            for i in range(len(temp)):
                if temp1[i] == 1:
                    temp[i] = 1
        elif secondFilter == 2:
            temp = temp1
        prodata = prodata[temp == 1]
        temp = np.ones(prodata.size)
        temp1 = np.ones(prodata.size)
    # if Normalize:
    if 'none' not in normalizationLevel:
        # print 'yes'
        level = httpParamDict.getlist('levels')
        level = [p.split('|')[1] for p in level]
        newLevel = []
        for lev in level:
            newLevel.extend(lev.split(';'))
        level = newLevel
        tempMatrix = [[] for i in range(len(level))]
        for line in prodata:
            empty = False
            for ele in range(len(level)):
                if float(line[level[ele]]) == 0 or float(line[level[ele]]) == -1.0:
                    empty = True
            if empty:
                continue
            for ele in range(len(level)):
                tempMatrix[ele].append(float(line[level[ele]]))
        minMedian = 0
        selectMedian = 0
        for i in range(len(level)):
            if minMedian < np.median(tempMatrix[i]):
                minMedian = np.median(tempMatrix[i])
                selectMedian = i
        for line in range(len(prodata)):
            for ele in range(len(level)):
                if prodata[line][level[ele]] == 0 or prodata[line][level[ele]] == -1:
                    continue
                prodata[line][level[ele]] = float(prodata[line][
                                                  level[ele]]) / np.median(tempMatrix[ele]) * np.median(tempMatrix[selectMedian])

    if property in titles:
        prodata.sort(order=property)
    elif 'VS' in property:
        (a, b) = property.split('VS')
        ctrl_list = list(prodata[b])
        expr_list = list(prodata[a])
        ratio_list = []
        for i in range(len(ctrl_list)):
            if float(ctrl_list[i]) == 0 or float(ctrl_list[i]) == -1:
                ans = 1e9
            elif float(expr_list[i]) == -1:
                ans = 0
            else:
                ans = expr_list[i] / ctrl_list[i]
            ratio_list.append(ans)
        prodata = rfn.append_fields(prodata, str(
            property), data=np.array(ratio_list), usemask=False)
        titles.append(property)
        fields.append({'name': property, 'type': 'float'})
        prodata.sort(order=property)
    #=========================================================================
    # if 'Normalize' in httpParamDict:
    #     Normalize=httpParamDict['Normalize']
    #     if Normalize=='true':
    #         level=httpParamDict.getlist('level')
    #         tempMatrix=[[] for i in range(len(level))]
    #     for line in prodata:
    #         if -1.0 in line or 0 in line:
    #             continue
    #         for ele in range(len(line)):
    #             if ele==0:
    #                 tempMatrix[ele].append(line[ele])
    #             else:
    #                 tempMatrix[ele].append(float(line[ele]))
    #=========================================================================

    if direction:
        prodata = prodata[::-1]
    try:
        start = int(httpParamDict['start'])
    except:
        start = 0
    try:
        limit = int(httpParamDict['limit'])
    except:
        limit = -1
    end = start + limit
    count = prodata.size
    if count < end or limit == -1:
        end = count

    if 'download' in httpParamDict:
        download = httpParamDict['download']
    else:
        download = False

    if download == 'yes':
        return newcmp_download(prodata, columns)

    if 'R_type' in httpParamDict:
        rType = httpParamDict['R_type']
    else:
        rType = ''

    if rType != '':
        data_source = []
        tempTitle = []
        if gridType != 'peptide':
            tempTitle.append('Symbol')
        else:
            tempTitle.append('Symbol')

        levels = httpParamDict.getlist('levels')

        if rType == 'venn':
            vennExp = httpParamDict.getlist('vennExp')
            levels = vennExp

        elif rType == 'volcano':
            controlExp = httpParamDict['controlExp']
            #==================================================================
            # temp = controlExp.split('_')
            # (type, expName, rank, repe) = (temp[0], int(temp[1]), int(temp[2]), int (temp[3]))
            # controlExp = Experiment.objects.get(id=expName).name
            #==================================================================
            caseExp = httpParamDict['caseExp']
            #==================================================================
            # temp = caseExp.split('_')
            # (type, expName, rank, repe) = (temp[0], int(temp[1]), int(temp[2]), int (temp[3]))
            # caseExp = Experiment.objects.get(id=expName).name
            #==================================================================
            levels = []
            levels.append(httpParamDict['caseExp'])
            levels.append(httpParamDict['controlExp'])

        elif rType == 'tf-tg':
            controlExp = httpParamDict['controlExp']
            caseExp = httpParamDict['caseExp']
            levels = []
            levels.append(httpParamDict['caseExp'])
            levels.append(httpParamDict['controlExp'])
            if '<br>' in levels[0]:
                for level_num in range(len(levels)):
                    tmp_str = levels[level_num]
                    levels[level_num] = '|'.join(
                        [tmp_str.split('<br>')[0], tmp_str.split('|')[1]])

        elif rType == 'kinaseSubstrate':
            controlExp = httpParamDict['controlExp']
            caseExp = httpParamDict['caseExp']
            levels = []
            levels.append(httpParamDict['caseExp'])
            levels.append(httpParamDict['controlExp'])
            if '<br>' in levels[0]:
                for level_num in range(len(levels)):
                    tmp_str = levels[level_num]
                    levels[level_num] = '|'.join(
                        [tmp_str.split('<br>')[0], tmp_str.split('|')[1]])

        elif rType == 'k-heatmap':
            kNum = int(float(httpParamDict['k_num']))

            if 'expList' in httpParamDict:
                levels = httpParamDict.getlist('expList')
                if '<br/>' in levels[0]:
                    for level_num in range(len(levels)):
                        tmp_str = levels[level_num]
                        tmp_str = tmp_str.split('|')
                        tmp_str[0] = tmp_str[0].split('<br/>')[0]
                        levels[level_num] = '|'.join(tmp_str)
        elif rType == 'kegg':
            species = httpParamDict['species']
        # print levels
        #======================================================================
        # for title in titles:
        #     if 'area' in title:
        #         tempTitle.append(title)
        #======================================================================

        # species = 'mmu'
        allSymbol = {}
        # print 'LEVEL:\n',levels
        # return 0
        '''  genebox start '''
        if rType == 'genebox':
            for level in levels:
                tmp = level.split("|")
                exp_units = tmp[1][:-1] if tmp[1].endswith(';') else tmp[1]
                exp_units = exp_units.split(';')
                for e in exp_units:
                    tempTitle.append(tmp[0] + '|' + e)
            data_source.append(tempTitle)
            # print 'LEVEL:\n',data_source
            # return
            for line in prodata:
                temp = []
                empty = False
                for title in tempTitle:  # Group1_Condition1|repeat_1158_1_1_area;repeat_1157_1_1_area;
                    if '|' not in title:
                        if gridType != 'peptide':
                            temp.append(line[title])
                        else:
                            temp.append(line['Sequence'] +
                                        '_' + line['Modification'])
                    else:
                        temp_value = []
                        tmpExp = title.split('|')[1]
                        if line[tmpExp] != '':
                            temp_value.append(line[tmpExp])
                        else:
                            empty = True
                            break
                        temp.extend(temp_value)
                if not empty:  # Every column has data
                    if temp[0] not in allSymbol:
                        allSymbol[temp[0]] = len(allSymbol)
                        data_source.append(temp)
                    else:
                        temp_idx = allSymbol[temp[0]]
                        for i in range(1, len(temp)):
                            data_source[temp_idx + 1][i] += temp[i]
            ''' Replace repeat_1158_1_1_area to Exp001011...... '''
            ncol_ds = len(data_source[0])
            for pp in range(ncol_ds):
                data_source[0][pp] = data_source[0][pp].split('|')[0]
                if 'repeat' in data_source[0][pp]:
                    temp = data_source[0][pp].split('_')
                    (type, exp_id, rank, repe) = (temp[0], int(
                        temp[1]), int(temp[2]), int(temp[3]))
                    data_source[0][pp] = Experiment.objects.get(id=exp_id).name

            tmpHtml, tmpPng, tmpPdf = pathway.Rplot5(data_source, rType)
            res = {"tmpHtml": tmpHtml, "png": tmpPng, "pdf": tmpPdf}
            result = json.dumps(res, cls=DjangoJSONEncoder)

            return HttpResponse(result)

        '''  genebox end '''

        statisticalMethod = httpParamDict[
            'statistical'] if 'statistical' in httpParamDict else ''

        for level in levels:
            tempTitle.append(level)
        data_source.append(tempTitle[:])

        ''' Transelate repeat*** to Exp*** '''
        dict_repeat2expname = {}
        ncol_ds = len(data_source[0])
        for pp in range(ncol_ds):
            data_source[0][pp] = data_source[0][pp].split('|')[0]
            if 'repeat' in data_source[0][pp]:
                temp = data_source[0][pp].split('_')
                (type, exp_id, rank, repe) = (temp[0], int(
                    temp[1]), int(temp[2]), int(temp[3]))
                expName = Experiment.objects.get(id=exp_id).name
                dict_repeat2expname[data_source[0][pp]] = expName
                data_source[0][pp] = expName

        ''' Just for getting Metadata Matrix, so skip prodata ^ ^ '''
        if 'forMetaMatrix' in httpParamDict:
            parameters = {}
            parameters['conditionLevels'] = []
            parameters['repeat2expname'] = dict_repeat2expname
            metadata_matrix, dataMeta = getPcaMetadata(
                data_source, parameters, ncol_ds)
            result = json.dumps({"dataMeta": dataMeta})
            return HttpResponse(result)

        for line in prodata:
            temp = []
            empty = False
            for title in tempTitle:  # Group1_Condition1|repeat_1158_1_1_area;repeat_1157_1_1_area;
                if '|' not in title:
                    if gridType != 'peptide':
                        temp.append(line[title])
                    else:
                        temp.append(line['Sequence'] + '_' +
                                    line['Modification'])
                else:
                    temp_value = []
                    # print title
                    tmpExps = title.split('|')[1]
                    tmpExps = tmpExps[
                        :-1] if tmpExps.endswith(';') else tmpExps
                    print tmpExps
                    print prodata.dtype.names
                    for tmpExp in tmpExps.split(';'):
                        if line[tmpExp] != '':
                            temp_value.append(line[tmpExp])
                        else:
                            empty = True
                            break
                    # temp.append(np.median(temp_value))
                    temp.append((temp_value))
            if not empty:
                if temp[0] not in allSymbol:
                    allSymbol[temp[0]] = len(allSymbol)
                    data_source.append(temp)
                else:
                    tmpSymbolRowNum = allSymbol[temp[0]]
                    for i in range(1, len(temp)):
                        # data_source[temp_symbol][i] += temp[i]
                        ''' data_source = [ ['a','b','c'],[ [1,2,3],[2,2,2],[2,1,1] ], ...  ] '''
                        data_source[tmpSymbolRowNum + 1][i].extend(temp[i])

        ''' for group or condition level, combine datas in same group or condition '''
        for line in range(1, len(data_source)):
            for ele in range(1, len(data_source[line])):
                if statisticalMethod == 'Average':
                    data_source[line][ele] = np.mean(data_source[line][ele])
                else:
                    data_source[line][ele] = np.median(data_source[line][ele])

        # print data_source
        data_source_copy = data_source
        tempTitle_copy = tempTitle

        # print data_source
        parameters = {}
        parameters['rType'] = rType

        if rType == 'PPI':
            print "ppi"
            expLength = 4
            expLength = int(request.GET["expNum"])
            cutoff = int(request.GET["cutoff"])
            initLoc = 5
            step = 4
            prodata_lst = []
            prodata_temp_lst = []
            prodata_temp_need_lst = []
            gi_lst = []
            geneSymbol_lst = []

            for prodata_line in prodata:
                for element in prodata_line:
                    prodata_temp_lst.append(element)
                prodata_temp_need_lst.append(prodata_temp_lst[0])
                geneSymbol = prodata_temp_lst[1]
                if geneSymbol == "":
                    geneSymbol = "NULL"
                prodata_temp_need_lst.append(geneSymbol)
                # prodata_temp_need_lst.append(prodata_temp_lst[1])
                # gi_lst.append(prodata_temp_lst[0])
                # geneSymbol_lst.append(prodata_temp_lst[1])
                for index in range(expLength):
                    loc = initLoc + index * step
                    value = prodata_temp_lst[loc]
                    if value == -1:
                        value = 0
                    else:
                        value = value
                    prodata_temp_need_lst.append(value)
#                 prodata_temp_need_lst.append(prodata_temp_lst[5])
#                 prodata_temp_need_lst.append(prodata_temp_lst[9])
#                 prodata_temp_need_lst.append(prodata_temp_lst[13])
#                 prodata_temp_need_lst.append(prodata_temp_lst[17])
                prodata_lst.append(prodata_temp_need_lst)
                prodata_temp_lst = []
                prodata_temp_need_lst = []

            # pathway.Rplot1
            parameters["expLength"] = expLength
            parameters["cutoff"] = cutoff
            datasource = prodata_lst
            # outJsonDict = pathway.Rplot1(gi_lst, geneSymbol_lst, datasource, parameters)
            outJsonDict = pathway.Rplot1(datasource, parameters)
            # print s
            # data = {"prodata_lst":prodata_lst,"code":outJsonDict['code']}
            # "GRNListString":outJsonDict["GRNListString"],
            # "code":outJsonDict['code'],
            # "GRNListString":outJsonDict["GRNListString"],
            # gi_lst
            data = {"gi_lst_str": outJsonDict["gi_lst_str"], "resultString": outJsonDict[
                "resultString"], "GRNListString": outJsonDict["GRNListString"]}
            result = json.dumps(data, cls=DjangoJSONEncoder)
            return HttpResponse(result)
        # http://61.50.134.132/gardener/newcmpprotein/?id=310&R_type=PPI&organism=mouse&ontology=BP&goClassificationLevel=2&goTxt=None&temp_name=&gridType=protein&normalizationLevel=none_none

        elif rType == 'GOClassification':
            if httpParamDict['goTxt'] != 'None':
                data_source = getGOtxtSymbol(httpParamDict['goTxt'])
            # {u'goClassificationLevel': [u'1'], u'_dc': [u'1429504329241'], u'id': [u'213'], u'ontology': [u'BP'], u'R_type': [u'GoClassification']}
            # parameters['species'] = 'Homo sapiens (Human)' #
            # httpParamDict['pcList']
            parameters['organism'] = httpParamDict['organism']  # "mouse"#
            parameters['ont'] = httpParamDict['ontology']  # "MF" #
            parameters['level'] = httpParamDict['goClassificationLevel']

            tmpHtml, txtSummary, tmpPng, tmpPdf = pathway.Rplot6(
                data_source, parameters)

            tmpData = []
            if os.path.isfile(txtSummary):
                with open(txtSummary) as f:
                    f.readline()
                    for line in f:
                        line = line.strip().split('\t')

                        temp = {}
                        temp["ID"] = line[0]
                        temp["Description"] = line[1]
                        temp["Count"] = line[2]
                        temp["GeneRatio"] = line[3]
                        temp["geneID"] = line[4]

                        tmpData.append(temp)

            res = {"tmpHtml": tmpHtml, "data": tmpData, "total": len(
                tmpData), "png": tmpPng, "pdf": tmpPdf, 'data_source': data_source}
            result = json.dumps(res, cls=DjangoJSONEncoder)

            return HttpResponse(result)

        elif rType == 'GOEnrich':
            if httpParamDict['goTxt'] != 'None':
                data_source = getGOtxtSymbol(httpParamDict['goTxt'])
            # {u'_dc': [u'1429504360616'], u'id': [u'213'], u'ontology': [u'BP'], u'R_type': [u'GoEnrich']}
            parameters['organism'] = httpParamDict['organism']
            parameters['organism'] = "mouse"  # httpParamDict['pcList']
            parameters['ont'] = httpParamDict['ontology']  # "MF" #

            tmpHtml, txtSummary, tmpPng, tmpPdf = pathway.Rplot6(
                data_source, parameters)

            tmpData = []
            if os.path.isfile(txtSummary):
                with open(txtSummary) as f:
                    f.readline()
                    for line in f:
                        line = line.strip().split('\t')

                        temp = {}
                        temp["ID"] = line[0]
                        temp["Description"] = line[1]
                        temp["GeneRatio"] = line[2]
                        temp["BgRatio"] = line[3]
                        temp["pvalue"] = line[4]
                        temp["p.adjust"] = line[5]
                        temp["qvalue"] = line[6]
                        temp["geneID"] = line[7]
                        temp["Count"] = line[8]

                        tmpData.append(temp)

            res = {"tmpHtml": tmpHtml, "data": tmpData,
                   "total": len(tmpData), "png": tmpPng, "pdf": tmpPdf}
            result = json.dumps(res, cls=DjangoJSONEncoder)

            return HttpResponse(result)

        elif rType == 'kegg':
            if httpParamDict['goTxt'] != 'None':
                data_source = getGOtxtArea(httpParamDict['goTxt'], data_source)

            parameters['species'] = species
            return HttpResponse(pathway.kegg_pathview(data_source, parameters))

        elif rType == 'volcano':
            #==================================================================
            # parameters['controlExp']=controlExp.split('|')[0].replace('<br>','\n')
            # parameters['caseExp']=caseExp.split('|')[0].replace('<br>','\n')
            #==================================================================
            parameters['controlExp'] = controlExp.split('|')[0]
            parameters['caseExp'] = caseExp.split('|')[0]
            parameters['xlim'] = httpParamDict['xlim']
            parameters['ylim'] = httpParamDict['ylim']
            # return HttpResponse(pathway.Rplot2(data_source, rType, exp1,
            # exp2))

            outJsonDict = pathway.Rplot2(data_source, parameters)
            result = json.dumps(outJsonDict)

            return HttpResponse(result)

        elif rType == 'tf-tg':
            if httpParamDict['goTxt'] != 'None':
                data_source = getGOtxtArea(httpParamDict['goTxt'], data_source)

            #==================================================================
            # parameters['controlExp']=controlExp.split('|')[0].replace('<br>','\n')
            # parameters['caseExp']=caseExp.split('|')[0].replace('<br>','\n')
            #==================================================================
            parameters['caseExp'] = levels[0]  # caseExp.split('|')[0]
            parameters['controlExp'] = levels[1]  # controlExp.split('|')[0]
            # return HttpResponse(pathway.Rplot2(data_source, rType, exp1,
            # exp2))
            outJsonDict = pathway.Rplot2(data_source, parameters)
            result = json.dumps(outJsonDict)

            return HttpResponse(result)

        elif rType == 'kinaseSubstrate':
            if httpParamDict['goTxt'] != 'None':
                data_source = getGOtxtArea(httpParamDict['goTxt'], data_source)

            #==================================================================
            # parameters['controlExp']=controlExp.split('|')[0].replace('<br>','\n')
            # parameters['caseExp']=caseExp.split('|')[0].replace('<br>','\n')
            #==================================================================
            parameters['caseExp'] = levels[0]  # caseExp.split('|')[0]
            parameters['controlExp'] = levels[1]  # controlExp.split('|')[0]
            # return HttpResponse(pathway.Rplot2(data_source, rType, exp1,
            # exp2))
            outJsonDict = pathway.Rplot2(data_source, parameters)
            result = json.dumps(outJsonDict)

            return HttpResponse(result)

        elif rType == 'venn':
            for ven_num in range(len(vennExp)):
                vennExp[ven_num] = vennExp[ven_num].split('|')[0]
                # vennExp[ven_num]=vennExp[ven_num].replace('<br>','\n')
            parameters['vennExp'] = vennExp
            # return HttpResponse(pathway.Rplot2(data_source, rType, exp1,
            # exp2))

            outJsonDict = pathway.Rplot2(data_source, parameters)
            result = json.dumps(outJsonDict)

            return HttpResponse(result)

        elif rType == 'motif':
            outJsonDict = pathway.Rplot2(data_source, parameters)
            result = json.dumps(outJsonDict)

            return HttpResponse(result)

        elif rType == 'k-heatmap':
            parameters['kNum'] = kNum
            parameters['minValue'] = '#' + httpParamDict['minValue']
            parameters['maxValue'] = '#' + httpParamDict['maxValue']
            if 'cutoff' in httpParamDict:
                parameters['cutoff'] = httpParamDict['cutoff']
            if 'zscore' in httpParamDict:
                parameters['zscore'] = httpParamDict['zscore']
            if 'log' in httpParamDict:
                parameters['log'] = httpParamDict['log']
            # return HttpResponse(pathway.Rplot3(data_source, rType, kNum))
            outJsonDict = pathway.Rplot3(data_source, parameters)
            return HttpResponse(json.dumps(outJsonDict, cls=DjangoJSONEncoder))

        elif rType == 'pca':
            parameters['pcList'] = httpParamDict['pcList']
            parameters['conditionLevels'] = httpParamDict.getlist(
                'conditionLevels')
            parameters['repeat2expname'] = dict_repeat2expname
            parameters['metadataList'] = httpParamDict['metadataList'][:-1]
            parameters['adjust'] = 0

            metadata_matrix, dataMeta = getPcaMetadata(
                data_source, parameters, ncol_ds)

            dataCorMatrix = []

            (tmpHtml, tmpFile, tmpMetaFile, src_metadata, srcCorMatrixFile,
             imageSrc) = pathway.Rplot4(data_source, parameters, metadata_matrix)

            data = {"imageSrc": imageSrc, "tmpHtml": tmpHtml, "tmpFile": tmpFile, "tmpMetaFile": tmpMetaFile, 'tmpSrcMetadata': src_metadata, 'tmpSrcCorMatrixFile': srcCorMatrixFile,
                    "dataMeta": dataMeta, "dataCorMatrix": dataCorMatrix}
            result = json.dumps(data)
            return HttpResponse(result)

        elif rType == 'transfer':
            temp_name = '_' + str(int(time.time()))
            if gridType == 'protein':
                ProFileName = quant_dir + csvname + temp_name + '.protab'
            elif gridType == 'gene':
                ProFileName = quant_dir + csvname + temp_name + '.genetab'
            else:
                ProFileName = quant_dir + csvname + temp_name + '.peptab'
            tempfile = open(ProFileName, 'w')
            allSymbol = {}
            levels = httpParamDict.getlist('levels')
            for column in levels:
                average = []
                median = []
                var = []
                temp_namelist = []
                column_data = column.split('|')[1].split(';')[:-1]
                for mm in prodata.dtype.names:
                    if mm in column_data:
                        temp_namelist.append(mm)
                for i in range(len(list(prodata[temp_namelist[0]]))):
                    temp_list = []
                    for mm in temp_namelist:
                        if prodata[mm][i] != -1:
                            temp_list.append(prodata[mm][i])
                        else:
                            temp_list.append(0)
                    average.append(np.mean(temp_list))
                    median.append(np.median(temp_list))
                    var.append(np.var(temp_list))
                column = column + '|' + 'Average'
                prodata = rfn.append_fields(prodata, str(
                    column), data=np.array(average), usemask=False)
                titles.append(column)
                fields.append({'name': column, 'type': 'float'})
                prodata = rfn.append_fields(prodata, str(column.split(
                    '|')[0] + '|Median'), data=np.array(median), usemask=False)
                titles.append(column.split('|')[0] + '|Median')
                fields.append({'name': column.split(
                    '|')[0] + '|Median', 'type': 'float'})
                prodata = rfn.append_fields(prodata, str(column.split(
                    '|')[0] + '|Std'), data=np.array(var), usemask=False)
                titles.append(column.split('|')[0] + '|Std')
                fields.append({'name': column.split(
                    '|')[0] + '|Std', 'type': 'float'})
            data_source = []
            temp = []
            for ele in prodata.dtype.names:
                if '|' in ele:
                    temp.append(ele)
                elif '_' not in ele:
                    temp.append(ele)
            data_source.append(temp)
            for line in prodata:
                temp = []
                for title in data_source[0]:
                    temp.append(line[title])
                data_source.append(temp)
            for line in data_source:
                for ele in range(len(line)):
                    if ele != len(line) - 1:
                        tempfile.write(str(line[ele]) + "\t")
                    else:
                        tempfile.write(str(line[ele]) + "\n")
            tempfile.close()
            data = {}
            data['temp_name'] = temp_name

            data['success'] = True
            result = json.dumps(data)
            return HttpResponse(result)
        elif rType == 'P2P':
            temp_name = 'tmp' + str(time.time())
            targetGridType = httpParamDict['targetGridType']
            if targetGridType == 'protein':
                fromFile = quant_dir + csvname + '.protab'
                tmpFile = quant_dir + csvname + temp_name + '.protab'
            elif targetGridType == 'gene':
                fromFile = quant_dir + csvname + '.genetab'
                tmpFile = quant_dir + csvname + temp_name + '.genetab'

            pepdata = prodata
            proDict = {}
            exps = []
            colNameAreaPsms = []
            for col_name in pepdata.dtype.names:
                if col_name.startswith('repeat'):
                    exps.append(col_name)
            for colIdx in range(0, len(exps), 4):
                colNameArea = exps[colIdx]
                colNamePsms = exps[colIdx + 3]
                colNameAreaPsms.append([colNameArea, colNamePsms])
            for line in pepdata:
                try:
                    pep_idx = str(line['index'])
                except:
                    pep_idx = ''
                pep_seq = line['Sequence']
                accList = line['accessions'].split(';')

                proNum = len(accList)
                for acc in accList:
                    if acc in proDict:
                        if pep_idx:
                            proDict[acc]['peptide'].append(pep_idx)
                        for e in colNameAreaPsms:
                            colNameArea, colNamePsms = e
                            area = float(line[colNameArea]) if float(
                                line[colNameArea]) > 0 else 0
                            psms = int(line[colNamePsms]) if int(
                                line[colNamePsms]) > 0 else 0
                            avgArea = area / proNum

                            proDict[acc][colNameArea] += avgArea
                            proDict[acc][colNamePsms] += psms

                    else:
                        proDict[acc] = {}
                        proDict[acc]['peptide'] = [pep_idx] if pep_idx else []
                        for e in colNameAreaPsms:
                            colNameArea, colNamePsms = e
                            area = float(line[colNameArea]) if float(
                                line[colNameArea]) > 0 else 0
                            psms = int(line[colNamePsms]) if int(
                                line[colNamePsms]) > 0 else 0
                            avgArea = area / proNum

                            proDict[acc][colNameArea] = avgArea
                            proDict[acc][colNamePsms] = psms

            tmpProdata = np.genfromtxt(
                fromFile, delimiter='\t', names=True, dtype=None)
            titles = []
            for col_name in tmpProdata.dtype.names:
                titles.append(col_name)

            toWrite = []
            toWrite.append(titles)
            for line in tmpProdata:
                acc = line['accessions']
                if acc in proDict:
                    # line['peptide'] = '1;2;3'
                    for key in proDict[acc]:
                        line[key] = str(proDict[acc][key])
                    line['peptide'] = ';'.join(proDict[acc]['peptide']) if proDict[
                        acc]['peptide'] else 'None'
                    tmpList = []
                    for t in titles:
                        tmpList.append(line[t])
                    toWrite.append(tmpList)

            with open(tmpFile, 'w') as tmpF:
                for line in toWrite:
                    line = [str(x) for x in line]
                    tmpF.write('\t'.join(line) + '\n')

            res = {"temp_name": temp_name}
            result = json.dumps(res, cls=DjangoJSONEncoder)
            return HttpResponse(result)

        else:

            if 'clusterType' in httpParamDict:
                parameters['clusterType'] = httpParamDict['clusterType']
            if 'fontsize' in httpParamDict:
                parameters['fontsize'] = httpParamDict['fontsize']
            if 'minValue' in httpParamDict:
                parameters['minValue'] = '#' + httpParamDict['minValue']
            if 'maxValue' in httpParamDict:
                parameters['maxValue'] = '#' + httpParamDict['maxValue']
            if 'cutoff' in httpParamDict:
                parameters['cutoff'] = httpParamDict['cutoff']
            if 'zscore' in httpParamDict:
                parameters['zscore'] = httpParamDict['zscore']
            if 'log' in httpParamDict:
                parameters['log'] = httpParamDict['log']
            if 'tryNormalize' in httpParamDict:
                parameters['tryNormalize'] = httpParamDict['tryNormalize']
                if Normalize in httpParamDict:
                    parameters['tryNormalize'] = '3'
            else:
                parameters['tryNormalize'] = '1'

            res = pathway.Rplot(data_source, parameters)

            return HttpResponse(res)

    #=========================================================================
    # for line in dataSource:
    #     #print line
    #     for ele in range(len(line)):
    #         if ele!= len(line)-1:
    #             tempfile.write(str(line[ele]) + "\t")
    #         else:
    #             tempfile.write(str(line[ele]) + "\n")
    # tempfile.close()
    #=========================================================================

    prodata = prodata[start:end]
    data = []
    average = 0
    i = 1
    for line in prodata:
        temp = {}
        temp['id'] = i
        if gridType != 'peptide':
            for anno in line['annotation'].split(','):
                anno = anno.split('_')
                temp[anno[0]] = int(anno[1])
        for title in titles:
            temp[title] = str(line[title])
        data.append(temp)
        i = i + 1
    metaData = {}
    metaData['fields'] = fields
    metaData['root'] = 'data'
    data = {"data": data, "metaData": metaData,
            'total': count, 'proname': ProFileName}
    # return HttpResponse(data)
    result = json.dumps(data)
    return HttpResponse(result)


def newcmp_pcaAdjust(request):
    preImage = request.GET['preImage']
    preSrcCorMatrixFile = request.GET['preSrcCorMatrixFile']
    tmpFile = request.GET['tmpFile']
    tmpMetaFile = request.GET['tmpMetaFile']
    todo_metalist = request.GET['todo_metalist'][:-1].split(';')
    pcList = request.GET['pcList']

    adjustedFile = tmpFile + '.adjusted'

    (code, adjustedFile_static) = pathway.pcaAdjust(
        tmpFile, tmpMetaFile, adjustedFile, todo_metalist)

    if os.path.isfile(adjustedFile):
        parameters = {}
        parameters['rType'] = 'pca'
        parameters['adjust'] = 1
        parameters['pcList'] = pcList
        parameters['metadataList'] = request.GET['todo_metalist'][:-1]
        parameters['tmpMetaFile'] = tmpMetaFile
        parameters['input'] = adjustedFile
        parameters['preInput'] = tmpFile
        parameters['preImage'] = preImage
        parameters['preSrcCorMatrixFile'] = preSrcCorMatrixFile
        (tmpHtml, tmpFile, tmpMetaFile, src_metadata, srcCorMatrixFile,
         imageSrc) = pathway.Rplot4([], parameters, [])

        # data = {"adjustedFile_static":adjustedFile_static, "ok":1, 'code':code}
        data = {"adjustedFile_static": adjustedFile_static, "ok": 1, 'code': code,
                "imageSrc": imageSrc,
                "tmpHtml": tmpHtml, "tmpFile": tmpFile, "tmpMetaFile": tmpMetaFile, 'tmpSrcMetadata': src_metadata, 'tmpSrcCorMatrixFile': srcCorMatrixFile,
                "dataMeta": [], "dataCorMatrix": []}
        result = json.dumps(data)
        return HttpResponse(result)

    else:
        data = {"adjustedFile_static": '', "ok": 0, 'code': ''}
    # return HttpResponse(data)
    result = json.dumps(data)
    return HttpResponse(result)


def newcmp_tree(request):
    columns = []
    if 'val' in request.GET:
        csvname = int(request.GET['val'])
        cont = XsearchTable.objects.get(id=csvname)
        expList = cont.exp_name
        expList = expList.split(',')
        # expList = (request.GET.getlist('explist'))
        #======================================================================
        # expList = (request.GET['explist'])
        # expList = expList.split(',')
        # if len(expList)>1:
        #     expList=expList[:-1]
        #======================================================================
        alist = []  # explist
        blist = []  # replist
        cacheList = set()
        for exp in expList:
            temp = exp.split('_')
            (type, exp_id, rank, repe) = (temp[0], int(
                temp[1]), int(temp[2]), int(temp[3]))
            ExpName = Experiment.objects.get(id=exp_id).name
            alist.append(ExpName)
            if type == 'exp':
                RepeatList = Search.objects.filter(
                    exp_id=exp_id).filter(rank=rank).filter(type='rep')
                for rep in RepeatList:
                    blist.append('repeat_' + str(rep.exp_id) + '_' +
                                 str(rep.rank) + '_' + str(rep.repeat_id))
                    cacheList.add(rep.exp_id)
            else:
                blist.append(exp)
        alist = list(set(alist))
        alist.sort()
        blist = list(set(blist))
        blist.sort()
        expDict = {}
        cacheExperiment = Experiment.objects.filter(id__in=cacheList)
        for exp in cacheExperiment:
            temp = {}
            temp['name'] = exp.name
            temp['des'] = exp.description
            expDict[exp.id] = temp
        #======================================================================
        # tempDicExp = {}
        # tempDicExp['text'] = 'Group1'
        # tempDicExp['expanded'] = True
        #======================================================================
        condition = {}
        condition['text'] = ''
        condition['expanded'] = True
        col = []
        for exp in alist:
            for temp1 in blist:
                temp = temp1.split('_')
                (type, exp_id, rank, repe) = (temp[0], int(
                    temp[1]), int(temp[2]), int(temp[3]))
                if expDict[exp_id]['name'] == exp:
                    # if Experiment.objects.get(id=exp_id).name == exp:
                    pp = {}
                    pp["text"] = exp + '_' + expDict[exp_id]['des']
                    pp['leaf'] = True
                    pp['checked'] = False
                    col.append(pp)
        condition['children'] = col
        #======================================================================
        # tempDicExp['children'] = condition
        # columns.append(tempDicExp)
        #======================================================================
        result = json.dumps(condition)
    elif 'out' in request.GET:
        expList = (request.GET.getlist('out'))
        # expList = expList.split(',')[:-1]
        condition = {}
        condition['text'] = 'Root'
        condition['expanded'] = True
        col = []
        for exp in expList:
            pp = {}
            pp["text"] = exp.split("|")[0]
            pp['leaf'] = True
            pp['checked'] = False
            col.append(pp)
        condition['children'] = col
        columns.append(condition)
        result = json.dumps(columns)
    return HttpResponse(result)


def newcmp_download(prodata, titles):
    # print titles
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename="comparison.txt"'
    writer = csv.writer(response, delimiter='\t')
    tempk = []
    for na in titles:
        if na in ['user_defined', '', 'undefined'] or 'ratio' in na:
            continue
        # if na=='modification' and 'Sequence' not in titles:
        #    continue
        if 'repeat' in na:
            temp = na.split('_')
            (type, exp_id, rank, repe) = (temp[0], int(
                temp[1]), int(temp[2]), int(temp[3]))
            exp = Experiment.objects.get(id=exp_id)
            na = exp.name + '_' + exp.description + '_' + temp[4]
        tempk.append(na)
        tempk = [str(item) for item in tempk]
    writer.writerow(tempk)
    for line in prodata:
        tempk = []
        for title in titles:
            if title in ['user_defined', '', 'undefined'] or 'ratio' in title:
                continue
            if title == 'modification' and 'modification' not in line:
                tempk.append('')
                continue
            # temp[title]=str(line[title])
            tempk.append(line[title])
        tempk = [str(item) for item in tempk]
        writer.writerow(tempk)
    # print "what the hell"
    return response

    # return null
''' For row expander '''


def newcmp_peptide(request):
    peptide = request.GET['peptide']
    peptide = peptide.split(';')
    csvname = request.GET['Xid']
    temp_name = request.GET['temp_name'] if 'temp_name' in request.GET else ''
    try:
        columndata = request.GET['columndata']
        # print columndata
    except:
        columndata = []
    try:
        dataidx = request.GET['dataidx']
    except:
        dataidx = []
    columndata = columndata.strip().split(';')[:-1]
    dataidx = dataidx.strip().split(';')[:-1]
    cont = XsearchTable.objects.get(id=csvname)
    pepFileName = quant_dir + csvname + temp_name + '.peptab'
    pepdata = np.genfromtxt(pepFileName, delimiter='\t',
                            names=True, dtype=None)
    if peptide == ['None'] or not peptide or peptide[0] == '':
        peptide = []
    else:
        peptide = [int(pp) for pp in peptide]
    # titles = pepdata.dtype.names
    titles = []
    for col_name in pepdata.dtype.names:
        if col_name[0] != 'r':  # 'r' -> 'repeat'
            titles.append(col_name)
    for idx in dataidx:
        if idx == '':
            continue
        if idx[0] == 'r':
            titles.append(idx)
    fields = []
    for title in titles:
        temp = {}
        temp['name'] = title
        if title in ['Sequence', 'Modification']:
            temp['type'] = 'string'
        else:
            temp['type'] = 'float'
        fields.append(temp)
    data = []
    for pep in peptide:
        temp = {}
        for title in titles:
            if 'VS' not in title and 'ratio' not in title:
                temp[title] = str(pepdata[pep][title])
            elif 'ratio' not in title:
                tt = title.split('VS')
                if pepdata[pep][tt[0]] == -1:
                    temp[title] = -1
                elif pepdata[pep][tt[1]] == 0 or pepdata[pep][tt[1]] == -1:
                    temp[title] = 1e10308
                else:
                    temp[title] = pepdata[pep][tt[0]] / pepdata[pep][tt[1]]
            if 'ratio' in title:
                temp[title] = 1
        data.append(temp)
    columns = [
        {'text': 'Sequence', 'dataIndex': 'Sequence', 'width': 180},
        {'text': 'Modification', 'dataIndex': 'Modification', 'width': 250}]
    for title in titles:
        if title == 'Modification' or title == 'Sequence':
            continue
        if '_area' in title and 'VS' not in title:
            # tempstr = title.split('_area')[0]
            kk = {}
            kk['text'] = 'Area'
            kk['dataIndex'] = title
            kk['width'] = 140
            columns.append(kk)
        elif 'VS' in title:
            kk = {}
            kk['text'] = 'Ratio'
            kk['dataIndex'] = title
            kk['width'] = 140
            columns.append(kk)
        elif 'psm' in title:
            kk = {}
            kk['text'] = 'PSM'
            kk['dataIndex'] = title
            kk['width'] = 140
            columns.append(kk)
        if 'ratio' in title:
            kk = {}
            kk['text'] = 'Ratio'
            kk['dataIndex'] = title
            kk['width'] = 140
            columns.append(kk)
        #======================================================================
        # else:
        #     kk = {}
        #     kk['text'] = 'Ratio'
        #     kk['dataIndex'] = title
        #     columns.append(kk)
        #======================================================================
    metaData = {}
    metaData['fields'] = fields
    metaData['columns'] = columns
    metaData['root'] = 'data'
    data = {"data": data, "metaData": metaData}
    result = json.dumps(data)
    return HttpResponse(result)


#===============================================================================
# def correct(request):
#     experiment_list = Experiment.objects.all()
#     for exp in experiment_list:
#         if exp.id > 70:
#             name = exp.name
#             name = int(name.split('Exp')[1:][0])
#             exp_exp = experiments.models.Experiment.objects.get(id=name)
#             cell = '-'
#             organ = '-'
#             tissue = '-'
#             fluid = '-'
#             temp_sample = experiments.models.Sample.objects.filter(experiment=exp_exp)[
#                 0]
#             if temp_sample.source_tissue:
# 
#                 speci = temp_sample.source_tissue.tissueName.name
#                 tissue = temp_sample.source_tissue.tissueSystem.name
#                 organ = temp_sample.source_tissue.tissueOrgan.name
#             elif temp_sample.source_cell:
# 
#                 try:
#                     speci = temp_sample.source_cell.tissueName.name
#                 except:
#                     sepci = '-'
#                 try:
#                     cell = temp_sample.source_cell.cellName.name
#                 except:
#                     cell = '-'
#             elif temp_sample.source_fluid:
#                 speci = temp_sample.source_fluid.tissueName.name
#                 fluid = temp_sample.source_fluid.fluid.name
#             elif temp_sample.source_others:
#                 speci = '-'
#                 tissue = '-'
#             exp.speci = speci
#             exp.tissue = tissue
#             exp.cell = cell
#             exp.organ = organ
#             exp.fluid = fluid
#             exp.save()
#     return HttpResponse('done')
#===============================================================================


#===============================================================================
# def uploadFiles(request):
#     if 'email' in request.POST:
#         user = request.POST['email']
#     else:
#         user = ''
#     if 'files' in request.POST:
#         file_name = request.POST['files']
#     else:
#         file_name = ''
#     if 'done' in request.POST:
#         done = request.POST['done']
#     else:
#         done = False
#     if file_name != '':
#         files = Upload_File.objects.filter(file_name=file_name)
#     if user == '' or file_name == '' or files.count() > 0:
#         success = False
#         if user == '' or file_name == '':
#             msg = 'Please Login'
#         else:
#             temp_file = files[0]
#             if done:
#                 files = Upload_File.objects.filter(
#                     file_name=file_name).filter(User=user)[0]
#                 files.done = done
#                 files.save()
#                 success = True
#                 msg = 'The status has been changed to uploaded'
#             else:
#                 if temp_file.done:
#                     msg = 'Sorry, this files is already uploaded, please contact admin.'
#                 else:
#                     if temp_file.User == user:
#                         msg = 'Please continue uplaod files'
#                     else:
#                         msg = 'Sorry, this files is already uploaded, please contact admin. '
#     else:
#         files = Upload_File(
#             file_name=file_name,
#             User=user,
#             update_date=datetime.datetime.now()
#         )
#         files.save()
#         success = True
#         msg = 'You can upload now.'
#     data = {'success': success, 'msg': msg}
#     result = json.dumps(data, cls=DjangoJSONEncoder)
#     return HttpResponse(result)
#===============================================================================


def sendtopublic(request):
    exp_list = request.POST['explist']
    lab2 = request.POST['lab']
    # print exp_list
    exp_list = exp_list.split(',')[:-1]
    msg = ''
    failure = False
    failMsg = ''
    lab = experiments.models.User_Laboratory.objects.filter(user=request.user)
    lab = lab[0].lab.name if lab.count() else ''
    for exp in exp_list:
        exp_num = exp.split('_')[1]
        experiment = Experiment.objects.get(id=int(exp_num))
        if experiment.lab == lab:
            share = Share_Exp.objects.filter(
                exp=experiment,
                lab=lab2
            )
            if share.count() == 0:
                share = Share_Exp(
                    exp=experiment,
                    lab=lab2
                )
                share.save()
            msg = msg + experiment.name + ';'
        else:
            failure = True
            failMsg = failMsg + experiment.name + ';'
    msg = msg[:-1]
    failMsg = failMsg[:-1]
    if msg != '':
        msg = msg + ' has been sent to ' + lab2 + ';'
    if failure:
        msg = msg + failMsg + ' cannot be share because of authority.Please contact admin.'
    data = {'success': True, 'msg': msg}
    result = json.dumps(data, cls=DjangoJSONEncoder)
    return HttpResponse(result)


def userAnnotation(request):
    userid = request.user.id
    exp = request.POST['exp'] if 'exp' in request.POST else ''
    symbols = request.POST['symbol'] if 'symbol' in request.POST else ''
    batch = True if 'batch' in request.POST else False
    symbols = symbols.strip().split('\n')
    annotation = request.POST['annotation']

    species = Experiment.objects.get(name=exp).species
    for symbol in symbols:
        (anno, sym) = user_defined.objects.get_or_create(
            species=species, user=userid, symbol=symbol)
        if batch:
            anno.annotation = anno.annotation + annotation + ';'
        else:
            anno.annotation = annotation + ';' if annotation != '' else ''
        anno.save()
    data = {'success': True}
    result = json.dumps(data, cls=DjangoJSONEncoder)
    return HttpResponse(result)


def protein2Genome(request):
    ExpID = request.POST['experiment_no']
    gi = request.POST.getlist('gi')
    result = genome.Protein2Genome_new(ExpID, gi)
    data = {'success': True, 'species': result[
        0], 'file': result[1], 'chr': result[2]}
    result = json.dumps(data, cls=DjangoJSONEncoder)
    return HttpResponse(result)


def PepLocation(request):
    return newfuncTest.getPepLoc(request)


def coverage(request):
    return newfuncTest.coverage(request)


def download_data(request):
    FilePath = '/usr/local/firmiana/data/ExpTable/'

    def create_file(req, exp):
        blah()
    req = request.GET['req']
    req = req.split('|')
    exps = req[0].split(';')  # exp number
    reqs = req[1].split(';')  # Gene,Protein,Peptide,metadata
    temp = tempfile.TemporaryFile()
    archive = zipfile.ZipFile(temp, 'w', zipfile.ZIP_DEFLATED)

    for req in reqs:
        for exp in exp:
            filename = FilePath + exp + '.' + req + '.txt'
            if not os.path.exists(filename):
                create_file(req, exp)
            archive.write(filename, filename)
    archive.close()
    wrapper = FileWrapper(temp)
    response = HttpResponse(wrapper, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename=download.zip'
    response['Content-Length'] = temp.tell()
    temp.seek(0)
    return response

# def ppi_xiaotian(request):
#
#     def getFromDB(exp_id):
#         #id = Search.objects.filter(exp_id=exp_id).filter(type='exp')[0].id
#         tmp = []
#         protein_list = Exp_Protein.objects.all().filter(search__exp__id = exp_id).filter(search__type='exp').filter(type=1)
#         for p in protein_list:
#             acc = p.accession
#             sym = p.symbol
#             if not sym or sym == '-':
#                 sym = 'NA'
#             fot = p.fot
#             tmp.append( (acc, sym, fot) )
#         return tmp
#     #===========================================================================
#     #     if e == '001211':
#     #         return [['gi1','',100] , ['gi2','Symbol2',200], ['gi3','Symbol2',300], ['gi4','Symbol3',400], ['gi5','Symbol4',500]]
#     #     else:
#     #         return [['gi3','Symbol2',1100] , ['gi11','Symbol32',2020], ['gi13','Symbol12',3010], ['gi32','Symbol34',40320], ['gi5','Symbol44',5010]]
#     #
#     #===========================================================================
#
#     cutoff = float(request.GET["cutoff"])
# #     percent = float(request.GET["percent"])
#     percent = 0.5
#     times = 1
#     randomNumber = 20
#     resultRatio = ""
# #     pre1 = '{0}ppi_tmp/firppiGlobal_{1}/'.format(pathway.tmpdir, time.time())
#     pre1 = '{0}ppi_tmp/firppiGlobal_{1}randomExp*{2}times/'.format(pathway.tmpdir,randomNumber,times)
#     os.mkdir(pre1)
#     ppiRankFileResultAddr = os.path.join(pre1, "ppi-rank-result.txt")
#
#     '''
#     expListTotal is a list including TFREandProfiling|hsa|done experiments
#     '''
#     expIDListTotal = '1039,1040,1041,1042,1043,1044,1045,1046,1047,1048,1049,1050,1051,1052,1053,1054,1055,1056,1057,1058,1063,1064,1065,1066,1067,1068,1069,1070,1071,1072,1073,1074,1075,1076,1077,1078,1079,1080,1157,1158,1159,1160,1215,1216,1217,1218,1219,1220,1221,1222,1223,1224,1225,1226,1227,1228,1229,1230,1231,1232,1233,1234,1235,1236,1237,1238,1239,1240,1241,1242,1243,1244,1245,1246,1247,1248,1249,1250,1251,1252,1253,1254,1255,1256,1257,1258,1259,1260,1304,1305,1306,1307,1308,1309,1310,1311,1312,1313,1314,1315,1325,1326,1327,1328,1335,1336,1339,1340,1341,1342,1343,1344,1345,1346,1347,1348,1349,1350,1351,1352,1353,1354,1355,1356,1421,1422,1423,1424,1425,1426,1427,1428,1429,1430,1431,1432,1433,1434,1435,1436,1437,1438,1439,1440,1441,1442,1443,1444,1445,1446,1447,1448,1449,1450,1451,1452,1453,1454,1455,1456,1457,1458,1459,1460,1462,1463,1464,1465,1466,1467,1468,1469,1470,1471,1472,1473,1474,1475,1476,1477,1478,1479,1480,1481,1482,1483,1484,1485,1553,1554,1555,1556,1557,1558,1559,1560,1561,1562,1594,1595,1596,1597,1598,1599,1600,1601,1602,1603,1604,1605,1892,1893,1939,1940,1941,1942,1943,1944,1945,1946,1947,1948,1949,1950,1951,1952,1953,1954,1955,1956,1957,1958,1959,1960,1988,2005,2006,2007,2008,2009,246,247,248,249,250,264,288,289,290,291,292,293,340,341,342,343,344,345,346,347,348,349,500,501,502,503,504,505,506,507,525,526,527,528,529,530,531,532,533,534,535,536,537,538,539,540,541,542,563,564,584,585,586,587,588,589,590,591,592,593,638,714,715,774,775,776,777,778,779,780,781,782,783,784,785,786,787,788,789,790,791,792,793,794,795,796,797,802,803,804,805,806,807,856,857,858,859,860,861,886,887,888,889,890,891,892,893,906,907,908,909,910,911,912,913,914,915,916,917,918,919,920,921,922,923,924,925,926,927,928,929,930,931,932,933,934,935,936,937,972,973,974,975,468,467,466,465,464,463,462,461,460,459,458,439,438,329,328,327,326,325,324,282,281,280,279,278,277,265,264,263,260,244,243,242,241,240,239,238,237,176,175,174,173,172,171,170,169,142,137,136,135,134,133,132,131,130,129,128,127,126,743,742,739,738,737,736,735,734,733,732,731,726,725,724,723,722,721,720,719,718,717,716,712,711,710,709,708,707,702,701,700,699,698,697,696,695,673,672,658,657,656,655,654,653,652,651,650,649,648,647,646,645,600,599,598,597,596,595,594,562,561,560,559,558,557,556,555,554,553,552,551,550,549,548,547,524,523,522,516,515,514,513,512,499,498,483,482,481,480,479,478,477,476,475,474,473,472,471,470,469,1060,1059,1038,1037,1036,1035,1034,1033,1032,1031,1009,1008,969,968,953,952,951,950,949,948,947,946,945,944,943,942,941,940,939,938,885,884,883,882,881,880,879,878,877,876,875,874,873,872,871,870,869,868,867,866,865,864,863,862,855,854,853,852,851,850,843,829,828,827,826,825,824,823,822,821,820,819,818,817,816,815,814,813,812,764,763,762,761,760,759,758,757,756,755,754,753,752,751,750,749,748,747,746,745,744,1510,1509,1508,1502,1501,1500,1499,1498,1497,1496,1495,1494,1493,1492,1491,1490,1489,1488,1487,1486,1417,1416,1413,1412,1411,1410,1409,1408,1407,1406,1405,1404,1403,1402,1401,1400,1399,1398,1397,1396,1395,1394,1393,1392,1214,1213,1212,1211,1210,1209,1208,1207,1206,1205,1204,1203,1202,1201,1200,1199,1198,1197,1196,1195,1194,1193,1192,1191,1190,1189,1188,1187,1186,1185,1184,1183,1182,1181,1180,1179,1178,1177,1176,1175,1174,1173,1172,1171,1170,1169,1168,1167,1166,1165,1164,1163,1162,1161,1062,1061,1964,1963,1962,1961,1855,1854,1853,1851,1850,1849,1848,1847,1846,1845,1844,1843,1842,1841,1840,1745,1744,1743,1742,1741,1740,1739,1738,1737,1736,1735,1734,1733,1732,1731,1730,1729,1699,1698,1697,1696,1695,1694,1693,1692,1691,1690,1689,1688,1687,1685,1684,1683,1682,1681,1680,1679,1678,1677,1676,1675,1674,1672,1671,1670,1668,1667,1665,1664,1663,1662,1661,1660,1659,1658,1657,1656,1655,1654,1653,1652,1651,1650,1649,1648,1647,1646,1620,1619,1618,1617,1616,1592,1591,1513,1512,1511'
#     expIDListTotal = expIDListTotal.split(',')
#     with open(ppiRankFileResultAddr, "w") as f:
#         f.write("SMC1A_SMC3__SMC1A"+"\t"+"SMC1A_RAD21__RAD21"+"\t"+"SMC3_RAD21__RAD21"+"\t"+"HDAC1_HDAC2__HDAC1"+"\t"+"RBBP4_RBBP7__RBBP4"+"\n")
#
#     for j in range(times):
#         expIDList = []
#         for i in range(randomNumber):
#             expIDList.append(random.choice(expIDListTotal))
#
#     #     expIDList = request.GET['expIDList'] #"001211,001212,001310"
#     #     expIDList = expIDList.split(',')
#         expLength = len(expIDList)
#
#         bigDict = {}
#         for i in range(expLength):
#             expID = expIDList[i]
#             fotList = getFromDB(expID) # [ [sym, fot], .... ]
#             for line in fotList:
#                 accession = line[0]
#                 symbol = line[1]
#                 fot = line[2]
#
#                 if accession in bigDict:
#                     bigDict[accession][i+1] = fot
#                 else:
#                     bigDict[accession] = [0] * (expLength+1)
#                     bigDict[accession][0] = symbol
#                     bigDict[accession][i+1] = fot
#         '''
#         bigDict ={
#                         "sym1":[100,200],
#                         "sym2":[100,200],
#                         "sym3":[100,200],
#                 }
#         '''
#
#         zero_count_cutoff = math.ceil(expLength*percent)
#         tempfileName1 = os.path.join(pre1, "temp-ppi.txt")
#         ppiRankFileAddr = os.path.join(pre1, "ppi-rank.txt")
#         '''
#         bigDict = {
#                    "accession1":["symbol1", 100, 101],
#                    "accession10":["symbol10", 0, 1011],
#                    }
#         '''
#         with open(tempfileName1, 'w') as f:
#             for accession,dict_Ele_List in bigDict.iteritems():
#                 #test zero_count
#                 zero_count = 0
#                 satisfy_zero_count_flag = True
#                 for fot in dict_Ele_List[1:]:
#                     if fot == 0: zero_count += 1
#                 if zero_count > zero_count_cutoff:
#                     satisfy_zero_count_flag = False
#                 if satisfy_zero_count_flag:
#                     tmp = [ str(x) for x in dict_Ele_List ]
#                     tmp.insert(0,accession)
#                     f.write( "\t".join(tmp) + "\n")
#
#         gi_lst = []
#         with open(tempfileName1, "r") as f:
#             for line in f:
#                 element = line.split("\t")
#                 gi_lst.append(element[0] + ";" + element[1])
#         gi_lst_str = ""
#         gi_lst_str = ",".join(gi_lst)
#
#         output_name = pre1 + 'ppi'
#
#         code, grn_list, grn_list_three, GRNListString, resultString = pathway.ppi(tempfileName1, output_name, expLength, pre1, cutoff)
#
#         resultRatioList = []
#
#         with open(ppiRankFileAddr, "r") as f:
#             for line in f:
#                 resultRatioList.append(line.strip("\n"))
#         with open(ppiRankFileResultAddr, "a") as f:
#             f.write(("\t".join(resultRatioList) + '\n').replace('"',''))
#
#     outJsonDict = {}
# #     outJsonDict["code"] = code
# #     outJsonDict["grn_list"] = grn_list
# #     outJsonDict["grn_list_three"] = grn_list_three
# #     outJsonDict["GRNListString"] = GRNListString
# #     outJsonDict["resultString"] = resultString
# #     outJsonDict["gi_lst_str"] = gi_lst_str
#
#     result = json.dumps(outJsonDict)
#
#     return HttpResponse(result)


def ppi_xiaotian(request):

    def getFromDB(exp_id):
        #id = Search.objects.filter(exp_id=exp_id).filter(type='exp')[0].id
        tmp = []
        protein_list = Exp_Protein.objects.all().filter(
            search__exp__id=exp_id).filter(search__type='exp').filter(type=1)
        for p in protein_list:
            acc = p.accession
            sym = p.symbol
            if not sym or sym == '-':
                sym = 'NA'
            fot = p.fot
            tmp.append((acc, sym, fot))
        return tmp
    #=========================================================================
    #     if e == '001211':
    #         return [['gi1','',100] , ['gi2','Symbol2',200], ['gi3','Symbol2',300], ['gi4','Symbol3',400], ['gi5','Symbol4',500]]
    #     else:
    #         return [['gi3','Symbol2',1100] , ['gi11','Symbol32',2020], ['gi13','Symbol12',3010], ['gi32','Symbol34',40320], ['gi5','Symbol44',5010]]
    #
    #=========================================================================

#     cutoff = float(request.GET["cutoff"])
#     percent = float(request.GET["percent"])
    cutoff = 9
    percent = 0.5
    times = 1
    randomNumber = 297
    '''
    expListTotal is a list including TFREandProfiling|hsa|done experiments
    '''
#     expIDListTotal = '1039,1040,1041,1042,1043,1044,1045,1046,1047,1048,1049,1050,1051,1052,1053,1054,1055,1056,1057,1058,1063,1064,1065,1066,1067,1068,1069,1070,1071,1072,1073,1074,1075,1076,1077,1078,1079,1080,1157,1158,1159,1160,1215,1216,1217,1218,1219,1220,1221,1222,1223,1224,1225,1226,1227,1228,1229,1230,1231,1232,1233,1234,1235,1236,1237,1238,1239,1240,1241,1242,1243,1244,1245,1246,1247,1248,1249,1250,1251,1252,1253,1254,1255,1256,1257,1258,1259,1260,1304,1305,1306,1307,1308,1309,1310,1311,1312,1313,1314,1315,1325,1326,1327,1328,1335,1336,1339,1340,1341,1342,1343,1344,1345,1346,1347,1348,1349,1350,1351,1352,1353,1354,1355,1356,1421,1422,1423,1424,1425,1426,1427,1428,1429,1430,1431,1432,1433,1434,1435,1436,1437,1438,1439,1440,1441,1442,1443,1444,1445,1446,1447,1448,1449,1450,1451,1452,1453,1454,1455,1456,1457,1458,1459,1460,1462,1463,1464,1465,1466,1467,1468,1469,1470,1471,1472,1473,1474,1475,1476,1477,1478,1479,1480,1481,1482,1483,1484,1485,1553,1554,1555,1556,1557,1558,1559,1560,1561,1562,1594,1595,1596,1597,1598,1599,1600,1601,1602,1603,1604,1605,1892,1893,1939,1940,1941,1942,1943,1944,1945,1946,1947,1948,1949,1950,1951,1952,1953,1954,1955,1956,1957,1958,1959,1960,1988,2005,2006,2007,2008,2009,246,247,248,249,250,264,288,289,290,291,292,293,340,341,342,343,344,345,346,347,348,349,500,501,502,503,504,505,506,507,525,526,527,528,529,530,531,532,533,534,535,536,537,538,539,540,541,542,563,564,584,585,586,587,588,589,590,591,592,593,638,714,715,774,775,776,777,778,779,780,781,782,783,784,785,786,787,788,789,790,791,792,793,794,795,796,797,802,803,804,805,806,807,856,857,858,859,860,861,886,887,888,889,890,891,892,893,906,907,908,909,910,911,912,913,914,915,916,917,918,919,920,921,922,923,924,925,926,927,928,929,930,931,932,933,934,935,936,937,972,973,974,975,468,467,466,465,464,463,462,461,460,459,458,439,438,329,328,327,326,325,324,282,281,280,279,278,277,265,264,263,260,244,243,242,241,240,239,238,237,176,175,174,173,172,171,170,169,142,137,136,135,134,133,132,131,130,129,128,127,126,743,742,739,738,737,736,735,734,733,732,731,726,725,724,723,722,721,720,719,718,717,716,712,711,710,709,708,707,702,701,700,699,698,697,696,695,673,672,658,657,656,655,654,653,652,651,650,649,648,647,646,645,600,599,598,597,596,595,594,562,561,560,559,558,557,556,555,554,553,552,551,550,549,548,547,524,523,522,516,515,514,513,512,499,498,483,482,481,480,479,478,477,476,475,474,473,472,471,470,469,1060,1059,1038,1037,1036,1035,1034,1033,1032,1031,1009,1008,969,968,953,952,951,950,949,948,947,946,945,944,943,942,941,940,939,938,885,884,883,882,881,880,879,878,877,876,875,874,873,872,871,870,869,868,867,866,865,864,863,862,855,854,853,852,851,850,843,829,828,827,826,825,824,823,822,821,820,819,818,817,816,815,814,813,812,764,763,762,761,760,759,758,757,756,755,754,753,752,751,750,749,748,747,746,745,744,1510,1509,1508,1502,1501,1500,1499,1498,1497,1496,1495,1494,1493,1492,1491,1490,1489,1488,1487,1486,1417,1416,1413,1412,1411,1410,1409,1408,1407,1406,1405,1404,1403,1402,1401,1400,1399,1398,1397,1396,1395,1394,1393,1392,1214,1213,1212,1211,1210,1209,1208,1207,1206,1205,1204,1203,1202,1201,1200,1199,1198,1197,1196,1195,1194,1193,1192,1191,1190,1189,1188,1187,1186,1185,1184,1183,1182,1181,1180,1179,1178,1177,1176,1175,1174,1173,1172,1171,1170,1169,1168,1167,1166,1165,1164,1163,1162,1161,1062,1061,1964,1963,1962,1961,1855,1854,1853,1851,1850,1849,1848,1847,1846,1845,1844,1843,1842,1841,1840,1745,1744,1743,1742,1741,1740,1739,1738,1737,1736,1735,1734,1733,1732,1731,1730,1729,1699,1698,1697,1696,1695,1694,1693,1692,1691,1690,1689,1688,1687,1685,1684,1683,1682,1681,1680,1679,1678,1677,1676,1675,1674,1672,1671,1670,1668,1667,1665,1664,1663,1662,1661,1660,1659,1658,1657,1656,1655,1654,1653,1652,1651,1650,1649,1648,1647,1646,1620,1619,1618,1617,1616,1592,1591,1513,1512,1511'
    expIDListTotal = '142,952,951,950,949,948,947,946,944,943,942,941,940,939,938,885,884,883,882,881,880,879,878,877,876,875,874,873,872,871,870,854,852,850,843,818,817,816,814,812,764,763,762,761,749,747,746,745,743,725,724,723,722,702,701,699,698,697,695,562,557,556,555,554,552,551,550,549,548,547,516,483,477,476,475,474,473,472,471,470,465,461,460,459,458,280,279,278,263,244,243,242,241,240,239,238,237,176,175,174,173,1493,1492,1491,1490,1489,1488,1487,1417,1416,1413,1412,1411,1410,1409,1408,1406,1405,1404,1403,1402,1401,1400,1399,1398,1397,1396,1395,1394,1393,1392,1214,1212,1211,1210,1209,1208,1207,1206,1205,1204,1203,1202,1201,1200,1199,1198,1197,1196,1195,1194,1193,1192,1191,1190,1189,1188,1187,1186,1185,1184,1183,1182,1181,1180,1179,1178,1177,1176,1175,1174,1173,1172,1171,1170,1169,1168,1167,1166,1165,1164,1163,1162,1161,1062,1061,1060,1059,1038,1037,1036,1035,1034,1033,1032,1031,1009,1008,969,968,953,1855,1854,1853,1851,1850,1849,1848,1847,1846,1845,1844,1842,1841,1840,1745,1744,1743,1742,1741,1739,1738,1736,1735,1734,1733,1732,1731,1730,1729,1699,1698,1697,1696,1695,1694,1693,1692,1691,1690,1689,1688,1687,1685,1684,1683,1682,1681,1680,1679,1678,1677,1676,1675,1674,1672,1671,1670,1668,1667,1665,1664,1663,1662,1661,1660,1659,1658,1657,1656,1655,1654,1653,1652,1651,1650,1649,1648,1647,1646,1606,1592,1591,1513,1512,1510,1509,1508,1502,1501,1500,1499,1498,1497,1496,1495,1494'
    expIDListTotal = expIDListTotal.split(',')

    for j in range(times):
        pre1 = '{0}ppi_tmp/firppiGlobal_{1}randomExp*{2}times{3}/'.format(
            pathway.tmpdir, randomNumber, times, j)
        if not os.path.exists(pre1):
            os.mkdir(pre1)
        expIDList = []
        for i in range(randomNumber):
            expIDList.append(random.choice(expIDListTotal))

        expLength = len(expIDList)

        bigDict = {}
        for i in range(expLength):
            expID = expIDList[i]
            fotList = getFromDB(expID)  # [ [sym, fot], .... ]
            for line in fotList:
                accession = line[0]
                symbol = line[1]
                fot = line[2]

                if accession in bigDict:
                    bigDict[accession][i + 1] = fot
                else:
                    bigDict[accession] = [0] * (expLength + 1)
                    bigDict[accession][0] = symbol
                    bigDict[accession][i + 1] = fot
        '''
        bigDict ={
                        "sym1":[100,200],
                        "sym2":[100,200],
                        "sym3":[100,200],
                }
        '''

        zero_count_cutoff = math.ceil(expLength * percent)
        tempfileName1 = os.path.join(pre1, "temp-ppi.txt")
        '''
        bigDict = {
                   "accession1":["symbol1", 100, 101],
                   "accession10":["symbol10", 0, 1011],
                   }
        '''
        with open(tempfileName1, 'w') as f:
            for accession, dict_Ele_List in bigDict.iteritems():
                # test zero_count
                zero_count = 0
                satisfy_zero_count_flag = True
                for fot in dict_Ele_List[1:]:
                    if fot == 0:
                        zero_count += 1
                if zero_count > zero_count_cutoff:
                    satisfy_zero_count_flag = False
                if satisfy_zero_count_flag:
                    tmp = [str(x) for x in dict_Ele_List]
                    tmp.insert(0, accession)
                    f.write("\t".join(tmp) + "\n")

        output_name = pre1 + 'ppi'

        code, grn_list, grn_list_three, GRNListString, resultString = pathway.ppi(
            tempfileName1, output_name, expLength, pre1, cutoff)

    gi_lst = []
    with open(tempfileName1, "r") as f:
        for line in f:
            element = line.split("\t")
            gi_lst.append(element[1])

    tempfileName2 = os.path.join(pre1, "ppi-grn-list.tree")
    with open(tempfileName2, "r") as f:
        line = f.readline()
        line = f.readline()
        for line in f:
            print line

    outJsonDict = {}

    result = json.dumps(outJsonDict)

    return HttpResponse(result)


def ppi_xiaotian_analysis(request):
    protein_list = Exp_Gene.objects.all().filter(
        search__exp__id=2256).filter(search__type='exp').filter(type=1)
    result = ''
    for p in protein_list:
        result += p.modification.split(',')[2] + ' '
#     def getFromDB(exp_id):
#         #id = Search.objects.filter(exp_id=exp_id).filter(type='exp')[0].id
#         tmp = []
#         protein_list = Exp_Gene.objects.all().filter(search__exp__id = exp_id).filter(search__type='exp').filter(type=1)
#         for p in protein_list:
#             if p.modification.split(',')[2].split('_')[1] == '1':
#                 geneid = str(p.gene_id)
#                 sym = p.symbol
#                 if not sym or sym == '-':
#                     sym = 'NA'
#                 fot = p.fot
#                 tmp.append( (geneid, sym, fot) )
#         return tmp
#     #===========================================================================
#     #     if e == '001211':
#     #         return [['gi1','',100] , ['gi2','Symbol2',200], ['gi3','Symbol2',300], ['gi4','Symbol3',400], ['gi5','Symbol4',500]]
#     #     else:
#     #         return [['gi3','Symbol2',1100] , ['gi11','Symbol32',2020], ['gi13','Symbol12',3010], ['gi32','Symbol34',40320], ['gi5','Symbol44',5010]]
#     #
#     #===========================================================================
#
# #     cutoff = float(request.GET["cutoff"])
# #     percent = float(request.GET["percent"])
#     '''
#     expListTotal is a list including TFREandProfiling|hsa|done experiments
#     '''
# #     expIDListTotal = '1039,1040,1041,1042,1043,1044,1045,1046,1047,1048,1049,1050,1051,1052,1053,1054,1055,1056,1057,1058,1063,1064,1065,1066,1067,1068,1069,1070,1071,1072,1073,1074,1075,1076,1077,1078,1079,1080,1157,1158,1159,1160,1215,1216,1217,1218,1219,1220,1221,1222,1223,1224,1225,1226,1227,1228,1229,1230,1231,1232,1233,1234,1235,1236,1237,1238,1239,1240,1241,1242,1243,1244,1245,1246,1247,1248,1249,1250,1251,1252,1253,1254,1255,1256,1257,1258,1259,1260,1304,1305,1306,1307,1308,1309,1310,1311,1312,1313,1314,1315,1325,1326,1327,1328,1335,1336,1339,1340,1341,1342,1343,1344,1345,1346,1347,1348,1349,1350,1351,1352,1353,1354,1355,1356,1421,1422,1423,1424,1425,1426,1427,1428,1429,1430,1431,1432,1433,1434,1435,1436,1437,1438,1439,1440,1441,1442,1443,1444,1445,1446,1447,1448,1449,1450,1451,1452,1453,1454,1455,1456,1457,1458,1459,1460,1462,1463,1464,1465,1466,1467,1468,1469,1470,1471,1472,1473,1474,1475,1476,1477,1478,1479,1480,1481,1482,1483,1484,1485,1553,1554,1555,1556,1557,1558,1559,1560,1561,1562,1594,1595,1596,1597,1598,1599,1600,1601,1602,1603,1604,1605,1892,1893,1939,1940,1941,1942,1943,1944,1945,1946,1947,1948,1949,1950,1951,1952,1953,1954,1955,1956,1957,1958,1959,1960,1988,2005,2006,2007,2008,2009,246,247,248,249,250,264,288,289,290,291,292,293,340,341,342,343,344,345,346,347,348,349,500,501,502,503,504,505,506,507,525,526,527,528,529,530,531,532,533,534,535,536,537,538,539,540,541,542,563,564,584,585,586,587,588,589,590,591,592,593,638,714,715,774,775,776,777,778,779,780,781,782,783,784,785,786,787,788,789,790,791,792,793,794,795,796,797,802,803,804,805,806,807,856,857,858,859,860,861,886,887,888,889,890,891,892,893,906,907,908,909,910,911,912,913,914,915,916,917,918,919,920,921,922,923,924,925,926,927,928,929,930,931,932,933,934,935,936,937,972,973,974,975,468,467,466,465,464,463,462,461,460,459,458,439,438,329,328,327,326,325,324,282,281,280,279,278,277,265,264,263,260,244,243,242,241,240,239,238,237,176,175,174,173,172,171,170,169,142,137,136,135,134,133,132,131,130,129,128,127,126,743,742,739,738,737,736,735,734,733,732,731,726,725,724,723,722,721,720,719,718,717,716,712,711,710,709,708,707,702,701,700,699,698,697,696,695,673,672,658,657,656,655,654,653,652,651,650,649,648,647,646,645,600,599,598,597,596,595,594,562,561,560,559,558,557,556,555,554,553,552,551,550,549,548,547,524,523,522,516,515,514,513,512,499,498,483,482,481,480,479,478,477,476,475,474,473,472,471,470,469,1060,1059,1038,1037,1036,1035,1034,1033,1032,1031,1009,1008,969,968,953,952,951,950,949,948,947,946,945,944,943,942,941,940,939,938,885,884,883,882,881,880,879,878,877,876,875,874,873,872,871,870,869,868,867,866,865,864,863,862,855,854,853,852,851,850,843,829,828,827,826,825,824,823,822,821,820,819,818,817,816,815,814,813,812,764,763,762,761,760,759,758,757,756,755,754,753,752,751,750,749,748,747,746,745,744,1510,1509,1508,1502,1501,1500,1499,1498,1497,1496,1495,1494,1493,1492,1491,1490,1489,1488,1487,1486,1417,1416,1413,1412,1411,1410,1409,1408,1407,1406,1405,1404,1403,1402,1401,1400,1399,1398,1397,1396,1395,1394,1393,1392,1214,1213,1212,1211,1210,1209,1208,1207,1206,1205,1204,1203,1202,1201,1200,1199,1198,1197,1196,1195,1194,1193,1192,1191,1190,1189,1188,1187,1186,1185,1184,1183,1182,1181,1180,1179,1178,1177,1176,1175,1174,1173,1172,1171,1170,1169,1168,1167,1166,1165,1164,1163,1162,1161,1062,1061,1964,1963,1962,1961,1855,1854,1853,1851,1850,1849,1848,1847,1846,1845,1844,1843,1842,1841,1840,1745,1744,1743,1742,1741,1740,1739,1738,1737,1736,1735,1734,1733,1732,1731,1730,1729,1699,1698,1697,1696,1695,1694,1693,1692,1691,1690,1689,1688,1687,1685,1684,1683,1682,1681,1680,1679,1678,1677,1676,1675,1674,1672,1671,1670,1668,1667,1665,1664,1663,1662,1661,1660,1659,1658,1657,1656,1655,1654,1653,1652,1651,1650,1649,1648,1647,1646,1620,1619,1618,1617,1616,1592,1591,1513,1512,1511'
#     expIDListTotal = '790,789,788,787,786,785,784,783,782,781,780,779,778,777,776,775,774,715,714,638,593,592,591,590,589,588,587,586,585,584,564,563,542,541,540,539,538,537,536,535,534,533,532,531,530,529,528,527,526,525,507,506,505,504,503,502,501,500,349,348,347,346,345,344,343,342,341,340,293,292,291,290,289,288,264,250,249,248,247,246,1079,1078,1077,1076,1075,1074,1073,1072,1071,1070,1069,1068,1067,1066,1065,1064,1063,1058,1057,1056,1055,1054,1053,1052,1051,1050,1049,1048,1047,1046,1045,1044,1043,1042,1041,1040,1039,975,974,973,972,937,936,935,934,933,932,931,930,929,928,927,926,925,924,923,922,921,920,919,918,917,916,915,914,913,912,911,910,909,908,907,906,893,892,891,890,889,888,887,886,861,860,859,858,857,856,807,806,805,804,803,802,797,796,795,794,793,792,791,2272,2271,2270,2269,2268,2267,2266,2265,2264,2263,2262,2261,2260,2259,2258,2257,2256,2255,2254,2253,2252,2251,2250,2249,2248,2247,2246,2245,2244,2243,2242,2241,2240,2238,2237,2236,2235,2234,2233,2232,2231,2230,2229,2228,2227,2189,2188,2187,2186,2185,2184,2183,2182,2181,2180,2179,2081,2080,2079,2078,2077,2076,2075,2074,2073,2072,2071,2070,2069,2068,2067,2066,2065,2063,2062,2061,2060,2059,2058,2026,2025,2024,2023,2022,2021,2020,2019,2009,2008,2007,2006,2005,2004,2003,2002,2001,2000,1999,1998,1997,1433,1432,1431,1430,1429,1428,1427,1426,1425,1424,1423,1422,1421,1356,1355,1354,1353,1352,1351,1350,1349,1348,1347,1346,1345,1344,1343,1342,1341,1340,1339,1336,1335,1328,1327,1326,1325,1315,1314,1313,1312,1311,1310,1309,1308,1307,1306,1305,1304,1260,1259,1258,1257,1256,1255,1254,1253,1252,1251,1250,1249,1248,1247,1246,1245,1244,1243,1242,1241,1240,1239,1238,1237,1236,1235,1234,1233,1232,1231,1230,1229,1228,1227,1226,1225,1224,1223,1222,1221,1220,1219,1218,1217,1216,1215,1160,1159,1158,1157,1080,1996,1995,1988,1960,1959,1958,1957,1956,1955,1954,1953,1952,1951,1950,1949,1948,1947,1946,1945,1944,1943,1942,1941,1940,1939,1893,1892,1605,1604,1603,1602,1601,1600,1599,1598,1597,1596,1595,1594,1562,1561,1560,1559,1558,1557,1556,1555,1554,1553,1485,1484,1483,1482,1481,1480,1479,1478,1477,1476,1475,1474,1473,1472,1471,1470,1469,1468,1467,1466,1465,1464,1463,1462,1460,1459,1458,1457,1456,1455,1454,1453,1452,1451,1450,1449,1448,1447,1446,1445,1444,1443,1442,1441,1440,1439,1438,1437,1436,1435,1434'
#     expIDListTotal = expIDListTotal.split(',')
#
# #     expIDList = []
# #     for i in range(10):
# #         expIDList.append(random.choice(expIDListTotal))
#     expIDList = expIDListTotal
#     pre1 = '{0}ppi_tmp/0_tfreHsaKinase/'.format(pathway.tmpdir)
# #     if not os.path.exists(pre1):
# #         os.mkdir(pre1)
#     expLength = len(expIDList)
#
#     bigDict = {}
#     for i in range(expLength):
#         expID = expIDList[i]
#         fotList = getFromDB(expID) # [ [sym, fot], .... ]
#         for line in fotList:
#             geneid = line[0]
#             symbol = line[1]
#             fot = line[2]
#
#             if geneid in bigDict:
#                 bigDict[geneid][i+1] = fot
#             else:
#                 bigDict[geneid] = [0] * (expLength+1)
#                 bigDict[geneid][0] = symbol
#                 bigDict[geneid][i+1] = fot
#     '''
#     bigDict ={
#                     "sym1":[100,200],
#                     "sym2":[100,200],
#                     "sym3":[100,200],
#             }
#     '''
#
#     tempfileName1 = os.path.join(pre1, "geneList.txt")
#     tempfileName2 = os.path.join(pre1, "result.txt")
#     '''
#     bigDict = {
#                "accession1":["symbol1", 100, 101],
#                "accession10":["symbol10", 0, 1011],
#                }
#     '''
#     with open(tempfileName1, 'w') as f:
#         for geneid,dict_Ele_List in bigDict.iteritems():
#             tmp = [ str(x) for x in dict_Ele_List ]
#             tmp.insert(0,geneid)
#             f.write( "\t".join(tmp) + "\n")
#     with open(tempfileName1, 'r') as f1:
#         with open(tempfileName2, 'w') as f2:
#             for line in f1:
#                 element = line.split('\t')
#                 s = element[0]+'\t' + element[1]+'\t'
#                 sum = 0
#                 for i in range(2,len(element)):
#                     if float(element[i])!=0:
#                         sum += float(element[i])
#                 s += str(sum/(len(element)-2))
#                 f2.write(s+'\n')
#
# #         output_name = pre1 + 'ppi'
# #
# #         code, grn_list, grn_list_three, GRNListString, resultString = pathway.ppi(tempfileName1, output_name, expLength, pre1, cutoff)
# #
# #     gi_lst = []
# #     with open(tempfileName1, "r") as f:
# #         for line in f:
# #             element = line.split("\t")
# #             gi_lst.append(element[1])
# #
# #     tempfileName2 = os.path.join(pre1, "ppi-grn-list.tree")
# #     with open(tempfileName2, "r") as f:
# #         line = f.readline()
# #         line = f.readline()
# #         for line in f:
# #             print line
# #
# #     outJsonDict = {}
#
# #     result = json.dumps(outJsonDict)
#     result = 'ok'

    return HttpResponse(result)

# def ppi_xiaotian_analysis(request):
#
#     #variables
#     cutoff = 1
#     times = 50
#     randomNumber = 100
#     result = ''
# #     requestingComplex = 'SMC1A SMC3 RAD21'
# #     requestingComplex = 'CHD3 CHD4 GATAD2A GATAD2B HDAC1 HDAC2 RBBP4 RBBP7 MBD2 MBD3 MTA1 MTA2 MTA3'
#     requestingComplex = 'ARID1A ARID1B SMARCA4 SMARCC1 SMARCC2 SMARCD1 SMARCD2 SMARCD3 ACTL6A ACTL6B'
#     requestingComplexList = requestingComplex.split(' ')
#
#     for j in range(times):
#         pre1 = '{0}ppi_tmp/firppiGlobal_{1}randomExp*{2}times{3}/'.format(pathway.tmpdir,randomNumber,times,j)
#         tempPPIFileTmpPPIAddr = os.path.join(pre1, "temp-ppi.txt")
#         tempPPIFilePPIGrnAddr = os.path.join(pre1, "ppi-grn.txt")
#         lineNumberList = []
#         lineNumber = 1
#
#         with open(tempPPIFileTmpPPIAddr, 'r') as f:
#             for line in f:
#                 lineList = line.split('\t')
#                 if lineList[1] not in requestingComplexList:
#                     lineNumber += 1
#                     continue
#                 else:
#                     lineNumberList.append(lineNumber)
#                     lineNumber += 1
#
#         grnLineNumber = 1
#         searchIndex = 0
#         grs = 0
#         meanTotal = 0
#         GRSRandomTimes = 50
#         numberList = range(lineNumber - 1)
#         for i in range(len(numberList)):
#             numberList[i] = numberList[i] + 1
#
#         lineLength = len(lineNumberList)
#         with open(tempPPIFilePPIGrnAddr, 'r') as f:
#             for line in f:
#                 if grnLineNumber != lineNumberList[searchIndex]:
#                     grnLineNumber += 1
#                     continue
#                 else:
#                     line = line.split('\t')
#                     for i in range(len(line)):
#                         line[i] = float(line[i])
#                     mean = numpy.mean(line)
#                     meanTotal += mean
#                     for i in range(lineLength):
#                         if(i != searchIndex):
#                             grs += ((line[lineNumberList[i] - 1] - mean)/numpy.std(line))*mean/(lineLength-1)
#                     grnLineNumber += 1
#                     searchIndex += 1
#                 if(searchIndex == lineLength):
#                     grs = grs / meanTotal
#                     result += str(grs) + ','
#                     break
#
#         #repeat GRSRandomTimes
#         randomGRSSum = 0
#         for i in range(GRSRandomTimes):
#             grnLineNumberRandom = 1
#             searchIndexRandom = 0
#             searchListSumRandom = 0
#             grsRandom = 0
#             meanTotalRandom = 0
#             randomNumberList = []
#             for k in range(len(requestingComplexList)):
#                 randomNumberList.append(random.choice(numberList))
#
#             with open(tempPPIFilePPIGrnAddr, 'r') as f:
#                 for line in f:
#                     if grnLineNumberRandom != randomNumberList[searchIndexRandom]:
#                         grnLineNumberRandom += 1
#                         continue
#                     else:
#                         line = line.split('\t')
#                         for i in range(len(line)):
#                             line[i] = float(line[i])
#                         mean = numpy.mean(line)
#                         meanTotalRandom += mean
#                         for i in range(lineLength):
#                             if(i != searchIndexRandom):
#                                 grsRandom += ((line[randomNumberList[i] - 1] - mean)/numpy.std(line))*mean/(lineLength-1)
#                         grnLineNumberRandom += 1
#                         searchIndexRandom += 1
#                     if(searchIndex == lineLength):
#                         grsRandom = grsRandom / meanTotalRandom
#                         randomGRSSum += grsRandom
#                         break
#         randomGRSMean = randomGRSSum / GRSRandomTimes
#         result += str(randomGRSMean) + ','
#     return HttpResponse(result)


@login_required(login_url=settings.LOGIN_PAGE)
def silac_peptide(request):
    exp_name=request.GET['exp_name']
    label=request.GET['label']
    if 'sid' in request.GET:
        sid = int(request.GET['sid'])
    else:
        sid = 0
    try:
        search_id = int(request.GET['search_id'])
    except:
        search_id = 0
    try:
        accession = str(request.GET['accession'])
    except:
        accession = 0
    try:
        exp_id = int(request.GET['exp_id'])
    except:
        exp_id = 0
    try:
        stype = str(request.GET['stype'])
    except:
        stype = ''
    try:
        rankid = int(request.GET['rankid'])
    except:
        rankid = 0
    try:
        symbol = str(request.GET['symbol'])
    except:
        symbol = 0
    start = int(request.GET['start'])
    limit = int(request.GET['limit'])
    end = start + limit
    peptide_list=labelledPeptide.objects.filter(labels=label).exclude(area=0)

    '''
    multi-sort is done below
    '''
    filters = []
    try:
        filters = json.loads(request.GET['filter'])
    except:
        filters = []
    property = '?'
    direction = ''
    try:
        sort = json.loads(str(request.GET['sort'])[1:-1])
        property = sort['property']
        if sort['direction'] == 'DESC':
            direction = '-'
        if property == 'exp_name':
            property = 'search'
    except:
        property = "ion_score"
        direction = '-'
    
    if len(filters) != 0:
        for filter in filters:
            if filter['type'] == 'string':
                if filter['field'] == 'exp_description':
                    peptide_list = peptide_list.filter(
                        search__exp__description__icontains=str(filter['value']))
                else:
                    kwargs = {str(filter['field']) +
                              '__icontains': str(filter['value'])}
                    peptide_list = peptide_list.filter(**kwargs)
            if filter['type'] == 'numeric':
                if filter['comparison'] == 'lt' or filter['comparison'] == 'gt':
                    kwargs = {
                        str(filter['field']) + '__' + str(filter['comparison']): str(filter['value'])}
                else:
                    kwargs = {str(filter['field']) +
                              '__exact': str(filter['value'])}
                peptide_list = peptide_list.filter(**kwargs)
            if filter['type'] == 'date':
                ptime = str(filter['value']).split('/')

                if filter['comparison'] == 'lt' or filter['comparison'] == 'gt':
                    today = str(datetime.datetime(
                        int(ptime[2]), int(ptime[0]), int(ptime[1])))
                    kwargs = {str(filter['field']) + '__' +
                              str(filter['comparison']): today}
                    peptide_list = peptide_list.filter(**kwargs)
                else:
                    today = datetime.datetime(int(ptime[2]), int(
                        ptime[0]), int(ptime[1])) - timedelta(days=1)
                    tomorrow = today + timedelta(days=2)
                    kwargs = {str(filter['field']) + '__gt': str(today)}
                    protein_list = protein_list.filter(**kwargs)
                    kwargs = {str(filter['field']) + '__lt': str(tomorrow)}
                    peptide_list = peptide_list.filter(**kwargs)
    if stype == 'protein':
        peptide_list = peptide_list.filter(protein_group_accessions__contains=accession).filter(
            search__id=search_id).exclude(type=-1)
        # return HttpResponse(str(accession)+''+str(search_id))
    elif stype == 'exper':
        peptide_list = peptide_list.filter(search__exp__name=exp_name).order_by(
            direction + property).exclude(type=-1)
    elif stype == 'search':
        peptide_list = peptide_list.filter(search__id=search_id).order_by(
            direction + property).exclude(type=-1)
    elif stype == 'gene':
        protein_list = protein_list.filter(symbol=symbol).filter(
            search__id=search_id).exclude(type=-1).values('accession')
        acc_list = []
        for tt in protein_list:
            acc_list.append(str(tt['accession']))
        temp_list = []
        for acc in acc_list:
            tt_list = peptide_list.filter(search__id=search_id).filter(
                protein_group_accessions__contains=acc).order_by(direction + property).exclude(type=-1)
            temp_list.extend(tt_list)
        peptide_list = list(set(temp_list))
    elif stype == 'anywhere':
        peptide_list = peptide_list.filter(Q(sequence__icontains=symbol) | Q(
            modification__icontains=symbol)).order_by(direction + property).exclude(type=-1)
    # only_list = peptide_list.values('sequence', 'modification')
    if stype != 'gene':
        count = peptide_list.count()
    else:
        count = len(peptide_list)

    # huge = peptide_list.aggregate(Max('area'))['area__max']
    if end > count or limit == -1:
        end = count
    peptide_list = peptide_list[start:end]
    # only_list = only_list[start:end]
    peptides = []
    for peptide in peptide_list:
        temp = {}
        temp['id'] = peptide.id
        temp['ms2'] = peptide.ms2_id
        temp['exp_description'] = peptide.search.exp.description
        temp['search_id'] = peptide.search_id
        temp['sequence'] = peptide.sequence
        temp['type'] = peptide.type
        temp['quality'] = peptide.quality
        temp['num_psms'] = peptide.num_psms
        temp['num_proteins'] = peptide.num_proteins
        temp['num_protein_groups'] = peptide.num_protein_groups
        temp['protein_group_accessions'] = peptide.protein_group_accessions
        temp['modification'] = peptide.modification
        temp['delta_cn'] = peptide.delta_cn
        temp['area'] = peptide.area
        temp['fot'] = peptide.fot
        temp['q_value'] = peptide.q_value
        temp['pep'] = peptide.pep
        temp['ion_score'] = peptide.ion_score
        temp['exp_value'] = peptide.exp_value
        temp['charge'] = peptide.charge
        temp['mh_da'] = peptide.mh_da
        temp['delta_m_ppm'] = peptide.delta_m_ppm
        temp['rt_min'] = round(float(peptide.rt_min), 2)
        temp['num_missed_cleavages'] = peptide.num_missed_cleavages
        if stype == 'anywhere':
            temp['exp_name'] = peptide.search.exp.name
        temp['fdr'] = peptide.fdr
        temp['from_where'] = peptide.from_where
        peptides.append(temp)
    data = {"data": peptides, "total": count}
    result = json.dumps(data, cls=DjangoJSONEncoder)
    return HttpResponse(result)


@login_required(login_url=settings.LOGIN_PAGE)
def silac_genes(request):
    exp_name=request.GET['exp_name']
    label=request.GET['label']
    stype = str(request.GET['stype']) if 'stype' in request.GET else ''
    symbol = str(request.GET['symbol']) if'symbol' in request.GET else ''
    start = int(request.GET['start']) if 'start' in request.GET else 0
    limit = int(request.GET['limit']) if 'limit' in request.GET else -1
    end = start + limit
    '''
    multi-sort is done below
    '''
    filters = []
    try:
        filters = json.loads(request.GET['filter'])
    except:
        filters = []
    property = '?'
    direction = ''
    try:
        sort = json.loads(str(request.GET['sort'])[1:-1])
        property = sort['property']
        if property == 'exp_name':
            property = 'search'
        if sort['direction'] == 'DESC':
            direction = '-'
    except:
        property = "area"
        direction = '-'

    gene_list=labelledGene.objects.filter(labels=label).exclude(area=0)
    
    if len(filters) != 0:
        for filter in filters:
            if filter['field'] == 'user_specified':
                anno_protein = user_defined.objects.filter(
                    user=request.user.id).filter(annotation__icontains=filter['value'])
                if stype != 'anywhere':
                    if stype == 'exper':
                        species = Search.objects.get(id=Search.objects.filter(
                            exp_id=sid).filter(type='exp')[0].id).exp.species
                    else:
                        species = Search.objects.get(id=sid).exp.species
                    anno_protein = anno_protein.filter(species=species)
                anno_proteins = anno_protein.values_list('symbol', flat=True)
                gene_list = gene_list.filter(symbol__in=anno_proteins)
                continue
            if filter['type'] == 'list':
                for anno in filter['value']:
                    kwargs = {str(filter['field']) + '__icontains': anno}
                    gene_list = gene_list.filter(**kwargs)
            if filter['type'] == 'string':
                if filter['field'] == 'exp_description':
                    gene_list = gene_list.filter(
                        search__exp__description__icontains=str(filter['value']))
                else:
                    kwargs = {str(filter['field']) +
                              '__icontains': str(filter['value'])}
                    gene_list = gene_list.filter(**kwargs)
            if filter['type'] == 'numeric':
                if filter['comparison'] == 'lt' or filter['comparison'] == 'gt':
                    kwargs = {
                        str(filter['field']) + '__' + str(filter['comparison']): str(filter['value'])}
                else:
                    kwargs = {str(filter['field']) +
                              '__exact': str(filter['value'])}
                gene_list = gene_list.filter(**kwargs)
            if filter['type'] == 'date':
                ptime = str(filter['value']).split('/')

                if filter['comparison'] == 'lt' or filter['comparison'] == 'gt':
                    today = str(datetime.datetime(
                        int(ptime[2]), int(ptime[0]), int(ptime[1])))
                    kwargs = {str(filter['field']) + '__' +
                              str(filter['comparison']): today}
                    gene_list = gene_list.filter(**kwargs)
                else:
                    today = datetime.datetime(int(ptime[2]), int(
                        ptime[0]), int(ptime[1])) - timedelta(days=1)
                    tomorrow = today + timedelta(days=2)
                    kwargs = {str(filter['field']) + '__gt': str(today)}
                    gene_list = gene_list.filter(**kwargs)
                    kwargs = {str(filter['field']) + '__lt': str(tomorrow)}
                    gene_list = gene_list.filter(**kwargs)
    if stype == 'exper':
        gene_list = gene_list.filter(search__exp__name=exp_name).exclude(type=-1)
    if stype == 'search':
        gene_list = gene_list.filter(search__id=sid).exclude(type=-1)
    if stype == 'anywhere':
        if property != 'search':
            gene_list = gene_list.filter(
                symbol__icontains=symbol).exclude(type=-1)
        else:
            gene_list = gene_list.filter(
                symbol__icontains=symbol).exclude(type=-1)
    if property == 'search':
        gene_list = gene_list.order_by(direction + 'search__exp__id')
    elif property == 'user_specified':  # some problems I don't know
        for gen in range(len(gene_list)):
            gene = gene_list[gen]
            anno = user_defined.objects.filter(
                user=request.user.id, species=gene.search.exp.species, symbol=gene.symbol)
            gene_list[gen].user_specified = anno[0].annotation if anno else ""
        sorted(gene_list, key=lambda x: x.user_specified)
    else:
        gene_list = gene_list.order_by(direction + property)
    count = gene_list.count()
    if end > count or limit == -1:
        end = count
    gene_list = gene_list[start:end]
    genes = []
    for gene in gene_list:
        temp = {}
        temp['id'] = gene.id
        temp['exp_description'] = gene.search.exp.description
        temp['search_id'] = gene.search_id
        temp['symbol'] = gene.symbol
        temp['gene_id'] = gene.gene_id
        temp['protein_gi'] = gene.protein_gi
        temp['num_proteins'] = gene.num_proteins
        temp['num_identified_proteins'] = gene.num_identified_proteins
        temp['num_uni_proteins'] = gene.num_uni_proteins
        temp['num_peptides'] = gene.num_peptides
        temp['num_uni_peptides'] = gene.num_uni_peptides
        anno = user_defined.objects.filter(
            user=request.user.id, species=gene.search.exp.species, symbol=gene.symbol)
        temp['user_specified'] = anno[0].annotation if anno else ""
        temp['area'] = gene.area
        temp['fot'] = gene.fot
        temp['ibaq'] = gene.ibaq
        temp['fdr'] = gene.fdr
        temp['description'] = gene.description
        temp['annotation'] = gene.annotation
        temp['modification'] = gene.modification
        if stype == 'anywhere':
            temp['exp_name'] = gene.search.exp.name
        temp['fdr'] = gene.fdr
        genes.append(temp)

    data = {"data": genes, "total": count}
    result = json.dumps(data, cls=DjangoJSONEncoder)

    return HttpResponse(result)

@login_required(login_url=settings.LOGIN_PAGE)
def silac_protein(request):
    exp_name=request.GET['exp_name']
    
    label=request.GET['label']

    stype = str(request.GET['stype']) if 'stype' in request.GET else ''

    symbol = str(request.GET['symbol']) if 'symbol' in request.GET else ''

    search_id = int(request.GET['search_id']
                    ) if 'search_id' in request.GET else 0

    protein_group_accessions = str(request.GET[
                                   'protein_group_accessions']) if 'protein_group_accessions' in request.GET else ''

    '''
    multi-sort is done below
    '''
    filters = []
    try:
        filters = json.loads(request.GET['filter'])
    except:
        filters = []
    property = '?'
    direction = ''
    try:
        sort = json.loads(str(request.GET['sort'])[1:-1])
        property = sort['property']
        if sort['direction'] == 'DESC':
            direction = '-'
    except:
        property = "coverage"
        direction = '-'
    protein_list=labelledProtein.objects.filter(labels=label).exclude(area=0)
    if stype == 'exper':
        protein_list = protein_list.filter(search__exp__name=exp_name).exclude(type=-1)
    if stype == 'search':
        protein_list = protein_list.filter(
            search__id=search_id).exclude(type=-1)
    if stype == 'gene':
        protein_list = protein_list.filter(symbol=symbol).filter(
            search__id=search_id).exclude(type=-1)
    if stype == 'peptide':
        protein_list = protein_list.filter(accession__in=protein_group_accessions.split(
            ';')).filter(search__id=search_id).exclude(type=-1)        
    if len(filters) != 0:
        for filter in filters:
            if filter['field'] == 'user_specified':
                anno_protein = user_defined.objects.filter(
                    user=request.user.id).filter(annotation__icontains=filter['value'])
                if stype != 'anywhere':
                    if stype == 'exper':
                        species = Search.objects.get(id=Search.objects.filter(
                            exp_id=sid).filter(type='exp')[0].id).exp.species
                    else:
                        species = Search.objects.get(id=sid).exp.species
                    anno_protein = anno_protein.filter(species=species)
                anno_proteins = anno_protein.values_list('symbol', flat=True)
                protein_list = protein_list.filter(symbol__in=anno_proteins)
                continue
            if filter['type'] == 'list':
                for anno in filter['value']:
                    kwargs = {str(filter['field']) + '__icontains': anno}
                    protein_list = protein_list.filter(**kwargs)
            elif filter['type'] == 'string':
                if filter['field'] == 'exp_description':
                    protein_list = protein_list.filter(
                        search__exp__description__icontains=str(filter['value']))
                else:
                    kwargs = {str(filter['field']) +
                              '__icontains': str(filter['value'])}
                    protein_list = protein_list.filter(**kwargs)

            elif filter['type'] == 'numeric':
                if filter['comparison'] == 'lt' or filter['comparison'] == 'gt':
                    kwargs = {
                        str(filter['field']) + '__' + str(filter['comparison']): str(filter['value'])}
                else:
                    kwargs = {str(filter['field']) +
                              '__exact': str(filter['value'])}
                protein_list = protein_list.filter(**kwargs)


    count = protein_list.count()

    if 'toGenome' in request.GET:
        gi = []
        for pro in protein_list:
            gi.append(pro.accession)
        # sid = Search.objects.filter(exp_id=sid).filter(type='exp')[0].id
        ExpID = Experiment.objects.get(id=ExpID).name
        result = genome.Protein2Genome_new(ExpID, gi)
        data = {'success': True, 'species': result[
            0], 'file': result[1], 'chr': result[2]}
        result = json.dumps(data, cls=DjangoJSONEncoder)
        return HttpResponse(result)

    start = int(request.GET['start'])if 'start' in request.GET else 0
    limit = int(request.GET['limit'])if 'limit' in request.GET else -1
    end = start + limit
    if end > count or limit == -1:
        end = count
    if property == 'exp_name':
        protein_list = protein_list.order_by(direction + 'search__exp__name')
    elif property == 'exp_description':
        protein_list = protein_list.order_by(
            direction + 'search__exp__description')
    elif property == 'user_specified':  # some problems I don't know
        for pro in range(len(protein_list)):
            protein = protein_list[pro]
            anno = user_defined.objects.filter(
                user=request.user.id, species=protein.search.exp.species, symbol=protein.symbol)
            protein_list[pro].user_specified = anno[
                0].annotation if anno else ""
        sorted(protein_list, key=attrgetter('user_specified'))
    else:
        protein_list = protein_list.order_by(direction + property)
    protein_list = protein_list[start:end]
    proteins = []

    for protein in protein_list:
        temp = {}
        temp['id'] = protein.id
        anno = user_defined.objects.filter(
            user=request.user.id, species=protein.search.exp.species, symbol=protein.symbol)
        temp['user_specified'] = anno[0].annotation if anno else ""
        temp['search_id'] = protein.search_id
        temp['exp_description'] = protein.search.exp.description
        temp['other_members'] = protein.other_members
        temp['accession'] = protein.accession
        temp['symbol'] = protein.symbol
        temp['description'] = protein.description
        temp['score'] = protein.score
        temp['coverage'] = protein.coverage
        temp['num_proteins'] = protein.num_proteins
        temp['num_uni_peptides'] = protein.num_uni_peptides
        temp['num_peptides'] = protein.num_peptides
        temp['num_psms'] = protein.num_psms
        temp['area'] = protein.area
        temp['length'] = protein.length
        temp['mw'] = protein.mw
        temp['fot'] = protein.fot
        temp['ibaq'] = protein.ibaq
        temp['fdr'] = protein.fdr
        temp['annotation'] = protein.annotation
        temp['modification'] = protein.modification
        temp['exp_name'] = protein.search.exp.name
#         temp['ref_score'] = ref_score_dict[protein.accession]
        proteins.append(temp)
    data = {"data": proteins, "total": count}
    result = json.dumps(data, cls=DjangoJSONEncoder)

    return HttpResponse(result)

def silac_protein_compare(request):
    exp_name=request.GET['exp_name']
    stype = str(request.GET['stype']) if 'stype' in request.GET else ''

    '''
    multi-sort is done below
    '''
    filters = []
    try:
        filters = json.loads(request.GET['filter'])
    except:
        filters = []
    property = '?'
    direction = ''
    try:
        sort = json.loads(str(request.GET['sort'])[1:-1])
        property = sort['property']
        if sort['direction'] == 'DESC':
            direction = '-'
    except:
        property = "coverage"
        direction = '-'
    if stype == 'exper':
        protein_list = labelledProtein.objects.filter(search__exp__name=exp_name).exclude(type=-1)
    heavy_protein_list=protein_list.filter(labels='heavy').exclude(area=0)
    light_protein_list=protein_list.filter(labels='light')
    protein_list = labelledProtein.objects.filter(search__exp__name=exp_name).exclude(type=-1).filter(labels='heavy')
    light_area={}
    light_ibaq={}
    light_ifot={}
    heavy_area={}
    heavy_ibaq={}
    heavy_ifot={}
    for protein in heavy_protein_list:
        acc=protein.accession
        heavy_area[acc]=protein.area
        heavy_ibaq[acc]=protein.ibaq
        heavy_ifot[acc]=protein.fot
    for protein in light_protein_list:
        acc=protein.accession
        light_area[acc]=protein.area
        light_ibaq[acc]=protein.ibaq
        light_ifot[acc]=protein.fot    
    if len(filters) != 0:
        for filter in filters:
            if filter['field'] == 'user_specified':
                anno_protein = user_defined.objects.filter(
                    user=request.user.id).filter(annotation__icontains=filter['value'])
                if stype != 'anywhere':
                    if stype == 'exper':
                        species = Search.objects.get(id=Search.objects.filter(
                            exp_id=sid).filter(type='exp')[0].id).exp.species
                    else:
                        species = Search.objects.get(id=sid).exp.species
                    anno_protein = anno_protein.filter(species=species)
                anno_proteins = anno_protein.values_list('symbol', flat=True)
                protein_list = protein_list.filter(symbol__in=anno_proteins)
                continue
            if filter['type'] == 'list':
                for anno in filter['value']:
                    kwargs = {str(filter['field']) + '__icontains': anno}
                    protein_list = protein_list.filter(**kwargs)
            elif filter['type'] == 'string':
                if filter['field'] == 'exp_description':
                    protein_list = protein_list.filter(
                        search__exp__description__icontains=str(filter['value']))
                else:
                    kwargs = {str(filter['field']) +
                              '__icontains': str(filter['value'])}
                    protein_list = protein_list.filter(**kwargs)

            elif filter['type'] == 'numeric':
                if filter['comparison'] == 'lt' or filter['comparison'] == 'gt':
                    kwargs = {
                        str(filter['field']) + '__' + str(filter['comparison']): str(filter['value'])}
                else:
                    kwargs = {str(filter['field']) +
                              '__exact': str(filter['value'])}
                protein_list = protein_list.filter(**kwargs)


    count = protein_list.count()

    if 'toGenome' in request.GET:
        gi = []
        for pro in protein_list:
            gi.append(pro.accession)
        # sid = Search.objects.filter(exp_id=sid).filter(type='exp')[0].id
        ExpID = Experiment.objects.get(id=ExpID).name
        result = genome.Protein2Genome_new(ExpID, gi)
        data = {'success': True, 'species': result[
            0], 'file': result[1], 'chr': result[2]}
        result = json.dumps(data, cls=DjangoJSONEncoder)
        return HttpResponse(result)

    start = int(request.GET['start'])if 'start' in request.GET else 0
    limit = int(request.GET['limit'])if 'limit' in request.GET else -1
    end = start + limit
    if end > count or limit == -1:
        end = count
#     if property == 'exp_name':
#         protein_list = protein_list.order_by(direction + 'search__exp__name')
#     elif property == 'exp_description':
#         protein_list = protein_list.order_by(
#             direction + 'search__exp__description')
#     elif property == 'user_specified':  # some problems I don't know
#         for pro in range(len(protein_list)):
#             protein = protein_list[pro]
#             anno = user_defined.objects.filter(
#                 user=request.user.id, species=protein.search.exp.species, symbol=protein.symbol)
#             protein_list[pro].user_specified = anno[
#                 0].annotation if anno else ""
#         sorted(protein_list, key=attrgetter('user_specified'))
#     else:
#         protein_list = protein_list.order_by(direction + property)
    protein_list = protein_list[start:end]
    proteins = []

    for protein in heavy_protein_list:
        temp = {}
#         temp['id'] = protein.id
        anno = user_defined.objects.filter(
            user=request.user.id, species=protein.search.exp.species, symbol=protein.symbol)
        temp['user_specified'] = anno[0].annotation if anno else ""
#         temp['search_id'] = protein.search_id
        temp['exp_description'] = protein.search.exp.description
        temp['other_members'] = protein.other_members
        temp['accession'] = protein.accession
        temp['symbol'] = protein.symbol
        temp['description'] = protein.description
        temp['score'] = protein.score
        temp['coverage'] = protein.coverage
        temp['num_proteins'] = protein.num_proteins
        temp['num_uni_peptides'] = protein.num_uni_peptides
        temp['num_peptides'] = protein.num_peptides
        temp['num_psms'] = protein.num_psms
        temp['harea'] = heavy_area[protein.accession]
        temp['larea'] = light_area[protein.accession]
        if light_area[protein.accession]>0:
            ratio=heavy_area[protein.accession]/light_area[protein.accession]
        else:
            continue
        temp['area_ratio'] = ratio
        temp['length'] = protein.length
        temp['mw'] = protein.mw
        temp['hfot'] = heavy_ifot[protein.accession]
        temp['lfot'] = light_ifot[protein.accession]
        if light_ifot[protein.accession]>0:
            ratio=heavy_ifot[protein.accession]/light_ifot[protein.accession]
        else:
            ratio=1e9
        temp['fot_ratio'] = ratio
        temp['hibaq'] = heavy_ibaq[protein.accession]
        temp['libaq'] = light_ibaq[protein.accession]
        if light_ibaq[protein.accession]>0:
            ratio=heavy_ibaq[protein.accession]/light_ibaq[protein.accession]
        else:
            ratio=1e9
        temp['ibaq_ratio'] = ratio
        temp['fdr'] = protein.fdr
        temp['annotation'] = protein.annotation
        temp['modification'] = protein.modification
        temp['exp_name'] = protein.search.exp.name
#         temp['ref_score'] = ref_score_dict[protein.accession]
        proteins.append(temp)
    proteins=sorted(proteins,key=lambda x: x[property])[start:end]
    data = {"data": proteins, "total": count}
    result = json.dumps(data, cls=DjangoJSONEncoder)

    return HttpResponse(result)



#20160808 for registration by zdd
#experiments_all_company (1)
#experiments_all_laboratory (N)
#experiments_all_laboratory_company (bulid relation)
def addACompany(request):
    companyName=request.GET['companyName']
    
    (object, created) = experiments.models.All_Company.objects.get_or_create(name=companyName, validated=True)
    #find created = False
    if created:
        prompt = "Add a company successfully! "
    else:
        prompt = companyName + "has existed!"
    
    data = {"success": created, "prompt":prompt}
    result = json.dumps(data, cls=DjangoJSONEncoder)
    return HttpResponse(result)

def addALaboratory(request):
    #for example
    #p1 = Publication(title='The Python Journal')
    #p1.save()
    #a1 = Article(headline='Django lets you build Web apps easily')
    #a1.save()
    #a1.publications.add(p1)
    createdFlag = False
    try:
        companyName=request.GET['companyName']
        laboratoryName=request.GET['laboratoryName']
        company = experiments.models.All_Company.objects.get(name=companyName, validated=True)
        laboratory = experiments.models.All_Laboratory(name=laboratoryName,validated=True)
        laboratory.save()
        laboratory.company.add(company)
        laboratory.save()
    except:
        prompt = "Add a laboratory unsuccessfully! "
    else:
        prompt = "Add a laboratory successfully! "
        createdFlag = True
    
    data = {"success": createdFlag, "prompt":prompt}
    result = json.dumps(data, cls=DjangoJSONEncoder)
    return HttpResponse(result)
