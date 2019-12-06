# Generated by Django 2.0.13 on 2019-12-05 20:42

import re
from django.db import migrations, models
import django.db.migrations.operations.special

def forwards(apps, schema_editor):
    AssetModel = apps.get_model('assets', 'Asset')

    for row in AssetModel.objects.all():

        row.asset_id = row.asset_id.upper()
        asset_search = re.search("^([A-Z0-9]*?[A-Z]?)([0-9]+)$", row.asset_id)
        if asset_search is None: # If the asset_id doesn't have a number at the end
            row.asset_id += "1"

        asset_search = re.search("^([A-Z0-9]*?[A-Z]?)([0-9]+)$", row.asset_id)
        row.asset_id_prefix = asset_search.group(1)
        row.asset_id_number = int(asset_search.group(2))

        row.save(update_fields=['asset_id', 'asset_id_prefix', 'asset_id_number'])

# Functions from the following migrations need manual copying.
# Move them and any dependencies into this file, then update the
# RunPython operations to refer to the local versions:
# assets.migrations.0008_auto_20191205_1937

class Migration(migrations.Migration):

    replaces = [('assets', '0008_auto_20191205_1937'), ('assets', '0009_auto_20191205_2041')]

    dependencies = [
        ('assets', '0007_auto_20190108_0202_squashed_0014_auto_20191017_2052'),
    ]

    operations = [
        migrations.AddField(
            model_name='asset',
            name='asset_id_number',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='asset',
            name='asset_id_prefix',
            field=models.CharField(default='', max_length=8),
        ),
        migrations.RunPython(
            code=forwards,
            reverse_code=django.db.migrations.operations.special.RunPython.noop,
        ),
        migrations.AlterModelOptions(
            name='asset',
            options={'ordering': ['asset_id_prefix', 'asset_id_number'], 'permissions': (('asset_finance', 'Can see financial data for assets'), ('view_asset', 'Can view an asset'))},
        ),
        migrations.AlterField(
            model_name='asset',
            name='asset_id',
            field=models.CharField(max_length=15, unique=True),
        )
    ]
