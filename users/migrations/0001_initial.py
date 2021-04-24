# Generated by Django 3.0.7 on 2021-04-24 23:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profileimage', models.ImageField(default='Pdefault.png', upload_to='profile_pics')),
                ('backgroundimage', models.ImageField(default='Bdefault.png', upload_to='background_pics')),
                ('bio', models.TextField(default='No bio', max_length=1000)),
                ('followers', models.ManyToManyField(blank=True, to='users.Profile')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
