from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime
from .models import *
from .utils import cookieCart, cartData, guestOrder
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
from django.urls import reverse
from django.http import HttpResponse
from django.template.loader import render_to_string
import pdfkit

def boleta_pdf(request):
    # Datos de ejemplo, en la práctica recibirías esto de la transacción de PayPal
    transaction_data = {
        'product': 'Nombre del producto',
        'price': 1500,
        'transaction_id': 'ABC12345',
        'buyer': 'Cliente Ejemplo',
        'date': '2024-11-11',
    }

    # Renderiza el HTML con los datos de la transacción
    html = render_to_string('boleta.html', transaction_data)

    # Configuración de PDFKit para generar el PDF
    pdfkit_config = pdfkit.configuration(wkhtmltopdf='/usr/local/bin/wkhtmltopdf')  # Asegúrate de tener la ruta correcta
    pdf = pdfkit.from_string(html, False, configuration=pdfkit_config)

    # Genera la respuesta como un archivo PDF
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="boleta.pdf"'
    
    return response

def boleta_view(request):
    # Supongamos que obtienes los datos de la transacción
    # En un caso real, podrías recuperar los datos desde una base de datos o desde PayPal IPN
    transaction_data = {
        'product': 'Nombre del producto',
        'price': 10.00,
        'transaction_id': 'ABC12345',
        'buyer': 'Cliente Ejemplo',
        'date': '2024-11-11',
    }

    # Renderiza la boleta en la pantalla
    return render(request, 'store/boleta.html', transaction_data)

def paypal_payment_view(request):
    # Ejemplo de datos para el formulario de PayPal
    paypal_dict = {
        "business": settings.PAYPAL_RECEIVER_EMAIL,
        "amount": "10.00",  # Ajusta el precio dinámicamente si es necesario
        "item_name": "Nombre del producto",
        "invoice": "unico-id-de-invoice",  # ID único para la transacción
        "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
        "return_url": request.build_absolute_uri(reverse('boleta')),
        "cancel_return": request.build_absolute_uri(reverse('cancel_url')),  # URL de cancelación
    }

    # Crear el formulario de PayPal con los datos
    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {"form": form}
    return render(request, "store/paypal_payment.html", context)

def store(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'store/store.html', context)



def cart(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/cart.html', context)

def checkout(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/checkout.html', context)

def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)

	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)

def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
	else:
		customer, order = guestOrder(request, data)

	total = float(data['form']['total'])
	order.transaction_id = transaction_id

	if total == order.get_cart_total:
		order.complete = True
	order.save()

	if order.shipping == True:
		ShippingAddress.objects.create(
		customer=customer,
		order=order,
		address=data['shipping']['address'],
		city=data['shipping']['city'],
		state=data['shipping']['state'],
		zipcode=data['shipping']['zipcode'],
		)

	return JsonResponse('Payment submitted..', safe=False)
