import json, random, django, os, sys

path = '/Users/bykov/work/azhar'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE']='main.settings'
django.setup()

from app.models import Student, Qualification

with open('./students.txt', 'r') as f:
    data = f.read()

    students = []
    q = Qualification.objects.all()

    for i in json.loads(data):
        students.append(Student(
            name=i['name'],
            surname=i['surname'],
            middle_name=i['middle_name'],
            birthday='1995-10-10',
            iin=i['iin'],
            nationality=i['nationality'],
            parents=i['parents'],
            education_lang=1,
            residence_address=i['residence_address'],
            residential_address=i['residential_address'],
            phone=i['phone'],
            avg_certificate=round(random.uniform(2, 5), 1),
            avg_subject=round(random.uniform(2, 5), 1),
            pay=1,
            education_type=1,
            status=1,
            qualification=q.filter(pk=random.randrange(start=1, stop=3)).first(),
        ))

    Student.objects.bulk_create(students)