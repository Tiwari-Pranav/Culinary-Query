import requests

class GenerateQuestions:
    def __init__(self, api_key):
        self.api_key = api_key
        self.api_url = "https://api.openai.com/v1/engines/text-davinci-003/completions"

    def process_response(self, response, menu_items):
        choices = response.json()["choices"]
        response_text = choices[0]["text"]
        
        # Split the response by "Questions for" to separate menu items
        menu_item_sections = response_text.split("Questions for ")[1:]
        
        questions_per_menu_item = []
        for section in menu_item_sections:
            lines = section.strip().split("\n")
            menu_item_name = lines[0].strip(": ")
            questions = []
            for line in lines[1:]:
                parts = line.split(". ")
                if len(parts) > 1:
                    question = parts[1]
                    questions.append(question)
            questions_per_menu_item.append((menu_item_name, questions))
        print (questions_per_menu_item)
        return questions_per_menu_item
        
    def generate_questions(self, menu_items):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        prompt = ""
        for menu_item in menu_items:
            prompt += (
                f"Generate three questions each for the following menu item:\n"
                f"Name: {menu_item.name}\n"
                f"Description: {menu_item.description}\n"
                f"Ingredients: {menu_item.ingredients}\n"
                f"1. \n"
                f"2. \n"
                f"3. \n"
                f"---\n"
            )

        data = {
            "prompt": prompt,
            "max_tokens": 1000  # Adjust max_tokens as needed
        }
        response = requests.post(self.api_url, json=data, headers=headers)

        if response.status_code == 200:
            questions_per_menu_item = self.process_response(response, menu_items)
            return questions_per_menu_item
        else:
            return []
                
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