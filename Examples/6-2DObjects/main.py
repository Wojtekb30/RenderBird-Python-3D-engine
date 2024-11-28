#Welcome to 6th example on rendering 2D objects.
#So, we often want to see 2D objects on our screen. For UI, in games for displaying health etc.
#Let's implement some then.

import RenderBirdCore

import pygame

r = RenderBirdCore.RenderBirdCore(1280, 720, "Example 6")

fpslimit = r.FPS_Limiter(50)

r.set_background_color(176, 196, 222)

#cube = r.RectangularPrism(width=1, depth=1, position=(0, 0, -3), rotation=(30, 30, 30), color_sides=False, frame_color=(255, 0, 0, 1))

cube = r.RectangularPrism(width=1,depth=1,position=(0,0,-3),rotation=(30,30,30),color_sides=True,color_back=(255,0,0,1),color_bottom=(0,255,0,1),color_front=(0,0,255,1),color_left=(255,0,128,1))

waiting = r.RunAfterTime(5)

#Let's define some 2D objects:
rectangle = r.Rectangle_2D(x=10,y=20,width=30,height=50,fill_color=(128,0,128,1),frame_color=(0,0,0,1),frame_width=2)

circle = r.Circle_2D(x=300,y=100,radius=30,fill_color=(0,255,0,1),frame_color=None,frame_width=0)

picture = r.Image_2D(image_path="rainbow.png", x=80,y=40,width=None,height=128,rotation=0)

def rotate_cube_function():
    cube.rotate(0.1, 0, 0)

while r.running == True:
    fpslimit.code_start_point()
    r.clear_screen()
    
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
        
    #r.camera.use_mouse_camera_controls(r.window_size_x,r.window_size_y,sensitivity=0.2,sensitivity_factor=1,reverse_horizontally=False,reverse_vertially=False,mouse_cursor_visible=True) 
    
    #Let's add some motion to the 2D objects:
    rectangle.move(2,1)
    picture.move(2,0)
    circle.move(0,1.2)
    
    #Now let's render them here:
    r.render_2d_objects([rectangle,circle,picture])
    #To render 2D objects you must use this function and place it right before update_display()
    
    #The 2D objects should now render in view, and eventually fly away.
    
    r.update_display()
    r.handle_close_event_direct()
    fpslimit.code_end_point_limit_framerate()

