# SourceCode / Firmiana Frontend
Firmiana Frontend directory contains source code of Firmiana website, which consits of five directories: experiments, gardener, javascript, leafy and repository.

Based on Django web framework, a Django project called "leafy" was created, which includs database configuration, Django-specific options and application-specific settings. And then three applications (experiments, gardener and repository) were created and installed into 'leafy' project. 'experiments' resposes the request of experimental metadata and 'gardener' responses the request of the request of experimental results. The third application called repository is used for responsing the request of data repository module.  
In the directory of 'Firmiana', 'javascript' directory contains all scripts that are used for implementing frontend interface of Firmiana based on Extjs framework.

* leafy: a Django project that initializes development of Firmiana. The directoty contains main functional scripts as follow:
  - admin.py: Registering existed models in leafy.models.
  - authority_trans.py: Setting of authority.
  - forms.py: Form operations of logging in Firmiana.
  - models.py: An auto-generated Django model module used for access control.
  - password_trans.py: Custom encryption function on accounts in Firmiana.
  - settings.py: Settings/configuration for Django projec of Firmiana.
  - urls.py: The URL declarations for Django project of Firmiana.
  - views.py: Functional respone modules used for proccessing external requests, including registeration, login and so on.
  - wsgi.py: An entry-point for WSGI-compatible web servers to serve Firmiana.
  

* experiments: an application that responses the request of experimental metadata of Firmiana. The directoty contains main functional scripts as follow:
  - admin.py: Registering existed models in experiments.models.
  - experiments_filters.py: Custom functions script used for filtering out experiments complying with specific filters.
  - manageChildAccount.py
  - models.py
  - password_trans.py
  - urls.py
  - views.py
 
