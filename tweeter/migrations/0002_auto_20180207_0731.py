# Generated by Django 2.0.2 on 2018-02-07 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tweeter', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='twitteruser',
            name='user_id',
            field=models.CharField(max_length=256, unique=True),
        ),
    ]