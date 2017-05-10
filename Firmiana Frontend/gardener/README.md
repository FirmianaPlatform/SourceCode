# SourceCode/Firmiana Frontend/gardener/
gardener: an application that responses the request from experimental results of Firmiana. The directoty contains main directories and functional scripts as follow:
  - scripts/R: A R scripts collection used for providing common bioinformatics analysis tools. 
  - cal_area.py: A functional script for protein quantification.
  - firmianaLib.py: Custom functions script used for filtering out experiments complying with specific filters.
  - genome.py: Custom functional script used for mappint proteome results to genome.
  - mascotDatParser.py: Custom functional script used for parsering data from Mascot.
  - models.py: A custom Django model module used for ralating to experimental results.
  - pathway.py: Custom functional scripts used for executing R scripts.
  - qc.py: Custom functional script used for quality control of experiments.
  - sqlFunc.py: Custom functional script used for connecting database of Firmiana.
  - urls.py: The URL declarations for Django application called gardener.
  - views.py: Functional respone modules used for proccessing external requests that achieve experimental results.
