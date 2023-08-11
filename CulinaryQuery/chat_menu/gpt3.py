import requests

class GenerateQuestions:
    def __init__(self, api_key):
        self.api_key = api_key
        self.api_url = "https://api.openai.com/v1/engines/text-davinci-003/completions"

    def generate_questions(self, menu_item):
        # Set the headers for the API request
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        # Create a prompt for generating questions based on menu item information
        prompt = (
            f"Generate three hard questions based on the following information:\n"
            f"Menu Item Name: {menu_item.name}\n"
            f"Ingredients: {menu_item.ingredients}\n"
            f"Description: {menu_item.description}\n"
            f"Questions:\n"
            f"1. \n"
            f"2. \n"
            f"3. \n"
        )

        # Prepare the data for the API request
        data = {
            "prompt": prompt,
            "max_tokens": 300  # Adjust max_tokens as needed
        }

        # Send the API request to OpenAI
        response = requests.post(self.api_url, json=data, headers=headers)

        if response.status_code == 200:
            # Extract the generated questions from the API response
            choices = response.json()["choices"]
            questions_text = choices[0]["text"]
            questions = questions_text.split("\n")
            
            # Remove any empty or whitespace-only strings from the list
            questions = [question.strip() for question in questions if question.strip()]
            
            # Remove numbers in front of questions
            questions = [question.split(". ", 1)[1] for question in questions]
            
            # Return the first three generated questions
            return questions[:3]
        else:
            # Return placeholders if the API request was unsuccessful
            return [None, None, None]
                
    def generate_question_from_text(self, description):
        # Set the headers for the API request
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        # Create a prompt for generating a question based on provided text
        data = {
            "prompt": f"Generate a question based on the following text: {description}\nQuestion:",
            "max_tokens": 100
        }
        
        # Send the API request to OpenAI
        response = requests.post(self.api_url, json=data, headers=headers)
        if response.status_code == 200:
            # Extract and return the generated question from the API response
            return response.json()["choices"][0]["text"].strip()
        else:
            # Return None if the API request was unsuccessful
            return None