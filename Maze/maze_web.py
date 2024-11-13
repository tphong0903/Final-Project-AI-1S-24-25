import streamlit as st
import numpy as np
from PIL import Image
from streamlit_drawable_canvas import st_canvas
import pandas as pd
import math
from simpleai.search import SearchProblem, astar, breadth_first, depth_first
import time

# Define cost of moving around the map
cost_regular = 1.0
cost_diagonal = 1.7

# Create the cost dictionary
COSTS = {
    "up": cost_regular,
    "down": cost_regular,
    "left": cost_regular,
    "right": cost_regular,
    "up left": cost_diagonal,
    "up right": cost_diagonal,
    "down left": cost_diagonal,
    "down right": cost_diagonal,
}

# Define the map
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

# Convert map to a list
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
if "listImage" not in st.session_state:
    st.session_state["listImage"] = []
if "is_auto_running" not in st.session_state:
    st.session_state["is_auto_running"] = False


class MazeApp:
    def __init__(self):

        if "objects" not in st.session_state:
            st.session_state["objects"] = []
        self.bg_image = Image.open("Maze/maze.bmp")
        self.canvas_placeholder = st.empty()
        self.valid_points = []
        self.listImage = []
        self.map = [row[:] for row in MAP]
        self.canvas_result = None
        self.problem = None
        self.result = None

    def handle_run(self, choice):
        list_point = self.canvas_result.json_data["objects"]
        for point in list_point:
            px = point['left'] + 3
            py = point['top'] + 3
            x = int(px / 21)
            y = int(py / 21)

            if MAP[y][x] != '#':
                self.valid_points.append(point)
                st.session_state["objects"].append(point)
        if len(self.valid_points) > 1:

            start_point = self.valid_points[0]
            goal_point = self.valid_points[1]

            x1 = int((start_point['left'] + 3) / 21)
            y1 = int((start_point['top'] + 3) / 21)
            x2 = int((goal_point['left'] + 3) / 21)
            y2 = int((goal_point['top'] + 3) / 21)

            self.map[y1][x1] = 'o'
            self.map[y2][x2] = 'x'

            self.problem = MazeSolver(self.map)
            if choice == 'A*':
                self.result = astar(self.problem, graph_search=True)
            elif choice == 'BFS':
                self.result = breadth_first(self.problem, graph_search=True)
            else:
                self.result = depth_first(self.problem, graph_search=True)

            st.session_state["objects"] = []
            if self.result:
                path = [x[1] for x in self.result.path()]
                if path:
                    self.draw_image(path)
                    st.session_state["listImage"] = self.listImage
        else:
            st.error("Điểm không hợp lệ sẽ bị xóa sau 2s, vui lòng chọn điểm khác")
            time.sleep(2)
            self.update_canvas()

    def display_path(self):
        st.session_state["is_auto_running"] = True
        self.listImage = st.session_state.get("listImage", [])
        for image in self.listImage:
            self.canvas_placeholder.image(image, width=710, channels="RGB")
            time.sleep(0.5)
        st.session_state["is_auto_running"] = False

    def draw_image(self, path):
        for x1, y2 in path:
            self.map[y2][x1] = 'o'
            image = np.ones((M * W, N * W, 3), np.uint8) * 255
            for x in range(M):
                for y in range(N):
                    if self.map[x][y] == '#':
                        image[x * W:(x + 1) * W, y * W:(y + 1) * W] = mau_do
                    elif self.map[x][y] == ' ':
                        image[x * W:(x + 1) * W, y * W:(y + 1) * W] = mau_trang
                    else:
                        image[x * W + 2:(x + 1) * W - 3, y * W + 2:(y + 1) * W - 3] = mau_xanh
            self.listImage.append(image)

    def update_canvas(self):
        self.canvas_result = st_canvas(
            fill_color="rgba(255, 165, 0, 0.3)",
            stroke_width=7,
            stroke_color="red",
            background_image=self.bg_image,
            update_streamlit=True,
            height=336,
            width=710,
            drawing_mode="point",
            initial_drawing={"objects": st.session_state["objects"]}
        )

    def btn_next_step_click(self):
        self.listImage = st.session_state.get("listImage")
        if st.session_state["current_step"] < len(self.listImage) - 2:
            st.session_state["current_step"] += 1
            self.canvas_placeholder.empty()
            self.canvas_placeholder.image(self.listImage[st.session_state["current_step"]], width=710, channels="RGB")
        st.write(f"Current Step: {st.session_state['current_step']}, Total Steps: {len(self.listImage) - 2}")

    def btn_prev_step_click(self):
        self.listImage = st.session_state.get("listImage")
        if st.session_state["current_step"] > 0:
            st.session_state["current_step"] -= 1
            print(st.session_state["current_step"])
            self.canvas_placeholder.image(self.listImage[st.session_state["current_step"]], width=710, channels="RGB")
        st.write(f"Current Step: {st.session_state['current_step']}, Total Steps: {len(self.listImage) - 2}")

    def run(self):
        with self.canvas_placeholder.container():
            self.update_canvas()
        col1, col2, col3 = st.columns([1, 1, 1])
        if st.button("Reset"):
            st.session_state["objects"] = []
            st.session_state["listImage"] = []
            st.session_state["current_step"] = 0
            self.valid_points = []
            self.map = MAP
            st.session_state["result2_ready"] = False
            st.session_state["is_auto_running"] = False

        choice = st.selectbox("Chọn thuật toán:", options=['A*', 'BFS', 'DFS'])
        if st.button("Run"):
            self.handle_run(choice)
            st.session_state["result2_ready"] = True

        if st.session_state.get("result2_ready", False):
            prev_disabled = st.session_state["current_step"] <= 0 or st.session_state["is_auto_running"]
            next_disabled = st.session_state["current_step"] >= len(st.session_state.get("listImage", [])) - 3 or \
                            st.session_state["is_auto_running"]

            with col1:
                if st.button("Prev", disabled=prev_disabled):
                    self.btn_prev_step_click()
            with col2:
                if st.session_state["is_auto_running"]:
                    if st.button("Stop Auto"):
                        st.session_state["is_auto_running"] = False
                else:
                    if st.button("Auto"):
                        self.display_path()
            with col3:
                if st.button("Next", disabled=next_disabled):
                    self.btn_next_step_click()


def main():
    app = MazeApp()
    app.run()


if __name__ == "__main__":
    main()
