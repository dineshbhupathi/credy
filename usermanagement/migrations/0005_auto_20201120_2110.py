# Generated by Django 3.1.3 on 2020-11-20 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usermanagement', '0004_auto_20201119_1910'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='collection',
            name='movies',
        ),
        migrations.AddField(
            model_name='collection',
            name='movies',
            field=models.ManyToManyField(blank=True, null=True, related_name='movie', to='usermanagement.Movies'),
        ),
    ]
