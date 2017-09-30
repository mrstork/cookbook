# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    replaces = [('recipes', '0001_initial'), ('recipes', '0002_recipe_draft'), ('recipes', '0003_auto_20170327_1910'), ('recipes', '0004_remove_recipeinstruction_order')]

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('title', models.CharField(blank=True, null=True, max_length=1000)),
                ('slug', models.CharField(blank=True, null=True, max_length=1000)),
                ('description', models.CharField(blank=True, null=True, max_length=1000)),
                ('serves', models.CharField(blank=True, null=True, max_length=100)),
                ('time', models.CharField(blank=True, null=True, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='RecipeEquipment',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='RecipeIngredient',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='RecipeInstruction',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('description', models.CharField(max_length=500)),
            ],
        ),
        migrations.AddField(
            model_name='recipe',
            name='equipment',
            field=models.ManyToManyField(to='recipes.RecipeEquipment'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(to='recipes.RecipeIngredient'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='instructions',
            field=models.ManyToManyField(to='recipes.RecipeInstruction'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='recipe',
            name='draft',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='recipe',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='recipe',
            name='image',
            field=models.ImageField(upload_to='recipe-images/', blank=True, null=True),
        ),
    ]
