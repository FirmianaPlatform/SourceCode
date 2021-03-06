# SourceCode / Firmiana Frontend
Firmiana Frontend directory contains source code of Firmiana website, which consits of five directories: experiments, gardener, javascript, leafy and repository.

Based on Django web framework, a Django project called "leafy" was created, which includs database configuration, Django-specific options and application-specific settings. And then three applications (experiments, gardener and repository) were created and installed into 'leafy' project. 'experiments' resposes the request of experimental metadata and 'gardener' responses the request of the request of experimental results. The third application called repository is used for responsing the request of data repository module.  
In the directory of 'Firmiana', 'javascript' directory contains all scripts that are used for implementing frontend interface of Firmiana based on Extjs framework.

* leafy: a Django project that initializes development of Firmiana. The directoty contains main functional scripts as follow:
  - admin.py: Registering existed models in leafy.models.
  - authority_trans.py: Setting of authority.
  - forms.py: Form operations of logging in Firmiana.
  - models.py: An auto-generated Django model module used for access control.
  - password_trans.py: Custom encryption and decryption function on accounts in Firmiana.
  - settings.py: Settings/configuration for Django projec of Firmiana.
  - urls.py: The URL declarations for Django project of Firmiana.
  - views.py: Functional respone modules used for proccessing external requests, including registeration, login and so on.
  - wsgi.py: An entry-point for WSGI-compatible web servers to serve Firmiana.
  
* experiments: an application that responses the request from experimental metadata of Firmiana. The directoty contains main functional scripts as follow:
  - admin.py: Registering existed models in experiments.models.
  - experiments_filters.py: Custom functions script used for filtering out experiments complying with specific filters.
  - manageChildAccount.py: Custom functions script used for managing sub-accounts.
  - models.py: A custom Django model module used for relating to experimental metadata.
  - password_trans.py: Custom encryption and decryption function on accounts in Firmiana.
  - urls.py: The URL declarations for Django application called experiments.
  - views.py: Functional respone modules used for proccessing external requests that managing experimental metadata.
 
* gardener: an application that responses the request from experimental results of Firmiana. The directoty contains main directories and functional scripts as follow:
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
  
* repository: an application that responses the request from data repository of Firmiana. The directoty contains main directories and functional scripts as follow:
  - models.py: A custom Django model module used for ralating to data repository.
  - repositoryProcess.py: Custom functional scripts used for executing operations of managing data repository.
  - urls.py: The URL declarations for Django application called repository.
  - views.py: Functional respone modules used for proccessing external requests from data repository operations.
  
* javascript: a directory that storing scipts that constructing frontend of Firmiana. The directoty contains main directories and functional scripts as follow:
  - boxselect/: boxselect for ExtJS 4.1, a combo box improved for multiple value querying, selection and management.
  - display/: A javascripts collections for showing mass spectrum.
  - gardener/: A javascripts collections for showing interface of main page in Firmiana.
  - register/: A javascripts collections for showing interface of registration in Firmiana.
  - repository/: A javascripts collections for showing interface of data repository in Firmiana.
  - swfobject/: A directory that stores swf plugin and the corresponding execution scripts.
  - GoogleAnalytics.js: External JS file from Google Analytics.
  - base_login_nav.js: A JS file that shows base login navigation.
  - contact.js: A JS file showing contact form.
  - invaitation.js：A JS file showing registration invaitation interface.
  - login_nav.js: A JS file that shows login navigation.

  
  

 

