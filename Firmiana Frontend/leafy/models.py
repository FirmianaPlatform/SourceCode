# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models

class ApiKeys(models.Model):
    id = models.IntegerField(primary_key=True)
    create_time = models.DateTimeField(null=True, blank=True)
    user_id = models.IntegerField(null=True, blank=True)
    key = models.CharField(max_length=96, unique=True, blank=True)
    class Meta:
        db_table = u'api_keys'

class AuthGroup(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=240, unique=True)
    class Meta:
        db_table = u'auth_group'

class AuthPermission(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=150)
    content_type = models.ForeignKey('DjangoContentType', unique=True)
    codename = models.CharField(max_length=300, unique=True)
    class Meta:
        db_table = u'auth_permission'
        
class AuthGroupPermissions(models.Model):
    id = models.IntegerField(primary_key=True)
    group = models.ForeignKey(AuthGroup, unique=True)
    permission = models.ForeignKey(AuthPermission)
    class Meta:
        db_table = u'auth_group_permissions'

class AuthUser(models.Model):
    id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=90, unique=True)
    first_name = models.CharField(max_length=90)
    last_name = models.CharField(max_length=90)
    email = models.CharField(max_length=225)
    password = models.CharField(max_length=384)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    is_superuser = models.IntegerField()
    last_login = models.DateTimeField()
    date_joined = models.DateTimeField()
    class Meta:
        db_table = u'auth_user'

class AuthUserGroups(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(AuthUser, unique=True)
    group = models.ForeignKey(AuthGroup)
    class Meta:
        db_table = u'auth_user_groups'

class AuthUserUserPermissions(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(AuthUser, unique=True)
    permission = models.ForeignKey(AuthPermission)
    class Meta:
        db_table = u'auth_user_user_permissions'

class CleanupEvent(models.Model):
    id = models.IntegerField(primary_key=True)
    create_time = models.DateTimeField(null=True, blank=True)
    message = models.CharField(max_length=3072, blank=True)
    class Meta:
        db_table = u'cleanup_event'

class CleanupEventDatasetAssociation(models.Model):
    id = models.IntegerField(primary_key=True)
    create_time = models.DateTimeField(null=True, blank=True)
    cleanup_event_id = models.IntegerField(null=True, blank=True)
    dataset_id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'cleanup_event_dataset_association'

class CleanupEventHdaAssociation(models.Model):
    id = models.IntegerField(primary_key=True)
    create_time = models.DateTimeField(null=True, blank=True)
    cleanup_event_id = models.IntegerField(null=True, blank=True)
    hda_id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'cleanup_event_hda_association'

class CleanupEventHistoryAssociation(models.Model):
    id = models.IntegerField(primary_key=True)
    create_time = models.DateTimeField(null=True, blank=True)
    cleanup_event_id = models.IntegerField(null=True, blank=True)
    history_id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'cleanup_event_history_association'

class CleanupEventIcdaAssociation(models.Model):
    id = models.IntegerField(primary_key=True)
    create_time = models.DateTimeField(null=True, blank=True)
    cleanup_event_id = models.IntegerField(null=True, blank=True)
    icda_id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'cleanup_event_icda_association'

class CleanupEventLddaAssociation(models.Model):
    id = models.IntegerField(primary_key=True)
    create_time = models.DateTimeField(null=True, blank=True)
    cleanup_event_id = models.IntegerField(null=True, blank=True)
    ldda_id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'cleanup_event_ldda_association'

class CleanupEventLibraryAssociation(models.Model):
    id = models.IntegerField(primary_key=True)
    create_time = models.DateTimeField(null=True, blank=True)
    cleanup_event_id = models.IntegerField(null=True, blank=True)
    library_id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'cleanup_event_library_association'

class CleanupEventLibraryDatasetAssociation(models.Model):
    id = models.IntegerField(primary_key=True)
    create_time = models.DateTimeField(null=True, blank=True)
    cleanup_event_id = models.IntegerField(null=True, blank=True)
    library_dataset_id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'cleanup_event_library_dataset_association'

class CleanupEventLibraryFolderAssociation(models.Model):
    id = models.IntegerField(primary_key=True)
    create_time = models.DateTimeField(null=True, blank=True)
    cleanup_event_id = models.IntegerField(null=True, blank=True)
    library_folder_id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'cleanup_event_library_folder_association'

class CleanupEventMetadataFileAssociation(models.Model):
    id = models.IntegerField(primary_key=True)
    create_time = models.DateTimeField(null=True, blank=True)
    cleanup_event_id = models.IntegerField(null=True, blank=True)
    metadata_file_id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'cleanup_event_metadata_file_association'

class DataManagerHistoryAssociation(models.Model):
    id = models.IntegerField(primary_key=True)
    create_time = models.DateTimeField(null=True, blank=True)
    update_time = models.DateTimeField(null=True, blank=True)
    history_id = models.IntegerField(null=True, blank=True)
    user_id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'data_manager_history_association'

class DataManagerJobAssociation(models.Model):
    id = models.IntegerField(primary_key=True)
    create_time = models.DateTimeField(null=True, blank=True)
    update_time = models.DateTimeField(null=True, blank=True)
    job_id = models.IntegerField(null=True, blank=True)
    data_manager_id = models.TextField(blank=True)
    class Meta:
        db_table = u'data_manager_job_association'

class Dataset(models.Model):
    id = models.IntegerField(primary_key=True)
    create_time = models.DateTimeField(null=True, blank=True)
    update_time = models.DateTimeField(null=True, blank=True)
    state = models.CharField(max_length=192, blank=True)
    deleted = models.IntegerField(null=True, blank=True)
    purged = models.IntegerField(null=True, blank=True)
    purgable = models.IntegerField(null=True, blank=True)
    external_filename = models.TextField(blank=True)
    _extra_files_path = models.TextField(blank=True)
    file_size = models.DecimalField(null=True, max_digits=16, decimal_places=0, blank=True)
    total_size = models.DecimalField(null=True, max_digits=16, decimal_places=0, blank=True)
    object_store_id = models.CharField(max_length=765, blank=True)
    uuid = models.CharField(max_length=96, blank=True)
    class Meta:
        db_table = u'dataset'

class DatasetPermissions(models.Model):
    id = models.IntegerField(primary_key=True)
    create_time = models.DateTimeField(null=True, blank=True)
    update_time = models.DateTimeField(null=True, blank=True)
    action = models.TextField(blank=True)
    dataset_id = models.IntegerField(null=True, blank=True)
    role_id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'dataset_permissions'

class DatasetTagAssociation(models.Model):
    id = models.IntegerField(primary_key=True)
    dataset_id = models.IntegerField(null=True, blank=True)
    tag_id = models.IntegerField(null=True, blank=True)
    user_tname = models.CharField(max_length=765, blank=True)
    value = models.CharField(max_length=765, blank=True)
    user_value = models.CharField(max_length=765, blank=True)
    class Meta:
        db_table = u'dataset_tag_association'

class DefaultHistoryPermissions(models.Model):
    id = models.IntegerField(primary_key=True)
    history_id = models.IntegerField(null=True, blank=True)
    action = models.TextField(blank=True)
    role_id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'default_history_permissions'

class DefaultQuotaAssociation(models.Model):
    id = models.IntegerField(primary_key=True)
    create_time = models.DateTimeField(null=True, blank=True)
    update_time = models.DateTimeField(null=True, blank=True)
    type = models.CharField(max_length=96, unique=True, blank=True)
    quota_id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'default_quota_association'

class DefaultUserPermissions(models.Model):
    id = models.IntegerField(primary_key=True)
    user_id = models.IntegerField(null=True, blank=True)
    action = models.TextField(blank=True)
    role_id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'default_user_permissions'

class DeferredJob(models.Model):
    id = models.IntegerField(primary_key=True)
    create_time = models.DateTimeField(null=True, blank=True)
    update_time = models.DateTimeField(null=True, blank=True)
    state = models.CharField(max_length=192, blank=True)
    plugin = models.CharField(max_length=384, blank=True)
    params = models.TextField(blank=True)
    class Meta:
        db_table = u'deferred_job'

class DjangoContentType(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=300)
    app_label = models.CharField(max_length=300, unique=True)
    model = models.CharField(max_length=300, unique=True)
    class Meta:
        db_table = u'django_content_type'
        
class DjangoAdminLog(models.Model):
    id = models.IntegerField(primary_key=True)
    action_time = models.DateTimeField()
    user = models.ForeignKey(AuthUser)
    content_type = models.ForeignKey(DjangoContentType, null=True, blank=True)
    object_id = models.TextField(blank=True)
    object_repr = models.CharField(max_length=600)
    action_flag = models.IntegerField()
    change_message = models.TextField()
    class Meta:
        db_table = u'django_admin_log'



class DjangoSession(models.Model):
    session_key = models.CharField(max_length=120, primary_key=True)
    session_data = models.TextField()
    expire_date = models.DateTimeField()
    class Meta:
        db_table = u'django_session'

class DjangoSite(models.Model):
    id = models.IntegerField(primary_key=True)
    domain = models.CharField(max_length=300)
    name = models.CharField(max_length=150)
    class Meta:
        db_table = u'django_site'

class Event(models.Model):
    id = models.IntegerField(primary_key=True)
    create_time = models.DateTimeField(null=True, blank=True)
    update_time = models.DateTimeField(null=True, blank=True)
    history_id = models.IntegerField(null=True, blank=True)
    user_id = models.IntegerField(null=True, blank=True)
    message = models.CharField(max_length=3072, blank=True)
    session_id = models.IntegerField(null=True, blank=True)
    tool_id = models.CharField(max_length=765, blank=True)
    class Meta:
        db_table = u'event'



class ExtendedMetadata(models.Model):
    id = models.IntegerField(primary_key=True)
    data = models.TextField(blank=True)
    class Meta:
        db_table = u'extended_metadata'

class ExtendedMetadataIndex(models.Model):
    id = models.IntegerField(primary_key=True)
    extended_metadata_id = models.IntegerField(null=True, blank=True)
    path = models.CharField(max_length=765, blank=True)
    value = models.TextField(blank=True)
    class Meta:
        db_table = u'extended_metadata_index'

class ExternalService(models.Model):
    id = models.IntegerField(primary_key=True)
    create_time = models.DateTimeField(null=True, blank=True)
    update_time = models.DateTimeField(null=True, blank=True)
    name = models.CharField(max_length=765)
    description = models.TextField(blank=True)
    version = models.CharField(max_length=765, blank=True)
    form_definition_id = models.IntegerField(null=True, blank=True)
    form_values_id = models.IntegerField(null=True, blank=True)
    deleted = models.IntegerField(null=True, blank=True)
    external_service_type_id = models.CharField(max_length=765, blank=True)
    class Meta:
        db_table = u'external_service'
"""
class FirmianaComparison(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=600, blank=True)
    description = models.CharField(max_length=6000, blank=True)
    quanttype = models.CharField(max_length=600, db_column='quantType', blank=True) # Field name made lowercase.
    filepath = models.CharField(max_length=600, blank=True)
    class Meta:
        db_table = u'firmiana_Comparison'

class FirmianaComparisonExperiment(models.Model):
    comparisonid = models.ForeignKey(FirmianaComparison, primary_key=True, db_column='comparisonID') # Field name made lowercase.
    experimentid = models.ForeignKey('FirmianaExperiment', db_column='experimentID') # Field name made lowercase.
    class Meta:
        db_table = u'firmiana_Comparison_Experiment'

class FirmianaConvertedrawfile(models.Model):
    id = models.IntegerField(primary_key=True)
    rawfileid = models.ForeignKey('FirmianaMsrunrawfile', null=True, db_column='rawfileID', blank=True) # Field name made lowercase.
    filetype = models.CharField(max_length=150, db_column='fileType') # Field name made lowercase.
    filepath = models.CharField(max_length=765)
    class Meta:
        db_table = u'firmiana_ConvertedRawfile'

class FirmianaDbsearchresult(models.Model):
    id = models.IntegerField(primary_key=True)
    convertedrawfileid = models.ForeignKey(FirmianaConvertedrawfile, null=True, db_column='convertedRawfileID', blank=True) # Field name made lowercase.
    searchtype = models.CharField(max_length=150, db_column='searchType') # Field name made lowercase.
    filepath = models.CharField(max_length=765)
    pepfilepath = models.CharField(max_length=765)
    class Meta:
        db_table = u'firmiana_DBSearchResult'

class FirmianaDbsearchresultQcresult(models.Model):
    dbsearchresultid = models.ForeignKey(FirmianaDbsearchresult, primary_key=True, db_column='dbsearchResultID') # Field name made lowercase.
    qcresultid = models.ForeignKey('FirmianaQcresult', db_column='qcResultID') # Field name made lowercase.
    class Meta:
        db_table = u'firmiana_DBSearchResult_QCResult'

class FirmianaExperiment(models.Model):
    id = models.IntegerField(primary_key=True)
    fractionnum = models.IntegerField(null=True, db_column='fractionNum', blank=True) # Field name made lowercase.
    replicatenum = models.IntegerField(null=True, db_column='replicateNum', blank=True) # Field name made lowercase.
    externalexperimentid = models.IntegerField(null=True, db_column='externalExperimentID', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'firmiana_Experiment'

class FirmianaFdrparam(models.Model):
    id = models.IntegerField(primary_key=True)
    qcresultid = models.ForeignKey('FirmianaQcresult', null=True, db_column='qcResultID', blank=True) # Field name made lowercase.
    error = models.FloatField(null=True, blank=True)
    minprob = models.FloatField(null=True, db_column='minProb', blank=True) # Field name made lowercase.
    numcorr = models.IntegerField(null=True, db_column='numCorr', blank=True) # Field name made lowercase.
    numincorr = models.IntegerField(null=True, db_column='numIncorr', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'firmiana_FDRParam'

class FirmianaMsrunrawfile(models.Model):
    id = models.IntegerField(primary_key=True)
    experimentid = models.ForeignKey(FirmianaExperiment, null=True, db_column='experimentID', blank=True) # Field name made lowercase.
    filepath = models.CharField(max_length=765)
    fractionno = models.IntegerField(null=True, db_column='fractionNo', blank=True) # Field name made lowercase.
    replicateno = models.IntegerField(null=True, db_column='replicateNo', blank=True) # Field name made lowercase.
    phvalue = models.FloatField(null=True, db_column='phValue', blank=True) # Field name made lowercase.
    volumn = models.FloatField(null=True, blank=True)
    filetype = models.CharField(max_length=150, db_column='fileType') # Field name made lowercase.
    class Meta:
        db_table = u'firmiana_MSRunRawfile'

class FirmianaMascotparam(models.Model):
    id = models.IntegerField(primary_key=True)
    dbsearchresultid = models.ForeignKey(FirmianaDbsearchresult, null=True, db_column='dbsearchResultID', blank=True) # Field name made lowercase.
    database = models.CharField(max_length=450)
    var_mods = models.CharField(max_length=765, blank=True)
    fix_mods = models.CharField(max_length=765, blank=True)
    enzyme = models.CharField(max_length=765, blank=True)
    precursor_tolu = models.CharField(max_length=30)
    missed_cleavages = models.IntegerField()
    fragment_ion_tol = models.FloatField(null=True, blank=True)
    allowed_charges = models.CharField(max_length=765, blank=True)
    instrument = models.CharField(max_length=450)
    precursor_search_type = models.CharField(max_length=450)
    class Meta:
        db_table = u'firmiana_MascotParam'

class FirmianaPeptidecomparisonvalueLabelfree(models.Model):
    id = models.IntegerField(primary_key=True)
    pepcomp_labelfreeid = models.ForeignKey('FirmianaPeptidecomparisonLabelfree', null=True, db_column='pepComp_LabelFreeID', blank=True) # Field name made lowercase.
    experimentid = models.ForeignKey(FirmianaExperiment, null=True, db_column='experimentID', blank=True) # Field name made lowercase.
    replicateno = models.IntegerField(null=True, db_column='replicateNo', blank=True) # Field name made lowercase.
    sc = models.IntegerField(null=True, blank=True)
    intensity = models.FloatField(null=True, blank=True)
    class Meta:
        db_table = u'firmiana_PeptideComparisonValue_LabelFree'

class FirmianaPeptidecomparisonLabelfree(models.Model):
    id = models.IntegerField(primary_key=True)
    comparisonid = models.ForeignKey(FirmianaComparison, null=True, db_column='comparisonID', blank=True) # Field name made lowercase.
    mass = models.FloatField(null=True, blank=True)
    charge = models.IntegerField(null=True, blank=True)
    sequence = models.CharField(max_length=600, blank=True)
    proteins = models.CharField(max_length=6000, blank=True)
    peptideid = models.IntegerField(null=True, db_column='peptideID', blank=True) # Field name made lowercase.
    filepath = models.CharField(max_length=600, blank=True)
    class Meta:
        db_table = u'firmiana_PeptideComparison_LabelFree'

class FirmianaGeneidmap(models.Model):
    id = models.IntegerField(primary_key=True)
    geneid = models.CharField(max_length=765, db_column='geneID', blank=True) # Field name made lowercase.
    taxid = models.CharField(max_length=765, db_column='taxID', blank=True) # Field name made lowercase.
    locustag = models.CharField(max_length=765, db_column='locusTag', blank=True) # Field name made lowercase.
    synonyms = models.CharField(max_length=765, blank=True)
    genesymbol = models.CharField(max_length=765, db_column='geneSymbol', blank=True) # Field name made lowercase.
    dbxrefs = models.CharField(max_length=765, db_column='dbXrefs', blank=True) # Field name made lowercase.
    chromosome = models.CharField(max_length=765, blank=True)
    maplocation = models.CharField(max_length=765, db_column='mapLocation', blank=True) # Field name made lowercase.
    description = models.CharField(max_length=765, blank=True)
    type = models.CharField(max_length=765, blank=True)
    symbolfromauth = models.CharField(max_length=765, db_column='symbolFromAuth', blank=True) # Field name made lowercase.
    fullname = models.CharField(max_length=765, db_column='fullName', blank=True) # Field name made lowercase.
    status = models.CharField(max_length=765, blank=True)
    others = models.CharField(max_length=765, blank=True)
    moddate = models.CharField(max_length=765, db_column='modDate', blank=True) # Field name made lowercase.
    deleted = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'firmiana_GeneIDMap'

class FirmianaPeptideidentification(models.Model):
    id = models.IntegerField(primary_key=True)
    qcresultid = models.ForeignKey('FirmianaQcresult', null=True, db_column='qcResultID', blank=True) # Field name made lowercase.
    spectrum = models.CharField(max_length=765, blank=True)
    startscan = models.CharField(max_length=60, db_column='startScan', blank=True) # Field name made lowercase.
    endscan = models.CharField(max_length=60, db_column='endScan', blank=True) # Field name made lowercase.
    precursorneutralmass = models.FloatField(null=True, db_column='precursorNeutralMass', blank=True) # Field name made lowercase.
    assumedcharge = models.IntegerField(null=True, db_column='assumedCharge', blank=True) # Field name made lowercase.
    retentiontime = models.FloatField(null=True, db_column='retentionTime', blank=True) # Field name made lowercase.
    peptide = models.CharField(max_length=765, blank=True)
    peptideprevaa = models.CharField(max_length=60, db_column='peptidePrevAa', blank=True) # Field name made lowercase.
    peptidenextaa = models.CharField(max_length=60, db_column='peptideNextAa', blank=True) # Field name made lowercase.
    numtotproteins = models.IntegerField(null=True, db_column='numTotProteins', blank=True) # Field name made lowercase.
    nummatchedions = models.IntegerField(null=True, db_column='numMatchedIons', blank=True) # Field name made lowercase.
    totnumions = models.IntegerField(null=True, db_column='totNumIons', blank=True) # Field name made lowercase.
    calcneutralpepmass = models.FloatField(null=True, db_column='calcNeutralPepMass', blank=True) # Field name made lowercase.
    nummissedcleavages = models.IntegerField(null=True, db_column='numMissedCleavages', blank=True) # Field name made lowercase.
    modification = models.CharField(max_length=765, blank=True)
    probability = models.FloatField(null=True, blank=True)
    iprobability = models.FloatField(null=True, blank=True)
    labelfreequantarea = models.FloatField(null=True, db_column='labelFreeQuantArea', blank=True) # Field name made lowercase.
    labelfreequantrt = models.FloatField(null=True, db_column='labelFreeQuantRT', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'firmiana_PeptideIdentification'

class FirmianaPeptideidentificationProteinseqinfo(models.Model):
    peptideidentificationid = models.ForeignKey(FirmianaPeptideidentification, primary_key=True, db_column='peptideIdentificationID') # Field name made lowercase.
    proteinseqinfoid = models.ForeignKey('FirmianaProteinseqinfo', db_column='proteinSeqInfoID') # Field name made lowercase.
    class Meta:
        db_table = u'firmiana_PeptideIdentification_ProteinSeqInfo'

class FirmianaPeptideProteinquantLabelfree(models.Model):
    peptidecomparison_labelfreeid = models.ForeignKey(FirmianaPeptidecomparisonLabelfree, primary_key=True, db_column='peptideComparison_LabelFreeID') # Field name made lowercase.
    proteinquant_labelfreeid = models.ForeignKey('FirmianaProteinquantLabelfree', db_column='proteinQuant_LabelFreeID') # Field name made lowercase.
    class Meta:
        db_table = u'firmiana_Peptide_ProteinQuant_LabelFree'

class FirmianaPeptideProteinIdentification(models.Model):
    peptideidentificationid = models.ForeignKey(FirmianaPeptideidentification, primary_key=True, db_column='peptideIdentificationID') # Field name made lowercase.
    proteinidentificationid = models.ForeignKey('FirmianaProteinidentification', db_column='proteinIdentificationID') # Field name made lowercase.
    class Meta:
        db_table = u'firmiana_Peptide_Protein_Identification'

class FirmianaProteingeneidmap(models.Model):
    id = models.IntegerField(primary_key=True)
    sourcedb = models.CharField(max_length=765, db_column='sourceDB', blank=True) # Field name made lowercase.
    sourceid = models.CharField(max_length=765, db_column='sourceID', blank=True) # Field name made lowercase.
    destdb = models.CharField(max_length=765, db_column='destDB', blank=True) # Field name made lowercase.
    destid = models.CharField(max_length=765, db_column='destID', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'firmiana_ProteinGeneIDMap'

class FirmianaProteinidentification(models.Model):
    id = models.IntegerField(primary_key=True)
    qcresultid = models.ForeignKey('FirmianaQcresult', null=True, db_column='qcResultID', blank=True) # Field name made lowercase.
    protein_name = models.CharField(max_length=1500, blank=True)
    n_indistinguishable_proteins = models.CharField(max_length=60, blank=True)
    probability = models.FloatField(null=True, blank=True)
    percent_coverage = models.FloatField(null=True, blank=True)
    unique_stripped_peptides = models.CharField(max_length=6000, blank=True)
    group_sibling_id = models.CharField(max_length=60, blank=True)
    total_number_peptides = models.IntegerField(null=True, blank=True)
    pct_spectrum_ids = models.FloatField(null=True, blank=True)
    confidence = models.FloatField(null=True, blank=True)
    indistinguishable_protein = models.CharField(max_length=6000, blank=True)
    class Meta:
        db_table = u'firmiana_ProteinIdentification'

class FirmianaProteinquantratioLabelfree(models.Model):
    id = models.IntegerField(primary_key=True)
    proteinquant_labelfreeid = models.ForeignKey('FirmianaProteinquantLabelfree', null=True, db_column='proteinQuant_LabelFreeID', blank=True) # Field name made lowercase.
    numerator = models.IntegerField(null=True, blank=True)
    denominator = models.IntegerField(null=True, blank=True)
    ratiovalue = models.FloatField(null=True, db_column='ratioValue', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'firmiana_ProteinQuantRatio_LabelFree'

class FirmianaProteinquantvalueLabelfree(models.Model):
    id = models.IntegerField(primary_key=True)
    proteinquant_labelfreeid = models.ForeignKey('FirmianaProteinquantLabelfree', null=True, db_column='proteinQuant_LabelFreeID', blank=True) # Field name made lowercase.
    experimentid = models.ForeignKey(FirmianaExperiment, null=True, db_column='experimentID', blank=True) # Field name made lowercase.
    replicateno = models.IntegerField(null=True, db_column='replicateNo', blank=True) # Field name made lowercase.
    intensity = models.FloatField(null=True, blank=True)
    uniqpeptidenum = models.IntegerField(null=True, db_column='uniqPeptideNum', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'firmiana_ProteinQuantValue_LabelFree'

class FirmianaProteinquantLabelfree(models.Model):
    id = models.IntegerField(primary_key=True)
    protein = models.CharField(max_length=6000, blank=True)
    comparisonid = models.ForeignKey(FirmianaComparison, null=True, db_column='comparisonID', blank=True) # Field name made lowercase.
    filepath = models.CharField(max_length=600, blank=True)
    class Meta:
        db_table = u'firmiana_ProteinQuant_LabelFree'

class FirmianaProteinseqidmap(models.Model):
    id = models.IntegerField(primary_key=True)
    sequenceid = models.ForeignKey('FirmianaProteinsequence', null=True, db_column='sequenceID', blank=True) # Field name made lowercase.
    dbtype = models.CharField(max_length=60, blank=True)
    dbversion = models.CharField(max_length=60, blank=True)
    dbname = models.CharField(max_length=300, blank=True)
    proteinseqinfoid = models.ForeignKey('FirmianaProteinseqinfo', null=True, db_column='proteinSeqInfoID', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'firmiana_ProteinSeqIDMap'

class FirmianaProteinseqinfo(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=600, blank=True)
    description = models.CharField(max_length=6000, blank=True)
    class Meta:
        db_table = u'firmiana_ProteinSeqInfo'

class FirmianaProteinsequence(models.Model):
    id = models.IntegerField(primary_key=True)
    sequence = models.CharField(max_length=150000, blank=True)
    class Meta:
        db_table = u'firmiana_ProteinSequence'

class FirmianaQcresult(models.Model):
    id = models.IntegerField(primary_key=True)
    filepath = models.CharField(max_length=765)
    method = models.CharField(max_length=150)
    class Meta:
        db_table = u'firmiana_QCResult'

class FirmianaQuantresult(models.Model):
    id = models.IntegerField(primary_key=True)
    qcresultid = models.ForeignKey('FirmianaQcresult', null=True, db_column='qcResultID', blank=True) # Field name made lowercase.
    filepath = models.CharField(max_length=765)
    method = models.CharField(max_length=150)
    class Meta:
        db_table = u'firmiana_QuantResult'

class FirmianaSearchscoresummary(models.Model):
    id = models.IntegerField(primary_key=True)
    pepidentificationid = models.ForeignKey(FirmianaPeptideidentification, null=True, db_column='pepIdentificationID', blank=True) # Field name made lowercase.
    fval = models.FloatField(null=True, blank=True)
    ntt = models.IntegerField(null=True, blank=True)
    nmc = models.IntegerField(null=True, blank=True)
    massd = models.FloatField(null=True, blank=True)
    isomassd = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'firmiana_SearchScoreSummary'

class FirmianaTwolabelquantresult(models.Model):
    id = models.IntegerField(primary_key=True)
    pepidentificationid = models.ForeignKey(FirmianaPeptideidentification, null=True, db_column='pepIdentificationID', blank=True) # Field name made lowercase.
    peptide = models.CharField(max_length=60, blank=True)
    heavyintensity = models.FloatField(null=True, db_column='heavyIntensity', blank=True) # Field name made lowercase.
    lightintensity = models.FloatField(null=True, db_column='lightIntensity', blank=True) # Field name made lowercase.
    ratio = models.CharField(max_length=60, blank=True)
    class Meta:
        db_table = u'firmiana_TwoLabelQuantResult'

class FirmianaXtandemparam(models.Model):
    id = models.IntegerField(primary_key=True)
    dbsearchresultid = models.ForeignKey(FirmianaDbsearchresult, null=True, db_column='dbsearchResultID', blank=True) # Field name made lowercase.
    database = models.CharField(max_length=450)
    var_mods = models.CharField(max_length=765, blank=True)
    fix_mods = models.CharField(max_length=765, blank=True)
    enzyme = models.CharField(max_length=765, blank=True)
    precursor_tolu = models.CharField(max_length=30)
    missed_cleavages = models.IntegerField()
    fragment_ion_tol = models.FloatField(null=True, blank=True)
    precursor_ion_tol = models.FloatField(null=True, blank=True)
    paramfile = models.CharField(max_length=450)
    taxonfile = models.CharField(max_length=450)
    class Meta:
        db_table = u'firmiana_XtandemParam'
"""
class FormDefinition(models.Model):
    id = models.IntegerField(primary_key=True)
    create_time = models.DateTimeField(null=True, blank=True)
    update_time = models.DateTimeField(null=True, blank=True)
    name = models.CharField(max_length=765)
    desc = models.TextField(blank=True)
    form_definition_current_id = models.IntegerField()
    fields = models.TextField(blank=True)
    type = models.CharField(max_length=765, blank=True)
    layout = models.TextField(blank=True)
    class Meta:
        db_table = u'form_definition'

class FormDefinitionCurrent(models.Model):
    id = models.IntegerField(primary_key=True)
    create_time = models.DateTimeField(null=True, blank=True)
    update_time = models.DateTimeField(null=True, blank=True)
    latest_form_id = models.IntegerField(null=True, blank=True)
    deleted = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'form_definition_current'

class FormValues(models.Model):
    id = models.IntegerField(primary_key=True)
    create_time = models.DateTimeField(null=True, blank=True)
    update_time = models.DateTimeField(null=True, blank=True)
    form_definition_id = models.IntegerField(null=True, blank=True)
    content = models.TextField(blank=True)
    class Meta:
        db_table = u'form_values'

class GalaxyGroup(models.Model):
    id = models.IntegerField(primary_key=True)
    create_time = models.DateTimeField(null=True, blank=True)
    update_time = models.DateTimeField(null=True, blank=True)
    name = models.CharField(max_length=765, unique=True, blank=True)
    deleted = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'galaxy_group'

class GalaxySession(models.Model):
    id = models.IntegerField(primary_key=True)
    create_time = models.DateTimeField(null=True, blank=True)
    update_time = models.DateTimeField(null=True, blank=True)
    user_id = models.IntegerField(null=True, blank=True)
    remote_host = models.CharField(max_length=765, blank=True)
    remote_addr = models.CharField(max_length=765, blank=True)
    referer = models.TextField(blank=True)
    current_history_id = models.IntegerField(null=True, blank=True)
    session_key = models.CharField(max_length=765, unique=True, blank=True)
    is_valid = models.IntegerField(null=True, blank=True)
    prev_session_id = models.IntegerField(null=True, blank=True)
    disk_usage = models.DecimalField(null=True, max_digits=16, decimal_places=0, blank=True)
    class Meta:
        db_table = u'galaxy_session'

class GalaxySessionToHistory(models.Model):
    id = models.IntegerField(primary_key=True)
    create_time = models.DateTimeField(null=True, blank=True)
    session_id = models.IntegerField(null=True, blank=True)
    history_id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'galaxy_session_to_history'
""" 
class GalaxyUser(models.Model):
    id = models.IntegerField(primary_key=True)
    create_time = models.DateTimeField(null=True, blank=True)
    update_time = models.DateTimeField(null=True, blank=True)
    email = models.CharField(max_length=765)
    password = models.CharField(max_length=120)
    external = models.IntegerField(null=True, blank=True)
    deleted = models.IntegerField(null=True, blank=True)
    purged = models.IntegerField(null=True, blank=True)
    username = models.CharField(max_length=765, blank=True)
    form_values_id = models.IntegerField(null=True, blank=True)
    disk_usage = models.DecimalField(null=True, max_digits=16, decimal_places=0, blank=True)
    class Meta:
        db_table = u'galaxy_user'
"""
class GalaxyUserOpenid(models.Model):
    id = models.IntegerField(primary_key=True)
    create_time = models.DateTimeField(null=True, blank=True)
    update_time = models.DateTimeField(null=True, blank=True)
    session_id = models.IntegerField(null=True, blank=True)
    user_id = models.IntegerField(null=True, blank=True)
    openid = models.TextField(unique=True, blank=True)
    provider = models.CharField(max_length=765, blank=True)
    class Meta:
        db_table = u'galaxy_user_openid'

class GenomeIndexToolData(models.Model):
    id = models.IntegerField(primary_key=True)
    job_id = models.IntegerField(null=True, blank=True)
    dataset_id = models.IntegerField(null=True, blank=True)
    deferred_job_id = models.IntegerField(null=True, blank=True)
    transfer_job_id = models.IntegerField(null=True, blank=True)
    fasta_path = models.CharField(max_length=765, blank=True)
    created_time = models.DateTimeField(null=True, blank=True)
    modified_time = models.DateTimeField(null=True, blank=True)
    indexer = models.CharField(max_length=192, blank=True)
    user_id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'genome_index_tool_data'

class GroupQuotaAssociation(models.Model):
    id = models.IntegerField(primary_key=True)
    group_id = models.IntegerField(null=True, blank=True)
    quota_id = models.IntegerField(null=True, blank=True)
    create_time = models.DateTimeField(null=True, blank=True)
    update_time = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'group_quota_association'

class GroupRoleAssociation(models.Model):
    id = models.IntegerField(primary_key=True)
    group_id = models.IntegerField(null=True, blank=True)
    role_id = models.IntegerField(null=True, blank=True)
    create_time = models.DateTimeField(null=True, blank=True)
    update_time = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'group_role_association'

class History(models.Model):
    id = models.IntegerField(primary_key=True)
    create_time = models.DateTimeField(null=True, blank=True)
    update_time = models.DateTimeField(null=True, blank=True)
    user_id = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=765, blank=True)
    hid_counter = models.IntegerField(null=True, blank=True)
    deleted = models.IntegerField(null=True, blank=True)
    purged = models.IntegerField(null=True, blank=True)
    genome_build = models.CharField(max_length=120, blank=True)
    importable = models.IntegerField(null=True, blank=True)
    slug = models.TextField(blank=True)
    published = models.IntegerField(null=True, blank=True)
    importing = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'history'

class HistoryAnnotationAssociation(models.Model):
    id = models.IntegerField(primary_key=True)
    history_id = models.IntegerField(null=True, blank=True)
    user_id = models.IntegerField(null=True, blank=True)
    annotation = models.TextField(blank=True)
    class Meta:
        db_table = u'history_annotation_association'

class HistoryDatasetAssociation(models.Model):
    id = models.IntegerField(primary_key=True)
    history_id = models.IntegerField(null=True, blank=True)
    dataset_id = models.IntegerField(null=True, blank=True)
    create_time = models.DateTimeField(null=True, blank=True)
    update_time = models.DateTimeField(null=True, blank=True)
    copied_from_history_dataset_association_id = models.IntegerField(null=True, blank=True)
    hid = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=765, blank=True)
    info = models.CharField(max_length=765, blank=True)
    blurb = models.CharField(max_length=765, blank=True)
    peek = models.TextField(blank=True)
    extension = models.CharField(max_length=192, blank=True)
    metadata = models.TextField(blank=True)
    parent_id = models.IntegerField(null=True, blank=True)
    designation = models.CharField(max_length=765, blank=True)
    deleted = models.IntegerField(null=True, blank=True)
    visible = models.IntegerField(null=True, blank=True)
    copied_from_library_dataset_dataset_association_id = models.IntegerField(null=True, blank=True)
    state = models.CharField(max_length=192, blank=True)
    purged = models.IntegerField(null=True, blank=True)
    tool_version = models.TextField(blank=True)
    class Meta:
        db_table = u'history_dataset_association'

class HistoryDatasetAssociationAnnotationAssociation(models.Model):
    id = models.IntegerField(primary_key=True)
    history_dataset_association_id = models.IntegerField(null=True, blank=True)
    user_id = models.IntegerField(null=True, blank=True)
    annotation = models.TextField(blank=True)
    class Meta:
        db_table = u'history_dataset_association_annotation_association'

class HistoryDatasetAssociationDisplayAtAuthorization(models.Model):
    id = models.IntegerField(primary_key=True)
    create_time = models.DateTimeField(null=True, blank=True)
    update_time = models.DateTimeField(null=True, blank=True)
    history_dataset_association_id = models.IntegerField(null=True, blank=True)
    user_id = models.IntegerField(null=True, blank=True)
    site = models.CharField(max_length=765, blank=True)
    class Meta:
        db_table = u'history_dataset_association_display_at_authorization'

class HistoryDatasetAssociationRatingAssociation(models.Model):
    id = models.IntegerField(primary_key=True)
    history_dataset_association_id = models.IntegerField(null=True, blank=True)
    user_id = models.IntegerField(null=True, blank=True)
    rating = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'history_dataset_association_rating_association'

class HistoryDatasetAssociationSubset(models.Model):
    id = models.IntegerField(primary_key=True)
    history_dataset_association_id = models.IntegerField(null=True, blank=True)
    history_dataset_association_subset_id = models.IntegerField(null=True, blank=True)
    location = models.CharField(max_length=765, blank=True)
    class Meta:
        db_table = u'history_dataset_association_subset'

class HistoryDatasetAssociationTagAssociation(models.Model):
    id = models.IntegerField(primary_key=True)
    history_dataset_association_id = models.IntegerField(null=True, blank=True)
    tag_id = models.IntegerField(null=True, blank=True)
    user_tname = models.CharField(max_length=765, blank=True)
    value = models.CharField(max_length=765, blank=True)
    user_value = models.CharField(max_length=765, blank=True)
    user_id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'history_dataset_association_tag_association'

class HistoryRatingAssociation(models.Model):
    id = models.IntegerField(primary_key=True)
    history_id = models.IntegerField(null=True, blank=True)
    user_id = models.IntegerField(null=True, blank=True)
    rating = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'history_rating_association'

class HistoryTagAssociation(models.Model):
    id = models.IntegerField(primary_key=True)
    history_id = models.IntegerField(null=True, blank=True)
    tag_id = models.IntegerField(null=True, blank=True)
    user_tname = models.CharField(max_length=765, blank=True)
    value = models.CharField(max_length=765, blank=True)
    user_value = models.CharField(max_length=765, blank=True)
    user_id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'history_tag_association'

class HistoryUserShareAssociation(models.Model):
    id = models.IntegerField(primary_key=True)
    history_id = models.IntegerField(null=True, blank=True)
    user_id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'history_user_share_association'

class ImplicitlyConvertedDatasetAssociation(models.Model):
    id = models.IntegerField(primary_key=True)
    create_time = models.DateTimeField(null=True, blank=True)
    update_time = models.DateTimeField(null=True, blank=True)
    hda_id = models.IntegerField(null=True, blank=True)
    hda_parent_id = models.IntegerField(null=True, blank=True)
    deleted = models.IntegerField(null=True, blank=True)
    metadata_safe = models.IntegerField(null=True, blank=True)
    type = models.CharField(max_length=765, blank=True)
    ldda_parent_id = models.IntegerField(null=True, blank=True)
    ldda_id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'implicitly_converted_dataset_association'

class Job(models.Model):
    id = models.IntegerField(primary_key=True)
    create_time = models.DateTimeField(null=True, blank=True)
    update_time = models.DateTimeField(null=True, blank=True)
    history_id = models.IntegerField(null=True, blank=True)
    tool_id = models.CharField(max_length=765, blank=True)
    tool_version = models.TextField(blank=True)
    state = models.CharField(max_length=192, blank=True)
    info = models.CharField(max_length=765, blank=True)
    command_line = models.TextField(blank=True)
    param_filename = models.CharField(max_length=3072, blank=True)
    runner_name = models.CharField(max_length=765, blank=True)
    stdout = models.TextField(blank=True)
    stderr = models.TextField(blank=True)
    traceback = models.TextField(blank=True)
    session_id = models.IntegerField(null=True, blank=True)
    job_runner_name = models.CharField(max_length=765, blank=True)
    job_runner_external_id = models.CharField(max_length=765, blank=True)
    library_folder_id = models.IntegerField(null=True, blank=True)
    user_id = models.IntegerField(null=True, blank=True)
    imported = models.IntegerField(null=True, blank=True)
    object_store_id = models.CharField(max_length=765, blank=True)
    params = models.CharField(max_length=765, blank=True)
    handler = models.CharField(max_length=765, blank=True)
    exit_code = models.IntegerField(null=True, blank=True)
    destination_id = models.CharField(max_length=765, blank=True)
    destination_params = models.TextField(blank=True)
    class Meta:
        db_table = u'job'

class JobExportHistoryArchive(models.Model):
    id = models.IntegerField(primary_key=True)
    job_id = models.IntegerField(null=True, blank=True)
    history_id = models.IntegerField(null=True, blank=True)
    dataset_id = models.IntegerField(null=True, blank=True)
    compressed = models.IntegerField(null=True, blank=True)
    history_attrs_filename = models.TextField(blank=True)
    datasets_attrs_filename = models.TextField(blank=True)
    jobs_attrs_filename = models.TextField(blank=True)
    class Meta:
        db_table = u'job_export_history_archive'

class JobExternalOutputMetadata(models.Model):
    id = models.IntegerField(primary_key=True)
    job_id = models.IntegerField(null=True, blank=True)
    history_dataset_association_id = models.IntegerField(null=True, blank=True)
    library_dataset_dataset_association_id = models.IntegerField(null=True, blank=True)
    filename_in = models.CharField(max_length=765, blank=True)
    filename_out = models.CharField(max_length=765, blank=True)
    filename_results_code = models.CharField(max_length=765, blank=True)
    filename_kwds = models.CharField(max_length=765, blank=True)
    job_runner_external_pid = models.CharField(max_length=765, blank=True)
    filename_override_metadata = models.CharField(max_length=765, blank=True)
    class Meta:
        db_table = u'job_external_output_metadata'

class JobImportHistoryArchive(models.Model):
    id = models.IntegerField(primary_key=True)
    job_id = models.IntegerField(null=True, blank=True)
    history_id = models.IntegerField(null=True, blank=True)
    archive_dir = models.TextField(blank=True)
    class Meta:
        db_table = u'job_import_history_archive'

class JobParameter(models.Model):
    id = models.IntegerField(primary_key=True)
    job_id = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=765, blank=True)
    value = models.TextField(blank=True)
    class Meta:
        db_table = u'job_parameter'

class JobToInputDataset(models.Model):
    id = models.IntegerField(primary_key=True)
    job_id = models.IntegerField(null=True, blank=True)
    dataset_id = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=765, blank=True)
    class Meta:
        db_table = u'job_to_input_dataset'

class JobToInputLibraryDataset(models.Model):
    id = models.IntegerField(primary_key=True)
    job_id = models.IntegerField(null=True, blank=True)
    ldda_id = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=765, blank=True)
    class Meta:
        db_table = u'job_to_input_library_dataset'

class JobToOutputDataset(models.Model):
    id = models.IntegerField(primary_key=True)
    job_id = models.IntegerField(null=True, blank=True)
    dataset_id = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=765, blank=True)
    class Meta:
        db_table = u'job_to_output_dataset'

class JobToOutputLibraryDataset(models.Model):
    id = models.IntegerField(primary_key=True)
    job_id = models.IntegerField(null=True, blank=True)
    ldda_id = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=765, blank=True)
    class Meta:
        db_table = u'job_to_output_library_dataset'

class Library(models.Model):
    id = models.IntegerField(primary_key=True)
    root_folder_id = models.IntegerField(null=True, blank=True)
    create_time = models.DateTimeField(null=True, blank=True)
    update_time = models.DateTimeField(null=True, blank=True)
    name = models.CharField(max_length=765, blank=True)
    deleted = models.IntegerField(null=True, blank=True)
    purged = models.IntegerField(null=True, blank=True)
    description = models.TextField(blank=True)
    synopsis = models.TextField(blank=True)
    class Meta:
        db_table = u'library'

class LibraryDataset(models.Model):
    id = models.IntegerField(primary_key=True)
    library_dataset_dataset_association_id = models.IntegerField(null=True, blank=True)
    folder_id = models.IntegerField(null=True, blank=True)
    order_id = models.IntegerField(null=True, blank=True)
    create_time = models.DateTimeField(null=True, blank=True)
    update_time = models.DateTimeField(null=True, blank=True)
    name = models.CharField(max_length=765, blank=True)
    info = models.CharField(max_length=765, blank=True)
    deleted = models.IntegerField(null=True, blank=True)
    purged = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'library_dataset'

class LibraryDatasetDatasetAssociation(models.Model):
    id = models.IntegerField(primary_key=True)
    library_dataset_id = models.IntegerField(null=True, blank=True)
    dataset_id = models.IntegerField(null=True, blank=True)
    create_time = models.DateTimeField(null=True, blank=True)
    update_time = models.DateTimeField(null=True, blank=True)
    copied_from_history_dataset_association_id = models.IntegerField(null=True, blank=True)
    copied_from_library_dataset_dataset_association_id = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=765, blank=True)
    info = models.CharField(max_length=765, blank=True)
    blurb = models.CharField(max_length=765, blank=True)
    peek = models.TextField(blank=True)
    extension = models.CharField(max_length=192, blank=True)
    metadata = models.TextField(blank=True)
    parent_id = models.IntegerField(null=True, blank=True)
    designation = models.CharField(max_length=765, blank=True)
    deleted = models.IntegerField(null=True, blank=True)
    visible = models.IntegerField(null=True, blank=True)
    user_id = models.IntegerField(null=True, blank=True)
    message = models.CharField(max_length=765, blank=True)
    state = models.CharField(max_length=192, blank=True)
    tool_version = models.TextField(blank=True)
    extended_metadata_id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'library_dataset_dataset_association'

class LibraryDatasetDatasetAssociationPermissions(models.Model):
    id = models.IntegerField(primary_key=True)
    create_time = models.DateTimeField(null=True, blank=True)
    update_time = models.DateTimeField(null=True, blank=True)
    action = models.TextField(blank=True)
    library_dataset_dataset_association_id = models.IntegerField(null=True, blank=True)
    role_id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'library_dataset_dataset_association_permissions'

class LibraryDatasetDatasetInfoAssociation(models.Model):
    id = models.IntegerField(primary_key=True)
    library_dataset_dataset_association_id = models.IntegerField(null=True, blank=True)
    form_definition_id = models.IntegerField(null=True, blank=True)
    form_values_id = models.IntegerField(null=True, blank=True)
    deleted = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'library_dataset_dataset_info_association'

class LibraryDatasetPermissions(models.Model):
    id = models.IntegerField(primary_key=True)
    create_time = models.DateTimeField(null=True, blank=True)
    update_time = models.DateTimeField(null=True, blank=True)
    action = models.TextField(blank=True)
    library_dataset_id = models.IntegerField(null=True, blank=True)
    role_id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'library_dataset_permissions'

class LibraryFolder(models.Model):
    id = models.IntegerField(primary_key=True)
    parent_id = models.IntegerField(null=True, blank=True)
    create_time = models.DateTimeField(null=True, blank=True)
    update_time = models.DateTimeField(null=True, blank=True)
    name = models.TextField(blank=True)
    description = models.TextField(blank=True)
    order_id = models.IntegerField(null=True, blank=True)
    item_count = models.IntegerField(null=True, blank=True)
    deleted = models.IntegerField(null=True, blank=True)
    purged = models.IntegerField(null=True, blank=True)
    genome_build = models.CharField(max_length=120, blank=True)
    class Meta:
        db_table = u'library_folder'

class LibraryFolderInfoAssociation(models.Model):
    id = models.IntegerField(primary_key=True)
    library_folder_id = models.IntegerField(null=True, blank=True)
    form_definition_id = models.IntegerField(null=True, blank=True)
    form_values_id = models.IntegerField(null=True, blank=True)
    deleted = models.IntegerField(null=True, blank=True)
    inheritable = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'library_folder_info_association'

class LibraryFolderPermissions(models.Model):
    id = models.IntegerField(primary_key=True)
    create_time = models.DateTimeField(null=True, blank=True)
    update_time = models.DateTimeField(null=True, blank=True)
    action = models.TextField(blank=True)
    library_folder_id = models.IntegerField(null=True, blank=True)
    role_id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'library_folder_permissions'

class LibraryInfoAssociation(models.Model):
    id = models.IntegerField(primary_key=True)
    library_id = models.IntegerField(null=True, blank=True)
    form_definition_id = models.IntegerField(null=True, blank=True)
    form_values_id = models.IntegerField(null=True, blank=True)
    deleted = models.IntegerField(null=True, blank=True)
    inheritable = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'library_info_association'

class LibraryPermissions(models.Model):
    id = models.IntegerField(primary_key=True)
    create_time = models.DateTimeField(null=True, blank=True)
    update_time = models.DateTimeField(null=True, blank=True)
    action = models.TextField(blank=True)
    library_id = models.IntegerField(null=True, blank=True)
    role_id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'library_permissions'

class MetadataFile(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField(blank=True)
    hda_id = models.IntegerField(null=True, blank=True)
    create_time = models.DateTimeField(null=True, blank=True)
    update_time = models.DateTimeField(null=True, blank=True)
    deleted = models.IntegerField(null=True, blank=True)
    purged = models.IntegerField(null=True, blank=True)
    lda_id = models.IntegerField(null=True, blank=True)
    object_store_id = models.CharField(max_length=765, blank=True)
    class Meta:
        db_table = u'metadata_file'

class MigrateTools(models.Model):
    repository_id = models.CharField(max_length=765, blank=True)
    repository_path = models.TextField(blank=True)
    version = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'migrate_tools'

class MigrateVersion(models.Model):
    repository_id = models.CharField(max_length=765, primary_key=True)
    repository_path = models.TextField(blank=True)
    version = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'migrate_version'

class Page(models.Model):
    id = models.IntegerField(primary_key=True)
    create_time = models.DateTimeField(null=True, blank=True)
    update_time = models.DateTimeField(null=True, blank=True)
    user_id = models.IntegerField()
    latest_revision_id = models.IntegerField(null=True, blank=True)
    title = models.TextField(blank=True)
    slug = models.TextField(blank=True)
    published = models.IntegerField(null=True, blank=True)
    deleted = models.IntegerField(null=True, blank=True)
    importable = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'page'

class PageAnnotationAssociation(models.Model):
    id = models.IntegerField(primary_key=True)
    page_id = models.IntegerField(null=True, blank=True)
    user_id = models.IntegerField(null=True, blank=True)
    annotation = models.TextField(blank=True)
    class Meta:
        db_table = u'page_annotation_association'

class PageRatingAssociation(models.Model):
    id = models.IntegerField(primary_key=True)
    page_id = models.IntegerField(null=True, blank=True)
    user_id = models.IntegerField(null=True, blank=True)
    rating = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'page_rating_association'

class PageRevision(models.Model):
    id = models.IntegerField(primary_key=True)
    create_time = models.DateTimeField(null=True, blank=True)
    update_time = models.DateTimeField(null=True, blank=True)
    page_id = models.IntegerField()
    title = models.TextField(blank=True)
    content = models.TextField(blank=True)
    class Meta:
        db_table = u'page_revision'

class PageTagAssociation(models.Model):
    id = models.IntegerField(primary_key=True)
    page_id = models.IntegerField(null=True, blank=True)
    tag_id = models.IntegerField(null=True, blank=True)
    user_tname = models.CharField(max_length=765, blank=True)
    value = models.CharField(max_length=765, blank=True)
    user_value = models.CharField(max_length=765, blank=True)
    user_id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'page_tag_association'

class PageUserShareAssociation(models.Model):
    id = models.IntegerField(primary_key=True)
    page_id = models.IntegerField(null=True, blank=True)
    user_id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'page_user_share_association'

class PostJobAction(models.Model):
    id = models.IntegerField(primary_key=True)
    workflow_step_id = models.IntegerField()
    action_type = models.CharField(max_length=765)
    output_name = models.CharField(max_length=765, blank=True)
    action_arguments = models.TextField(blank=True)
    class Meta:
        db_table = u'post_job_action'

class PostJobActionAssociation(models.Model):
    id = models.IntegerField(primary_key=True)
    post_job_action_id = models.IntegerField()
    job_id = models.IntegerField()
    class Meta:
        db_table = u'post_job_action_association'

class Quota(models.Model):
    id = models.IntegerField(primary_key=True)
    create_time = models.DateTimeField(null=True, blank=True)
    update_time = models.DateTimeField(null=True, blank=True)
    name = models.CharField(max_length=765, unique=True, blank=True)
    description = models.TextField(blank=True)
    bytes = models.BigIntegerField(null=True, blank=True)
    operation = models.CharField(max_length=24, blank=True)
    deleted = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'quota'

class RepositoryDependency(models.Model):
    id = models.IntegerField(primary_key=True)
    create_time = models.DateTimeField(null=True, blank=True)
    update_time = models.DateTimeField(null=True, blank=True)
    tool_shed_repository_id = models.IntegerField()
    class Meta:
        db_table = u'repository_dependency'

class RepositoryRepositoryDependencyAssociation(models.Model):
    id = models.IntegerField(primary_key=True)
    create_time = models.DateTimeField(null=True, blank=True)
    update_time = models.DateTimeField(null=True, blank=True)
    tool_shed_repository_id = models.IntegerField(null=True, blank=True)
    repository_dependency_id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'repository_repository_dependency_association'

class Request(models.Model):
    id = models.IntegerField(primary_key=True)
    create_time = models.DateTimeField(null=True, blank=True)
    update_time = models.DateTimeField(null=True, blank=True)
    name = models.CharField(max_length=765)
    desc = models.TextField(blank=True)
    form_values_id = models.IntegerField(null=True, blank=True)
    request_type_id = models.IntegerField(null=True, blank=True)
    user_id = models.IntegerField(null=True, blank=True)
    deleted = models.IntegerField(null=True, blank=True)
    notification = models.TextField(blank=True)
    class Meta:
        db_table = u'request'

class RequestEvent(models.Model):
    id = models.IntegerField(primary_key=True)
    create_time = models.DateTimeField(null=True, blank=True)
    update_time = models.DateTimeField(null=True, blank=True)
    request_id = models.IntegerField(null=True, blank=True)
    state = models.CharField(max_length=765, blank=True)
    comment = models.TextField(blank=True)
    class Meta:
        db_table = u'request_event'

class RequestType(models.Model):
    id = models.IntegerField(primary_key=True)
    create_time = models.DateTimeField(null=True, blank=True)
    update_time = models.DateTimeField(null=True, blank=True)
    name = models.CharField(max_length=765)
    desc = models.TextField(blank=True)
    request_form_id = models.IntegerField(null=True, blank=True)
    sample_form_id = models.IntegerField(null=True, blank=True)
    deleted = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'request_type'

class RequestTypeExternalServiceAssociation(models.Model):
    id = models.IntegerField(primary_key=True)
    request_type_id = models.IntegerField(null=True, blank=True)
    external_service_id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'request_type_external_service_association'

class RequestTypePermissions(models.Model):
    id = models.IntegerField(primary_key=True)
    create_time = models.DateTimeField(null=True, blank=True)
    update_time = models.DateTimeField(null=True, blank=True)
    action = models.TextField(blank=True)
    request_type_id = models.IntegerField(null=True, blank=True)
    role_id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'request_type_permissions'

class RequestTypeRunAssociation(models.Model):
    id = models.IntegerField(primary_key=True)
    request_type_id = models.IntegerField()
    run_id = models.IntegerField()
    class Meta:
        db_table = u'request_type_run_association'

class Role(models.Model):
    id = models.IntegerField(primary_key=True)
    create_time = models.DateTimeField(null=True, blank=True)
    update_time = models.DateTimeField(null=True, blank=True)
    name = models.CharField(max_length=765, unique=True, blank=True)
    description = models.TextField(blank=True)
    type = models.CharField(max_length=120, blank=True)
    deleted = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'role'

class Run(models.Model):
    id = models.IntegerField(primary_key=True)
    create_time = models.DateTimeField(null=True, blank=True)
    update_time = models.DateTimeField(null=True, blank=True)
    form_definition_id = models.IntegerField(null=True, blank=True)
    form_values_id = models.IntegerField(null=True, blank=True)
    deleted = models.IntegerField(null=True, blank=True)
    subindex = models.CharField(max_length=765, blank=True)
    class Meta:
        db_table = u'run'

class Sample(models.Model):
    id = models.IntegerField(primary_key=True)
    create_time = models.DateTimeField(null=True, blank=True)
    update_time = models.DateTimeField(null=True, blank=True)
    name = models.CharField(max_length=765)
    desc = models.TextField(blank=True)
    form_values_id = models.IntegerField(null=True, blank=True)
    request_id = models.IntegerField(null=True, blank=True)
    deleted = models.IntegerField(null=True, blank=True)
    bar_code = models.CharField(max_length=765, blank=True)
    library_id = models.IntegerField(null=True, blank=True)
    folder_id = models.IntegerField(null=True, blank=True)
    workflow = models.TextField(blank=True)
    history_id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'sample'

class SampleDataset(models.Model):
    id = models.IntegerField(primary_key=True)
    create_time = models.DateTimeField(null=True, blank=True)
    update_time = models.DateTimeField(null=True, blank=True)
    sample_id = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=765)
    status = models.CharField(max_length=765)
    error_msg = models.TextField(blank=True)
    size = models.CharField(max_length=765, blank=True)
    file_path = models.TextField(blank=True)
    external_service_id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'sample_dataset'

class SampleEvent(models.Model):
    id = models.IntegerField(primary_key=True)
    create_time = models.DateTimeField(null=True, blank=True)
    update_time = models.DateTimeField(null=True, blank=True)
    sample_id = models.IntegerField(null=True, blank=True)
    sample_state_id = models.IntegerField(null=True, blank=True)
    comment = models.TextField(blank=True)
    class Meta:
        db_table = u'sample_event'

class SampleRunAssociation(models.Model):
    id = models.IntegerField(primary_key=True)
    sample_id = models.IntegerField()
    run_id = models.IntegerField()
    class Meta:
        db_table = u'sample_run_association'

class SampleState(models.Model):
    id = models.IntegerField(primary_key=True)
    create_time = models.DateTimeField(null=True, blank=True)
    update_time = models.DateTimeField(null=True, blank=True)
    name = models.CharField(max_length=765)
    desc = models.TextField(blank=True)
    request_type_id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'sample_state'

class StoredWorkflow(models.Model):
    id = models.IntegerField(primary_key=True)
    create_time = models.DateTimeField(null=True, blank=True)
    update_time = models.DateTimeField(null=True, blank=True)
    user_id = models.IntegerField()
    latest_workflow_id = models.IntegerField(null=True, blank=True)
    name = models.TextField(blank=True)
    deleted = models.IntegerField(null=True, blank=True)
    importable = models.IntegerField(null=True, blank=True)
    slug = models.TextField(blank=True)
    published = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'stored_workflow'

class StoredWorkflowAnnotationAssociation(models.Model):
    id = models.IntegerField(primary_key=True)
    stored_workflow_id = models.IntegerField(null=True, blank=True)
    user_id = models.IntegerField(null=True, blank=True)
    annotation = models.TextField(blank=True)
    class Meta:
        db_table = u'stored_workflow_annotation_association'

class StoredWorkflowMenuEntry(models.Model):
    id = models.IntegerField(primary_key=True)
    stored_workflow_id = models.IntegerField(null=True, blank=True)
    user_id = models.IntegerField(null=True, blank=True)
    order_index = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'stored_workflow_menu_entry'

class StoredWorkflowRatingAssociation(models.Model):
    id = models.IntegerField(primary_key=True)
    stored_workflow_id = models.IntegerField(null=True, blank=True)
    user_id = models.IntegerField(null=True, blank=True)
    rating = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'stored_workflow_rating_association'

class StoredWorkflowTagAssociation(models.Model):
    id = models.IntegerField(primary_key=True)
    stored_workflow_id = models.IntegerField(null=True, blank=True)
    tag_id = models.IntegerField(null=True, blank=True)
    user_id = models.IntegerField(null=True, blank=True)
    user_tname = models.CharField(max_length=765, blank=True)
    value = models.CharField(max_length=765, blank=True)
    user_value = models.CharField(max_length=765, blank=True)
    class Meta:
        db_table = u'stored_workflow_tag_association'

class StoredWorkflowUserShareConnection(models.Model):
    id = models.IntegerField(primary_key=True)
    stored_workflow_id = models.IntegerField(null=True, blank=True)
    user_id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'stored_workflow_user_share_connection'

class Tag(models.Model):
    id = models.IntegerField(primary_key=True)
    type = models.IntegerField(null=True, blank=True)
    parent_id = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=765, unique=True, blank=True)
    class Meta:
        db_table = u'tag'

class Task(models.Model):
    id = models.IntegerField(primary_key=True)
    create_time = models.DateTimeField(null=True, blank=True)
    execution_time = models.DateTimeField(null=True, blank=True)
    update_time = models.DateTimeField(null=True, blank=True)
    state = models.CharField(max_length=192, blank=True)
    command_line = models.TextField(blank=True)
    param_filename = models.CharField(max_length=3072, blank=True)
    runner_name = models.CharField(max_length=765, blank=True)
    stdout = models.TextField(blank=True)
    stderr = models.TextField(blank=True)
    traceback = models.TextField(blank=True)
    job_id = models.IntegerField()
    task_runner_name = models.CharField(max_length=765, blank=True)
    task_runner_external_id = models.CharField(max_length=765, blank=True)
    prepare_input_files_cmd = models.TextField(blank=True)
    working_directory = models.CharField(max_length=3072, blank=True)
    info = models.CharField(max_length=765, blank=True)
    exit_code = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'task'

class ToolDependency(models.Model):
    id = models.IntegerField(primary_key=True)
    create_time = models.DateTimeField(null=True, blank=True)
    update_time = models.DateTimeField(null=True, blank=True)
    tool_shed_repository_id = models.IntegerField()
    name = models.CharField(max_length=765, blank=True)
    version = models.TextField(blank=True)
    type = models.CharField(max_length=120, blank=True)
    status = models.CharField(max_length=765)
    error_message = models.TextField(blank=True)
    class Meta:
        db_table = u'tool_dependency'

class ToolShedRepository(models.Model):
    id = models.IntegerField(primary_key=True)
    create_time = models.DateTimeField(null=True, blank=True)
    update_time = models.DateTimeField(null=True, blank=True)
    tool_shed = models.CharField(max_length=765, blank=True)
    name = models.CharField(max_length=765, blank=True)
    description = models.TextField(blank=True)
    owner = models.CharField(max_length=765, blank=True)
    changeset_revision = models.CharField(max_length=765, blank=True)
    deleted = models.IntegerField(null=True, blank=True)
    metadata = models.TextField(blank=True)
    includes_datatypes = models.IntegerField(null=True, blank=True)
    update_available = models.IntegerField(null=True, blank=True)
    installed_changeset_revision = models.CharField(max_length=765, blank=True)
    uninstalled = models.IntegerField(null=True, blank=True)
    dist_to_shed = models.IntegerField(null=True, blank=True)
    ctx_rev = models.CharField(max_length=30, blank=True)
    status = models.CharField(max_length=765, blank=True)
    error_message = models.TextField(blank=True)
    class Meta:
        db_table = u'tool_shed_repository'

class ToolTagAssociation(models.Model):
    id = models.IntegerField(primary_key=True)
    tool_id = models.CharField(max_length=765, blank=True)
    tag_id = models.IntegerField(null=True, blank=True)
    user_id = models.IntegerField(null=True, blank=True)
    user_tname = models.CharField(max_length=765, blank=True)
    value = models.CharField(max_length=765, blank=True)
    user_value = models.CharField(max_length=765, blank=True)
    class Meta:
        db_table = u'tool_tag_association'

class ToolVersion(models.Model):
    id = models.IntegerField(primary_key=True)
    create_time = models.DateTimeField(null=True, blank=True)
    update_time = models.DateTimeField(null=True, blank=True)
    tool_id = models.CharField(max_length=765, blank=True)
    tool_shed_repository_id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'tool_version'

class ToolVersionAssociation(models.Model):
    id = models.IntegerField(primary_key=True)
    tool_id = models.IntegerField()
    parent_id = models.IntegerField()
    class Meta:
        db_table = u'tool_version_association'

class TransferJob(models.Model):
    id = models.IntegerField(primary_key=True)
    create_time = models.DateTimeField(null=True, blank=True)
    update_time = models.DateTimeField(null=True, blank=True)
    state = models.CharField(max_length=192, blank=True)
    path = models.CharField(max_length=3072, blank=True)
    params = models.TextField(blank=True)
    info = models.TextField(blank=True)
    pid = models.IntegerField(null=True, blank=True)
    socket = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'transfer_job'

class UserAction(models.Model):
    id = models.IntegerField(primary_key=True)
    create_time = models.DateTimeField(null=True, blank=True)
    user_id = models.IntegerField(null=True, blank=True)
    session_id = models.IntegerField(null=True, blank=True)
    action = models.CharField(max_length=765, blank=True)
    context = models.CharField(max_length=1536, blank=True)
    params = models.CharField(max_length=3072, blank=True)
    class Meta:
        db_table = u'user_action'

class UserAddress(models.Model):
    id = models.IntegerField(primary_key=True)
    create_time = models.DateTimeField(null=True, blank=True)
    update_time = models.DateTimeField(null=True, blank=True)
    user_id = models.IntegerField(null=True, blank=True)
    desc = models.TextField(blank=True)
    name = models.CharField(max_length=765)
    institution = models.CharField(max_length=765, blank=True)
    address = models.CharField(max_length=765)
    city = models.CharField(max_length=765)
    state = models.CharField(max_length=765)
    postal_code = models.CharField(max_length=765)
    country = models.CharField(max_length=765)
    phone = models.CharField(max_length=765, blank=True)
    deleted = models.IntegerField(null=True, blank=True)
    purged = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'user_address'

class UserGroupAssociation(models.Model):
    id = models.IntegerField(primary_key=True)
    user_id = models.IntegerField(null=True, blank=True)
    group_id = models.IntegerField(null=True, blank=True)
    create_time = models.DateTimeField(null=True, blank=True)
    update_time = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'user_group_association'

class UserPreference(models.Model):
    id = models.IntegerField(primary_key=True)
    user_id = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=765, blank=True)
    value = models.CharField(max_length=3072, blank=True)
    class Meta:
        db_table = u'user_preference'

class UserQuotaAssociation(models.Model):
    id = models.IntegerField(primary_key=True)
    user_id = models.IntegerField(null=True, blank=True)
    quota_id = models.IntegerField(null=True, blank=True)
    create_time = models.DateTimeField(null=True, blank=True)
    update_time = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'user_quota_association'

class UserRoleAssociation(models.Model):
    id = models.IntegerField(primary_key=True)
    user_id = models.IntegerField(null=True, blank=True)
    role_id = models.IntegerField(null=True, blank=True)
    create_time = models.DateTimeField(null=True, blank=True)
    update_time = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'user_role_association'

class ValidationError(models.Model):
    id = models.IntegerField(primary_key=True)
    dataset_id = models.IntegerField(null=True, blank=True)
    message = models.CharField(max_length=765, blank=True)
    err_type = models.CharField(max_length=192, blank=True)
    attributes = models.TextField(blank=True)
    class Meta:
        db_table = u'validation_error'

class Visualization(models.Model):
    id = models.IntegerField(primary_key=True)
    create_time = models.DateTimeField(null=True, blank=True)
    update_time = models.DateTimeField(null=True, blank=True)
    user_id = models.IntegerField()
    latest_revision_id = models.IntegerField(null=True, blank=True)
    title = models.TextField(blank=True)
    type = models.TextField(blank=True)
    deleted = models.IntegerField(null=True, blank=True)
    importable = models.IntegerField(null=True, blank=True)
    slug = models.TextField(blank=True)
    published = models.IntegerField(null=True, blank=True)
    dbkey = models.TextField(blank=True)
    class Meta:
        db_table = u'visualization'

class VisualizationAnnotationAssociation(models.Model):
    id = models.IntegerField(primary_key=True)
    visualization_id = models.IntegerField(null=True, blank=True)
    user_id = models.IntegerField(null=True, blank=True)
    annotation = models.TextField(blank=True)
    class Meta:
        db_table = u'visualization_annotation_association'

class VisualizationRatingAssociation(models.Model):
    id = models.IntegerField(primary_key=True)
    visualization_id = models.IntegerField(null=True, blank=True)
    user_id = models.IntegerField(null=True, blank=True)
    rating = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'visualization_rating_association'

class VisualizationRevision(models.Model):
    id = models.IntegerField(primary_key=True)
    create_time = models.DateTimeField(null=True, blank=True)
    update_time = models.DateTimeField(null=True, blank=True)
    visualization_id = models.IntegerField()
    title = models.TextField(blank=True)
    config = models.TextField(blank=True)
    dbkey = models.TextField(blank=True)
    class Meta:
        db_table = u'visualization_revision'

class VisualizationTagAssociation(models.Model):
    id = models.IntegerField(primary_key=True)
    visualization_id = models.IntegerField(null=True, blank=True)
    tag_id = models.IntegerField(null=True, blank=True)
    user_id = models.IntegerField(null=True, blank=True)
    user_tname = models.CharField(max_length=765, blank=True)
    value = models.CharField(max_length=765, blank=True)
    user_value = models.CharField(max_length=765, blank=True)
    class Meta:
        db_table = u'visualization_tag_association'

class VisualizationUserShareAssociation(models.Model):
    id = models.IntegerField(primary_key=True)
    visualization_id = models.IntegerField(null=True, blank=True)
    user_id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'visualization_user_share_association'

class Workflow(models.Model):
    id = models.IntegerField(primary_key=True)
    create_time = models.DateTimeField(null=True, blank=True)
    update_time = models.DateTimeField(null=True, blank=True)
    stored_workflow_id = models.IntegerField()
    name = models.TextField(blank=True)
    has_cycles = models.IntegerField(null=True, blank=True)
    has_errors = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'workflow'

class WorkflowInvocation(models.Model):
    id = models.IntegerField(primary_key=True)
    create_time = models.DateTimeField(null=True, blank=True)
    update_time = models.DateTimeField(null=True, blank=True)
    workflow_id = models.IntegerField()
    class Meta:
        db_table = u'workflow_invocation'

class WorkflowInvocationStep(models.Model):
    id = models.IntegerField(primary_key=True)
    create_time = models.DateTimeField(null=True, blank=True)
    update_time = models.DateTimeField(null=True, blank=True)
    workflow_invocation_id = models.IntegerField()
    workflow_step_id = models.IntegerField()
    job_id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'workflow_invocation_step'

class WorkflowOutput(models.Model):
    id = models.IntegerField(primary_key=True)
    workflow_step_id = models.IntegerField()
    output_name = models.CharField(max_length=765, blank=True)
    class Meta:
        db_table = u'workflow_output'

class WorkflowStep(models.Model):
    id = models.IntegerField(primary_key=True)
    create_time = models.DateTimeField(null=True, blank=True)
    update_time = models.DateTimeField(null=True, blank=True)
    workflow_id = models.IntegerField()
    type = models.CharField(max_length=192, blank=True)
    tool_id = models.TextField(blank=True)
    tool_version = models.TextField(blank=True)
    tool_inputs = models.TextField(blank=True)
    tool_errors = models.TextField(blank=True)
    position = models.TextField(blank=True)
    config = models.TextField(blank=True)
    order_index = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'workflow_step'

class WorkflowStepAnnotationAssociation(models.Model):
    id = models.IntegerField(primary_key=True)
    workflow_step_id = models.IntegerField(null=True, blank=True)
    user_id = models.IntegerField(null=True, blank=True)
    annotation = models.TextField(blank=True)
    class Meta:
        db_table = u'workflow_step_annotation_association'

class WorkflowStepConnection(models.Model):
    id = models.IntegerField(primary_key=True)
    output_step_id = models.IntegerField(null=True, blank=True)
    input_step_id = models.IntegerField(null=True, blank=True)
    output_name = models.TextField(blank=True)
    input_name = models.TextField(blank=True)
    class Meta:
        db_table = u'workflow_step_connection'

class WorkflowStepTagAssociation(models.Model):
    id = models.IntegerField(primary_key=True)
    workflow_step_id = models.IntegerField(null=True, blank=True)
    tag_id = models.IntegerField(null=True, blank=True)
    user_id = models.IntegerField(null=True, blank=True)
    user_tname = models.CharField(max_length=765, blank=True)
    value = models.CharField(max_length=765, blank=True)
    user_value = models.CharField(max_length=765, blank=True)
    class Meta:
        db_table = u'workflow_step_tag_association'

class WorkflowTagAssociation(models.Model):
    id = models.IntegerField(primary_key=True)
    workflow_id = models.IntegerField(null=True, blank=True)
    tag_id = models.IntegerField(null=True, blank=True)
    user_id = models.IntegerField(null=True, blank=True)
    user_tname = models.CharField(max_length=765, blank=True)
    value = models.CharField(max_length=765, blank=True)
    user_value = models.CharField(max_length=765, blank=True)
    class Meta:
        db_table = u'workflow_tag_association'


        

    