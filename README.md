Question 1: By default are Django signals executed synchronously or asynchronously? 
Answer: 
By default, Django signals are executed synchronously. This means that when the signal is sent, all 
connected receivers are executed before the flow proceeds further in the code. 
Here’s a simple code snippet to prove this: 
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
Expected Output (in sequence): 
Signal received. Processing... 
(wait 5 seconds) 
Signal processed. 
Model save completed. 
Conclusion: The print("Model save completed.") line is not executed until the signal handler finishes 
execution, proving that the signal is synchronous. 


Question 2: Do Django signals run in the same thread as the caller? 
Answer: 
Yes, by default, Django signals run in the same thread as the caller. This means that if you print the 
current thread's identifier inside both the model-saving logic and the signal handler, they will match. 
Code Snippet: 
# models.py 
from django.db import models 
from django.db.models.signals import post_save 
from django.dispatch import receiver 
import threading 
class MyModel(models.Model): 
name = models.CharField(max_length=100) 
@receiver(post_save, sender=MyModel) 
def my_signal_handler(sender, instance, **kwargs): 
print(f"Signal thread ID: {threading.get_ident()}") 
# In shell or view 
print(f"Main thread ID: {threading.get_ident()}") 
MyModel.objects.create(name="thread-test") 
Expected Output: 
Main thread ID: 140735135707008 
Signal thread ID: 140735135707008 
Conclusion: The matching thread IDs confirm that the signal handler is executed in the same thread 
as the caller. 


Question 3: By default do Django signals run in the same database transaction as the caller? 
Answer: 
Yes, Django signals run in the same database transaction as the caller by default. This means that if 
the transaction is rolled back after the signal is triggered, changes in both the main operation and 
the signal handler are rolled back. 
Code Snippet: 
from django.db import models, transaction 
from django.db.models.signals import post_save 
from django.dispatch import receiver 
class MyModel(models.Model): 
name = models.CharField(max_length=100) 
class Log(models.Model): 
message = models.CharField(max_length=255) 
@receiver(post_save, sender=MyModel) 
def my_signal_handler(sender, instance, **kwargs): 
Log.objects.create(message=f"Created {instance.name}") 
from django.db import transaction 
try: 
with transaction.atomic(): 
MyModel.objects.create(name='test') 
raise Exception("Rolling back!") 
except: 
pass 
print("Logs:", Log.objects.all())  # Should print an empty queryset 
