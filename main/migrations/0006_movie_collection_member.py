# Generated by Django 5.0 on 2024-06-07 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_collection_movie_belongs_to_collection_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='collection_member',
            field=models.BooleanField(default=False),
        ),
    ]
