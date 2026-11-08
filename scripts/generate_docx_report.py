"""Script to generate Pakistan Agriculture Expert System project report docx file.
Adheres strictly to user instructions:
- Table of Contents with bulleted entries and dotted leaders (. . . 1)
- 1-paragraph simple Introduction
- 4-line Problem Statement paragraph
- Requirements with 2-column tables (Functional and Non-Functional from expert-system.md)
- Empty placeholder spaces for High Level Design, Code Explanation, and Results
- 5-line Summary paragraph
- Main headings formatted strictly as Bold, Italic, and Underlined
- 100% black font color, zero colors or colored table shading
"""

import os
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement
from docx.oxml.ns import qn


def set_cell_border(cell, **kwargs):
    """Set black borders on a docx table cell."""
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcBorders = OxmlElement('w:tcBorders')
    for edge in ('top', 'left', 'bottom', 'right'):
        edge_data = kwargs.get(edge)
        if edge_data:
            tag = f'w:{edge}'
            element = OxmlElement(tag)
            element.set(qn('w:val'), edge_data.get('val', 'single'))
            element.set(qn('w:sz'), str(edge_data.get('sz', 4)))
            element.set(qn('w:space'), '0')
            element.set(qn('w:color'), edge_data.get('color', '000000'))
            tcBorders.append(element)
    tcPr.append(tcBorders)


def add_main_heading(doc: Document, text: str):
    """Add a main heading formatted strictly as Bold, Italic, and Underlined in pure black."""
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = "Times New Roman"
    run.font.size = Pt(14)
    run.font.bold = True
    run.font.italic = True
    run.font.underline = True
    run.font.color.rgb = RGBColor(0, 0, 0)
    return p


def add_subheading(doc: Document, text: str):
    """Add a subheading formatted in black bold font."""
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = "Times New Roman"
    run.font.size = Pt(12)
    run.font.bold = True
    run.font.color.rgb = RGBColor(0, 0, 0)
    return p


def add_body_paragraph(doc: Document, text: str):
    """Add standard body paragraph in pure black text."""
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.line_spacing = 1.15
    run = p.add_run(text)
    run.font.name = "Times New Roman"
    run.font.size = Pt(11)
    run.font.color.rgb = RGBColor(0, 0, 0)
    return p


def build_document(output_path: str):
    doc = Document()

    # Configure 1-inch margins
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # Document Title
    title_p = doc.add_paragraph()
    title_p.paragraph_format.space_before = Pt(0)
    title_p.paragraph_format.space_after = Pt(12)
    title_run = title_p.add_run("Pakistan Agriculture Expert System — Project Report")
    title_run.font.name = "Times New Roman"
    title_run.font.size = Pt(18)
    title_run.font.bold = True
    title_run.font.color.rgb = RGBColor(0, 0, 0)

    # 1. Table of Contents
    add_main_heading(doc, "Table of Contents")

    toc_items = [
        ("1. Introduction", "1"),
        ("2. Problem Statement", "2"),
        ("3. Requirements", "3"),
        ("   • 3.1 Functional Requirements", "3"),
        ("   • 3.2 Non-Functional Requirements", "4"),
        ("4. High Level Design", "5"),
        ("5. Code Explanation", "6"),
        ("6. Results", "7"),
        ("7. Summary", "8"),
    ]

    for item_text, page_num in toc_items:
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(1)
        p.paragraph_format.space_after = Pt(2)
        # Bullet entry with dots
        run1 = p.add_run(f"•  {item_text} ")
        run1.font.name = "Times New Roman"
        run1.font.size = Pt(11)
        run1.font.color.rgb = RGBColor(0, 0, 0)

        run_dots = p.add_run("......................................................................................................."[:42])
        run_dots.font.name = "Times New Roman"
        run_dots.font.size = Pt(11)
        run_dots.font.color.rgb = RGBColor(0, 0, 0)

        run_page = p.add_run(f" {page_num}")
        run_page.font.name = "Times New Roman"
        run_page.font.size = Pt(11)
        run_page.font.bold = True
        run_page.font.color.rgb = RGBColor(0, 0, 0)

    # Page Break after TOC
    doc.add_page_break()

    # 2. Introduction (Only 1 paragraph in simple easy terms)
    add_main_heading(doc, "1. Introduction")
    intro_text = (
        "The Pakistan Agriculture Expert System is an easy-to-use digital assistant created to help local "
        "farmers quickly identify crop problems and protect their harvest. Agriculture is the backbone of "
        "Pakistan's economy, yet many farmers struggle to get timely advice when their crops face sudden diseases, "
        "destructive insect pests, or poor soil fertility across major crops like Wheat, Cotton, Rice, Sugarcane, "
        "and Maize. By asking simple questions about visible symptoms and soil conditions, this system uses built-in "
        "agricultural rules to give farmers instant diagnosis, safe treatment recommendations, and exact fertilizer "
        "quantities directly through any web browser."
    )
    add_body_paragraph(doc, intro_text)

    # 3. Problem Statement (Exactly 4 lines in one single paragraph)
    add_main_heading(doc, "2. Problem Statement")
    problem_text = (
        "Smallholder farmers across Pakistan experience severe yield losses because access to qualified agricultural extension officers is scarce and laboratory testing remains slow and expensive.\n"
        "Without timely diagnostic support, growers routinely misidentify foliage infections, spray incorrect chemical pesticides, and misjudge soil macronutrient deficiencies.\n"
        "This uncontrolled chemical application raises farm operational expenses, accelerates insect pest immunity, and leaves hazardous pesticide residues in food grain crops.\n"
        "Consequently, there is an urgent need for an automated, accessible expert advisory tool that delivers immediate, validated agronomic guidance to protect national crop production."
    )
    add_body_paragraph(doc, problem_text)

    # 4. Requirements
    add_main_heading(doc, "3. Requirements")

    # 4.1 Functional Requirements
    add_subheading(doc, "3.1 Functional Requirements")
    add_body_paragraph(doc, "The functional requirements define the core operational features provided by the expert system to the farmer, directly transcribed from expert-system.md:")

    func_reqs = [
        ("Disease Identification", "App identifies disease of crop."),
        ("Disease Solution", "App provides disease solution after identification."),
        ("Disease Input Form", "App takes crop disease information from farmer."),
        ("Pest Identification", "App identifies pest."),
        ("Pest Solution", "App provides pest solution after identification."),
        ("Pest Input Form", "App takes pest information from the farmer."),
        ("Nutrient Deficiency", "App identifies soil deficiencies from foliage signs."),
        ("Fertilizer Prescription", "App calculates exact fertilizer dosage (NPK) and soil fix."),
        ("Nutrient Input Form", "App takes leaf discoloration patterns, crop stage, and soil pH.")
    ]

    table_func = doc.add_table(rows=1, cols=2)
    table_func.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_func.autofit = False

    # Header row
    hdr_cells = table_func.rows[0].cells
    hdr_cells[0].width = Inches(2.3)
    hdr_cells[1].width = Inches(4.2)
    for idx, text in enumerate(["Requirement", "Description"]):
        cell = hdr_cells[idx]
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.space_after = Pt(4)
        run = p.add_run(text)
        run.font.name = "Times New Roman"
        run.font.size = Pt(11)
        run.font.bold = True
        run.font.color.rgb = RGBColor(0, 0, 0)
        set_cell_border(cell, top={'sz': 8, 'val': 'single', 'color': '000000'},
                             bottom={'sz': 8, 'val': 'single', 'color': '000000'},
                             left={'sz': 4, 'val': 'single', 'color': '000000'},
                             right={'sz': 4, 'val': 'single', 'color': '000000'})

    for req, desc in func_reqs:
        row_cells = table_func.add_row().cells
        row_cells[0].width = Inches(2.3)
        row_cells[1].width = Inches(4.2)
        for idx, text in enumerate([req, desc]):
            cell = row_cells[idx]
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(3)
            p.paragraph_format.space_after = Pt(3)
            run = p.add_run(text)
            run.font.name = "Times New Roman"
            run.font.size = Pt(10.5)
            run.font.color.rgb = RGBColor(0, 0, 0)
            set_cell_border(cell, top={'sz': 4, 'val': 'single', 'color': '000000'},
                                 bottom={'sz': 4, 'val': 'single', 'color': '000000'},
                                 left={'sz': 4, 'val': 'single', 'color': '000000'},
                                 right={'sz': 4, 'val': 'single', 'color': '000000'})

    # 4.2 Non-Functional Requirements
    add_subheading(doc, "3.2 Non-Functional Requirements")
    add_body_paragraph(doc, "The non-functional requirements define the system's operational constraints, performance thresholds, and architectural reliability criteria:")

    non_func_reqs = [
        ("Performance & Latency", "Inference engine evaluates rule chain in < 1.0 second."),
        ("Fault Tolerance & Robustness", "Malformed inputs trigger friendly error alerts without Python traceback crashes."),
        ("UI Responsiveness", "Streamlit page reloads in < 500ms."),
        ("Scalable", "In future, if new features planned, easy to scale.")
    ]

    table_non_func = doc.add_table(rows=1, cols=2)
    table_non_func.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_non_func.autofit = False

    hdr_nf_cells = table_non_func.rows[0].cells
    hdr_nf_cells[0].width = Inches(2.3)
    hdr_nf_cells[1].width = Inches(4.2)
    for idx, text in enumerate(["Requirement", "Description"]):
        cell = hdr_nf_cells[idx]
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.space_after = Pt(4)
        run = p.add_run(text)
        run.font.name = "Times New Roman"
        run.font.size = Pt(11)
        run.font.bold = True
        run.font.color.rgb = RGBColor(0, 0, 0)
        set_cell_border(cell, top={'sz': 8, 'val': 'single', 'color': '000000'},
                             bottom={'sz': 8, 'val': 'single', 'color': '000000'},
                             left={'sz': 4, 'val': 'single', 'color': '000000'},
                             right={'sz': 4, 'val': 'single', 'color': '000000'})

    for req, desc in non_func_reqs:
        row_cells = table_non_func.add_row().cells
        row_cells[0].width = Inches(2.3)
        row_cells[1].width = Inches(4.2)
        for idx, text in enumerate([req, desc]):
            cell = row_cells[idx]
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(3)
            p.paragraph_format.space_after = Pt(3)
            run = p.add_run(text)
            run.font.name = "Times New Roman"
            run.font.size = Pt(10.5)
            run.font.color.rgb = RGBColor(0, 0, 0)
            set_cell_border(cell, top={'sz': 4, 'val': 'single', 'color': '000000'},
                                 bottom={'sz': 4, 'val': 'single', 'color': '000000'},
                                 left={'sz': 4, 'val': 'single', 'color': '000000'},
                                 right={'sz': 4, 'val': 'single', 'color': '000000'})

    # 5. High Level Design (Empty space left for user)
    add_main_heading(doc, "4. High Level Design")
    for _ in range(8):
        doc.add_paragraph()

    # 6. Code Explanation (Empty space left for user)
    add_main_heading(doc, "5. Code Explanation")
    for _ in range(8):
        doc.add_paragraph()

    # 7. Results (Empty space left for user)
    add_main_heading(doc, "6. Results")
    for _ in range(8):
        doc.add_paragraph()

    # 8. Summary (Exactly 5 lines in one single paragraph)
    add_main_heading(doc, "7. Summary")
    summary_text = (
        "The Pakistan Agriculture Expert System provides an intelligent, accessible diagnostic platform tailored for Pakistani farming conditions across five major economic cash and food crops.\n"
        "By implementing a modular forward-chaining inference engine in pure Python, the system evaluates more than sixty codified agricultural rules in sub-millisecond execution times.\n"
        "The intuitive Streamlit web interface guides farmers through disease identification, pest management with pre-harvest safety controls, and precise soil nutrient prescriptions.\n"
        "Its transparent four-step explanation module and calibrated certainty factor scoring build user trust while maintaining strict adherence to known system boundaries.\n"
        "Ultimately, this digital agronomy assistant empowers rural growers with expert decision support, reducing unnecessary crop loss and optimizing chemical input sustainability."
    )
    add_body_paragraph(doc, summary_text)

    # Save document
    doc.save(output_path)
    print(f"Document successfully saved to: {output_path}")


if __name__ == "__main__":
    out_file = "/home/prx/Projects/expert-system/Project_Report_Expert_System.docx"
    build_document(out_file)
