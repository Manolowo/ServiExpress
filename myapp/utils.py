from bs4 import BeautifulSoup
from django.http import HttpResponse
from django.template.loader import get_template
from io import BytesIO

from xhtml2pdf import pisa

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)

    # Eliminar elementos no deseados del HTML
    soup = BeautifulSoup(html, 'html.parser')
    elements_to_remove = ['button', 'form']
    
    for element_name in elements_to_remove:
        for tag in soup.find_all(element_name):
            tag.decompose()

    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(str(soup).encode("ISO-8859-1")), result)

    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')

    return None
