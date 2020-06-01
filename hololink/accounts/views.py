from django.shortcuts import HttpResponse, render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from .forms import SignUpWithEmailForm
import uuid


def sign_up_with_email(request): 
    if request.method == 'POST': 
        form = SignUpWithEmailForm(request.POST) 
        if form.is_valid():
            user = form.save(commit=False)
            email = form.cleaned_data.get('email')
            username = email[0:email.index('@')]
            user.username = username
            random_uuid_password = uuid.uuid4().hex[0:6]
            user.set_password(random_uuid_password)
            user.save()
            # send a random uuid password email
            recipient = f'{email}'
            subject = "[Hololink] You have created an account."
            try:
                if '_' in username:
                    username_readable = ' '.join([ word[0].upper() + word[1:] for word in username.split('_') ])
                else:
                    username_readable = username
            except:
                username_readable = username
            message = f'Hi {username_readable},'
            message += '\n\nYou have created a new account on Hololink. You could login and change it on Hololink later.'
            message += f'\n\nYour account: {username}'
            message += f'\nYour password: {random_uuid_password}'
            message += '\n\nSincerely,'
            message += '\nHololink'
            send_password_email(
                subject=subject,
                message=message,
                recipient=recipient,
            )
            return redirect('/accounts/password_reset/done/')
    else: 
        form = SignUpWithEmailForm()
    context = {
        'form': form,
    }
    return render(request, 'registration/sign_up_with_email.html', context) 

# a email-sending script, not a view
def send_password_email(subject, message, recipient):
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient],
            fail_silently=False,
        )
    except:
        pass

# This is not used now.
def sign_up(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = UserCreationForm()
    context = {
        'form': form,
    }
    return render(request, 'registration/sign_up.html', context)
