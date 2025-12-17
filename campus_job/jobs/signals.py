from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Application, Notification

@receiver(post_save, sender=Application)
def create_application_notifications(sender, instance, created, **kwargs):
    if created:
        employer_user = instance.job.employer.user
        Notification.objects.create(
            user=employer_user,
            content=f"Новый отклик на вакансию \"{instance.job.title}\" от {instance.user.get_full_name() or instance.user.username}"
        )
    else:
        update_fields = kwargs.get('update_fields')
        if update_fields and 'status' in update_fields:
            if instance.status in ['accepted', 'rejected']:
                status_text = "принята" if instance.status == 'accepted' else "отклонена"
                Notification.objects.create(
                    user=instance.user,
                    content=f"Ваша заявка на вакансию \"{instance.job.title}\" была {status_text}"
                )