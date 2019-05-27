from django.db import models
from datetime import datetime, timedelta
# Create your models here.


# class UserManager(models.Manager):
#     use_related_fields = True

#     def new(self, **kwargs):
#         return self.filter(pub_date__lte=timezone.now(), **kwargs)


class User(models.Model):
    user_name = models.CharField(max_length=50, primary_key=True)
    user_email = models.EmailField(max_length=70, default="zinuzian@naver.com")
    membership_remaining = models.PositiveIntegerField(default=3)
    total_pay = models.PositiveIntegerField(default=0)

    # Methods
    # def get_absolute_url(self):
    #     """Returns the url to access a particular instance of MyModelName."""
    #     return reverse('model-detail-view', args=[str(self.id)])

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.user_name
    
    
    def update_expire_date(self, add_expire_date):
        d = timedelta(days = add_expire_date)
        expire_date = datetime.now() + d


class WithdrawnUser(models.Model):
    user_name = models.CharField(max_length=50, primary_key=True)
    user_email = models.EmailField(max_length=70, default="zinuzian@naver.com")
    membership_remaining = models.PositiveIntegerField(default=3)
    total_pay = models.PositiveIntegerField(default=0)