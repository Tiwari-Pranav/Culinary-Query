from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status

from .models import MenuItem, Question
from .serializers import MenuItemSerializer, QuestionSerializer

class MenuItemTestCase(APITestCase):
    
    def setUp(self):
        '''Setup initial data for the tests'''
        self.menu_item=MenuItem.objects.create(name="Paneer Tikka", description="Paneer Tikka is a popular vegetarian appetizer where cubes of paneer (Indian cottage cheese) are marinated in a mixture of yogurt and spices, then skewered and grilled or baked to perfection. It's a flavorful and slightly charred dish often served with chutney.", ingredients= "Paneer, yogurt, spices (cumin, coriander, paprika, turmeric, etc.), ginger, garlic, lemon juice, bell peppers, onions, and skewers.")
        
    def test_menuitem_create(self):
        '''Test creating a new menu item'''
        menu_item_data={
            "name": "Test Menu Item",
            "ingredients": "Test ingredients",
            "description": "Test description"
        }
        response = self.client.post(reverse("menuitem_list"), data=menu_item_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(MenuItem.objects.count(), 2)

    def test_retrieve_menu_item(self):
        '''Test retrieving a menu item'''
        response = self.client.get(reverse("menuitem_description", args=[self.menu_item.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'],self.menu_item.name)
        self.assertEqual(response.data['description'],self.menu_item.description)
        self.assertEqual(response.data['ingredients'],self.menu_item.ingredients)
        
    def test_update_menu_item(self):
        '''Test updating a menu item'''
        menu_item_data={
            "name": "Test Menu Item",
            "ingredients": "Test ingredients",
            "description": "Test description"
        }
        response = self.client.put(reverse("menuitem_description", args=[self.menu_item.id]), data=menu_item_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'],menu_item_data['name'])
        self.assertEqual(response.data['description'],menu_item_data['description'])
        self.assertEqual(response.data['ingredients'],menu_item_data['ingredients'])
        
    def test_delete_menu_item(self):
        '''Test deleting a menu item'''
        response = self.client.delete(reverse("menuitem_description", args=[self.menu_item.id]))
        self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)


class QuestionsViewTestCase(APITestCase):
    '''Setup initial data for the tests'''
    
    def setUp(self):
        self.menu_item=MenuItem.objects.create(name="Paneer Tikka", description="Paneer Tikka is a popular vegetarian appetizer where cubes of paneer (Indian cottage cheese) are marinated in a mixture of yogurt and spices, then skewered and grilled or baked to perfection. It's a flavorful and slightly charred dish often served with chutney.", ingredients= "Paneer, yogurt, spices (cumin, coriander, paprika, turmeric, etc.), ginger, garlic, lemon juice, bell peppers, onions, and skewers.")
        self.questions=Question.objects.create(menu_item=self.menu_item,question_text="What is Paneer Tikka reciepe?")
        
        
    def test_menuitem_questions_view(self):
        '''Test retrieving pre-generated questions for a menu item'''
        response = self.client.get(reverse("pre_generated_questions", args=[self.menu_item.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class QuestionsGenerateTestCase(APITestCase):
    def setUp(self):
        '''Setup initial data for the tests'''
        self.menu_item=MenuItem.objects.create(name="Paneer Tikka", description="Paneer Tikka is a popular vegetarian appetizer where cubes of paneer (Indian cottage cheese) are marinated in a mixture of yogurt and spices, then skewered and grilled or baked to perfection. It's a flavorful and slightly charred dish often served with chutney.", ingredients= "Paneer, yogurt, spices (cumin, coriander, paprika, turmeric, etc.), ginger, garlic, lemon juice, bell peppers, onions, and skewers.")
        self.text="Paneer Tikka the Indian Dish"
        
    def test_generate_questions(self):
        '''Test generating questions for a menu item'''
        response = self.client.post(reverse("generate_questions"),data={"menu_item_ids": [self.menu_item.id]})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Question.objects.count(), 3)
    
    def test_generate_question(self):
        '''Test generating a question from provided text'''
        response = self.client.post(reverse("generate_question"),data={"text": self.text})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)




