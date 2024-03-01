# Generated by Django 4.2.5 on 2024-02-29 14:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0002_alter_organization_website'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('image', models.ImageField(blank=True, null=True, upload_to='project_images/')),
                ('description', models.TextField()),
                ('deployed_link', models.URLField(blank=True, null=True)),
                ('tech_stack', models.JSONField(default=list)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('job_seeker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='projects', to='accounts.jobseeker')),
            ],
            options={
                'ordering': ('-created_at',),
            },
        ),
    ]