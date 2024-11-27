#Hello and welcome to the second example where we will render a cube.

import RenderBirdCore

r = RenderBirdCore.RenderBirdCore(1280, 720, "Example 2")

fpslimit = r.FPS_Limiter(50)

r.set_background_color(176, 196, 222)

#Let's define object that will be our cube:
cube = r.RectangularPrism(width=1,depth=1,position=(0,0,-3),rotation=(30,30,30),rotation_speed=(0,0,0),color_sides=False,frame_color=(255,0,0,1))
#Here we created a prism at position XYZ 0,0,-3, rotated 30 degrees in all angles, and with a red frame and no solid sides.
#Keep argument rotation_speed as (0,0,0), it is sadly broken. Sorry!

#Anyway, to render a cube with filled sides, let's set color_sides to True.
#Uncomment the line below to use such a cube instead:
cube = r.RectangularPrism(width=1,depth=1,position=(0,0,-3),rotation=(30,30,30),rotation_speed=(0,0,0),color_sides=True,color_back=(255,0,0,1),color_bottom=(0,255,0,1),color_front=(0,0,255,1),color_left=(255,0,128,1))

#Let's define an RunAfterTime object, we will use it later.
waiting = r.RunAfterTime(5) #It is set to do something after 5 seconds since its initalization.

#Let's define a function that will rotate the cube, RunAfterTime will need it.
def rotate_cube_function():
    cube.rotate(0.1,0,0)

while r.running == True:
    fpslimit.code_start_point()
    r.clear_screen()
    
    #Use draw() to render the object.
    cube.draw()
    
    #Now let's use the RunAfterTime to make the cube rotate after 5 seconds pass:
    waiting.run_after_time(rotate_cube_function)
    
    r.update_display()
    r.handle_close_event_direct()
    fpslimit.code_end_point_limit_framerate()

#After running this code, you will first see a cube, which will then start slow rotation after 5 seconds.