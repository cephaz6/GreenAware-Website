# Generated by Django 5.0.3 on 2024-04-27 11:31

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_customuser_user_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='api_key',
        ),
        migrations.CreateModel(
            name='ApiKey',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('api_key', models.CharField(max_length=100)),
                ('subscription_package', models.CharField(blank=True, max_length=100, null=True)),
                ('calls', models.IntegerField(default=0)),
                ('quota_allotted', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_active', models.BooleanField(default=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='api_keys', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PaymentInformation',
            fields=[
                ('payment_id', models.AutoField(primary_key=True, serialize=False)),
                ('address', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=100)),
                ('country', models.CharField(max_length=100)),
                ('phone_number', models.CharField(max_length=20)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payment_information', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TransactionHistory',
            fields=[
                ('transaction_id', models.AutoField(primary_key=True, serialize=False)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transaction_history', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
