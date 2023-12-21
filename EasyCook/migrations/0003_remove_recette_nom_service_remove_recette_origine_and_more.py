# Generated by Django 4.2.7 on 2023-12-14 15:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('EasyCook', '0002_remove_recette_service_recette_nom_service_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recette',
            name='nom_service',
        ),
        migrations.RemoveField(
            model_name='recette',
            name='origine',
        ),
        migrations.AddField(
            model_name='recette',
            name='service',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='recette', to='EasyCook.service'),
        ),
    ]