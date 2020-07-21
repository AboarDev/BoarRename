from rename import Rename
from tkinter import filedialog
from tkinter import *
from tkinter import ttk


class App:
    def __init__(self):
        self.rn = Rename()
        self.root = Tk()
        self.root.title('Rename Files')
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.root.resizable(FALSE,FALSE)
        self.options = ["Custom/Folder Name","sequential","4 Digit","Remove Brackets"]
        self.extensions = ["ANY"]

        self.mainframe = ttk.Frame(self.root, padding="6 6 6 6")
        self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

        self.dir_name = StringVar()
        self.a_dir = StringVar()
        self.min_var = IntVar()
        self.min_var.set(1)
        self.max_var = IntVar()
        self.max_var.set(1)
        self.a_dir.set('Directory')
        self.folder = None
        self.tree = ttk.Treeview(self.mainframe, columns=('newname'))
        self.tree.grid(column=1, row=3, columnspan=5)
        self.tree.heading('#0', text='Current Filename')
        self.tree.heading('0', text='New Filename')
        self.tree.column('#0',width=300)
        self.tree.column('0', width=300)

        self.addWhitespace = BooleanVar()
        self.addWhitespace.set(TRUE)

        self.scroll = ttk.Scrollbar(self.mainframe, orient=VERTICAL, command=self.tree.yview)
        self.scroll.grid(column=6, row=3, sticky=(N,S))

        self.tree.configure(yscrollcommand=self.scroll.set)

        self.path = ttk.Label(self.mainframe, width=100, textvariable=self.a_dir)
        self.path.grid(column=1, row=1, columnspan=5, sticky=W)

        self.dir_entry = ttk.Entry(self.mainframe, width=7, textvariable=self.dir_name)
        self.dir_entry.grid(column=1, row=2, columnspan=5, sticky=(W, E))

        self.min = ttk.Entry(self.mainframe, width=4, textvariable=self.min_var)
        self.min.grid(column=2, row=5)

        self.minMax = ttk.Label(self.mainframe, width = 10, text="Min / Max")
        self.minMax.grid(column=1,row=5)

        self.max = ttk.Entry(self.mainframe, width=4, textvariable=self.max_var)
        self.max.grid(column=3, row=5)

        self.ab = ttk.Button(self.mainframe, text='Select Directory', command=self.open_dir)
        self.ab.grid(column=3, row=8, sticky=E)

        self.refresh = ttk.Button(self.mainframe, text='refresh/preview', command=self.refresh)
        self.refresh.grid(column=4, row=8, sticky=E)

        self.spacingCheck = ttk.Checkbutton(self.mainframe,text='Add Spaces',variable = self.addWhitespace)
        self.spacingCheck.grid(column = 3, row = 6)
        self.spacingCheck.bind('<Button-1>',self.setSpacing)

        self.choseOptionLabel = ttk.Label(self.mainframe, width = 16, text="Renaming Mode")
        self.choseOptionLabel.grid(column = 1, row = 6)

        self.choseOption = ttk.Combobox(self.mainframe, values = self.options, state='readonly')
        self.choseOption.grid(column = 2, row = 6)
        self.choseOption.current(newindex = 0)
        self.choseOption.bind('<<ComboboxSelected>>',self.setMode)

        self.apply = ttk.Button(self.mainframe, text='Apply', command=self.apply)
        self.apply.grid(column=5, row=8, sticky=E)
        self.apply.state(['disabled'])

        ttk.Label(self.mainframe, text="Chose Extension").grid(row=7,column=1)

        self.selectExtension = ttk.Combobox(self.mainframe,state='readonly', values=self.extensions, postcommand=self.getExtensions)
        self.selectExtension.grid(column = 2, row =7)
        self.selectExtension.current(newindex = 0)
        self.selectExtension.bind('<<ComboboxSelected>>',self.setExtension)

        for child in self.mainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)

    def getExtensions(self):
        theExtensions = self.rn.extensions
        #theExtensions.append("ANY")
        self.selectExtension["values"] = theExtensions

    def setExtension(self, *args):
        self.rn.theExtension = self.selectExtension.current()

    def setMode(self, *args):
        self.rn.theMode = self.choseOption.current()
        print(self.rn.theMode)

    def setSpacing(self, *args):
        self.rn.addSpacing = not self.addWhitespace.get()

    def open_dir(self):
        self.folder = filedialog.askdirectory()
        if len(self.folder) > 0:
            self.a_dir.set(self.folder)
            self.folder = self.rn.inputs(self.folder)
            self.tree.delete(*self.tree.get_children())
            preview = self.rn.preview(self.folder,self.tree)
            print(self.tree)
            self.dir_name.set(preview)
            self.max_var.set(self.rn.max)
            self.apply.state(['!disabled'])
        else:
            self.apply.state(['disabled'])
            return

    def refresh(self):
        print('refreshed')
        self.tree.delete(*self.tree.get_children())
        self.dir_name.set(self.rn.preview(self.folder, self.tree,self.dir_name.get()))

    def apply(self):
        name = self.dir_name.get()
        self.rn.renames(self.folder, name, self.min_var.get(), self.max_var.get)


a_app = App()
a_app.root.mainloop()
