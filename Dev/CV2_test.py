from RenderBirdCore import *
import cv2
import pygame

from PIL import Image

r = RenderBirdCore(1280, 720, camera_maximum_render_distance=1000)

fpslimit = r.FPS_Limiter(50)

r.set_background_color(176, 196, 222)

#cube = r.RectangularPrism(width=1, depth=1, position=(0, 0, -3), rotation=(30, 30, 30), color_sides=False, frame_color=(255, 0, 0, 1))

cube = r.RectangularPrism(width=1,depth=1,position=(0,0,-3),rotation=(30,30,30),color_sides=True,color_back=(255,0,0,1),color_bottom=(0,255,0,1),color_front=(0,0,255,1),color_left=(255,0,128,1))

waiting = r.RunAfterTime(5)

img = Image.open('text.png')


#imagenormal = r.Image_2D("text.png",100,100,20,40)
rect = r.Rectangle_2D(100,0,10,10,(255,0,255,255))
circ = r.Circle_2D(200,100,30,(1,1,1,255))

cap = cv2.VideoCapture(0)

def rotate_cube_function():
    cube.rotate(0.5, 0, 0)



heart_rotation = [0,0,0]
heart2_rotation = [0,0,0]
heart3_rotation = [0,0,0]

while r.running == True:
    fpslimit.code_start_point()
    r.clear_screen()
    
    
    ret, frame = cap.read()
    
    
    #imagepil = r.Image_2D_PIL(Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)),0,0,200,100)
    heart = r.Model3D_STL("heart.stl",None,(255,0,0,1),(0,0,-10),4,heart_rotation,True,Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
    heart.rotate(0.5,0.5,0.5)
    heart_rotation = heart.rotation
    
    heart2 = r.Model3D_STL("heart.stl",None,(1,1,1,1),(5,0,-10),4,heart_rotation,True,Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
    heart2.rotate(0.5,0.5,0.5)
    heart2_rotation = heart.rotation
    
    heart3 = r.Model3D_STL("heart.stl",None,(1,1,1,1),(-5,0,-10),4,heart_rotation,True,Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
    heart3.rotate(0.5,0.5,0.5)
    heart3_rotation = heart.rotation
    
    print(heart_rotation)
    cube.draw()
    
    waiting.run_after_time(rotate_cube_function)
    
    if r.key_pressed(pygame.K_w): 
        r.camera.move(0,0,0.05) 
    if r.key_pressed(pygame.K_s): 
        r.camera.move(0,0,-0.05) 
    if r.key_pressed(pygame.K_a): 
        r.camera.move(-0.05,0,0) 
    if r.key_pressed(pygame.K_d): 
        r.camera.move(0.05,0,0) 
        
    if r.key_pressed(pygame.K_e): 
        r.camera.move(0,0.05,0) 
    if r.key_pressed(pygame.K_q): 
        r.camera.move(0,-0.05,0) 
    
    if r.key_pressed(pygame.K_UP):
        r.camera.rotate(0.8,0,0)
    if r.key_pressed(pygame.K_DOWN):
        r.camera.rotate(-0.8,0,0)
    if r.key_pressed(pygame.K_LEFT):
        r.camera.rotate(0,-0.8,0)
    if r.key_pressed(pygame.K_RIGHT):
        r.camera.rotate(0,0.8,0)
        
    heart.draw()
    heart2.draw()
    heart3.draw()
    
    r.render_2d_objects([rect, circ])
    #imagepil.draw(r)
    r.update_display()
    r.handle_close_event_direct()
    fpslimit.code_end_point_limit_framerate()

