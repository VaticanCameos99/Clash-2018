from django.contrib import admin
from accounts.models import UserProfile, MCQ, Question_list
from django.contrib.auth.models import User
# Register your models here.
admin.site.register(UserProfile)
admin.site.register(MCQ)
admin.site.register(Question_list)

