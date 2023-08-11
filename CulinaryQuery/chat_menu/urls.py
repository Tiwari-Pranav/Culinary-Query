from django.urls import path, include
from .views import *

urlpatterns = [
    path('menuitems/',MenuItemAPIView.as_view(),name='menuitem_list'),
    path('menuitems/<int:pk>/',MenuItemDetailAPIView.as_view(),name='menuitem_description'),
    path('generate-questions/', GenerateQuestionsAPIView.as_view(), name='generate_questions'),
    path('suggest-questions/<int:pk>/', PreGeneratedQuestionsAPIView.as_view(), name='pre_generated_questions'),
    path('generate-question/', GenerateQuestionFromTextAPIView.as_view(), name='generate_question'),
]
