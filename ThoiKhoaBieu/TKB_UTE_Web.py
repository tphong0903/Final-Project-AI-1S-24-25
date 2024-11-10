import pandas as pd
import numpy as np
from constraint import *
import streamlit as st
import time
class Teacher:
    def __init__(self, id, subjects):
        self.id = id
        self.subjects = subjects

class Class:
    def __init__(self, id, subjects):
        self.id = id
        self.subjects = subjects
        
numberRoom=0

def SapXep(file_path):
    dataframe1 = pd.read_excel(file_path)
    dataframe_cleaned = dataframe1.loc[:, ~dataframe1.columns.str.contains('^Unnamed')]
    dataframe_cleaned = dataframe_cleaned.dropna()

    teacherID_data = dataframe_cleaned["CBGD"].unique()

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
        listTeacher.append(Teacher(id, listSubjectOfTeacher))

    for id in classID_data:
        listSubjectOfClass = set()
        for index, row in dataframe_cleaned.iterrows():
            if id in row["Lớp"]:
                listSubjectOfClass.add(row["Mã LHP"])
        listClass.append(Class(id, listSubjectOfClass))

    L = len(listAllSubject)
    numberRoom = (int(L / 18) + 1)
    st.write(f'Số lượng môn học là: {L}')

    sch_problem = Problem(BacktrackingSolver())
    sch_problem.addVariables(listAllSubject, list(range(1, numberRoom * 18)))
    sch_problem.addConstraint(AllDifferentConstraint(), listAllSubject)

    for teacher in listTeacher:
        sch_problem.addConstraint(FunctionConstraint(kiem_tra_trung), list(teacher.subjects))

    start = time.time()
    soln_dts = sch_problem.getSolution()
    elapsed = time.time() - start

    if soln_dts is not None:
        data_sorted = dict(sorted(soln_dts.items(), key=lambda item: item[1], reverse=False))
        return data_sorted, listClass, listTeacher

def kiem_tra_trung(*values):
    data = list(values)
    data.sort()
    L = len(data)
    for i in range(L - 1):
        x = data[i]
        kiem_tra = []
        y = x
        while True:
            y += 18
            if y > numberRoom * 18:
                break
            kiem_tra.append(y)
        if any(v in kiem_tra for v in data[i + 1:]):
            return False
    return True

def SetTKB(value, x, rows, phong):
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

    if value in T2_buoi_1:
        rows[0][0] = x + '\nPhòng: ' + phong[T2_buoi_1.tolist().index(value)]
    elif value in T2_buoi_2:
        rows[1][0] = x + '\nPhòng: ' + phong[T2_buoi_2.tolist().index(value)]
    elif value in T2_buoi_3:
        rows[2][0] = x + '\nPhòng: ' + phong[T2_buoi_3.tolist().index(value)]
    elif value in T3_buoi_1:
        rows[0][1] = x + '\nPhòng: ' + phong[T3_buoi_1.tolist().index(value)]
    elif value in T3_buoi_2:
        rows[1][1] = x + '\nPhòng: ' + phong[T3_buoi_2.tolist().index(value)]
    elif value in T3_buoi_3:
        rows[2][1] = x + '\nPhòng: ' + phong[T3_buoi_3.tolist().index(value)]
    elif value in T4_buoi_1:
        rows[0][2] = x + '\nPhòng: ' + phong[T4_buoi_1.tolist().index(value)]
    elif value in T4_buoi_2:
        rows[1][2] = x + '\nPhòng: ' + phong[T4_buoi_2.tolist().index(value)]
    elif value in T4_buoi_3:
        rows[2][2] = x + '\nPhòng: ' + phong[T4_buoi_3.tolist().index(value)]
    elif value in T5_buoi_1:
        rows[0][3] = x + '\nPhòng: ' + phong[T5_buoi_1.tolist().index(value)]
    elif value in T5_buoi_2:
        rows[1][3] = x + '\nPhòng: ' + phong[T5_buoi_2.tolist().index(value)]
    elif value in T5_buoi_3:
        rows[2][3] = x + '\nPhòng: ' + phong[T5_buoi_3.tolist().index(value)]
    elif value in T6_buoi_1:
        rows[0][4] = x + '\nPhòng: ' + phong[T6_buoi_1.tolist().index(value)]
    elif value in T6_buoi_2:
        rows[1][4] = x + '\nPhòng: ' + phong[T6_buoi_2.tolist().index(value)]
    elif value in T6_buoi_3:
        rows[2][4] = x + '\nPhòng: ' + phong[T6_buoi_3.tolist().index(value)]
    elif value in T7_buoi_1:
        rows[0][5] = x + '\nPhòng: ' + phong[T7_buoi_1.tolist().index(value)]
    elif value in T7_buoi_2:
        rows[1][5] = x + '\nPhòng: ' + phong[T7_buoi_2.tolist().index(value)]
    elif value in T7_buoi_3:
        rows[2][5] = x + '\nPhòng: ' + phong[T7_buoi_3.tolist().index(value)]

    return rows

def create_table(rows):
    df = pd.DataFrame(rows, columns=["Thứ 2", "Thứ 3", "Thứ 4", "Thứ 5", "Thứ 6", "Thứ 7"])
    df.insert(0, "", ["7h->10h30", "11h30->15h", "16h->19h30"])
    df = df.reset_index(drop=True)
    df = df.fillna("")
    st.dataframe(df, width=1000,hide_index=True,use_container_width=True) 

def display_schedule(data, selected_id, entities):
    rows = np.empty((3, 6), dtype=object)
    rows[:] = np.nan
    phong = ["A101", "A102", "A103", "B101", "B102", "B103","A104","A105","A106","B104", "B105", "B106"]

    for entity in entities:
        if entity.id == selected_id:
            for subject in entity.subjects:
                SetTKB(data[subject], subject, rows, phong)
            create_table(rows)

st.title("Sắp xếp TKB")

uploaded_file = st.file_uploader("Chọn file Excel", type="xlsx")

if "data" not in st.session_state:
    st.session_state.data = None
    st.session_state.listClass = None
    st.session_state.listTeacher = None

if st.button("Sắp xếp"):    
    if uploaded_file is not None:
        data, listClass, listTeacher = SapXep(uploaded_file)
        if all([data, listClass, listTeacher]):
            # Store in session state
            st.session_state.data = data
            st.session_state.listClass = listClass
            st.session_state.listTeacher = listTeacher
        else:
            st.error("Lỗi khi xử lý dữ liệu! Vui lòng kiểm tra file đầu vào.")
    else:
        st.error("Vui lòng chọn file")

data = st.session_state.data
listClass = st.session_state.listClass
listTeacher = st.session_state.listTeacher

if all([data, listClass, listTeacher]):
    option = st.selectbox("Chọn loại", ["Giáo Viên", "Lớp"])
    if option == "Giáo Viên":
        selected_teacher = st.selectbox("Chọn giáo viên", [teacher.id for teacher in listTeacher])
        if st.button("In TKB", key="print_teacher"):
            display_schedule(data, selected_teacher, listTeacher)
            
    else:
        selected_class = st.selectbox("Chọn lớp", [cls.id for cls in listClass])
        if st.button("In TKB", key="print_class"):
            display_schedule(data, selected_class, listClass)


