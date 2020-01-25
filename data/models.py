# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.




class UserData(models.Model):
    user = models.CharField(max_length=150)
    number = models.IntegerField()
    account = models.IntegerField()
    loan_amount = models.IntegerField()
    status = models.IntegerField()
    date = models.DateField()
    ref_name = models.CharField(max_length=150)
    ref_number = models.IntegerField()
    def __str__(self):
        return '{} id {} name'.format(self.id, self.user)
# UserData.objects.create(user='vivek',number='9968038609', account ='123456789',loan_amount='1000',status='0',ref_name='suraj',ref_number='9968888888')