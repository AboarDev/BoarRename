from rename import Rename
from tkinter import filedialog
from tkinter import *
from tkinter import ttk


class App:
    def __init__(self):
        self.rn = Rename()
        self.root = Tk()
        self.root.title('BoarRename2')
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.root.resizable(FALSE,FALSE)

        self.mainframe = ttk.Frame(self.root, padding="6 6 6 6")
        self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

        self.dir_name = StringVar()
        self.a_dir = StringVar()
        self.min_var = IntVar()
        self.min_var.set(1)
        self.max_var = IntVar()
        self.max_var.set(148)
        self.a_dir.set('Directory')
        self.folder = None
        self.tree = ttk.Treeview(self.mainframe, columns=('size'))
        self.tree.grid(column=1, row=3, columnspan=5)
        self.tree.insert('', 'end', 'widgets', text='Widget Tour', values=(''))
        self.tree.heading('#0', text='Current Filename')
        self.tree.heading('0', text='New Filename')

        self.path = ttk.Label(self.mainframe, width=50, textvariable=self.a_dir)
        self.path.grid(column=1, row=1, columnspan=5, sticky=W)

        self.dir_entry = ttk.Entry(self.mainframe, width=7, textvariable=self.dir_name)
        self.dir_entry.grid(column=1, row=2, columnspan=5, sticky=(W, E))

        self.min = ttk.Entry(self.mainframe, width=4, textvariable=self.min_var)
        self.min.grid(column=3, row=4)

        self.max = ttk.Entry(self.mainframe, width=4, textvariable=self.max_var)
        self.max.grid(column=4, row=4)

        self.ab = ttk.Button(self.mainframe, text='Select Directory', command=self.open_dir)
        self.ab.grid(column=1, row=4, sticky=W)

        self.refresh = ttk.Button(self.mainframe, text='refresh/preview')
        self.refresh.grid(column=2, row=4, sticky=W)

        self.apply = ttk.Button(self.mainframe, text='Apply', command=self.apply)
        self.apply.grid(column=5, row=4, sticky=E)
        self.apply.state(['disabled'])

        for child in self.mainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)

    def open_dir(self):
        self.folder = filedialog.askdirectory()
        if len(self.folder) > 0:
            self.a_dir.set(self.folder)
            self.folder = self.rn.inputs(self.folder)
            preview = self.rn.preview(self.folder)
            self.dir_name.set(preview)
            self.apply.state(['!disabled'])
        else:
            self.apply.state(['disabled'])
            return

    def apply(self):
        name = self.dir_name.get()
        self.rn.renames(self.folder, name, self.min_var.get(), self.max_var.get)


a_app = App()
a_app.root.mainloop()
