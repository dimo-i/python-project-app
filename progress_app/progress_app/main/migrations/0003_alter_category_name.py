# Generated by Django 4.0.1 on 2022-04-13 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_remove_project_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(db_index=True, max_length=50, unique=True),
        ),
    ]