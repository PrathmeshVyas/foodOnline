from django.shortcuts import render, get_object_or_404
from vendor.models import Vendor
from menu.models import Category, FoodItem
from django.db.models import Prefetch
from django.http import HttpResponse, JsonResponse
from .models import Cart
from .context_processors import get_cart_count
# Create your views here.
def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

def marketplace(request):
    vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)
    vendor_count = vendors.count()
    context = {
        'vendors':vendors,
        'vendor_count':vendor_count,
    }
    return render(request, 'marketplace/listing.html', context)

def vendor_detail(request,vendor_slug):
    vendor = get_object_or_404(Vendor, vendor_slug=vendor_slug)
    categories = Category.objects.filter(vendor = vendor).prefetch_related(
        Prefetch(
            'fooditems',
            queryset=FoodItem.objects.filter(is_available=True)
        )
    )
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
    else:
        cart_items=None

    context= {
        'vendor':vendor,
        'categories':categories,
        'cart_items': cart_items,
    }
    return render(request, 'marketplace/vendor_detail.html', context)


def add_to_cart(request, food_id):
    if request.user.is_authenticated:
        if is_ajax(request):
            try:
                fooditem = FoodItem.objects.get(id=food_id)
                try:
                    chkCart = Cart.objects.get(user=request.user, fooditem=fooditem)
                    #increase card quantity
                    chkCart.quantity += 1
                    chkCart.save()
                    return JsonResponse({'status':'Success', 'messsage': 'increased cart quantity', 'cart_counter':get_cart_count(request), 'qty': chkCart.quantity})
                except:
                    chkCart=Cart.objects.create(user=request.user, fooditem=fooditem, quantity=1)
                    return JsonResponse({'status':'Success', 'message': 'item added to your cart', 'cart_counter':get_cart_count(request), 'qty': chkCart.quantity})
            except:
                return JsonResponse({'status': 'Failed', 'message':'This food does not exists'})
        else:
            return JsonResponse({'status': 'Failed', 'message':'Invalid request'})
    else:
        return JsonResponse({'status': 'Failed', 'message': 'Please login to continue'})

def decrease_cart(request, food_id):
    if request.user.is_authenticated:
        if is_ajax(request):
            try:
                fooditem = FoodItem.objects.get(id=food_id)
                try:
                    chkCart = Cart.objects.get(user=request.user, fooditem=fooditem)
                    #decrease card quantity
                    if chkCart.quantity > 1:
                        chkCart.quantity -= 1
                        chkCart.save()
                    else:
                        chkCart.delete()
                        chkCart.quantity=0
                    return JsonResponse({'status':'Success', 'cart_counter':get_cart_count(request), 'qty': chkCart.quantity})
                except:
                    return JsonResponse({'status':'Failed', 'message': 'you do not have this item in your cart'})
            except:
                return JsonResponse({'status': 'Failed', 'message':'This food does not exists'})
        else:
            return JsonResponse({'status': 'Failed', 'message':'Invalid request'})
    else:
        return JsonResponse({'status': 'Failed', 'message': 'Please login to continue'})