import requests
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin
import tkinter as tk

def get_all_forms(url):
    """Given a `url`, it returns all forms from the HTML content"""
    soup = bs(requests.get(url).content, "html.parser")
    return soup.find_all("form")

def get_form_details(form):
    """
    This function extracts all possible useful information about an HTML `form`
    """
    details = {}
    action = form.attrs.get("action", "").lower()
    method = form.attrs.get("method", "get").lower()
    inputs = []
    for input_tag in form.find_all("input"):
        input_type = input_tag.attrs.get("type", "text")
        input_name = input_tag.attrs.get("name")
        inputs.append({"type": input_type, "name": input_name})
    details["action"] = action
    details["method"] = method
    details["inputs"] = inputs
    return details

def submit_form(form_details, url, value):
    """
    Submits a form given in `form_details`
    """
    target_url = urljoin(url, form_details["action"])
    inputs = form_details["inputs"]
    data = {}
    for input in inputs:
        if input["type"] == "text" or input["type"] == "search":
            input["value"] = value
        input_name = input.get("name")
        input_value = input.get("value")
        if input_name and input_value:
            data[input_name] = input_value

    if form_details["method"] == "post":
        return requests.post(target_url, data=data)
    else:
        return requests.get(target_url, params=data)

def scan_xss(url):
    """
    Given a `url`, it prints all XSS vulnerable forms
    """
    forms = get_all_forms(url)
    vulnerable_forms = []

    js_script = "<script>alert('XSS')</script>"
    for form in forms:
        form_details = get_form_details(form)
        content = submit_form(form_details, url, js_script).content.decode()
        if js_script in content:
            vulnerable_forms.append(form_details)

    return vulnerable_forms

def start_scan():
    url = url_entry.get()
    if not url:
        return

    vulnerable_forms = scan_xss(url)
    listbox.delete(0, tk.END)  # Clear previous entries
    if vulnerable_forms:
        for form in vulnerable_forms:
            listbox.insert(tk.END, f"Vulnerable Form: {form}")
    else:
        listbox.insert(tk.END, "No vulnerable forms found.")
        
# Function to refresh
def clear_entry():
    url_entry.delete(0, tk.END)
    listbox.delete(0, tk.END)


# GUI setup
root = tk.Tk()
root.title("XSS Scanner")


# Colors
qxp = '#4A4A4A'
xtc = '#A4A4A4'
zkn = '#00f000'
m1c = '#00ffff'
bgc = '#222222'
dbg = '#000000'
fgc = '#111111'

root.tk_setPalette(background=bgc, foreground=m1c, activeBackground=fgc,
                   activeForeground=bgc, highlightColor=m1c, highlightBackground=m1c)

url_label = tk.Label(root, text="Enter URL:", bg=bgc, fg=m1c)
url_label.pack(pady=5)

url_entry = tk.Entry(root, width=44, bg='#4A4A4A', fg=zkn)
url_entry.pack()

url_label = tk.Label(root, text="Extract all useful information about HTML forms:", bg=bgc, fg=m1c)
url_label.pack()

frame = tk.Frame(root, bg=bgc)

scan_button = tk.Button(root, text="Start XSS Scan", command=start_scan, bg=qxp, fg='#00FF00')
scan_button.pack(padx=2, pady=10)
scan_button.place(x=190, y=78)

refresh_button = tk.Button(root, text="Refresh", command=clear_entry, bg=qxp, fg=m1c)
refresh_button.pack(padx=2, pady=10)
refresh_button.place(x=280, y=78)
frame.pack(padx=10, pady=10)

frame = tk.Frame(root, bg='#222222')
frame.pack(padx=5, pady=5)

listbox = tk.Listbox(root, width=80, height=20, bg='#A4A4A4', fg=m1c)
listbox.pack(padx=20, pady=10)

statusbar = tk.Label(root, text="#################################################", fg='#4A4A4A', border=2)
statusbar.pack()
statusbar = tk.Label(root, text='XSS SCANNER - Cross Site Scripting Tool')
statusbar.pack()
statusbar = tk.Label(root, text="Scan Websites | Discover XSS Vulnerability Forms")
statusbar.pack()
statusbar = tk.Label(root, text="#################################################", fg='#4A4A4A', border=2)
statusbar.pack()

root.mainloop()
