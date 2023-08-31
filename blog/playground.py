import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_querysets.settings')
django.setup()

from blog.models import Author, Article, Comment
from _generate_test_data import cleanup_and_create_data

cleanup_and_create_data()

# Récupérer tous les articles publiés cette année qui contiennent Django
articles = Article.objects.filter(published_date__year=2023, title__icontains='django')
print(articles)


articles = Article.objects.filter(published_date__year=2023).exclude(title__icontains='django')
print(articles)

print(Article.objects.get(title='Django pour les débutants'))
try:
    print(Article.objects.get(title='Django avancé'))
except Article.DoesNotExist:
    print("L'article n'existe pas !")

