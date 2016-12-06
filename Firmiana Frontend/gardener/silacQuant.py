import gardener.models
import experiments.models


def get_ibaq_num(pro_seq):
    length = len(pro_seq)
    tmp_len = 0
    ans = 0
    for i in range(length):
        tmp_len = tmp_len + 1
        if pro_seq[i] == 'K' or pro_seq[i] == 'R':
            if i == length - 1 or pro_seq[i + 1] != 'P':
                if tmp_len >= 7 and tmp_len <= 40:
                    ans = ans + 1
            tmp_len = 0
    if ans == 0:
        ans = 1
    return ans


def SILAC(exp):
    a = 1
    a = a + 1
exp = 'Exp007004'
experiment = experiments.models.Experiment.objects.get(name=exp)
modification = []
for dynamic_modification in experiment.dynamic_modifications.all():
    if 'Label' in dynamic_modification.name:
        modification.append(dynamic_modification.name)
peptides = gardener.models.Exp_Peptide.objects.filter(search__exp__name=exp)
heavy_peptides = []
light_peptides = []
for pep in peptides:
    heavy = False
    for modi in modification:
        if modi in pep.modification:
            heavy_peptides.append(pep)
            heavy = True
            break
    if not heavy:
        light_peptides.append(pep)
heavy = []
for heavy_peptide in heavy_peptides:
    tmp_peptide = gardener.models.labelledPeptide.create(
        heavy_peptide, 'heavy')
    heavy.append(tmp_peptide)
gardener.models.labelledPeptide.objects.bulk_create(heavy)
light = []
for light_peptide in light_peptides:
    tmp_peptide = gardener.models.labelledPeptide.create(
        light_peptide, 'light')
    light.append(tmp_peptide)
gardener.models.labelledPeptide.objects.bulk_create(light)

proteins = gardener.models.Exp_Protein.objects.filter(search__exp__name=exp)
total_ibaq_heavy = 0
heavy_proteins = []
for protein in proteins:
    area = 0
    sequence = gardener.models.Fasta_Data.objects.get(
        protein_gi=protein.accession.split('|')[1]).sequence
    ibaq_num = get_ibaq_num(sequence)
    for pep in heavy:
        if protein.accession in pep.protein_group_accessions:
            area = area + pep.area
    ibaq = area / ibaq_num
    total_ibaq_heavy = ibaq + total_ibaq_heavy
for protein in proteins:
    area = 0
    sequence = gardener.models.Fasta_Data.objects.get(
        protein_gi=protein.accession.split('|')[1]).sequence
    ibaq_num = get_ibaq_num(sequence)
    for pep in heavy:
        if protein.accession in pep.protein_group_accessions:
            area = area + pep.area
    ibaq = area / ibaq_num
    ifot = ibaq / total_ibaq_heavy*1e6
    tmp_protein = gardener.models.labelledProtein.create(
        protein, 'heavy', protein.num_uni_peptides,
        protein.num_peptides, area, ifot, ibaq)
    heavy_proteins.append(tmp_protein)
gardener.models.labelledProtein.objects.bulk_create(heavy_proteins)

light_proteins = []
total_ibaq_light = 0
for protein in proteins:
    area = 0
    sequence = gardener.models.Fasta_Data.objects.get(
        protein_gi=protein.accession.split('|')[1]).sequence
    ibaq_num = get_ibaq_num(sequence)
    for pep in light:
        if protein.accession in pep.protein_group_accessions:
            area = area + pep.area
    ibaq = area / ibaq_num
    total_ibaq_light = ibaq + total_ibaq_light
for protein in proteins:
    area = 0
    sequence = gardener.models.Fasta_Data.objects.get(
        protein_gi=protein.accession.split('|')[1]).sequence
    ibaq_num = get_ibaq_num(sequence)
    for pep in light:
        if protein.accession in pep.protein_group_accessions:
            area = area + pep.area
    ibaq = area / ibaq_num
    ifot = ibaq / total_ibaq_light*1e6
    tmp_protein = gardener.models.labelledProtein.create(
        protein, 'light', protein.num_uni_peptides,
        protein.num_peptides, area, ifot, ibaq)
    light_proteins.append(tmp_protein)
gardener.models.labelledProtein.objects.bulk_create(light_proteins)


genes = gardener.models.Exp_Gene.objects.filter(search__exp__name=exp)
heavy_genes = []
for gene in genes:
    area = 0
    ibaq = 0
    ifot = 0
    for heavy_protein in heavy_proteins:
        if heavy_protein.accession in gene.protein_gi:
            area = area + heavy_protein.area
            ibaq = ibaq + heavy_protein.ibaq
    ifot = ibaq / total_ibaq_heavy*1e6
    tmp_gene = gardener.models.labelledGene.create(
        gene, 'heavy', gene.num_uni_peptides,
        gene.num_peptides, area, ifot, ibaq)
    heavy_genes.append(tmp_gene)
gardener.models.labelledGene.objects.bulk_create(heavy_genes)

light_genes = []
for gene in genes:
    area = 0
    ibaq = 0
    ifot = 0
    for light_protein in light_proteins:
        if light_protein.accession in gene.protein_gi:
            area = area + light_protein.area
            ibaq = ibaq + light_protein.ibaq
    ifot = ibaq / total_ibaq_light*1e6
    tmp_gene = gardener.models.labelledGene.create(
        gene, 'light', gene.num_uni_peptides,
        gene.num_peptides, area, ifot, ibaq)
    light_genes.append(tmp_gene)
gardener.models.labelledGene.objects.bulk_create(light_genes)
