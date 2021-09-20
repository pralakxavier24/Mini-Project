from django.db import models
# Create your models here.
from django.contrib.auth.models import User


class user_Action_Detail(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    p_desc = models.CharField(max_length=255)
    p_pic = models.FileField(upload_to='pics', null=True, blank=True)
    p_heading = models.CharField(max_length=20)

    def __str__(self):
        return self.p_heading
