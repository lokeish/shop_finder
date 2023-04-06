from django.shortcuts import render
from django.contrib.gis.measure import Distance
from django.contrib.gis.geos import Point
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Shop
from .forms import ShopForm, UpdateShopForm
from shops.util import helper

def create_shop(request):
    print("create shop starting -->", request.method)
    if request.method == 'POST':
        shop_name = request.POST.get('name')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        address = request.POST.get('address')
        name_exists = helper.check_name(shop_name)
        if name_exists:
            return render(request, 'shop_form.html',{'message':'Name exists already'})
        else:
            location = Point(float(longitude), float(latitude), srid=4326)
            shop = Shop(name=shop_name, location=location, address=address)
            shop.save()
            return redirect('shop_detail', pk=shop.pk)
    return render(request, 'shop_form.html')

def update_shop(request, pk):
    print("starting of function", request.method)
    try:
        shop = get_object_or_404(Shop, pk=pk)
    except Exception as ex:
        return HttpResponse('This shop id does not exist :(')
    if request.method == 'POST':
        shop_name = request.POST.get('name')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        address = request.POST.get('address')
        name_exists = helper.check_name(shop_name)
        if name_exists:
            return render(request, 'shop_form.html',{'message':'Name exists already'})
            return redirect('shop_detail', pk=shop.pk)
        else:
            location = Point(float(longitude), float(latitude), srid=4326)
            shop = Shop(name=shop_name, location=location, address=address, id=pk)
            shop.save()
            return redirect('shop_detail', pk=shop.pk)

    return render(request, 'shop_form.html', {'shop': shop})

def search_shops(request):
    if request.method == 'POST':
        # get form data
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        user_location = Point(float(longitude), float(latitude))
        distance = request.POST.get('distance')
        shops = Shop.objects.filter(
            location__distance_lte=(user_location, Distance(km=distance))
        )
        # return HttpResponse("Searching near by shops")
        return render(request, 'shop_list.html', {'shops': shops})
    else:
        # display search form
        return render(request, 'shop_search.html')


def shop_list(request):
    shops = Shop.objects.all()
    return render(request, 'shop_list.html', {'shops': shops})

def shop_detail(request, pk):
    try:
        shop = get_object_or_404(Shop, pk=pk)
        return render(request, 'shop_detail.html', {'shop': shop})
    except Exception as ex:
        return HttpResponse("This shop id does not exis :(")


def check_website(request):
    return render(request, 'base.html')