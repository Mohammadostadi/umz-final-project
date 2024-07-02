from tkinter import *
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk 
import requests
from bs4 import BeautifulSoup
import csv
import re

root = Tk()
root.geometry('390x400')
root.title("Search Scraper")

label_padx = Label(root, text="Search in Web").place(x=155, y=40)
group=['game','technology','news', 'sports']
ttk.LabelFrame(root, text="Chose Category").place(x=30, y=80, height=50, width=300)
selected_group = ttk.Combobox(root, values=group)
selected_group.place(x=30, y=100, height=30, width=300)


def on_checkbox_change(checkbox_value, checkbox_var):
    url = 'https://www.skysports.com/{}'
    if(checkbox_var.get()):
        word = checkbox_value 
        def get_word_data(word, url):
            try:
                data = []
                
                response = requests.get(url.format(word))
                soup = BeautifulSoup(response.content, 'html.parser')

                    # using regex to show only www.example.com form
                match = re.search(r"https://([^/]+)", url)
                match=match.group(1)
                paragraphs = [p.text for p in soup.find_all('p')]
                data.extend([(p, match) for p in paragraphs])
                return data
            except (Exception , TypeError):
                messagebox.showerror("Error", "Site URL may not be correct")
        try:
            try:
                data = get_word_data(word, url)
            except:
                messagebox.showerror("Error", "invalid word")



            # Store the data in a CSV file
            fileAdd("word_data_total.csv", "a", data)
            fileAdd("word_data.csv", "w", data)
            

            show("word_data.csv")
        except TypeError:
            print ('Nothing Founded')

# Function to create multiple checkboxes using a loop
def create_checkboxes(root, num_checkboxes):
    checkboxes = []  # List to store BooleanVar objects for each checkbox

    # Loop to create checkboxes dynamically
    for i in num_checkboxes:
        checkbox_var = tk.BooleanVar()  # Variable to track the state of the checkbox
        checkbox = tk.Checkbutton(
            root,
            text=i,
            variable=checkbox_var,
            command=lambda i=i, var=checkbox_var: on_checkbox_change(i, var)
        )
        checkbox.pack()  # Place the checkbox in the window
        checkboxes.append(checkbox_var)  # Add the variable to the list

    return checkboxes  # Retu

def urlCheck(urls, selected_urls):
    global urls_main
    if selected_urls.get() == '':
        urls_main.extend(urls)
    else:
        for i in urls:
            if i == selected_urls.get():
                urls_main.append(i)
    ttk.LabelFrame(root, text="Search To").place(x=30, y=200, height=70, width=300)
    global entryWord
    entryWord=ttk.Entry(root)
    entryWord.place(x=30, y=220, height=40, width=300)
    wordSearch=Button(root , text = "search",command=scriptSearch).place(x=335,y=220, height=30, width=50)
    
def checkTime(urls):
    ttk.LabelFrame(root, text="Select URL").place(x=30, y=150, height=50, width=300)
    selected_urls = ttk.Combobox(root, values=urls)
    selected_urls.place(x=30, y=170, height=30, width=300) 
    def urlsCheck():
        urlCheck(urls, selected_urls)
        
    UrlCheck=Button(root , text = "Check",command=urlsCheck).place(x=335,y=170, height=30, width=50)
    

def fileAdd(fileName, do, data):
    file = open(fileName, do, encoding="utf-8", newline='')
    writer = csv.writer(file)
    writer.writerow(['Text', 'URL'])
    for text, url in data:
        writer.writerow([text, url])
    file.close()
    
    
def show(fileName):
    window_group = Toplevel()
    window_group.title("Show Information")
    window_group.geometry("400x400")
    window_group.resizable(width = False , height = False)
    # Create a Text widget
    text_widget = Text(window_group)
    text_widget.pack(side="left", fill="both", expand=True)

    scrollbar_group = Scrollbar(window_group,orient='vertical', command=text_widget.yview)
    #scrollbar_group.place(x=5,y=10, height=380)

    text_widget.configure(yscrollcommand=scrollbar_group.set)
    scrollbar_group.pack(side="right", fill="y")

    text_widget.pack()
    
    # Open the CSV file
    with open(fileName, 'r',encoding="utf-8", newline='') as csvFile:
        reader = csv.reader(csvFile)
        next(reader)  # Skip the header row
        for row in reader:
            text = '\t'.join(row)
            text_widget.insert(tk.END, text + "\n\n")


def checkBox():
    pass

def groupCheck():
    global urls_main
    urls_main=[]
    check=selected_group.get()
    if check == "technology":
        urls=['https://en.wikipedia.org/wiki/{}','https://techcrunch.com/?s={}']
        checkTime(urls)

    elif check == "game":    
        urls=['https://en.wikipedia.org/wiki/{}','https://www.zoomg.ir/search/{}/']
        checkTime(urls)

    elif check == "news":    
        urls=['https://en.wikipedia.org/wiki/{}','https://dig.watch/?s={}']
        checkTime(urls)
    elif check == "sports":    
        
        num_checkboxes = ['football', 'basketball']  # Number of checkboxes to create
        checkboxes = create_checkboxes(root, num_checkboxes)
        

GroupCheck=Button(root , text = "check",command=groupCheck).place(x=335,y=100, height=30, width=50)


def scriptSearch():

    
        
    def get_word_data(word, urls):
        try:
            data = []
            for url in urls:
                response = requests.get(url.format(word))
                soup = BeautifulSoup(response.content, 'html.parser')

                # using regex to show only www.example.com form
                match = re.search(r"https://([^/]+)", url)
                match=match.group(1)
                paragraphs = [p.text for p in soup.find_all('p')]
                data.extend([(p, match) for p in paragraphs])
            return data
        except (Exception , TypeError):
            messagebox.showerror("Error", "Site URL may not be correct")
    try:
        try:
            data = get_word_data(entryWord.get(), urls_main)
        except:
            messagebox.showerror("Error", "invalid word")



        # Store the data in a CSV file
        fileAdd("word_data_total.csv", "a", data)
        fileAdd("word_data.csv", "w", data)
        

        show("word_data.csv")
    except TypeError:
        print ('Nothing Founded')

def removeData():
    # Open the CSV file in write mode, which will erase its contents
    file = open('word_data_total.csv', 'w', newline='')
    writer = csv.writer(file)
    writer.writerow([])  # Write an empty list to the file
    file.close()
    
    
def showData():
    show("word_data_total.csv")
    
removeData=Button(root , text = "Remove",command=removeData).place(x=20,y=370)
showData=Button(root , text = "Show",command=showData).place(x=70,y=370)


root.mainloop()