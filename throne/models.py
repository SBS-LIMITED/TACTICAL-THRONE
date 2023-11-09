from django.db import models

class Account(models.Model):
    first_name = models.CharField(max_length=100, null=False)
    last_name = models.CharField(max_length=100, null=False)
    email = models.EmailField(max_length=200, null=False, primary_key=True)
    phone_no = models.IntegerField(null=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

class H_key(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    h_key = models.CharField( max_length=500, null=False)
    iv = models.BinaryField(null=False)
    password = models.CharField(max_length=200, null=False)

    def __str__(self):
        return self.h_key