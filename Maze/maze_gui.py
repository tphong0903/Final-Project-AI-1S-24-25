# Tài liệu tham khảo
# A. Artasanchez, P. Joshi, 
# Artificial Intelligence with Python, 
# 2nd Edition, Packt, 2020
# Trang 242

import math
from simpleai.search import SearchProblem, astar, breadth_first, depth_first
import numpy as np
import cv2
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox
import time
import copy

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
##############################################
#         #              #           #       #
# ####    ########       #   #######         #
#    #    #              #   #               #
#    ###     #####  ######   ########    #####
#      #   ###   #           #      #    #   #
#      #     #   #  #  #   ###   ####  #     #
#     #####    #    #  #     #  ##  #  #######
#     #        #       #     #  #   ##       #
# #######     ######  ########  #    ####### #
#     #       #          #        #    #     #
#    ###      ###   ######  #######    ####  #
#    #   #    #      #         #       #     #
# ########   #######    ######     #   # #   #
#             #          #         #     #   #
##############################################
"""

# Convert map to a list
MAP = [list(x) for x in MAP.split("\n") if x]
MAP2 = MAP
M = len(MAP)
N = len(MAP[0])
W = 21

mau_xanh = np.zeros((W, W, 3), np.uint8) + (np.uint8(255), np.uint8(0), np.uint8(0))
mau_trang = np.zeros((W, W, 3), np.uint8) + (np.uint8(255), np.uint8(255), np.uint8(255))
image = np.ones((M * W, N * W, 3), np.uint8) * 255

for x in range(0, M):
    for y in range(0, N):
        if MAP[x][y] == '#':
            image[x * W:(x + 1) * W, y * W:(y + 1) * W] = mau_xanh
        elif MAP[x][y] == ' ':
            image[x * W:(x + 1) * W, y * W:(y + 1) * W] = mau_trang

color_coverted = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
pil_image = Image.fromarray(color_coverted)


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


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.dem = 0
        self.path = []
        self.current_step = 0
        self.result = None
        self.MAP = copy.deepcopy(MAP2)
        self.title('Tìm đường trong mê cung')
        self.cvs_me_cung = tk.Canvas(self, width=N * W, height=M * W,
                                     relief=tk.SUNKEN, border=1)

        self.image_tk = ImageTk.PhotoImage(pil_image)
        self.cvs_me_cung.create_image(0, 0, anchor=tk.NW, image=self.image_tk)

        self.cvs_me_cung.bind("<Button-1>", self.xu_ly_mouse)

        lbl_frm_menu = tk.LabelFrame(self)
        btn_start_A = tk.Button(lbl_frm_menu, text='A*', width=7,
                                command=lambda: self.btn_start_click(1))
        btn_start_BFS = tk.Button(lbl_frm_menu, text='BFS', width=7,
                                  command=lambda: self.btn_start_click(2))
        btn_start_UC = tk.Button(lbl_frm_menu, text='DFS', width=7,
                                 command=lambda: self.btn_start_click(3))
        btn_reset = tk.Button(lbl_frm_menu, text='Reset', width=7,
                              command=self.btn_reset_click)
        btn_start_A.grid(row=0, column=0, padx=5, pady=5, sticky=tk.N)
        btn_start_BFS.grid(row=1, column=0, padx=5, pady=5, sticky=tk.N)
        btn_start_UC.grid(row=2, column=0, padx=5, pady=5, sticky=tk.N)
        btn_reset.grid(row=3, column=0, padx=5, pady=5, sticky=tk.N)

        self.cvs_me_cung.grid(row=0, column=0, padx=5, pady=5)
        lbl_frm_menu.grid(row=0, column=1, padx=5, pady=7, sticky=tk.NW)

        lbl_frm_step = tk.LabelFrame(self)
        self.btn_draw_auto = tk.Button(lbl_frm_step, text='Auto', width=7,
                                       command=self.btn_draw_click)
        self.btn_prev_step = tk.Button(lbl_frm_step, text='Prev', width=7,
                                       command=self.btn_prev_step_click)
        self.btn_next_step = tk.Button(lbl_frm_step, text='Next', width=7,
                                       command=self.btn_next_step_click)
        self.step_label = tk.Label(lbl_frm_step, text='Số bước: 0 / 0', width=12)
        self.btn_draw_auto.grid(row=0, column=1, padx=5, pady=5, sticky=tk.N)
        self.btn_prev_step.grid(row=0, column=0, padx=5, pady=5, sticky=tk.N)
        self.btn_next_step.grid(row=0, column=2, padx=5, pady=5, sticky=tk.N)
        self.btn_next_step.grid(row=0, column=2, padx=5, pady=5, sticky=tk.N)
        self.step_label.grid(row=1, column=1, padx=5, pady=5, sticky=tk.N)
        lbl_frm_step.grid(row=1, column=0, padx=5, pady=7, sticky=tk.N)

    def xu_ly_mouse(self, event):
        if self.dem == 0:
            px = event.x
            py = event.y
            x = px // W
            y = py // W
            if self.MAP[y][x] != '#':
                self.MAP[y][x] = 'o'
                self.dem = self.dem + 1
                self.cvs_me_cung.create_oval(x * W + 2, y * W + 2, (x + 1) * W - 2, (y + 1) * W - 2,
                                             outline='#FF0000', fill='#FF0000')
            else:
                messagebox.showinfo("Thông báo", "Điểm không hợp lệ!!!")
        elif self.dem == 1:
            px = event.x
            py = event.y
            x = px // W
            y = py // W
            if self.MAP[y][x] != '#':
                self.MAP[y][x] = 'x'
                self.dem = self.dem + 1
                self.cvs_me_cung.create_rectangle(x * W + 2, y * W + 2, (x + 1) * W - 2, (y + 1) * W - 2,
                                                  outline='#FF0000', fill='#FF0000')
            else:
                messagebox.showinfo("Thông báo", "Điểm không hợp lệ!!!")

    def btn_start_click(self, check):
        if self.result is not None:
            self.btn_reset_click()
        if self.dem < 2:
            messagebox.showinfo("Thông báo", "Vui lòng chọn điểm!!!")
        else:
            problem = MazeSolver(self.MAP)
            # Run the solver
            self.result = None
            if check == 1:
                self.result = astar(problem, graph_search=True)
            elif check == 2:
                self.result = breadth_first(problem, graph_search=True)
            else:
                self.result = depth_first(problem, graph_search=True)
            # Extract the path
            if self.result:
                self.path = [x[1] for x in self.result.path()]
                self.current_step = 0
                messagebox.showinfo("Thông báo", "Đã tìm xong!!!")
                self.update_step_label()

    def btn_reset_click(self):
        self.btn_prev_step.config(state=tk.ACTIVE)
        self.btn_next_step.config(state=tk.ACTIVE)
        self.dem = 0
        self.path = []
        self.current_step = 0
        self.result = None
        self.MAP = copy.deepcopy(MAP2)
        self.cvs_me_cung.delete(tk.ALL)
        self.cvs_me_cung.create_image(0, 0, anchor=tk.NW, image=self.image_tk)

    def btn_draw_click(self):
        if self.dem < 2 or self.result is None:
            messagebox.showinfo("Thông báo", "Vui lòng thuật toán!!!")
        else:
            self.btn_prev_step.config(state=tk.DISABLED)
            self.btn_next_step.config(state=tk.DISABLED)
            path = [x[1] for x in self.result.path()]
            for i in range(1, len(self.path)):
                if self.result is None:
                    break
                x = path[i][0]
                y = path[i][1]
                self.cvs_me_cung.create_rectangle(x * W + 2, y * W + 2, (x + 1) * W - 2, (y + 1) * W - 2,
                                                  outline='#FF0000', fill='#FF0000')
                time.sleep(0.5)
                self.current_step += 1
                self.cvs_me_cung.update()
                self.update_step_label()

    def btn_next_step_click(self):
        if self.dem < 2 or self.result is None:
            messagebox.showinfo("Thông báo", "Vui lòng thuật toán!!!")
        else:
            if self.current_step < len(self.path) - 1:
                self.btn_prev_step.config(state=tk.ACTIVE)
                self.current_step += 1
                x, y = self.path[self.current_step]
                self.cvs_me_cung.create_rectangle(x * W + 2, y * W + 2, (x + 1) * W - 2, (y + 1) * W - 2,
                                                  outline='#FF0000', fill='#FF0000')
                self.update_step_label()
            if self.current_step == len(self.path) - 2:
                self.btn_next_step.config(state=tk.DISABLED)

    def btn_prev_step_click(self):
        if self.dem < 2 or self.result is None:
            messagebox.showinfo("Thông báo", "Vui lòng thuật toán!!!")
        else:
            if self.current_step > 0:
                self.btn_next_step.config(state=tk.ACTIVE)
                x, y = self.path[self.current_step]
                self.cvs_me_cung.create_rectangle(x * W + 2, y * W + 2, (x + 1) * W - 2, (y + 1) * W - 2,
                                                  outline='#FFFFFF', fill='#FFFFFF')
                self.current_step -= 1
                self.update_step_label()
            elif self.current_step == 0:
                self.btn_prev_step.config(state=tk.DISABLED)

    def update_step_label(self):
        total_steps = len(self.path) - 1 if self.path else 0
        if self.current_step == total_steps:
            self.current_step -= 1
        self.step_label.config(text=f"Số bước: {self.current_step} / {total_steps - 1}")


if __name__ == "__main__":
    app = App()
    app.mainloop()
