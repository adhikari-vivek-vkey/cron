# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Profile, AccountDetail, LoanDetail, UserStatu

# Register your models here.
admin.site.register(Profile)
admin.site.register(AccountDetail)
admin.site.register(LoanDetail)
admin.site.register(UserStatu)
