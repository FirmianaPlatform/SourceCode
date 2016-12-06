'''
Created on 2016.4.10

@author: MS_zdd
'''
from experiments.models import *

def importIntoExperimentTable(experimentId):
    experiment = Experiment.objects.all().filter(id=experimentId)[0]
    (workflowMode, workflowMode_sign) = Workflow_mode.objects.get_or_create(name="Mascot")
    experiment.workflowMode = workflowMode
    experiment.save()


def importIntoMascot_modeTable(experimentId):
    (missedCleavagesAllowed, missedCleavagesAllowed_sign) = Mascot_mode_missedCleavagesAllowed.objects.get_or_create(name='2')
    (mascotEnzyme, mascotEnzyme_sign) = Mascot_mode_mascotEnzyme.objects.get_or_create(name='Trypsin')
    (peptideCharge, peptideCharge_sign) = Mascot_mode_peptideCharge.objects.get_or_create(name='2+, 3+ and 4+')
    (precursorSearchType, precursorSearchType_sign) = Mascot_mode_precursorSearchType.objects.get_or_create(name='Monoisotopic')
    mascotMode = Mascot_mode(experimentId = experimentId, missedCleavagesAllowed = missedCleavagesAllowed, mascotEnzyme = mascotEnzyme, peptideCharge = peptideCharge, precursorSearchType = precursorSearchType)
    mascotMode.save()

def importExperimentalfdr_infoTable(experimentId):
    experimentalFDR_level = "Protein"
    experimentalFDR_value = 0.01
    experimentalFDR_info = Experimentalfdr_info(experimentId=experimentId, experimentalFDR_level=experimentalFDR_level, experimentalFDR_value=experimentalFDR_value)
    experimentalFDR_info.save()

def __main__():
    
#     testNoList = range(5398, 5401)
#     for experimentId in testNoList:
#         importExperimentalfdr_infoTable(experimentId)
#         importIntoMascot_modeTable(experimentId)
#         importIntoExperimentTable(experimentId)
    print 'start'
    explist = Experiment.objects.all()
    for exp in explist:
        experimentId = exp.id
        if experimentId < 5398:
            importExperimentalfdr_infoTable(experimentId)
            importIntoMascot_modeTable(experimentId)
            importIntoExperimentTable(experimentId)
    print 'end'
        
        
    