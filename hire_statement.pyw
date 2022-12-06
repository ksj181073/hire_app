import tkinter as tk
from datetime import datetime
from configparser import ConfigParser
from vessel_info import Vessel
from statement import HireStatement
from PdfGenerator import InsertSignfields, GenerateStatement_PDF
from tkinter import filedialog as fd, messagebox as msgbox

import os
from PIL import Image as Pillow_Img, ImageTk as Pillow_Img_Tk

ini_file_name = "on_off_hire.ini"
conf = ConfigParser()
conf.read(ini_file_name, encoding='utf8')

vessel = Vessel()

vessel.operator.name = conf['Operator']['Name']
vessel.operator.address = conf['Operator']['Address']
vessel.operator.zip = conf['Operator']['Zip']
vessel.operator.city = conf['Operator']['City']
vessel.operator.phone = conf['Operator']['Phone']
vessel.operator.www = conf['Operator']['www']
vessel.operator.vat = conf['Operator']['VAT']

vessel.operator.icon = conf['Operator']['Icon']
vessel.operator.logo = conf['Operator']['Logo']

vessel.owner.name = conf['Owner']['Name']

vessel.name = conf['Vessel']['Name']
vessel.imo = conf['Vessel']['IMO']
vessel.master.name = conf["Vessel"]['Master']

def Main():
    RunGui()

def RunGui():
    root = Gui()
    root.mainloop()

def Gui():
    mainwin = tk.Tk()
    
    vessel_name = tk.StringVar()
    vessel_name.set(vessel.name)
    vessel_imo = tk.StringVar()
    vessel_imo.set(vessel.imo)
    master_name = tk.StringVar()
    master_name.set(vessel.master.name)

    on_off_hire_choice = tk.StringVar()
    on_off_hire_choice.set("on")

    # consumable_mgo = tk.DoubleVar()
    # consumable_lo = tk.IntVar()
    # consumable_fw = tk.DoubleVar()

    consumable_mgo = tk.StringVar()
    consumable_lo = tk.StringVar()
    consumable_fw = tk.StringVar()

    date_day = tk.IntVar()
    date_month = tk.IntVar()
    date_year = tk.IntVar()
    time_hr = tk.IntVar()
    time_min = tk.IntVar()

    location = tk.StringVar()

    charterer_name = tk.StringVar()
    project = tk.StringVar()

    app_width = 570
    app_height = 430
    app_x = 500
    app_y = 300

    screen_width = mainwin.winfo_screenwidth()
    screen_height = mainwin.winfo_screenheight()

    app_x = int((screen_width - app_width) / 2)
    app_y = int((screen_height - app_height) / 2)

    mainwin.title(f"On-Hire Statement - {vessel.operator.name}")
    mainwin.geometry(f"{app_width}x{app_height}+{app_x}+{app_y}")
 
    mainwin.minsize(width=app_width, height=app_height)
    mainwin.maxsize(width=app_width, height=app_height)

    try:
        mainwin.iconbitmap(vessel.operator.icon)
    except:
        pass

    input_frame = tk.Frame(mainwin)

    on_off_frame = tk.Frame(input_frame)
    tk.Radiobutton(on_off_frame, variable=on_off_hire_choice, text="On-hire", value="on").grid(row=0, column=0)
    tk.Radiobutton(on_off_frame, variable=on_off_hire_choice, text="Off-hire", value="off").grid(row=0, column=1)
    on_off_frame.grid(padx=5, pady=5, sticky=tk.W)

    def validate_imo(user_input, widgettext, widgettextafter, widgetname):
        if user_input.isdigit() and len(widgettextafter) <= 7:
            return True

        elif user_input == "":
            return True

        else:
            return False
    
    valimo = (mainwin.register(validate_imo), '%S', '%s', '%P', '%W')

    static_frame = tk.Frame(input_frame)
    static_frame.columnconfigure(1, weight=1)
    tk.Label(static_frame, text="Vessel Name:", width=15, anchor=tk.W).grid(row=0, column=0, sticky=tk.W, pady=2)
    tk.Entry(static_frame, textvariable=vessel_name).grid(row=0, column=1, sticky=tk.W)
    tk.Label(static_frame, text="Vessel IMO:").grid(row=1, column=0, sticky=tk.W, pady=2)
    tk.Entry(static_frame, textvariable=vessel_imo, width=10, validate='key', validatecommand=valimo).grid(row=1, column=1, sticky=tk.W)
    tk.Label(static_frame, text="Master Name:").grid(row=2, column=0, sticky=tk.W, pady=2)
    tk.Entry(static_frame, textvariable=master_name, width=30).grid(row=2, column=1, sticky=tk.W)
    static_frame.grid(padx=5, pady=5, sticky=tk.W)

    client_frame = tk.Frame(input_frame)
    client_frame.columnconfigure(1, weight=1)
    tk.Label(client_frame, text="Charterer Name:", width=15, anchor=tk.W).grid(row=0, column=0, sticky=tk.W, pady=2)
    charter_entry = tk.Entry(client_frame, textvariable=charterer_name, width=30)
    charter_entry.grid(row=0, column=1, sticky=tk.W)
    tk.Label(client_frame, text="Project:").grid(row=1, column=0, sticky=tk.W, pady=2)
    tk.Entry(client_frame, textvariable=project, width=70).grid(row=1, column=1, sticky=tk.W)
    client_frame.grid(padx=5, pady=5, sticky=tk.W)

    charter_entry.focus()

    def validate_consumables(user_input, widgettext, widgettextafter, widgetname):
        decimal = "."

        if user_input.isdigit():
            return True

        elif user_input == "," or user_input == ".":
            if len(widgettext) > len(widgettextafter):  # Deletion
                return True

            else:
                if (str(widgettext).find(decimal) >= 0):
                    return False
                else:
                    if user_input == ",":
                        return False
                    else:
                        return True

        elif user_input == "":
            return True

        else:
            return False
    
    def invalidate_consumables(user_input, widgettext, widgettextafter, widgetname):
        if user_input == ",":
            msgbox.showinfo(title="Decimal Point", message="Please use a period ('.') instead of a comma (',') as decimal point")

    valcons = (mainwin.register(validate_consumables), '%S', '%s', '%P', '%W')
    invalcons = (mainwin.register(invalidate_consumables), '%S', '%s', '%P', '%W')

    consumables_frame = tk.LabelFrame(input_frame, text="Consumable Survey")
    consumables_frame.columnconfigure(2, weight=1)
    tk.Label(consumables_frame, text="Marine Gas Oil:", width=15, anchor=tk.W).grid(row=0, column=0, sticky=tk.W, pady=2)
    tk.Entry(name="mgo_entry", master=consumables_frame, textvariable=consumable_mgo, width=7, validate='key', validatecommand=valcons, invalidcommand=invalcons).grid(row=0, column=1, sticky=tk.W)
    tk.Label(consumables_frame, text="M3", anchor=tk.W).grid(row=0, column=2, sticky=tk.W)
    tk.Label(consumables_frame, text="Lube Oil:").grid(row=1, column=0, sticky=tk.W, pady=2)
    tk.Entry(name="lo_entry", master=consumables_frame, textvariable=consumable_lo, width=7, validate='key', validatecommand=valcons, invalidcommand=invalcons).grid(row=1, column=1, sticky=tk.W)
    tk.Label(consumables_frame, text="Ltr", anchor=tk.W).grid(row=1, column=2, sticky=tk.W)
    tk.Label(consumables_frame, text="Fresh Water:").grid(row=2, column=0, sticky=tk.W, pady=2)
    tk.Entry(name="fw_entry", master=consumables_frame, textvariable=consumable_fw, width=7, validate='key', validatecommand=valcons, invalidcommand=invalcons).grid(row=2, column=1, sticky=tk.W)
    tk.Label(consumables_frame, text="M3", anchor=tk.W).grid(row=2, column=2, sticky=tk.W)
    consumables_frame.grid(padx=5, pady=5, sticky=tk.W+tk.E)

    date_place_frame = tk.Frame(input_frame)
    date_place_frame.columnconfigure(1, weight=1)
    
    date_frame = tk.Frame(date_place_frame)

    def validate_date_and_time(user_input, widgetname, widgettext):
        if user_input.isdigit():
            # Fetching minimum and maximum value of the spinbox
            minval = int(mainwin.nametowidget(widgetname).config('from')[4])
            maxval = int(mainwin.nametowidget(widgetname).config('to')[4])
    
            # check if the number is within the range
            if widgettext != "":
                if int(widgettext) not in range(minval, maxval + 1):
                    return False
    
            return True
    
        # if input is blank string
        elif user_input == "":
            return True
    
        # return false if input is not numeric
        else:
            return False

    valfunc = (mainwin.register(validate_date_and_time), '%S', '%W', '%P')

    tk.Label(date_place_frame, text="Date:", width=15, anchor=tk.W).grid(row=0, column=0, sticky=tk.W, pady=2)
    tk.Spinbox(date_frame, from_=1, to=31, textvariable=date_day, width=2, validate='key', validatecommand=valfunc, justify=tk.RIGHT).grid(row=0, column=0, sticky=tk.W)
    tk.Spinbox(date_frame, from_=1, to=12, textvariable=date_month, width=2, validate='key', validatecommand=valfunc, justify=tk.RIGHT).grid(row=0, column=1, sticky=tk.W)
    tk.Spinbox(date_frame, from_=1, to=2080, textvariable=date_year, width=4, validate='key', validatecommand=valfunc, justify=tk.RIGHT).grid(row=0, column=2, sticky=tk.W)
    date_frame.grid(row=0, column=1, sticky=tk.W)

    time_frame = tk.Frame(date_place_frame)
    tk.Label(date_place_frame, text="Time:", width=15, anchor=tk.W).grid(row=1, column=0, sticky=tk.W, pady=2)
    tk.Spinbox(time_frame, from_=0, to=23, textvariable=time_hr, width=2, validate='key', validatecommand=valfunc, justify=tk.RIGHT).grid(row=0, column=0, sticky=tk.W)
    tk.Label(time_frame, text=":").grid(row=0, column=1, sticky=tk.W)
    tk.Spinbox(time_frame, from_=0, to=59, textvariable=time_min, width=2, validate='key', validatecommand=valfunc, justify=tk.RIGHT).grid(row=0, column=2, sticky=tk.W)
    time_frame.grid(row=1, column=1, sticky=tk.W)

    tk.Label(date_place_frame, text="Location:").grid(row=3, column=0, sticky=tk.W, pady=2)
    tk.Entry(date_place_frame, textvariable=location, width=60).grid(row=3, column=1, sticky=tk.W)
    date_place_frame.grid(padx=5, pady=5, sticky=tk.W)

    input_frame.grid(row=1, padx=10, pady=5, sticky='ew')

    def change_title(*args):
        mainwin.title(f"{on_off_hire_choice.get().title()}-Hire Statement - {vessel.operator.name}")

    on_off_hire_choice.trace_add('write', change_title)

    def update_vessel(*args):
        vessel.name = vessel_name.get()

        conf['Vessel']['Name'] = vessel.name

        with open(ini_file_name, 'w', encoding='utf8') as inifile:
            conf.write(inifile)

    vessel_name.trace_add('write', update_vessel)

    def update_imo(*args):
        vessel.imo = vessel_imo.get()

        conf['Vessel']['IMO'] = vessel.imo

        with open(ini_file_name, 'w', encoding='utf8') as inifile:
            conf.write(inifile)

    vessel_imo.trace_add('write', update_imo)

    def update_master(*args):
        vessel.master = master_name.get()

        conf['Vessel']['Master'] = vessel.master

        with open(ini_file_name, 'w', encoding='utf8') as inifile:
            conf.write(inifile)

    master_name.trace_add('write', update_master)

    def get_active_statement():
        try:
            charter_date_time = datetime(day=date_day.get(), month=date_month.get(), year=date_year.get(), hour=time_hr.get(), minute=time_min.get())
        except ValueError as valerr:
            raise ValueError(valerr)
        
        hire = HireStatement( hire_date=charter_date_time,
                                        location=location.get(),
                                        on_hire=on_off_hire_choice.get(),
                                        charterer=charterer_name.get(),
                                        project=project.get(),
                                        mgo=consumable_mgo.get(),
                                        lo=consumable_lo.get(),
                                        fw=consumable_fw.get())
        
        return hire
    
    def btn_new_click():
        consumable_mgo.set("")
        consumable_lo.set("")
        consumable_fw.set("")

        charterer_name.set("")
        project.set("")

        today = datetime.now()
        date_day.set(today.day)
        date_month.set(today.month)
        date_year.set(today.year)
        time_hr.set(today.hour)
        time_min.set(today.minute)

        location.set("")

        charter_entry.focus()

    def btn_pdf_click():
        try:
            hire_statemant = get_active_statement()
            statement_file = GenerateStatement_PDF(hireObj=hire_statemant, vessel=vessel, conf=conf, ini_file_name=ini_file_name)
            InsertSignfields(statement_file)
        except ValueError as valerr:
            msgbox.showerror(message=f"The date is not valid\n{valerr}", title="Date Error")
    
    def btn_save_click():
        hire_statemant = get_active_statement()

        filename = f"{hire_statemant.date.strftime('%Y-%m-%d')} - {hire_statemant.on_hire.title()}-hire - {hire_statemant.charterer.name}"
        hire_statemant.date.strftime('%B %Y, at %H:%M LT')

        filepath = fd.asksaveasfilename(title=f"Save {hire_statemant.on_hire.title()}-hire Figures...", 
                                        filetypes=(('On-Off-Hire-files', '*.hire'),('All files', '*.*')),
                                        initialdir=conf['Directory']['working'], 
                                        initialfile=filename)

        if not (os.path.splitext(filepath)[1] == ".hire"):
            filepath += ".hire"
        
        with open(filepath, 'w') as jsonfile:
            jsonfile.write(hire_statemant.toJSON())

        conf['Directory']['working'] = os.path.dirname(filepath)

        with open(ini_file_name, 'w', encoding='utf8') as inifile:
            conf.write(inifile)
    
    def btn_load_click():
        from json.decoder import JSONDecodeError

        statement_txt = ""

        filepath = fd.askopenfilename(title=f"Load On/Off-hire Figures...", 
                                        filetypes=(('On-Off-Hire-files', '*.hire'),('All files', '*.*')),
                                        initialdir=conf['Directory']['working'])

        if filepath:
            try:
                with open(filepath, 'r') as jsonfile:
                    statement_txt = jsonfile.read()
                
                conf['Directory']['working'] = os.path.dirname(filepath)
                
                hire_statement = HireStatement()
                hire_statement.fromJSON(statement_txt)

                on_off_hire_choice.set(hire_statement.on_hire)
                charterer_name.set(hire_statement.charterer.name)
                project.set(hire_statement.project)
                consumable_mgo.set(hire_statement.mgo)
                consumable_lo.set(hire_statement.lo)
                consumable_fw.set(hire_statement.fw)
                date_day.set(hire_statement.date.day)
                date_month.set(hire_statement.date.month)
                date_year.set(hire_statement.date.year)
                time_hr.set(hire_statement.date.hour)
                time_min.set(hire_statement.date.minute)
                location.set(hire_statement.location)
            except JSONDecodeError as json_err:
                msgbox.showerror(title="Fatal Error", message=f"Cannot decode hire-file: {json_err.msg}")
                print(f"Cannot decode hire-file: {json_err.msg}")
            except Exception as err:
                msgbox.showerror(title="Fatal Error", message=f"Error loading hire-file")
                print(f"Error loading hire-file")
    
    # Application menu
    menu = tk.Menu(mainwin)
    mainwin.configure(menu=menu)

    file_menu = tk.Menu(menu, tearoff=False)
    menu.add_cascade(label="File", menu=file_menu)
    file_menu.add_cascade(label="New...",command=btn_new_click)
    file_menu.add_cascade(label="Open...",command=btn_load_click)
    file_menu.add_cascade(label="Save As...",command=btn_save_click)
    file_menu.add_separator()
    file_menu.add_command(label="Quit", command=mainwin.destroy)
    options_menu = tk.Menu(menu, tearoff=False)
    menu.add_cascade(label="Options", menu=options_menu)
    options_menu.add_command(label="Generate PDF", command=btn_pdf_click)
    help_menu = tk.Menu(menu, tearoff=False)
    menu.add_cascade(label="Help", menu=help_menu)
    help_menu.add_command(  label="About...",
                            command=lambda: msgbox.showinfo(title="About",
                                                            message="On/Off-hire statement generator\nversion 0.1\n\nCreated by Kristian S. Jensen")
    )

    # Applicatio toolbar
    # Button icons provided by: https://iconarchive.com/
    toolbar_frame = tk.Frame(master=mainwin, bd=1, relief=tk.RAISED)

    global img_new
    global img_open
    global img_save
    global img_pdf
    global img_quit

    try:
        img_new = Pillow_Img_Tk.PhotoImage(Pillow_Img.open("./Images/24_pxl/Files-New-File-icon.png"))
        img_open = Pillow_Img_Tk.PhotoImage(Pillow_Img.open("./Images/24_pxl/open-file-icon.png"))
        img_save = Pillow_Img_Tk.PhotoImage(Pillow_Img.open("./Images/24_pxl/Save-icon.png"))
        img_pdf = Pillow_Img_Tk.PhotoImage(Pillow_Img.open("./Images/24_pxl/Adobe-PDF-Document-icon.png"))
        img_quit = Pillow_Img_Tk.PhotoImage(Pillow_Img.open("./Images/24_pxl/Button-Log-Off-icon.png"))

        tk.Button( master=toolbar_frame, relief=tk.FLAT, command=btn_new_click, image=img_new, text="New").pack(side=tk.LEFT, padx=2, pady=2)
        tk.Button( master=toolbar_frame, relief=tk.FLAT, command=btn_load_click, image=img_open, text="Open").pack(side=tk.LEFT, padx=2, pady=2)
        tk.Button( master=toolbar_frame, relief=tk.FLAT, command=btn_save_click, image=img_save, text="Save").pack(side=tk.LEFT, padx=2, pady=2)
        tk.Label(master=toolbar_frame, width=3).pack(side=tk.LEFT)
        tk.Button( master=toolbar_frame, relief=tk.FLAT, command=btn_pdf_click, image=img_pdf, text="PDF").pack(side=tk.LEFT, padx=2, pady=2)
        tk.Button( master=toolbar_frame, relief=tk.FLAT, command=mainwin.quit, image=img_quit, text="Quit").pack(side=tk.RIGHT, padx=2, pady=2)
    except:
        tk.Button( master=toolbar_frame, relief=tk.FLAT, command=btn_new_click, text="New").pack(side=tk.LEFT, padx=2, pady=2)
        tk.Button( master=toolbar_frame, relief=tk.FLAT, command=btn_load_click, text="Open").pack(side=tk.LEFT, padx=2, pady=2)
        tk.Button( master=toolbar_frame, relief=tk.FLAT, command=btn_save_click, text="Save").pack(side=tk.LEFT, padx=2, pady=2)
        tk.Button( master=toolbar_frame, relief=tk.FLAT, command=btn_pdf_click, text="PDF").pack(side=tk.LEFT, padx=2, pady=2)
        tk.Button( master=toolbar_frame, relief=tk.FLAT, command=mainwin.quit, text="Quit").pack(side=tk.RIGHT, padx=2, pady=2)

    toolbar_frame.grid(row=0, sticky='nwe')

    # Clear all dynamic fields
    btn_new_click()

    return mainwin



if __name__ == "__main__":
    Main()