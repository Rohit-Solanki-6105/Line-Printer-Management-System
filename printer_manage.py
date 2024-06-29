from win32print import *

def_printer = GetDefaultPrinter()
print(f"default: {def_printer}")

def get_printer():
    try:
        with open('settings.settings', 'r') as settings_file:
            settings_data = json.load(settings_file)
            # print(settings_data)
            return settings_data['printer']

    except:
        # print("doesn't exist")
        pass
# printer = "EPSON FX Series 1 (136)"
printer = get_printer()
def get_all_printers():
    printers_info = EnumPrinters(PRINTER_ENUM_LOCAL, None, 1)
    printers = [printer_info[2] for printer_info in printers_info]
    return printers

def display_printers():
    all_printers = get_all_printers()
    if all_printers:
                    # printer_list.delete(1.0, tk.END)  # Clear previous content
        for printer in all_printers:
            # printer_list = ctk.CTkLabel(scroll_frame, text=printer)
            print(printer)

display_printers()


# # getting default printer
# string = GetDefaultPrinter()
# print(string)
def printer_check(in_printer = printer):
    try:
        PyPrinterHANDLE = OpenPrinter(in_printer)
        # print(PyPrinterHANDLE)
        #code for printer below this
        if(PyPrinterHANDLE):
            return True
            # print("on")
        else:
            return False
        
        ClosePrinter(PyPrinterHANDLE)
    except Exception as e:
        print(e)
        return False
    


# printer_selected = "EPSON FX Series 1 (136)"
# print("isOn = ", printer_stat(printer_selected))

# PyPrinterHANDLE = OpenPrinter(printer_selected)
# print(PyPrinterHANDLE)
#code for printer below this
# if(PyPrinterHANDLE):
#     print("on")
# else:
#     print("off")
def use_printer():
    try:
        if printer_check():
            SetDefaultPrinter(printer)
            print(f"In use: {printer}")
    except Exception as e:
        print(e)
    
# use_printer()

def release_printer():
    try:
        if printer_check():
            SetDefaultPrinter(def_printer)
            print(f"Released: {printer}")
            print(f"In use: {def_printer}")
    except Exception as e:
        print(e)

# release_printer()
#code for printer above this
# ClosePrinter(PyPrinterHANDLE)
# print(PyPrinterHANDLE)

# if(PyPrinterHANDLE):
#     print("on")
# else:
#     print("off")
