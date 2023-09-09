
from django.core.mail import send_mail
from django.http import HttpResponse
from django.conf import settings
from celery import shared_task


@shared_task
def order_created(request):
    subject = 'welcome to GFG world'
    message = 'Hi mario, thank you for registering in geeksforgeeks.'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ["spceissimo@gmail.com", ]
    send_mail(subject, message, email_from, recipient_list)
    return HttpResponse("mail inviata !")
