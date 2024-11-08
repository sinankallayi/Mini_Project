# Generated by Django 5.1 on 2024-09-08 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('edan_app', '0003_room_table'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room_table',
            name='availability',
            field=models.CharField(choices=[('available', 'Available'), ('unavailable', 'Unavailable')], max_length=50),
        ),
        migrations.AlterField(
            model_name='room_table',
            name='description',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='room_table',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='room_table',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='room_table',
            name='type',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='room_table',
            name='video',
            field=models.FileField(blank=True, null=True, upload_to='room_video/'),
        ),
    ]
