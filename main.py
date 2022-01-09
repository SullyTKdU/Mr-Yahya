from tkinter import *
import random
import sqlite3
from tkinter import ttk
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.messagebox import showinfo
from tkinter import messagebox


class MyWindow:
    def __init__(self, win):
        self.window = win
      

        self.StudentID_lbl = Label(win,
                                   text='Student ID',
                                   bg="LavenderBlush4",
                                   font=("Times", 8, "bold", "italic"))
        self.StudentID_lbl.place(x=10, y=10)
        self.StudentID_ent = Entry(
            bd=1,
            width=10,
        )
        self.StudentID_ent.place(x=90, y=4)

        self.clicked = StringVar()
        self.clicked.set("Edit data")
        options = ["First Name", "Last name", "Age"]
        self.drop = OptionMenu(win, self.clicked, *options)
        self.drop.place(y=500, x=640)

        self.Editdata_lbl = Label(win,
                                  text='Edit data\nwith\nStudentID',
                                  bg="LavenderBlush4",
                                  font=("Times", 8, "bold", "italic"))
        self.Editdata_lbl.place(x=450, y=500)
        self.Editdata_ent = Entry(
            bd=1,
            width=10,
        )
        self.Editdata_ent.place(x=525, y=500)
        self.t10 = Entry(
            bd=1,
            width=10,
        )
        self.t10.place(x=525, y=530)
        self.edit = Button(win,
                           text='edit',
                           command=self.edit,
                           bg="slate gray")
        self.edit.place(x=460, y=565)

        self.firstname_lbl = Label(win,
                                   text='First name',
                                   bg="LavenderBlush4",
                                   font=("Times", 8, "bold", "italic"))
        self.firstname_lbl.place(x=200, y=10)
        self.firstname_ent = Entry(
            bd=1,
            width=30,
        )
        self.firstname_ent.place(x=280, y=5)

        self.surname_lbl = Label(win,
                                 text='Surname',
                                 bg="LavenderBlush4",
                                 font=("Times", 8, "bold", "italic"))
        self.surname_lbl.place(x=200, y=40)
        self.surname_ent = Entry(bd=1, width=30)
        self.surname_ent.place(x=280, y=35)

        self.Age_lbl = Label(win,
                             text='Age',
                             bg="LavenderBlush4",
                             font=("Times", 8, "bold", "italic"))
        self.Age_lbl.place(x=10, y=40)
        self.Age_ent = Entry(bd=1, width=10)
        self.Age_ent.place(x=90, y=35)

        self.Delete_lbl = Label(win,
                                text='Delete student\nusing ID',
                                bg="LavenderBlush4",
                                font=("Times", 8, "bold", "italic"))
        self.Delete_lbl.place(x=20, y=500)
        self.delete_ent = Entry(bd=3, width=10)
        self.delete_ent.place(x=120, y=500)
        self.delete = Button(win,
                             text=' Delete',
                             command=self.delete,
                             bg="slate grey")
        self.delete.place(x=20, y=550)

        self.search_lbl = Label(win,
                                text='Search\nusing ID',
                                bg="LavenderBlush4",
                                font=("Times", 8, "bold", "italic"))
        self.search_lbl.place(x=270, y=500)
        self.search_ent = Entry(bd=1, width=10)
        self.search_ent.place(x=330, y=500)
        self.search_bt = Button(win,
                                text=' Search',
                                command=self.search,
                                bg="slate grey")
        self.search_bt.place(x=270, y=550)

        

        self.store_bt = Button(win,
                               text=' Store Data',
                               command=self.store,
                               bg="slate grey")
        self.store_bt.place(x=170, y=90)

        self.show_bt = Button(win,
                              text=' Show Data',
                              command=self.check,
                              bg="slate grey")
        self.show_bt.place(x=280, y=90)

        

    def store(self):
        
        StudentID = (self.StudentID_ent.get())
        Firstname = (self.firstname_ent.get())
        Surname = (self.surname_ent.get())
        Age = (self.Age_ent.get())

        print(len(Surname),len(Firstname))

        self.StudentID_ent.delete(0, 'end')
        self.firstname_ent.delete(0, 'end')
        self.surname_ent.delete(0, 'end')
        self.Age_ent.delete(0, 'end')
       
        print((len(Firstname), len(Surname) , len(Age)))

        if len(StudentID)!=6:
            messagebox.showerror(title="Length error", message="The student ID must be 6 digits long")
            MyWindow(win)
        if (len(Firstname)==0 or len(Surname)==0 or len(Age)==0) :
            messagebox.showerror(title="Input error", message="There must be an input for each field")
            MyWindow(win)
        

        self.conn = sqlite3.connect("students.db")
        self.c = self.conn.cursor()
        self.c.execute("""CREATE TABLE IF NOT EXISTS students (
              firstname VARCHAR,
              Surname VARCHAR, 
              Age INTEGER,
              StudentID INTEGER
      );""")
        self.c.execute("INSERT INTO students VALUES (?, ?, ?, ?);",
                       (Firstname, Surname, Age, StudentID))
        self.conn.commit()
        self.conn.close()

        

    def check(self):
        self.conn = sqlite3.connect("students.db")
        self.c = self.conn.cursor()

        h = self.c.execute("SELECT * FROM students")
        item = self.c.fetchall()
        i = 999

        columns = ('first_name', 'last_name', 'Age', 'StudentID')
        self.tree = ttk.Treeview(self.window, columns=columns, show='headings')
        self.tree.heading('first_name', text='First Name')
        self.tree.heading('last_name', text='Last Name')
        self.tree.heading('StudentID', text='StudentID')
        self.tree.heading('Age', text='Age')
        for items in item:
            self.tree.insert('', tk.END, values=items)
        self.tree.grid(row=40, column=0, sticky='nsew')
        self.tree.place(y=190, x=20)
        scrollbar = ttk.Scrollbar(
            self.window,
            orient=tk.VERTICAL,
            command=self.tree.yview,
        )
        self.tree.configure(yscroll=scrollbar.set)
        
        scrollbar.grid(row=0, column=1, sticky='ns')
        scrollbar.place(y=20)
        print("Successfully added!")

        self.conn.commit()
        self.conn.close()

    def delete(self):
        ID = self.delete_ent.get()
        self.conn = sqlite3.connect("students.db")
        self.c = self.conn.cursor()
        self.c.fetchall
        self.c.execute("""DELETE from students where StudentID=(?);""", (ID, ))
        self.conn.commit()
        self.conn.close()
        print("Succesfully deleted!")
        self.delete_ent.delete(0, 'end')

    def search(self):
        ID = self.search_ent.get()
        for record in self.tree.get_children():
            self.tree.delete(record)
        self.conn = sqlite3.connect("students.db")
        self.c = self.conn.cursor()
        self.c.fetchall
        self.c.execute("SELECT * FROM students WHERE StudentID=(?);", (ID, ))
        item = self.c.fetchall()
        for items in item:
            self.tree.insert('', tk.END, values=items)
        print("Search complete")

    def refresh(self):
        self.conn = sqlite3.connect("students.db")
        self.c = self.conn.cursor()

        h = self.c.execute("SELECT * FROM students")
        item = self.c.fetchall()

        columns = ('first_name', 'last_name', 'Age', 'StudentID')
        self.tree = ttk.Treeview(self.window, columns=columns, show='headings')
        self.tree.heading('first_name', text='First Name')
        self.tree.heading('last_name', text='Last Name')
        self.tree.heading('StudentID', text='StudentID')
        self.tree.heading('Age', text='Age')
        for items in item:
            self.tree.insert('', tk.END, values=items)
        self.tree.grid(row=40, column=0)
        self.tree.place(y=190, x=20)
        scrollbar = ttk.Scrollbar(self.window,
                                  orient=tk.VERTICAL,
                                  command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=5, column=1)
        scrollbar.place(y=200)
        for items in item:
            print(item)

            self.conn.commit()
            self.search_ent.delete(0, 'end')

    def edit(self):
        self.conn = sqlite3.connect("students.db")
        self.c = self.conn.cursor()
        Column = (self.clicked.get())
        Change = (self.t10.get())
        ID = (self.Editdata_ent.get())
        print(Column)

        if Column == "First Name":
            self.c.execute("SELECT * FROM students")
            self.c.execute(
                """UPDATE students set  firstname = (?) WHERE StudentID = (?);""",
                (
                    Change,
                    ID,
                ))
            print("Succesfully updated")

        elif Column == "Last name":
            self.c.execute("SELECT * FROM students")
            self.c.execute(
                """UPDATE students set Surname = (?) WHERE StudentID= (?);""",
                (
                    Change,
                    ID,
                ))
            print("Succesfully updated")

        elif Column == "Age":
            int(Change)
            self.c.execute("SELECT * FROM students")
            self.c.execute(
                """UPDATE students set  Age = (?) WHERE StudentID = (?);""", (
                    Change,
                    ID,
                ))
            print("Succesfully updated")
        self.conn.commit()
        self.conn.close()
        self.Editdata_ent.delete(0, 'end')
        self.t10.delete(0, 'end')

    def clear(self):
        self.conn = sqlite3.connect("students.db")
        self.c = self.conn.cursor()
        self.c.execute("SELECT * FROM students")
        self.c.execute('DELETE FROM students;', )
        print("table successfully cleared")
        self.conn.commit()
        self.conn.close()

    def generate(self):
       self.gen_num=random.randint(100000,999999)
       self.Random_ent.delete(0, 'end')
       self.Random_ent.insert(END,str(self.gen_num))

    def use(self):
      self.StudentID_ent.delete(0, 'end')
      self.Random_ent.delete(0, 'end')
      self.StudentID_ent.insert(END,str(self.gen_num))



window = tk.Tk()
mywin = MyWindow(window)
window.title('Hello Python')
window.geometry("500x300+10+10")
window.attributes('-fullscreen', True)
window.configure(bg='LavenderBlush4')
window.mainloop()
