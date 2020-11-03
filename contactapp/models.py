from django.db import models



class ContactUs(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=70, default="")
    mobile = models.CharField(max_length = 15,unique = True, null='true', blank='true')
    message = models.CharField(max_length=500, default="")
    attachments = models.FileField(upload_to="%Y/%m/%d")
    
    def __str__(self):
        return self.first_name
