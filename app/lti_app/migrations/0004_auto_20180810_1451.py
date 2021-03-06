# Generated by Django 2.0.6 on 2018-08-10 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lti_app', '0003_auto_20180810_1436'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='assignment',
            name='checks',
        ),
        migrations.AddField(
            model_name='assignment',
            name='academic_style_check',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='assignment',
            name='citation_check',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='assignment',
            name='grammar_check',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='assignment',
            name='plagiarism_check',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='assignment',
            name='semantics_check',
            field=models.IntegerField(default=1),
        ),
    ]
