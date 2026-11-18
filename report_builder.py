import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, Image, HRFlowable
)
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT

def get_report_styles():
    c_primary = colors.HexColor('#1e3a8a')
    c_secondary = colors.HexColor('#0f172a')
    c_accent = colors.HexColor('#0284c7')
    c_dark = colors.HexColor('#1e293b')

    styles = {
        'c_primary': c_primary,
        'c_secondary': c_secondary,
        'c_accent': c_accent,
        'c_dark': c_dark,
        'cov_mini_style': ParagraphStyle('CovMini', fontName='Times-Bold', fontSize=16, leading=20, alignment=TA_CENTER, textColor=colors.black, spaceAfter=2),
        'cov_on_style': ParagraphStyle('CovOn', fontName='Times-Bold', fontSize=14, leading=18, alignment=TA_CENTER, textColor=colors.black, spaceAfter=10),
        'cov_title_style': ParagraphStyle('CovTitle', fontName='Times-Bold', fontSize=15, leading=19, alignment=TA_CENTER, textColor=colors.black, spaceAfter=14),
        'cov_submitted_style': ParagraphStyle('CovSubmitted', fontName='Times-Roman', fontSize=11, leading=15, alignment=TA_CENTER, textColor=colors.black, spaceAfter=4),
        'cov_degree_style': ParagraphStyle('CovDegree', fontName='Times-Bold', fontSize=13, leading=17, alignment=TA_CENTER, textColor=colors.black, spaceAfter=3),
        'cov_degree_word': ParagraphStyle('CovDegreeWord', fontName='Times-Roman', fontSize=11, leading=15, alignment=TA_CENTER, textColor=colors.black, spaceAfter=2),
        'cov_in_style': ParagraphStyle('CovIn', fontName='Times-Roman', fontSize=11, leading=15, alignment=TA_CENTER, textColor=colors.black, spaceAfter=2),
        'cov_dept_style': ParagraphStyle('CovDept', fontName='Times-Bold', fontSize=14, leading=18, alignment=TA_CENTER, textColor=colors.black, spaceAfter=14),
        'cov_by_style': ParagraphStyle('CovBy', fontName='Times-Bold', fontSize=11, leading=15, alignment=TA_CENTER, textColor=colors.black, spaceAfter=4),
        'cov_student_style': ParagraphStyle('CovStudent', fontName='Times-Bold', fontSize=11.5, leading=16, alignment=TA_CENTER, textColor=colors.black),
        'cov_supervision_style': ParagraphStyle('CovSupervision', fontName='Times-Bold', fontSize=11, leading=15, alignment=TA_CENTER, textColor=colors.black, spaceAfter=3),
        'cov_supervisor_name': ParagraphStyle('CovSupervisorName', fontName='Times-Bold', fontSize=12, leading=16, alignment=TA_CENTER, textColor=colors.black, spaceAfter=1),
        'cov_designation': ParagraphStyle('CovDesignation', fontName='Times-Roman', fontSize=11, leading=15, alignment=TA_CENTER, textColor=colors.black, spaceAfter=8),
        'cov_college_style': ParagraphStyle('CovCollege', fontName='Times-Bold', fontSize=13.5, leading=17, alignment=TA_CENTER, textColor=colors.black, spaceAfter=2),
        'cov_affiliated_style': ParagraphStyle('CovAffiliated', fontName='Times-Bold', fontSize=11, leading=15, alignment=TA_CENTER, textColor=colors.black, spaceAfter=2),
        'cov_univ_style': ParagraphStyle('CovUniv', fontName='Times-Bold', fontSize=11.5, leading=15.5, alignment=TA_CENTER, textColor=colors.black, spaceAfter=4),
        'cov_date_style': ParagraphStyle('CovDate', fontName='Times-Bold', fontSize=12, leading=16, alignment=TA_CENTER, textColor=colors.black),

        'prelim_heading_style': ParagraphStyle('PrelimHeading', fontName='Times-Bold', fontSize=14, leading=18, alignment=TA_CENTER, textColor=colors.black, spaceAfter=10),
        'prelim_body_style': ParagraphStyle('PrelimBody', fontName='Times-Roman', fontSize=11, leading=16.5, alignment=TA_JUSTIFY, textColor=c_dark, spaceAfter=10),
        'abstract_body_style': ParagraphStyle('AbstractBody', fontName='Times-Italic', fontSize=10.5, leading=15, alignment=TA_JUSTIFY, textColor=c_dark, spaceAfter=10),

        'toc_item_style': ParagraphStyle('TOCItem', fontName='Times-Roman', fontSize=9, leading=10.5, alignment=TA_LEFT, textColor=colors.black),
        'toc_item_bold': ParagraphStyle('TOCItemBold', fontName='Times-Bold', fontSize=9, leading=10.5, alignment=TA_LEFT, textColor=colors.black),
        'toc_page_style': ParagraphStyle('TOCPage', fontName='Times-Roman', fontSize=9, leading=10.5, alignment=TA_RIGHT, textColor=colors.black),
        'toc_page_bold': ParagraphStyle('TOCPageBold', fontName='Times-Bold', fontSize=9, leading=10.5, alignment=TA_RIGHT, textColor=colors.black),

        'chapter_num_style': ParagraphStyle('ChapterNum', fontName='Times-Bold', fontSize=13, leading=16, alignment=TA_CENTER, textColor=c_accent, spaceBefore=8, spaceAfter=12, keepWithNext=True),
        'chapter_title_style': ParagraphStyle('ChapterTitle', fontName='Times-Bold', fontSize=15, leading=19, alignment=TA_CENTER, textColor=c_primary, spaceBefore=2, spaceAfter=14, keepWithNext=True),
        'sec_head_style': ParagraphStyle('SecHead', fontName='Times-Bold', fontSize=11.5, leading=15, alignment=TA_LEFT, textColor=c_primary, spaceBefore=11, spaceAfter=4, keepWithNext=True),
        'subsec_head_style': ParagraphStyle('SubSecHead', fontName='Times-Bold', fontSize=10.5, leading=14, alignment=TA_LEFT, textColor=c_secondary, spaceBefore=8, spaceAfter=3, keepWithNext=True),
        'body_style': ParagraphStyle('ReportBody', fontName='Times-Roman', fontSize=9.5, leading=13.5, alignment=TA_JUSTIFY, textColor=c_dark, spaceAfter=5),
        'bullet_style': ParagraphStyle('ReportBullet', fontName='Times-Roman', fontSize=9.5, leading=13, alignment=TA_LEFT, leftIndent=15, textColor=c_dark, spaceAfter=3),
        'callout_style': ParagraphStyle('CalloutText', fontName='Times-Italic', fontSize=9, leading=12.5, alignment=TA_JUSTIFY, textColor=c_dark),
        'caption_style': ParagraphStyle('CaptionStyle', fontName='Times-Bold', fontSize=8.5, leading=11.5, alignment=TA_CENTER, textColor=c_secondary, spaceBefore=4, spaceAfter=8, keepWithNext=True),
        'table_title_style': ParagraphStyle('TableTitleStyle', fontName='Times-Bold', fontSize=8.5, leading=11.5, alignment=TA_CENTER, textColor=c_secondary, spaceBefore=7, spaceAfter=3, keepWithNext=True),
        'table_cell_style': ParagraphStyle('TableCell', fontName='Times-Roman', fontSize=8, leading=11, alignment=TA_LEFT, textColor=c_dark),
        'table_cell_bold': ParagraphStyle('TableCellBold', fontName='Times-Bold', fontSize=8, leading=11, alignment=TA_LEFT, textColor=c_dark),
        'table_cell_header': ParagraphStyle('TableCellHeader', fontName='Times-Bold', fontSize=8, leading=11, alignment=TA_CENTER, textColor=colors.white),
        'code_snippet_style': ParagraphStyle('CodeSnippet', fontName='Courier', fontSize=7.5, leading=9.5, textColor=colors.HexColor('#0f172a'), leftIndent=6),
        'ref_style': ParagraphStyle('RefLine', fontName='Times-Roman', fontSize=9.5, leading=13.5, alignment=TA_JUSTIFY, leftIndent=18, firstLineIndent=-18, spaceAfter=4, textColor=c_dark)
    }
    return styles
