
from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from forms import RegistrationForm, VerificationForm
from .models import User
from twilio.rest import Client
# from django_otp.models import Device
# from django_otp.oath import TOTP

# Create your views here.
def otp_register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        account_sid = 'ACb78b2fd3a07bfb51bc243bbc8b1a08f5' # Found on Twilio Console Dashboard
        auth_token = 'd3892a335ca6e3a1a1d6dc80dddb81b8' # Found on Twilio Console Dashboard
         # Phone number you used to verify your Twilio account
        TwilioNumber = '+13182257674' # Phone number given to you by Twilio
        client = Client(account_sid, auth_token)        
        if form.is_valid():
            user = form.save()
            phone_number = form.cleaned_data.get('phone_number')
            token_number = user.token_number
            if user.id:
                client.api.account.messages.create(
                        to=phone_number,
                        from_=TwilioNumber,
                        body='I sent a text message from Python!'+str(token_number))
                # user.twiliosmsdevice_set.create(name='SMS',key=token_number, number=phone_number)
                # device = user.twiliosmsdevice_set.get()
                # device.generate_challenge()
            return HttpResponseRedirect('/otp/verify/'+str(user.id))
    else:
        form = RegistrationForm()
    context = {}
    context.update(csrf(request))
    context['form'] = form
    return render_to_response('register.html', context)

def otp_login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            if request.POST.get('next') != 'None':
                return HttpResponseRedirect(request.POST.get('next'))
            return HttpResponse('User ' + user.username + ' is logged in.' +
                                '<p>Please <a href="/otp/status/">click here</a> to check verification status.</p>')
        else:
            return HttpResponse('User is invalid!' +
                                '<p>Please <a href="/otp/login/">click here</a> to login.</p>')
    else:
        form = AuthenticationForm()
    context = {}
    context['next'] = request.GET.get('next')
    context.update(csrf(request))
    context['form'] = form
    return render_to_response('login.html', context)

@login_required(login_url='/otp/login')
def otp_verify(request,pk):
    user_data = User.objects.filter(pk=pk)[0]
    username = user_data.username
    token_number = user_data.token_number
    if request.method == 'POST':
        form = VerificationForm(request.POST)
        token = form.getToken()

        if token:
            user = User.objects.get_by_natural_key(request.user.username)
            # token_number = form.cleaned_data.get('token_number')
            # device = user.twiliosmsdevice_set.get()
            # device = django_otp.devices_for_user(user)
            if user:
                # status = device.verify_token(token)
                # if status:
                if int(token_number) == int(token):
                    user.is_verified = True
                    user.save()
                    return HttpResponse('User: ' + username + '\n' + 'Verified.' +
                                        '<p>Please <a href="/otp/logout/">click here</a> to logout.</p>')
                else:
                    return HttpResponse('User: ' + username + '\n' + 'could not be verified.' +
                                        '<p><a href="/otp/verify/'+str(pk)+'">Click here to generate new token</a></P>')
            else:
                return HttpResponse('User: ' + username + ' Worng token!' +
                                    '<p><a href="/otp/verify/'+str(pk)+'">Click here to generate new token</a></P>')
    else:
        form = VerificationForm()
    context = {}
    context.update(csrf(request))
    context['form'] = form
    return render_to_response('verify.html', context)

@login_required(login_url='/otp/login')
def otp_token(request):
    user = User.objects.get_by_natural_key(request.user.username)
    # device = user.twiliosmsdevice_set.get()
    # device.generate_challenge()
    return HttpResponseRedirect('/otp/verify')
    
def otp_status(request):
    if request.user.username:
        user = User.objects.get_by_natural_key(request.user.username)
        if user.is_verified:
            return HttpResponse(user.username + ' is verified.' +
                                '<p>Please <a href="/otp/logout/">click here</a> to logout.</p>')
        else:
            return HttpResponse(user.username + ' is not verified.' +
                                '<p><a href="/otp/verify/'+str(user.id)+'">Click here to generate new token</a></P>')
    return HttpResponse('<p>Please <a href="/otp/login/">login</a> to check verification status.</p>')

def otp_logout(request):
    logout(request)
    return HttpResponse('You are logged out.' +
                        '<p>Please <a href="/otp/login/">click here</a> to login.</p>')
