# Generated by Django 5.0.3 on 2024-04-17 22:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='user_id',
            field=models.CharField(max_length=10, primary_key=True, serialize=False, unique=True),
        ),
    ]
