from time import sleep
from celery import shared_task


@shared_task
def notify_custmoers(message):
    print('Sending 10k emails...')
    print(message)
    sleep(10)
    print('Emails were sucessfully sent!')
