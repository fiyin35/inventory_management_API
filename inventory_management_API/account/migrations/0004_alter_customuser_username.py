# Generated by Django 5.1.4 on 2024-12-28 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_alter_customuser_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='username',
            field=models.TextField(max_length=35, unique=True),
        ),
    ]