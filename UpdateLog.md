Version 0.1.0:
- First ever version.

Version 0.1.1:
- Removed rotation_speed argument from RectangularPrism because it was unused.
- Changed method name in SoundManager from add_sound to add_sound_to_memory.
- Made Model3D_STL render with image textures without performance loss. I promise to not change already existing method names again btw.

Version 0.1.2: 
- Fixed Model3D_STL to be able to render in plain color if no texture image file is provided.

Version 0.1.3:
- Fixed collission detection of RectangularPrism.
- Fixed 2D image rendering.
- Set version to 0.1.3 within the code itself, I forgot to update it earlier.
- Added methods for color normalization and de-normalization.
- Added mouse cursor detection method for 2D objects.
- Added variant of 2D image which is loaded from a PIL Image variable not file.
- Model3D_STL now supports texture from a PIL image variable too.
- Fixed use_mouse_camera_controls() method of the Camera which allows to look around with mouse, like in first-person videogames.

Version 0.1.4:
- Added class PreventMovingInsideObjects which allows to prevent an object from moving inside (clipping into) another objects. This includes the camera.
- Camera now has collission detection and a hitbox.
- Renamed Camera's class from "Camera" to "Camera_class". This will be less confusing than unusable "Camera" and usable object of "camera".
- Added a function (method) to move an object alongside a direction vector with certain speed factor. You can use this to for example make a bullet fly in direction player is currently facing.
- Added a similar function (method) to rotate an object to match rotation of a vector.
- Added textured rectangular prism, which can have (even transparent) images as sides. You can use PIL image variable, load image from path or still use a plain color.
- Added a class for easy management of asynchronous functions. It allows to start, stop and read status and results of async functions.
- Added a method which renders only 3D objects that are currently visible, which allows to increase performance.

Version 0.1.5 (planned to release on January 2025):
- Improve rendering of textures of Textured_RectangularPrism so they render normally.
- Add more texturing methods for Model3D_STL.

Version 0.1.6 (planned to release on January or February 2025):
- Light/shading support and new related methods, funtions, objects and functionalities.
