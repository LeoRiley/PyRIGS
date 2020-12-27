# Generated by Django 3.1.2 on 2020-12-27 17:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('RIGS', '0047_auto_20201213_1642'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='riskassessment',
            name='event_size',
        ),
        migrations.AlterField(
            model_name='riskassessment',
            name='power_mic',
            field=models.ForeignKey(blank=True, help_text='Who is the Power MIC? (if yes to the above question, this person <em>must</em> be a Power Technician or Power Supervisor)', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='power_mic', to=settings.AUTH_USER_MODEL, verbose_name='Power MIC'),
        ),
    ]
