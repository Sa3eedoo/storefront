from django.core.mail import send_mail, mail_admins, BadHeaderError, EmailMessage
from django.shortcuts import render
from templated_mail.mail import BaseEmailMessage


def say_hello(request):
    try:
        send_mail('subject', 'message', 'from2@admin.com', ['ms@customer.com'])
        mail_admins('subject', 'messsage', html_message='message')

        message = EmailMessage('subject', 'message',
                               'from2@admin.com', ['ms@customer.com'])
        message.attach_file('playground/static/images/panda.jpg')
        message.send()

        message = BaseEmailMessage(
            template_name='emails/hello.html',
            context={'name': 'Mahmoud'}
        )
        message.send(['ms@customer.com'])
    except BadHeaderError:
        pass
    return render(request, 'hello.html', {'name': 'Saeed'})
