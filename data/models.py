# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
import django


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    number = models.BigIntegerField(unique=True)
    ref_name = models.CharField(max_length=150)
    ref_number = models.BigIntegerField()

    def __str__(self):
        return '{} id {} name'.format(self.id, self.user)


class LoanDetail(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    loan_date = models.DateTimeField(default=django.utils.timezone.now)
    loan_amount = models.IntegerField()
    status = models.IntegerField(default=0)

    def __str__(self):
        return 'id {}  user name {} Amount {} status {} date {}'.format(self.id, self.user_id, self.loan_amount,
                                                                        self.status, self.loan_date)


class UserStatu(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.IntegerField()


class AccountDetail(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account = models.TextField()
