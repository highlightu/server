# Generated by Django 2.1.7 on 2019-04-12 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_name', models.CharField(max_length=50, primary_key=True, serialize=False)),
            ],
        ),
    ]
