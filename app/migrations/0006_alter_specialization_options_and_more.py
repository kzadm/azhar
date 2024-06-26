# Generated by Django 5.0.6 on 2024-05-25 11:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0005_alter_group_options_alter_qualification_options_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="specialization",
            options={
                "verbose_name": "Специальность",
                "verbose_name_plural": "Специальность",
            },
        ),
        migrations.AlterField(
            model_name="group",
            name="qualification",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="group_qualification",
                to="app.qualification",
                verbose_name="Квалификация",
            ),
        ),
        migrations.AlterField(
            model_name="qualification",
            name="specialization",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="qualification_specialization",
                to="app.specialization",
                verbose_name="Специальность",
            ),
        ),
    ]
