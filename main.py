from tkinter import *
import PyPDF2
from tkinter import filedialog
import pyttsx3
import os

root = Tk()
root.title('Text to Speech')
root.iconbitmap('./static/images/favicon.ico')
root.geometry("650x500")

engine = pyttsx3.init()
audio_file = ""


def play():
    text = my_text.get(1.0, 10.0)
    engine.say(text)
    engine.runAndWait()


def open_and_save():
    global audio_file
    open_file = filedialog.askopenfilename(
        initialdir="C:/user/Lee",
        title="Open PDF File",
        filetypes=(
            ("PDF Files", "*.pdf"),
            ("All Files", "*.*")))
    print(f"File Name: {open_file}")
    file_name = open_file[open_file.rfind("/")+1:open_file.rfind(".pdf")]
    audio_file = f"{file_name}.mp3"
    audio_file = audio_file.replace(" ", "-")

    # Check to see if there is a file
    if open_file:
        # Open the pdf file
        pdf_file = PyPDF2.PdfFileReader(open_file)

        number_of_pages = pdf_file.getNumPages()
        print(number_of_pages)
        for page in range(number_of_pages):
            # Set the page to read
            page = pdf_file.getPage(page)
            # Extract the text from the pdf file
            page_stuff = page.extractText()
            # print(page_stuff)
            # Add text to textbox
            my_text.insert(END, page_stuff)

        engine.save_to_file(my_text.get(1.0, END), audio_file)
        # engine.say(page_stuff)
        engine.runAndWait()


def play_audiobook():
    global audio_file
    print(f"PLAY_AUDIOBOOK: {audio_file}")
    os.system("start " + audio_file)


toolbar_frame = Frame(root)
toolbar_frame.pack(fill=X, pady=5)
open_button = Button(toolbar_frame, text="Open", command=open_and_save)
open_button.grid(row=0, column=0, sticky=W, padx=5)

play_button = Button(toolbar_frame, text="Play", command=play_audiobook)
play_button.grid(row=0, column=1, padx=5)

# vertical scroll on text area
vertical_scroll = Scrollbar(root)
vertical_scroll.pack(side=RIGHT, fill=Y)

# Create a textbox
my_text = Text(root, height=30, width=75, yscrollcommand=vertical_scroll.set)
my_text.pack(pady=10)

vertical_scroll.config(command=my_text.yview)


# Clear the textbox
def clear_text_box():
    my_text.delete(1.0, END)

# Open our pdf file
def open_pdf():
    # Grab the filename of the pdf file
    open_file = filedialog.askopenfilename(
        initialdir="C:/user/Lee",
        title="Open PDF File",
        filetypes=(
            ("PDF Files", "*.pdf"),
            ("All Files", "*.*")))

    # Check to see if there is a file
    if open_file:
        # Open the pdf file
        pdf_file = PyPDF2.PdfFileReader(open_file)
        number_of_pages = pdf_file.getNumPages()
        # print(number_of_pages)
        for page in range(number_of_pages):
            # Set the page to read
            page = pdf_file.getPage(page)
            # Extract the text from the pdf file
            page_stuff = page.extractText()

            # Add text to textbox
            my_text.insert(END, page_stuff)


# Create A Menu
my_menu = Menu(root)
root.config(menu=my_menu)

# Add some dropdown menus
file_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Open", command=open_and_save)
file_menu.add_command(label="Clear", command=clear_text_box)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)


root.mainloop()
