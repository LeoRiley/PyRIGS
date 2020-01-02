# Generated by Django 2.0.13 on 2020-01-02 20:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0010_assetstatus_display_class'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assetstatus',
            name='display_class',
            field=models.CharField(help_text='HTML class to be appended to alter display of assets with this status, such as in the list.', max_length=80),
        ),
    ]
