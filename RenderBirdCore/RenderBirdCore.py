import pygame
from pygame.locals import *
import sys
from OpenGL.GL import *
from OpenGL.GLU import *
import time
import math
from PIL import Image
import numpy as np
import os
import struct
from OpenGL.arrays import vbo
from io import StringIO

class RenderBirdCore:
    def __init__(self, window_size_x=1280, window_size_y=720, window_title="RenderBird Program", depth_testing=True,camera_x=0, camera_y=0, camera_z=0, camera_pitch=0, camera_yaw=0, camera_roll=0, camera_fov=45, camera_minimum_render_distance=0.1, camera_maximum_render_distance=50.0):
        pygame.init()
        RENDERBIRD_VERSION = "0.1.0"
        self.window_size_x = window_size_x
        self.window_size_y = window_size_y
        self.screen = pygame.display.set_mode((self.window_size_x, self.window_size_y), DOUBLEBUF | OPENGL)
        pygame.display.set_caption(window_title)
        self.depth_testing_enabled = depth_testing
        if depth_testing:
            glEnable(GL_DEPTH_TEST)
            glDepthFunc(GL_LESS)  # Use the default depth function (objects closer to the camera are rendered first)
        
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        
        # Initialize the camera
        self.camera = self.Camera(self.window_size_x, self.window_size_y, camera_x, camera_y, camera_z, camera_pitch, camera_yaw, camera_roll, camera_fov, camera_minimum_render_distance, camera_maximum_render_distance)
        self.run_once_list = []
        self.running = True
        self.background_color = (0.0, 0.0, 0.0, 1.0)  # RGBA
        self.is_fullscreen = False
        print("Started OpenGL and RenderBird " + RENDERBIRD_VERSION)
    
    
    def enter_fullscreen(self):
        """
        Switch to fullscreen mode
        """
        self.is_fullscreen = True
        self.screen = pygame.display.set_mode(
            (self.window_size_x, self.window_size_y),
            pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.OPENGL
        )
        
    
    def exit_fullscreen(self):
        """
        Switch to windowed mode
        """
        self.is_fullscreen = False
        self.screen = pygame.display.set_mode(
            (self.window_size_x, self.window_size_y),
            pygame.RESIZABLE | pygame.DOUBLEBUF | pygame.OPENGL
        )
        
    
    def toggle_fullscreen(self):
        """
        Toggle between fullscreen and windowed mode
        """
        if self.is_fullscreen:
            self.exit_fullscreen()
        else:
            self.enter_fullscreen()
    
    
    def enable_depth_testing(self, value: bool):
        """
        Use value argument to turn it on or off.
        With Depth Testing enabled, objects render in order as you see them. Objects closer to camera are rendered first.
        Without it, an object that is behind another object may render like if it was in front of it, which may look confusing to say at least.
        """
        self.depth_testing_enabled = value
        if value:
            glEnable(GL_DEPTH_TEST)
            glDepthFunc(GL_LESS)
        else:
            glDisable(GL_DEPTH_TEST)

    def GetPygameScreen(self):
        """
        Returns PyGame screen object
        """
        return self.screen


    class Camera:
        def __init__(self, view_width, view_height, x=0, y=0, z=0, pitch=0, yaw=0, roll=0, fov=45, minimum_render_distance=0.1, maximum_render_distance=50):
            """
            Initializes the Camera with position, rotation, and perspective settings.
            
            :param view_width: Width of the viewport.
            :param view_height: Height of the viewport.
            :param x: Initial X position.
            :param y: Initial Y position.
            :param z: Initial Z position.
            :param pitch: Initial pitch angle (rotation around X-axis).
            :param yaw: Initial yaw angle (rotation around Y-axis).
            :param roll: Initial roll angle (rotation around Z-axis).
            :param fov: Field of view angle.
            :param minimum_render_distance: Minimum render distance.
            :param maximum_render_distance: Maximum render distance.
            """
            
            self.view_width = view_width
            self.view_height = view_height
            self.position = [x, y, z]
            self.rotation = [pitch, yaw, roll]
            self.fov = fov
            self.min_render_distance = minimum_render_distance
            self.max_render_distance = maximum_render_distance
            self.forward_vector = [0, 0, -1]  # Initial forward direction
            self.setup_perspective()
            self.update_forward_vector()
        
        def update_forward_vector(self):
            """
            Updates the forward vector based on current pitch and yaw angles.
            """
            pitch_rad = math.radians(self.rotation[0])
            yaw_rad = math.radians(self.rotation[1])
            self.forward_vector = [
                math.cos(pitch_rad) * math.sin(yaw_rad),
                math.sin(pitch_rad),
                -math.cos(pitch_rad) * math.cos(yaw_rad)
            ]
            ##print(f"Updated Forward Vector: X={self.forward_vector[0]:.2f}, Y={self.forward_vector[1]:.2f}, Z={self.forward_vector[2]:.2f}")
        
        def rotate_pitch(self, delta_pitch, reverse=False):
            """
            Rotates the camera's pitch.
            
            :param delta_pitch: The amount to change the pitch by.
            :param reverse: If True, reverses the pitch direction.
            """
            if reverse:
                delta_pitch = -delta_pitch
            self.rotation[0] += delta_pitch
            self.rotation[0] = max(-90, min(90, self.rotation[0]))
            self.update_forward_vector()
            self.setup_perspective()
        
        def rotate_yaw(self, delta_yaw, reverse=False):
            """
            Rotates the camera's yaw.
            
            :param delta_yaw: The amount to change the yaw by.
            :param reverse: If True, reverses the yaw direction.
            """
            if reverse:
                delta_yaw = -delta_yaw
            self.rotation[1] += delta_yaw
            self.update_forward_vector()
            self.setup_perspective()
        
        def rotate(self, pitch, yaw, roll):
            """
            Rotates the camera by specified pitch, yaw, and roll angles.
            
            :param pitch: Change in pitch angle.
            :param yaw: Change in yaw angle.
            :param roll: Change in roll angle.
            """
            self.rotation[0] += pitch
            self.rotation[1] += yaw
            self.rotation[2] += roll
            self.update_forward_vector()
            self.setup_perspective()
        
        def setup_perspective(self):
            """
            Sets up the perspective projection and camera view using gluLookAt.
            """
            glMatrixMode(GL_PROJECTION)
            glLoadIdentity()
            gluPerspective(self.fov, (self.view_width / self.view_height), self.min_render_distance, self.max_render_distance)
            
            glMatrixMode(GL_MODELVIEW)
            glLoadIdentity()
            
            target = [
                self.position[0] + self.forward_vector[0],
                self.position[1] + self.forward_vector[1],
                self.position[2] + self.forward_vector[2]
            ]
            
            gluLookAt(
                self.position[0], self.position[1], self.position[2],  
                target[0], target[1], target[2],                          
                0, 1, 0                                                  
            )
        
        def apply_rotation(self):
            """
            This method is retained for compatibility but is no longer used since gluLookAt is employed.
            """
            glRotatef(self.rotation[0], 1, 0, 0)  # Pitch
            glRotatef(self.rotation[1], 0, 1, 0)  # Yaw
            glRotatef(self.rotation[2], 0, 0, 1)  # Roll
        
        def translate(self, dx, dy, dz):
            """
            Translates the camera by the given amounts.
            
            :param dx: Translation along the X-axis.
            :param dy: Translation along the Y-axis.
            :param dz: Translation along the Z-axis.
            """
            self.position[0] += dx
            self.position[1] += dy
            self.position[2] += dz
            self.setup_perspective()
        
        def move(self, x_transform, y_transform, z_transform):
            """
            Moves the camera based on input transformations, considering the current yaw angle.
            
            :param x_transform: Movement along the right vector (strafe).
            :param y_transform: Movement along the up vector.
            :param z_transform: Movement along the forward vector.
            """
            # Calculate movement in world coordinates based on yaw
            yaw_rad = math.radians(self.rotation[1])
            # Right vector (perpendicular to forward vector in the horizontal plane)
            right = [
                math.cos(yaw_rad),
                0,
                math.sin(yaw_rad)
            ]
            # Forward vector in the horizontal plane (ignoring pitch for strafing)
            forward = [
                math.sin(yaw_rad),
                0,
                -math.cos(yaw_rad)
            ]
            
            # Calculate the movement in world coordinates
            dx = x_transform * right[0] + z_transform * forward[0]
            dy = y_transform
            dz = x_transform * right[2] + z_transform * forward[2]
            
            self.translate(dx, dy, dz)
        
        def look_around(self, delta_x, delta_y, sensitivity=0.1, reverse_horiz=False, reverse_vert=False):
            """
            Adjusts the camera's yaw and pitch based on mouse movement.
    
            :param delta_x: Mouse movement in the X-direction.
            :param delta_y: Mouse movement in the Y-direction.
            :param sensitivity: Sensitivity factor for mouse movement.
            :param reverse_horiz: If True, reverses the horizontal look direction.
            :param reverse_vert: If True, reverses the vertical look direction.
            """
            delta_x *= sensitivity
            delta_y *= sensitivity
            delta_y = -delta_y
            
            if reverse_horiz:
                delta_x = -delta_x
            if reverse_vert:
                delta_y = -delta_y
    
            self.rotation[1] += delta_x  # Yaw
            self.rotation[0] += delta_y  # Pitch
    
            self.rotation[0] = max(-90, min(90, self.rotation[0]))
    
            self.update_forward_vector()
            self.setup_perspective()
    
        def use_mouse_camera_controls(self, window_size_x: int, window_size_y: int, sensitivity=0.1, sensitivity_factor=1, reverse_horizontally=False, reverse_vertially=False, mouse_cursor_visible=False):
            """
            Implements mouse-based camera controls by capturing mouse movement and adjusting the camera's orientation.
    
            :param window_size_x: Width of the window.
            :param window_size_y: Height of the window.
            :param sensitivity: Sensitivity factor for mouse movement.
            :param sensitivity_factor: Additional sensitivity scaling factor.
            :param reverse_horizontally: If True, reverses horizontal mouse movement.
            :param reverse_vertially: If True, reverses vertical mouse movement.
            :param mouse_cursor_visible: If True, makes the mouse cursor visible.
            """
            mouse_x, mouse_y = pygame.mouse.get_pos()
            delta_x = (mouse_x - window_size_x / 2) / sensitivity_factor
            delta_y = (mouse_y - window_size_y / 2) / sensitivity_factor
            pygame.mouse.set_pos(window_size_x // 2, window_size_y // 2)
            pygame.mouse.set_visible(mouse_cursor_visible)
            self.look_around(delta_x, delta_y, sensitivity, reverse_horizontally, reverse_vertially)
        
        def get_world_position(self):
            """
            Returns the camera's position in world coordinates.
            
            :return: A list representing the camera's X, Y, Z position.
            """
            return self.position.copy()
        
        def detect_objects_in_view(self, objects, max_distance, angle_threshold):
            """
            Detects objects within the camera's view based on distance and angle threshold.
            
            :param objects: A list of objects with a 'position' attribute.
            :param max_distance: Maximum distance to detect objects.
            :param angle_threshold: Maximum angle (in degrees) from the forward vector to consider.
            :return: A list of detected objects.
            """
            detected_objects = []
            cam_pos = self.get_world_position()
            yaw_rad = math.radians(self.rotation[1])
            pitch_rad = math.radians(self.rotation[0])
            angle_threshold_rad = math.radians(angle_threshold)
            
            # Forward vector based on yaw and pitch
            forward = [
                math.cos(pitch_rad) * math.sin(yaw_rad),
                math.sin(pitch_rad),
                -math.cos(pitch_rad) * math.cos(yaw_rad)
            ]
            
            for obj in objects:
                obj_pos = obj.position
                cam_to_obj = [obj_pos[i] - cam_pos[i] for i in range(3)]
                distance = math.sqrt(sum(comp ** 2 for comp in cam_to_obj))
                
                if distance <= max_distance:
                    cam_to_obj_normalized = [comp / distance for comp in cam_to_obj]
                    dot_product = sum((forward[i] * cam_to_obj_normalized[i] for i in range(3)))
                    dot_product = max(min(dot_product, 1.0), -1.0)
                    angle = math.acos(dot_product)
                    angle_deg = math.degrees(angle)
                    
                    if angle <= angle_threshold_rad:
                        detected_objects.append(obj)
                        #print(f"Detected Object: {obj}")
            
            return detected_objects
        
        def draw_forward_vector(self, length=2.0):
            """
            Draws a line representing the camera's forward vector for debugging purposes.
            
            :param length: The length of the forward vector line.
            """
            glPushMatrix()
            glLoadIdentity()
            glBegin(GL_LINES)
            glColor3f(1.0, 0.0, 0.0)  # Red color for the forward vector
            cam_world_pos = self.get_world_position()
            glVertex3f(cam_world_pos[0], cam_world_pos[1], cam_world_pos[2])
            glVertex3f(
                cam_world_pos[0] + self.forward_vector[0] * length,
                cam_world_pos[1] + self.forward_vector[1] * length,
                cam_world_pos[2] + self.forward_vector[2] * length
            )
            glEnd()
            glPopMatrix()
        

    #Utility and functions:

    class RunAfterTime:
        """
        Allows to run a function after certain amount of time passes.
        """
        def __init__(self, seconds: float):
            """
            :param seconds: Seconds that must pass from initalization or last reset for the function to run.
            """
            self.seconds = seconds
            self.start_time = time.time()
            self.run_once_list = []
            
        def run_once(self, function, *args, remove_not_run=False):
            """
            Run a function one time.
            :param function: Function
            :param *args: The function's arguments
            :param remove_not_run: If True, it will remove the function from its memory, making it possible to run again.
            """
            function_name = function.__name__
            if remove_not_run:
                if function_name in self.run_once_list:
                    self.run_once_list.remove(function_name)
            else:
                if function_name not in self.run_once_list:
                    self.run_once_list.append(function_name)
                    return function(*args)
            return None
                
        def run_once_after_time(self, function, *args):
            """
            Run a function once after certain amount of time
            :param function: Function
            :param *args: The function's arguments
            """
            if time.time() >= self.start_time + self.seconds:
                return self.run_once(function, *args)
            return None
                
        def run_after_time(self, function, *args):
            """
            Run a function after certain amount of time, without lock to run it only once.
            :param function: Function
            :param *args: The function's arguments
            """
            if time.time() >= self.start_time + self.seconds:
                return function(*args)
            return None
        
        def reset_start_time(self):
            """
            Resets the timestamp since which the function waits to run functions.
            """
            self.start_time = time.time()
            return self.start_time


    def run_once(self, function, *args, remove_not_run=False):
        """
        Run a function one time.
        :param function: Function
        :param *args: The function's arguments
        :param remove_not_run: If True, it will remove the function from its memory, making it possible to run again.
        """
        function_name = function.__name__
        if remove_not_run:
            if function_name in self.run_once_list:
                self.run_once_list.remove(function_name)
        else:
            if function_name not in self.run_once_list:  
                self.run_once_list.append(function_name)
                return function(*args)
        return None


    def key_pressed(self, key_pygame_var):
        """
        Returns whenever a keyboard key was pressed.
        :param key_pygame_var: Key to check for, PyGame variable, for example K_w
        """
        keys = pygame.key.get_pressed()
        return keys[key_pygame_var]
    
    def update_display(self):
        """
        Update the display to render things.
        """
        pygame.display.flip()
        glFlush()
        
    def set_background_color(self, r: float, g: float, b: float):
        """
        Sets color of the background (or if you prefer sky)
        """
        if r > 1:
            r = r / 255
        if g > 1:
            g = g / 255
        if b > 1:
            b = b / 255
        self.background_color = (r, g, b, 1.0)

    def clear_screen(self):
        """
        Clear screen to get rid of old frame
        """
        glClearColor(*self.background_color)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    def safe_close(self):
        """
        Closes the program ensuring PyGame and OpenGL stop too
        """
        print("Stopping PyGame and RenderBird. Goodbye!")
        pygame.time.wait(100)
        pygame.quit()
        sys.exit()
        exit()

    def handle_close_event(self):
        """
        Checks if program is commanded to close by the OS (for example because someone clicked X to close its window)
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
    def handle_close_event_direct(self):
        """
        Checks if program is commanded to close by the OS (for example because someone clicked X to close its window)
        Runs safe_close() instead of just changing running bool variable to False.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.safe_close()

    def draw_world_axes(self,length=5.0):
        """
        Draws the world coordinate axes for debugging purposes.
        
        :param length: Length of each axis line.
        """
        glPushMatrix()
        glBegin(GL_LINES)
        
        # X-axis (Red)
        glColor3f(1.0, 0.0, 0.0)
        glVertex3f(0, 0, 0)
        glVertex3f(length, 0, 0)
        
        # Y-axis (Green)
        glColor3f(0.0, 1.0, 0.0)
        glVertex3f(0, 0, 0)
        glVertex3f(0, length, 0)
        
        # Z-axis (Blue)
        glColor3f(0.0, 0.0, 1.0)
        glVertex3f(0, 0, 0)
        glVertex3f(0, 0, length)
        
        glEnd()
        glPopMatrix()


    class FPS_Limiter:
        """
        Allows to limit frames per second and program's speed in a consistent way, ensuring same top execution speed on all devices.
        """
        def __init__(self, max_fps: int):
            """
            :param max_fps: Maximum frames per second, I recommend 30, 50 or 60
            """
            self.max_fps = max_fps
            self.first_time_reading = 0.0
        
        def code_start_point(self):
            """
            Put this at the beggining of your program's While (main)loop.
            Reads time when it starts.
            """
            self.first_time_reading = time.time()
        
        def code_end_point_limit_framerate(self):
            """
            Put this at the end of your program's While (main)loop.
            Waits until proper amount of time since code_start_point passed to ensure the top speed.
            """
            wait = 1 / self.max_fps
            while True:
                current_time = time.time()
                if current_time - self.first_time_reading >= wait:
                    break



    #3D Objects:
                
    class Cube:
        """
        3D cube object, left for compatibility.
        Since you can create cubes with RectangularPrism, only it will be getting updates.
        """
        def __init__(self, size=1, position=(0, 0, 0), rotation=(0, 0, 0), rotation_speed=(0, 0, 0),
                     color_sides=False, frame_color=(1, 1, 1, 1),
                     color_front=(1, 1, 1, 1), color_back=(1, 1, 1, 1), color_left=(1, 1, 1, 1),
                     color_right=(1, 1, 1, 1), color_top=(1, 1, 1, 1), color_bottom=(1, 1, 1, 1)):
            self.size = size
            self.position = list(position)  # Ensure it's always a list
            self.rotation = list(rotation)  # (pitch, yaw, roll) angles
            self.rotation_speed = list(rotation_speed)  # Speed of rotation for each axis
            self.color_sides = color_sides
            self.frame_color = frame_color
            colors = {
                "front": color_front,
                "back": color_back,
                "left": color_left,
                "right": color_right,
                "top": color_top,
                "bottom": color_bottom,
            }
            self.colors = colors

        def translate(self, x_velocity=0, y_velocity=0, z_velocity=0):
            """Smoothly translates the cube in the 3D space."""
            self.position[0] += x_velocity
            self.position[1] += y_velocity
            self.position[2] += z_velocity

        def rotate(self, delta_pitch=0, delta_yaw=0, delta_roll=0):
            """Smoothly rotates the cube by specified angles."""
            self.rotation[0] += delta_pitch
            self.rotation[1] += delta_yaw
            self.rotation[2] += delta_roll

        def update_rotation(self):
            """Automatically rotates the cube using its rotation_speed."""
            self.rotation[0] += self.rotation_speed[0]
            self.rotation[1] += self.rotation_speed[1]
            self.rotation[2] += self.rotation_speed[2]

        def draw(self):
            """Draws the cube at its current position and with its current rotation."""
            half_size = self.size / 2
            vertices = [
                # Front face
                (half_size, -half_size, -half_size),
                (half_size, half_size, -half_size),
                (-half_size, half_size, -half_size),
                (-half_size, -half_size, -half_size),
                # Back face
                (half_size, -half_size, half_size),
                (half_size, half_size, half_size),
                (-half_size, -half_size, half_size),
                (-half_size, half_size, half_size),
            ]

            if self.color_sides:
                faces = [
                    (0, 1, 2, 3),  # Front face
                    (3, 2, 7, 6),  # Back face
                    (0, 3, 6, 4),  # Left face
                    (1, 5, 7, 2),  # Right face
                    (4, 5, 1, 0),  # Bottom face
                    (5, 4, 6, 7),  # Top face
                ]
            else:
                faces = [
                    (0, 1), (1, 2), (2, 3), (3, 0),
                    (4, 5), (5, 7), (7, 6), (6, 4),
                    (0, 4), (1, 5), (2, 7), (3, 6)
                ]

            color_mapping = {
                0: self.colors["front"],
                1: self.colors["top"],
                2: self.colors["left"],
                3: self.colors["right"],
                4: self.colors["bottom"],
                5: self.colors["back"]
            }

            glPushMatrix()
            glTranslatef(*self.position)
            glRotatef(self.rotation[0], 1, 0, 0)  # Pitch
            glRotatef(self.rotation[1], 0, 1, 0)  # Yaw
            glRotatef(self.rotation[2], 0, 0, 1)  # Roll

            glEnable(GL_BLEND)
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

            if self.color_sides:
                glBegin(GL_QUADS)
            else:
                glBegin(GL_LINES)

            for i, face in enumerate(faces):
                if self.color_sides:
                    if i < 6:  # Apply color mapping to faces
                        glColor4fv(color_mapping[i])
                    else:
                        glColor4fv(self.frame_color)
                else:
                    glColor4fv(self.frame_color)

                for vertex in face:
                    glVertex3fv(vertices[vertex])

            glEnd()
            glDisable(GL_BLEND)
            glPopMatrix()

        def check_collision(self, other):
            """
            Checks if this object collides with another object using AABB.
            :param other: Another object with a position and size/dimensions.
            :return: True if there is a collision, False otherwise.
            """
            if (abs(self.position[0] - other.position[0]) < (self.size / 2 + other.size / 2) and
                abs(self.position[1] - other.position[1]) < (self.size / 2 + other.size / 2) and
                abs(self.position[2] - other.position[2]) < (self.size / 2 + other.size / 2)):
                return True
            return False
                

    class RectangularPrism:
        """
        A 3D rectangular prism object.
        """
        def __init__(self, width=1, height=1, depth=1, position=(0, 0, 0), rotation=(0, 0, 0),
                     color_sides=False, frame_color=(1, 1, 1, 1),
                     color_front=(1, 1, 1, 1), color_back=(1, 1, 1, 1), color_left=(1, 1, 1, 1),
                     color_right=(1, 1, 1, 1), color_top=(1, 1, 1, 1), color_bottom=(1, 1, 1, 1)):
            """
            :param width: Width
            :param height: Height
            :param depth: Depth
            :param position: Position in 3D space (for example (0,0,0))
            :param rotation: Initial rotation in 3D space (for example (0,0,0))
            :param color_sides: If False, use frame_color to set color of the frame. Otherwise, the other arguments will be used.
            All color arguments expect a tuple with 4 numbers (Red, Green, Blue, Transparency).
            """
            self.width = width
            self.height = height
            self.depth = depth
            self.position = list(position)  
            self.rotation = list(rotation)  # (pitch, yaw, roll) angles
            self.rotation_speed = [0,0,0]  
            self.color_sides = color_sides
            self.frame_color = frame_color
            colors = {
                "front": color_front,
                "back": color_back,
                "left": color_left,
                "right": color_right,
                "top": color_top,
                "bottom": color_bottom,
            }
            self.colors = colors

        def translate(self, x_velocity=0, y_velocity=0, z_velocity=0):
            """Smoothly translates the prism in the 3D space."""
            self.position[0] += x_velocity
            self.position[1] += y_velocity
            self.position[2] += z_velocity

        def rotate(self, delta_pitch=0, delta_yaw=0, delta_roll=0):
            """Smoothly rotates the prism by specified angles."""
            self.rotation[0] += delta_pitch
            self.rotation[1] += delta_yaw
            self.rotation[2] += delta_roll

        def update_rotation(self):
            """Automatically rotates the prism using its rotation_speed."""
            self.rotation[0] += self.rotation_speed[0]
            self.rotation[1] += self.rotation_speed[1]
            self.rotation[2] += self.rotation_speed[2]

        def draw(self):
            """Draws the prism at its current position and with its current rotation."""
            half_width = self.width / 2
            half_height = self.height / 2
            half_depth = self.depth / 2
            vertices = [
                # Front face
                (half_width, -half_height, -half_depth),
                (half_width, half_height, -half_depth),
                (-half_width, half_height, -half_depth),
                (-half_width, -half_height, -half_depth),
                # Back face
                (half_width, -half_height, half_depth),
                (half_width, half_height, half_depth),
                (-half_width, -half_height, half_depth),
                (-half_width, half_height, half_depth),
            ]

            if self.color_sides:
                faces = [
                    (0, 1, 2, 3),  # Front face
                    (3, 2, 7, 6),  # Back face
                    (0, 3, 6, 4),  # Left face
                    (1, 5, 7, 2),  # Right face
                    (4, 5, 1, 0),  # Bottom face
                    (5, 4, 6, 7),  # Top face
                ]
            else:
                faces = [
                    (0, 1), (1, 2), (2, 3), (3, 0),
                    (4, 5), (5, 7), (7, 6), (6, 4),
                    (0, 4), (1, 5), (2, 7), (3, 6)
                ]

            color_mapping = {
                0: self.colors["front"],
                1: self.colors["top"],
                2: self.colors["left"],
                3: self.colors["right"],
                4: self.colors["bottom"],
                5: self.colors["back"]
            }

            glPushMatrix()
            glTranslatef(*self.position)
            glRotatef(self.rotation[0], 1, 0, 0)  # Pitch
            glRotatef(self.rotation[1], 0, 1, 0)  # Yaw
            glRotatef(self.rotation[2], 0, 0, 1)  # Roll

            glEnable(GL_BLEND)
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

            if self.color_sides:
                glBegin(GL_QUADS)
            else:
                glBegin(GL_LINES)

            for i, face in enumerate(faces):
                if self.color_sides:
                    if i < 6:  # Apply color mapping to faces
                        glColor4fv(color_mapping[i])
                    else:
                        glColor4fv(self.frame_color)
                else:
                    glColor4fv(self.frame_color)

                for vertex in face:
                    glVertex3fv(vertices[vertex])

            glEnd()
            glDisable(GL_BLEND)
            glPopMatrix()
            
        def check_collision(self, other):
            """
            Checks if this object collides with another object using AABB.
            :param other: Another object with a position and size/dimensions.
            :return: True if there is a collision, False otherwise.
            """
            if (abs(self.position[0] - other.position[0]) < (self.size / 2 + other.size / 2) and
                abs(self.position[1] - other.position[1]) < (self.size / 2 + other.size / 2) and
                abs(self.position[2] - other.position[2]) < (self.size / 2 + other.size / 2)):
                return True
            return False


    '''class Model3D_VeryLowPolyOneTexture:
        def __init__(self, obj_path, texture_path=None, mtl_path=None, position=(0, 0, 0), scale=100, rotation=(0, 0, 0), rotation_speed=(0, 0, 0)):
            """
            A class to load and render 3D models from .obj files with .mtl support and optional texture.
            :param obj_path: Path to the .obj file.
            :param texture_path: Path to a default texture image (overridden by .mtl if specified).
            :param position: Initial 3D position of the model (x, y, z).
            :param scale: Scaling factor in percentage (default is 100%).
            :param rotation: Initial rotation angles (pitch, yaw, roll).
            :param rotation_speed: Rotation speed for each axis.
            """
            self.obj_path = obj_path
            if mtl_path != None:
                self.mtl_path = mtl_path
            else:
                self.mtl_path = obj_path.replace(".obj", ".mtl")  # Default .mtl path
            self.texture_path = texture_path
            self.position = list(position)
            self.rotation = list(rotation)
            self.rotation_speed = list(rotation_speed)
            self.scale = scale / 100.0  # Convert percentage to a scaling factor

            # Data storage
            self.vertices = []
            self.normals = []
            self.tex_coords = []
            self.faces_with_materials = []
            self.materials = {}
            self.texture_id = None

            # Load model, materials, and texture
            self.load_model()
            if os.path.exists(self.mtl_path):
                self.load_mtl()
            if self.texture_path and os.path.exists(self.texture_path):
                self.load_texture()

        def load_model(self):
            """
            Parses the .obj file and stores vertex, normal, texture coordinate, and face data.
            Associates faces with materials (if specified).
            """
            with open(self.obj_path, "r") as file:
                current_material = None
                for line in file:
                    parts = line.strip().split()
                    if not parts or parts[0].startswith("#"):
                        continue
                    if parts[0] == "v":  # Vertex
                        self.vertices.append([float(x) for x in parts[1:4]])
                    elif parts[0] == "vn":  # Normal
                        self.normals.append([float(x) for x in parts[1:4]])
                    elif parts[0] == "vt":  # Texture coordinate
                        self.tex_coords.append([float(x) for x in parts[1:3]])
                    elif parts[0] == "usemtl":  # Material usage
                        current_material = parts[1]
                    elif parts[0] == "f":  # Face
                        face = []
                        for vertex in parts[1:]:
                            vertex_data = vertex.split("/")
                            vertex_index = int(vertex_data[0]) - 1
                            texture_index = int(vertex_data[1]) - 1 if len(vertex_data) > 1 and vertex_data[1] else None
                            normal_index = int(vertex_data[2]) - 1 if len(vertex_data) > 2 and vertex_data[2] else None
                            face.append((vertex_index, texture_index, normal_index))
                        self.faces_with_materials.append((face, current_material))


        def load_texture(self, texture_path=None):
            """
            Loads a texture image from the specified path.
            If no path is provided, defaults to the texture_path set in the constructor.
            """
            if not texture_path:
                texture_path = self.texture_path
            if not texture_path or not os.path.exists(texture_path):
                return

            img = Image.open(texture_path)
            img_data = np.array(img.convert("RGBA"), dtype=np.uint8)

            self.texture_id = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, self.texture_id)

            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, img.width, img.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
            glBindTexture(GL_TEXTURE_2D, 0)

        def load_mtl(self):
            """
            Parses the .mtl file and extracts material definitions.
            """
            with open(self.mtl_path, "r") as file:
                current_material = None
                for line in file:
                    parts = line.strip().split()
                    if not parts or parts[0].startswith("#"):
                        continue
                    if parts[0] == "newmtl":  # Start a new material
                        current_material = parts[1]
                        self.materials[current_material] = {
                            "Ka": [0.0, 0.0, 0.0],  # Ambient color
                            "Kd": [0.5, 0.5, 0.5],  # Diffuse color
                            "Ks": [0.5, 0.5, 0.5],  # Specular color
                            "map_Kd": None,  # Diffuse texture map
                        }
                    elif current_material:
                        if parts[0] == "Ka":  # Ambient color
                            self.materials[current_material]["Ka"] = [float(x) for x in parts[1:4]]
                        elif parts[0] == "Kd":  # Diffuse color
                            self.materials[current_material]["Kd"] = [float(x) for x in parts[1:4]]
                        elif parts[0] == "Ks":  # Specular color
                            self.materials[current_material]["Ks"] = [float(x) for x in parts[1:4]]
                        elif parts[0] == "map_Kd":  # Diffuse texture map
                            self.materials[current_material]["map_Kd"] = parts[1]
                            # Load texture if specified in .mtl
                            texture_path = os.path.join(os.path.dirname(self.mtl_path), parts[1])  # Full path
                            self.load_texture(texture_path)
                            #print(f"Loaded texture: {texture_path}")



        def draw(self):
            """
            Renders the 3D model with materials and textures applied.
            """
            glPushMatrix()
            glTranslatef(*self.position)
            glRotatef(self.rotation[0], 1, 0, 0)  # Pitch
            glRotatef(self.rotation[1], 0, 1, 0)  # Yaw
            glRotatef(self.rotation[2], 0, 0, 1)  # Roll
            glScalef(self.scale, self.scale, self.scale)

            for face, material in self.faces_with_materials:
                if material:
                    mat = self.materials.get(material, {})

                    # Apply material properties if defined
                    if "Ka" in mat:  # Ambient color
                        glMaterialfv(GL_FRONT, GL_AMBIENT, mat["Ka"])
                    if "Kd" in mat:  # Diffuse color
                        glMaterialfv(GL_FRONT, GL_DIFFUSE, mat["Kd"])
                    if "Ks" in mat:  # Specular color
                        glMaterialfv(GL_FRONT, GL_SPECULAR, mat["Ks"])

                    # Handle texture loading and application
                    if "map_Kd" in mat and mat["map_Kd"]:
                        texture_path = os.path.join(os.path.dirname(self.mtl_path), mat["map_Kd"])
                        if self.texture_id is None:  # Load texture only if it's not already loaded
                            self.load_texture(texture_path)
                            #print(f"Loaded texture: {texture_path}")

                        if self.texture_id:
                            glEnable(GL_TEXTURE_2D)  # Enable texture if texture exists
                            glBindTexture(GL_TEXTURE_2D, self.texture_id)  # Bind the loaded texture
                        else:
                            glDisable(GL_TEXTURE_2D)  # Disable texture if no texture found
                    else:
                        glDisable(GL_TEXTURE_2D)  # Disable texture if no texture map is provided

                else:
                    # Disable textures if no material is found
                    glDisable(GL_TEXTURE_2D)

                # Draw the faces
                glBegin(GL_TRIANGLES)
                for vertex_index, texture_index, normal_index in face:
                    if texture_index is not None and self.tex_coords:
                        glTexCoord2fv(self.tex_coords[texture_index])  # Apply texture coordinates if available
                    if normal_index is not None and self.normals:
                        glNormal3fv(self.normals[normal_index])  # Apply normals if available
                    if vertex_index is not None:
                        glVertex3fv(self.vertices[vertex_index])  # Apply vertex position
                glEnd()

                # Unbind texture after rendering each face
                if self.texture_id:
                    glBindTexture(GL_TEXTURE_2D, 0)  # Unbind texture
                    glDisable(GL_TEXTURE_2D)  # Disable texture

            glPopMatrix()



        def translate(self, x_velocity=0, y_velocity=0, z_velocity=0):
            """Translates the model by the specified velocity."""
            self.position[0] += x_velocity
            self.position[1] += y_velocity
            self.position[2] += z_velocity

        def rotate(self, delta_pitch=0, delta_yaw=0, delta_roll=0):
            """Rotates the model by the specified angles."""
            self.rotation[0] += delta_pitch
            self.rotation[1] += delta_yaw
            self.rotation[2] += delta_roll

        def update_rotation(self):
            """Automatically rotates the model using its rotation speed."""
            self.rotation[0] += self.rotation_speed[0]
            self.rotation[1] += self.rotation_speed[1]
            self.rotation[2] += self.rotation_speed[2]
    '''

    class Model3D_STL:
        def __init__(self, stl_path, texture_path=None, color=(1, 1, 1, 1),
                     position=(0, 0, 0), scale=100.0, rotation=(0, 0, 0)):
            """
            Loads and renders a 3D model from an STL file with optional texture or plain color.
            :param stl_path: Path to the .STL 3D model file
            :param texture_path: Path to texture image file to use, set None for plain color.
            :param color: Plain color to use if there is no image texture used.
            :param position: X Y Z position in the world, tuple.
            :param scale: Scale of the rendered 3D model in %
            :param rotation: Tuple determining how to rotate the 3D model in degrees.
            """
            self.stl_path = stl_path
            self.texture_path = texture_path
            self.color = color
            self.position = list(position)
            self.scale = scale / 100.0
            self.rotation = list(rotation)
            self.vertices = []
            self.normals = []
            self.faces = []
            self.texture_coords = []  
            self.texture_id = None

            self.load_model()
            self.generate_texture_coordinates()
            self.create_buffers()
            if self.texture_path and os.path.exists(self.texture_path):
                self.load_texture()

        def load_model(self):
            """
            Parses the STL file and extracts vertices and faces.
            Supports both ASCII and binary STL formats.
            """
            try:
                with open(self.stl_path, 'rb') as file:
                    header = file.read(80)
                    try:
                        num_triangles = struct.unpack('<I', file.read(4))[0]
                        for _ in range(num_triangles):
                            data = file.read(50)  # 12 floats: normal (3), vertices (9), 2-byte attribute
                            if len(data) < 50:
                                break
                            unpacked = struct.unpack('<12fH', data)
                            normal = unpacked[0:3]
                            v1 = unpacked[3:6]
                            v2 = unpacked[6:9]
                            v3 = unpacked[9:12]
                            self.normals.append(self.normalize_vector(normal))
                            self.faces.append((len(self.vertices), len(self.vertices) + 1, len(self.vertices) + 2))
                            self.vertices.extend([v1, v2, v3])
                    except struct.error:
                        # ASCII STL handling
                        file.seek(0)
                        content = file.read().decode('utf-8', errors='ignore')
                        sio = StringIO(content)
                        current_normal = None
                        for line in sio:
                            parts = line.strip().split()
                            if not parts:
                                continue
                            if parts[0] == 'facet' and parts[1] == 'normal':
                                current_normal = self.normalize_vector(list(map(float, parts[2:5])))
                            elif parts[0] == 'vertex':
                                vertex = list(map(float, parts[1:4]))
                                self.vertices.append(vertex)
                            elif parts[0] == 'endfacet':
                                if len(self.vertices) >= 3:
                                    idx = len(self.vertices) - 3
                                    self.faces.append((idx, idx + 1, idx + 2))
                                    self.normals.append(current_normal)
            except Exception as e:
                raise SystemExit(f"Failed to load STL file '{self.stl_path}': {e}")

        def normalize_vector(self, vector):
            """Normalize a 3D vector to unit length."""
            length = math.sqrt(sum(coord ** 2 for coord in vector))
            if length > 0:
                return [coord / length for coord in vector]
            return vector

        def generate_texture_coordinates(self):
            """
            Generates UV texture coordinates for the model.
            Maps vertices to a normalized space using the bounding box.
            """
            if not self.vertices:
                raise ValueError("No vertices found. Ensure the model is loaded before generating texture coordinates.")

            min_x = min(vertex[0] for vertex in self.vertices)
            max_x = max(vertex[0] for vertex in self.vertices)
            min_y = min(vertex[1] for vertex in self.vertices)
            max_y = max(vertex[1] for vertex in self.vertices)

            for vertex in self.vertices:
                u = (vertex[0] - min_x) / (max_x - min_x) if max_x != min_x else 0
                v = (vertex[1] - min_y) / (max_y - min_y) if max_y != min_y else 0
                self.texture_coords.append((u, v))

        def create_buffers(self):
            """
            Creates Vertex Buffer Objects (VBOs) for efficient rendering.
            """
            vertex_data = []
            for i, vertex in enumerate(self.vertices):
                u, v = self.texture_coords[i]
                vertex_data.extend([*vertex, u, v])  # Add position and UV

            vertex_data = np.array(vertex_data, dtype=np.float32)
            index_data = np.array([index for face in self.faces for index in face], dtype=np.uint32)

            self.vertex_vbo = vbo.VBO(vertex_data)
            self.index_vbo = vbo.VBO(index_data, target=GL_ELEMENT_ARRAY_BUFFER)

        def load_texture(self):
            """
            Loads a texture image and binds it for OpenGL rendering.
            """
            try:
                img = Image.open(self.texture_path).convert("RGBA")
                img_data = img.tobytes("raw", "RGBA", 0, -1)
                self.texture_id = glGenTextures(1)
                glBindTexture(GL_TEXTURE_2D, self.texture_id)

                glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, img.width, img.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)

                glGenerateMipmap(GL_TEXTURE_2D)
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

                glBindTexture(GL_TEXTURE_2D, 0)
            except Exception as e:
                self.texture_id = None
                #print(f"Failed to load texture: {e}")

        def draw(self):
            """
            Renders the STL model with texture or plain color.
            """
            glPushMatrix()
            glTranslatef(*self.position)
            glScalef(self.scale, self.scale, self.scale)
            glRotatef(self.rotation[0], 1, 0, 0)
            glRotatef(self.rotation[1], 0, 1, 0)
            glRotatef(self.rotation[2], 0, 0, 1)

            if self.texture_id:
                glEnable(GL_TEXTURE_2D)
                glBindTexture(GL_TEXTURE_2D, self.texture_id)

            self.vertex_vbo.bind()
            glEnableClientState(GL_VERTEX_ARRAY)
            glEnableClientState(GL_TEXTURE_COORD_ARRAY)

            glVertexPointer(3, GL_FLOAT, 20, self.vertex_vbo)
            glTexCoordPointer(2, GL_FLOAT, 20, self.vertex_vbo + 12)

            self.index_vbo.bind()
            glDrawElements(GL_TRIANGLES, len(self.faces) * 3, GL_UNSIGNED_INT, None)

            self.vertex_vbo.unbind()
            self.index_vbo.unbind()
            glDisableClientState(GL_VERTEX_ARRAY)
            glDisableClientState(GL_TEXTURE_COORD_ARRAY)

            if self.texture_id:
                glBindTexture(GL_TEXTURE_2D, 0)
                glDisable(GL_TEXTURE_2D)

            glPopMatrix()

        def translate(self, dx=0, dy=0, dz=0):
            """Translates the model by the specified deltas."""
            self.position[0] += dx
            self.position[1] += dy
            self.position[2] += dz

        def rotate(self, delta_pitch=0, delta_yaw=0, delta_roll=0):
            """Rotates the model by the specified angles."""
            self.rotation[0] += delta_pitch
            self.rotation[1] += delta_yaw
            self.rotation[2] += delta_roll

        def update_rotation(self):
            """Applies continuous rotation based on current rotation angles."""
            self.rotate()



    #2D Objects:
    
    class Rectangle_2D:
        """Represents a rectangle object for 2D rendering using OpenGL."""
        def __init__(self, x, y, width, height, fill_color, frame_color=None, frame_width=1):
            """
            Initialize the Rectangle with x, y coordinates, width, height, fill color,
            and optional frame color and width.

            :param x: X-coordinate of the top-left corner.
            :param y: Y-coordinate of the top-left corner.
            :param width: Width of the rectangle.
            :param height: Height of the rectangle.
            :param fill_color: Tuple representing RGBA color (0-1 range).
            :param frame_color: Tuple representing RGBA frame color (0-1 range), optional.
            :param frame_width: Width of the frame line, optional.
            """
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            self.fill_color = fill_color  # Expected to be a tuple with values in [0,1]
            self.frame_color = frame_color  # Expected to be a tuple with values in [0,1] or None
            self.frame_width = frame_width
            
        def move(self,x,y):
            self.x += x
            self.y += y
            
        def setlocation(self,x,y):
            self.x=x
            self.y=y
            
        def draw(self, app):
            """Draw the rectangle using OpenGL."""
            
            app.draw_rectangle_2d((self.x, self.y, self.width, self.height), self.fill_color)

            if self.frame_color and self.frame_width > 0:
                glLineWidth(self.frame_width)
                glColor4f(*self.frame_color)
                glBegin(GL_LINE_LOOP)
                glVertex2f(self.x, self.y)
                glVertex2f(self.x + self.width, self.y)
                glVertex2f(self.x + self.width, self.y + self.height)
                glVertex2f(self.x, self.y + self.height)
                glEnd()
                

    
    class Circle_2D:
        """Represents a circle object for 2D rendering using OpenGL."""
        def __init__(self, x, y, radius, fill_color, frame_color=None, frame_width=1, segments=32):
            """
            Initialize the Circle with x, y coordinates, radius, fill color,
            and optional frame color and width.

            :param x: X-coordinate of the center.
            :param y: Y-coordinate of the center.
            :param radius: Radius of the circle.
            :param fill_color: Tuple representing RGBA color (0-1 range).
            :param frame_color: Tuple representing RGBA frame color (0-1 range), optional.
            :param frame_width: Width of the frame line, optional.
            :param segments: Number of segments to approximate the circle.
            """
            self.x = x
            self.y = y
            self.radius = radius
            self.fill_color = fill_color  # Expected to be a tuple with values in [0,1]
            self.frame_color = frame_color  # Expected to be a tuple with values in [0,1] or None
            self.frame_width = frame_width
            self.segments = segments
            
        def move(self,x,y):
            self.x += x
            self.y += y
            
        def setlocation(self,x,y):
            self.x=x
            self.y=y
            
        def draw(self, app):
            """Draw the circle using OpenGL."""
            
            app.draw_circle_2d(self, self.segments)

            if self.frame_color and self.frame_width > 0:
                glLineWidth(self.frame_width)
                glColor4f(*self.frame_color)
                glBegin(GL_LINE_LOOP)
                for i in range(self.segments):
                    angle = 2 * math.pi * i / self.segments
                    glVertex2f(self.x + math.cos(angle) * self.radius, self.y + math.sin(angle) * self.radius)
                glEnd()
    
    
    class Image_2D:
        """Represents an image object for 2D rendering using OpenGL."""
        def __init__(self, image_path, x, y, width=None, height=None, rotation=0):
            """
            Initialize the Image with the image path, position, and optional dimensions.

            :param image_path: Path to the image file.
            :param x: X-coordinate of the top-left corner.
            :param y: Y-coordinate of the top-left corner.
            :param width: Width to scale the image to, optional.
            :param height: Height to scale the image to, optional.
            :param rotation: Rotate image within its rendering zone.
            """
            self.image_path = image_path
            self.x = x
            self.y = y

            try:
                image = pygame.image.load(image_path).convert_alpha()
            except pygame.error as e:
                #print(f"Failed to load image {image_path}: {e}")
                raise SystemExit(e)
            image = pygame.transform.rotate(image, 180 + rotation)
        
            if width and height:
                image = pygame.transform.scale(image, (width, height))
                self.width = width
                self.height = height
            else:
                self.width, self.height = image.get_size()

            image_data = pygame.image.tostring(image, "RGBA", True)

            # Generate an OpenGL texture ID
            self.texture_id = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, self.texture_id)

            # Set texture parameters
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)  # or GL_NEAREST
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)  # or GL_NEAREST

            # Upload the texture data to OpenGL
            glTexImage2D(
                GL_TEXTURE_2D,
                0,
                GL_RGBA,
                self.width,
                self.height,
                0,
                GL_RGBA,
                GL_UNSIGNED_BYTE,
                image_data
            )

            glBindTexture(GL_TEXTURE_2D, 0)  # Unbind the texture
            
        def move(self,x,y):
            self.x += x
            self.y += y
            
        def setlocation(self,x,y):
            self.x=x
            self.y=y
            
        def draw(self, app):
            """Draw the image as a textured quad using OpenGL."""
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, self.texture_id)
            glColor4f(1, 1, 1, 1)  # Set color to white to display texture as-is

            glBegin(GL_QUADS)
            glTexCoord2f(0, 0)
            glVertex2f(self.x, self.y)

            glTexCoord2f(1, 0)
            glVertex2f(self.x + self.width, self.y)

            glTexCoord2f(1, 1)
            glVertex2f(self.x + self.width, self.y + self.height)

            glTexCoord2f(0, 1)
            glVertex2f(self.x, self.y + self.height)
            glEnd()

            glBindTexture(GL_TEXTURE_2D, 0)
            glDisable(GL_TEXTURE_2D)


    #2D rendering methods
            
            
    def set_perspective(self):
        """Set up the perspective projection for 3D rendering."""
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(self.camera.fov, (self.window_size_x / self.window_size_y), self.camera.min_render_distance, self.camera.max_render_distance)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        self.camera.setup_perspective()

    def set_orthographic(self):
        """Set up an orthographic projection for 2D rendering."""
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()  # Save current projection matrix
        glLoadIdentity()
        gluOrtho2D(0, self.window_size_x, self.window_size_y, 0)  # Top-left corner is (0,0)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()  # Save current modelview matrix
        glLoadIdentity()

    def reset_projection(self):
        """Reset to the previous projection and modelview matrices."""
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        glPopMatrix()

    def draw_rectangle_2d(self, rect, color):
        """
        Draw a 2D rectangle using OpenGL primitives.

        :param rect: Tuple (x, y, width, height).
        :param color: Tuple (r, g, b, a) with values in [0,1].
        """
        x, y, width, height = rect
        r, g, b, a = color
        glColor4f(r, g, b, a)
        glBegin(GL_QUADS)
        glVertex2f(x, y)
        glVertex2f(x + width, y)
        glVertex2f(x + width, y + height)
        glVertex2f(x, y + height)
        glEnd()

    def draw_circle_2d(self, circle, segments=32):
        """
        Draw a filled 2D circle using OpenGL.

        :param circle: Instance of Circle_2D class.
        :param segments: Number of segments to approximate the circle.
        """
        glColor4f(*circle.fill_color)
        glBegin(GL_TRIANGLE_FAN)
        glVertex2f(circle.x, circle.y)  # Center of circle
        for i in range(segments + 1):
            angle = 2 * math.pi * i / segments
            glVertex2f(circle.x + math.cos(angle) * circle.radius, circle.y + math.sin(angle) * circle.radius)
        glEnd()

    def render_2d_objects(self, object_list):
        """
        Render 2D objects using OpenGL. Should be called after rendering 3D objects.

        :param object_list: List of 2D objects (Rectangle_2D, Circle_2D, Image_2D, etc.).
        """
        self.set_orthographic()  # Switch to orthographic projection

        # Disable depth testing to ensure 2D UI elements are rendered on top
        glDisable(GL_DEPTH_TEST)

        for obj in object_list:
            if hasattr(obj, 'draw'):
                obj.draw(self)  # Pass the app instance to the draw method
            else:
                print(f"Warning: Object {obj} does not have a 'draw' method.")

        # Re-enable depth testing if it was enabled
        if self.depth_testing_enabled:
            glEnable(GL_DEPTH_TEST)

        self.reset_projection()  # Switch back to perspective projection
        
    #Audio:
       
    class SoundManager:
        """
        Allows to use and control audio in your program.
        Currently, it's just primitive audio playback, without support for audio within 3D space.
        """
        def __init__(self, channel_amount=8):
            """
            Initializes the Pygame mixer and creates dictionaries to store sounds, their playing status, and whether they should loop.
            :param channel_amount: Set how many PyGame audio channels to create, default 8.
            """
            pygame.mixer.init()
            self.sounds = {}
            self.is_playing = {}
            self.loop = {}
            self.channels = [pygame.mixer.Channel(i) for i in range(channel_amount)]
            self.channel_amount = channel_amount
        def add_sound_to_memory(self, name: str, file_path: str, loop=False):
            """
            Adds a new sound to the manager.
            
            
            :param name: The name of the sound, string. Any you want.
            :param file_path: The file path of the sound file, use whatever format PyGame and your system support.
            :param loop: Whether the sound should loop (for example background music) or not (for example sound effect), bool.
            """
            self.sounds[name] = pygame.mixer.Sound(file_path)
            self.is_playing[name] = False
            self.loop[name] = loop

        def play_sound(self, name: str):
            """
            Plays the specified sound.
            :param name: The name of the sound to play.
            """
            if not self.is_playing[name]:
                for channel in self.channels:
                    if not channel.get_busy():
                        channel.play(self.sounds[name], -1 if self.loop[name] else 0)
                        self.is_playing[name] = True
                        break

        def stop_sound(self, name:str):
            """
            Stops the specified sound.
            :param name (str): The name of the sound to stop.
            """
            for channel in self.channels:
                if channel.get_busy() and channel.get_sound() == self.sounds[name]:
                    channel.stop()
                    self.is_playing[name] = False
                    break

        def update(self):
            """
            Updates the playing status of the sounds.
            Checks if any of the sounds that are currently playing have finished playing, and if so, sets their playing status to False.
            """
            for name, is_playing in self.is_playing.items():
                if is_playing:
                    found_channel = False
                    for channel in self.channels:
                        if channel.get_busy() and channel.get_sound() == self.sounds[name]:
                            found_channel = True
                            break
                    if not found_channel:
                        self.is_playing[name] = False
