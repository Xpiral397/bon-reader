# Generated by Django 5.0.6 on 2024-06-06 06:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('novel', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='novel',
            old_name='lending_gender',
            new_name='leading_gender',
        ),
        migrations.AddField(
            model_name='novel',
            name='length',
            field=models.IntegerField(default=0),
        ),
    ]
