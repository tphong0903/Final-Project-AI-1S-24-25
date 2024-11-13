import cv2
import numpy as np

# Đọc hình ảnh
image = cv2.imread('hehe.jpg')

# Chuyển đổi sang ảnh xám
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Chuyển ảnh xám thành trắng đen (bằng ngưỡng)
_, binary = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)

# Phát hiện viền bằng thuật toán Canny
edges = cv2.Canny(binary, 100, 200)

# Tìm các khu vực (contours)
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Đếm số lượng khu vực
num_contours = len(contours)

# Hiển thị kết quả
print(f'Số lượng khu vực: {num_contours}')

# Vẽ viền lên hình ảnh gốc (tuỳ chọn)
cv2.drawContours(image, contours, -1, (0, 255, 0), 2)

# Hiển thị hình ảnh
cv2.imshow('Binary Image', binary)
cv2.imshow('Edges', edges)
cv2.imshow('Contours', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
