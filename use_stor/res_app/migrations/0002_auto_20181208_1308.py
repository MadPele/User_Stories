# Generated by Django 2.1.4 on 2018-12-08 13:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('res_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='reservation',
            unique_together={('date', 'room')},
        ),
    ]