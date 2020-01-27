# ilter(user=request.user, repayment_status__lte=1, disbursement_status__gte=1).count()
from django.utils import timezone
# call_feedback.objects.filter(date__gte='2020-01-17', date__lte='2020-01-25').values('date')
# orderId = "CDXO" + timezone.localtime(timezone.now()).strftime("%d%m%Y") + str(request.user.id) + str(Loans.objects.filter(user=request.user).count())

from datetime import timedelta
from data.models import Profile, LoanDetail, AccountDetail
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.decorators import api_view

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

# send_message(d)
# 'id': 2, 'user_id': 3, 'loan_date': datetime.datetime(2020, 1, 4, 7, 10, 21, tzinfo=<UTC>), 'loan_amount': 2000, 'status': 0
d = []
def info(request):
    a = Profile.objects.filter(id=1).values('number', 'ref_name', 'ref_number')
    b = AccountDetail.object.filter(id=1).values('account')

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
            print(d)
            a += 1
            if len(data) == a:
                return Response({'data': data}, 200)
    else:
        return Response({'error': 'no data filter'}, 400)

