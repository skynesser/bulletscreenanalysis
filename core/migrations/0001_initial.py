# Generated by Django 4.0.6 on 2022-07-13 03:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BilibiliURI',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='BulletScreen',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.CharField(max_length=30)),
                ('content', models.CharField(max_length=200)),
                ('URI_ID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.bilibiliuri')),
            ],
        ),
    ]
