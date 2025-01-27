from django.db import migrations
from django.contrib.auth.hashers import identify_hasher, make_password
import logging
from oauth2_provider.models import get_application_model
import oauth2_provider.generators
import oauth2_provider.models


def forwards_func(apps, schema_editor):
    """
    Forward migration touches every application.client_secret which will cause it to be hashed if not already the case.
    """
    Application = get_application_model() #apps.get_model('oauth2_provider', 'application')
    applications = Application.objects.all()
    for application in applications:
        application.save(update_fields=['client_secret'])


class Migration(migrations.Migration):

    dependencies = [
        ('oauth2_provider', '0005_auto_20211222_2352'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='client_secret',
            field=oauth2_provider.models.ClientSecretField(blank=True, db_index=True, default=oauth2_provider.generators.generate_client_secret, help_text='Hashed on Save. Copy it now if this is a new secret.', max_length=255),
        ),
        migrations.RunPython(forwards_func),
    ]
