from django.conf.urls.defaults import patterns, include, url
from leafy.views import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'firmiana.views.home', name='home'),
    # url(r'^firmiana/', include('firmiana.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^gardener/', include('gardener.urls')),
    url(r'^ispec/', include('ispec.urls')),
    url(r'^gardener_dev/', include('gardener_dev.urls')),
    url(r'^dataProcess/', include('dataProcess.urls')),
    url(r'^dataViewer/', include('dataViewer.urls')),
    url(r'^repository/', include('repository.urls')),
    
    # repository
    url(r'^repos/printHelloWorld_test/$', 'repository.views.printHelloWorld_test'),
    
    url(r'^repos/addAProjectRecord/$', 'repository.views.addAProjectRecord'),
    url(r'^repos/showAllProjects/$', 'repository.views.showAllProjectsByUserId'),
    url(r'^repos/getProjectStatus/$', 'repository.views.getProjectStatus'),
    url(r'^repos/changeProjectStatus/$', 'repository.views.changeProjectStatus_views'),
    url(r'^repos/showMetadataByPxdNo/$', 'repository.views.showMetadataByPxdNo_views'),
    url(r'^repos/updateMetadataByPxdNo/$', 'repository.views.updateMetadataForAProject_views'),
    url(r'^repos/showAllChildAccountInfoInProjectLevel/$', 'repository.views.showAllChildAccountInfo_inRepository_views'),
    url(r'^repos/sharedProjectToChild/$', 'repository.views.addChildUserSharedProject_views'),
    url(r'^repos/updateChildAccountSharedProject/$', 'repository.views.updateChildAccountSharedProject_views'),
    url(r'^repos/deleteAProjectRecord/$', 'repository.views.deleteAProjectRecord'),
    url(r'^repos/display/(.*)/$', 'repository.views.record_display'),
        
    # repository
    
    url(r'^api/', include('api.urls')),
    url(r'^responders/', include('responders.urls')),
    # url(r'^infinity/',include('infinity.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    (r'^msanalysis/', include('msanalysis.urls')),
    (r'^experiments/', include('experiments.urls')),
    (r'^display/', include('display.urls')),
    (r'^LFQuantViewer/', include('LFQuantViewer.urls')),
    (r'^$', main_page),
    (r'^contact-post/$',contact_post),
    (r'^login/$', login_page),
    (r'^loginNewDemo/$', login_page_newDemo),
    (r'^logins/$', logins),
    (r'^logout/$', logout_page),
    (r'^regist/$', register_page),
    (r'^register_success/$', register_success),
    (r'^forgetpsd/(\w+)/$', forgetpsd_valide),
    (r'^forgetpsd/$', forgetpsd),
    (r'^invite/$', invite),
    (r'^invite/success/$', invite_success),
    (r'^contact/$', contact),
    (r'^contact/thanks/$', contact_success),
    (r'^entrez/$', entrez),
    (r'^entrez/data/search$', entrez_search),
    (r'^changepassword/$', changepassword),
    (r'^visicount/$', visicount),
    (r'^runtool/$', runtool),
    (r'^runworkflow/$', runworkflow),
    (r'^showhistory/$', showhistory),
    (r'^ForGalaxy/$', ForGalaxy),
    (r'^checkError/$', galaxy_checkError),
    (r'^truncateExp/$', truncateExp),

    (r'^develop/$', developENV),
    (r'^developHomepage/$', developHomepageENV),
    
    
    (r'^getCloudFileList/$', getCloudFileList),
    (r'^getLocalFileList/$', getLocalFileList),
    
    
)

