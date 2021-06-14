"""forum URL Configuration

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
from forumapp import views
from login import views as loginviews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home, name='home'),
    #path('test',views.test, name='test'),
    path('signup',loginviews.signup, name='signup'),
    path('login',loginviews.login, name ='login'),
    path('logout', loginviews.logout, name = 'logout'),
    path('thread/<int:my_id>',views.thread, name = 'thread'),
    path('thread/<int:my_id>/create',views.create, name ='create'),
    path('thread/<int:thread_ids>/<int:topic_ids>/view',views.discussion, name='discussion'),
    path('delete/<int:thread_id>/<int:topic_id>',views.delete_topic , name='delete_topic'),
    path('delete/<int:thread_id>/<int:topic_id>/<int:comment_id>',views.delete_comment , name='delete_comment')

]
