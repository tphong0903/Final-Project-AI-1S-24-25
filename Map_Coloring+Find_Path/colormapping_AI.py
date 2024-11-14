import cv2
import numpy as np
from simpleai.search import CspProblem, backtrack


def constraint_func(names, values):
    return values[0] != values[1]


def map_coloring():
    names = ('TayNinh', 'BinhPhuoc', 'BinhDuong', 'DongNai', 'BRVT',
             'TPHCM', 'LongAn', 'TienGiang', 'BenTre', 'TraVinh',
             'VinhLong', 'DongThap', 'AnGiang', 'CanTho', 'SocTrang',
             'HauGiang', 'KienGiang', 'CaMau', 'BacLieu',)

    names_point = [
        (391, 105), (500, 64), (459, 146), (534, 157), (545, 233),
        (470, 210), (397, 220), (401, 256), (440, 289), (419, 335),
        (375, 300), (308, 226), (269, 239), (307, 294), (367, 371),
        (336, 338), (266, 335), (252, 437), (309, 408)
    ]

    color_available = [
        'gray', 'green', 'yellow', 'purple', 'cyan', 'magenta', 'orange',
        'brown', 'pink', 'lime', 'olive', 'maroon', 'navy', 'teal',
        'gold', 'coral', 'salmon', 'violet', 'indigo'
    ]

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

    # Tạo danh sách ràng buộc
    constraints = []
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            constraints.append(((names[i], names[j]), constraint_func))

    # Giải bài toán CSP
    problem = CspProblem(names, colors, constraints)
    result = backtrack(problem)

    # Kiểm tra kết quả
    if not result:
        print("Không tìm được giải pháp.")
        exit()

    print('\nColor mapping:\n')
    for k, v in result.items():
        print(k, '==>', v)


    image = cv2.imread('Map_Coloring+Find_Path\input.png', cv2.IMREAD_GRAYSCALE)
    M, N = image.shape
    image_color = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

    color_map = {
        'gray': (104,104,104),
        'green': (0, 255, 0),
        'yellow': (0, 255, 255),
        'purple': (128, 0, 128),
        'cyan': (255, 255, 0),
        'magenta': (255, 0, 255),
        'orange': (0, 165, 255),
        'brown': (19, 69, 139),
        'pink': (203, 192, 255),
        'lime': (0, 255, 128),
        'olive': (0, 128, 128),
        'maroon': (0, 0, 128),
        'navy': (128, 0, 0),
        'teal': (128, 128, 0),
        'gold': (0, 215, 255),
        'coral': (80, 127, 255),
        'salmon': (114, 128, 250),
        'violet': (238, 130, 238),
        'indigo': (75, 0, 130)
    }

    mask = np.zeros((M + 2, N + 2), np.uint8)
    for province, color_name in result.items():
        point = names_point[names.index(province)]
        color = color_map[color_name]
        cv2.floodFill(image_color, mask, point, color)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(image_color, province, (point[0] - 15, point[1] - 8), font, 0.3, (0, 0, 0), 1, cv2.LINE_AA)

    image_resized = cv2.resize(image_color, (900, 600))
    cv2.imwrite('Map_Coloring+Find_Path/colored_map.png', image_resized)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
