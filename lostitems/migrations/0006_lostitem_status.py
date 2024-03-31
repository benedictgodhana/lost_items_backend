# Generated by Django 5.0.3 on 2024-03-30 21:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lostitems', '0005_alter_lostitem_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='lostitem',
            name='status',
            field=models.CharField(choices=[('lost', 'Lost'), ('found', 'Found'), ('claimed', 'Claimed')], default='lost', max_length=10),
        ),
    ]