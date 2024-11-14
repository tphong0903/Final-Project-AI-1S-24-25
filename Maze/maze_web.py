import streamlit as st
import numpy as np
from PIL import Image
from PIL import Image, ImageDraw
from streamlit_drawable_canvas import st_canvas
import pandas as pd
import math
from simpleai.search import SearchProblem, astar, breadth_first, depth_first
import time

# Define cost of moving around the  MAP
cost_regular = 1.0
cost_diagonal = 1.7

# Create the cost dictionary
COSTS = {
    "up": cost_regular,
    "down": cost_regular,
    "left": cost_regular,
    "right": cost_regular,
}

# Define the  MAP
MAP = """
##################################
#         #              #       #
# ####    ########       #   #####
#    #    #              #       #
#    ###     #####  ######   #####
#      #   ###   #               #
#      #     #   #  #  #   ##    #
#     #####    #    #  #         #
#     #        #       #     #   #
# #######     ######  ########   #
#     #       #          #       #
#    ###      ###   ######  ######
#    #   #    #      #           #
# ########   #######    #####    #
#             #          #       #
##################################
"""

# Convert  MAP to a list
MAP = [list(x) for x in MAP.split("\n") if x]
MAP2 = MAP
M = len(MAP)
N = len(MAP[0])
W = 21
mau_xanh = np.zeros((W - 5, W - 5, 3), np.uint8) + (np.uint8(255), np.uint8(0), np.uint8(0))
mau_trang = np.zeros((W, W, 3), np.uint8) + (np.uint8(255), np.uint8(255), np.uint8(255))
mau_do = np.zeros((W, W, 3), np.uint8) + (np.uint8(0), np.uint8(0), np.uint8(255))


class MazeSolver(SearchProblem):
    def __init__(self, board):
        self.board = board
        self.goal = (0, 0)
        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                if self.board[y][x].lower() == "o":
                    self.initial = (x, y)
                elif self.board[y][x].lower() == "x":
                    self.goal = (x, y)

        super(MazeSolver, self).__init__(initial_state=self.initial)

    def actions(self, state):
        actions = []
        for action in COSTS.keys():
            newx, newy = self.result(state, action)
            if self.board[newy][newx] != "#":
                actions.append(action)
        return actions

    def result(self, state, action):
        x, y = state
        if action.count("up"):
            y -= 1
        if action.count("down"):
            y += 1
        if action.count("left"):
            x -= 1
        if action.count("right"):
            x += 1
        new_state = (x, y)
        return new_state

    def is_goal(self, state):
        return state == self.goal

    def cost(self, state, action, state2):
        return COSTS[action]

    def heuristic(self, state):
        x, y = state
        gx, gy = self.goal
        return math.sqrt((x - gx) ** 2 + (y - gy) ** 2)


st.title("Maze Solver")
if "current_step" not in st.session_state:
    st.session_state["current_step"] = 0
if "dem" not in st.session_state:
    st.session_state["dem"] = 0
if "listImage" not in st.session_state:
    st.session_state["listImage"] = []
if "is_auto_running" not in st.session_state:
    st.session_state["is_auto_running"] = False
if "bg_image" not in st.session_state:
    bg_image = Image.open("Maze/maze.bmp")
    st.session_state["bg_image"] = bg_image
if "points" not in st.session_state:
    st.session_state["points"] = []

canvas_placeholder = st.empty()
with canvas_placeholder.container():
    canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)",
        stroke_width=7,
        stroke_color="red",
        background_image=st.session_state["bg_image"],
        update_streamlit=True,
        height=336,
        width=710,
        point_display_radius=0,
        drawing_mode="point"
    )
valid_points = []
choice = "A*"


def display_path():
    st.session_state["is_auto_running"] = True
    listImage = st.session_state["listImage"]
    for image in listImage:
        canvas_placeholder.empty()
        canvas_placeholder.image(image, width=710, channels="RGB")
        time.sleep(0.5)
    st.session_state["is_auto_running"] = False


def draw_image(path):
    listImage = []
    for x1, y2 in path:
        MAP[y2][x1] = 'o'
        image = np.ones((M * W, N * W, 3), np.uint8) * 255
        for x in range(M):
            for y in range(N):
                if MAP[x][y] == '#':
                    image[x * W:(x + 1) * W, y * W:(y + 1) * W] = mau_do
                elif MAP[x][y] == ' ':
                    image[x * W:(x + 1) * W, y * W:(y + 1) * W] = mau_trang
                else:
                    image[x * W + 2:(x + 1) * W - 3, y * W + 2:(y + 1) * W - 3] = mau_xanh
        listImage.append(image)
    return listImage


def btn_next_step_click():
    listImage = st.session_state.get("listImage")
    if st.session_state["current_step"] < len(listImage) - 2:
        st.session_state["current_step"] += 1
        canvas_placeholder.empty()
        canvas_placeholder.image(listImage[st.session_state["current_step"]], width=710, channels="RGB")
    st.write(f"Current Step: {st.session_state['current_step']}, Total Steps: {len(listImage) - 2}")


def btn_prev_step_click():
    listImage = st.session_state.get("listImage")
    if st.session_state["current_step"] > 0:
        st.session_state["current_step"] -= 1
        canvas_placeholder.image(listImage[st.session_state["current_step"]], width=710, channels="RGB")
    st.write(f"Current Step: {st.session_state['current_step']}, Total Steps: {len(listImage) - 2}")


if canvas_result.json_data is not None:
    list_point = canvas_result.json_data["objects"]
    if len(list_point) > 0:
        px = list_point[-1]['left']
        py = list_point[-1]['top']
        x1 = int(px // 21)
        y1 = int(py // 21)
        if MAP[y1][x1] != '#':
            MAP[y1][x1] = 'o'
            if st.session_state["dem"] < 2:
                st.session_state["dem"] += 1
            st.session_state["points"].append((x1, y1))
            image = np.ones((M * W, N * W, 3), np.uint8) * 255
            for x in range(M):
                for y in range(N):
                    if MAP[x][y] == '#':
                        image[x * W:(x + 1) * W, y * W:(y + 1) * W] = mau_do
                    elif MAP[x][y] == ' ':
                        image[x * W:(x + 1) * W, y * W:(y + 1) * W] = mau_trang
            for point in st.session_state["points"]:
                px, py = point
                image[py * W + 2:(py + 1) * W - 3, px * W + 2:(px + 1) * W - 3] = mau_xanh
            st.session_state["bg_image"] = Image.fromarray(image)
            st.rerun()


def handle_run():
    if len(st.session_state["points"]) >= 2:
        x1 = st.session_state["points"][0][0]
        y1 = st.session_state["points"][0][1]

        x2 = st.session_state["points"][1][0]
        y2 = st.session_state["points"][1][1]

        MAP[y1][x1] = 'o'
        MAP[y2][x2] = 'x'
        problem = MazeSolver(MAP)
        if choice == 'A*':
            result = astar(problem, graph_search=True)
        elif choice == 'BFS':
            result = breadth_first(problem, graph_search=True)
        else:
            result = depth_first(problem, graph_search=True)

        if result:
            path = [x[1] for x in result.path()]
            if path:
                st.session_state["listImage"] = draw_image(path)


col1, col2, col3 = st.columns([1, 1, 1])
if st.button("Reset"):
    st.session_state["listImage"] = []
    st.session_state["current_step"] = 0
    st.session_state["bg_image"] = Image.open("Maze/maze.bmp")
    valid_points = []
    MAP = MAP2
    st.session_state["points"] = []
    st.session_state["result2_ready"] = False
    st.session_state["is_auto_running"] = False

choice = st.selectbox("Chọn thuật toán:", options=['A*', 'BFS', 'DFS'])
if st.button("Run"):
    st.session_state["result2_ready"] = True
    handle_run()

if st.session_state.get("result2_ready", False):
    prev_disabled = st.session_state["current_step"] <= 0 or st.session_state["is_auto_running"]
    next_disabled = st.session_state["current_step"] >= len(st.session_state.get("listImage", [])) - 3 or \
                    st.session_state["is_auto_running"]

    with col1:
        if st.button("Prev", disabled=prev_disabled):
            btn_prev_step_click()
    with col2:
        if st.session_state["is_auto_running"]:
            if st.button("Stop Auto"):
                st.session_state["is_auto_running"] = False
        else:
            if st.button("Auto"):
                display_path()
    with col3:
        if st.button("Next", disabled=next_disabled):
            btn_next_step_click()
