# Generated by Django 2.1.4 on 2018-12-18 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academy', '0002_auto_20181218_1319'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jedi',
            name='last_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
