import streamlit as st
import streamlit.components.v1 as components

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.image as mpimg


import numpy as np
from colormapping_AI import map_coloring
from search import *


provinces_map = UndirectedGraph(dict(
    TayNinh=dict(BinhPhuoc=50, BinhDuong=30, DongNai=100, TPHCM=80),
    BinhPhuoc=dict(TayNinh=50, BinhDuong=60),
    BinhDuong=dict(TayNinh=30, BinhPhuoc=60, TPHCM=50),
    DongNai=dict(TayNinh=100, TPHCM=60, BinhDuong=70),
    BRVT=dict(TPHCM=70, DongNai=120),
    TPHCM=dict(TayNinh=80, BinhDuong=50, DongNai=60, BRVT=70, LongAn=40, TienGiang=60),
    LongAn=dict(TPHCM=40, TienGiang=50),
    TienGiang=dict(TPHCM=60, LongAn=50, BenTre=30),
    BenTre=dict(TienGiang=30, TraVinh=40),
    TraVinh=dict(BenTre=40, VinhLong=50),
    VinhLong=dict(TraVinh=50, DongThap=60),
    DongThap=dict(VinhLong=60, AnGiang=70),
    AnGiang=dict(DongThap=70, CanTho=80),
    CanTho=dict(AnGiang=80, SocTrang=50),
    SocTrang=dict(CanTho=50, HauGiang=30),
    HauGiang=dict(SocTrang=30, KienGiang=40),
    KienGiang=dict(HauGiang=40, CaMau=90),
    CaMau=dict(KienGiang=90, BacLieu=60),
    BacLieu=dict(CaMau=60)
))

# Define the locations of the provinces
provinces_map.locations = dict(
    TayNinh=(430, 580),
    BinhPhuoc=(550, 650),
    BinhDuong=(550, 550),
    DongNai=(650, 530),
    BRVT=(650, 440),
    TPHCM=(530, 500),
    LongAn=(450, 460),
    TienGiang=(450, 420),
    BenTre=(520, 350),
    TraVinh=(500, 300),
    VinhLong=(420, 360),
    DongThap=(370, 420),
    AnGiang=(300, 420),
    CanTho=(350, 370),
    SocTrang=(450, 280),
    HauGiang=(380, 320),
    KienGiang=(280, 300),
    CaMau=(250, 200),
    BacLieu=(350, 230)
)

map_locations = provinces_map.locations
graph_dict = provinces_map.graph_dict



xmin = 91
xmax = 562
ymin = 270
ymax = 570

import matplotlib.pyplot as plt
import matplotlib.image as mpimg

def ve_ban_do():
    map_coloring()
    img = mpimg.imread('colored_map.png')

    # Create the figure and axis
    fig, ax = plt.subplots()
    ax.set_title('')  
    ax.axis('off')

    ax.set_xticks([])  
    ax.set_yticks([])  


    ax.imshow(img, extent=[xmin-150, xmax+150, ymin-150, ymax+150], aspect='auto')
    
    ax.axis([xmin-150, xmax+150, ymin-150, ymax+150])  
# Increase extent to zoom in
    # Plot the cities and paths over the image
    for key in graph_dict:
        city = graph_dict[key]
        x0 = map_locations[key][0]
        y0 = map_locations[key][1]

        # Plot the cities
        diem, = ax.plot(x0, y0, 's', color='#00008B')

        # Add city labels
        

        # Plot the paths between cities
        for neighbor in city:
            x1 = map_locations[neighbor][0]
            y1 = map_locations[neighbor][1]
            ax.plot([x0, x1], [y0, y1], 'b')  # Blue lines for the paths

    return fig



def ve_mui_ten(b, a, tx, ty):
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
        q_mui_ten.append([q[0,0], q[1,0]])
    return q_mui_ten 



if "flag_anim" not in st.session_state:
    st.session_state["flag_anim"] = False
if st.session_state["flag_anim"] == False:
    if "flag_ve_ban_do" not in st.session_state:
        st.session_state["flag_ve_ban_do"] = True
        fig = ve_ban_do()
        st.session_state['fig'] = fig
        st.pyplot(fig)
        print(st.session_state["flag_ve_ban_do"])
        print('Vẽ bản đồ lần đầu')
    else:
        if st.session_state["flag_ve_ban_do"] == False:
            st.session_state["flag_ve_ban_do"] = True
            fig = ve_ban_do()
            st.session_state['fig'] = fig
            st.pyplot(fig)
        else:
            print('Đã vẽ bản đồ')
            st.pyplot(st.session_state['fig'])
    
    lst_provinces = [province for province in provinces_map.locations]

    start_city = st.selectbox('Bạn chọn thành phố bắt đầu:', lst_provinces)
    dest_city = st.selectbox('Bạn chọn thành phố đích:', lst_provinces)

   
    st.session_state['start_city'] = start_city
    st.session_state['dest_city']  = dest_city


    if st.button('Direction'):
        if start_city is dest_city:
            st.write('Thành phố bắt đầu và thành phố đích không được trùng nhau')
            st.stop()
        romania_problem = GraphProblem(start_city, dest_city, provinces_map)
        c = astar_search(romania_problem)
        lst_path = c.path()
        print('Con duong tim thay: ')

        for data in lst_path:
            city = data.state 
            print(city, end = ' ')
        print()
        path_locations = {}
        for data in lst_path:
            city = data.state
            path_locations[city] = map_locations[city]
        print(path_locations)

        lst_path_location_x = []
        lst_path_location_y = []

        for city in path_locations:
            lst_path_location_x.append(path_locations[city][0])
            lst_path_location_y.append(path_locations[city][1])

        print(lst_path_location_x)
        print(lst_path_location_y)

        map_coloring()
        img = mpimg.imread('colored_map.png')

        fig, ax = plt.subplots()
        ax.set_title('')
        ax.axis('off')
  
        ax.set_xticks([])  
        ax.set_yticks([])  
        ax.imshow(img, extent=[xmin-150, xmax+150, ymin-150, ymax+150], aspect='auto')
    
        ax.axis([xmin-150, xmax+150, ymin-150, ymax+150])  


        for key in graph_dict:
            city = graph_dict[key]
            x0 = map_locations[key][0]
            y0 = map_locations[key][1]

            diem, = ax.plot(x0, y0, 's', color='#00008B')

           

            for neighbor in city:
                x1 = map_locations[neighbor][0]
                y1 = map_locations[neighbor][1]
                doan_thang, = ax.plot([x0, x1], [y0, y1], 'b')

            path_tim_thay, = ax.plot(lst_path_location_x, lst_path_location_y, '#FFA500')
        print('Đã gán fig có hướng dẫn')
        st.session_state['fig'] = fig
        st.rerun()

    if st.button('Run'):
        start_city = st.session_state['start_city']
        dest_city = st.session_state['dest_city']

        romania_problem = GraphProblem(start_city, dest_city, provinces_map)
        c = astar_search(romania_problem)
        lst_path = c.path()
        print('Con duong tim thay: ')

        for data in lst_path:
            city = data.state 
            print(city, end = ' ')
        print()
        path_locations = {}
        for data in lst_path:
            city = data.state
            path_locations[city] = map_locations[city]
        print(path_locations)

        lst_path_location_x = []
        lst_path_location_y = []

        for city in path_locations:
            lst_path_location_x.append(path_locations[city][0])
            lst_path_location_y.append(path_locations[city][1])

        print(lst_path_location_x)
        print(lst_path_location_y)


        fig, ax = plt.subplots()

        dem = 0

        lst_doan_thang = []
        for key in graph_dict:
            city = graph_dict[key]
            x0 = map_locations[key][0]
            y0 = map_locations[key][1]

            diem, = ax.plot(x0, y0, 's', color='#00008B')
            lst_doan_thang.append(diem)

            

            for neighbor in city:
                x1 = map_locations[neighbor][0]
                y1 = map_locations[neighbor][1]
                doan_thang, = ax.plot([x0, x1], [y0, y1], 'b')
                lst_doan_thang.append(doan_thang)
                dem = dem + 1

            path_tim_thay, = ax.plot(lst_path_location_x, lst_path_location_y, '#FFA500')
            lst_doan_thang.append(path_tim_thay)

        print('Dem: ', dem)

        N = 11
        d = 100

        lst_vi_tri = []

        L = len(lst_path_location_x)
        for i in range(0,L-1):
            x1 = lst_path_location_x[i]
            y1 = lst_path_location_y[i]
            x2 = lst_path_location_x[i+1]
            y2 = lst_path_location_y[i+1]

            b = y2-y1
            a = x2-x1


            d0 = np.sqrt((x2-x1)**2 + (y2-y1)**2)
            N0 = int(N*d0/d)
            dt = 1/(N0-1)
            for j in range(0, N0):
                t = j*dt
                x = x1 + (x2-x1)*t
                y = y1 + (y2-y1)*t

                q = ve_mui_ten(b,a,x,y)
                lst_vi_tri.append(q)



        blue_polygon, = ax.fill([],[], color = 'blue')

        FRAME = len(lst_vi_tri)

        def init():
            map_coloring()
            img = mpimg.imread('colored_map.png')
            ax.imshow(img, extent=[xmin-150, xmax+150, ymin-150, ymax+150], aspect='auto')
            ax.set_title('')
            ax.axis('off')
            ax.set_xticks([])  
            ax.set_yticks([])  
            ax.axis([xmin-150, xmax+150, ymin-150, ymax+150])  

            # Trả về nhiều đoạn thẳng và đoạn thẳng tìm được
            return lst_doan_thang, blue_polygon

        def animate(i):
            blue_polygon.set_xy(lst_vi_tri[i])
            return lst_doan_thang, blue_polygon 

        anim = FuncAnimation(fig, animate, frames=FRAME, interval=200, init_func=init, repeat=False)

        st.session_state["flag_anim"] = True
        st.session_state['anim'] = anim
        st.rerun()

else:
    if st.session_state["flag_anim"] == True:
        components.html(st.session_state["anim"].to_jshtml(), height = 550)
        _, _, col3, _, _ = st.columns(5)
        if col3.button('Reset'):
            st.session_state["flag_anim"] = False
            st.session_state["flag_ve_ban_do"] = False
            st.rerun()

