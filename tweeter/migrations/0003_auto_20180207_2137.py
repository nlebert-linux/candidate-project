# Generated by Django 2.0.2 on 2018-02-08 03:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tweeter', '0002_auto_20180207_0731'),
    ]

    operations = [
        migrations.AlterField(
            model_name='twitteruser',
            name='language',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]