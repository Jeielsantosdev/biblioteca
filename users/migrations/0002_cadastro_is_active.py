# Generated by Django 5.1.6 on 2025-02-25 23:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cadastro',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]
