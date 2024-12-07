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
