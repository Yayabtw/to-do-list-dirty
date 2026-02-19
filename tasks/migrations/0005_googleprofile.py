# Generated manually for Google OAuth

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tasks', '0004_franceconnectprofile'),
    ]

    operations = [
        migrations.CreateModel(
            name='GoogleProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sub', models.CharField(db_index=True, max_length=255, unique=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='google_profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Profil Google',
                'verbose_name_plural': 'Profils Google',
            },
        ),
    ]
