# Generated by Django 5.0 on 2024-06-07 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_alter_movie_release_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('poster_path', models.CharField(blank=True, max_length=200, null=True)),
                ('backdrop_path', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='movie',
            name='belongs_to_collection',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='movie',
            name='poster_url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='movie',
            name='tagline',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
