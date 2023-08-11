from django.shortcuts import render
# Create your views here.
from .serializers import *
from .models import MenuItem, Question
from .gpt3 import GenerateQuestions
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import status 
from rest_framework.response import Response
from decouple import config

# Load the OpenAI API key from the environment variables
api_key=config('OPENAI_API_KEY')
# Initialize the GPT-3 instance for question generation
gpt3_instance = GenerateQuestions(api_key)

class MenuItemAPIView(generics.ListCreateAPIView):
    '''View for listing and creating menu items'''
    queryset=MenuItem.objects.all()
    serializer_class=MenuItemSerializer
    
class MenuItemDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    '''View for retrieving, updating, and deleting individual menu items'''
    queryset=MenuItem.objects.all()
    serializer_class=MenuItemSerializer
    

class GenerateQuestionsAPIView(APIView):
    '''View for generating and saving questions for menu items'''
    
    def post(self, request):
        '''Handling post request'''
        try:
            menu_item_ids = request.data.get("menu_item_ids", [])
            
            #Filter the menu items for which questions have to be generated
            menu_items = MenuItem.objects.filter(id__in=menu_item_ids)
            
            generated_questions = []

            for menu_item in menu_items:
                # Generate questions using the GPT-3 instance
                questions = gpt3_instance.generate_questions(menu_item)
                for question_text in questions:
                    if question_text:
                        generated_questions.append(Question(menu_item=menu_item, question_text=question_text))
            
            if generated_questions:
                try:
                    created_questions = Question.objects.bulk_create(generated_questions)
                    return Response({"message": "Questions generated and saved."}, status=status.HTTP_201_CREATED)
                except Exception as bulk_create_error:
                    return Response({"message": "Failed to save generated questions.", "error": str(bulk_create_error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                return Response({"message": "Failed to generate questions."}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(
                {'message': 'An error occurred while generating questions.', 'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
# View for fetching pre-generated questions for a specific menu item
class PreGeneratedQuestionsAPIView(APIView):
    def get(self, request, pk):
        try:
            menuitem=MenuItem.objects.get(pk=pk)
        except MenuItem.DoesNotExist:
            return Response({'message': 'An error occurred while suggesting questions.', 'error':'Menu Item does not exist'}, status=status.HTTP_404_NOT_FOUND)
        questions=Question.objects.filter(menu_item=menuitem)
        serializer=QuestionSerializer(questions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# View for generating a question from provided text
class GenerateQuestionFromTextAPIView(APIView):
    def post(self,request):
        try:
            text=request.data['text']  
            if text:
                # Generate a question from provided text using the GPT-3 instance
                generate_question = gpt3_instance.generate_question_from_text(text)
                if generate_question:
                    return Response({"question": generate_question}, status=status.HTTP_201_CREATED)
                else:
                    return Response({"message": "Failed to generate question."}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"message": "Text not provided"}, status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
            return Response({"message":"Something went wrong.","error":"The text field is missing in the request data."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            Response({'message':'Unfortunately, Something went wrong. Please try again later.','error':str(e)},status=status.HTTP_400_BAD_REQUEST)
         