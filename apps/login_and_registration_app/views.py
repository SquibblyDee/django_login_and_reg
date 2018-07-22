from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib import messages

import bcrypt

#  import our db
from .models import User

def index(request):
    return render(request,'login_and_registration_app/index.html')

def process_register(request, methods=['POST']):
    # pass the post data to the method we wrote and save the response in a variable called errors
    errors = User.objects.register_validator(request.POST)
    # check if the errors object has anything in it
    if len(errors):
        # if the errors object contains anything, loop through each key-value pair and make a flash message
        for key, value in errors.items():
            messages.error(request, value)
            print("WEVE HIT AN ERROR")
        # redirect the user back to the form to fix the errors
        return redirect('/', id)
    else:
        # if the errors object is empty, that means there were no errors!
        # add our new record to the table , push what we need to session,
        # and redirect to /success to render our final page
        User.objects.create(first_name=request.POST['input_first_name'], last_name=request.POST['input_last_name'], email=request.POST['input_email'], password=bcrypt.hashpw(request.POST['input_password'].encode('utf8'), bcrypt.gensalt()))
        request.session['user_id'] = User.objects.last().id
        request.session['isloggedin'] = True
        request.session['welcomename'] = request.POST['input_first_name']
        request.session['welcomemessage'] = 'Successfully registered!'
        return redirect('/success')

def process_login(request, methods=['POST']):
    #check for errors returned by our login_validator
    login_errors = User.objects.login_validator(request.POST)
    if len(login_errors):
        for key, value in login_errors.items():
            messages.error(request, value)
            print("WEVE HIT AN ERROR")
        # redirect the user back to the form to fix the errors
        return redirect('/', id)
    else:
    # Query the data we need
        query = User.objects.all().values('id', 'email', 'first_name', 'password')
        # Iterate through query until we find user email then verify password is legit
        for row in query:
            if row['email'] == request.POST['login_email'] and bcrypt.checkpw(request.POST['login_password'].encode(), row['password'].encode()): 
                request.session['isloggedin'] = True
                request.session['user_id'] = row['id']
                request.session['welcomename'] = row['first_name']
                request.session['welcomemessage'] = 'Successfully logged in!'
                return redirect('/success')
    
    #return redirect('/')

def success(request):
    # If the user has a isLoggedin session 
    if 'isloggedin' in request.session and request.session['isloggedin'] == True:
        return render(request, 'login_and_registration_app/success.html')
    else:
        return redirect('/')
