from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received
from django.dispatch import receiver
from django.conf import settings
from .models import Order

@receiver(valid_ipn_received)
def paypal_payment_received(sender, **kwargs):
    ipn_obj = sender
    # Verifica que el pago fue completado
    if ipn_obj.payment_status == ST_PP_COMPLETED:
        # Verifica que el receptor es tu cuenta
        if ipn_obj.receiver_email == settings.PAYPAL_RECEIVER_EMAIL:
            # Busca el pedido correspondiente en tu base de datos
            try:
                order = Order.objects.get(transaction_id=ipn_obj.invoice)
                # Actualiza los detalles de la transacción de PayPal
                order.payment_gross = ipn_obj.mc_gross
                order.payer_email = ipn_obj.payer_email
                order.payment_date = ipn_obj.payment_date
                order.complete = True
                order.save()
            except Order.DoesNotExist:
                # Maneja el caso en que la orden no exista
                pass
