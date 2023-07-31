from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Hotel, Hotelbooking, HotelImages, Amenities, Contact, Image
from django.db.models import Q


# Create your views here.

def check_booking(start_date, end_date, uid, room_count):
    qs = Hotelbooking.objects.filter(
        start_date__lte=start_date,
        end_date__gte=end_date,
        hotel__uid=uid
    )

    if len(qs) >= room_count:
        return False

    return True


def home(request):

    amenities_obj = Amenities.objects.all()
    hotel_obj = Hotel.objects.all()

    if request.user.is_authenticated:
        user = request.user
        pro_obj = Image.objects.filter(user=user)

    sort_by = request.GET.get('sort_by')
    search = request.GET.get('search')
    ammi = request.GET.getlist('amenities')

    if sort_by:
        if sort_by == "ASC":
            hotel_obj = hotel_obj.order_by('hotel_price')
        elif sort_by == "DSC":
            hotel_obj = hotel_obj.order_by('hotel_price')

    if search:
        hotel_obj = Hotel.objects.filter(
            Q(hotel_name__icontains=search) |
            Q(description__icontains=search))

    if len(ammi):
        hotel_obj = hotel_obj.filter(amenities__amenity_name__in=ammi)

    context = {'hotels_objs': hotel_obj,
               'amenities_objs': amenities_obj, 'search': search, 'pro': pro_obj}

    return render(request, 'home.html', context=context)

# ---------------------------------------------------------------------------


def hotel_detail(request, uid):
    hotel_obj = Hotel.objects.get(uid=uid)
    if request.user.is_authenticated:
        user = request.user
        pro_obj = Image.objects.filter(user=user)

    if request.method == 'POST':
        checkin = request.POST.get('checkin')
        checkout = request.POST.get('checkout')
        hotel = Hotel.objects.get(uid=uid)

        if not check_booking(checkin, checkout, uid, hotel.room_count):
            messages.warning(
                request, 'Hotel is already booked in these dates ')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        Hotelbooking.objects.create(hotel=hotel, user=request.user,
                                    start_date=checkin, end_date=checkout, booking_type='Pre Paid')

        messages.success(request, 'Your booking has been saved')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    return render(request, 'hotel_detail.html', {
        'hotels_obj': hotel_obj, 'pro': pro_obj
    })


def login_page(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user_obj = authenticate(username=username, password=password)
        if not user_obj:
            messages.error(request, "Please enter the correct details")
            return redirect('login')

        login(request, user_obj)
        return redirect('/')

    return render(request, 'login.html')


def register_page(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        user_obj = User.objects.filter(username=username, email=email)

        if user_obj.exists():
            messages.error(request, 'User already exists!')
            return redirect('register')

        user = User.objects.create(username=username, email=email)
        user.set_password(password)
        user.save()
        messages.success(
            request, 'Your account has been created successfully!')
        return redirect('login')

    return render(request, 'register.html')


def logout_page(request):
    logout(request)
    messages.success(request, 'Logout successfully')
    return redirect('login')


def user_booking(request):
    if request.user.is_authenticated:
        user = request.user
        user_booking = Hotelbooking.objects.filter(user=user)
        pro_obj = Image.objects.filter(user=user)
    return render(request, 'index_b.html', {'user_booking': user_booking, 'pro': pro_obj})


def contact(request):
    if request.user.is_authenticated:
        user = request.user
        pro_obj = Image.objects.filter(user=user)
    if request.method == "POST":
        user = request.user
        fname = request.POST['fname']
        lname = request.POST['lname']
        query = request.POST['query']

        contact_obj = Contact(user=user, f_name=fname,
                              l_name=lname, query=query)
        contact_obj.save()
        messages.success(request, "Your query has been sent!")
    return render(request, 'contact.html', {'pro': pro_obj})


def check_limit(request):
    if request.method == "GET":
        user = request.GET.get('action')
        checkin = request.GET.get('checkin')
        checkout = request.GET.get('checkout')

        if not check_booking(checkin, checkout):
            messages.warning(
                request, 'Hotel is already booked in these dates ')
            return redirect('home')
        else:
            messages.success(request, 'Yes you can the hotel of this date')
            return redirect('home')

    context = {'checkin': checkin,
               'checkout': checkout, 'user': user}

    return render(request, 'home.html', context)


def profile(request):
    if request.user.is_authenticated:
        user = request.user
        pro_obj = Image.objects.filter(user=user)

    if request.method == "POST":
        name = request.POST['name']
        pic = request.FILES['file']

        img_obj = Image(name=name, photo=pic)
        img_obj.save()
        messages.success(request, 'Your profile has been saved')
        return redirect('profile')

    return render(request, 'profile.html', {'pro': pro_obj})


# def update_profile(request):
#     if request.user.is_authenticated:
#         user = request.user
#         pro_obj = Image.objects.filter(user=user)

#     if request.method == "POST":
#         pic = request.FILES['file']

#         img_obj = Image(photo=pic)
#         img_obj.save()
#         messages.success(request, 'Your profile has been Updated')
#         return redirect('profile')

#     return render(request, 'profile.html', {'pro': pro_obj})


def delete(request, id):
    pro_dlt = Image.objects.filter(id=id)
    pro_dlt.delete()
    messages.success(request, 'Profile deleting successfully')
    return redirect('profile')
