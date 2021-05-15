from tkinter import *
from tkinter import filedialog, messagebox
from tkinter.ttk import Combobox

from PIL import Image, ImageDraw, ImageFont

PINK = "#e2979c"
FONT = ("Courier", 12, "bold")
sample_img = 'sample.png'


class MainPage:
    def __init__(self, master):
        self.master = master
        self.frame = Frame(self.master)
        self.master.title("Welcome to Watermark your picture!")
        self.master.config(padx=25, pady=25, bg=PINK)
        self.title = Label(self.frame, text="Generate your own Watermark Image", font=("Constantia", 22, "bold"),
                           bg=PINK,fg="white")
        self.title.grid(row=0, column=0, columnspan=3)
        self.canvas = Canvas(self.frame, width=530, height=520, bg=PINK, highlightthickness=0)
        self.picture = PhotoImage(file=sample_img)
        self.canvas.create_image(260, 260, image=self.picture)
        self.canvas.grid(row=1, column=0,columnspan=2)
        self.generate_image = Button(self.frame, text="Watermark Image by Text", command=self.create_window)
        self.generate_image.grid(row=2, column=0)

        self.generate_image_logo = Button(self.frame, text="Watermark Image by Logo", command=self.create_logo)
        self.generate_image_logo.grid(row=2, column=1)

        self.frame.pack()

    def create_window(self):
        self.newWindow = Toplevel(self.master)
        self.app = Page2(self.newWindow, False)

    def create_logo(self):
        self.newWindow = Toplevel(self.master)
        self.app = Logo(self.newWindow)


class Page2:
    def __init__(self, master, Logo):
        self.master = master
        self.frame = Frame(self.master)
        self.filename = None
        self.master.title("Watermark your picture!")
        self.master.config(padx=50, pady=50, bg=PINK)

        self.upload_label = Label(self.frame, text="Upload your image: ", font=FONT, bg=PINK)
        self.upload_label.grid(row=0, column=0, sticky="w")

        self.upload_button = Button(self.frame, text="Open Folder", command=self.open_folder)
        self.upload_button.grid(row=0, column=1, columnspan=2, sticky="e")

        if Logo:
            self.upload_logo_button = Button(self.frame, text="Upload", command=self.open_logo)
            self.upload_logo_button.grid(row=1, column=1,columnspan=2, sticky="e")
            self.upload_logo_label = Label(self.frame, text="Your Watermark Logo:", font=FONT, bg=PINK)
            self.upload_logo_label.grid(row=1, column=0, sticky="w")
        if not Logo:
            self.text_label = Label(self.frame, text="Your Watermark:", font=FONT, bg=PINK)
            self.text_label.grid(row=2, column=0, sticky="w")
            self.text_entry = Entry(self.frame, width=20)
            self.text_entry.grid(row=2, column=1, columnspan=2, sticky="e")
            self.text_entry.insert(0, "Sample")
            self.text_entry.focus()

            self.color_label = Label(self.frame, text="Color :", font=FONT, bg=PINK)
            self.color_label.grid(row=4,column=0, sticky="w")
            self.color_checkbox = Combobox(self.frame)
            self.color_checkbox['values'] = ("White","Black","Tomato","DodgerBlue","DarkSlateGrey")
            self.color_checkbox.current(0)
            self.color_checkbox.grid(row=4,column=1, sticky="e")

            self.text_scale = Label(self.frame, text="Font Size :", font=FONT, bg=PINK)
            self.text_scale.grid(row=3, column=0, sticky="w")
            self.scale_widget = Scale(self.frame, from_=25, to=200, orient=HORIZONTAL, bg=PINK)
            self.scale_widget.set(25)
            self.scale_widget.grid(row=3, column=1, sticky="e")

        self.submit = Button(self.frame, text="Submit", command=self.generate)
        self.submit.grid(row=5, column=0, columnspan=2)
        self.frame.pack()

    def open_folder(self):
        self.filename = filedialog.askopenfilename()
        print("Selected :", self.filename)
        self.im = Image.open(self.filename)

    def generate(self):
        if self.filename != None:
            width, height = self.im.size
            draw = ImageDraw.Draw(self.im)
            text = self.text_entry.get()
            fontsize = self.scale_widget.get()
            font = ImageFont.truetype('arial.ttf', fontsize)
            color = self.color_checkbox.get()
            textwidth, textheight = draw.textsize(text, font)
            margin = 10
            x = width / 2 - textwidth - margin
            y = height / 2 - textheight
            draw.multiline_text((x, y), text, font=font, fill=color)
            self.im.show()
        elif self.filename == None:
            messagebox.showwarning(title="Upload your image!",
                                   message='You did not choose the picture you want to wateramark!')


class Logo(Page2):
    def __init__(self, master):
        Page2.__init__(self, master, True)
        self.watermark = None

    def open_logo(self):
        self.watermark = filedialog.askopenfilename()
        print("Selected :", self.watermark)
        self.logo = Image.open(self.watermark)

    def generate(self):
        if self.watermark != None and self.filename != None:
            base_image = Image.open(self.filename)
            position = ((base_image.width - self.logo.width), (base_image.height - self.logo.height))
            base_image.paste(self.logo, position)
            base_image.show()

def main():
    window = Tk()
    app = MainPage(window)
    window.mainloop()


if __name__ == "__main__":
    main()
