# ilter(user=request.user, repayment_status__lte=1, disbursement_status__gte=1).count()
from django.utils import timezone
# call_feedback.objects.filter(date__gte='2020-01-17', date__lte='2020-01-25').values('date')
# orderId = "CDXO" + timezone.localtime(timezone.now()).strftime("%d%m%Y") + str(request.user.id) + str(Loans.objects.filter(user=request.user).count())

