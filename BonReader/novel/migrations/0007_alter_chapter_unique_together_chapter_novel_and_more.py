# Generated by Django 5.0.6 on 2024-08-01 16:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('novel', '0006_alter_chapter_content_alter_chapter_un_save_text'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='chapter',
            unique_together=set(),
        ),
        migrations.AddField(
            model_name='chapter',
            name='novel',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='novel.novel'),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='chapter',
            unique_together={('chapter', 'novel')},
        ),
    ]
