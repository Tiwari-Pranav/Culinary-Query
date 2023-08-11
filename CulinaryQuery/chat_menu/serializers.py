from rest_framework import serializers
from .models import *

class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model=MenuItem
        fields='__all__'
        
class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Question
        fields='__all__'
        