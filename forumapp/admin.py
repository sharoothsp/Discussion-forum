from django.contrib import admin

from .models import Mainthread, Subthread, Comment

admin.site.register(Mainthread)
admin.site.register(Subthread)
admin.site.register(Comment)
