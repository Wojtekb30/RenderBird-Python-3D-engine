#Welcome to third example! Here, we shall allow the camera to move and look around.

import RenderBirdCore

#We must import PyGame to be allowed to use its key variables
import pygame

r = RenderBirdCore.RenderBirdCore(1280, 720, "Example 3")

fpslimit = r.FPS_Limiter(50)

r.set_background_color(176, 196, 222)

#cube = r.RectangularPrism(width=1, depth=1, position=(0, 0, -3), rotation=(30, 30, 30), rotation_speed=(0, 0, 0), color_sides=False, frame_color=(255, 0, 0, 1))

#Let's use the fully colored cube now.
cube = r.RectangularPrism(width=1,depth=1,position=(0,0,-3),rotation=(30,30,30),rotation_speed=(0,0,0),color_sides=True,color_back=(255,0,0,1),color_bottom=(0,255,0,1),color_front=(0,0,255,1),color_left=(255,0,128,1))

waiting = r.RunAfterTime(5)

def rotate_cube_function():
    cube.rotate(0.1, 0, 0)

while r.running == True:
    fpslimit.code_start_point()
    r.clear_screen()
    
    cube.draw()
    
    waiting.run_after_time(rotate_cube_function)
    
    #We can use key_pressed to check if a button was clicked.
    #Let's implement moving with WSAD, like in most videogames.
    if r.key_pressed(pygame.K_w): #Press w to...
        r.camera.move(0,0,0.05) #...to fly Forward
    if r.key_pressed(pygame.K_s): #Press s to...
        r.camera.move(0,0,-0.05) #...to fly Backwards
    if r.key_pressed(pygame.K_a): #Press a to...
        r.camera.move(-0.05,0,0) #...to fly Left
    if r.key_pressed(pygame.K_d): #Press d to...
        r.camera.move(0.05,0,0) #...to fly Right
        
    #Let's also add flying up and down:
    if r.key_pressed(pygame.K_e): #If e pressed then...
        r.camera.move(0,0.05,0) #...fly up
    if r.key_pressed(pygame.K_q): #if q pressed...
        r.camera.move(0,-0.05,0) #...fly down
    
    #Now let's also add looking around (camera rotation) with arrow keys:
    if r.key_pressed(pygame.K_UP):
        r.camera.rotate(0.8,0,0)
    if r.key_pressed(pygame.K_DOWN):
        r.camera.rotate(-0.8,0,0)
    if r.key_pressed(pygame.K_LEFT):
        r.camera.rotate(0,-0.8,0)
    if r.key_pressed(pygame.K_RIGHT):
        r.camera.rotate(0,0.8,0)
        
    #We can also add looking around with mouse. Uncomment it to try it out!
    #r.camera.use_mouse_camera_controls(r.window_size_x,r.window_size_y,sensitivity=0.2,sensitivity_factor=1,reverse_horizontally=False,reverse_vertially=False,mouse_cursor_visible=True) 
    
    r.update_display()
    r.handle_close_event_direct()
    fpslimit.code_end_point_limit_framerate()

#Now you should be able to fly around the scene.