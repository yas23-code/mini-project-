import os
import sys
import math
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak,
    KeepTogether, Image, HRFlowable, Flowable
)
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.pdfgen import canvas
import pypdf

from report_builder import get_report_styles
from report_sections_prelim import add_cover_and_prelim
from report_sections_chap1_2 import add_chapter1_and_2
from report_sections_chap3 import add_chapter3
from report_sections_chap4_5 import add_chapter4_5_and_end

# --- Flowable for Page Markers ---
class PageMarker(Flowable):
    def __init__(self, marker_type, header_title="", key=None):
        super().__init__()
        self.marker_type = marker_type
        self.header_title = header_title
        self.key = key

    def draw(self):
        self.canv.current_page_marker = self.marker_type
        self.canv.current_header_title = self.header_title

# --- Helper for Roman Numerals ---
def to_roman(n):
    vals = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
    syms = ['m', 'cm', 'd', 'cd', 'c', 'xc', 'l', 'xl', 'x', 'ix', 'v', 'iv', 'i']
    res = ''
    for v, s in zip(vals, syms):
        while n >= v:
            res += s
            n -= v
    return res

# --- Two-Pass Custom Canvas ---
class CompleteAcademicCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []
        self.current_page_marker = 'COVER'
        self.current_header_title = ''

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        chapter1_idx = None
        for idx, state in enumerate(self._saved_page_states):
            marker = state.get('current_page_marker', '')
            if marker.startswith('CHAPTER'):
                chapter1_idx = idx
                break
        if chapter1_idx is None:
            chapter1_idx = 10

        total_chapter_pages = num_pages - chapter1_idx

        for idx, state in enumerate(self._saved_page_states):
            self.__dict__.update(state)
            marker = state.get('current_page_marker', 'COVER')
            header_title = state.get('current_header_title', '')
            width, height = A4
            margin_left = 50
            margin_right = width - 50

            self.saveState()

            if marker == 'COVER':
                # Official outer frame border strictly as per institutional template format
                self.setStrokeColor(colors.black)
                self.setLineWidth(1.5)
                self.rect(34, 30, width - 68, height - 60)
                self.setLineWidth(0.6)
                self.rect(36.5, 32.5, width - 73, height - 65)
            elif marker == 'PRELIM':
                prelim_roman = to_roman(idx + 1)
                self.setFont('Times-Italic', 8.5)
                self.setFillColor(colors.HexColor('#64748b'))
                self.drawRightString(margin_right, height - 34, "CrimeLens 2.0: AI-Powered Public Safety Suite")
                self.setStrokeColor(colors.HexColor('#cbd5e1'))
                self.setLineWidth(0.6)
                self.line(margin_left, height - 38, margin_right, height - 38)
                self.setFont('Times-Roman', 9.5)
                self.setFillColor(colors.HexColor('#1e293b'))
                self.drawCentredString(width / 2.0, 32, prelim_roman)
            else:
                chapter_page = idx - chapter1_idx + 1
                display_title = header_title if header_title else "CrimeLens 2.0"
                self.setFont('Times-BoldItalic', 8.5)
                self.setFillColor(colors.HexColor('#1e3a8a'))
                self.drawString(margin_left, height - 34, display_title)
                self.setFont('Times-Italic', 8)
                self.setFillColor(colors.HexColor('#64748b'))
                self.drawRightString(margin_right, height - 34, "Dept of CSE, ABESEC")
                self.setStrokeColor(colors.HexColor('#94a3b8'))
                self.setLineWidth(0.6)
                self.line(margin_left, height - 38, margin_right, height - 38)

                self.setStrokeColor(colors.HexColor('#cbd5e1'))
                self.setLineWidth(0.6)
                self.line(margin_left, 42, margin_right, 42)
                self.setFont('Times-Roman', 7.5)
                self.setFillColor(colors.HexColor('#64748b'))
                self.drawString(margin_left, 30,
                    "Team: Utkarsh (1209), Vaibhav (1215), Vanshika (1229), Yash (1296) | Guide: Ms. Anuksha Srivastav | HOD: Dr. Pankaj Sharma")
                self.setFont('Times-Bold', 8.5)
                self.setFillColor(colors.HexColor('#0f172a'))
                self.drawRightString(margin_right, 30, f"Page {chapter_page} of {total_chapter_pages}")

            self.restoreState()
            super().showPage()
        super().save()

def generate_report(output_path="CrimeLens_BTech_Project_Report.pdf"):
    fig_dir = os.path.dirname(os.path.abspath(__file__))
    styles = get_report_styles()
    content_width = 495

    # Exact TOC mapping verified across all 26 chapter pages
    toc_mapping = {
        'c1': '1',
        'c1_1': '1',
        'c1_2': '1',
        'c1_3': '2',
        'c1_4': '2',
        'c1_5': '3',
        'c1_6': '4',
        'c2': '5',
        'c2_1': '5',
        'c2_2': '6',
        'c2_3': '6',
        'c2_7': '7',
        'c3': '9',
        'c3_1': '9',
        'c3_2': '10',
        'c3_3': '10',
        'c3_4': '11',
        'c3_5': '11',
        'c3_6': '12',
        'c4': '14',
        'c4_1': '14',
        'c4_6': '17',
        'c4_7': '17',
        'c5': '21',
        'c5_1': '21',
        'c5_2': '21',
        'app': '24',
        'ref': '26'
    }

    story = []
    # 1. Cover & 9 Preliminary Pages (Pages 1 to 10)
    add_cover_and_prelim(story, PageMarker, styles, fig_dir, toc_mapping=toc_mapping)
    # 2. Chapters 1 & 2 (Chapter Pages 1 to 8)
    add_chapter1_and_2(story, PageMarker, styles, fig_dir, content_width)
    # 3. Chapter 3 (Chapter Pages 9 to 12)
    add_chapter3(story, PageMarker, styles, fig_dir, content_width)
    # 4. Chapters 4, 5, Appendix, References (Chapter Pages 13 to 22)
    add_chapter4_5_and_end(story, PageMarker, styles, fig_dir, content_width)

    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=50,
        rightMargin=50,
        topMargin=46,
        bottomMargin=48
    )

    doc.build(story, canvasmaker=CompleteAcademicCanvas)
    print(f"Report compiled successfully: {output_path}")

    reader = pypdf.PdfReader(output_path)
    total_pages = len(reader.pages)
    chapter_pages = total_pages - 10
    print(f"Total Pages: {total_pages} (1 Cover + 9 Prelim + {chapter_pages} Chapter Pages)")
    assert chapter_pages > 20, f"Error: Chapter pages ({chapter_pages}) must exceed 20 pages!"

if __name__ == "__main__":
    generate_report()
