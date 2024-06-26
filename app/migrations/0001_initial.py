# Generated by Django 5.0.6 on 2024-05-25 10:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Qualification",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, null=True)),
                ("updated_at", models.DateTimeField(auto_now=True, null=True)),
                ("name", models.CharField(max_length=100, verbose_name="Квалификация")),
            ],
            options={
                "db_table": "qualification",
            },
        ),
        migrations.CreateModel(
            name="Specialization",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, null=True)),
                ("updated_at", models.DateTimeField(auto_now=True, null=True)),
                (
                    "name",
                    models.CharField(max_length=100, verbose_name="Специальность"),
                ),
            ],
            options={
                "db_table": "specialization",
            },
        ),
        migrations.CreateModel(
            name="Group",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, null=True)),
                ("updated_at", models.DateTimeField(auto_now=True, null=True)),
                (
                    "name",
                    models.CharField(max_length=100, verbose_name="Название группы"),
                ),
                (
                    "qualification",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="group_qualification",
                        to="app.qualification",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.AddField(
            model_name="qualification",
            name="specialization",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="qualification_specialization",
                to="app.specialization",
            ),
        ),
        migrations.CreateModel(
            name="Student",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, null=True)),
                ("updated_at", models.DateTimeField(auto_now=True, null=True)),
                ("name", models.CharField(max_length=50, verbose_name="Имя")),
                ("surname", models.CharField(max_length=50, verbose_name="Фамилия")),
                (
                    "middle_name",
                    models.CharField(max_length=50, verbose_name="Отчество"),
                ),
                ("birthday", models.DateField(verbose_name="Дата рождения")),
                ("iin", models.CharField(max_length=12, verbose_name="ИИН")),
                (
                    "nationality",
                    models.CharField(max_length=20, verbose_name="Национальность"),
                ),
                (
                    "parents",
                    models.CharField(
                        max_length=300, verbose_name="ФИО и контакты родителей"
                    ),
                ),
                (
                    "education_lang",
                    models.IntegerField(
                        choices=[(1, "Казахский"), (2, "Русский")],
                        default=1,
                        verbose_name="Язык обучения",
                    ),
                ),
                (
                    "residence_address",
                    models.CharField(max_length=255, verbose_name="Адрес прописки"),
                ),
                (
                    "residential_address",
                    models.CharField(max_length=255, verbose_name="Адрес проживания"),
                ),
                (
                    "phone",
                    models.CharField(max_length=30, verbose_name="Номер телефона"),
                ),
                (
                    "avg_certificate",
                    models.FloatField(verbose_name="Средний балл аттестата"),
                ),
                (
                    "avg_subject",
                    models.FloatField(verbose_name="Средний балл по предметам"),
                ),
                (
                    "pay",
                    models.IntegerField(
                        choices=[(1, "Грант"), (2, "Коммерческий")],
                        default=1,
                        verbose_name="Оплата за обучение",
                    ),
                ),
                (
                    "education_type",
                    models.IntegerField(
                        choices=[(1, "Очная"), (2, "Дистанциионная")],
                        default=1,
                        verbose_name="Форма обучения",
                    ),
                ),
                (
                    "status",
                    models.IntegerField(
                        choices=[
                            (1, "Ожидание"),
                            (2, "Поступил"),
                            (3, "Не поступил"),
                            (4, "Забрал документы"),
                        ],
                        default=1,
                    ),
                ),
                (
                    "qualification",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="student_qualification",
                        to="app.qualification",
                    ),
                ),
            ],
            options={
                "db_table": "student",
            },
        ),
        migrations.CreateModel(
            name="StudentGroup",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, null=True)),
                ("updated_at", models.DateTimeField(auto_now=True, null=True)),
                (
                    "group",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="student_group_group",
                        to="app.group",
                    ),
                ),
                (
                    "student",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="student_group_student",
                        to="app.student",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
