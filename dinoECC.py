def is_on_curve(x, y, p):
    # 检查点 (x, y) 是否在椭圆曲线 y^2 = x^3 + x + 1 上
    if (y ** 2) % p != (x ** 3 + x + 1) % p:
        return False
    return True

def find_points_on_elliptic_curve(p):
    # 找到椭圆曲线 y^2 = x^3 + x + 1 在有限域 F_p 上的所有点
    points = []
    for x in range(p):
        for y in range(p):
            if is_on_curve(x, y, p):
                points.append((x, y))
    return points

# 选择一个素数 p 作为有限域的大小
p = 23
points = find_points_on_elliptic_curve(p)
print(f"椭圆曲线的解点有：")
for point in points:
    print(point,end=" ")
print("O")