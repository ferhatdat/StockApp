from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Purchases, Sales

@receiver(pre_save, sender=Purchases)
def calculate_total_price(sender, instance, **kwargs):
    instance.price_total = instance.price * instance.quantity

@receiver(pre_save, sender=Sales)
def calculate_total_price_S(sender, instance, **kwargs):
    instance.price_total = instance.price * instance.quantity