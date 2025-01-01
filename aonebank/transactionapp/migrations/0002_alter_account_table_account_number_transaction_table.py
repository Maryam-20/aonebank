# Generated by Django 4.2.16 on 2024-10-19 17:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('transactionapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account_table',
            name='account_number',
            field=models.CharField(default='229079593', max_length=10, unique=True),
        ),
        migrations.CreateModel(
            name='Transaction_table',
            fields=[
                ('transaction_id', models.AutoField(primary_key=True, serialize=False)),
                ('transaction_type', models.CharField(max_length=20)),
                ('transaction_date', models.DateField(auto_now_add=True)),
                ('transaction_amount', models.BigIntegerField()),
                ('recepient_phone_number', models.CharField(max_length=11, null=True)),
                ('recepient_bank_name', models.CharField(max_length=30, null=True)),
                ('recepient_account_number', models.CharField(max_length=10, null=True)),
                ('sender_bank_name', models.CharField(max_length=20, null=True)),
                ('bill_type', models.CharField(max_length=10, null=True)),
                ('mobile_network', models.CharField(max_length=10, null=True)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='transactionapp.account_table')),
                ('sender', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sender', to='transactionapp.account_table')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]