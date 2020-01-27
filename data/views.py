# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views import View
from .script import DaySMS
from data.models import Profile, LoanDetail
from django.shortcuts import render
# Create your views here.


class Message(View):
    model = LoanDetail
    fields = ['user', 'loan_date', 'loan_amount', 'status']

    def post(self, request):
        return DaySMS(request)
