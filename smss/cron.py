from . import settings
from django.core.mail import send_mail
from data.Newmessage import send_message
# import cronjobs

to = 'harshroy603@gmail.com'


def my_scheduled_job():
    send_mail('Celery Task Worked!', 'This is proof the task worked!', settings.DEFAULT_FROM_EMAIL, [to])


# @cronjobs.register
# def periodic_task():
#     print('hello')
#     send_mail('Celery Task Worked!', 'This is proof the task worked!', settings.DEFAULT_FROM_EMAIL, [to])

# from cronjobs import register
# @register(lock=False)
# def my_cron_job():
#     # Multiple instances of me can run simultaneously.