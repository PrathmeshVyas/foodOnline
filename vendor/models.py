from django.db import models
from accounts.models import User, UserProfile
from django.shortcuts import render
# Create your models here.
from accounts.utils import send_notification

class Vendor(models.Model):
    user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE)
    user_profile = models.OneToOneField(UserProfile, related_name='userprofile', on_delete=models.CASCADE)
    vendor_name=models.CharField(max_length=100)
    vendor_license = models.ImageField(upload_to='vendor/license')
    is_approved = models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    modified_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.vendor_name

    def save(self, *args, **kwargs):
        if self.pk is not None:
            #update
            orig=Vendor.objects.get(pk=self.pk)
            context = {
                    'user':self.user,
                    'is_approved':self.is_approved
                }
            if orig.is_approved != self.is_approved:
                #send notification mail
                mail_subject='congratulations! your restaurant is approved'
                mail_template='accounts/emails/admin_approval_email.html'
                send_notification(mail_subject, mail_template, context)
            else:
                #send notification mail
                mail_subject='Sorry! you are not eligible for publishing your menu on our marketplace'
                mail_template='accounts/emails/admin_approval_email.html'
                send_notification(mail_subject, mail_template, context)
        return super(Vendor, self).save(*args, **kwargs)