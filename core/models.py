from django.db import models
from django.contrib.auth.models import User
import uuid
from django.dispatch import receiver
from django.db.models.signals import post_save
import string, random


class PasswordReset(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reset_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    created_when = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Password reset for {self.user.username} at {self.created_when}"


class Accounts(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='useraccount')
    name = models.CharField(max_length=10, unique=True, editable=False)
    pic = models.ImageField(upload_to='profile_pictures/', default='default.png')
    type = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=11, null=False, blank=False)
    dob = models.DateField(max_length=50, null=True, blank=True)
    gender = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)
    # street = models.CharField(max_length=50, null=True, blank=True)
    postal_code = models.CharField(max_length=50, null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # created_by = models.ForeignKey(User,on_delete= models.SET_NULL,null=True,related_name='created_accounts')
    # updated_by = models.ForeignKey(User,on_delete= models.SET_NULL,null=True, related_name='created_accounts')
    # created_by = models.ForeignKey(
    #     User, on_delete=models.SET_NULL, null=True,
    #     related_name='created_accounts', related_query_name='created_account'
    # )
    # updated_by = models.ForeignKey(
    #     User, on_delete=models.SET_NULL, null=True,
    #     related_name='updated_accounts', related_query_name='updated_account'
    # )

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = self.generate_account()

        super().save(*args, **kwargs)

    # def generate_account(self):
    #     last_name = Accounts.objects.exclude(name_is_null= True).order_by('id').last()
    #     if not last_name or not last_name.name:
    #         new_name = '1000000000'
    #     else:
    #         last_name = int(last_name.name)
    #         new_name = str(last_name+1).zfill(10)
    #     return new_name

    def generate_account(self):
        last_name = Accounts.objects.exclude(name__isnull=True).order_by('id').last()
        if not last_name or not last_name.name:
            new_name = '1000000000'
        else:
            last_name = int(last_name.name)
            new_name = str(last_name + 1).zfill(10)
        return new_name


@receiver(post_save, sender=User)
def create_or_update_account(sender, instance, created, **kwargs):
    if created:
        Accounts.objects.create(user=instance)
    else:
        instance.useraccount.save()


class Transactions(models.Model):
    transaction_type = models.CharField(max_length=100, null=False)
