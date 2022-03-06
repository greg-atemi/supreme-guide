from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from vote.forms import VoterForm, CountyForm
from vote.models import Voter, County


def index(request):
    return render(request, 'vote/user/index.html')


def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname

        myuser.save()

        messages.success(request, "Your Account has been created successfully.")

        return redirect('vote:login')

    return render(request, 'vote/admin/signup.html')


def county_detail(request):
    if request.method == "POST":
        county_code = request.POST['county_code']
        county_name = request.POST['county_name']

        mycounty = County.objects.create(county_code=county_code, county_name=county_name)
        mycounty.county_code = county_code
        mycounty.county_name = county_name

        mycounty.save()

        messages.success(request, "County added successfully.")

        return redirect('vote:county_list')

    return render(request, 'vote/admin/county_detail.html')


def county_list(request):
    county = County.objects.all()
    context = {'county': county, }
    return render(request, 'vote/admin/county_list.html', context)


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username=username, password=pass1)

        if user is not None:
            auth_login(request, user)
            fname = user.first_name
            lname = user.last_name
            context = {
                'fname': fname, 'lname': lname
            }
            messages.success(request, "Login Successful.")
            # return redirect("/vote/dashboard", context)
            return render(request, "vote/admin/dashboard.html", context)

        else:
            messages.error(request, messages.ERROR, "Your Username or Password is incorrect")
            # return redirect('/')

    return render(request, 'vote/admin/login.html')


def log_out(request):
    logout(request)
    messages.success(request, "You have been Logged Out Successfully!")
    return render(request, 'vote/admin/logout.html')


@login_required
def dashboard(request):
    return render(request, 'vote/admin/dashboard.html')


def bio(request):
    return render(request, 'vote/user/bio.html')


def location(request):
    return render(request, 'vote/user/location.html')


def photo(request):
    return render(request, 'vote/user/photo.html')


def success(request):
    return render(request, 'vote/user/success.html')


def confirmation(request):
    return render(request, 'vote/user/confirmation.html')


def voter_list(request):
    return render(request, 'vote/admin/voter_list.html')


def constituency_list(request):
    return render(request, 'vote/admin/constituency_list.html')


def ward_list(request):
    return render(request, 'vote/admin/ward_list.html')


@login_required
def create_voter(request):
    form = VoterForm()
    if request.method == 'POST':
        form = VoterForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = VoterForm()

    return render(request, 'vote/admin/create_voter.html', {"form": form})


def constituency_detail(request):
    return render(request, 'vote/admin/constituency_detail.html')


def ward_detail(request):
    return render(request, 'vote/admin/ward_detail.html')


def auth(request):
    return render(request, 'vote/user/auth.html')


def auth2(request):
    return render(request, 'vote/user/auth2.html')


def auth3(request):
    return render(request, 'vote/user/auth3.html')
