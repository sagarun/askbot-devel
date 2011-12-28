from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph,SimpleDocTemplate,Spacer
from reportlab.platypus.paragraph import FragLine
from reportlab.lib.styles import ParagraphStyle as PS
from django.http import HttpResponse
from askbot.models import Question, Answer, Comment
from askbot.conf import settings as askbot_settings
from StringIO import StringIO
from reportlab.lib.units import inch
from reportlab.graphics.shapes import Line,PolyLine


def to_pdf(request,question_id):
    """ Export to pdf """
    
    question_object = Question.objects.filter(id=question_id)
    if question_object.exists() == True:
        question_title = question_object.values()[0].get('title')
        question_body = question_object.values()[0].get('html')
    
  
    pdf_filename = question_title.replace(' ','_')+".pdf"
    buffer = StringIO()
    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=%s' % pdf_filename

    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
    pdftext = []
    h1 = PS(name = 'Heading1', fontSize = 14, leading = 16)
    h2 = PS(name = 'Heading2', fontSize = 12, leading = 14)
    pdftext.append(Paragraph('Question', h1)) 
    pdftext.append(Spacer(1,0.25*inch))
    pdftext.append(Paragraph(question_title, h2))
    pdftext.append(Spacer(1,0.15*inch))
    pdftext.append(Paragraph(question_body, PS('body')))
    pdftext.append(Spacer(1,0.25*inch))
    pdftext.append(Paragraph('Answer', h1))
    pdftext.append(Spacer(1,0.15*inch))

    answers = Answer.objects.filter(question=question_id)
    if answers.exists() == True:
      for answer in answers:
          pdftext.append(Paragraph(answer.html, PS('body')))
          pdftext.append(Spacer(1, 0.10*inch))
        
    doc.build(pdftext)
    response.write(buffer.getvalue())
    buffer.close()
    return response
