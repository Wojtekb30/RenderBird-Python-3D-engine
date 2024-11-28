import RenderBirdCore

import pygame

r = RenderBirdCore.RenderBirdCore(1280, 720, "Example 5")

fpslimit = r.FPS_Limiter(50)

r.set_background_color(176, 196, 222)

heart = r.Model3D_STL(stl_path="heart.stl", texture_path=None, color=(255,0,0,255),position=(0,0,-5),scale=5)

#heart = r.Model3D_STL(stl_path="heart.stl", texture_path="rainbow.png", color=(255,0,0,255),position=(0,0,-5),scale=5)

while r.running == True:
    fpslimit.code_start_point()
    r.clear_screen()
    
    heart.draw()
    heart.rotate(0,0.3,0)
    
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
        
    r.update_display()
    r.handle_close_event_direct()
    fpslimit.code_end_point_limit_framerate()
