# Generated by Django 4.2.3 on 2023-07-11 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('card', '0002_alter_expertcard_city'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expertcard',
            name='country',
            field=models.CharField(blank=True, choices=[('Nigeria', 'Nigeria'), ('Kenya', 'Kenya'), ('uganda', 'Uganda')], max_length=30, null=True),
        ),
    ]
