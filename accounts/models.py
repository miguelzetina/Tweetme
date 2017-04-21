from django.conf import settings
from django.db import models
from django.urls import reverse_lazy

# Create your models here.


class UserProfileManager(models.Manager):
    use_for_related_fields = True

    def all(self):
        qs = self.get_queryset().all()
        try:
            if self.instance:
                qs = qs.exclude(user=self.instance)
        except:
            pass
        return qs

    def toogle_follow(self, user, to_toogle_user):
        user_profile, created = UserProfile.objects.get_or_create(user=user)
        if to_toogle_user in user_profile.following.all():
            user_profile.following.remove(to_toogle_user)
            added = False
        else:
            user_profile.following.add(to_toogle_user)
            added = True
        return added

    def is_following(self, user, followed_by_user):
        user_profile, created = UserProfile.objects.get_or_create(user=user)
        if created:
            return False
        if followed_by_user in user_profile.following.all():
            return True
        return False


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name='profile')  # user.profile
    following = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name='followed_by')
    # user.profile.following -- usuarios que sigo
    # user.followed_by -- usuarios que me siguen -- reverse relationship

    objects = UserProfileManager()

    def __str__(self):
        return str(self.following.all().count())

    def get_following(self):
        users = self.following.all()
        return users.exclude(username=self.user.username)

    def get_follow_url(self):
        return reverse_lazy("profiles:follow", kwargs={"username": "self.user.username"})

    def get_absolute_url(self):
        return reverse_lazy("profiles:detail", kwargs={"username": "self.user.username"})
