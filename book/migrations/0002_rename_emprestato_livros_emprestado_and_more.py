# Generated by Django 5.1.6 on 2025-03-17 00:39

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameField(
            model_name='livros',
            old_name='emprestato',
            new_name='emprestado',
        ),
        migrations.AddField(
            model_name='biblioteca',
            name='usuario_admin',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='biblioteca', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='biblioteca',
            name='cep',
            field=models.CharField(max_length=9),
        ),
        migrations.AlterField(
            model_name='livros',
            name='biblioteca',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='livros', to='book.biblioteca'),
        ),
    ]
