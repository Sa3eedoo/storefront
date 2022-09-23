from django.core.mail import send_mail, mail_admins, BadHeaderError
from django.shortcuts import render


def say_hello(request):
    try:
        send_mail('subject', 'message', 'from2@admin.com', ['ms@customer.com'])
        mail_admins('subject', 'messsage', html_message='message')
    except BadHeaderError:
        pass
    return render(request, 'hello.html', {'name': 'Saeed'})
