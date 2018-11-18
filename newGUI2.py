from tkinter import *
from tkinter import font
from tkinter import messagebox
from tkinter.filedialog import askopenfilenames
from tkinter.ttk import Treeview
import output_file as of
import manger as mg
from PIL import ImageTk, Image
import dbi as db
import os
import shutil
import moce_dir

####gui for the program
class Application(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.grid()
        self.focus_force()
        self.create_widgets()
        self.mydb=db.DBHandler()
        self.mydb.connect()
        self.mydb.build_dictionary()

    def create_widgets(self):
        self.user = StringVar()
        self.frame = Frame(self, width=1000, height=600)
        self.frame.grid(row = 0,column = 1)
        self.img = ImageTk.PhotoImage(Image.open('back.jpg'))
        self.background = Label(self, image=self.img)
        self.background.place(x=0, y=0, relwidth=1, relheight=1)
        self.fontemp = font.Font(self, size=30, weight='bold')
        self.fontemp2 = font.Font(self, size=10, weight='bold')
        self.head = Label(self, text="Ultimate Cat Search 2018",font=self.fontemp)
        self.head.config(bg="#E8EAE6")
        self.head.place(x=255,y=100)
        self.enterText = Entry(self,width=140,textvariable=self.user)
        self.enterText.grid(row = 0,column = 1)
        self.Submit = Button(self, text="Cat Search", command=self.search, height=3, width=10,font=self.fontemp2)
        self.Submit.place(x = 445,y = 350)
        self.adminButton = Button(self, text="Admin", command=self.popup_Login, height=2, width=5,font=self.fontemp2)
        self.adminButton.place(x=10, y=10)
        self.help=Button(self,text="Help", command=self.help, height=2, width=7,font=self.fontemp2)
        self.help.place(x=65, y=10)

    def search(self):
        moce_dir.delete_takeFrom()
        search_result= self.mydb.search(self.user.get())
        # print('search_result: ',search_result)
        if search_result.__len__() == 0:
            # print(' search ended Not found any')
            messagebox.showinfo("ERROR", "NOT FOUND ANY MATCH TRY AGAIN")
        else:
            self.result = Toplevel()
            self.result.wm_title("search result")
            self.result.geometry("900x500+30+30")
            self.result.grid()
            self.result.entries = {}
            self.result.tableheight = search_result.__len__()
            self.result.tablewidth = 5

            self.result.tree = Treeview(self.result)
            self.result.tree['columns'] = ('Title', 'Author', 'Languages','Brief')
            self.result.tree.heading("#0", text='Document',anchor='w')
            self.result.tree.column("#0", width=65 ,anchor="w")
            self.result.tree.heading('Title', text='Title')
            self.result.tree.column('Title', anchor='center', stretch=True)
            self.result.tree.heading('Author', text='Author')
            self.result.tree.column('Author', anchor='center', stretch=True)
            self.result.tree.heading('Languages', text='Languages')
            self.result.tree.column('Languages', anchor='center', stretch=True)
            self.result.tree.heading('Brief', text='Brief')
            self.result.tree.column('Brief', anchor='center', stretch=True)
            self.result.tree.grid(sticky=(N, S, W, E))
            self.result.tree.grid_rowconfigure(0, weight=1)
            self.result.tree.grid_columnconfigure(0, weight=1)

            for row in range(self.result.tableheight):
                    self.result.tree.insert('', 'end',text=search_result[row][0], values=(search_result[row][1],search_result[row][2],search_result[row][3],search_result[row][4]) )
            self.result.tree.bind("<Double-1>", self.OnDoubleClick)

    def OnDoubleClick(self,event):
        item = self.result.tree.selection()[0]
        # print("you clicked on", self.result.tree.item(item, "text"))
        doc=self.mydb.get_one_doc_by_id(self.result.tree.item(item, "text"))
        self.openFile(doc)

    def openFile(self,doc):
        # print('doc: ',doc[5])
        of.output_File(doc[5],self.mydb.tokens)

    def admin(self):
        self.admin= Toplevel()
        self.admin.wm_title("Admin Login")
        self.admin.geometry("450x300+30+30")
        self.admin.background = Label(self.admin)
        self.admin.background.place(x=0, y=0, relwidth=1, relheight=1)
        self.admin.add_button= Button(self.admin,text="Add Files", command=self.addFiles,height=2, width=7,font=self.fontemp2)
        self.admin.add_button.place(x=15, y=10)
        self.admin.IndexFiles= Button(self.admin, text="Index Files", command=self.IndexFiles, height=2, width=9,font=self.fontemp2)
        self.admin.IndexFiles.place(x=100, y=10)
        self.admin.remove= Button(self.admin, text="Remove", command=self.remove, height=2, width=9,font=self.fontemp2)
        self.admin.remove.place(x=200, y=10)
        self.admin.restore = Button(self.admin, text="Restore", command=self.restore, height=2, width=9, font=self.fontemp2)
        self.admin.restore.place(x=300, y=10)

    def popup_Login(self):
        self.win = Toplevel()
        self.win.wm_title("Admin Login")
        self.win.geometry("270x200+30+30")
        self.win.label_username = Label(self.win, text="Username",font=self.fontemp2)
        self.win.label_password = Label(self.win, text="Password",font=self.fontemp2)
        self.win.entry_username = Entry(self.win)
        self.win.entry_password = Entry(self.win, show="*")
        self.win.label_username.grid(row=2, sticky=E,column=3,pady=10,padx=10)
        self.win.label_password.grid(row=3, sticky=E,column=3,pady=10,padx=10)
        self.win.entry_username.grid(row=2, column=4)
        self.win.entry_password.grid(row=3, column=4)
        self.win.b = Button(self.win, text="Submit", command=self.checkLogin ,font=self.fontemp2)
        self.win.b.grid(row=4, column=3)

    def checkLogin(self):
        username = self.win.entry_password.get()
        password = self.win.entry_password.get()
        if username == "admin" and password == "admin":
            self.win.destroy()
            self.admin()
        else:
            messagebox.showinfo("Login error","Admin login Error")

    def IndexFiles(self):
        result=mg.main()
        if result==0:
            print("success index files")
        self.mydb.build_dictionary()

    def addFiles(self):
        try:
            curr_directory = os.getcwd()+"/source"
            filez= askopenfilenames(initialdir=curr_directory, title="Select file",filetypes=(("Text File", "*.txt"), ("all files", "*.*")))
            for f in filez:
                if os.path.isfile(f):
                    shutil.copy2(f,curr_directory)

        except:
            print("No file exists")
        print("success")

    def help(self):
        self.help_view = Toplevel()
        self.help_view.wm_title("Help View")
        self.help_view.geometry("670x400+30+30")
        str1="Search Engine\n"
        str2="For actions click on the buttons.\n"
        str3="Admin is the mangement tool for the program.\n"
        str4="Add files :browse and choose files for indexing.\n"+"index files :index the files.\n"
        str5="Remove:remove docs.\n"
        str6="Query:using boolean search for example (a AND b)OR c // (a AND b)NOT c \n"
        strpr=str1+str2+str3+str4+str5+str6
        self.help_view.t=Text(self.help_view,height=400,width=600)
        self.help_view.t.insert(END,strpr)
        self.help_view.t.pack()

    def remove(self):
        search_result = self.mydb.get_all_doc()
        if search_result.__len__() == 0:
            print(' search ended Not found any')
            messagebox.showinfo("ERROR", "NOT FOUND ANY MATCH TRY AGAIN")
        else:
            self.remove_view = Toplevel()
            self.remove_view.wm_title("search result")
            self.remove_view.geometry("900x500+30+30")
            self.remove_view.grid()
            self.remove_view.entries = {}
            self.remove_view.tableheight = search_result.__len__()
            self.remove_view.tablewidth = 5

            self.remove_view.tree = Treeview(self.remove_view)
            self.remove_view.tree['columns'] = ('Title', 'Author', 'Languages', 'Brief')
            self.remove_view.tree.heading("#0", text='Document', anchor='w')
            self.remove_view.tree.column("#0", width=65, anchor="w")
            self.remove_view.tree.heading('Title', text='Title')
            self.remove_view.tree.column('Title', anchor='center', stretch=True)
            self.remove_view.tree.heading('Author', text='Author')
            self.remove_view.tree.column('Author', anchor='center', stretch=True)
            self.remove_view.tree.heading('Languages', text='Languages')
            self.remove_view.tree.column('Languages', anchor='center', stretch=True)
            self.remove_view.tree.heading('Brief', text='Brief')
            self.remove_view.tree.column('Brief', anchor='center', stretch=True)
            self.remove_view.tree.grid(sticky=(N, S, W, E))
            self.remove_view.tree.grid_rowconfigure(0, weight=1)
            self.remove_view.tree.grid_columnconfigure(0, weight=1)


            for row in range(self.remove_view.tableheight):
                    self.remove_view.tree.insert('', 'end',text=search_result[row][0], values=(search_result[row][1],search_result[row][2],search_result[row][3],search_result[row][4]) )
            self.remove_view.tree.bind("<Double-1>", self.OnDoubleClick2)

    def OnDoubleClick2(self,event):
        item = self.remove_view.tree.selection()[0]
        # print("you clicked on", self.remove_view.tree.item(item, "text"))
        doc=self.mydb.get_one_doc_by_id(self.remove_view.tree.item(item, "text"))
        print('hidden_docs.append',doc[0])
        self.mydb.dictionary.hidden_docs.append(doc[0])
        str1=str(doc[0])
        stri="the file removed "+str1
        messagebox.showinfo("Remove", stri)

    def restore(self):
        search_result = self.mydb.get_hidden_file(self.mydb.dictionary.hidden_docs)
        if search_result.__len__() == 0:
            print(' restore Not found any')
            messagebox.showinfo("ERROR", "NOT FOUND ANY MATCH TRY AGAIN")
        else:
            self.restore = Toplevel()
            self.restore.wm_title("restore")
            self.restore.geometry("900x500+30+30")
            self.restore.grid()
            self.restore.entries = {}
            self.restore.tableheight = search_result.__len__()
            self.restore.tablewidth = 5

            self.restore.tree = Treeview(self.restore)
            self.restore.tree['columns'] = ('Title', 'Author', 'Languages', 'Brief')
            self.restore.tree.heading("#0", text='Document', anchor='w')
            self.restore.tree.column("#0", width=65, anchor="w")
            self.restore.tree.heading('Title', text='Title')
            self.restore.tree.column('Title', anchor='center', stretch=True)
            self.restore.tree.heading('Author', text='Author')
            self.restore.tree.column('Author', anchor='center', stretch=True)
            self.restore.tree.heading('Languages', text='Languages')
            self.restore.tree.column('Languages', anchor='center', stretch=True)
            self.restore.tree.heading('Brief', text='Brief')
            self.restore.tree.column('Brief', anchor='center', stretch=True)
            self.restore.tree.grid(sticky=(N, S, W, E))
            self.restore.tree.grid_rowconfigure(0, weight=1)
            self.restore.tree.grid_columnconfigure(0, weight=1)

            for row in range(self.restore.tableheight):
                self.restore.tree.insert('', 'end', text=search_result[row][0], values=(
                search_result[row][1], search_result[row][2], search_result[row][3], search_result[row][4]))
            self.restore.tree.bind("<Double-1>", self.OnDoubleClick3)

    def OnDoubleClick3(self, event):
        item = self.restore.tree.selection()[0]
        # print("you clicked on", self.remove_view.tree.item(item, "text"))
        doc = self.mydb.get_one_doc_by_id(self.restore.tree.item(item, "text"))
        print('hidden_docs.append', doc[0])
        self.mydb.dictionary.un_hide_doc(doc[0])
        str1 = str(doc[0])
        stri = "the file restore " + str1
        messagebox.showinfo("restore", stri)


if __name__ == "__main__":
    root = Tk()
    root.title("Cat Search")
    app = Application(master=root)
    app.mainloop()

