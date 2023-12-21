# Generated by Django 4.2.7 on 2023-12-19 09:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('EasyCook', '0003_remove_recette_nom_service_remove_recette_origine_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='frigo',
            name='ingredients_dispo',
            field=models.ManyToManyField(to='EasyCook.ingredients', verbose_name='ingredients_dispo'),
        ),
        migrations.AlterField(
            model_name='ingredients',
            name='nom_ingredient',
            field=models.CharField(max_length=50, primary_key=True, serialize=False, verbose_name='Nom_ingrédient'),
        ),
        migrations.AlterField(
            model_name='ingredients',
            name='unite',
            field=models.CharField(max_length=50, verbose_name='Unité'),
        ),
        migrations.AlterField(
            model_name='recette',
            name='nom_ingredient',
            field=models.ManyToManyField(to='EasyCook.ingredients', verbose_name='Ingredients'),
        ),
        migrations.AlterField(
            model_name='recette',
            name='nom_recette',
            field=models.CharField(max_length=100, primary_key=True, serialize=False, verbose_name='Nom de la recette'),
        ),
        migrations.AlterField(
            model_name='recetteingredients',
            name='nom_ingredient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='EasyCook.ingredients', verbose_name='Ingredients'),
        ),
        migrations.AlterField(
            model_name='recetteingredients',
            name='nom_recette',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='EasyCook.recette', verbose_name='Nom de la recette'),
        ),
        migrations.AlterField(
            model_name='review',
            name='commentaire',
            field=models.CharField(max_length=200, verbose_name='Commentaire'),
        ),
        migrations.AlterField(
            model_name='review',
            name='id_review',
            field=models.AutoField(max_length=100, primary_key=True, serialize=False, verbose_name='ID de la revue'),
        ),
        migrations.AlterField(
            model_name='review',
            name='nom_recette',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='EasyCook.recette', verbose_name='Nom de la recette'),
        ),
        migrations.AlterField(
            model_name='review',
            name='note',
            field=models.IntegerField(choices=[(0, '0'), (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], verbose_name='Note'),
        ),
        migrations.AlterField(
            model_name='service',
            name='id_service',
            field=models.AutoField(max_length=100, primary_key=True, serialize=False, verbose_name='ID du service'),
        ),
        migrations.AlterField(
            model_name='service',
            name='nom_recette',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='service_recette', to='EasyCook.recette', unique=True, verbose_name='Nom de la recette'),
        ),
    ]