from django.db import models

# Create your models here.


class Experiment(models.Model):
    name = models.CharField(max_length=90, db_index=True)
    type = models.CharField(max_length=90, db_index=True)
    bait = models.CharField(max_length=90, db_index=True)
    description = models.CharField(max_length=9000)
    species = models.CharField(max_length=50, db_index=True)
    cell_type = models.CharField(max_length=50, db_index=True, blank=True)
    tissue = models.CharField(max_length=50, db_index=True, blank=True)
    organ = models.CharField(max_length=50, db_index=True, blank=True)
    fluid = models.CharField(max_length=50, db_index=True, blank=True)
    num_fraction = models.IntegerField(db_index=True)
    num_repeat = models.IntegerField(db_index=True)
    num_spectrum = models.IntegerField(db_index=True)
    num_peptide = models.IntegerField(db_index=True)
    num_isoform = models.IntegerField(db_index=True)
    num_gene = models.IntegerField(db_index=True)
    instrument = models.CharField(max_length=767, db_index=True)
    protocol = models.CharField(max_length=767, db_index=True)
    lab = models.CharField(max_length=90, db_index=True)
    operator = models.CharField(max_length=90, db_index=True)
    experiment_date = models.DateTimeField(
        null=True, blank=True, db_index=True)
    index_date = models.DateTimeField(null=True, blank=True, db_index=True)
    update_date = models.DateTimeField(null=True, blank=True)
    stage = models.IntegerField()
    started = models.IntegerField()
    taxid = models.CharField(max_length=255, null=True, blank=True)
    is_public = models.IntegerField()
    is_deleted = models.IntegerField()
    state = models.CharField(default='new', max_length=10)
    priority = models.IntegerField()
    file_source = models.CharField(max_length=50, db_index=True)

    def __unicode__(self):
        return self.name


class Search(models.Model):
    repeat_id = models.IntegerField(db_index=True)
    fraction_id = models.IntegerField(db_index=True)
    type = models.CharField(max_length=90, db_index=True)
    name = models.CharField(max_length=90, db_index=True)
    exp = models.ForeignKey(Experiment)
    rank = models.IntegerField(db_index=True)
    num_spectrum = models.IntegerField(db_index=True)
    num_peptide = models.IntegerField(db_index=True)
    num_isoform = models.IntegerField(db_index=True)
    num_gene = models.IntegerField(db_index=True)
    log = models.TextField(null=True, blank=True)
    create_time = models.DateTimeField(null=True, blank=True, db_index=True)
    update_time = models.DateTimeField(null=True, blank=True, db_index=True)
    user = models.CharField(max_length=100, db_index=True)
    stage = models.IntegerField(db_index=True)
    rt_max = models.FloatField(db_index=True)
    parameter = models.TextField()
    state = models.CharField(default='running', max_length=10)

    def __unicode__(self):
        return str(self.id)


class Protein(models.Model):
    search = models.ForeignKey(Search)
    accession = models.CharField(max_length=200, db_index=True)
    type = models.IntegerField()
    other_members = models.TextField(null=True, blank=True)
    symbol = models.CharField(max_length=200, db_index=True)
    description = models.TextField()
    score = models.FloatField(db_index=True)
    coverage = models.FloatField()
    num_proteins = models.IntegerField()
    num_uni_peptides = models.IntegerField()
    num_peptides = models.IntegerField()
    num_psms = models.IntegerField()
    area = models.FloatField(db_index=True)
    length = models.IntegerField()
    mw = models.FloatField()
    calc_pi = models.FloatField()
    fot = models.FloatField(db_index=True, null=True, blank=True)
    ibaq = models.FloatField(db_index=True, null=True, blank=True)

    def __unicode__(self):
        return self.accession


class Repeat_Protein(models.Model):
    search = models.ForeignKey(Search)
    accession = models.CharField(
        max_length=200, db_index=True, null=True, blank=True)
    type = models.IntegerField(null=True, blank=True)
    other_members = models.TextField(null=True, blank=True)
    symbol = models.CharField(
        max_length=200, db_index=True, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    score = models.FloatField(db_index=True, null=True, blank=True)
    coverage = models.FloatField(null=True, blank=True)
    num_proteins = models.IntegerField(null=True, blank=True)
    num_uni_peptides = models.IntegerField(null=True, blank=True)
    num_peptides = models.IntegerField(null=True, blank=True)
    num_psms = models.IntegerField(null=True, blank=True)
    area = models.FloatField(db_index=True, null=True, blank=True)
    length = models.IntegerField(null=True, blank=True)
    mw = models.FloatField(null=True, blank=True)
    calc_pi = models.FloatField(null=True, blank=True)
    fdr = models.FloatField(null=True, blank=True)
    fot = models.FloatField(db_index=True, null=True, blank=True)
    ibaq = models.FloatField(db_index=True, null=True, blank=True)
    annotation = models.CharField(
        db_index=True, max_length=100, null=True, blank=True)
    modification = models.CharField(
        db_index=True, max_length=200, null=True, blank=True)

    def __unicode__(self):
        return self.accession


class Exp_Protein(models.Model):
    search = models.ForeignKey(Search)
    accession = models.CharField(
        max_length=200, db_index=True, null=True, blank=True)
    type = models.IntegerField(null=True, blank=True)
    other_members = models.TextField(null=True, blank=True)
    symbol = models.CharField(
        max_length=200, db_index=True, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    score = models.FloatField(db_index=True, null=True, blank=True)
    coverage = models.FloatField(null=True, blank=True)
    num_proteins = models.IntegerField(null=True, blank=True)
    num_uni_peptides = models.IntegerField(null=True, blank=True)
    num_peptides = models.IntegerField(null=True, blank=True)
    num_psms = models.IntegerField(null=True, blank=True)
    area = models.FloatField(db_index=True, null=True, blank=True)
    length = models.IntegerField(null=True, blank=True)
    mw = models.FloatField(null=True, blank=True)
    calc_pi = models.FloatField(null=True, blank=True)
    fdr = models.FloatField(null=True, blank=True)
    fot = models.FloatField(db_index=True, null=True, blank=True)
    ibaq = models.FloatField(db_index=True, null=True, blank=True)
    annotation = models.CharField(
        db_index=True, max_length=100, null=True, blank=True)
    modification = models.CharField(
        db_index=True, max_length=200, null=True, blank=True)

    def __unicode__(self):
        return self.accession

class Exp_Protein_200(models.Model): 
    search = models.ForeignKey(Search)
    accession = models.CharField(
        max_length=200, db_index=True, null=True, blank=True)
    type = models.IntegerField(null=True, blank=True)
    other_members = models.TextField(null=True, blank=True)
    symbol = models.CharField(
        max_length=200, db_index=True, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    score = models.FloatField(db_index=True, null=True, blank=True)
    coverage = models.FloatField(null=True, blank=True)
    num_proteins = models.IntegerField(null=True, blank=True)
    num_uni_peptides = models.IntegerField(null=True, blank=True)
    num_peptides = models.IntegerField(null=True, blank=True)
    num_psms = models.IntegerField(null=True, blank=True)
    area = models.FloatField(db_index=True, null=True, blank=True)
    length = models.IntegerField(null=True, blank=True)
    mw = models.FloatField(null=True, blank=True)
    calc_pi = models.FloatField(null=True, blank=True)
    fdr = models.FloatField(null=True, blank=True)
    fot = models.FloatField(db_index=True, null=True, blank=True)
    ibaq = models.FloatField(db_index=True, null=True, blank=True)
    annotation = models.CharField(
        db_index=True, max_length=100, null=True, blank=True)
    modification = models.CharField(
        db_index=True, max_length=200, null=True, blank=True)

    def __unicode__(self):
        return self.accession

class Gene(models.Model):
    search = models.ForeignKey(Search)
    symbol = models.CharField(max_length=200, db_index=True)
    gene_id = models.IntegerField(db_index=True)
    protein_gi = models.TextField()
    num_proteins = models.IntegerField()
    num_identified_proteins = models.IntegerField()
    num_uni_proteins = models.IntegerField()
    num_peptides = models.IntegerField()
    num_uni_peptides = models.IntegerField()
    num_psms = models.IntegerField()
    area = models.FloatField(db_index=True)
    fdr = models.FloatField()
    description = models.TextField()
    type = models.IntegerField()
    score = models.FloatField(db_index=True)
    fot = models.FloatField(db_index=True, null=True, blank=True)
    ibaq = models.FloatField(db_index=True, null=True, blank=True)

    def __unicode__(self):
        return self.gene_id


class Repeat_Gene(models.Model):
    search = models.ForeignKey(Search)
    symbol = models.CharField(
        max_length=200, db_index=True, null=True, blank=True)
    gene_id = models.IntegerField(db_index=True, null=True, blank=True)
    protein_gi = models.TextField(null=True, blank=True)
    num_proteins = models.IntegerField(null=True, blank=True)
    num_identified_proteins = models.IntegerField(null=True, blank=True)
    num_uni_proteins = models.IntegerField(null=True, blank=True)
    num_peptides = models.IntegerField(null=True, blank=True)
    num_uni_peptides = models.IntegerField(null=True, blank=True)
    num_psms = models.IntegerField()
    area = models.FloatField(db_index=True, null=True, blank=True)
    fdr = models.FloatField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    type = models.IntegerField(null=True, blank=True)
    score = models.FloatField(db_index=True, null=True, blank=True)
    fot = models.FloatField(db_index=True, null=True, blank=True)
    ibaq = models.FloatField(db_index=True, null=True, blank=True)
    annotation = models.CharField(
        db_index=True, max_length=100, null=True, blank=True)
    modification = models.CharField(
        db_index=True, max_length=200, null=True, blank=True)

    def __unicode__(self):
        return self.gene_id


class Exp_Gene(models.Model):
    search = models.ForeignKey(Search)
    symbol = models.CharField(
        max_length=200, null=True, blank=True, db_index=True)
    gene_id = models.IntegerField(db_index=True, null=True, blank=True)
    protein_gi = models.TextField(null=True, blank=True)
    num_proteins = models.IntegerField(null=True, blank=True)
    num_identified_proteins = models.IntegerField(null=True, blank=True)
    num_uni_proteins = models.IntegerField(null=True, blank=True)
    num_peptides = models.IntegerField(null=True, blank=True)
    num_uni_peptides = models.IntegerField(null=True, blank=True)
    num_psms = models.IntegerField()
    area = models.FloatField(db_index=True, null=True, blank=True)
    fdr = models.FloatField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    type = models.IntegerField(null=True, blank=True)
    score = models.FloatField(db_index=True, null=True, blank=True)
    fot = models.FloatField(
        db_index=True, null=True, blank=True)
    ibaq = models.FloatField(
        db_index=True, null=True, blank=True)
    annotation = models.CharField(
        db_index=True, max_length=100, null=True, blank=True)
    modification = models.CharField(
        db_index=True, max_length=200, null=True, blank=True)

    def __unicode__(self):
        return self.gene_id


class MS1(models.Model):
    search = models.ForeignKey(Search)
    # f_num = models.IntegerField(db_index=True)
    # r_num = models.IntegerField(db_index=True)
    scan_num = models.IntegerField(db_index=True)
    # scan_num_ms2 = models.IntegerField(db_index=True)
    rt = models.FloatField(db_index=True)
    intensity = models.FloatField(db_index=True)
    # file_name = models.CharField(max_length=200, blank=True)
    # file_name = models.CharField(max_length=200, blank=True)


class MS2(models.Model):
    ms1 = models.ForeignKey(MS1)
    search = models.ForeignKey(Search)
    # charge = models.IntegerField(db_index=True)
    # exp = models.ForeignKey(Experiment)
    # f_num = models.IntegerField(db_index=True)
    # r_num = models.IntegerField(db_index=True)
    # search = models.ForeignKey(Search)
    scan_num = models.IntegerField(db_index=True)
    # mz = models.FloatField(db_index=True)
    pre_mz = models.FloatField(db_index=True)
    rt = models.FloatField(db_index=True)
    # peptide = models.CharField(max_length=200, blank=True,db_index=True)
    # intensity = models.FloatField(db_index=True)
    # ionscore = models.FloatField(db_index=True)
    # file_name = models.CharField(max_length=200, blank=True)


class Peptide(models.Model):
    ms2_id = models.IntegerField(db_index=True, null=True, blank=True)
    # ms2 = models.ForeignKey(MS2)
    search = models.ForeignKey(Search)
    # protein = models.ForeignKey(Protein)
    quality = models.CharField(max_length=200)
    sequence = models.CharField(max_length=500, db_index=True)
    type = models.IntegerField()
    num_psms = models.IntegerField()
    num_proteins = models.IntegerField()
    num_protein_groups = models.IntegerField()
    protein_group_accessions = models.TextField()
    modification = models.CharField(max_length=767, db_index=True)
    delta_cn = models.FloatField()
    area = models.FloatField(db_index=True)
    q_value = models.FloatField(db_index=True)
    pep = models.FloatField()
    ion_score = models.FloatField(db_index=True)
    exp_value = models.FloatField()
    charge = models.IntegerField()
    mh_da = models.FloatField(db_index=True)
    delta_m_ppm = models.FloatField()
    rt_min = models.FloatField(db_index=True)
    num_missed_cleavages = models.IntegerField()
    from_where = models.CharField(max_length=200)
    fdr = models.FloatField(null=True, blank=True)
    fot = models.FloatField(db_index=True, null=True, blank=True)
    # protein_group_accession = models.CharField(max_length=200, blank=True)

    def __unicode__(self):
        return str(self.id) + self.sequence


class Repeat_Peptide(models.Model):
    ms2_id = models.IntegerField(db_index=True, null=True, blank=True)
    search = models.ForeignKey(Search)
    # protein = models.ForeignKey(Protein)
    quality = models.CharField(
        max_length=200, null=True, blank=True)
    sequence = models.CharField(
        max_length=500, db_index=True, null=True, blank=True)
    type = models.IntegerField(null=True, blank=True)
    num_psms = models.IntegerField(null=True, blank=True)
    num_proteins = models.IntegerField(null=True, blank=True)
    num_protein_groups = models.IntegerField(null=True, blank=True)
    protein_group_accessions = models.TextField(null=True, blank=True)
    modification = models.CharField(
        max_length=767, db_index=True, null=True, blank=True)
    delta_cn = models.FloatField(null=True, blank=True)
    area = models.FloatField(db_index=True, null=True, blank=True)
    q_value = models.FloatField(db_index=True, null=True, blank=True)
    pep = models.FloatField(null=True, blank=True)
    ion_score = models.FloatField(db_index=True, null=True, blank=True)
    exp_value = models.FloatField(null=True, blank=True)
    charge = models.IntegerField(null=True, blank=True)
    mh_da = models.FloatField(db_index=True, null=True, blank=True)
    delta_m_ppm = models.FloatField(null=True, blank=True)
    rt_min = models.FloatField(db_index=True, null=True, blank=True)
    num_missed_cleavages = models.IntegerField(null=True, blank=True)
    fdr = models.FloatField(null=True, blank=True)
    from_where = models.CharField(max_length=200)
    fot = models.FloatField(db_index=True, null=True, blank=True)
    # protein_group_accession = models.CharField(max_length=200, blank=True)

    def __unicode__(self):
        return str(self.id) + self.sequence


class Exp_Peptide(models.Model):
    ms2_id = models.IntegerField(db_index=True, null=True, blank=True)
    search = models.ForeignKey(Search)
    # protein = models.ForeignKey(Protein)
    quality = models.CharField(max_length=200, null=True, blank=True)
    sequence = models.CharField(
        max_length=500, db_index=True, null=True, blank=True)
    type = models.IntegerField(null=True, blank=True)
    num_psms = models.IntegerField(null=True, blank=True)
    num_proteins = models.IntegerField(null=True, blank=True)
    num_protein_groups = models.IntegerField(null=True, blank=True)
    protein_group_accessions = models.TextField(null=True, blank=True)
    modification = models.CharField(
        max_length=767, db_index=True, null=True, blank=True)
    delta_cn = models.FloatField(null=True, blank=True)
    area = models.FloatField(db_index=True, null=True, blank=True)
    q_value = models.FloatField(db_index=True, null=True, blank=True)
    pep = models.FloatField(null=True, blank=True)
    ion_score = models.FloatField(db_index=True, null=True, blank=True)
    exp_value = models.FloatField(null=True, blank=True)
    charge = models.IntegerField(null=True, blank=True)
    mh_da = models.FloatField(db_index=True, null=True, blank=True)
    delta_m_ppm = models.FloatField(null=True, blank=True)
    rt_min = models.FloatField(db_index=True, null=True, blank=True)
    num_missed_cleavages = models.IntegerField(null=True, blank=True)
    fdr = models.FloatField(null=True, blank=True)
    from_where = models.CharField(max_length=200)
    fot = models.FloatField(db_index=True, null=True, blank=True)
    # protein_group_accession = models.CharField(max_length=200, blank=True)

    def __unicode__(self):
        return str(self.id) + self.sequence

class Exp_Peptide_200(models.Model):
    ms2_id = models.IntegerField(db_index=True, null=True, blank=True)
    search = models.ForeignKey(Search)
    # protein = models.ForeignKey(Protein)
    quality = models.CharField(max_length=200, null=True, blank=True)
    sequence = models.CharField(
        max_length=500, db_index=True, null=True, blank=True)
    type = models.IntegerField(null=True, blank=True)
    num_psms = models.IntegerField(null=True, blank=True)
    num_proteins = models.IntegerField(null=True, blank=True)
    num_protein_groups = models.IntegerField(null=True, blank=True)
    protein_group_accessions = models.TextField(null=True, blank=True)
    modification = models.CharField(
        max_length=767, db_index=True, null=True, blank=True)
    delta_cn = models.FloatField(null=True, blank=True)
    area = models.FloatField(db_index=True, null=True, blank=True)
    q_value = models.FloatField(db_index=True, null=True, blank=True)
    pep = models.FloatField(null=True, blank=True)
    ion_score = models.FloatField(db_index=True, null=True, blank=True)
    exp_value = models.FloatField(null=True, blank=True)
    charge = models.IntegerField(null=True, blank=True)
    mh_da = models.FloatField(db_index=True, null=True, blank=True)
    delta_m_ppm = models.FloatField(null=True, blank=True)
    rt_min = models.FloatField(db_index=True, null=True, blank=True)
    num_missed_cleavages = models.IntegerField(null=True, blank=True)
    fdr = models.FloatField(null=True, blank=True)
    from_where = models.CharField(max_length=200)
    fot = models.FloatField(db_index=True, null=True, blank=True)
    # protein_group_accession = models.CharField(max_length=200, blank=True)

    def __unicode__(self):
        return str(self.id) + self.sequence

class GeneInfo(models.Model):
    tax_id = models.CharField(max_length=20)
    gene_id = models.CharField(max_length=20, blank=True)
    symbol = models.CharField(max_length=200, blank=True)
    locustag = models.CharField(max_length=200, blank=True)
    synonyms = models.CharField(max_length=900, blank=True)
    dbxrefs = models.CharField(max_length=900, blank=True)
    chromosome = models.CharField(max_length=50, blank=True)
    maplocation = models.CharField(max_length=50, blank=True)
    description = models.TextField()
    type = models.CharField(max_length=100, blank=True)
    symbolfromauth = models.CharField(max_length=900, blank=True)
    fullname = models.CharField(max_length=900, blank=True)
    status = models.CharField(max_length=200, blank=True)
    others = models.TextField()
    moddate = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return self.symbol


class File(models.Model):
    name = models.CharField(max_length=200, blank=True)
    exp = models.ForeignKey(Experiment)
    rank = models.IntegerField(db_index=True)
    type = models.CharField(max_length=200, blank=True)
    file_type = models.CharField(max_length=200, blank=True)
    jobid = models.CharField(max_length=50, blank=True)
    size = models.CharField(max_length=200, blank=True)
    path = models.CharField(max_length=200, blank=True)
    date = models.DateTimeField(null=True, blank=True, db_index=True)

    def __unicode__(self):
        return self.name


class Fasta_File(models.Model):
    name = models.CharField(
        max_length=200, db_index=True, null=True, blank=True)
    create_time = models.DateTimeField(null=True, blank=True, db_index=True)
    update_time = models.DateTimeField(null=True, blank=True, db_index=True)
    user = models.CharField(
        max_length=200, db_index=True, null=True, blank=True)


class BioannotationType(models.Model):
    name = models.CharField(max_length=40, blank=True)
    species = models.CharField(
        db_index=True, max_length=40, null=True, blank=True)


class Annotation(models.Model):
    symbol = models.CharField(
        max_length=200, db_index=True, null=True, blank=True)
    annotation_id = models.ForeignKey(BioannotationType)
    species = models.CharField(
        max_length=100, db_index=True, null=True, blank=True)


class Fasta_Data(models.Model):
    fasta_file = models.ForeignKey(Fasta_File)
    protein_gi = models.CharField(
        max_length=200, db_index=True, null=True, blank=True)
    length = models.IntegerField(db_index=True, null=True, blank=True)
    sequence = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    symbol = models.CharField(
        max_length=200, db_index=True, null=True, blank=True)
    accession = models.CharField(
        max_length=255, db_index=True, null=True, blank=True)
    acc_type = models.CharField(
        max_length=255, db_index=True, null=True, blank=True)
    prefix = models.CharField(
        max_length=255, db_index=True, null=True, blank=True)
    ibaq_num = models.IntegerField(
        db_index=True, null=True, blank=True)
    annotation_id = models.CharField(
        max_length=20, null=True, blank=True)


class Gene_Location(models.Model):
    chr = models.CharField(
        max_length=200, db_index=True, null=True, blank=True)
    start = models.IntegerField(db_index=True, null=True, blank=True)
    end = models.IntegerField(db_index=True, null=True, blank=True)
    symbol = models.CharField(
        max_length=200, db_index=True, null=True, blank=True)


# class Fraction(models.Model):
# class Search(models.Model):

"""
class MS1data(models.Model):
    ms1 = models.ForeignKey(MS1)
    file_name = models.CharField(max_length=500, blank=True)

class MS1_MS2(models.Model):
    file_name = models.CharField(max_length=200, blank=True)
    #search_id = models.IntegerField(db_index=True)
    ms1 = models.IntegerField(db_index=True)
    ms2 = models.IntegerField(db_index=True)
"""


class XsearchTable(models.Model):
    dmz = models.FloatField()
    drt = models.FloatField()
    ionscore = models.FloatField()
    searchs = models.TextField(db_index=True)
    compare = models.BooleanField(default=False, db_index=True)
    qc = models.BooleanField(default=False, db_index=True)
    done = models.BooleanField(default=False, db_index=True)
    ProGene = models.CharField(max_length=200, db_index=True, blank=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    user = models.CharField(max_length=100, db_index=True)
    status = models.CharField(max_length=10, db_index=True)
    exp_name = models.TextField(null=True, blank=True)
    exp_num = models.IntegerField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return self.id


class UploadFile(models.Model):
    fileName = models.CharField(max_length=200, blank=True, db_index=True)
    upLoadID = models.IntegerField(null=True, blank=True)

    def __unicode__(self):
        return self.fileName


class Share_Exp(models.Model):
    exp = models.ForeignKey(Experiment)
    lab = models.CharField(max_length=90, db_index=True)

    def __unicode__(self):
        return self.id


class user_defined(models.Model):
    user = models.CharField(max_length=90, db_index=True)
    species = models.CharField(max_length=50, db_index=True)
    symbol = models.CharField(max_length=250, db_index=True)
    annotation = models.TextField()

    def __unicode__(self):
        return self.symbol + '(' + self.species + ')' + '\t' + self.annotation


class Kinase_SubStrate(models.Model):
    kinase = models.CharField(max_length=50, db_index=True, blank=True)
    kin_acc_id = models.CharField(max_length=50, db_index=True, blank=True)
    kin_gene_symbol = models.CharField(
        max_length=50, db_index=True, blank=True)
    chr_loc_hum = models.CharField(max_length=50, db_index=True, blank=True)
    kin_org = models.CharField(max_length=50, db_index=True, blank=True)
    substrate = models.CharField(max_length=50, db_index=True, blank=True)
    sub_gene_id = models.CharField(max_length=50, db_index=True, blank=True)
    sub_acc_id = models.CharField(max_length=50, db_index=True, blank=True)
    sub_gene_symbol = models.CharField(
        max_length=50, db_index=True, blank=True)
    sub_org = models.CharField(
        max_length=50, db_index=True, blank=True)
    sub_chr_loc_hum = models.CharField(
        max_length=50, db_index=True, blank=True)
    sub_mod_rsd = models.CharField(max_length=50, db_index=True, blank=True)
    site_grp_id = models.CharField(max_length=50, db_index=True, blank=True)
    modsite_seq = models.CharField(max_length=50, db_index=True, blank=True)
    in_vivo_rxn = models.CharField(max_length=50, db_index=True, blank=True)
    in_vitro_rxn = models.CharField(max_length=50, db_index=True, blank=True)
    cst_cat = models.CharField(max_length=100, db_index=True, blank=True)

    def __unicode__(self):
        return self.id


class gene2accession(models.Model):
    protein_gi = models.CharField(max_length=100, db_index=True, blank=True)
    mrna_accession = models.CharField(
        max_length=100, db_index=True, blank=True)


class Best_Responders_WCE(models.Model):
    peptide_sequence = models.CharField(max_length=500, db_index=True)
    protein_gi = models.CharField(
        max_length=200, db_index=True, null=True, blank=True)
    ref_score = models.FloatField(db_index=True, null=True, blank=True)
    flag = models.CharField(max_length=90, db_index=True)

    def __unicode__(self):
        return str(self.id)


class Best_Responders_TFRE(models.Model):
    peptide_sequence = models.CharField(max_length=500, db_index=True)
    protein_gi = models.CharField(
        max_length=200, db_index=True, null=True, blank=True)
    ref_score = models.FloatField(db_index=True, null=True, blank=True)
    flag = models.CharField(max_length=90, db_index=True)

    def __unicode__(self):
        return str(self.id)
# class protein_BR(models.Model):
#     protein_id = models.ForeignKey(Protein.id)
#     br_score = models.FloatField(db_index=True, null=True, blank=True)


class ProteinLocation(models.Model):
    accession = models.CharField(max_length=200, db_index=True)
    match = models.IntegerField()
    mismatch = models.IntegerField()
    repmatch = models.IntegerField()
    ns = models.IntegerField()
    qGapCount = models.IntegerField()
    qGapBases = models.IntegerField()
    tGapCount = models.IntegerField()
    tGapBases = models.IntegerField()
    strand = models.CharField(max_length=2)
    qName = models.CharField(max_length=200)
    qSize = models.IntegerField()
    qStart = models.IntegerField()
    qEnd = models.IntegerField()
    tName = models.CharField(max_length=200)
    tSize = models.IntegerField()
    tStart = models.IntegerField()
    tEnd = models.IntegerField()
    blockEnd = models.IntegerField()
    blockSize = models.CharField(max_length=2000)
    qStarts = models.CharField(max_length=2000)
    tStarts = models.CharField(max_length=2000)

    def __unicode__(self):
        return self.accession

    @classmethod
    def create(cls, content):
        book = cls(accession=content[0],
                   match=content[1],
                   mismatch=content[2],
                   repmatch=content[3],
                   ns=content[4],
                   qGapCount=content[5],
                   qGapBases=content[6],
                   tGapCount=content[7],
                   tGapBases=content[8],
                   strand=content[9],
                   qName=content[10],
                   qSize=content[11],
                   qStart=content[12],
                   qEnd=content[13],
                   tName=content[14],
                   tSize=content[15],
                   tStart=content[16],
                   tEnd=content[17],
                   blockEnd=content[18],
                   blockSize=content[19],
                   qStarts=content[20],
                   tStarts=content[21]
                   )
        # do something with the book
        return book

    def returnLine(self):
        book = [self.match,
                self.mismatch,
                self.repmatch,
                self.ns,
                self.qGapCount,
                self.qGapBases,
                self.tGapCount,
                self.tGapBases,
                self.strand,
                self.qName,
                self.qSize,
                self.qStart,
                self.qEnd,
                self.tName,
                self.tSize,
                self.tStart,
                self.tEnd,
                self.blockEnd,
                self.blockSize,
                self.qStarts,
                self.tStarts]
        return book


class labelledPeptide(models.Model):
    ms2_id = models.IntegerField(db_index=True, null=True, blank=True)
    search = models.ForeignKey(Search)
    # protein = models.ForeignKey(Protein)
    quality = models.CharField(max_length=200, null=True, blank=True)
    sequence = models.CharField(
        max_length=500, db_index=True, null=True, blank=True)
    type = models.IntegerField(null=True, blank=True)
    num_psms = models.IntegerField(null=True, blank=True)
    num_proteins = models.IntegerField(null=True, blank=True)
    num_protein_groups = models.IntegerField(null=True, blank=True)
    protein_group_accessions = models.TextField(null=True, blank=True)
    modification = models.CharField(
        max_length=767, db_index=True, null=True, blank=True)
    delta_cn = models.FloatField(null=True, blank=True)
    area = models.FloatField(db_index=True, null=True, blank=True)
    q_value = models.FloatField(db_index=True, null=True, blank=True)
    pep = models.FloatField(null=True, blank=True)
    ion_score = models.FloatField(db_index=True, null=True, blank=True)
    exp_value = models.FloatField(null=True, blank=True)
    charge = models.IntegerField(null=True, blank=True)
    mh_da = models.FloatField(db_index=True, null=True, blank=True)
    delta_m_ppm = models.FloatField(null=True, blank=True)
    rt_min = models.FloatField(db_index=True, null=True, blank=True)
    num_missed_cleavages = models.IntegerField(null=True, blank=True)
    fdr = models.FloatField(null=True, blank=True)
    from_where = models.CharField(max_length=200)
    fot = models.FloatField(db_index=True, null=True, blank=True)
    labels = models.CharField(
        db_index=True, max_length=200, null=True, blank=True)

    # protein_group_accession = models.CharField(max_length=200, blank=True)
    def __unicode__(self):
        return str(self.id) + self.sequence

    @classmethod
    def create(cls, light_peptide, label):
        peptide = cls(
            ms2_id=light_peptide.ms2_id,
            search=light_peptide.search,
            quality=light_peptide.quality,
            sequence=light_peptide.sequence,
            type=light_peptide.type,
            num_psms=light_peptide.num_psms,
            num_proteins=light_peptide.num_proteins,
            num_protein_groups=light_peptide.num_protein_groups,
            protein_group_accessions=light_peptide.protein_group_accessions,
            modification=light_peptide.modification,
            delta_cn=light_peptide.delta_cn,
            area=light_peptide.area,
            q_value=light_peptide.q_value,
            pep=light_peptide.pep,
            ion_score=light_peptide.ion_score,
            exp_value=light_peptide.exp_value,
            charge=light_peptide.charge,
            mh_da=light_peptide.mh_da,
            delta_m_ppm=light_peptide.delta_m_ppm,
            rt_min=light_peptide.rt_min,
            num_missed_cleavages=light_peptide.num_missed_cleavages,
            fdr=light_peptide.fdr,
            from_where=light_peptide.from_where,
            fot=light_peptide.fot,
            labels=label)
        return peptide


class labelledProtein(models.Model):
    search = models.ForeignKey(Search)
    accession = models.CharField(
        max_length=200, db_index=True, null=True, blank=True)
    type = models.IntegerField(null=True, blank=True)
    other_members = models.TextField(null=True, blank=True)
    symbol = models.CharField(
        max_length=200, db_index=True, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    score = models.FloatField(db_index=True, null=True, blank=True)
    coverage = models.FloatField(null=True, blank=True)
    num_proteins = models.IntegerField(null=True, blank=True)
    num_uni_peptides = models.IntegerField(null=True, blank=True)
    num_peptides = models.IntegerField(null=True, blank=True)
    num_psms = models.IntegerField(null=True, blank=True)
    area = models.FloatField(db_index=True, null=True, blank=True)
    length = models.IntegerField(null=True, blank=True)
    mw = models.FloatField(null=True, blank=True)
    calc_pi = models.FloatField(null=True, blank=True)
    fdr = models.FloatField(null=True, blank=True)
    fot = models.FloatField(db_index=True, null=True, blank=True)
    ibaq = models.FloatField(db_index=True, null=True, blank=True)
    annotation = models.CharField(
        db_index=True, max_length=100, null=True, blank=True)
    modification = models.CharField(
        db_index=True, max_length=200, null=True, blank=True)
    labels = models.CharField(
        db_index=True, max_length=200, null=True, blank=True)

    def __unicode__(self):
        return self.accession

    @classmethod
    def create(cls, light_proteins, label, num_uni_peptides,
               num_peptides, area, fot, ibaq):
        protein = cls(
            search=light_proteins.search,
            accession=light_proteins.accession,
            type=light_proteins.type,
            other_members=light_proteins.other_members,
            symbol=light_proteins.symbol,
            score=light_proteins.score,
            description=light_proteins.description,
            coverage=light_proteins.coverage,
            num_proteins=light_proteins.num_proteins,
            num_uni_peptides=num_uni_peptides,
            num_peptides=num_peptides,
            num_psms=light_proteins.num_psms,
            area=area,
            length=light_proteins.length,
            mw=light_proteins.mw,
            calc_pi=light_proteins.calc_pi,
            fdr=light_proteins.fdr,
            fot=fot,
            ibaq=ibaq,
            annotation=light_proteins.annotation,
            modification=light_proteins.modification,
            labels=label)
        return protein


class labelledGene(models.Model):
    search = models.ForeignKey(Search)
    symbol = models.CharField(
        max_length=200, db_index=True, null=True, blank=True)
    gene_id = models.IntegerField(db_index=True, null=True, blank=True)
    protein_gi = models.TextField(null=True, blank=True)
    num_proteins = models.IntegerField(null=True, blank=True)
    num_identified_proteins = models.IntegerField(null=True, blank=True)
    num_uni_proteins = models.IntegerField(null=True, blank=True)
    num_peptides = models.IntegerField(null=True, blank=True)
    num_uni_peptides = models.IntegerField(null=True, blank=True)
    num_psms = models.IntegerField()
    area = models.FloatField(db_index=True, null=True, blank=True)
    fdr = models.FloatField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    type = models.IntegerField(null=True, blank=True)
    score = models.FloatField(db_index=True, null=True, blank=True)
    fot = models.FloatField(db_index=True, null=True, blank=True)
    ibaq = models.FloatField(db_index=True, null=True, blank=True)
    annotation = models.CharField(
        db_index=True, max_length=100, null=True, blank=True)
    modification = models.CharField(
        db_index=True, max_length=200, null=True, blank=True)
    labels = models.CharField(
        db_index=True, max_length=200, null=True, blank=True)

    def __unicode__(self):
        return self.gene_id

    @classmethod
    def create(cls, light_genes, label, num_uni_peptides,
               num_peptides, area, fot, ibaq):
        gene = cls(
            search=light_genes.search,
            symbol=light_genes.symbol,
            gene_id=light_genes.gene_id,
            protein_gi=light_genes.protein_gi,
            num_proteins=light_genes.num_proteins,
            num_identified_proteins=light_genes.num_identified_proteins,
            num_uni_proteins=light_genes.num_uni_proteins,
            num_peptides=num_peptides,
            num_uni_peptides=num_uni_peptides,
            num_psms=light_genes.num_psms,
            area=area,
            fdr=light_genes.fdr,
            description=light_genes.description,
            type=light_genes.type,
            score=light_genes.score,
            fot=fot,
            ibaq=ibaq,
            annotation=light_genes.annotation,
            modification=light_genes.modification,
            labels=label)
        return gene
