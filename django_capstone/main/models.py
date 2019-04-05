from django.db import models


class User(models.Model):
    user_ID = models.CharField(max_length=100)

    # @classmethod
    def create(self, user_ID):
        # user = cls(user_ID=user_ID)
        # print("user {0} is created!".format(user))
        self.user_ID = user_ID
        self.save()
        # do something with the user
        # return user

    def __str__(self):
        return self.user_ID
