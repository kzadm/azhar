import docx
from io import BytesIO
from docxtpl import DocxTemplate
from main.settings import MEDIA_URL


def generate_students_word(data):
    # ('№', 'Ф.И.О. студента', 'Дата рождения', 'Тел.', 'Ф.И.О. родителей, контактные тел.', 'Место жительства', 'Национ.', 'ИИН',)
    context = {}

    context['group_name'] = data['group_name']
    context['specialization'] = data['specialization']
    context['specialization_number'] = data['specialization_number']
    context['qualification'] = data['qualification']
    context['qualification_number'] = data['qualification_number']
    context['students'] = data['students']

    return generate_template(f"{MEDIA_URL}/students.docx", context, f'svedeniya.docx')


def generate_order_word(data):
    context = {}

    context['specialization'] = data['specialization']
    context['specialization_number'] = data['specialization_number']
    context['qualification'] = data['qualification']
    context['qualification_number'] = data['qualification_number']
    context['students'] = data['students']

    return generate_template(f"{MEDIA_URL}/order.docx", context, f'order.docx')


def generate_template(file_path, context, filename='test.docx'):
    doc = docx.Document()
    buffer = BytesIO()
    doc.save(buffer)
    
    tpl = DocxTemplate(file_path)
    tpl.render(context)
    modified_buffer = BytesIO()
    tpl.save(modified_buffer)
    modified_buffer.seek(0)

    return modified_buffer.getvalue(), filename