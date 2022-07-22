# Generated by Django 4.0.6 on 2022-07-16 17:37

from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('img', models.ImageField(upload_to='profiles/')),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None)),
                ('address_1', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=50)),
                ('zipcode', models.CharField(max_length=20)),
                ('bio', models.TextField()),
                ('temper', models.CharField(max_length=255)),
                ('available', models.BooleanField(default=False)),
                ('friends', models.ManyToManyField(blank=True, to='profiles.profile')),
            ],
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=255)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='statuses', to='profiles.profile')),
            ],
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='photos')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='profiles.profile')),
            ],
        ),
    ]
