# Generated by Django 3.0.7 on 2020-07-04 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0007_auto_20200630_1135'),
    ]

    operations = [
        migrations.AddField(
            model_name='articlepost',
            name='links',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
