import os
import django
from datetime import datetime, timedelta
import zoneinfo

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_querysets.settings')
django.setup()

from blog.models import Author, Article, Comment


def cleanup_and_create_data():
    # Nettoyage de tous les modèles
    Author.objects.all().delete()
    Article.objects.all().delete()
    Comment.objects.all().delete()

    # Création des auteurs
    author1 = Author.objects.create(name='John Doe', email='john.doe@example.com')
    author2 = Author.objects.create(name='Jane Doe', email='jane.doe@example.com')
    author3 = Author.objects.create(name='Emily Smith', email='emily.smith@example.com')

    # Création des articles
    article1 = Article.objects.create(
        title='Django pour les débutants',
        content='Lorem ipsum dolor sit amet...',
        published_date=datetime.now(zoneinfo.ZoneInfo("Europe/Paris")),
        author=author1
    )

    article2 = Article.objects.create(
        title='Comment utiliser les Querysets',
        content='Lorem ipsum dolor sit amet...',
        published_date=datetime.now(zoneinfo.ZoneInfo("Europe/Paris")) - timedelta(days=2),
        author=author2
    )

    article3 = Article.objects.create(
        title='Optimisation avec Django',
        content='Lorem ipsum dolor sit amet...',
        published_date=datetime.now(zoneinfo.ZoneInfo("Europe/Paris")) - timedelta(days=60),
        author=author3
    )

    article4 = Article.objects.create(
        title='Queryset avancés avec Django',
        content='Lorem ipsum dolor sit amet...',
        published_date=datetime.now(zoneinfo.ZoneInfo("Europe/Paris")) - timedelta(days=800),
        author=author3
    )

    # Création des commentaires
    comment1 = Comment.objects.create(
        article=article1,
        content='Super article !',
        posted_at=datetime.now()
    )

    comment2 = Comment.objects.create(
        article=article1,
        content='Merci pour ces informations !',
        posted_at=datetime.now() - timedelta(hours=2)
    )

    comment3 = Comment.objects.create(
        article=article2,
        content='Très utile !',
        posted_at=datetime.now() - timedelta(hours=5)
    )

    print("Données de test créées avec succès.")
