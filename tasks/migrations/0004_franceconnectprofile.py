from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tasks', '0003_add_user_to_series'),
    ]

    operations = [
        migrations.CreateModel(
            name='FranceConnectProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sub', models.CharField(db_index=True, max_length=255, unique=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='france_connect_profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Profil France Connect',
                'verbose_name_plural': 'Profils France Connect',
            },
        ),
    ]
