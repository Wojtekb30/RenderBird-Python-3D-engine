#Welcome to the first example on how to use RenderBird!
#Here, I will write the base for any RenderBird program.
#You can use it as a good starting point for your projects. Versions without comments will be provided.

#Let's first import RenderBirdCore
import RenderBirdCore

#Now, let's define an instance of it:
r = RenderBirdCore.RenderBirdCore(1280,720,"Example 1")
#I used the 3 major arguments. First is desired window width, then height, then title.
#Next argument would be about rendering mode, which I recommend to keep set to True,
#and all the other initial camera position and rendering distance.

#We shall define any objects (3D models, functional classes etc.) before the loop.

#Let's put FPS limiter here:
fpslimit = r.FPS_Limiter(50) #Let's limit rendering speed to 50 FPS.

#Let's set the background (or if you prefer sky) color to light blue, because why not.
r.set_background_color(176,196,222)

#Let's create a loop for the program. We shall use 'running' bool variable of the class:
while r.running==True:
    #Let's start with beginning method of FPS limiter:
    fpslimit.code_start_point()
    #In the beggining we also must clear screen to make it possible to render new things.
    r.clear_screen()
    
    #Any code then goes here.
    
    #After everything we must use update_display() to actually render anything.
    r.update_display()
    
    #Let's always include this so the program is able to close.
    r.handle_close_event_direct()
    #Alternatively, we can use handle_close_event() to just set 'running' variable to False and thus end the loop this way.
    #We'd have to use safe_close() after and outside the loop tho.
    
    #Finally, let's put this in the end of our code to let the FPS limiter work.
    fpslimit.code_end_point_limit_framerate()
    
#Running this code, you should see a 720x1280 sky blue window titled "Example 1".