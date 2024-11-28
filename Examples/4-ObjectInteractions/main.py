#Welcome to part 4, were I will show how to program interaction with an object.

import RenderBirdCore

import pygame

r = RenderBirdCore.RenderBirdCore(1280, 720, "Example 4")

fpslimit = r.FPS_Limiter(50)

r.set_background_color(176, 196, 222)

#Let's summon the cube more far away
cube = r.RectangularPrism(width=1,depth=1,position=(0,0,-10),rotation=(30,30,30),color_sides=True,color_back=(255,0,0,1),color_bottom=(0,255,0,1),color_front=(0,0,255,1),color_left=(255,0,128,1))

#Let's get rid of the RunAfterTime, it will not be useful in this example.
#waiting = r.RunAfterTime(5)

#Let's define a bool which we will use to turn on rotation of the cube:
rotate_cube = False

def rotate_cube_function():
    #I increased the rotation speed for better effect.
    cube.rotate(1, 0, 0)

while r.running == True:
    fpslimit.code_start_point()
    r.clear_screen()
    
    cube.draw()
    
    #waiting.run_after_time(rotate_cube_function)
    
    #Now let's set up a variable that will be saving whenever we detected the cube in distance of 4 units and tolerance of 10 degrees.
    detected_cube_list = r.camera.detect_objects_in_view([cube],4,10)
    #The function returns list of objects it detected, if they are among those in the list provided as first argument.
    #Since here we are looking for one object, we can look at lenght of the list to determine whenever the cube was detected
    cube_detected = bool(len(detected_cube_list))
    #print(cube_detected) #Uncomment this to see current state in logs.
    
    #Now let's implement logic to start rotation. Let's check whenever r was pressed and cube_detected is true:
    if r.key_pressed(pygame.K_r) and cube_detected == True:
        rotate_cube = True
    if rotate_cube == True:
        rotate_cube_function()
        
    #Now you must fly close to the cube and then press r to start it's rotation.
    
    #Let's also make t button stop the rotation:
    if r.key_pressed(pygame.K_t) and cube_detected == True:
        rotate_cube = False
    
    #Now run the program, fly close to the cube and then press r to make it rotate, or t to make it stop.
        
    #RenderBird also supports detecting collissions between objects, just use this function which returns a bool:
    #new_bool = cube.check_collision(other_object)
    
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

#Now run the program, fly close to the cube and then press r to make it rotate, or t to make it stop.
#For custom 3D model it is recommended to create a invisible RectangularPrism in their location for interaction and collission detection.