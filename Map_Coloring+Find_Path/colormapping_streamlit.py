import cv2
import numpy as np
from simpleai.search import CspProblem, backtrack
import streamlit as st
from PIL import Image
import time

def constraint_func(names, values):
    return values[0] != values[1]

def map_coloring():
    global steps, current_step
    names = ('TayNinh', 'BinhPhuoc', 'BinhDuong', 'DongNai', 'BRVT',
             'TPHCM', 'LongAn', 'TienGiang', 'BenTre', 'TraVinh', 
             'VinhLong', 'DongThap', 'AnGiang', 'CanTho', 'SocTrang', 
             'HauGiang', 'KienGiang', 'CaMau', 'BacLieu')
    names_point = [
        (391, 105), (500, 64), (459, 146), (534, 157), (545, 233),
        (470, 210), (397, 220), (401, 256), (440, 289), (419, 335),
        (375, 300), (308, 226), (269, 239), (307, 294), (367, 371),
        (336, 338), (266, 335), (252, 437), (309, 408)
    ]
    color_available = ['gray', 'green', 'yellow', 'purple', 'cyan', 'magenta', 'orange',
                       'brown', 'pink', 'lime', 'olive', 'maroon', 'navy', 'teal',
                       'gold', 'coral', 'salmon', 'violet', 'indigo']
    colors = dict((name, color_available.copy()) for name in names)
    neighbors = {
        'TayNinh': ['BinhPhuoc', 'BinhDuong', 'TPHCM', 'LongAn'],
        'BinhPhuoc': ['TayNinh', 'BinhDuong', 'DongNai'],
        'BinhDuong': ['TayNinh', 'BinhPhuoc', 'DongNai', 'TPHCM'],
        'DongNai': ['BinhPhuoc', 'BinhDuong', 'BRVT', 'TPHCM'],
        'BRVT': ['DongNai', 'TPHCM'],
        'TPHCM': ['TayNinh', 'BinhDuong', 'DongNai', 'BRVT', 'LongAn'],
        'LongAn': ['TPHCM', 'TienGiang'],
        'TienGiang': ['LongAn', 'BenTre', 'VinhLong'],
        'BenTre': ['TienGiang', 'TraVinh'],
        'TraVinh': ['BenTre', 'VinhLong', 'SocTrang'],
        'VinhLong': ['TienGiang', 'TraVinh', 'DongThap', 'CanTho'],
        'DongThap': ['VinhLong', 'AnGiang', 'CanTho'],
        'AnGiang': ['DongThap', 'KienGiang', 'CanTho'],
        'CanTho': ['AnGiang', 'DongThap', 'VinhLong', 'HauGiang'],
        'HauGiang': ['CanTho', 'SocTrang', 'BacLieu'],
        'SocTrang': ['TraVinh', 'HauGiang', 'BacLieu'],
        'BacLieu': ['SocTrang', 'HauGiang', 'CaMau'],
        'CaMau': ['BacLieu', 'KienGiang'],
        'KienGiang': ['AnGiang', 'CaMau']
    }
    constraints = []
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            constraints.append(((names[i], names[j]), constraint_func))
    problem = CspProblem(names, colors, constraints)
    result = backtrack(problem)
    if not result:
        st.error("Không tìm được giải pháp.")
        return
    image = cv2.imread('Map_Coloring+Find_Path\\input.png', cv2.IMREAD_GRAYSCALE)
    image_color = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    color_map = {
        'gray': (104, 104, 104), 'green': (0, 255, 0), 'yellow': (0, 255, 255),
        'purple': (128, 0, 128), 'cyan': (255, 255, 0), 'magenta': (255, 0, 255),
        'orange': (0, 165, 255), 'brown': (19, 69, 139), 'pink': (203, 192, 255),
        'lime': (0, 255, 128), 'olive': (0, 128, 128), 'maroon': (0, 0, 128),
        'navy': (128, 0, 0), 'teal': (128, 128, 0), 'gold': (0, 215, 255),
        'coral': (80, 127, 255), 'salmon': (114, 128, 250), 'violet': (238, 130, 238),
        'indigo': (75, 0, 130)
    }
    mask = np.zeros((image.shape[0] + 2, image.shape[1] + 2), np.uint8)
    steps = []
    for province, color_name in result.items():
        point = names_point[names.index(province)]
        color = color_map[color_name]
        cv2.floodFill(image_color, mask, point, color)
        cv2.putText(image_color, province, (point[0] - 15, point[1] - 8), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 0, 0), 1)
        steps.append(image_color.copy())
    return steps

def update_image(image, placeholder):
    image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    placeholder.image(image, use_column_width=True)


def main():
    st.title("Map Coloring")

    if 'steps' not in st.session_state:
        st.session_state.steps = []
    if 'current_step' not in st.session_state:
        st.session_state.current_step = 0
    if 'started' not in st.session_state:
        st.session_state.started = False

    image_placeholder = st.empty()

    if not st.session_state.steps and not st.session_state.started:
        image = cv2.imread('Map_Coloring+Find_Path\\input.png', cv2.IMREAD_GRAYSCALE)
        image_color = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        update_image(image_color, image_placeholder)

    if not st.session_state.started and st.button("Start"):
        st.session_state.steps = map_coloring()
        st.session_state.current_step = 0
        st.session_state.started = True
        if st.session_state.steps:
            update_image(st.session_state.steps[st.session_state.current_step], image_placeholder)

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.session_state.steps and st.button("Back"):
            if st.session_state.current_step > 0:
                st.session_state.current_step -= 1
                update_image(st.session_state.steps[st.session_state.current_step], image_placeholder)
    with col2:
        if st.session_state.steps and st.button("Next"):
            if st.session_state.current_step < len(st.session_state.steps) - 1:
                st.session_state.current_step += 1
                update_image(st.session_state.steps[st.session_state.current_step], image_placeholder)
    with col3:
        if st.session_state.steps and st.button("Auto"):
            for step in range(st.session_state.current_step, len(st.session_state.steps)):
                update_image(st.session_state.steps[step], image_placeholder)
                st.session_state.current_step = step
                time.sleep(0.5)

    if st.session_state.started and st.button("Reset"):
        st.session_state.steps = []
        st.session_state.current_step = 0
        st.session_state.started = False
        image = cv2.imread('Map_Coloring+Find_Path\\input.png', cv2.IMREAD_GRAYSCALE)
        image_color = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        update_image(image_color, image_placeholder)


if __name__ == "__main__":
    main()
