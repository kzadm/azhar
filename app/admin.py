from django import forms
from django.contrib import admin, messages
from django.contrib.admin import ModelAdmin
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.http import HttpResponse
from .models import (
    Student, Specialization, Qualification,
    Group, StudentGroup
)
from .services import generate_students_word


def distribute_students(students, n):
    sorted_students = sorted(students, key=lambda student: student.avg_certificate)
    groups = [[] for _ in range(n)]
    while sorted_students:
        for i in range(n):
            if sorted_students:
                groups[i].append(sorted_students.pop(0))
            if sorted_students:
                groups[i].append(sorted_students.pop())

    return groups


@admin.register(Qualification)
class SpecializationAdmin(ModelAdmin):
    list_display = ('name', 'specialization', 'get_total_students', 'get_total_unassigned_students')
    search_fields = ['name', 'specialization__name']
    actions = ('assign_students',)

    @admin.action(description="Распределить студентов по группам")
    def assign_students(self, request, queryset):
        print(queryset)
        for qualification in queryset:
            students = qualification.student_qualification.all()
            groups = qualification.group_qualification.all()
            groups_count = len(groups)
            results = distribute_students(students, groups_count)
            for i, result in enumerate(results):
                student_group = []
                StudentGroup.objects.filter(group=groups[i]).delete()
                for j in result:
                    student_group.append(StudentGroup(student=j, group=groups[i]))
                StudentGroup.objects.bulk_create(student_group)
        self.message_user(
            request,
            'Распределение выполнено',
            messages.SUCCESS,
        )

    @admin.display(description='Всего студентов')
    def get_total_students(self, obj):
        data = obj.student_qualification.count()
        return data
    
    @admin.display(description='Всего нераспределенных студентов')
    def get_total_unassigned_students(self, obj):
        return obj.student_qualification.filter(student_group_student__isnull=True).count()


@admin.register(Student)
class StudentAdmin(ModelAdmin):
    list_display = ('get_fio', 'iin', 'avg_certificate', 'avg_subject', 'status', 'get_qualification', 'get_group')
    search_fields = ['surname', 'name', 'middle_name', 'qualification__name', 'student_group_student__group__name']

    @admin.display(description='Квалификация')
    def get_qualification(self, obj):
        return obj.qualification.name
    
    @admin.display(description='Группа')
    def get_group(self, obj):
        return obj.student_group_student.group.name if obj.student_group_student is not None else None
    
    @admin.display(description='ФИО')
    def get_fio(self, obj):
        return f'{obj.surname} {obj.name} {obj.middle_name}'


class GroupFormAdmin(forms.ModelForm):
    students = forms.ModelMultipleChoiceField(
        queryset=Student.objects.none(),
        required=False,
        widget=FilteredSelectMultiple(verbose_name="Студенты", is_stacked=False)
    )

    def __init__(self, *args, **kwargs):
        super(GroupFormAdmin, self).__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            print(self.instance.qualification.id)
            print(Student.objects.filter(qualification_id=self.instance.qualification.id).all())
            self.fields['students'].queryset = Student.objects.filter(qualification=self.instance.qualification)
            self.fields['students'].initial = [i.student for i in self.instance.student_group_group.select_related('student').all()]

    def clean(self):
        ids = [i.id for i in self.cleaned_data['students']]
        exists_students = StudentGroup.objects.filter(student_id__in=ids).exclude(group_id=self.instance.id).select_related('student').all()
        if len(exists_students):
            raise forms.ValidationError('Студент {} уже добавлен в другую группу'.format(
                ', '.join([f'{i.student.surname} {i.student.name} {i.student.middle_name}' for i in exists_students])
            ))

    
    def save(self, commit=True):
        group = super(GroupFormAdmin, self).save(commit=False)

        if commit:
            group.save()
        if group.pk:
            StudentGroup.objects.filter(group_id=group.pk).delete()
            group_students = []
            for i in self.cleaned_data['students']:
                group_students.append(StudentGroup(student_id=i.id, group_id=group.pk))
            StudentGroup.objects.bulk_create(group_students)

        return group

        


@admin.register(Group)
class GroupAdmin(ModelAdmin):
    list_display = ('name', 'qualification', 'get_specialization', 'get_students_count', 'get_average_score')
    search_fields = ['name', 'qualification__name', 'qualification__specialization__name']
    actions = ('generate_excel',)
    form = GroupFormAdmin

    @admin.action(description="Сформировать сведения о студентах")
    def generate_excel(self, request, queryset):
        if len(queryset) > 1:
            self.message_user(
                request,
                'Выберите только одну группу',
                messages.WARNING,
            )
            return False
        group = queryset[0]
        pages = {}
        # for i in queryset:
        students = Student.objects.filter(student_group_student__group__id=group.id).all()
        data = {
            "group_name": queryset[0].name,
            "students": [],
            "specialization": group.qualification.specialization.name,
            "specialization_number": group.qualification.specialization.number,
            "qualification": group.qualification.name,
            "qualification_number": group.qualification.number

        }
        counter = 1
        for student in students:
            data['students'].append({
                'counter': counter,
                'fio': f'{student.surname} {student.surname} {student.middle_name}',
                'birthday': student.birthday.strftime('%d.%m.%Y'),
                'phone': student.phone,
                'parents': student.parents,
                'residential_address': student.residential_address,
                'nationality': student.nationality,
                'iin': student.iin
            })
            counter += 1

        document, document_name = generate_students_word(data)
        print(document_name)
        response = HttpResponse(document, content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        # response = HttpResponse()
        response['Content-Disposition'] = f'attachment; filename="{document_name}"'
        return response

    @admin.display(description='Количество студентов')
    def get_students_count(self, obj):
        return obj.student_group_group.count()
    

    @admin.display(description='Средний балл')
    def get_average_score(self, obj):
        data = obj.student_group_group.select_related('student').all()
        avg = 0
        for i in data:
            avg += i.student.avg_certificate
        return round(avg / len(data), 1) if len(data) else 0


    @admin.display(description='Специальность')
    def get_specialization(self, obj):
        return obj.qualification.specialization.name


admin.site.register(Specialization)