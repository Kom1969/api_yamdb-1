# Generated by Django 3.2 on 2023-03-17 10:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_auto_20230316_2232'),
    ]

    operations = [
        migrations.RenameField(
            model_name='review',
            old_name='rate',
            new_name='score',
        ),
    ]
