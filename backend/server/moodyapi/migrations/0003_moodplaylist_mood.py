# Generated by Django 3.1.7 on 2021-03-26 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moodyapi', '0002_classifiedsong_mood'),
    ]

    operations = [
        migrations.AddField(
            model_name='moodplaylist',
            name='mood',
            field=models.CharField(choices=[('happy', 'happy'), ('sad', 'sad'), ('relaxed', 'relaxed'), ('angry', 'angry')], default='', max_length=8),
        ),
    ]
