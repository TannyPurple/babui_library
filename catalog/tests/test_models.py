from django.test import TestCase
from catalog.models import Author

# Create your tests here.

class AuthorModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Author.objects.create(first_name = 'Mahbubul',last_name = 'huq')
    
    def test_first_name_lable(self):
        author = Author.objects.get(id=1)
        field_lable = author._meta.get_field('first_name').verbose_name
        self.assertEqual(field_lable,'first name')

    def test_date_of_death_lable(self):
        author = Author.objects.get(id=1)
        field_lable = author._meta.get_field('death_date').verbose_name
        self.assertEqual(field_lable,'died')

    def first_name_max_length(self):
        author = Author.objects.get(id =1)
        max_length =author._meta.get_field('first_name').max_length
        self.assertEqual(max_length,250)

    def test_object_is_last_comma_first_name(self):
        author = Author.objects.get(id=1)
        expected_object_name = f'{author.first_name} {author.last_name}'
        self.assertEqual(str(author),expected_object_name)
    
    def test_get_absolute_url(self):
        author = Author.objects.get(id=1)
        self.assertEqual(author.get_absolute_url(),'/catalog/author/1/')