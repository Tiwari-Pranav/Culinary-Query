from django.core.management.base import BaseCommand
from chat_menu.models import MenuItem, Question
from chat_menu.gpt3 import GenerateQuestions  # Import your GenerateQuestion class
from decouple import config
api_key=config('OPENAI_API_KEY')

class Command(BaseCommand):
    help = 'Generate questions for menu items'

    def handle(self, *args, **options):
        menu_items = MenuItem.objects.all()
        gpt3_instance = GenerateQuestions(api_key)  # Create an instance of GenerateQuestion
 
        generated_questions = []
        
        for menu_item in menu_items:
                questions = gpt3_instance.generate_questions(menu_item)
                for question_text in questions:
                    if question_text:
                        generated_questions.append(Question(menu_item=menu_item, question_text=question_text))
                        
        if generated_questions:
                try:
                    Question.objects.bulk_create(generated_questions)
                    self.stdout.write(self.style.SUCCESS('Questions generated and saved.'))
                except Exception as bulk_create_error:
                    self.stdout.write(self.style.ERROR_OUTPUT({"message": "Failed to save generated questions.", "error": str(bulk_create_error)}))
        else:
                self.stdout.write(self.style.ERROR_OUTPUT({"message": "Failed to generate questions."}))