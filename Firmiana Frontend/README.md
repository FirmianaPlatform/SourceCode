# SourceCode / Firmiana Frontend
Firmiana Frontend directory contains source code of Firmiana website, which consits of five directories: experiments, gardener, javascript, leafy and repository.

Based on Django web framework, a Django project called "leafy" was created, which includs database configuration, Django-specific options and application-specific settings. And then three applications (experiments, gardener and repository) were created and installed into 'leafy' project. 'experiments' resposes the request of experimental metadata and 'gardener' responses the request of the request of experimental results. The third application called repository is used for responsing the request of data repository module.  
In the directory of 'Firmiana', 'javascript' directory contains all scripts that are used for implementing frontend interface of Firmiana based on Extjs framework.

* leafy:  a Django project that initializes development of Firmiana.The directoty contains:
  - admin.py
  - authority_trans.py
  - config.py
  - forms.py
  - manage.py
  - models.py
  - password_trans.py
  - settings.py
  - urls.py
  - views.py
  - wsgi.py
