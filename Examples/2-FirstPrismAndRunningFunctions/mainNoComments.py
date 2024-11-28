import RenderBirdCore

r = RenderBirdCore.RenderBirdCore(1280, 720, "Example 2")

fpslimit = r.FPS_Limiter(50)

r.set_background_color(176, 196, 222)

cube = r.RectangularPrism(width=1, depth=1, position=(0, 0, -3), rotation=(30, 30, 30), color_sides=False, frame_color=(255, 0, 0, 1))

#cube = r.RectangularPrism(width=1,depth=1,position=(0,0,-3),rotation=(30,30,30),color_sides=True,color_back=(255,0,0,1),color_bottom=(0,255,0,1),color_front=(0,0,255,1),color_left=(255,0,128,1))

waiting = r.RunAfterTime(5)

def rotate_cube_function():
    cube.rotate(0.1, 0, 0)

while r.running == True:
    fpslimit.code_start_point()
    r.clear_screen()
    
    cube.draw()
    
    waiting.run_after_time(rotate_cube_function)
    
    r.update_display()
    r.handle_close_event_direct()
    fpslimit.code_end_point_limit_framerate()

