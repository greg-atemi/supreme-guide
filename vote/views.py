from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from vote.forms import VoterForm
from vote.models import County, Constituency, Ward, Voter


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
            messages.success(request, "Login Successful.")
            return redirect('vote:dashboard')

        else:
            messages.error(request, "Your Username or Password is incorrect")

    return render(request, 'vote/admin/login.html')


def log_out(request):
    logout(request)
    messages.success(request, "You have been Logged Out Successfully!")
    return render(request, 'vote/admin/logout.html')


def dashboard(request):
    if request.user.is_authenticated:
        fname = request.user.first_name
        lname = request.user.last_name
        context = {
            'fname': fname, 'lname': lname
        }
    else:
        messages.info(request, "Login to continue")
        return redirect('vote:login')

    return render(request, 'vote/admin/dashboard.html', context)


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
    context = {
        'county': county
    }
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


def create_voter(request):
    if request.user.is_authenticated:
        ward = Ward.objects.all()
        county = County.objects.all()
        constituency = Constituency.objects.all()
        context = {
            'ward': ward,
            'county': county,
            'constituency': constituency
        }
        if request.method == "POST":
            id_serial_number = request.POST['id_serial_number']
            email = request.user.id
            first_name = request.POST['first_name']
            middle_name = request.POST['middle_name']
            surname = request.POST['surname']
            phone_number = request.POST['phone_number']
            image = request.POST['image']
            gender = request.POST['gender']
            ward_code = request.POST['ward_code']

            myvoter = Voter.objects.create(id_serial_number=id_serial_number, email_id=email, first_name=first_name,
                                           middle_name=middle_name, surname=surname, phone_number=phone_number,
                                           photo=image, gender=gender, ward_code_id=ward_code)

            myvoter.save()

            messages.success(request, "Voter added successfully.")

            return redirect('vote:voter_list')
    else:
        messages.info(request, "Login to continue")
        return redirect('vote:login')

    return render(request, 'vote/admin/create_voter.html', context)


def voter_list(request):
    if request.user.is_authenticated:
        voter = Voter.objects.all()
        user = User.objects.all()
        context = {
            'voter': voter,
            'user': user
        }
    else:
        messages.info(request, "Login to continue")
        return redirect('vote:login')

    return render(request, 'vote/admin/voter_list.html', context)


def auth(request):
    return render(request, 'vote/user/auth.html')


def auth2(request):
    return render(request, 'vote/user/auth2.html')


def auth3(request):
    return render(request, 'vote/user/auth3.html')
