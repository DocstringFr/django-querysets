import os
from datetime import timedelta
from pprint import pprint

import django
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_querysets.settings')
django.setup()

from blog.models import Author, Article, Comment, Tag, Formation
from generate_test_data import cleanup_and_create_data
from django.db import connection, connections
from django.db.models import Q

cleanup_and_create_data()


def relation_et_lookup():
    # On récupère le premier article
    article = Article.objects.first()

    """Récupération de l'auteur (relation ForeignKey)"""
    # On remet à 0 le compteur de requêtes
    connections['default'].queries_log.clear()

    # On affiche l'auteur de l'article
    print(article.author)
    pprint(connection.queries)
    # On l'affiche une deuxième fois
    print(article.author)
    # On remarque que cela ne produit pas de requête supplémentaire, la valeur en cache est utilisée.
    pprint(connection.queries)

    # On récupère l'auteur à partir du modèle Author
    author = Author.objects.get(articles__author__name='John Doe')
    print(author)

    # On récupère l'auteur à partir d'une requête plus flou
    author = Author.objects.get(articles__author__name__icontains='john')
    print(author)

    """Récupération des articles de l'auteur"""
    # On récupère tous les articles de cet auteur
    articles = Article.objects.filter(author=author)
    print(articles)

    # On récupère tous les articles de cet auteur, mais en partant de l'auteur
    articles = author.articles.all()
    print(articles)

    """Récupération des commentaires de l'article"""
    # On récupère tous les commentaires de cet article
    comments = Comment.objects.filter(article=article)
    print(comments)
    print(comments.query)

    # On récupère tous les commentaires de cet article, mais en partant de l'article
    comments = article.comments.all()
    print(comments)
    print(comments.query)

    """Récupération des tags (modèle qui n'a pas de "related_name")"""
    # Récupérer les tags de l'article
    tags = article.tag_set.all()
    print(tags)

    tags_from_john = Tag.objects.filter(articles__author__name__icontains='jane')
    print(tags_from_john)

    django_tag = Tag.objects.get(name='Django')
    print(django_tag.articles.all())


def objects_q():
    # Rechercher les articles écrits soit par John Doe, soit par Jane Doe
    articles_by_john_or_jane = Article.objects.filter(Q(author__name='John Doe') | Q(author__name='Jane Doe'))
    print("Articles écrits par John Doe ou Jane Doe")
    print(articles_by_john_or_jane)
    print()

    print("Articles qui contiennent le tag Django ou Python")
    articles_django_or_python = Article.objects.filter(Q(tag__name='Django') | Q(tag__name='Python'))
    print(articles_django_or_python.query)
    # Équivalent à ça
    articles_django_or_python = Article.objects.filter(tag__name__in=['Django', 'Python'])
    print(articles_django_or_python.query)
    print(f"Nombre d'articles trouvés: {articles_django_or_python.count()}")
    for article in articles_django_or_python:
        print(article.title, "contient les tags", [tag.name for tag in article.tag_set.all()])

    print()

    # Requête avec 3 Q objects
    articles = Article.objects.filter(
        Q(author__email__icontains='emily') &
        (Q(tag__name='Django') | Q(content__icontains="django"))
    )

    # Affichage des articles trouvés
    print("Articles écrits par une autrice dont l'email contient 'emily' et qui ont soit le tag Django soit contiennent le mot django")
    for article in articles.distinct():  # Notez l'utilisation de distinct() pour éviter les doublons
        print(f"Titre: {article.title}, {article.author.name}, {article.pk}")


def aggregate_and_annotate():
    """Fonction qui montre des exemples de l'utilisation des aggrégations et annotations (Count, Sum, annotate etc)"""

    from django.db.models import Count, Sum, Max, Min, Avg

    authors_with_article_count = Author.objects.annotate(num_articles=Count('articles'))

    emily = Author.objects.get(name='Emily Smith')
    print(f"{emily.name} a écrit {emily.articles.count()} articles.")
    print()

    for author in authors_with_article_count:
        print(f"{author.name} a écrit {author.num_articles} articles.")

    print()
    # Récupérer les auteurs qui ont le plus de commentaires
    authors_with_comment_count = Author.objects.annotate(num_comments=Count('articles__comments')).order_by('-num_comments')
    for author in authors_with_comment_count:
        print(f"{author.num_comments} commentaires ont été écrits sur les articles de {author.name}")

    print()

    # Récupérer les auteurs qui ont écrit le plus d'articles taggés avec Django
    authors_with_django_article_count = (
        Author.objects
        .filter(articles__tag__name='Python')
        .annotate(num_django_articles=Count('articles'))
        .order_by('-num_django_articles')
    )

    for author in authors_with_django_article_count:
        print(f"{author.name} a écrit {author.num_django_articles} articles taggés avec Python")

    print()

    # Récupérer le prix moyen de toutes les formations
    aggregate = Formation.objects.aggregate(prix_moyen=Avg('price'), prix_max=Max('price'), prix_min=Min('price'))
    print(f"Le prix moyen de toutes les formations est de {aggregate['prix_moyen']}€, "
          f"la plus chère est à {aggregate['prix_max']}€ et la moins chère à {aggregate['prix_min']}€")


aggregate_and_annotate()
