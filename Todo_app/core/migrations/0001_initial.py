# Generated by Django 5.2.1 on 2025-07-04 10:21

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('deadline', models.DateField()),
                ('is_done', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('assignee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks_received', to=settings.AUTH_USER_MODEL)),
                ('assigner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks_assigned', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
