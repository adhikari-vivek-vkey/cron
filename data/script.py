from datetime import timedelta
from data.models import Profile, LoanDetail, AccountDetail
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .Newmessage import send_message
d = {
    'contact_no': 9968038609,
    'loan_amount': 1000,
    'paid_status': "0",
    'disbursal_date': '2020-01-13',
    'users_name': "hello",
    'ref_number': 7065119155,
    'ref_name': "references",
    'account_number': 123444454,
}

d = []


def info(request):
    profile = Profile.objects.filter(user__username='aman').values('number', 'ref_name', 'ref_number')[0]
    acc = AccountDetail.object.filter(user__username='aman').values('account')[0]
    loan = LoanDetail.objects.filter(user__username='aman').values('loan_date', 'loan_amount', 'status')[0]
    data = {
        'users_name': profile['name'],
        'contact_no': profile['number'],
        'loan_amount': loan['loan_amount'],
        'paid_status': loan['status'],
        'disbursal_date': loan['disbursal_date'],
        'ref_number': profile['ref_number'],
        'ref_name': profile['ref_name'],
        'account_number': acc['account'],
    }
    send_message(data)


@api_view(['POST'])
def DaySMS(request):
    FilterDate = str(timezone.now().date() - timedelta(days=10))
    print(FilterDate)
    data = LoanDetail.objects.filter(loan_date__lte=FilterDate + ' 00:00:00', status__lte=1).values()
    print(data)
    if data:
        a = 0
        for i in data:
            d.append(i)
            a += 1
            if len(data) == a:
                return Response({'data': data}, 200)
    else:
        return Response({'error': 'no data filter'}, 400)
