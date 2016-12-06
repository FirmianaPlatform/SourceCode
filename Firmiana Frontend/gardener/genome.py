import os
import sys
import re
import time
import datetime
import commands
import Bio
from Bio import SeqIO
from Bio.Blast.Applications import NcbiblastxCommandline
import gardener.models
from multiprocessing.dummy import Pool as ThreadPool
tmpdir = '/usr/local/firmiana/leafy/static/'


def time_now():
    print datetime.datetime.now().strftime('%X')


def get_loc(name):
    loc_dic = {}
    for line in open(name):
        tmp = {}
        cls = line.strip().split('\t')
        if cls[3] not in loc_dic:
            tmp['ch'] = cls[0]
            tmp['st'] = cls[1]
            tmp['et'] = cls[2]
            loc_dic[cls[3]] = tmp
    return(loc_dic)


def get_acc_mRNA(pro_gi):
    result = gardener.models.gene2accession.objects.filter(protein_gi=pro_gi)
    if len(result) > 0:
        result = result[0]
        result.mrna_accession = '' if result.mrna_accession == None or result.mrna_accession == '-' else result.mrna_accession
        return result.mrna_accession
    else:
        return ''


def pep2loc_file(para):
    dna_list, chr, start, nmid, seq = para
    ti = time.time()
    fpep = '/dev/shm/temp_pep{0}'.format(ti)
    fdna = '/dev/shm/temp_dna{0}'.format(ti)
    fout = '/dev/shm/temp_blastout{0}'.format(ti)
    if os.path.isfile(fout):
        os.remove(fout)

    pep = open(fpep, 'w')
    dna = open(fdna, 'w')

    pep.write(seq)
    pep.close()
    dna.write(re.sub(r'[a-z]', '', dna_list.get_raw(nmid)))
    dna.close()
    return start, ti, seq, chr


def pep2loc(para):
    start, ti, seq, chr = para
    fpep = '/dev/shm/temp_pep{0}'.format(ti)
    fdna = '/dev/shm/temp_dna{0}'.format(ti)
    fout = '/dev/shm/temp_blastout{0}'.format(ti)
    if os.path.isfile(fout):
        os.remove(fout)
    blastx_cline = NcbiblastxCommandline(
        cmd='tblastn', query=fpep, subject=fdna, evalue=0.001, outfmt=10, out=fout)
    blastx_cline()
    out = []
    while not os.path.isfile(fout):
        time.sleep(0.1)
    for line in open(fout, 'r'):
        tmp = []
        cls = line.strip().split(',')
        if cls[2] == '100.00':
            tmp.append(chr)
            st = int(cls[8]) if int(cls[8]) < int(cls[9]) else int(cls[9])
            et = int(cls[9]) if int(cls[8]) < int(cls[9]) else int(cls[8])
            tmp.append(str(int(start) + st))
            tmp.append(str(int(start) + et))
            tmp.append(seq)
            out.append(tmp)
    return(out)


def Protein2Genome(ExpID, protein_gis):

    species = gardener.models.Experiment.objects.get(name=ExpID).species
    if species == 'Homo sapiens (Human)':
        spec = 'human'
    else:
        spec = 'mouse'
    chr = ''
    temp_list = []
    loc_dic = get_loc(
        '/usr/local/firmiana/data/ncbi_refseq/human_refseq_gene.bed')
    dna_list = SeqIO.index(
        '/usr/local/firmiana/data/ncbi_refseq/human_uniq_refseq.fa', 'fasta')
    peptides = gardener.models.Exp_Peptide.objects.filter(
        search__exp__name=ExpID)
    pro_dict = {}
    for protein_gi in range(len(protein_gis)):
        protein_gis[protein_gi] = protein_gis[protein_gi].split('|')[1]
    for pep in peptides:
        accs = pep.protein_group_accessions
        seq = pep.sequence
        accs = accs.split(';')
        for acc in accs:
            acc = acc.split('|')[1]
            if acc in protein_gis:
                if acc not in pro_dict:
                    pro_dict[acc] = set()
                pro_dict[acc].add(seq)
    #pool = ThreadPool(20)
    parameter = []
    result = []
    for protein_gi in protein_gis:
        mrna_acc = get_acc_mRNA(protein_gi)
        if mrna_acc != '':
            mrna_acc = mrna_acc.split('.')[0]
            nmid = mrna_acc
            if nmid in loc_dic and nmid in dna_list:
                for pep in pro_dict[protein_gi]:
                    para = pep2loc_file(
                        (dna_list, loc_dic[nmid]['ch'], loc_dic[nmid]['st'], nmid, pep))
                    res = pep2loc(para)
                    # print res
                    for temp in res:
                        chr = temp[0]
                        if int(temp[1]) > int(temp[2]):
                            print temp[1], temp[2], file_name
                        line = '\t'.join(temp)
                        line += '\n'
                        temp_list.append(line)
    #=========================================================================
    # time_now()
    # results = pool.map(pep2loc,parameter)
    #=========================================================================

    # pool.close()
    # pool.join()
    # time_now()
    file_name = '{0}genome/{1}.txt'.format(tmpdir, time.time())

    f = open(file_name, 'w')

    temp_list = list(set(temp_list))
    f.write('track name=ProteinToGenome description=""\n')
    for t in temp_list:
        f.write(t)
    f.close()
    file_name = file_name.replace('/usr/local/firmiana/leafy', '')
    return (spec, file_name, chr)


# def Protein2Genome_new(ExpID, protein_gis):
#     output_folder = '/usr/local/firmiana/leafy/static/'
#     spe_dic = {'Homo sapiens (Human)': 'human',
#                'Sus scrofa (Pig)': 'pig',
#                'Bos taurus (Bovine)': 'bovine',
#                'Rattus norvegicus (Rat)': 'rat',
#                'Mus musculus (Mouse)': 'mouse'}
#     port_dic = {'human': '19001',
#                 'mouse': '19002',
#                 'rat': '19003',
#                 'bovine': '19004',
#                 'pig': '19005'
#                 }
#     file_name = '{0}genome/{1}'.format(output_folder, time.time())
#     print file_name
#     species = gardener.models.Experiment.objects.get(name=ExpID).species
#     species = spe_dic[species]
#     port = port_dic[species]
#     protein_gis = [protein_gi[3:] for protein_gi in protein_gis]
#     fout = open('{}.fasta'.format(file_name), 'w')
#     for protein_gi in protein_gis:
#         protein = gardener.models.Fasta_Data.objects.get(protein_gi=protein_gi)
#         fout.write('>' + protein.protein_gi + '|' +
#                    protein.symbol + '|' + protein.description + '\n')
#         fout.write(protein.sequence + '\n')
#     fout.close()
#     os.chdir('/usr/local/firmiana/data/ucsc/Genome/')
#     cmd = '/usr/local/firmiana/external_tools/kentUtils/bin/gfClient '
#     cmd = cmd + '127.0.0.1 ' + port + ' '
#     cmd = cmd + './ '
#     cmd = cmd + '{}.fasta '.format(file_name)
#     cmd = cmd + '{}.psl -q=prot -t=dnax'.format(file_name)
#     output = commands.getstatusoutput(cmd)
#     print cmd
#     cmd = '/usr/local/firmiana/external_tools/kentUtils/bin/pslToBed '
#     cmd = cmd + '{}.psl '.format(file_name)
#     cmd = cmd + '{}.bed'.format(file_name)
#     print cmd
#     output = commands.getstatusoutput(cmd)
#     print output
#     f = open('{}.bed'.format(file_name), 'U')
#     pos = {}
#     for line in f:
#         word = line.split('\t')
#         if word[0] not in pos:
#             pos[word[0]] = []
#         pos[word[0]].append((word[1], word[2]))
#     f.close()
#     print pos
#     max_num = 0
#     max_pos = ''
#     for posit in pos:
#         if len(pos[posit]) > max_num:
#             max_num = len(pos[posit])
#             max_pos = posit
#     print max_pos
#     left = 1e10
#     right = 0
#     print pos[max_pos]
#     for pp in pos[max_pos]:
#         left = min(left, int(pp[0]))
#         right = max(right, int(pp[1]))
#     fout = open('{}.bed'.format(file_name + '_new'), 'w')
#     fout.write('browser position {}:{}-{}'.format(max_pos,
#                                                   left, right) + '\n')
#     fout.write('track name=Firmiana description="User Defined Tracks"' + '\n')
#     f = open('{}.bed'.format(file_name), 'U')
#     for line in f:
#         fout.write(line)
#     f.close()
#     fout.close()
#     out_file = '{}.bed'.format(file_name + '_new')
#     out_file = out_file.replace('/usr/local/firmiana/leafy', '')
#     return(species, out_file, max_pos)
def Protein2Genome_new(ExpID, protein_gis):
    output_folder = '/usr/local/firmiana/leafy/static/'
    spe_dic = {'Homo sapiens (Human)': 'human',
               'Sus scrofa (Pig)': 'pig',
               'Bos taurus (Bovine)': 'bovine',
               'Rattus norvegicus (Rat)': 'rat',
               'Mus musculus (Mouse)': 'mouse'}
    file_name = '{0}genome/{1}'.format(output_folder, time.time())
    print file_name
    species = gardener.models.Experiment.objects.get(name=ExpID).species
    species = spe_dic[species]
    psl_file = '{}.psl'.format(file_name)
    fout = open(psl_file, 'w')
    fout.write('psLayout version 3\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\nmatch\tmis- \trep. \tN\'s\tQ gap\tQ gap\tT gap\tT gap\tstrand\tQ        \tQ   \tQ    \tQ  \tT        \tT   \tT    \tT  \tblock\tblockSizes \tqStarts\t tStarts\n     \tmatch\tmatch\t   \tcount\tbases\tcount\tbases\t      \tname     \tsize\tstart\tend\tname     \tsize\tstart\tend\tcount\t\t\t\n - --------------------------------------------------------------------------------------------------------------------------------------------------------------\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\n')
    for gi in protein_gis:
        psl_line = gardener.models.ProteinLocation.objects.filter(accession=gi)
        for ps in psl_line:
            line = [str(word) for word in ps.returnLine()]
            fout.write('\t'.join(line) + '\n')
    fout.close()
    print psl_file
    cmd = '/usr/local/firmiana/external_tools/kentUtils/bin/pslToBed '
    cmd = cmd + '{}.psl '.format(file_name)
    cmd = cmd + '{}.bed'.format(file_name)
    print cmd
    output = commands.getstatusoutput(cmd)
    print output
    f = open('{}.bed'.format(file_name), 'U')
    pos = {}
    for line in f:
        word = line.split('\t')
        if word[0] not in pos:
            pos[word[0]] = []
        pos[word[0]].append((word[1], word[2]))
    f.close()
    print pos
    max_num = 0
    max_pos = ''
    for posit in pos:
        if len(pos[posit]) > max_num:
            max_num = len(pos[posit])
            max_pos = posit
    print max_pos
    left = 1e10
    right = 0
    print pos[max_pos]
    for pp in pos[max_pos]:
        left = min(left, int(pp[0]))
        right = max(right, int(pp[1]))
    fout = open('{}.bed'.format(file_name + '_new'), 'w')
    fout.write('browser position {}:{}-{}'.format(max_pos,
                                                  left, right) + '\n')
    fout.write('track name=Firmiana description="Firmiana Tracks"' + '\n')
    f = open('{}.bed'.format(file_name), 'U')
    for line in f:
        fout.write(line)
    f.close()
    fout.close()
    out_file = '{}.bed'.format(file_name + '_new')
    out_file = out_file.replace('/usr/local/firmiana/leafy', '')
    return(species, out_file, max_pos)


def __main__():
    ExpID = 'Exp001446'
    protein_gi = 'gi|4506671'
    Protein2Genome(ExpID, protein_gi)
