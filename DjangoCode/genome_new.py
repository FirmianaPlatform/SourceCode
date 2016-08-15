import gardener.models
import os
import commands
import time
import datetime
# using BLAT instead of BLAST
# Serving locate in ./gfClient 127.0.0.1 19001 ./ ../../../data/test.fasta ../../../data/test.out -q=prot -t=dnax
# Serving locate in'./gfServer start 127.0.0.1 19001
# ../../../data/hg38.2bit -trans'


def Protein2Genome_new(ExpID, protein_gis):
    output_folder = '/usr/local/firmiana/leafy/static/'
    spe_dic = {'Homo sapiens (Human)': 'human',
               'Sus scrofa (Pig)': 'pig',
               'Bos taurus (Bovine)': 'bovine',
               'Rattus norvegicus (Rat)': 'rat',
               'Mus musculus (Mouse)': 'mouse'}
    port_dic = {'human': '19001',
                'mouse': '19002',
                'rat': '19003',
                'bovine': '19004',
                'pig': '19005'
                }
    file_name = '{0}genome/{1}'.format(output_folder, time.time())
    print file_name
    species = gardener.models.Experiment.objects.get(name=ExpID).species
    species = spe_dic[species]
    port = port_dic[species]
    protein_gis = [protein_gi[3:] for protein_gi in protein_gis]
    fout = open('{}.fasta'.format(file_name), 'w')
    for protein_gi in protein_gis:
        protein = gardener.models.Fasta_Data.objects.get(protein_gi=protein_gi)
        fout.write('>' + protein.protein_gi + '|' +
                   protein.symbol + '|' + protein.description + '\n')
        fout.write(protein.sequence + '\n')
    fout.close()
    os.chdir('/usr/local/firmiana/data/ucsc/Genome/')
    cmd = '/usr/local/firmiana/external_tools/kentUtils/bin/gfClient '
    cmd = cmd + '127.0.0.1 ' + port + ' '
    cmd = cmd + './ '
    cmd = cmd + '{}.fasta '.format(file_name)
    cmd = cmd + '{}.psl -q=prot -t=dnax'.format(file_name)
    output = commands.getstatusoutput(cmd)
    print cmd
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
    fout.write('track name=Firmiana description="User Defined Tracks"' + '\n')
    f = open('{}.bed'.format(file_name), 'U')
    for line in f:
        fout.write(line)
    f.close()
    fout.close()
    out_file = '{}.bed'.format(file_name + '_new')
    out_file = out_file.replace('/usr/local/firmiana/leafy', '')
    return(species, out_file, max_pos)


def __main__():
    ExpID = 'Exp006295'
    protein_gi = ['gi|6671549']
    Protein2Genome_new(ExpID, protein_gi)
