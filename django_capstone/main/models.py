from django.db import models
from django.urls import reverse
# Create your models here.


# class UserManager(models.Manager):
#     use_related_fields = True

#     def new(self, **kwargs):
#         return self.filter(pub_date__lte=timezone.now(), **kwargs)


class User(models.Model):
    user_name = models.CharField(max_length=200)

    # Methods
    # def get_absolute_url(self):
    #     """Returns the url to access a particular instance of MyModelName."""
    #     return reverse('model-detail-view', args=[str(self.id)])

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.user_name
