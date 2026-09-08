from celery import shared_task

from .services import delete_expired_unverified_users


@shared_task
def delete_expired_unverified_users_task():
        
    return delete_expired_unverified_users()
