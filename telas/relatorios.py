import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, PageTemplate, Frame
from reportlab.platypus import Paragraph, Spacer, ListFlowable, ListItem


class Relatorios():
    def __init__(self,
                 filename:str = None, 
                 logo:str = None,
                 size:any= letter,
                 left_margin:int=0.75,
                 right_margin:int=0.75, 
                 top_margin:int=1.5 , 
                 bottom_margin:int=1.5 ,
                 title_font_Size:int = 16,
                 title_text_color:any = colors.black,
                 title_back_color:any = None,
                 title_alignment:int = 1,
                 title_text:str = None, 
                 footer_text:str = None                
                 ):
        self.master             = self
        self.logo               = logo
        self.content            = []
        self.pagesize           = size
        self.leftMargin         = left_margin * inch
        self.rightMargin        = right_margin * inch
        self.topMargin          = top_margin * inch
        self.bottomMargin       = bottom_margin* inch
        
        if self.logo == None:
            self.logo = os.path.join(os.path.dirname(os.path.realpath(os.path.dirname(os.path.realpath(__file__)))), "img" + os.sep + "logo.png")
        
        if filename == None:
            filename = "arquivo.pdf"

        self.path = os.path.join(os.path.dirname(os.path.realpath(os.path.dirname(os.path.realpath(__file__)))), "_tmps" + os.sep + filename)      
              
        self.doc = SimpleDocTemplate(self.path, pagesize =self.pagesize, leftMargin=self.leftMargin, 
                                    rightMargin=self.rightMargin, topMargin=self.topMargin, bottomMargin=self.bottomMargin)

        styles = getSampleStyleSheet()
        
        title_style = ParagraphStyle('TableTitle', parent=styles['Title'])
        title_style.fontSize  = title_font_Size
        title_style.textColor = title_text_color
        title_style.backColor = title_back_color
        title_style.alignment = title_alignment

        def header(canvas, doc):
            canvas.saveState()
            canvas.drawImage(self.logo, doc.leftMargin, doc.height + doc.topMargin - 0.1 * inch, width=1.5 * inch, height=1.5 * inch)
            if title_text != None:
                title = Paragraph(title_text, title_style)
                title.wrapOn(canvas, doc.width, doc.topMargin)
                title.drawOn(canvas, doc.leftMargin, doc.height + doc.topMargin)
            canvas.restoreState()
        
        def footer(canvas, doc):
            if footer_text!= None:
                canvas.saveState()
                footer = Paragraph(f"<i>{footer_text}</i>", self.styles['Normal'])
                footer.wrapOn(canvas, doc.width, doc.bottomMargin)
                footer.drawOn(canvas, doc.leftMargin, doc.bottomMargin - 2 * inch)
                canvas.restoreState()
            
        frame = Frame(self.doc.leftMargin, self.doc.bottomMargin, self.doc.width, self.doc.height - 2 * inch, id='normal')
        page_template = PageTemplate(id='main', onPage=header, onPageEnd=footer, frames=[frame])
        self.doc.addPageTemplates([page_template])
        
    
    def paragraph(self, fontSize:int = 12, alignment:int = 1, text:str = None, textColor=colors.black, backColor=colors.white):
        style = ParagraphStyle('HinoTitleStyle')
        style.fontName = 'Helvetica-Bold'
        style.fontSize = fontSize
        style.alignment = alignment
        style.textColor = textColor
        style.backColor = backColor   
        paragraph = Paragraph(text, style)       
        self.content.append(paragraph) 
        
    def add_table(self,
                 table_back_ground = colors.black,
                 table_text_color = colors.white,
                 table_text_align = "CENTER",
                 table_color_grid = colors.black,                 
                 cel_back_color = colors.lightgrey,
                 table_full=True,
                 colWidths=[],
                 data = []):
        
        colWidths = [valor * inch for valor in colWidths]
        total_table_width = sum(colWidths)
        total_table_width_com_margin = total_table_width + self.leftMargin    
        if table_full==True:
            colWidths = [w / total_table_width_com_margin * self.pagesize[0] for w in colWidths]
        
        table = Table(data, colWidths=colWidths, rowHeights=0.4 * inch)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), table_back_ground),
            ('TEXTCOLOR', (0, 0), (-1, 0), table_text_color),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('ALIGN', (0, 0), (-1, 0), table_text_align),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
            ('GRID', (0, 0), (-1, -1), 1, table_color_grid)
        ]))
        
        self.content.append(Spacer(1, -1.5 * inch)) 
        self.content.append(table)
        
    def build(self):       
        self.doc.build(self.content)   
        