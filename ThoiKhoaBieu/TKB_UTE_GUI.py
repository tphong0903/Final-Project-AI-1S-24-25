import pandas as pd
from constraint import *
from time import time
import numpy as np
from tkinter import * 
from tkinter import ttk
import tkinter as tk
from tkinter import filedialog, messagebox
class Teacher:
    def __init__(self, id, subjects):
        self.id = id
        self.subjects = subjects

class Class:

    def __init__(self, id, subjects):
        self.id = id
        self.subjects = subjects



options = {"Giáo Viên": [""], "Lớp": [""]}
optionClass = []
optionTeacher =[]
numberRoom = 0

def SapXep(file_path):
    # xử lý file excel
    dataframe1 = pd.read_excel(file_path)
    dataframe_cleaned = dataframe1.loc[:, ~dataframe1.columns.str.contains('^Unnamed')]
    dataframe_cleaned = dataframe_cleaned.dropna()

    #list Teacher
    teacherID_data = dataframe_cleaned["CBGD"].unique()

    #list Class
    classID_data = set()
    for classes in dataframe_cleaned["Lớp"]:
        split_classes = classes.split(',') 
        for class_id in split_classes:
            classID_data.add(class_id.strip())
    classID_data = list(classID_data)

    listTeacher = []
    listClass = []
    listAllSubject = list(dataframe_cleaned["Mã LHP"].unique())

    for id in teacherID_data:
        listSubjectOfTeacher = set()
        for index, row in dataframe_cleaned.iterrows():
            if row["CBGD"] == id:
                listSubjectOfTeacher.add(row["Mã LHP"])
        listTeacher.append(Teacher(id,listSubjectOfTeacher))

    for id in classID_data:
        listSubjectOfClass = set()
        for index, row in dataframe_cleaned.iterrows():
            if id in row["Lớp"]:
                listSubjectOfClass.add(row["Mã LHP"])
        listClass.append(Class(id,listSubjectOfClass))

    L = len(listAllSubject)
    numberRoom = (int(L/18)+1)
    print('Số lượng môn học là: %d' % L)

    sch_problem = Problem(BacktrackingSolver())

    sch_problem.addVariables(listAllSubject, list(range(1, numberRoom*18)))
    sch_problem.addConstraint(AllDifferentConstraint(), listAllSubject)

    for teacher in listTeacher:
        sch_problem.addConstraint(FunctionConstraint(kiem_tra_trung),list(teacher.subjects))

    print('Running...')
    start = time()
    soln_dts = sch_problem.getSolution()
    elapsed = time() - start
    print('Mất %d giây' % elapsed)

    if soln_dts is not None:
        data_sorted = dict(sorted(soln_dts.items(), key=lambda item: item[1], reverse=False))
        return data_sorted,listClass,listTeacher

def kiem_tra_trung(*values):
    data = list(values)
    data.sort()
    L = len(data)
    ket_qua = True
    for i in range(0, L-1):
        x = data[i]

        kiem_tra = []
        y = x
        while (True):
            y = y + 18
            if y >  numberRoom*18:
                break
            kiem_tra.append(y)
        phan_con_lai = data[i+1:]
        for v in phan_con_lai:
            if v in kiem_tra:
                ket_qua = False
                return ket_qua
    return ket_qua


def SetTKB(value,x,rows,phong):
    T2_buoi_1 = np.array([1, 19, 37, 55])
    T2_buoi_2 = T2_buoi_1 + 6
    T2_buoi_3 = T2_buoi_2 + 6

    T3_buoi_1 = T2_buoi_1 + 1
    T3_buoi_2 = T3_buoi_1 + 6
    T3_buoi_3 = T3_buoi_2 + 6

    T4_buoi_1 = T3_buoi_1 + 1
    T4_buoi_2 = T4_buoi_1 + 6
    T4_buoi_3 = T4_buoi_2 + 6

    T5_buoi_1 = T4_buoi_1 + 1
    T5_buoi_2 = T5_buoi_1 + 6
    T5_buoi_3 = T5_buoi_2 + 6

    T6_buoi_1 = T5_buoi_1 + 1
    T6_buoi_2 = T6_buoi_1 + 6
    T6_buoi_3 = T6_buoi_2 + 6

    T7_buoi_1 = T6_buoi_1 + 1
    T7_buoi_2 = T7_buoi_1 + 6
    T7_buoi_3 = T7_buoi_2 + 6
    # T2
    if value in list(T2_buoi_1):
        vi_tri = list(T2_buoi_1).index(value)
        rows[0][0] = x + '\nPhòng: ' + phong[vi_tri]
    elif value in list(T2_buoi_2):
        vi_tri = list(T2_buoi_2).index(value)
        rows[1][0] = x + '\nPhòng: ' + phong[vi_tri]
    elif value in list(T2_buoi_3):
        vi_tri = list(T2_buoi_3).index(value)
        rows[2][0] = x + '\nPhòng: ' + phong[vi_tri]

    # T3        
    elif value in list(T3_buoi_1):
        vi_tri = list(T3_buoi_1).index(value)
        rows[0][1] = x + '\nPhòng: ' + phong[vi_tri]
    elif value in list(T3_buoi_2):
        vi_tri = list(T3_buoi_2).index(value)
        rows[1][1] = x + '\nPhòng: ' + phong[vi_tri]
    elif value in list(T3_buoi_3):
        vi_tri = list(T3_buoi_3).index(value)
        rows[2][1] = x + '\nPhòng: ' + phong[vi_tri]

    # T4        
    elif value in list(T4_buoi_1):
        vi_tri = list(T4_buoi_1).index(value)
        rows[0][2] = x + '\nPhòng: ' + phong[vi_tri]
    elif value in list(T4_buoi_2):
        vi_tri = list(T4_buoi_2).index(value)
        rows[1][2] = x + '\nPhòng: ' + phong[vi_tri]
    elif value in list(T4_buoi_3):
        vi_tri = list(T4_buoi_3).index(value)
        rows[2][2] = x + '\nPhòng: ' + phong[vi_tri]

    # T5
    elif value in list(T5_buoi_1):
        vi_tri = list(T5_buoi_1).index(value)
        rows[0][3] = x + '\nPhòng: ' + phong[vi_tri]
    elif value in list(T5_buoi_2):
        vi_tri = list(T5_buoi_2).index(value)
        rows[1][3] = x + '\nPhòng: ' + phong[vi_tri]
    elif value in list(T5_buoi_3):
        vi_tri = list(T5_buoi_3).index(value)
        rows[2][3] = x + '\nPhòng: ' + phong[vi_tri]

    # T6
    elif value in list(T6_buoi_1):
        vi_tri = list(T6_buoi_1).index(value)
        rows[0][4] = x + '\nPhòng: ' + phong[vi_tri]
    elif value in list(T6_buoi_2):
        vi_tri = list(T6_buoi_2).index(value)
        rows[1][4] = x + '\nPhòng: ' + phong[vi_tri]
    elif value in list(T6_buoi_3):
        vi_tri = list(T6_buoi_3).index(value)
        rows[2][4] = x + '\nPhòng: ' + phong[vi_tri]

    # T7
    elif value in list(T7_buoi_1):
                vi_tri = list(T7_buoi_1).index(value)
                rows[0][5] = x + '\nPhòng: ' + phong[vi_tri]
    elif value in list(T7_buoi_2):
                vi_tri = list(T7_buoi_2).index(value)
                rows[1][5] = x + '\nPhòng: ' + phong[vi_tri]
    elif value in list(T7_buoi_3):
                vi_tri = list(T7_buoi_3).index(value)
                rows[2][5] = x + '\nPhòng: ' + phong[vi_tri]   
    return rows




class App(tk.Tk):
    def	__init__(self):
        super().__init__()
        self.title('Sắp xếp TKB')
        self.geometry('1200x750')
        
        Label(self, text="Sắp xếp Thời Khóa Biểu tự động",fg="Red" ,font=("Arial Bold", 20)).grid(row=0, column=0, columnspan=3, pady=10)
        Label(self, text="Chọn file excel(như file mẫu: DataTest.xlsx): ", font=("Arial", 15)).grid(row=1, column=0, columnspan=2, pady=10)

        self.tphong_file_btn = Button(self, text="File", command=self.tphong_handle_file_input, width=20)
        self.tphong_file_btn.grid(row=1, column=1,columnspan=3, pady=10)

        Label(self, text="File đã chọn:", font=("Arial", 15)).grid(row=2, column=0, columnspan=3, pady=10)
        self.phong24_result_text = Text(self, height=2, width=60)
        self.phong24_result_text.grid(row=3, column=0, columnspan=3, pady=10)

        self.tphong_read_btn = Button(self, text="Sắp xếp", command=self.tphong_handle_SapXep, width=20)
        self.tphong_read_btn.grid(row=4, column=0,columnspan=3, pady=10)

        #Choice 
        self.selected_choice = StringVar(self)
        self.selected_choice.set("Giáo Viên")  # Đặt giá trị mặc định là "Choice 1"
        self.selected_choice.trace("w",self.on_select_choice)

        self.option_choice = StringVar(self)

        self.radio_button1 = Radiobutton(self, text="Giáo Viên", variable=self.selected_choice, value="Giáo Viên")
        self.radio_button1.grid(row=5, column=0,columnspan=2, pady=10)

        self.radio_button2 = Radiobutton(self, text="Lớp", variable=self.selected_choice, value="Lớp")
        self.radio_button2.grid(row=5, column=1,columnspan=3, pady=10)

        # Thay thế bằng Listbox và Scrollbar
        self.listbox_frame = Frame(self)
        self.listbox_frame.grid(row=6, column=0, columnspan=3, pady=10)

        self.option_listbox = Listbox(self.listbox_frame, height=5, width=50)
        self.option_listbox.pack(side=LEFT, fill=BOTH)

        self.scrollbar = Scrollbar(self.listbox_frame)
        self.scrollbar.pack(side=RIGHT, fill=Y)

        self.option_listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.option_listbox.yview)

        self.tphong_read_btn = Button(self, text="In", command=self.tphong_handle_In, width=20)
        self.tphong_read_btn.grid(row=7, column=0,columnspan=3, pady=10)


        self.style = ttk.Style()
        # Thiết lập cho Treeview
        self.style.configure("Treeview", rowheight=40) 
        # Create Treeview table
        self.tree = ttk.Treeview(self, columns=('Giờ', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7'), show='headings')
        for col in ('Giờ','T2', 'T3', 'T4', 'T5', 'T6', 'T7'):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)
        self.tree.grid(row=8, column=0,columnspan=3, pady=10)


        for i in range(3):
            self.grid_columnconfigure(i, weight=1)

    def TKB_GV(self,data,GV):
        rows = [
            ['', '', '', '', '', ''],
            ['', '', '', '', '', ''],
            ['', '', '', '', '', '']
        ]
        phong = {0:'A3_304', 1:'A3_305', 2:'A3_306', 3:'A3_306',4:'A3_307',5:'A3_309',6:'A3_309',7:'A3_310'}
        for i in range(0, 3):
            for j in range(0, 6):
                rows[i][j] = ''
        MaGV=GV.id
        for x in GV.subjects:
            value = data[x]
            rows = SetTKB(value,x,rows,phong)    

        self.create_table(rows)

    def tphong_handle_file_input(self):
        self.phong_file_path = filedialog.askopenfilename( title="Chọn file Excel",filetypes=[("Excel Files", "*.xlsx")])
        self.phong24_result_text.delete('1.0', END)
        self.phong24_result_text.insert(END, self.phong_file_path)

    def tphong_handle_SapXep(self):
        file_path = self.phong24_result_text.get("1.0", END).strip()
        global data,listClass,listTeacher
        data,listClass,listTeacher = SapXep(file_path)
        if data is not None:
            for x in listTeacher:
                optionTeacher.append(int(x.id))
            for x in listClass:
                optionClass.append(x.id)
            self.on_select_choice()
            messagebox.showinfo("Thông báo", "Sắp xong ròi nè!!")

    # Cập nhật danh sách trong Listbox
    def update_listbox(self):
        self.option_listbox.delete(0, END)
        if self.selected_choice.get() == "Giáo Viên":
            options_list = optionTeacher
        else:
            options_list = optionClass
            
        for option in options_list:
            self.option_listbox.insert(END, option)

    # Thiết lập sự kiện theo dõi thay đổi của selected_choice
    def on_select_choice(self,*args):
        self.update_listbox() 

    def tphong_handle_In(self):
        selected_indices = self.option_listbox.curselection()
        if selected_indices:  
            selected_value = self.option_listbox.get(selected_indices[0])
            selected=self.selected_choice.get()
            if selected == "Giáo Viên":
                for gv in listTeacher:
                    if(gv.id == selected_value):
                        if(gv.subjects is None):
                            messagebox.showinfo("Thông báo", "Không tìm thấy TKB!!")
                        else:
                            self.TKB_GV(data,gv)
                            break
            else:
                for mon in listClass:
                    if(str(mon.id) == selected_value):
                        if(mon.subjects is None):
                            messagebox.showinfo("Thông báo", "Không tìm thấy TKB!!")
                        else:
                            self.TKB_GV(data,mon)
                            break
        else:
            print("Không có mục nào được chọn.")

    def create_table(self,rows):
        for item in self.tree.get_children():
            self.tree.delete(item)
        default_time = ["7h-10h30","11h30-15h","16h-19h30"]
        i=0
        for row in rows:
            self.tree.insert('', 'end', values=(default_time[i], *row))
            i+=1


if	__name__ ==	"__main__":
    app	= App()
    app.mainloop()