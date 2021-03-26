# Generated by Django 3.1.7 on 2021-03-10 19:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moodyapi', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='classifiedsong',
            name='mood',
            field=models.CharField(choices=[('happy', 'happy'), ('sad', 'sad'), ('relaxed', 'relaxed'), ('angry', 'angry')], default='', max_length=8),
        ),
    ]