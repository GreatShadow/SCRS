# Generated by Django 4.1.1 on 2022-09-24 08:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0004_course_course_field'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='difficulty',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='course',
            name='passed_ratio',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='course',
            name='satisfaction',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='course',
            name='selected_ratio',
            field=models.FloatField(default=0.0),
        ),
    ]
