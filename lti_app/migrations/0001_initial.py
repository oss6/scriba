# Generated by Django 2.0.6 on 2018-07-05 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_id', models.CharField(max_length=20)),
                ('assignment_id', models.CharField(max_length=20)),
                ('assignment_type', models.CharField(choices=[('D', 'Diagnostic'), ('G', 'Graded')], max_length=1)),
                ('max_points', models.FloatField()),
                ('outcome_service_url', models.TextField()),
                ('result_sourcedid', models.CharField(max_length=255)),
                ('reference', models.TextField()),
                ('excerpt', models.TextField()),
            ],
        ),
    ]