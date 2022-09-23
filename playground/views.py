from django.core.mail import send_mail, mail_admins, BadHeaderError, EmailMessage
from django.shortcuts import render


def say_hello(request):
    try:
        send_mail('subject', 'message', 'from2@admin.com', ['ms@customer.com'])
        mail_admins('subject', 'messsage', html_message='message')

        message = EmailMessage('subject', 'message',
                               'from2@admin.com', ['ms@customer.com'])
        message.attach_file('playground/static/images/panda.jpg')
        message.send()
    except BadHeaderError:
        pass
    return render(request, 'hello.html', {'name': 'Saeed'})
