from statement import HireStatement
from vessel_info import Vessel
from configparser import ConfigParser

def GenerateStatement_PDF(vessel=Vessel(), hireObj=HireStatement(), conf=ConfigParser(), ini_file_name=""):
    from fpdf import FPDF
    from tkinter import filedialog as fd, simpledialog as sd, messagebox as msgbox
    import os

    statement_title = f"{hireObj.on_hire.title()}-Hire Statement - {vessel.operator.name}"
    statement_subject=f"{hireObj.charterer.name} - {hireObj.project}"

    class JD_PDF(FPDF):
        def header(self) -> None:
            self.set_font(family='Tahoma', style='B', size=16)
            self.cell(w=160, h=8, txt=vessel.operator.name, ln=True, align='R')
            self.set_font(family='Arial', size=9)
            self.cell(w=160, h=4, txt=f"{vessel.operator.address}", ln=True, align='R')
            self.cell(w=160, h=4, txt=f"{vessel.operator.zip} {vessel.operator.city}", ln=True, align='R')
            self.cell(w=160, h=4, txt=f"{vessel.operator.phone}", ln=True, align='R')
            self.cell(w=160, h=4, txt=f"{vessel.operator.www}", ln=True, align='R', link=f"{vessel.operator.www}")
            self.cell(w=160, h=4, txt=f"{vessel.operator.vat}", ln=True, align='R')
            self.set_draw_color(r=168, g=143, b=94) # hex #A88F5E
            self.rect(x=5, y=5, w=200, h=287, style='S')
            self.image(name=vessel.operator.logo, x=174, y=12, h=26, w=26, link=f"{vessel.operator.www}")

        def footer(self) -> None:
            self.set_xy(x=0, y=280)
            self.set_text_color(r=168, g=143, b=94)
            self.set_font(family='Tahoma', size=8)
            self.cell(w=210, h=10, txt=f"{vessel.operator.name} • {vessel.operator.address} • {vessel.operator.zip} {vessel.operator.city} • {vessel.operator.phone} • {vessel.operator.www} • {vessel.operator.vat}", align='C', border=False)

    statement = JD_PDF()
    statement.add_font(family='Tahoma', fname="Tahoma Regular font.ttf", uni=True)
    statement.add_font(family='Tahoma', fname="TAHOMAB0.ttf", uni=True, style='B')
    statement.add_page()

    statement.set_left_margin(20)
    statement.set_author(author=vessel.master.name)
    statement.set_title(title=statement_title)
    statement.set_subject(statement_subject)
    statement.set_font(family='Arial', style='B', size=16)
    statement.cell(w=115, h=30, border=False, txt=f"Bunker {hireObj.on_hire.title()}-Hire Statement")
    statement.set_font(family='Arial', style='I', size=10)

    statement.cell(w=50, h=30, border=False, txt=f"{hireObj.date.strftime('%d/%m-%Y')}", ln=True)

    statement.set_font(family='Arial', style='B', size=10)
    statement.cell(w=50, h=10, border=False, txt=f"Charterer's Name:")
    statement.set_font(family='Arial', style='I', size=10)
    statement.cell(w=125, h=10, border=False, txt=f"{hireObj.charterer.name}", ln=True)
    statement.set_font(family='Arial', style='B', size=10)
    statement.cell(w=50, h=10, border=False, txt=f"Project:")
    statement.set_font(family='Arial', style='I', size=10)
    statement.cell(w=125, h=10, border=False, txt=f"{hireObj.project}", ln=True)
    statement.set_font(family='Arial', style='B', size=10)
    statement.cell(w=50, h=10, border=False, txt=f"Vessel Name:")
    statement.set_font(family='Arial', style='I', size=10)
    statement.cell(w=125, h=10, border=False, txt=f"{vessel.name}", ln=True)
    statement.set_font(family='Arial', style='B', size=10)
    statement.cell(w=50, h=10, border=False, txt=f"IMO Number:")
    statement.set_font(family='Arial', style='I', size=10)
    statement.cell(w=125, h=10, border=False, txt=f"{vessel.imo}", ln=True)

    statement.set_y(118)

    statement.set_font(family='Arial', style='B', size=10)
    statement.cell(w=50, h=10, border=False, txt=f"Consumable Survey", ln=True)
    statement.cell(w=50, h=10, border=False, txt=f"Marine Gas Oil:")
    statement.set_font(family='Arial', size=10)
    statement.cell(w=125, h=10, border=False, txt=f"{float(hireObj.mgo):,.1f} M3", ln=True)
    statement.set_font(family='Arial', style='B', size=10)
    statement.cell(w=50, h=10, border=False, txt=f"Lube Oil:")
    statement.set_font(family='Arial', size=10)
    statement.cell(w=125, h=10, border=False, txt=f"{float(hireObj.lo):,.0f} Ltr", ln=True)
    statement.set_font(family='Arial', style='B', size=10)
    statement.cell(w=50, h=10, border=False, txt=f"Fresh Water:")
    statement.set_font(family='Arial', size=10)
    statement.cell(w=125, h=10, border=False, txt=f"{float(hireObj.fw):,.1f} M3", ln=True)
    statement.set_font(family='Arial', style='B', size=10)
    statement.cell(w=50, h=10, border=False, txt=f"Date & Time:")

    ordinal = ""
    if hireObj.date.day in [1, 21, 31]:
        ordinal = "st"
    elif hireObj.date.day in [2, 22]:
        ordinal = "nd"
    elif hireObj.date.day in [3, 23]:
        ordinal = "rd"
    else:
        ordinal = "th"

    statement.cell(w=125, h=10, border=False, txt=f"{hireObj.date.strftime('%d')}{ordinal} {hireObj.date.strftime('%B %Y, at %H:%M LT')}", ln=True)
    statement.set_font(family='Arial', style='B', size=10)
    statement.cell(w=50, h=10, border=False, txt=f"Location:")
    statement.set_font(family='Arial', size=10)
    statement.cell(w=125, h=10, border=False, txt=f"{hireObj.location}")

    statement.set_y(220)

    statement.set_font(family='Arial', size=9)
    statement.cell(w=125, h=5, border=False, txt=f"On behalf of {vessel.operator.name}")
    statement.cell(w=50, h=5, border=False, txt=f"On behalf of Client", ln=True)
    
    statement.line(x1=20, y1=240, x2=70, y2=240)
    statement.line(x1=145, y1=240, x2=195, y2=240)

    statement.set_y(240)

    statement.set_font(family='Arial', style='BI', size=10)
    statement.cell(w=125, h=5, border=False, txt=f"{vessel.master.name}", ln=True)
    statement.set_font(family='Arial', style='I', size=10)
    statement.cell(w=125, h=5, border=False, txt=f"Master / {vessel.name}", ln=True)
    statement.set_font(family='Arial', size=10)
    statement.cell(w=125, h=5, border=False, txt=f"{vessel.owner.name}")
    statement.set_font(family='Arial', style='I', size=10)
    statement.cell(w=50, h=5, border=False, txt=f"{hireObj.charterer.name}", ln=True)

    try:
        filename = f"{hireObj.date.strftime('%Y-%m-%d')} - {hireObj.on_hire.title()}-hire - {hireObj.charterer.name}"

        filepath = fd.asksaveasfilename(title=f"Save {hireObj.on_hire.title()}-hire Statement...", 
                                        filetypes=(('PDF-files', '*.pdf'),('All files', '*.*')),
                                        initialdir=conf['Directory']['working'],
                                        initialfile=filename)

        if not (os.path.splitext(filepath)[1] == ".pdf"):
            filepath += ".pdf"
        
        statement.output(filepath, 'F')

        conf['Directory']['working'] = os.path.dirname(filepath)

        with open(ini_file_name, 'w', encoding='utf8') as inifile:
            conf.write(inifile)

        return filepath

    except PermissionError:
        print("PermissionError: Access to file demied")

        return ""

def InsertSignfields(filename=""):
    from pyhanko.sign.fields import SigFieldSpec, append_signature_field
    from pyhanko.pdf_utils.incremental_writer import IncrementalPdfFileWriter

    with open(filename, 'rb+') as doc:
        w = IncrementalPdfFileWriter(doc)
        owner_specs = SigFieldSpec(sig_field_name="owner_signature", on_page=0, box=(60, 165, 195, 200), empty_field_appearance=False)
        charterer_specs = SigFieldSpec(sig_field_name="charterer_signature", on_page=0, box=(415, 165, 550, 200), empty_field_appearance=False)
        append_signature_field(w, owner_specs)
        append_signature_field(w, charterer_specs)
        w.write_in_place()
