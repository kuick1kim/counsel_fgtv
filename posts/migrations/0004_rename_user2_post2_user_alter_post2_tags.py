# Generated by Django 4.2.9 on 2024-01-14 05:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_post2'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post2',
            old_name='user2',
            new_name='user',
        ),
        migrations.AlterField(
            model_name='post2',
            name='tags',
            field=models.ManyToManyField(blank=True, to='posts.hashtag', verbose_name='해시태그 목록'),
        ),
    ]
