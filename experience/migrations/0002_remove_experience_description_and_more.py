# Generated by Django 4.2.5 on 2024-03-10 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('experience', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='experience',
            name='description',
        ),
        migrations.AlterField(
            model_name='experience',
            name='company',
            field=models.CharField(max_length=100),
        ),
    ]
