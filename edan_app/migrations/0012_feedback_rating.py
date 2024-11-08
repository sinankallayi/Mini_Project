# Generated by Django 5.1 on 2024-10-02 08:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('edan_app', '0011_rename_timestamp_message_sent_at_message_sent_by'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feedback', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('guest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='edan_app.guest_table')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='edan_app.room_table')),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('guest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='edan_app.guest_table')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='edan_app.room_table')),
            ],
        ),
    ]
