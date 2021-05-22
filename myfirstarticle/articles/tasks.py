from celery import shared_task
from ..database import db
from ..model import Article, ArticleView


@shared_task
def sync_article_views():
    """This function counts views of all the published Articles and updates every Article's `views` field."""

    items = Article.query.filter_by(published=True).all()
    for item in items:
        view_count = ArticleView.query.filter_by(article_id=item.id).count()
        item.views = view_count

    db.session.commit()
