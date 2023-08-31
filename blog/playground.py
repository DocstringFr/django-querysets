import os
import time
from datetime import timedelta
from pprint import pprint

import django
from django.db.models import F
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_querysets.settings')
django.setup()

from blog.models import Author, Article, Comment, Tag, Formation
from generate_test_data import cleanup_and_create_data
from django.db import connection, connections
from django.db.models import Q

cleanup_and_create_data()


def n_plus_1_issues_select_related():
    connections['default'].queries_log.clear()

    # Problème N+1
    articles = Article.objects.select_related('author').all()

    # Dans le cas d'une relation ForeignKey, on peut utiliser prefetch_related aussi
    # articles = Article.objects.prefetch_related('author').all()
    for article in articles:
        print(article.author.name)

    pprint(connection.queries)
    pprint(len(connection.queries))


def n_plus_1_issues_prefetch_related():
    connections['default'].queries_log.clear()

    # Création d'un problème N+1
    authors = Author.objects.prefetch_related('articles').all()
    # authors = Author.objects.prefetch_related('articles').all()
    for author in authors:
        print(author.articles.all())

    pprint(connection.queries)
    pprint(len(connection.queries))


def update_multiple_objects_at_once():
    connections['default'].queries_log.clear()

    # for article in Article.objects.filter(published_date__lte=timezone.now() - timedelta(days=30)):
    #     article.title = 'Article périmé'
    #     article.save()

    Article.objects.filter(published_date__lte=timezone.now() - timedelta(days=30)).update(title='Article périmé')

    pprint(connection.queries)
    pprint(len(connection.queries))


def update_using_f_objects():
    # Ajouter 10€ à tous les prix des formations

    print("Prix actuels")
    for formation in Formation.objects.all():
        print(formation.price)

    print()
    Formation.objects.update(price=F('price') + 10)

    print("Prix après mise à jour")
    for formation in Formation.objects.all():
        print(formation.price)

a = time.time()
update_multiple_objects_at_once()
print(time.time() - a)