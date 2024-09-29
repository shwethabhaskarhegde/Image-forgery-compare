"""Image_forgery_detection URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from detection import views
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    url('^index', views.index, name="index"),
    url('^insertreg', views.insertreg, name="insertreg"),
    url('^logcheck', views.logcheck, name="logcheck"),
    url('^send_email', views.send_email, name="send_email"),
    url('^showuser', views.showuser, name="showuser"),
    url('^fileupload', views.fileupload, name="fileupload"),
    url('^deluser(?P<pk>\d+)/$', views.deluser, name="deluser"),
    url('^image_upload', views.image_upload, name="image_upload"),
    url('^showimage', views.showimage, name="showimage"),
    url('^viewimage', views.viewimage, name="viewimage"),
    url('^change_pass', views.change_pass, name="change_pass"),
    url('^uchange_pass', views.uchange_pass, name="uchange_pass"),
    url('^userhome', views.userhome, name="userhome"),
    url('^adminhome', views.adminhome, name="adminhome"),
    url('^feedback', views.feedback, name="feedback"),
    url('^showfeedback', views.showfeedback, name="showfeedback"),
    url('^delshowimg(?P<pk>\d+)/$', views.delshowimg, name="delshowimg"),
    url('^delviewimg(?P<pk>\d+)/$', views.delviewimg, name="delviewimg"),
    # url('^compare(P<oimage>\w+)/(P<uimage>\w+)/$', views.compare, name="compare"),
    url('^compare(<string:oimage>)/(<string:uimage>)/$', views.compare, name="compare"),

url('^selectimage(?P<pk>\d+)/$', views.selectimage, name="selectimage"),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

