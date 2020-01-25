from . import settings
from django.core.mail import send_mail
from data.Newmessage import send_message
# import cronjobs

to = 'harshroy603@gmail.com'


def my_scheduled_job():
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

    send_message(d)
    send_mail('Celery Task Worked!', 'This is proof the task worked!', settings.DEFAULT_FROM_EMAIL, [to])


# @cronjobs.register
# def periodic_task():
#     print('hello')
#     send_mail('Celery Task Worked!', 'This is proof the task worked!', settings.DEFAULT_FROM_EMAIL, [to])

# from cronjobs import register
# @register(lock=False)
# def my_cron_job():
#     # Multiple instances of me can run simultaneously.