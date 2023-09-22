from django.db import models
from user_app.models import CustomUser
# from rest_framework import permissions


class Project(models.Model): 
    name = models.CharField(max_length=100)
    description = models.TextField()
    project_type = models.CharField(max_length=20)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.name
    
    class Meta:
        ordering=['-created_time']
        
        
class Contributor(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
       return str(self.user.username)
    
    class Meta:
        ordering=['-created_time'] 
        

