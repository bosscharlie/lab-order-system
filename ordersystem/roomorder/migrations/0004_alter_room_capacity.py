# Generated by Django 3.2.9 on 2021-11-06 03:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roomorder', '0003_auto_20211105_1332'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='capacity',
            field=models.IntegerField(default=20, verbose_name='可容纳人数'),
        ),
    ]
