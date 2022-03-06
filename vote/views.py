from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from vote.forms import VoterForm
from vote.models import County, Constituency, Ward


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
            return render(request, "vote/admin/dashboard.html", context)

        else:
            messages.error(request, messages.ERROR, "Your Username or Password is incorrect")

    return render(request, 'vote/admin/login.html')


def log_out(request):
    logout(request)
    messages.success(request, "You have been Logged Out Successfully!")
    return render(request, 'vote/admin/logout.html')


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


def constituency_detail(request):
    county = County.objects.all()
    context = {'county': county}
    if request.method == "POST":
        constituency_code = request.POST['constituency_code']
        constituency_name = request.POST['constituency_name']
        county_code = request.POST['county_code']

        myconstituency = Constituency.objects.create(constituency_code=constituency_code,
                                                     constituency_name=constituency_name,
                                                     county_code_id=county_code
                                                     )

        myconstituency.constituency_code = constituency_code
        myconstituency.constituency_name = constituency_name
        myconstituency.county_code_id = county_code

        myconstituency.save()

        messages.success(request, "Constituency added successfully.")

        return redirect('vote:constituency_list')

    return render(request, 'vote/admin/constituency_detail.html', context)


def constituency_list(request):
    constituency = Constituency.objects.all()
    context = {'constituency': constituency, }
    return render(request, 'vote/admin/constituency_list.html', context)


def ward_detail(request):
    constituency = Constituency.objects.all()
    context = {'constituency': constituency}
    if request.method == "POST":
        ward_code = request.POST['ward_code']
        ward_name = request.POST['ward_name']
        constituency_code = request.POST['constituency_code']

        myward = Ward.objects.create(ward_code=ward_code,
                                     ward_name=ward_name,
                                     constituency_code_id=constituency_code
                                     )

        myward.ward_code = ward_code
        myward.ward_name = ward_name
        myward.constituency_code_id = constituency_code

        myward.save()

        messages.success(request, "Ward added successfully.")

        return redirect('vote:ward_list')

    return render(request, 'vote/admin/ward_detail.html', context)


def ward_list(request):
    ward = Ward.objects.all()
    context = {'ward': ward, }
    return render(request, 'vote/admin/ward_list.html', context)


def voter_list(request):
    return render(request, 'vote/admin/voter_list.html')


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


def auth(request):
    return render(request, 'vote/user/auth.html')


def auth2(request):
    return render(request, 'vote/user/auth2.html')


def auth3(request):
    return render(request, 'vote/user/auth3.html')
