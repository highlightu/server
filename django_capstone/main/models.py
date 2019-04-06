from django.db import models

# Create your models here.


# class UserManager(models.Manager):
#     use_related_fields = True

#     def new(self, **kwargs):
#         return self.filter(pub_date__lte=timezone.now(), **kwargs)


class User(models.Model):
    user_name = models.CharField(max_length=200)
    # objects = UserManager()
