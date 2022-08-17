# Generated by Django 3.1.5 on 2022-08-17 03:28

from django.db import migrations, models
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_user_email_alter_user_nickname_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserAuth',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('phone_number', models.CharField(max_length=11, primary_key=True, serialize=False, verbose_name='휴대폰 번호')),
                ('auth_number', models.IntegerField(verbose_name='인증 번호')),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'user_auth',
            },
        ),
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterModelTable(
            name='user',
            table='user',
        ),
    ]