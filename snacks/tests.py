from django.http import response
from django.test import TestCase
from django.urls import reverse , reverse_lazy
from django.contrib.auth  import get_user_model
from .models import Snack
# Create your tests here.


class SnackTests(TestCase):
    def setUp(self):
        self.user=get_user_model().objects.create_user(
            username = 'ruba',
            email='a@gmal.com',
            password='pass'
            
        )  
        self.snack= Snack.objects.create(
            title = 'candy',
            purchaser = self.user,
            description = 'anything about candy. '
        ) 
    
    def test_string_representation(self):
        self.assertEqual(str(self.snack),'candy')
        
    def test_snack_content(self):
        self.assertEqual(f"{self.snack.title}",'candy')
        self.assertEqual(f"{self.snack.purchaser}",'ruba')
        self.assertEqual(f"{self.snack.description}",'anything about candy. ')
        
    def test_snack_list_view(self):
        response= self.client.get(reverse('snack_list'))
        self.assertEqual(response.status_code,200)
        self.assertContains(response, "candy")
        self.assertTemplateUsed(response,'snack_list.html')
        
    def test_snack_detail_view(self):
        response= self.client.get(reverse('snack_detail', args='1'))
        self.assertEqual(response.status_code,200)
        self.assertContains(response, "candy")
        self.assertTemplateUsed(response,'snack_detail.html')
    
    
    def test_snack_create_view(self):
        response= self.client.post(
            reverse('snack_create'),
         {
            "title" : "chips",
            "purchaser" : self.user.id,
            "description" :"anything about chips. "                           
          },
         follow=True
         )
        self.assertRedirects(response,reverse('snack_detail',args='2'))
        
        

    def test_snack_update_view_redirect(self):
        response = self.client.post(
            reverse("snack_update", args="1"),
            {"title": "pepsi","purchaser":self.user.id,"description":"anythin"}
        )

        self.assertRedirects(response, reverse('snack_detail',args='1'))

    def test_thing_delete_view(self):
        response = self.client.get(reverse("snack_delete", args="1"))
        self.assertEqual(response.status_code, 200)    
    
        



