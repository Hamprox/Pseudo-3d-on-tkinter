import tkinter as tk
from math import *
from collections import namedtuple

# Вектор в 3D
Vector3 = namedtuple('Vector3', ['x', 'y', 'z'])

# Операции с векторами
def vec_add(v1, v2):
    return Vector3(v1.x + v2.x, v1.y + v2.y, v1.z + v2.z)

def vec_sub(v1, v2):
    return Vector3(v1.x - v2.x, v1.y - v2.y, v1.z - v2.z)

def vec_dot(v1, v2):
    return v1.x*v2.x + v1.y*v2.y + v1.z*v2.z

def vec_cross(v1, v2):
    return Vector3(v1.y*v2.z - v1.z*v2.y, v1.z*v2.x - v1.x*v2.z, v1.x*v2.y - v1.y*v2.x)

def vec_scale(v, s):
    return Vector3(v.x*s, v.y*s, v.z*s)

def vec_normalize(v):
    mag = sqrt(vec_dot(v, v))
    return vec_scale(v, 1/mag) if mag > 0 else v

def rotate_point_around_y(point, angle, hinge):
    dx = point.x - hinge.x
    dz = point.z - hinge.z
    x_rot = dx * cos(angle) + dz * sin(angle)
    z_rot = -dx * sin(angle) + dz * cos(angle)
    return Vector3(hinge.x + x_rot, point.y, hinge.z + z_rot)

# Плоскость для клиппинга
Plane = namedtuple('Plane', ['normal', 'd'])

# Класс камеры
class Camera:
    def __init__(self, position, yaw, pitch):
        self.position = position
        self.yaw = yaw
        self.pitch = pitch

    def get_view_matrix(self):
        forward = Vector3(cos(self.yaw)*cos(self.pitch), sin(self.pitch), sin(self.yaw)*cos(self.pitch))
        forward = vec_normalize(forward)
        right = vec_normalize(vec_cross(Vector3(0,1,0), forward))
        up = vec_normalize(vec_cross(forward, right))
        return right, up, forward

    def transform_to_camera_space(self, point):
        right, up, forward = self.get_view_matrix()
        p = vec_sub(point, self.position)
        return Vector3(vec_dot(right, p), vec_dot(up, p), -vec_dot(forward, p))

# Класс полигона
class Polygon:
    def __init__(self, vertices, color):
        self.vertices = vertices
        self.color = color

# Класс сцены
class Scene:
    def __init__(self):
        L = 2
        self.polygons = [
            # Пол
            Polygon([Vector3(-L,0,-L), Vector3(L,0,-L), Vector3(L,0,L)], 'gray'),
            Polygon([Vector3(-L,0,-L), Vector3(L,0,L), Vector3(-L,0,L)], 'gray'),
            # Пол (обратная сторона)
            Polygon([Vector3(-L,0,-L), Vector3(-L,0,L), Vector3(L,0,L)], 'gray'),
            Polygon([Vector3(-L,0,-L), Vector3(L,0,L), Vector3(L,0,-L)], 'gray'),
            # Потолок
            Polygon([Vector3(-L,2,-L), Vector3(L,2,-L), Vector3(L,2,L)], 'lightgray'),
            Polygon([Vector3(-L,2,-L), Vector3(L,2,L), Vector3(-L,2,L)], 'lightgray'),
            # Потолок (обратная сторона)
            Polygon([Vector3(-L,2,-L), Vector3(-L,2,L), Vector3(L,2,L)], 'lightgray'),
            Polygon([Vector3(-L,2,-L), Vector3(L,2,L), Vector3(L,2,-L)], 'lightgray'),
            # Левая стена
            Polygon([Vector3(-L,0,-L), Vector3(-L,2,-L), Vector3(-L,2,L)], 'red'),
            Polygon([Vector3(-L,0,-L), Vector3(-L,2,L), Vector3(-L,0,L)], 'red'),
            # Левая стена (обратная сторона)
            Polygon([Vector3(-L,0,-L), Vector3(-L,0,L), Vector3(-L,2,L)], 'red'),
            Polygon([Vector3(-L,0,-L), Vector3(-L,2,L), Vector3(-L,2,-L)], 'red'),
            # Правая стена
            Polygon([Vector3(L,0,-L), Vector3(L,2,-L), Vector3(L,2,L)], 'green'),
            Polygon([Vector3(L,0,-L), Vector3(L,2,L), Vector3(L,0,L)], 'green'),
            # Правая стена (обратная сторона)
            Polygon([Vector3(L,0,-L), Vector3(L,0,L), Vector3(L,2,L)], 'green'),
            Polygon([Vector3(L,0,-L), Vector3(L,2,L), Vector3(L,2,-L)], 'green'),
            # Задняя стена
            Polygon([Vector3(-L,0,L), Vector3(L,0,L), Vector3(L,2,L)], 'yellow'),
            Polygon([Vector3(-L,0,L), Vector3(L,2,L), Vector3(-L,2,L)], 'yellow'),
            # Задняя стена (обратная сторона)
            Polygon([Vector3(-L,0,L), Vector3(-L,2,L), Vector3(L,2,L)], 'yellow'),
            Polygon([Vector3(-L,0,L), Vector3(L,2,L), Vector3(L,0,L)], 'yellow'),
            # Передняя стена с вырезом для двери
            Polygon([Vector3(-L,1.5,-L), Vector3(L,1.5,-L), Vector3(L,2,-L), Vector3(-L,2,-L)], 'blue'),
            Polygon([Vector3(-L,0,-L), Vector3(-0.5,0,-L), Vector3(-0.5,1.5,-L), Vector3(-L,1.5,-L)], 'blue'),
            Polygon([Vector3(0.5,0,-L), Vector3(L,0,-L), Vector3(L,1.5,-L), Vector3(0.5,1.5,-L)], 'blue'),
            # Передняя стена (обратная сторона)
            Polygon([Vector3(-L,1.5,-L), Vector3(-L,2,-L), Vector3(L,2,-L), Vector3(L,1.5,-L)], 'blue'),
            Polygon([Vector3(-L,0,-L), Vector3(-L,1.5,-L), Vector3(-0.5,1.5,-L), Vector3(-0.5,0,-L)], 'blue'),
            Polygon([Vector3(0.5,0,-L), Vector3(0.5,1.5,-L), Vector3(L,1.5,-L), Vector3(L,0,-L)], 'blue'),
        ]
        self.camera = Camera(Vector3(0,1,0), 0, 0)
        self.near = 0.1
        self.fov_v = 60
        self.door_angle = 0

    def get_door_vertices(self):
        L = 2
        door_left = -0.5
        door_right = 0.5
        door_bottom = 0
        door_top = 1.5
        door_vertices_closed = [
            Vector3(door_left, door_bottom, -L),
            Vector3(door_right, door_bottom, -L),
            Vector3(door_right, door_top, -L),
            Vector3(door_left, door_top, -L)
        ]
        hinge = Vector3(door_left, 0, -L)
        return [rotate_point_around_y(v, self.door_angle, hinge) for v in door_vertices_closed]

    def get_door_center(self):
        door_vertices = self.get_door_vertices()
        sum_x = sum(v.x for v in door_vertices)
        sum_y = sum(v.y for v in door_vertices)
        sum_z = sum(v.z for v in door_vertices)
        return Vector3(sum_x / 4, sum_y / 4, sum_z / 4)

    def clip_polygon(self, polygon):
        plane = Plane(Vector3(0,0,-1), -self.near)
        def inside(p):
            return vec_dot(plane.normal, p) + plane.d >= 0
        clipped_vertices = []
        for i in range(len(polygon.vertices)):
            p1 = polygon.vertices[i]
            p2 = polygon.vertices[(i+1)%len(polygon.vertices)]
            if inside(p1):
                if inside(p2):
                    clipped_vertices.append(p2)
                else:
                    t = -(vec_dot(plane.normal, p1) + plane.d) / vec_dot(plane.normal, vec_sub(p2, p1))
                    intersection = vec_add(p1, vec_scale(vec_sub(p2, p1), t))
                    clipped_vertices.append(intersection)
            else:
                if inside(p2):
                    t = -(vec_dot(plane.normal, p1) + plane.d) / vec_dot(plane.normal, vec_sub(p2, p1))
                    intersection = vec_add(p1, vec_scale(vec_sub(p2, p1), t))
                    clipped_vertices.append(intersection)
                    clipped_vertices.append(p2)
        return Polygon(clipped_vertices, polygon.color) if len(clipped_vertices) >= 3 else None

    def project_point(self, point, width, height):
        tan_fov_v_2 = tan(radians(self.fov_v / 2))
        aspect = width / height
        tan_fov_h_2 = aspect * tan_fov_v_2
        x_proj = (point.x / -point.z) / tan_fov_h_2
        y_proj = (point.y / -point.z) / tan_fov_v_2
        canvas_x = (x_proj + 1) * (width / 2)
        canvas_y = (1 - y_proj) * (height / 2)
        return canvas_x, canvas_y

    def render(self, canvas, width, height):
        canvas.delete('scene')
        camera_polygons = []
        for poly in self.polygons + [Polygon(self.get_door_vertices(), 'brown')]:
            camera_vertices = [self.camera.transform_to_camera_space(v) for v in poly.vertices]
            camera_poly = Polygon(camera_vertices, poly.color)
            clipped_poly = self.clip_polygon(camera_poly)
            if clipped_poly:
                camera_polygons.append(clipped_poly)
        # Сортировка по максимальному z для исправления видимости двери
        camera_polygons.sort(key=lambda p: max(v.z for v in p.vertices), reverse=True)
        for poly in camera_polygons:
            projected_points = [self.project_point(v, width, height) for v in poly.vertices]
            canvas.create_polygon(projected_points, fill=poly.color, tags='scene')

    def is_inside_room(self, position):
        L = 2
        if self.door_angle == pi/2:  # дверь открыта
            if position.z >= -L:
                return -L < position.x < L and 0 < position.y < 2
            else:  # position.z < -L
                return -0.5 < position.x < 0.5 and 0 < position.y < 2
        else:  # дверь закрыта
            return -L < position.x < L and 0 < position.y < 2 and -L < position.z < L

# Класс джойстика
class Joystick:
    def __init__(self, canvas, cx, cy, radius):
        self.canvas = canvas
        self.cx = cx
        self.cy = cy
        self.radius = radius
        self.dragging = False
        self.knob_x = cx
        self.knob_y = cy
        self.base_id = None
        self.knob_id = None

    def is_inside(self, x, y):
        dx = x - self.cx
        dy = y - self.cy
        return dx*dx + dy*dy <= self.radius**2

    def start_drag(self, x, y):
        self.dragging = True
        self.update_drag(x, y)

    def update_drag(self, x, y):
        dx = x - self.cx
        dy = y - self.cy
        dist = sqrt(dx*dx + dy*dy)
        if dist > self.radius:
            dx = dx * self.radius / dist
            dy = dy * self.radius / dist
        self.knob_x = self.cx + dx
        self.knob_y = self.cy + dy

    def end_drag(self):
        self.dragging = False
        self.knob_x = self.cx
        self.knob_y = self.cy

    def get_input(self):
        dx = (self.knob_x - self.cx) / self.radius
        dy = (self.knob_y - self.cy) / self.radius
        return -dx, -dy

    def draw(self):
        if self.base_id is not None:
            self.canvas.delete(self.base_id)
        if self.knob_id is not None:
            self.canvas.delete(self.knob_id)
        self.base_id = self.canvas.create_oval(self.cx - self.radius, self.cy - self.radius, 
                                               self.cx + self.radius, self.cy + self.radius, fill='lightgray', tags='ui')
        knob_radius = 20
        self.knob_id = self.canvas.create_oval(self.knob_x - knob_radius, self.knob_y - knob_radius, 
                                               self.knob_x + knob_radius, self.knob_y + knob_radius, fill='gray', tags='ui')

# Приложение
class App:
    def __init__(self):
        self.root = tk.Tk()
        self.canvas = tk.Canvas(self.root, width=800, height=600)
        self.canvas.pack()
        self.scene = Scene()
        self.move_joystick = Joystick(self.canvas, 100, 500, 50)
        self.view_joystick = Joystick(self.canvas, 700, 500, 50)
        self.canvas.bind('<Button-1>', self.on_mouse_down)
        self.canvas.bind('<B1-Motion>', self.on_mouse_move)
        self.canvas.bind('<ButtonRelease-1>', self.on_mouse_up)
        self.door_button = tk.Button(self.root, text="Toggle Door", command=self.try_toggle_door)
        self.canvas.create_window(400, 550, window=self.door_button)
        self.crosshair_ids = []
        self.can_toggle_door = False
        self.status_text_id = self.canvas.create_text(400, 20, text="", fill="white", font=("Arial", 16), tags='ui')
        self.running = True
        self.update()

    def on_mouse_down(self, event):
        if self.move_joystick.is_inside(event.x, event.y):
            self.move_joystick.start_drag(event.x, event.y)
        elif self.view_joystick.is_inside(event.x, event.y):
            self.view_joystick.start_drag(event.x, event.y)

    def on_mouse_move(self, event):
        if self.move_joystick.dragging:
            self.move_joystick.update_drag(event.x, event.y)
        elif self.view_joystick.dragging:
            self.view_joystick.update_drag(event.x, event.y)

    def on_mouse_up(self, event):
        self.move_joystick.end_drag()
        self.view_joystick.end_drag()

    def draw_crosshair(self):
        for cid in self.crosshair_ids:
            self.canvas.delete(cid)
        self.crosshair_ids = []
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        center_x = width / 2
        center_y = height / 2
        h_line = self.canvas.create_line(center_x - 10, center_y, center_x + 10, center_y, fill='white', tags='ui')
        v_line = self.canvas.create_line(center_x, center_y - 10, center_x, center_y + 10, fill='white', tags='ui')
        self.crosshair_ids = [h_line, v_line]

    def try_toggle_door(self):
        print(f"Trying to toggle door: can_toggle_door={self.can_toggle_door}")
        if self.can_toggle_door:
            self.scene.door_angle = pi / 2 if self.scene.door_angle == 0 else 0
            print(f"Door angle set to {self.scene.door_angle}")

    def update(self):
        if not self.running:
            return
        view_dx, view_dy = self.view_joystick.get_input()
        move_dx, move_dy = self.move_joystick.get_input()
        self.scene.camera.yaw += view_dx * 0.05
        self.scene.camera.pitch += view_dy * 0.05
        self.scene.camera.pitch = max(-pi/2, min(pi/2, self.scene.camera.pitch))
        right, up, forward = self.scene.camera.get_view_matrix()
        move_speed = 0.1
        new_position = vec_add(self.scene.camera.position, vec_scale(forward, move_dy * move_speed))
        if self.scene.is_inside_room(new_position):
            self.scene.camera.position = new_position
        new_position = vec_add(self.scene.camera.position, vec_scale(right, -move_dx * move_speed))
        if self.scene.is_inside_room(new_position):
            self.scene.camera.position = new_position
        self.scene.render(self.canvas, self.canvas.winfo_width(), self.canvas.winfo_height())
        self.move_joystick.draw()
        self.view_joystick.draw()
        self.draw_crosshair()
        
        # Обновление статуса двери
        self.canvas.delete(self.status_text_id)
        door_center = self.scene.get_door_center()
        camera_door_center = self.scene.camera.transform_to_camera_space(door_center)
        if camera_door_center.z < 0:
            projected = self.scene.project_point(camera_door_center, self.canvas.winfo_width(), self.canvas.winfo_height())
            screen_center = (self.canvas.winfo_width() / 2, self.canvas.winfo_height() / 2)
            dx = projected[0] - screen_center[0]
            dy = projected[1] - screen_center[1]
            distance_on_screen = sqrt(dx*dx + dy*dy)
            distance_to_door = sqrt(vec_dot(vec_sub(door_center, self.scene.camera.position), vec_sub(door_center, self.scene.camera.position)))
            self.can_toggle_door = distance_on_screen < 150 and distance_to_door < 2.5
            if self.can_toggle_door:
                self.status_text_id = self.canvas.create_text(400, 20, text="Door: Ready", fill="white", font=("Arial", 16), tags='ui')
            else:
                self.status_text_id = self.canvas.create_text(400, 20, text="Door: Too Far", fill="white", font=("Arial", 16), tags='ui')
        else:
            self.can_toggle_door = False
            self.status_text_id = self.canvas.create_text(400, 20, text="Door: Not in View", fill="white", font=("Arial", 16), tags='ui')
        
        self.root.after(16, self.update)

# Запуск
app = App()
app.root.mainloop()
