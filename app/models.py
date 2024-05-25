from django.db import models

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True


class EducationLanguageChoice(models.IntegerChoices):
    KAZAKH = 1, 'Казахский'
    RUSSIAN = 2, 'Русский'


class PayType(models.IntegerChoices):
    GRANT = 1, 'Грант'
    COMMERCE = 2, 'Коммерческий'


class EducationForm(models.IntegerChoices):
    FULL_TIME = 1, 'Очная'
    DISTANCE = 2, 'Дистанциионная'


class StudentStatus(models.IntegerChoices):
    AWAIT = 1, 'Ожидание'
    AGREED = 2, 'Поступил'
    NOT_AGREED = 3, 'Не поступил'
    REFUND = 4, 'Забрал документы'


class Student(BaseModel):
    name = models.CharField(max_length=50, verbose_name='Имя')
    surname = models.CharField(max_length=50, verbose_name='Фамилия')
    middle_name = models.CharField(max_length=50, verbose_name='Отчество')
    birthday = models.DateField(verbose_name='Дата рождения')
    iin = models.CharField(max_length=12, verbose_name='ИИН')
    nationality = models.CharField(max_length=20, verbose_name='Национальность')
    parents = models.CharField(max_length=300, verbose_name='ФИО и контакты родителей')
    education_lang = models.IntegerField(choices=EducationLanguageChoice, default=EducationLanguageChoice.KAZAKH, verbose_name='Язык обучения')
    residence_address = models.CharField(max_length=255, verbose_name='Адрес прописки')
    residential_address = models.CharField(max_length=255, verbose_name='Адрес проживания')
    phone = models.CharField(max_length=30, verbose_name='Номер телефона')
    avg_certificate = models.FloatField(verbose_name='Средний балл аттестата')
    avg_subject = models.FloatField(verbose_name='Средний балл по предметам')
    pay = models.IntegerField(choices=PayType, default=PayType.GRANT, verbose_name='Оплата за обучение')
    education_type = models.IntegerField(choices=EducationForm, default=EducationForm.FULL_TIME, verbose_name='Форма обучения')
    status = models.IntegerField(choices=StudentStatus, default=StudentStatus.AWAIT, verbose_name='Статус')
    qualification = models.ForeignKey('Qualification', on_delete=models.DO_NOTHING, related_name='student_qualification')

    class Meta:
        db_table = 'student'
        verbose_name = "Студент"
        verbose_name_plural = "Студент"

    def __str__(self):
        return f'{self.surname} {self.name} {self.middle_name}'


class Specialization(BaseModel):
    name = models.CharField(max_length=100, verbose_name='Специальность')
    number = models.CharField(max_length=30, verbose_name='Шифр специальности')

    class Meta:
        db_table = 'specialization'
        verbose_name = "Специальность"
        verbose_name_plural = "Специальность"

    def __str__(self):
        return self.name


class Qualification(BaseModel):
    name = models.CharField(max_length=100, verbose_name='Квалификация')
    number = models.CharField(max_length=30, verbose_name='Шифр квалификации')
    specialization = models.ForeignKey(Specialization, on_delete=models.DO_NOTHING, related_name='qualification_specialization', verbose_name='Специальность')

    class Meta:
        db_table = 'qualification'
        verbose_name = "Квалификация"
        verbose_name_plural = "Квалификация"

    def __str__(self):
        return self.name


class Group(BaseModel):
    name = models.CharField(max_length=100, verbose_name='Название группы')
    qualification = models.ForeignKey(Qualification, on_delete=models.DO_NOTHING, related_name='group_qualification', verbose_name='Квалификация')

    class Meta:
        db_table = 'group'
        verbose_name = "Группа"
        verbose_name_plural = "Группа"

    def __str__(self):
        return self.name


class StudentGroup(BaseModel):
    student = models.OneToOneField(Student, on_delete=models.DO_NOTHING, related_name='student_group_student')
    group = models.ForeignKey(Group, on_delete=models.DO_NOTHING, related_name='student_group_group')

    class Meta:
        db_table = 'student_group'
        verbose_name = "Группа студента"
        verbose_name_plural = "Группа студента"

