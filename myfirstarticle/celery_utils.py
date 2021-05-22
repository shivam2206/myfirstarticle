def schedule_tasks(celery):
    celery.conf.beat_schedule = {
        'sync-article-views': {
            'task': 'myfirstarticle.articles.tasks.sync_article_views',
            'schedule': 5 * 60,
            'args': ()
        },
    }
