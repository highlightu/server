# Generated by Django 2.1.7 on 2019-04-12 17:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('videoNumber', models.IntegerField()),
                ('delay', models.IntegerField()),
                ('face', models.BooleanField(default=False)),
                ('speech', models.BooleanField(default=False)),
                ('chat', models.BooleanField(default=False)),
                ('youtube', models.BooleanField(default=False)),
                ('date', models.CharField(max_length=50)),
                ('videoFileURL', models.CharField(max_length=200)),
                ('title', models.CharField(max_length=100)),
                ('rect_x', models.IntegerField(default=0)),
                ('rect_y', models.IntegerField(default=0)),
                ('rect_width', models.IntegerField(default=0)),
                ('rect_height', models.IntegerField(default=0)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.User')),
            ],
            options={
                'ordering': ('owner',),
            },
        ),
    ]
