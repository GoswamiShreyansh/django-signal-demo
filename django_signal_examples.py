# models.py
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
import time

class MyModel(models.Model):
    name = models.CharField(max_length=100)

@receiver(post_save, sender=MyModel)
def my_signal_handler(sender, instance, **kwargs):
    print("Signal received. Processing...")
    time.sleep(5)
    print("Signal processed.")

# Simulate save operation
obj = MyModel.objects.create(name='test')
print("Model save completed.")


import threading

class ThreadModel(models.Model):
    name = models.CharField(max_length=100)

@receiver(post_save, sender=ThreadModel)
def thread_signal_handler(sender, instance, **kwargs):
    print(f"Signal thread ID: {threading.get_ident()}")

print(f"Main thread ID: {threading.get_ident()}")
ThreadModel.objects.create(name='Thread Test')


from django.db import transaction

class Log(models.Model):
    message = models.CharField(max_length=255)

class TransactionModel(models.Model):
    name = models.CharField(max_length=100)

@receiver(post_save, sender=TransactionModel)
def transaction_signal_handler(sender, instance, **kwargs):
    Log.objects.create(message=f"Created {instance.name}")

# Wrap in atomic block
try:
    with transaction.atomic():
        TransactionModel.objects.create(name='Rollback Test')
        raise Exception("Rolling back!")
except:
    pass

print("Logs:", Log.objects.all())  # Should be empty
