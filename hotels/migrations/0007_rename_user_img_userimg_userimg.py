# Generated by Django 4.1.7 on 2023-06-28 16:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0006_userimg'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userimg',
            old_name='user_img',
            new_name='userimg',
        ),
    ]
