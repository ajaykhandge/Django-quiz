from django.db import models
from django.core.validators import MinLengthValidator, int_list_validator
from django.contrib.auth.models import User
 
# Create your models here.

QUIZES_NAME = (
    ('COC','Clash of Codes'),
    ('WEBER','Weber'),
    ('HOTKEYS','Hotkeys'),
     
    
)

class Participant(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True,related_name='participant')   
    college_name = models.CharField(max_length=100,blank=False,null=False)
    phone_no = models.CharField(max_length=10,null=False,blank=False,unique=True)
    quiz_name = models.CharField(max_length = 40,choices=QUIZES_NAME,blank=False, null=False,default=QUIZES_NAME[0])
    team_name = models.CharField(max_length=40,blank=True, null=True)
    quiz_status = models.BooleanField(default=False,blank=False, null=False)
    
 