# Generated by Django 5.1 on 2024-09-01 22:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('edan_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='guest_table',
            old_name='LOGIN',
            new_name='login',
        ),
        migrations.AlterField(
            model_name='logintable',
            name='email',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]