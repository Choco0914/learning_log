# Generated by Django 2.1.1 on 2018-10-14 01:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('learning_logs', '0006_comment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='topic',
        ),
        migrations.AddField(
            model_name='comment',
            name='entry',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='learning_logs.Entry'),
            preserve_default=False,
        ),
    ]
