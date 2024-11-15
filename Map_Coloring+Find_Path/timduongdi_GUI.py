import cv2
from search import *
import tkinter as tk
import tkinter.ttk as ttk
from PIL import Image, ImageTk
import time
import numpy as np

provinces_map = UndirectedGraph(dict(
    TayNinh=dict(BinhPhuoc=50, BinhDuong=30, LongAn=100, TPHCM=80),
    BinhPhuoc=dict(TayNinh=50, BinhDuong=60,DongNai=50),
    BinhDuong=dict(TayNinh=30, BinhPhuoc=60, TPHCM=50,DongNai=50),
    DongNai=dict(BinhPhuoc=50, TPHCM=60, BinhDuong=70,BRVT=30),
    BRVT=dict(TPHCM=70, DongNai=120),
    TPHCM=dict(TayNinh=80, BinhDuong=50, DongNai=60, BRVT=70, LongAn=40, TienGiang=60),
    LongAn=dict(TPHCM=40, TienGiang=50,TayNinh=100,DongThap=30),
    TienGiang=dict(TPHCM=60, LongAn=50, BenTre=30,DongThap=40,VinhLong=40),
    BenTre=dict(TienGiang=30, TraVinh=40,VinhLong=40),
    TraVinh=dict(BenTre=40, VinhLong=50,SocTrang=40),
    VinhLong=dict(TraVinh=50, DongThap=60,BenTre=40,TienGiang=40,SocTrang=40,CanTho=40,HauGiang=40),
    DongThap=dict(VinhLong=60, AnGiang=70,TienGiang=40,LongAn=30,CanTho=40),
    AnGiang=dict(DongThap=70, CanTho=80,KienGiang=60),
    CanTho=dict(AnGiang=80,DongThap=40,VinhLong=40,HauGiang=50,KienGiang=50),
    SocTrang=dict( HauGiang=30,TraVinh=40,VinhLong=40,SocTrang=40),
    HauGiang=dict(SocTrang=30, KienGiang=40,CanTho=50,VinhLong=40,BacLieu=40),
    KienGiang=dict(HauGiang=40, CaMau=90,AnGiang=60,CanTho=50,BacLieu=60),
    CaMau=dict(KienGiang=90, BacLieu=60),
    BacLieu=dict(CaMau=60, KienGiang=60, SocTrang=40,HauGiang=40)
))

provinces_map.locations = dict(
    TayNinh=(554, 500), BinhPhuoc=(700, 550), BinhDuong=(657, 430), DongNai=(760, 430),
    BRVT=(765, 330), TPHCM=(650, 360), LongAn=(554, 350), TienGiang=(554, 300),
    BenTre=(630, 250), TraVinh=(600, 180), VinhLong=(520, 240), DongThap=(450, 330),
    AnGiang=(380, 320), CanTho=(430, 250), SocTrang=(550, 150), HauGiang=(450, 180),
    KienGiang=(380, 200), CaMau=(365, 50), BacLieu=(440, 100)
)



graph_dict = provinces_map.graph_dict
romania_locations = provinces_map.locations


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.start = 'TayNinh'
        self.dest = 'DongNai'
        self.path_location = None

        self.title('Search')
        self.cvs_map = tk.Canvas(self, width=840, height=680, relief=tk.SUNKEN, border=1)

        self.add_image_to_bottom()
        self.ve_ban_do()
        lbl_frm_menu = tk.LabelFrame(self)
        lst_provinces = [province for province in provinces_map.locations]

        lbl_start = ttk.Label(lbl_frm_menu, text='Start')

        self.cbo_start = ttk.Combobox(lbl_frm_menu, values=lst_provinces)
        self.cbo_start.set('TayNinh')
        self.cbo_start.bind("<<ComboboxSelected>>", self.cbo_start_click)

        lbl_start.grid(row=0, column=0, padx=5, pady=0, sticky=tk.W)

        self.cbo_start.grid(row=1, column=0, padx=5, pady=5)

        lbl_dest = ttk.Label(lbl_frm_menu, text='Dest')

        self.cbo_dest = ttk.Combobox(lbl_frm_menu, values=lst_provinces)
        self.cbo_dest.set('DongNai')
        self.cbo_dest.bind("<<ComboboxSelected>>", self.cbo_dest_click)

        btn_direction = ttk.Button(lbl_frm_menu, text='Direction',
                                   command=self.btn_direction_click)
        btn_run = ttk.Button(lbl_frm_menu, text='Run',
                             command=self.btn_run_click)

        lbl_dest.grid(row=2, column=0, padx=5, pady=0, sticky=tk.W)

        self.cbo_dest.grid(row=3, column=0, padx=5, pady=5)

        btn_direction.grid(row=4, column=0, padx=5, pady=5)
        btn_run.grid(row=5, column=0, padx=5, pady=5)

        self.cvs_map.grid(row=0, column=0, padx=5, pady=5)
        lbl_frm_menu.grid(row=0, column=1, padx=5, pady=7, sticky=tk.N)

    def ve_ban_do(self):
        for city in graph_dict:
            x0 = romania_locations[city][0]
            y0 = 640 - romania_locations[city][1]
            self.cvs_map.create_rectangle(x0 - 4, y0 - 4, x0 + 4, y0 + 4,
                                          fill='blue', outline='blue')

         
            for neighbor in graph_dict[city]:
                x1 = romania_locations[neighbor][0]
                y1 = 640 - romania_locations[neighbor][1]
                self.cvs_map.create_line(x0, y0, x1, y1, width=2)

    def cbo_start_click(self, *args):
        self.start = self.cbo_start.get()

    def cbo_dest_click(self, *args):
        self.dest = self.cbo_dest.get()

    def btn_direction_click(self):
        self.cvs_map.delete(tk.ALL)
        self.add_image_to_bottom()  
        self.ve_ban_do()

        romania_problem = GraphProblem(self.start, self.dest, provinces_map)
        c = astar_search(romania_problem)
        lst_path = c.path()
        self.path_location = []
        for data in lst_path:
            city = data.state
            x = provinces_map.locations[city][0]
            y = 640 - provinces_map.locations[city][1]
            self.path_location.append((x, y))

        self.cvs_map.create_line(self.path_location, fill='red',width=2)

    def btn_run_click(self):
        bg_color = self.cvs_map['background']
        N = 21
        d = 100
        L = len(self.path_location)
        for i in range(0, L - 1):
            x0 = self.path_location[i][0]
            y0 = self.path_location[i][1]
            x1 = self.path_location[i + 1][0]
            y1 = self.path_location[i + 1][1]
            b = y1 - y0
            a = x1 - x0

            d1 = np.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2)
            N1 = int(N * d1 / d)
            dt = 1.0 / (N1 - 1)
            for j in range(0, N1):
                t = j * dt
                x = x0 + (x1 - x0) * t
                y = y0 + (y1 - y0) * t

                self.cvs_map.delete(tk.ALL)

                self.add_image_to_bottom()  # Ensure the image stays as the background
                self.ve_ban_do()
                self.cvs_map.create_line(self.path_location, fill='red',width=2)

                self.ve_mui_ten(b, a, x, y, '#00008B')

                self.update()
                time.sleep(0.01)
    def ve_mui_ten(self, b, a, tx, ty, color):
        p_mui_ten = [(0,0,1), (-20,10,1), (-15,0,1), (-20,-10,1)]
        p_mui_ten_ma_tran = [np.array([[0],[0],[1]],np.float32),
                             np.array([[-20],[10],[1]],np.float32),
                             np.array([[-15],[0],[1]],np.float32),
                             np.array([[-20],[-10],[1]],np.float32)]

        # Tạo ma trận dời (tịnh tiến) - translate
        M1 = np.array([[1, 0, tx], 
                       [0, 1, ty], 
                       [0, 0, 1]], np.float32)

        # Tạo ma trận quay - rotation
        theta = np.arctan2(b, a)
        M2 = np.array([[np.cos(theta), -np.sin(theta), 0],
                       [np.sin(theta),  np.cos(theta), 0],
                       [     0,             0,        1]], np.float32)

        M = np.matmul(M1, M2)

        q_mui_ten = []
        for p in p_mui_ten_ma_tran:
            q = np.matmul(M, p)
            q_mui_ten.append((q[0,0], q[1,0]))

        self.cvs_map.create_polygon(q_mui_ten, fill = color, outline = color,width=5)
    def add_image_to_bottom(self):
        image = Image.open('colored_map.png')
        image = image.resize((840, 680)) 
        photo = ImageTk.PhotoImage(image)
        self.bg_image = self.cvs_map.create_image(0, 0, image=photo, anchor=tk.NW)
        self.cvs_map.image = photo  


if __name__ == '__main__':
    app = App()
    app.mainloop()
