from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .forms import OrderForm
from .models import Order, Payment, OrderedFood
from marketplace.models import Cart
from marketplace.context_processors import get_cart_amounts
import simplejson as json
from .utils import genrate_order_number
from accounts.utils import send_notification
from django.contrib.auth.decorators import login_required
import razorpay
from foodOnline_main.settings import RZP_KEY_ID, RZP_SECRET_KEY
from orders.models import Order
# Create your views here.

client = razorpay.Client(auth=(RZP_KEY_ID, RZP_SECRET_KEY))

@login_required(login_url='login')
def place_order(request):
    cart_items=Cart.objects.filter(user=request.user).order_by('created_at')
    cart_count=cart_items.count()
    if cart_count <= 0:
        return redirect('marketplace')

    sub_total = get_cart_amounts(request)['subtotal']
    total_tax = get_cart_amounts(request)['tax']
    grand_total = get_cart_amounts(request)['grand_total']
    tax_data = get_cart_amounts(request)['tax_dict']

    form = OrderForm(request.POST)
    if form.is_valid():
        order=Order()
        order.first_name=form.cleaned_data['first_name']
        order.last_name=form.cleaned_data['last_name']
        order.phone=form.cleaned_data['phone']
        order.address=form.cleaned_data['address']
        order.country=form.cleaned_data['country']
        order.state=form.cleaned_data['state']
        order.city=form.cleaned_data['pin_code']
        order.user=request.user
        order.total=grand_total
        order.tax_data=json.dumps(tax_data)
        order.total_tax=total_tax
        order.payment_method=request.POST['payment_method']
        order.save()# order id genratred
        order.order_number=genrate_order_number(order.id)
        order.save()

        # razorpay payment integration
        DATA = {
            "amount": float(order.total) * 100,
            "currency": "INR",
            "receipt": "receipt#1"+order.order_number,
            "notes": {
                    "key1": "value3",
                    "key2": "value2"
            }
        }
        rzp_order = client.order.create(data=DATA)
        # print(rzp_order)
        rzp_order_id=rzp_order['id']
        # print(rzp_order_id)
        context = {
            'order':order,
            'cart_items':cart_items,
            'rzp_order_id':rzp_order_id,
            'RZP_KEY_ID':RZP_KEY_ID,
            'rzp_amount':float(order.total) * 100
        }
        return render(request, 'orders/placeorder.html', context)

    else:
        print(form.errors)

    return render(request, 'orders/placeorder.html')

@login_required(login_url='login')
def payments(request):
    # check is f request is ajax or not
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == 'POST':
    # store payment details in payment model
        order_number=request.POST.get('order_number')
        transaction_id=request.POST.get('transaction_id')
        payment_method=request.POST.get('payment_method')
        status=request.POST.get('status')

        print("--->", order_number, transaction_id, payment_method, status)
        order = Order.objects.get(user=request.user, order_number=order_number)
        payment = Payment(
            user=request.user,
            transaction_id=transaction_id,
            payment_method=payment_method,
            amount=order.total,
            status=status
        )
        payment.save()

        #update order model
        order.payment=payment
        order.is_ordered=True
        order.save()
    
        #store cart items in ordered food model
        cart_items=Cart.objects.filter(user=request.user)
        for item in cart_items:
            ordered_food=OrderedFood()
            ordered_food.order=order
            ordered_food.payment=payment
            ordered_food.user=request.user
            ordered_food.fooditem=item.fooditem
            ordered_food.quantity=item.quantity
            ordered_food.price=item.fooditem.price
            ordered_food.amount = item.fooditem.price * item.quantity #total amount
            ordered_food.save()
        
        # send order confirmation mail to customer
        mail_subject = "Thank you for ordering with us."
        email_template = "orders/order_confirmation_email.html"
        context = {
            'user':request.user,
            'to_email':order.email,
            'order':order
        }
        # send_notification(mail_subject, email_template, context)

        # send new order received mail to vendor
        mail_subject="you have received a new order"
        mail_template="orders/new_order_received.html"
        to_emails=[]
        for i in cart_items:
            if i.fooditem.vendor.user.email not in to_emails:
                to_emails.append(i.fooditem.vendor.user.email)
        print("to_emails==>", to_emails)
        context = {
            'order':order,
            'to_email':to_emails
        }
        # send_notification(mail_subject, mail_template, context)
        
        # clear the cart if payment is success
        # cart_items.delete()
        response = {
            'order_number':order_number,
            'transaction_id':transaction_id
        }
        #return back with ajax with status sucess or failure
        return JsonResponse(response)
    return HttpResponse('HAR HAR MAHADEV')


def order_complete(request):
    order_number = request.GET.get('order_no')
    transaction_id = request.GET.get('trans_id')

    try:
        order=Order.objects.get(order_number=order_number, payment__transaction_id=transaction_id, is_ordered=True)
        ordered_food=OrderedFood.objects.filter(order=order)

        sub_total=0
        for item in ordered_food:
            sub_total+=(item.price*item.quantity)

        tax_data=json.loads(order.tax_data)
        # print(tax_data)
        context = {
            'order':order,
            'ordered_food':ordered_food,
            'sub_total':sub_total,
            'tax_data':tax_data
        }
        return render(request, 'orders/order_complete.html', context)
    except:
        return redirect('home')

    