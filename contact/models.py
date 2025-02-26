from django.db import models

# Create your models here.
class Contact(models.Model):
    name =models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    
#      Feedback_Model

class Feedback(models.Model):
    username= models.CharField(max_length=255)
    useremail = models.EmailField()
    feedback = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return  f"{self.username} - {self.useremail}"