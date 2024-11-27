import RenderBirdCore

r = RenderBirdCore.RenderBirdCore(1280, 720, "Example 1")

fpslimit = r.FPS_Limiter(50)

#r.set_background_color(176, 196, 222)

while r.running == True:
    fpslimit.code_start_point()
    r.clear_screen()
    
    # Functional code like events goes here.
    
    r.update_display()
    r.handle_close_event_direct()
    fpslimit.code_end_point_limit_framerate()

