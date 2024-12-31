from RenderBirdCore import *
from PIL import Image
import pygame

r = RenderBirdCore(1280, 720)

fpslimit = r.FPS_Limiter(50)

r.set_background_color(176, 196, 222)

#cube = r.RectangularPrism(width=1, depth=1, position=(0, 0, -3), rotation=(30, 30, 30), color_sides=False, frame_color=(255, 0, 0, 1))

#cube = r.RectangularPrism(width=1,depth=1,position=(0,0,-3),rotation=(0,0,0),color_sides=True,color_back=(255,0,0,1),color_bottom=(0,255,0,1),color_front=(0,0,255,1),color_left=(255,0,128,1))


cube = r.TexturedRectangularPrism(1,2,1,(0,0,-3),(0,0,0),(0,0,0,255),"tex.bmp",Image.open("text.png"))

waiting = r.RunAfterTime(5)

def rotate_cube_function():
    cube.rotate(0.1, 0, 0)

obiekty = []
x=0
y=0
for i in range(0,1000):
    if x>10:
        y+=1
        x=0
    x+=1
    obiekty.append(r.RectangularPrism(width=1,depth=1,position=(x,y,-3),rotation=(0,0,0),color_sides=True,color_back=(255,0,0,1),color_bottom=(0,255,0,1),color_front=(0,0,255,1),color_left=(255,0,128,1)))

stl = r.Model3D_STL("cube.stl",None,(255,255,0,1),(0,0,-5),1,(0,0,0),1,Image.open("tex.bmp"),1,2,0.5,0.5,0.5)

anticollission = r.PreventMovingInsideObjects(r.camera,[cube,stl])

while r.running == True:
    fpslimit.code_start_point()
    r.clear_screen()
    
    cube.draw()
    #r.render_visible_3d_objects(obiekty)
    
    #waiting.run_after_time(rotate_cube_function)
    
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
        
    #r.camera.use_mouse_camera_controls(r.window_size_x,r.window_size_y,sensitivity=0.2,sensitivity_factor=1,reverse_horizontally=False,reverse_vertically=False,mouse_cursor_visible=True) 
    v = r.camera.forward_vector
    #r.MoveObjectAlongVector(cube,v,0.01)
    #r.RotateObjectToVector(cube,v)
    #print(r.camera.check_collision(cube))
    if anticollission.check_and_correct():
        print(time.time())
    
    stl.draw()
    r.update_display()
    r.handle_close_event_direct()
    fpslimit.code_end_point_limit_framerate()

