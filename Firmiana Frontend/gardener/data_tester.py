import sys
import random
import os
import re
import numpy as np
from datetime import datetime, date, time
sys.path.insert(0,'/usr/local/firmiana/leafy/')
from django.conf import settings
from gardener.models import *
from django.utils import timezone


def create_search(exp):
    for n_re in range(int(exp.num_repeat)):
        for n_fr in range(int(exp.num_fraction)):
            repeat_id=n_re
            fraction_id=n_fr
            name="Search"+random.choice(("Ref","Test","BPRC_1"))+"_"+str(fraction_id)+"_"+str(repeat_id)
            num_spectrum=int(random.uniform(0.8,1.2)*exp.num_spectrum/exp.num_fraction) if exp.num_spectrum>0 and exp.num_fraction>0 else 0
            num_peptide=int(random.uniform(0.8,1.2)*exp.num_peptide/exp.num_fraction) if exp.num_spectrum>0 and exp.num_fraction>0 else 0
            num_isoform=int(random.uniform(0.8,1.2)*exp.num_isoform/exp.num_fraction) if exp.num_spectrum>0 and exp.num_fraction>0 else 0  
            log="Software parameters and log summaryI"
            date=exp.index_date
            user=random.choice(("Lihong Diao","ChenDing","BPRC_1"))
            stage=random.randint(1,10)
            Search.objects.create(repeat_id=repeat_id,fraction_id=fraction_id,name=name,exp=exp,num_spectrum=num_spectrum,num_peptide=num_peptide,
                                  num_isoform=num_isoform,log=log,date=date,user=user,stage= stage)


def sampling_matrix(mx,num_out):
    newlist=range(mx.shape[0])
    random.shuffle(newlist)
    outmx=mx[newlist[0:random.randint(num_out,mx.shape[0])],:]
    return outmx

def get_peptide(pro,mpep):
    outm=np.zeros((1,18))
    for n_mpep in range(mpep.shape[0]):
        if pro in mpep[n_mpep,5]:
            outm=np.vstack((outm,mpep[n_mpep,]))
    if outm.shape[0]>1:
        return outm[1:,:]
    else:
        return False
    
             
        
# mpro=np.genfromtxt("/usr/local/firmiana/incubator/data/protein.txt",dtype='str',comments="///",delimiter="\t")
# mpep=np.genfromtxt("/usr/local/firmiana/incubator/data/peptide.txt",dtype='str',comments="///",delimiter="\t")
def create_protein_peptide(search,mpro,mpep):
    mpro=mpro[1:,:]
    mpep=mpep[1:,:]
    outmpro=sampling_matrix(mpro,20)
    smpro=0
    for n_mpro in range(outmpro.shape[0]):
        area_i=random.uniform(0.1,10)
        pro=Protein.objects.create(search=search,
                               accession=outmpro[n_mpro,0],
                               symbol="Need Update",
                               description=outmpro[n_mpro,1],
                               score=outmpro[n_mpro,2],
                               coverage=outmpro[n_mpro,3],
                               num_proteins=outmpro[n_mpro,4],
                               num_uni_peptides=outmpro[n_mpro,5],
                               num_peptides=outmpro[n_mpro,6],
                               num_psms=outmpro[n_mpro,7],
                               area=area_i*(float(outmpro[n_mpro,8]) if len(outmpro[n_mpro,8])>0 else 0),
                               length=outmpro[n_mpro,9],
                               mw=outmpro[n_mpro,10],
                               calc_pi=outmpro[n_mpro,11],
                               )
        mpep_out=get_peptide(pro.accession,mpep)
        if mpep_out.shape>1:
           mpep_out= sampling_matrix(mpep_out,1)
           for n_mpep in range(mpep_out.shape[0]):
               pep=Peptide.objects.create(protein=pro,
                                          quality=mpep_out[n_mpep,0],
                                          sequence=mpep_out[n_mpep,1],
                                          num_psms=mpep_out[n_mpep,2],
                                          num_proteins=mpep_out[n_mpep,3],
                                          num_protein_groups=mpep_out[n_mpep,4],
                                          protein_group_accessions=mpep_out[n_mpep,5],
                                          modification=mpep_out[n_mpep,6],
                                          delta_cn=mpep_out[n_mpep,7],
                                          area=area_i*(float(mpep_out[n_mpep,8]) if len(mpep_out[n_mpep,8])>0 else 0),
                                          q_value=mpep_out[n_mpep,9],
                                          pep=mpep_out[n_mpep,10],
                                          ion_score=mpep_out[n_mpep,11],
                                          exp_value=mpep_out[n_mpep,12],
                                          charge=mpep_out[n_mpep,13],
                                          mh_da=mpep_out[n_mpep,14],
                                          delta_m_ppm=mpep_out[n_mpep,15],
                                          rt_min=mpep_out[n_mpep,16],
                                          num_missed_cleavages=mpep_out[n_mpep,17],
                                          )
 
def make_geneinfo():
    fg=open("/usr/local/firmiana/incubator/data/ncbi/gene_info","r")
    timezone.localtime(timezone.now())
    for (num,line) in enumerate(fg): 
        if num==0:
            continue
        cols=line.strip().split("\t")
        if cols[0] in ("9606","10090"):
            GeneInfo.objects.create(    tax_id = cols[0],
                                        gene_id = cols[1],
                                        symbol = cols[2],
                                        locustag = cols[3],
                                        synonyms = cols[4],
                                        dbxrefs = cols[5],
                                        chromosome = cols[6],
                                        maplocation = cols[7],
                                        description =cols[8],
                                        type = cols[9],
                                        symbolfromauth = cols[10],
                                        fullname = cols[11],
                                        status = cols[12],
                                        others = cols[13],
                                        moddate = datetime.strptime(cols[14], "%Y%m%d")                                    
                                   )
            

make_geneinfo()
# all_exp=Experiment.objects.all()
# for exp in all_exp:
#     for i in range(int(exp.num_fraction)):
#         create_search(exp)


# all_search=Search.objects.all()
# for search in all_search:
#     create_protein_peptide(search,mpro,mpep)
 


