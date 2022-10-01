from django.shortcuts import render
from .tasks import notify_custmoers


def say_hello(request):
    notify_custmoers.delay('Hello')
    return render(request, 'hello.html', {'name': 'Saeed'})
