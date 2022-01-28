# Generated by Django 4.0.1 on 2022-01-28 14:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SavedPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_title', models.CharField(max_length=150, unique=True)),
                ('number_upvotes', models.IntegerField()),
                ('number_comments', models.IntegerField()),
                ('post_link', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='TopLevelComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contents', models.TextField(unique=True)),
                ('number_upvotes', models.IntegerField()),
                ('parent_post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='saved_posts.savedpost')),
            ],
        ),
    ]
