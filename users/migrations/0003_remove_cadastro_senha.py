# Generated by Django 5.1.6 on 2025-03-04 00:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_cadastro_senha'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cadastro',
            name='senha',
        ),
    ]
