# Generated by Django 3.2.9 on 2021-11-06 05:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('roomorder', '0004_alter_room_capacity'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='book',
            unique_together={('user', 'room', 'date', 'time_id')},
        ),
    ]
