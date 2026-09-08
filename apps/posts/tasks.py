from celery import shared_task

from .services import delete_expired_posts



@shared_task
def delete_expired_posts_task():

    return delete_expired_posts()

