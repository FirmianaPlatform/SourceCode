from gardener.models import *
import experiments.models
import csv
from django.http import HttpResponse, Http404, HttpResponseRedirect
def getPepLoc(request):
    exp = request.GET['expName']
    path = '/usr/local/firmiana/incubator/python/readFasta/'
    peptides = Exp_Peptide.objects.filter(search__exp__name=exp)
    fastaFile = experiments.models.Experiment.objects.filter(name=exp)[0].search_database.name
    if fastaFile == 'Human_refseq':
        fileName = path + 'human_protein_faa_2013_0704.fasta'
    elif fastaFile == 'Mouse_refseq':
        fileName = path + 'mouse_protein_faa_2013_0704.fasta'
    proSeq = {}
    seq = ''
    name = ''
    with open(fileName, 'U') as f:
        for line in f:
            if line[0] == '>':
                if seq != '':
                    proSeq[name] = seq
                word = line.split('|')
                seq = ''
                name = 'gi|' + word[1]
            else:
                seq = seq + line.strip()
        proSeq[name] = seq     
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename="pepLocation{0}.txt"'.format(exp)
    writer = csv.writer(response, delimiter='\t')
    writer.writerow(['Peptide', 'Protein ID', 'Protein Length', 'Position'])
    for pep in peptides:
        proteins = pep.protein_group_accessions.split(';')
        for pro in proteins:
            temp = []
            temp.append(pep.sequence)
            temp.append(pro)
            temp.append(len(proSeq[pro]))
            pos = proSeq[pro].index(pep.sequence.upper())
            temp.append(str(pos + 1) + '-' + str(pos + len(pep.sequence) + 1))
            temp = [str(pp) for pp in temp]
            writer.writerow(temp)
    return response


def coverage(request):
    # gi=request.GET['gi']
    gi = request.GET['accession']
    #gi = 'gi|47132620'
    seq = Fasta_Data.objects.filter(protein_gi=gi.split('|')[1])[0].sequence
    expName = request.GET['expName']
    peptide = Exp_Peptide.objects.filter(protein_group_accessions__contains=gi).filter(search__exp__name=expName).exclude(type=-1)
    oldSeq = seq
    newSeq = seq
    modiSeq=seq
    for pep in peptide:
        idx = seq.index(pep.sequence.upper())
        newSeq = newSeq[:idx] + newSeq[idx:idx + len(pep.sequence)].lower() + newSeq[idx + len(pep.sequence):]
        modiSeq = modiSeq[:idx] + pep.sequence + modiSeq[idx + len(pep.sequence):]
    low = 0
    for ch in newSeq:
        if ch.islower():
            low = low + 1
    print low * 1.0 / len(newSeq)
    content='<table><tr>'
    if len(modiSeq)<=60:
        content='<td align="right">1</td><td align="left">-</td><td align="right">'+str(len(modiSeq))+'</td><td align="left">'
    else:
        content=content+'<td align="right">1</td><td align="left">-</td><td align="left">60</td><td align="left">'
    idx=0
    black=False
    for modi in range(len(modiSeq)):
        if newSeq[modi].islower() and not black:
            black=True
            content=content+'<span style="font-weight:bold">'+modiSeq[modi]
        elif newSeq[modi].isupper() and black:
            black=False
            content=content+'</span>'+modiSeq[modi]
        else:
            content=content+modiSeq[modi]
        idx=idx+1
        if idx%60==0:
            if black:
                black=False
                content=content+'</span>'
            content=content+'</tr>'
            content=content+'<tr>'
            if idx+60<=len(modiSeq):
                content=content+'<td align="right">'+str(idx+1)+'</td><td align="left">-</td><td align="right">'+str(idx+60)+'</td><td align="right">'
            else:
                content=content+'<td align="right">'+str(idx+1)+'</td><td align="left">-</td><td align="right">'+str(len(modiSeq))+'</td><td align="right">'
        elif idx%10==0:
            if black:
                black=False
                content=content+'</span>'
            content=content+'</td><td align="left">'
    content=content+'</tr></table>'
    print content
    return HttpResponse(content)
        
    
def getCmpMetadata(Exps):
    Exps='exp_1389_1_1,exp_1388_1_1,exp_1387_1_1,exp_1386_1_1,exp_1385_1_1,exp_1384_1_1,exp_1383_1_1,exp_1382_1_1,exp_1381_1_1,exp_1380_1_1,exp_1379_1_1,exp_1378_1_1,exp_1377_1_1,exp_1376_1_1,exp_1375_1_1,exp_1374_1_1,exp_1373_1_1,exp_1372_1_1,exp_1371_1_1,exp_1370_1_1,exp_1369_1_1,exp_1368_1_1,exp_1123_1_1,exp_1122_1_1,exp_1121_1_1,exp_1120_1_1,exp_1117_1_1,exp_1116_1_1,exp_1115_1_1,exp_1114_1_1,exp_1113_1_1,exp_1112_1_1,exp_1111_1_1,exp_1110_1_1,exp_1109_1_1,exp_1108_1_1,exp_1107_1_1,exp_1106_1_1,exp_1105_1_1,exp_1104_1_1,exp_1103_1_1,exp_1102_1_1,exp_1101_1_1,exp_1100_1_1,exp_1099_1_1,exp_1098_1_1,exp_1097_1_1,exp_1096_1_1,exp_1095_1_1,exp_1094_1_1,exp_1093_1_1,exp_1092_1_1,exp_1091_1_1,exp_1090_1_1,exp_1089_1_1,exp_1088_1_1,exp_1087_1_1,exp_1086_1_1,exp_1085_1_1,exp_1084_1_1,exp_1083_1_1,exp_1082_1_1,exp_989_1_1,exp_988_1_1,exp_987_1_1,exp_986_1_1,exp_985_1_1,exp_984_1_1,exp_983_1_1,exp_982_1_1,exp_967_1_1,exp_966_1_1,exp_965_1_1,exp_964_1_1,exp_963_1_1,exp_962_1_1,exp_961_1_1,exp_960_1_1,exp_959_1_1,exp_958_1_1,exp_957_1_1,exp_956_1_1,exp_955_1_1,exp_954_1_1,exp_694_1_1,exp_693_1_1,exp_692_1_1,exp_691_1_1,exp_690_1_1,exp_689_1_1,exp_688_1_1,exp_687_1_1,exp_686_1_1,exp_685_1_1,exp_684_1_1,exp_683_1_1,exp_682_1_1,exp_681_1_1,exp_680_1_1,exp_679_1_1,exp_678_1_1,exp_677_1_1,exp_634_1_1,exp_633_1_1,exp_632_1_1,exp_631_1_1,exp_630_1_1,exp_629_1_1,exp_628_1_1,exp_627_1_1,exp_626_1_1,exp_625_1_1,exp_358_1_1,exp_357_1_1,exp_355_1_1,exp_354_1_1,exp_353_1_1,exp_352_1_1,exp_351_1_1,exp_350_1_1,exp_322_1_1,exp_321_1_1,exp_320_1_1,exp_319_1_1,exp_318_1_1,exp_317_1_1,exp_316_1_1,exp_315_1_1,exp_314_1_1,exp_313_1_1,exp_312_1_1,exp_311_1_1,exp_310_1_1,exp_309_1_1,exp_308_1_1,exp_307_1_1,exp_306_1_1,exp_305_1_1,exp_304_1_1,exp_303_1_1,exp_302_1_1,exp_301_1_1,exp_300_1_1,exp_299_1_1,exp_298_1_1,exp_297_1_1,exp_295_1_1,exp_294_1_1'
    Exps=Exps.split(',')
    Exps=[int(pp.split('_')[1]) for pp in Exps]
    Exps=[Experiment.objects.get(id=pp).name for pp in Exps]
    out='/home/galaxy/tio2.txt'
    f=open(out,'wb')
    f.write('ExpName\tExperimenter\tDate\tType\tDescription\tSample No\tReagent No\tSeperation\tDigest\tDatabase Params\tIspec No\n')
    for exp in Exps:
        f.write(exp)
        f.write('\t')
        exp=int(exp.split('Exp')[1])
        exp=experiments.models.Experiment.objects.get(id=exp)
        f.write(exp.company+'/'+exp.lab+'/'+exp.experimenter)
        f.write('\t')
        f.write(str(exp.date))
        f.write('\t')
        f.write(exp.type.name)
        f.write('\t')
        f.write(exp.description)
        f.write('\t')
        if len(exp.samples.all())>0:
            f.write(str(exp.samples.all()[0].id))
        else:
            f.write('')
        f.write('\t')

        if len(exp.reagents.all())>0:
            f.write(str(exp.reagents.all()[0].id))
        else:
            f.write('')
        f.write('\t')

        if len(exp.separation_methods.all())>0:
            f.write(exp.separation_methods.all()[0].name)
        else:
            f.write('')
        f.write('\t')

        f.write(exp.digest_type.name+'/'+exp.digest_enzyme.name)
        f.write('\t')

        f.write(exp.search_database.name+'/'+exp.instrument_name.name+'/'+exp.ms1.name+'/'+exp.ms1_details.name+exp.ms2.name+'/'+exp.ms2_details.name)
        f.write('\t')

        f.write(exp.fm_no)

        f.write('\n')
    f.close()
    
    
    
def readFasta(fileName):
    filePath='/usr/local/firmiana/data/ProteinSequence/'
    Proteins={}
    seq=''
    gi=''
    with open(filePath+fileName,'r') as f:
        for line in f:
            if line[0]=='>' :
                if seq!='':
                    Proteins[gi]=seq
                gi=line.split('|')[1]
                gi='gi|'+gi
                seq=''
            else:
                seq=seq+line.strip()
        return Proteins
    
def preWork(peptides,proteins,selectModification):
    PTM=[]
    for peptide in peptides:
        gis=peptide['gis'].split(';')#gi|4505835
        sequence=peptide['sequence']#SLDDsEEDDDEDSGHSSR
        modification=peptide['modification'].split(';')#Phospho (ST)(5)
        peps=[]
        for modi in modification:
            if selectModification in modi:
                peps.append(sequence,modi)
                
                
                
                
                
                
def WeiminOutput():
    import gardener.models
    import experiments.models
    f=open('/home/galaxy/CNHPP.txt','U')
    output_exp=[]
    for line in f:
        output_exp.append(line.split('\t')[0])
        print line.split('\t')[0]
    meta_exp=experiments.models.Experiment.objects.filter(name__in=output_exp)
    f=open('/home/galaxy/CNHPP_OUT.txt','wb')
    for meta in meta_exp:
        f.write(meta.name)
        tissue=meta.samples.all()[0].source_tissue
        try:
            if tissue.tissueType.name=='Tumor':
                f.write('T')
            else:
                f.write('P')
        except:
            print tissue
        f.write('\t')
        f.write('Human\t')
        try:
            f.write(tissue.tissueOrgan.name)
        except:
            print tissue
        f.write('\t')
        try:
            f.write(str(meta.samples.all()[0].id)+'\t')
        except:
            print tissue.id
        try:
            f.write(tissue.specific_ID+'\t')
        except:
            f.write('NULL\t')
        f.write(meta.samples.all()[0].ubi_subcells.all()[0].name+'\t')
        try:
            f.write(tissue.gender.name+'\n')
        except:
            f.write('null\n')
    f.close()
    
def getMetadata():
    import gardener.models
    import experiments.models
    f=open('/home/galaxy/profiling.txt','U')
    output_exp=[]
    for line in f:
        output_exp.append(line.strip())
    f.close()
    
    meta_exp=experiments.models.Experiment.objects.filter(id__in=output_exp)
    f=open('/home/galaxy/profiling_metadata.txt','wb')
    for meta in meta_exp:
        f.write(meta.name+'\t')
        tissue=meta.samples.all()[0].source_tissue
        try:
            f.write(tissue.gender.name+'\t')
        except:
            f.write('null\t')
        try:
            f.write(tissue.tissueOrgan.name)
        except:
            print tissue
        f.write('\t')
        try:
            f.write(tissue.tissueStructure)
        except:
            print tissue
        f.write('\t')
        try:
            if tissue.tissueType.name=='Tumor':
                f.write('T')
            else:
                f.write('P')
        except:
            print tissue
        f.write('\t')
        f.write(meta.type.name+'\t')
        f.write(meta.separation_methods.all()[0].name+'\t')
        f.write(meta.digest_type.name+'\t')
        f.write(meta.instrument_name.name+'\n')
    f.close()
    
    
    
def parseGeneloaction(filenames):
    f=open(filenames,'U')
    line_number=0
    pks=[]
    for line in f:
        line_number=line_number+1
        if line_number<6:
            continue
        word=line.strip().split('\t')
        accession=word[9].split('ref')[0][:-1]
        word=[accession]+word
        location=ProteinLocation.create(word)
        pks.append(location)
    print 'done'
    ProteinLocation.objects.bulk_create(pks)
    f.close()
    print 'done'
    
