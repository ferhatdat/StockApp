from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, Group
from rest_framework.authtoken.models import Token



@receiver(post_save, sender=User)
def create_Token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user_id=instance.id)
        user = User.objects.get(username=instance.username)
        if not user.is_superuser:
            group = Group.objects.get(name='Read_Only')
            user.groups.add(group)
            user.save()
