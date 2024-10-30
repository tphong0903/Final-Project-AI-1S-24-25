# Tài liệu tham khảo 
# https://github.com/andre1araujo/CSP-for-School-Timetables/blob/main/CSP_Notebook.ipynb

# Import constraint library
from constraint import *
from time import time
import pandas as pd
import numpy as np
P_6352 = ['ARIN330585_01', 'ARIN330585_02']
P_7084 = ['ARIN330585_03CLC', 'INPR140285_07', 'INPR140285_08', 'INPY131685_06', 'INPY131685_07']
P_9079 = ['ARIN330585_04CLC', 'ARIN330585_05CLC', 'ARIN330585_06CLC', 'ARIN330585_07CLC', 'DIPR430685_01', 'DIPR430685_02', 'INPY131685_10', 'INPY131685_11']
P_9831 = ['ARIN330585E_01FIE', 'ARIN330585E_02FIE', 'DIGR230485E_01FIE', 'DIGR230485E_02FIE']
P_0623 = ['ARIN330585E_03FIE', 'MALE431085E_01FIE']
P_3995 = ['BDPR431385_01', 'BDPR431385_02CLC']
P_2151 = ['DIGR230485_02CLC', 'DIGR230485_03CLC', 'DIGR230485_04CLC', 'ITAP138785_07', 'ITAP138785_08']
P_0562 = ['DIGR230485E_03FIE']
P_3984 = ['DIPR430685_01CLC', 'DLEA432085E_01FIE', 'DLEA432085E_02FIE']
P_0309 = ['DLEA432085_01', 'DLEA432085_02CLC', 'INPR130285_01', 'INPR130285E_02FIE', 'INPR140285_01', 'INPR140285_02', 'INPR140285_03', 'INPR140285_04']
P_7094 = ['INIT130185_01', 'INIT130185_02', 'INIT130185_03', 'INIT130185_04']
P_2148 = ['INIT130185E_01FIE', 'INIT130185E_02FIE']
P_9153 = ['INPR130285E_01FIE', 'INPR140285_05', 'INPR140285_06']
P_1352 = ['INPY131685_05']
P_6452 = ['INPY131685_08', 'INPY131685_09']
P_9999 = ['ITAP138785_01', 'ITAP138785_02', 'ITAP138785_03']
P_6920 = ['ITAP138785_04', 'ITAP138785_05']
P_0561 = ['ITAP138785_06']
P_9983 = ['MALE431085_01CLC', 'MALE431085_02CLC', 'MALE431085_03CLC']

dict_list = []
dict_list.append({'P_6352': P_6352})
dict_list.append({'P_7084': P_7084})
dict_list.append({'P_9079': P_9079})
dict_list.append({'P_9831': P_9831})
dict_list.append({'P_0623': P_0623})
dict_list.append({'P_3995': P_3995})
dict_list.append({'P_2151': P_2151})
dict_list.append({'P_0562': P_0562})
dict_list.append({'P_3984': P_3984})
dict_list.append({'P_0309': P_0309})
dict_list.append({'P_7094': P_7094})
dict_list.append({'P_2148': P_2148})
dict_list.append({'P_9153': P_9153})
dict_list.append({'P_1352': P_1352})
dict_list.append({'P_6452': P_6452})
dict_list.append({'P_9999': P_9999})
dict_list.append({'P_6920': P_6920})
dict_list.append({'P_0561': P_0561})
dict_list.append({'P_9983': P_9983})

C1 = [
    'ARIN330585_01', 
    'BDPR431385_01', 
    'DIPR430685_01', 
    'DLEA432085_01', 
    'MALE431085_01CLC'
]


ma_mon_hoc = [
    'ARIN330585E_01FIE', 
    'ARIN330585E_02FIE', 
    'ARIN330585E_03FIE', 
    'ARIN330585_01', 
    'ARIN330585_02', 
    'ARIN330585_03CLC', 
    'ARIN330585_04CLC', 
    'ARIN330585_05CLC', 
    'ARIN330585_06CLC', 
    'ARIN330585_07CLC', 
    'BDPR431385_01', 
    'BDPR431385_02CLC', 
    'DIGR230485E_01FIE', 
    'DIGR230485E_02FIE', 
    'DIGR230485E_03FIE', 
    'DIGR230485_02CLC', 
    'DIGR230485_03CLC', 
    'DIGR230485_04CLC', 
    'DIPR430685_01', 
    'DIPR430685_01CLC', 
    'DIPR430685_02', 
    'DLEA432085E_01FIE', 
    'DLEA432085E_02FIE', 
    'DLEA432085_01', 
    'DLEA432085_02CLC', 
    'INIT130185E_01FIE', 
    'INIT130185E_02FIE', 
    'INIT130185_01', 
    'INIT130185_02', 
    'INIT130185_03', 
    'INIT130185_04', 
    'INPR130285E_01FIE', 
    'INPR130285E_02FIE', 
    'INPR130285_01', 
    'INPR140285_01', 
    'INPR140285_02', 
    'INPR140285_03', 
    'INPR140285_04', 
    'INPR140285_05', 
    'INPR140285_06', 
    'INPR140285_07', 
    'INPR140285_08', 
    'INPY131685_05', 
    'INPY131685_06', 
    'INPY131685_07', 
    'INPY131685_08', 
    'INPY131685_09', 
    'INPY131685_10', 
    'INPY131685_11', 
    'ITAP138785_01', 
    'ITAP138785_02', 
    'ITAP138785_03', 
    'ITAP138785_04', 
    'ITAP138785_05', 
    'ITAP138785_06', 
    'ITAP138785_07', 
    'ITAP138785_08', 
    'MALE431085E_01FIE', 
    'MALE431085_01CLC', 
    'MALE431085_02CLC', 
    'MALE431085_03CLC'
]

L = len(ma_mon_hoc)
print('Số lượng môn học là: %d' % L)

sch_problem = Problem(BacktrackingSolver())

# Phòng học 1
sch_problem.addVariables(ma_mon_hoc, list(range(1, 73)))

# Nhiều phòng học không được trùng buổi với một thầy
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
            if y > 72:
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
        rows[1][0] = x + '\nPhòng: ' + phong[vi_tri]
    elif value in list(T2_buoi_2):
        vi_tri = list(T2_buoi_2).index(value)
        rows[2][0] = x + '\nPhòng: ' + phong[vi_tri]
    elif value in list(T2_buoi_3):
        vi_tri = list(T2_buoi_3).index(value)
        rows[3][0] = x + '\nPhòng: ' + phong[vi_tri]

    # T3        
    elif value in list(T3_buoi_1):
        vi_tri = list(T3_buoi_1).index(value)
        rows[1][1] = x + '\nPhòng: ' + phong[vi_tri]
    elif value in list(T3_buoi_2):
        vi_tri = list(T3_buoi_2).index(value)
        rows[2][1] = x + '\nPhòng: ' + phong[vi_tri]
    elif value in list(T3_buoi_3):
        vi_tri = list(T3_buoi_3).index(value)
        rows[3][1] = x + '\nPhòng: ' + phong[vi_tri]

    # T4        
    elif value in list(T4_buoi_1):
        vi_tri = list(T4_buoi_1).index(value)
        rows[1][2] = x + '\nPhòng: ' + phong[vi_tri]
    elif value in list(T4_buoi_2):
        vi_tri = list(T4_buoi_2).index(value)
        rows[2][2] = x + '\nPhòng: ' + phong[vi_tri]
    elif value in list(T4_buoi_3):
        vi_tri = list(T4_buoi_3).index(value)
        rows[3][2] = x + '\nPhòng: ' + phong[vi_tri]

    # T5
    elif value in list(T5_buoi_1):
        vi_tri = list(T5_buoi_1).index(value)
        rows[1][3] = x + '\nPhòng: ' + phong[vi_tri]
    elif value in list(T5_buoi_2):
        vi_tri = list(T5_buoi_2).index(value)
        rows[2][3] = x + '\nPhòng: ' + phong[vi_tri]
    elif value in list(T5_buoi_3):
        vi_tri = list(T5_buoi_3).index(value)
        rows[3][3] = x + '\nPhòng: ' + phong[vi_tri]

    # T6
    elif value in list(T6_buoi_1):
        vi_tri = list(T6_buoi_1).index(value)
        rows[1][4] = x + '\nPhòng: ' + phong[vi_tri]
    elif value in list(T6_buoi_2):
        vi_tri = list(T6_buoi_2).index(value)
        rows[2][4] = x + '\nPhòng: ' + phong[vi_tri]
    elif value in list(T6_buoi_3):
        vi_tri = list(T6_buoi_3).index(value)
        rows[3][4] = x + '\nPhòng: ' + phong[vi_tri]

    # T7
    elif value in list(T7_buoi_1):
                vi_tri = list(T7_buoi_1).index(value)
                rows[1][5] = x + '\nPhòng: ' + phong[vi_tri]
    elif value in list(T7_buoi_2):
                vi_tri = list(T7_buoi_2).index(value)
                rows[2][5] = x + '\nPhòng: ' + phong[vi_tri]
    elif value in list(T7_buoi_3):
                vi_tri = list(T7_buoi_3).index(value)
                rows[3][5] = x + '\nPhòng: ' + phong[vi_tri]   
    return rows

def TKB_GV(data,GV):
    rows = [
        ['T2', 'T3', 'T4', 'T5', 'T6', 'T7'],
        ['', '', '', '', '', ''],
        ['', '', '', '', '', ''],
        ['', '', '', '', '', '']
    ]
    phong = {0:'A3_304', 1:'A3_305', 2:'A3_306', 3:'A3_306'}
    for i in range(1, 4):
        for j in range(0, 6):
            rows[i][j] = ''
    MaGV = ''
    for gv, subjects in GV.items():
        MaGV=gv
        for x in subjects:
            value = data[x]
            # T2    
            rows = SetTKB(value,x,rows,phong)    

    df = pd.DataFrame(rows)  # Chuyển đổi danh sách thành DataFrame
    df.to_excel(f'tkb_{MaGV}.xlsx', index=False)  # Lưu vào file Excel

sch_problem.addConstraint(AllDifferentConstraint(), ma_mon_hoc)


sch_problem.addConstraint(FunctionConstraint(kiem_tra_trung), P_6352)
sch_problem.addConstraint(FunctionConstraint(kiem_tra_trung), P_7084)
sch_problem.addConstraint(FunctionConstraint(kiem_tra_trung), P_9079)
sch_problem.addConstraint(FunctionConstraint(kiem_tra_trung), P_9831)
sch_problem.addConstraint(FunctionConstraint(kiem_tra_trung), P_0623)
sch_problem.addConstraint(FunctionConstraint(kiem_tra_trung), P_3995)
sch_problem.addConstraint(FunctionConstraint(kiem_tra_trung), P_2151)
sch_problem.addConstraint(FunctionConstraint(kiem_tra_trung), P_0562)
sch_problem.addConstraint(FunctionConstraint(kiem_tra_trung), P_3984)
sch_problem.addConstraint(FunctionConstraint(kiem_tra_trung), P_0309)
sch_problem.addConstraint(FunctionConstraint(kiem_tra_trung), P_7094)
sch_problem.addConstraint(FunctionConstraint(kiem_tra_trung), P_2148)
sch_problem.addConstraint(FunctionConstraint(kiem_tra_trung), P_9153)
sch_problem.addConstraint(FunctionConstraint(kiem_tra_trung), P_1352)
sch_problem.addConstraint(FunctionConstraint(kiem_tra_trung), P_6452)
sch_problem.addConstraint(FunctionConstraint(kiem_tra_trung), P_9999)
sch_problem.addConstraint(FunctionConstraint(kiem_tra_trung), P_6920)
sch_problem.addConstraint(FunctionConstraint(kiem_tra_trung), P_0561)
sch_problem.addConstraint(FunctionConstraint(kiem_tra_trung), P_9983)

print('Running...')
start = time()
soln_dts = sch_problem.getSolution()
if soln_dts is None:
    print(soln_dts)
elapsed = time() - start
print('Mất %d giây' % elapsed)
if soln_dts is not None:
    data_sorted = dict(sorted(soln_dts.items(), key=lambda item: item[1], reverse=False))
    print(data_sorted)
    # for gv_dict in dict_list:
    #     TKB_GV(data_sorted,gv_dict)


