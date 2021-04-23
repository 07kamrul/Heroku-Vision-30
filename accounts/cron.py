from .models import Test

def cronJob():
    Test.objects.create(title='Test')

