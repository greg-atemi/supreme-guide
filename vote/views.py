from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail, EmailMessage
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from vote.models import County, Constituency, Ward, Voter
from KuraProject import settings
from vote.tokens import generate_token


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

        if User.objects.filter(username=username):
            messages.error(request, "Username already exists!!")
            return redirect('vote:signup')

        if User.objects.filter(email=email):
            messages.error(request, "Email already exists!!")
            return redirect('vote:signup')

        if pass1 != pass2:
            messages.error(request, "Passwords do not match")
            return redirect('vote:signup')

        if not pass1.isalnum():
            messages.error(request, "Password must contain both letters and numbers")
            return redirect('vote:signup')

        if len(pass1) < 7:
            messages.error(request, "Password must contain at least 8 characters")
            return redirect('vote:signup')

        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.is_active = False

        myuser.save()

        messages.success(request, "Your Account has been created successfully. \n ")
        messages.success(request, "We have sent you a confirmation link to your email. \n ")
        messages.success(request, "Please click on it to activate your account. \n ")

        # Welcome Email

        subject = "Welcome to Kura Electronic Voter Registration System"
        message = "Hello " + myuser.first_name + "\n Welcome to Kura Electronic Voter Registration System| \n Thank " \
                                                 "you for visiting our website \n We have sent you a confirmation " \
                                                 "email, please confirm your email address in order to activate your " \
                                                 "account. \n\n Thank You \n Greg Atemi "
        from_email = settings.EMAIL_HOST_USER
        to_list = [
            myuser.email
        ]
        send_mail(subject, message, from_email, to_list, fail_silently=False)

        # Email Address Confirmation Email

        current_site = get_current_site(request)
        email_subject = "Confirm your email"
        message2 = render_to_string("vote/admin/email_confirmation.html", {
            'name': myuser.first_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token': generate_token.make_token(myuser)
        })
        email = EmailMessage(
            email_subject,
            message2,
            settings.EMAIL_HOST_USER,
            [myuser.email],
        )
        email.fail_silently = False
        email.send()

        return redirect('vote:login')

    return render(request, 'vote/user/signup.html')


def login_admin(request):
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

    return render(request, 'vote/admin/login_admin.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username=username, password=pass1)

        if user is not None:
            auth_login(request, user)
            messages.success(request, "Login Successful.")
            return redirect('vote:index')

        else:
            messages.error(request, "Your Username or Password is incorrect")

    return render(request, 'vote/user/login.html')


def log_out(request):
    logout(request)
    return render(request, 'vote/admin/logout.html')


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)

    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser, token):
        myuser.is_active = True
        myuser.save()
        return redirect('vote:login')
    else:
        return render(request, 'vote/admin/activation_failed.html')


def activation_failed(request):
    return render(request, 'vote/admin/activation_failed.html')


def dashboard(request):
    if request.user.is_authenticated and request.user.is_staff:
        total = Voter.objects.count()
        threshold = (total / 10) * 100
        fname = request.user.first_name
        lname = request.user.last_name
        context = {
            'fname': fname, 'lname': lname, 'total': total, 'threshold': threshold
        }
    else:
        messages.info(request, "Login as Administrator to continue")
        return redirect('vote:login')

    return render(request, 'vote/admin/dashboard.html', context)


def county_detail(request):
    if request.user.is_authenticated and request.user.is_staff:
        fname = request.user.first_name
        lname = request.user.last_name
        context = {
            'fname': fname,
            'lname': lname
        }
        if request.method == "POST":
            county_code = request.POST['county_code']
            county_name = request.POST['county_name']

            mycounty = County.objects.create(county_code=county_code, county_name=county_name)
            mycounty.county_code = county_code
            mycounty.county_name = county_name

            mycounty.save()

            messages.success(request, "County added successfully.")

            return redirect('vote:county_list')
    else:
        messages.info(request, "Login to continue")
        return redirect('vote:login')

    return render(request, 'vote/admin/county_detail.html', context)


def admin_account(request):
    if request.user.is_authenticated and request.user.is_staff:
        uname = request.user.username
        fname = request.user.first_name
        lname = request.user.last_name
        email = request.user.email
        context = {
            'uname': uname,
            'fname': fname,
            'lname': lname,
            'email': email
        }
    else:
        messages.info(request, "Login to continue")
        return redirect('vote:login')

    return render(request, 'vote/admin/admin_account.html', context)


def county_list(request):
    if request.user.is_authenticated and request.user.is_staff:
        county = County.objects.all()
        fname = request.user.first_name
        lname = request.user.last_name
        context = {
            'fname': fname,
            'lname': lname,
            'county': county
        }
    else:
        messages.info(request, "Login to continue")
        return redirect('vote:login')

    return render(request, 'vote/admin/county_list.html', context)


def constituency_detail(request):
    if request.user.is_authenticated and request.user.is_staff:
        county = County.objects.all()
        fname = request.user.first_name
        lname = request.user.last_name
        context = {
            'county': county,
            'fname': fname,
            'lname': lname
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

    else:
        messages.info(request, "Login to continue")
        return redirect('vote:login')

    return render(request, 'vote/admin/constituency_detail.html', context)


def constituency_list(request):
    if request.user.is_authenticated and request.user.is_staff:
        fname = request.user.first_name
        lname = request.user.last_name
        constituency = Constituency.objects.all()
        context = {
            'constituency': constituency,
            'fname': fname,
            'lname': lname
        }
    else:
        messages.info(request, "Login to continue")
        return redirect('vote:login')

    return render(request, 'vote/admin/constituency_list.html', context)


def ward_detail(request):
    if request.user.is_authenticated and request.user.is_staff:
        fname = request.user.first_name
        lname = request.user.last_name
        constituency = Constituency.objects.all()
        context = {
            'constituency': constituency,
            'fname': fname,
            'lname': lname
        }
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

    else:
        messages.info(request, "Login to continue")
        return redirect('vote:login')

    return render(request, 'vote/admin/ward_detail.html', context)


def ward_list(request):
    if request.user.is_authenticated and request.user.is_staff:
        fname = request.user.first_name
        lname = request.user.last_name
        ward = Ward.objects.all()
        context = {
            'ward': ward,
            'fname': fname,
            'lname': lname
        }
    else:
        messages.info(request, "Login to continue")
        return redirect('vote:login')

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
    if request.user.is_authenticated and request.user.is_staff:
        fname = request.user.first_name
        lname = request.user.last_name
        ward = Ward.objects.all()
        county = County.objects.all()
        constituency = Constituency.objects.all()
        context = {
            'ward': ward,
            'county': county,
            'constituency': constituency,
            'fname': fname,
            'lname': lname
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
    if request.user.is_authenticated and request.user.is_staff:
        fname = request.user.first_name
        lname = request.user.last_name
        voter = Voter.objects.all()
        user = User.objects.all()
        context = {
            'voter': voter,
            'user': user,
            'fname': fname,
            'lname': lname
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
