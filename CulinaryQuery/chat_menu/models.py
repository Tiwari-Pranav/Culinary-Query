from django.db import models

# Create your models here.
class MenuItem(models.Model):
    name=models.CharField(max_length=50)
    description=models.TextField(max_length=300)
    ingredients=models.TextField(max_length=250)
    
    def __str__(self) -> str:
        return self.name
    
class Question(models.Model):
    menu_item=models.ForeignKey(MenuItem,on_delete=models.CASCADE ,related_name='questions')
    question_text=models.TextField(max_length=200)
    created_at=models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.question_text