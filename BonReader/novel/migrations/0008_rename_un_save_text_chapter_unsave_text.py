# Generated by Django 5.0.6 on 2024-08-03 07:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('novel', '0007_alter_chapter_unique_together_chapter_novel_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chapter',
            old_name='un_save_text',
            new_name='unsave_text',
        ),
    ]