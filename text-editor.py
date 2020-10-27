import os     
import tkinter
from tkinter import *
from tkinter.filedialog import askopenfilename,asksaveasfilename
from tkinter import ttk,colorchooser,messagebox

class TextEditor: 
    root = Tk() 
    width = 600
    height = 500
    text_area = Text(root) 
    menu_bar = Menu(root) 
    file_menu = Menu(menu_bar, tearoff=0) 
    edit_menu = Menu(menu_bar, tearoff=0) 
    help_menu = Menu(menu_bar, tearoff=0)
    format_toolbar = Frame(root)
    scroll_bar = Scrollbar(text_area)      
    file = None
    font_family = tkinter.StringVar() 
    font_size = tkinter.StringVar()
    font_bold = False
    font_italics = False
    font_underline = False
    bold =None
    italic = None
    underline = None

  
    def __init__(self):  
        self.root.title('Text Editor - Untitled') 
        screenWidth = self.root.winfo_screenwidth() 
        screenHeight = self.root.winfo_screenheight() 
        left = (screenWidth / 2) - (self.width / 2)  
        top = (screenHeight / 2) - (self.height /2)  
        self.root.geometry('%dx%d+%d+%d' % (self.width, self.height, left, top))  
  
        # row and column config
        self.root.grid_rowconfigure(1, weight=1) 
        self.root.grid_columnconfigure(0, weight=1) 

        
        #file menu defined
        self.file_menu.add_command(label = "New",command=self.new_file) 
        self.file_menu.add_command(label = "Open",command=self.open_file) 
        self.file_menu.add_command(label = "Save",command=self.save_file) 
        self.file_menu.add_command(label = "Save As",command=self.save_as_file) 
        self.file_menu.add_separator() 
        self.file_menu.add_command(label = "Exit",command=self.quit_app) 
        self.menu_bar.add_cascade(label = "File",menu=self.file_menu) 
        
        # edit menu defined
        self.edit_menu.add_command(label = "Cut",command=self.cut) 
        self.edit_menu.add_command(label = "Copy",command=self.copy) 
        self.edit_menu.add_command(label = "Paste",command=self.paste) 
        self.menu_bar.add_cascade(label = "Edit",menu=self.edit_menu) 
        
        # edit help menu
        self.help_menu.add_command(label = "About",command=self.show_about) 
        self.menu_bar.add_cascade(label = "Help", 
                                    menu = self.help_menu) 
        
        #define main menu bar
        self.root.config(menu=self.menu_bar) 
        self.scroll_bar.pack(side=RIGHT,fill=Y)

        #format toolbar
        self.format_menu()

        #text area
        self.text_area.grid(row=1,column=0,sticky = 'nsew')
          
        # Scrollbar will adjust automatically according to the content         
        self.scroll_bar.config(command=self.text_area.yview)      
        self.text_area.config(yscrollcommand=self.scroll_bar.set) 
      

    def format_menu(self):
        # setting font family
        font_family_label = Label(self.format_toolbar,text='Font')
        font_family_label.grid(row=0,column=0)
        font_options = ttk.Combobox(self.format_toolbar, width = 18,  
                                    textvariable = self.font_family) 
        
        # Adding combobox drop down list for font family
        font_options['values'] = ('Arial','Modern', 'Times New Roman','Courier', 'MS Serif',
                                'MS Sans Serif','Quicksand','Calibri','Cambria','Comic Sans MS',
                                'Lato','Great Vibes') 
        font_options.grid(row=0, column=1,padx=5) 
        font_options.current(0)

        #setting font size
        font_size_label = Label(self.format_toolbar,text='Size')
        font_size_label.grid(row=0,column=2)
        font_size_options = ttk.Combobox(self.format_toolbar, width = 4,  
                                    textvariable = self.font_size) 

        # Adding combobox drop down list for font size
        font_size_options['values'] = ('10','12','14','16','18','20','22','24','26','30','32',
                                        '34','36','38','40','42') 
        font_size_options.grid(row=0, column=3,padx=5) 
        font_size_options.current(1)

        #setting font color
        color_label = Label(self.format_toolbar,text='Color')
        color_label.grid(row=0,column=4)
        color_btn = Button(self.format_toolbar,width="2",command=lambda:self.select_color(color_btn)) 
        color_btn.grid(row=0,column=5,padx=5)
        color_btn.config(background='black')

        #setting font style buttons
        empty_label = Label(self.format_toolbar)
        empty_label.grid(row=0,column = 6,padx=10)
        bold = Button(self.format_toolbar,text='B',width="2",command=lambda:self.set_text_style('b'))
        bold.grid(row=0,column=7,pady=2)
        italics = Button(self.format_toolbar,text='I',width="2",command=lambda:self.set_text_style('i'))
        italics.grid(row=0,column=8,padx=7)
        underline = Button(self.format_toolbar,text='U',width="2",command=lambda:self.set_text_style('u'))
        underline.grid(row=0,column=9)

        #empty column for right margin
        empty_label = Label(self.format_toolbar)
        empty_label.grid(row=0,column =10,padx=73)

        #defining format toolbar on grid
        self.format_toolbar.grid(row=0,column=0,sticky='ns')

        #function call on change in dropbox selection
        self.font_family.trace('w', self.set_format_options)
        self.font_size.trace('w', self.set_format_options)
    
    def select_color(self,btn):
        #open color picker and select color_code
        color_code = colorchooser.askcolor(title ='Choose color')[1]
        self.text_area.config(foreground=color_code)
        btn.config(background=color_code,foreground=color_code)
        
    def set_text_style(self,id):
        #toggle b/w font styles
        if id=='b':
            self.font_bold = not self.font_bold
            if self.font_bold:
                self.bold = 'bold'
            else:
                self.bold =None
        if id=='i' :
            self.font_italics = not self.font_italics
            if self.font_italics:
                self.italic = 'italic'
            else:
                self.italic = None
        if id=='u':
            self.font_underline = not self.font_underline
            if self.font_underline:
                self.underline = 'underline'
            else:
                self.underline = None
        self.set_format_options()


    def set_format_options(self,*args):
        font = self.font_family.get()
        size = int(self.font_size.get())
        #check font styles and apply config accordingly
        if self.bold and self.italic and self.underline:
            self.text_area.config(font=(font,size,self.bold,self.italic,self.underline)) 
        elif self.bold and self.italic:
            self.text_area.config(font=(font,size,self.bold,self.italic))
        elif self.bold and self.underline:
            self.text_area.config(font=(font,size,self.bold,self.underline)) 
        elif self.italic and self.underline:
            self.text_area.config(font=(font,size,self.italic,self.underline)) 
        elif self.bold:
            self.text_area.config(font=(font,size,self.bold))         
        elif self.italic:
            self.text_area.config(font=(font,size,self.italic)) 
        elif self.underline:
            self.text_area.config(font=(font,size,self.underline)) 
        else:
            self.text_area.config(font=(font,size))

    def quit_app(self): 
        self.root.destroy() 
    
    def open_file(self): 
        self.file = askopenfilename(defaultextension='.txt', filetypes=[('All Files','*.*'), 
                    ('Text Documents','*.txt')])
        #if no file selected,set value as none
        if self.file == '': 
            self.file = None
        #else open file,delete old text in text_area and add the new text
        else: 
            self.root.title('Text Editor - '+os.path.basename(self.file)) 
            self.text_area.delete(1.0,END) 
            file = open(self.file,'r') 
            self.text_area.insert(1.0,file.read()) 
            file.close() 

          
    def new_file(self): 
        self.root.title('Untitled - Text Editor') 
        self.file = None
        self.text_area.delete(1.0,END) 
  

    def save_file(self): 
        if self.file == None: 
            self.file = asksaveasfilename(initialfile='Untitled.txt', defaultextension='.txt', 
                        filetypes=[('Text Documents','*.txt')]) 
            if self.file == '': 
                self.file = None
            else: 
                file = open(self.file,'w') 
                file.write(self.text_area.get(1.0,END)) 
                file.close() 
                self.root.title('Text Editor - '+os.path.basename(self.file)) 
              
        else: 
            file = open(self.file,'w') 
            file.write(self.text_area.get(1.0,END)) 
            file.close() 

    def save_as_file(self):
        self.file = None
        self.save_file()

    def cut(self): 
        self.text_area.event_generate("<<Cut>>") 
  
    def copy(self): 
        self.text_area.event_generate("<<Copy>>") 
  
    def paste(self): 
        self.text_area.event_generate("<<Paste>>") 

    def show_about(self): 
        messagebox.showinfo("About", "This is a basic text editor created in Tkinter.")
  
    def run(self): 
        self.root.mainloop() 
  
  
  
# Run main application 
txt_editor = TextEditor() 
txt_editor.run() 
