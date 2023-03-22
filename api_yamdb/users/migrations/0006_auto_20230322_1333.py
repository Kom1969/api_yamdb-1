# Generated by Django 3.2 on 2023-03-22 08:33

from django.db import migrations, models
import users.validators


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20230316_2341'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('user', 'User'), ('moderator', 'Moderator'), ('admin', 'Admin')], default='user', help_text='Роль пользователя с правами доступа', max_length=13, verbose_name='Роль'),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=150, unique=True, validators=[users.validators.username_validator], verbose_name='Юзернейм'),
        ),
    ]
