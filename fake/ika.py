class Control:
	"""Represents a single button or axis. (such as a key, or a joystick button)
	Access these through an input device.  They can never be created directly."""
	def Delta():#<built-in method Delta of Control object at 0x09C03AA0>
		"""Control.Delta() -> float
		
		Returns the change in position of the control since the last time Pressed() or Delta() was called."""
		pass
	def Position():#<built-in method Position of Control object at 0x09C03AA0>
		"""Control.Position() -> float
		
		Returns the position of the control.  Most controls are normalized, meaning that their value is in the
		range of 0 through 1. (1 being pressed all the way, 0 being unpressed)
		
		The mouse axis are the only exception to this.  Their range is equal to the screen resolution."""
		pass
	def Pressed():#<built-in method Pressed of Control object at 0x09C03AA0>
		"""Control.Pressed() -> int
		
		Returns nonzero if the key has been pressed since the last time Pressed() or Delta() have been called"""
		pass
	onpress=None
	onunpress=None
AddBlend=3
AlphaBlend=2
class Canvas(object):
	"""A software representation of an image that can be manipulated easily.
	
	Canvas(filename)
	
	Loads the image specified by 'filename' into a new canvas.
	
	Canvas(width, height)
	
	Creates a new, blank canvas of the specified size."""
	def AlphaMask():#<method 'AlphaMask' of 'Canvas' objects>
		"""Canvas.AlphaMask()
		
		Takes the max of r/g/b for each pixel, and applies the value to that pixel's a.
		Very handy in conjunction with ika.Video.GrabCanvas and canvas blitting routines."""
		pass
	def Blit(destcanvas, x, y, blendmode):#<method 'Blit' of 'Canvas' objects>
		"""Canvas.Blit(destcanvas, x, y, blendmode)
		
		Draws the image on destcanvas, at position (x, y)
		blendmode specifies the algorithm used to blend pixels.  It is one of
		the available blend modes defined in ika's constants section.
		blendmode defaults to ika.AlphaBlend."""
		pass
	def Clear():#<method 'Clear' of 'Canvas' objects>
		"""Canvas.Clear([colour])
		
		Sets every pixel on the canvas to the colour given.  If colour is omitted, 
		flat black is used."""
		pass
	def Clip():#<method 'Clip' of 'Canvas' objects>
		"""Canvas.Clip([x, y, width, height])
		
		Sets the clipping rectangle of the canvas.  Blitting to the canvas will be confined to
		the clip rectangle; blitting the canvas on others will only blit the clipped region.
		
		If no arguments are specified, the clip rectangle is reset to cover the whole canvas."""
		pass
	def DrawLine(x1, y1, x2, y2, colour):#<method 'DrawLine' of 'Canvas' objects>
		"""Canvas.DrawLine(x1, y1, x2, y2, colour, [blendmode])
		
		Draws a line from (x1, y1) to (x2, y2) of the colour and blendmode specified."""
		pass
	def DrawRect(x1, y1, x2, y2, colour):#<method 'DrawRect' of 'Canvas' objects>
		"""Canvas.DrawRect(x1, y1, x2, y2, colour, [blendmode])
		
		Draws a rect from top left (x1, y1) to bottom right (x2, y2) of the colour and blendmode specified."""
		pass
	def DrawText(font, x, y, text):#<method 'DrawText' of 'Canvas' objects>
		"""Canvas.DrawText(font, x, y, text)
		
		Draws a string starting at (x,y) with the font.  No word wrapping is done."""
		pass
	def Flip():#<method 'Flip' of 'Canvas' objects>
		"""Canvas.Flip()
		
		Flips the contents of the canvas on the X axis.
		(turns it upside down)"""
		pass
	def GetPixel(x, y):#<method 'GetPixel' of 'Canvas' objects>
		"""Canvas.GetPixel(x, y)
		
		Returns the pixel at position (x, y) on the canvas, as a packed 32bpp RGBA colour."""
		pass
	def Mirror():#<method 'Mirror' of 'Canvas' objects>
		"""Canvas.Mirror()
		
		Mirrors the contents of the canvas along the Y axis.
		(left to right)"""
		pass
	def Resize(width, height):#<method 'Resize' of 'Canvas' objects>
		"""Canvas.Resize(width, height)
		
		Resizes the canvas to the size specified.  No scaling takes place; if the dimensions
		given are smaller than the existing image, it is cropped.  Blank, transparent space is
		added when the canvas is enlarged."""
		pass
	def Rotate():#<method 'Rotate' of 'Canvas' objects>
		"""Canvas.Rotate()
		
		Rotates the contents of the canvas 90 degrees, clockwise."""
		pass
	def Save(fname):#<method 'Save' of 'Canvas' objects>
		"""Canvas.Save(fname)
		
		Writes the image to the filename specified in PNG format.
		
		ie.  canvas.Save('myimage.png')"""
		pass
	def ScaleBlit(destcanvas, x, y, width, height, blendmode):#<method 'ScaleBlit' of 'Canvas' objects>
		"""Canvas.ScaleBlit(destcanvas, x, y, width, height, blendmode)
		
		Draws the image on destcanvas, at position (x, y), scaled to (width, height) pixels in size.
		blendmode specifies the algorithm used to blend pixels.  It is one of
		the available blend modes defined in ika's constants section.
		blendmode defaults to ika.AlphaBlend."""
		pass
	def SetPixel(x, y, colour):#<method 'SetPixel' of 'Canvas' objects>
		"""Canvas.SetPixel(x, y, colour)
		
		Sets the pixel at (x, y) on the canvas to the colour specified.  This function
		totally disregards alpha.  It *sets* the pixel, in the truest sense of the word."""
		pass
	def TileBlit(destcanvas, x, y, width, height):#<method 'TileBlit' of 'Canvas' objects>
		"""Canvas.TileBlit(destcanvas, x, y, width, height, [offsetx, offsety, blendmode])
		
		Tiles the image within the region specified, on destcanvas.  The tiling is offset
		(moved) by offsetx and offsety. (both default to zero)
		blendmode specifies the algorithm used to blend pixels.  It is one of
		the available blend modes defined in ika's constants section.
		blendmode defaults to ika.AlphaBlend."""
		pass
	@property
	def height():
		"""Gets the height of the canvas"""
		pass
	@property
	def width():
		"""Gets the width of the canvas"""
		pass
def Delay(time):#<built-in function Delay>
	"""Delay(time)
	
	Freezes the engine for a number of 'ticks'. (one tick is 1/100th of a second)"""
	pass
def EntitiesAt(x, y, width, height, layer):#<built-in function EntitiesAt>
	"""EntitiesAt(x, y, width, height, layer) -> list
	
	Returns a list containing all entities within the given rect,
	on the given layer.  If there are no entities there, the empty
	list is returned."""
	pass
class Entity(object):
	"""Entity(x, y, layer, spritename) -> Entity
	
	Creates a new entity at pixel coordinates (x,y) on the
	layer index specified.  The new entity uses the sprite
	indicated."""
	def DetectCollision():#<method 'DetectCollision' of 'Entity' objects>
		"""Entity.DetectCollision() -> Entity
		
		If an entity is touching the entity, then it is returned.
		None is returned if there is no entity touching it."""
		pass
	def Draw():#<method 'Draw' of 'Entity' objects>
		"""Entity.Draw([x[, y[, frame]]])
		
		Draws the entity at the position specified.  x and y default to
		the position where they would normally draw, given the window position
		and the entity position.
		
		Render scripts are ignored by this method, and can easily be used within
		them without hassle."""
		pass
	def GetAllAnimScripts():#<method 'GetAllAnimScripts' of 'Entity' objects>
		"""Entity.GetAllAnimScripts() -> dict
		
		Returns a dict containing all animation scripts defined in the entity's current
		spriteset."""
		pass
	def GetAnimScript(name):#<method 'GetAnimScript' of 'Entity' objects>
		"""Entity.GetAnimScript(name ->str) -> str
		
		Returns the animation script with the name given, for the entity's current
		spriteset.  The empty string is returned if no such script exists."""
		pass
	def IsMoving():#<method 'IsMoving' of 'Entity' objects>
		"""Entity.IsMoving() -> int
		
		If the entity is moving, the result is 1.  If not, it is 0."""
		pass
	def MoveTo(x, y):#<method 'MoveTo' of 'Entity' objects>
		"""Entity.MoveTo(x, y)
		
		Directs the entity to move towards the position specified."""
		pass
	def Render():#<method 'Render' of 'Entity' objects>
		"""Entity.Render()
		
		Draws the entity at the position specified.  Unlike Entity.Draw,
		Entity.Render() will call a render script if one is set.
		
		For this reason, *DO NOT CALL THIS IN A RENDER SCRIPT*.  Puppies
		will explode, and you will be very sad."""
		pass
	def Stop():#<method 'Stop' of 'Entity' objects>
		"""Entity.Stop()
		
		Directs the entity to stop whatever it is doing."""
		pass
	def Touches(ent):#<method 'Touches' of 'Entity' objects>
		"""Touches(ent) -> boolean
		
		Returns true if the entity is touching entity ent, else False."""
		pass
	def Update():#<method 'Update' of 'Entity' objects>
		"""Entity.Update()
		
		Performs 1/100th of a second of entity AI. Calling this 100 times a second.
		will cause the entity to move around as if the engine was in control."""
		pass
	def Wait(time):#<method 'Wait' of 'Entity' objects>
		"""Entity.Wait(time)
		
		Causes the entity to halt for the given interval before
		resuming motion."""
		pass
	@property
	def actscript():
		"""Gets or sets the object called when the entity is activated."""
		pass
	@property
	def adjacentactivate():
		"""Gets or sets the object called when the entity touches another entity."""
		pass
	@property
	def curframe():
		"""Gets the entity's currently displayed frame"""
		pass
	@property
	def direction():
		"""Gets or sets the entity's direction"""
		pass
	@property
	def entobs():
		"""If nonzero, the entity is unable to walk through entities whose isobs property is set."""
		pass
	@property
	def hotheight():
		"""Gets the height of the entity's hotspot."""
		pass
	@property
	def hotwidth():
		"""Gets the width of the entity's hotspot."""
		pass
	@property
	def hotx():
		"""Gets the X position of the entity's hotspot."""
		pass
	@property
	def hoty():
		"""Gets the Y position of the entity's hotspot."""
		pass
	@property
	def isobs():
		"""If nonzero, the entity will obstruct other entities."""
		pass
	@property
	def layer():
		"""Gets or sets the index of the layer that the entity exists on."""
		pass
	@property
	def mapobs():
		"""If nonzero, the entity is unable to walk on obstructed areas of the map."""
		pass
	@property
	def movescript():
		"""Gets or sets the entity's current move script."""
		pass
	@property
	def name():
		"""Gets or sets the entity's name.  This is more or less for your own convenience only."""
		pass
	@property
	def renderscript():
		"""Gets or sets a script to be called when the entity is drawn.
		If None, the default behaviour is performed. (ie to draw the
		current frame at the current position)
		The function should be of the form myscript(entity, x, y, frame),
		where x and y are the screen coordinates where the entity
		would normally be drawn, and frame is the frame that would
		be displayed."""
		pass
	@property
	def specanim():
		"""If not None, this animation strand is used instead of the normal animation scripts."""
		pass
	@property
	def specframe():
		"""If not -1, this frame is displayed instead of the normal animation"""
		pass
	@property
	def speed():
		"""Gets or sets the entity's speed, in pixels/second"""
		pass
	@property
	def spriteheight():
		"""Gets the height of the entity's sprite."""
		pass
	@property
	def spritename():
		"""Gets or sets the filename of the sprite used to display the entity.  Setting this will load a spriteset and make the sprite use it."""
		pass
	@property
	def spritewidth():
		"""Gets the width of the entity's sprite."""
		pass
	@property
	def visible():
		"""If nonzero, the entity is drawn when onscreen"""
		pass
	@property
	def x():
		"""Gets or sets the entity's X position. (in pixels)"""
		pass
	@property
	def y():
		"""Gets or sets the entity's Y position. (in pixels)"""
		pass
def Exit():#<built-in function Exit>
	"""Exit([message])
	
	Exits ika immediately, displaying the message onscreen, if specified."""
	pass
class Font(object):
	"""ika.Font(fontFileName)->font
	
	A proportional bitmap font.  fontFileName is a string that contains
	the filename to a font file."""
	def CenterPrint(x, y, text):#<method 'CenterPrint' of 'Font' objects>
		"""Font.CenterPrint(x, y, text)
		
		Prints a string of text on screen, 
		with x as the center point rather than the leftmost point."""
		pass
	def Print(x, y, text):#<method 'Print' of 'Font' objects>
		"""Font.Print(x, y, text)
		
		Prints a string of text on screen at (x, y)."""
		pass
	def RightPrint(x, y, text):#<method 'RightPrint' of 'Font' objects>
		"""Font.RightPrint(x, y, text)
		
		Prints a string of text on screen, with x as the rightmost point
		rather than the leftmost point."""
		pass
	def StringHeight(text):#<method 'StringHeight' of 'Font' objects>
		"""Font.StringHeight(text) -> int
		
		Returns how many pixels in height the passed string would be, 
		if printed in this font.  Takes newlines into account."""
		pass
	def StringWidth(text):#<method 'StringWidth' of 'Font' objects>
		"""Font.StringWidth(text) -> int
		
		Returns how many pixels in width the passed string would be, 
		if printed in this font.  Takes newlines into account."""
		pass
	@property
	def height():
		"""Gets the height of the font."""
		pass
	@property
	def letterspacing():
		"""Gets or sets the letter spacing of the font."""
		pass
	@property
	def linespacing():
		"""Gets or sets the line spacing of the font."""
		pass
	@property
	def tabsize():
		"""Gets or sets the tab size of the font."""
		pass
	@property
	def width():
		"""Gets the width of the widest glyph in the font."""
		pass
	@property
	def wordspacing():
		"""Gets or sets the word spacing of the font."""
		pass
def GetCameraTarget():#<built-in function GetCameraTarget>
	"""GetCameraTarget() -> Entity
	
	Returns the entity that the camera is following, or None if it is free."""
	pass
def GetCaption():#<built-in function GetCaption>
	"""GetCaption() -> string
	
	Returns the caption on the ika window title bar."""
	pass
def GetFrameRate():#<built-in function GetFrameRate>
	"""GetFrameRate() -> int
	
	Returns the current engine framerate, in frames per second."""
	pass
def GetPlayer(entity):#<built-in function GetPlayer>
	"""GetPlayer(entity) -> Entity
	
	Returns the current player entity, or None if there isn't one."""
	pass
def GetRGB(colour):#<built-in function GetRGB>
	"""GetRGB(colour) -> tuple(int, int, int, int)
	
	Returns a 4-tuple containing the red, blue, green, and alpha values of the colour
	passed, respectively."""
	pass
def GetTime():#<built-in function GetTime>
	"""GetTime() -> int
	
	Returns the number of ticks since the engine was started."""
	pass
def HookRetrace(function):#<built-in function HookRetrace>
	"""HookRetrace(function)
	
	Adds the function to the retrace queue. (it will be called whenever the map is drawn, 
	whether by Map.Render or by other means)"""
	pass
def HookTimer(function):#<built-in function HookTimer>
	"""HookTimer(function)
	
	Adds the function to the timer queue. (the function will be called 100 times per second.
	This feature should be used sparingly, as it will cause serious problems if the queue
	cannot be executed in less than 1/100th of a second."""
	pass
class Image(object):
	"""A hardware-dependant image."""
	def Blit(x, y):#<method 'Blit' of 'Image' objects>
		"""Image.Blit(x, y[, blendmode])
		
		Draws the image at (x, y).
		blendmode specifies the algorithm used to blend pixels.  It is one of
		the available blend modes defined in ika's constants section.
		blendmode defaults to ika.AlphaBlend."""
		pass
	def ClipBlit(x, y, ix, iy, iw, ih):#<method 'ClipBlit' of 'Image' objects>
		"""ClipBlit(x, y, ix, iy, iw, ih[, blendmode])
		
		Draws a portion of the image defined by the coordinates (ix, iy, iw, ih)
		at screen coordinates (x, y).
		blendmode specifies the algorithm used to blend pixels.  It is one of
		the available blend modes defined in ika's constants section.
		blendmode defaults to ika.AlphaBlend."""
		pass
	def DistortBlit((x1, y1), (x2, y2), (x3, y3), (x4, y4)):#<method 'DistortBlit' of 'Image' objects>
		"""Image.DistortBlit((x1, y1), (x2, y2), (x3, y3), (x4, y4)[, blendmode])
		
		Blits the image scaled to the four points specified.blendmode specifies the algorithm used to blend pixels.  It is one of
		the available blend modes defined in ika's constants section.
		blendmode defaults to ika.AlphaBlend."""
		pass
	def RotateBlit(x, y, angle):#<method 'RotateBlit' of 'Image' objects>
		"""RotateBlit(x, y, angle, [scalex[, scaley [, blendmode]]])
		
		Draws the image at (x, y), rotating to the angle given.
		scalex and scaley are floating point values used as a scale factor.  The default is 1.
		blendmode specifies the algorithm used to blend pixels.  It is one of
		the available blend modes defined in ika's constants section.
		blendmode defaults to ika.AlphaBlend."""
		pass
	def ScaleBlit(x, y, width, height):#<method 'ScaleBlit' of 'Image' objects>
		"""Image.ScaleBlit(x, y, width, height[, blendmode])
		
		Blits the image, but stretches it out to the dimensions
		specified in (width, height).blendmode specifies the algorithm used to blend pixels.  It is one of
		the available blend modes defined in ika's constants section.
		blendmode defaults to ika.AlphaBlend."""
		pass
	def TileBlit(x, y, width, height):#<method 'TileBlit' of 'Image' objects>
		"""Image.TileBlit(x, y, width, height[, scalex[, scaley[, blendmode]]])
		
		Draws the image onscreen, "tiling" it as necessary to fit the rectangle specified.
		scalex and scaley are floating point values used as a scale factor.  The default is 1.
		blendmode specifies the algorithm used to blend pixels.  It is one of
		the available blend modes defined in ika's constants section.
		blendmode defaults to ika.AlphaBlend."""
		pass
	def TintBlit(x, y, tintColour):#<method 'TintBlit' of 'Image' objects>
		"""Image.TintBlit(x, y, tintColour[, blendMode])
		
		Draws the image onscreen, using tintColour to 'tint' the image.
		Each pixel is multiplied by tintColour.  The resultant values are then
		scaled before the pixel is plotted.
		
		In English, this means that RGBA(255, 255, 255, 255) is a normal blit,
		while RGBA(0, 0, 0, 255) will leave the alpha channel intact, but reduce
		all pixels to black. (effectively drawing a silhouette)
		
		blendMode is handled the same way as all the other blits.
		
		Lots of effects could be created by using this creatively.  Experiment!"""
		pass
	def TintDistortBlit((upleftX, upleftY, upleftTint), (uprightX, uprightY, uprightTint), (downrightX, downrightY, downrightTint), (downleftX, downleftY, downrightTint)):#<method 'TintDistortBlit' of 'Image' objects>
		"""Image.TintDistortBlit((upleftX, upleftY, upleftTint), (uprightX, uprightY, uprightTint), (downrightX, downrightY, downrightTint), (downleftX, downleftY, downrightTint)[, blendmode])
		
		Combines the effects of DistortBlit and TintBlit.  Each corner can be tinted individually,
		using the same algorithm as TintBlit.  The corners, if not the same, are smoothly interpolated
		across the image."""
		pass
	def TintTileBlit(x, y, width, height, tintColour, scalex=1, scaley=1, blendmode=Normal):#<method 'TintTileBlit' of 'Image' objects>
		"""Image.TintTileBlit(x, y, width, height, tintColour, scalex=1, scaley=1, blendmode=Normal)
		
		"tile"-blits the image, just like Video.TileBlit, except it multiplies each pixel by
		tintColour, resulting in a colour tint."""
		pass
	@property
	def height():
		"""Gets the height of the image."""
		pass
	@property
	def width():
		"""Gets the width of the image."""
		pass
class Input(object):
	"""Interface for hardware input devices. (such as the keyboard and mouse)"""
	def Unpress():#<built-in method Unpress of Input object at 0x09A383E0>
		"""Unpress()
		
		Unsets the Pressed() property of all controls.  Has no effect on
		their positions.
		Individual controls can be unpressed by simply calling their Pressed()
		method, discarding the result."""
		pass
	def Update():#<built-in method Update of Input object at 0x09A383E0>
		"""Update()
		
		Updates the state of the mouse, and any attached input devices.
		Also gives the OS a chance to do background tasks.  Continuous
		loops should call this occasionally to give the OS time to perform
		its tasks."""
		pass
	cancel=Control() # <Control object at 0x09C03860>
	down=Control() # <Control object at 0x09C03C20>
	enter=Control() # <Control object at 0x09C03860>
	joysticks=()
	class keyboard(object):
		"""The keyboard. Get access to this object from ika.Input.keyboard.
		There can only be one instance of the Keyboard."""
		ClearKeyQueue=Control()
		GetKey=Control()
		WasKeyPressed=Control()
	left=Control() # <Control object at 0x09C03860>
	class mouse(object):
		"""The mouse.  Access this through ika.Input.mouse
		Additional instances of this object cannot be created."""
		left=Control()
		middle=Control()
		right=Control()
		wheel=Control()
		x=Control()
		y=Control()
	right=Control() # <Control object at 0x09C03860>
	up=Control() # <Control object at 0x09C03C20>
def Log(message):#<built-in function Log>
	"""Log(message)
	
	Writes a string to ika.log, if logging is enabled."""
	pass
Matte=1
MultiplyBlend=5
class Music(object):
	"""Streamed sound data.  Almost always used for music, but could be useful
	any time sound data needs to be looped or paused and resumed."""
	def Pause():#<method 'Pause' of 'Music' objects>
		"""Music.Pause()
		
		Pauses the stream.  Calling Music.Play() will cause playback to resume
		where it left off."""
		pass
	def Play():#<method 'Play' of 'Music' objects>
		"""Music.Play()
		
		Plays the stream."""
		pass
	@property
	def loop():
		"""If nonzero, the sound loops.  If zero, then the sound stops playing when it reaches the end."""
		pass
	@property
	def pan():
		"""Panning.  -1 is left.  1 is right.  0 is centre."""
		pass
	@property
	def pitchshift():
		"""Pitch shift.  1.0 is normal, I think.  2.0 being double the frequency.  I think.  TODO: document this after testing"""
		pass
	@property
	def position():
		"""The chronological position of the sound, in milliseconds."""
		pass
	@property
	def volume():
		"""The volume of the sound.  Ranges from 0 to 1, with 1 being full volume."""
		pass
Opaque=0
PreserveBlend=6
def ProcessEntities():#<built-in function ProcessEntities>
	"""ProcessEntities()
	
	Performs 1/100th of a second of entity AI.  Calling this 100 times a second
	will cause entities to move around as if the engine was in control."""
	pass
def RGB(r, g, b):#<built-in function RGB>
	"""RGB(r, g, b[, a]) -> int
	
	Creates a 32bpp colour value from the four colour levels passed.  If alpha is
	omitted, it is assumed to be 255. (opaque)"""
	pass
def Random(min, max):#<built-in function Random>
	"""Random(min, max) -> int
	
	Returns a random integer less than or equal to min, and less than max.
	ie.  min <= value < max"""
	pass
def Render():#<built-in function Render>
	"""Render([layerList])
	
	Redraw the scene.  layerList is an optional sequence of integers;
	ika will only draw these layers, in the order given, if specified.
	If layerList is omitted, all layers will be drawn, in their predefined
	order (set in the editor)
	
	If layerList is omitted, the screen is cleared to black before rendering
	begins."""
	pass
def SetCameraTarget(entity):#<built-in function SetCameraTarget>
	"""SetCameraTarget(entity)
	
	Sets the camera target to the entity specified.  If None is passed instead, 
	the camera remains stationary, and can be altered with the Map.xwin and Map.ywin
	properties."""
	pass
def SetCaption(newcaption):#<built-in function SetCaption>
	"""SetCaption(newcaption)
	
	Sets the caption on the ika window title bar."""
	pass
def SetMapPath(newmappath):#<built-in function SetMapPath>
	"""SetMapPath(newmappath)
	
	Sets the folder for ika to load both map and tileset files from.
	Make to sure to end your folder with a trailing /!"""
	pass
def SetPlayer(entity):#<built-in function SetPlayer>
	"""SetPlayer(entity)
	
	Sets the player entity to the entity passed.  The player entity is the entity
	that moves according to user input.  Passing None instead unsets any player entity
	that may have been previously set."""
	pass
def SetRenderList(index, *args):#<built-in function SetRenderList>
	"""SetRenderList(index, ...)
	
	Sets the default rendering order used with Map.Render.  This can be useful for
	hiding layers, or moving them up and down in the ordering."""
	pass
class Sound(object):
	"""A sound effect.  Unlike Music, Sounds can be played multiple times at once."""
	def Pause():#<method 'Pause' of 'Sound' objects>
		"""Sound.Pause()
		
		Pauses the sound effect.  Calling Sound.Play() will cause playback to start over."""
		pass
	def Play():#<method 'Play' of 'Sound' objects>
		"""Sound.Play()
		
		Plays the sound effect."""
		pass
	@property
	def pan():
		"""Panning.  -1 is left.  1 is right.  0 is centre."""
		pass
	@property
	def pitchshift():
		"""Pitch shift.  1.0 is normal, I think.  2.0 being double the frequency.  I think.  TODO: document this after testing"""
		pass
	@property
	def volume():
		"""The volume of the sound effect.  Ranges from 0 to 1, with 1 being full volume."""
		pass
SubtractBlend=4
def UnhookRetrace():#<built-in function UnhookRetrace>
	"""UnhookRetrace([function])
	
	Removes the function from the retrace queue if it is present.  If not, the call does
	nothing.  If the argument is omitted, then the list is cleared in its entirety."""
	pass
def UnhookTimer():#<built-in function UnhookTimer>
	"""UnhookTimer([function])
	
	Removes the function from the timer queue if it is present.  If not, the call does
	nothing.  If the argument is omitted, then the list is cleared in its entirety."""
	pass
Version=0.63
class Video(object):
	"""Interface for ika's graphics engine."""
	def Blit(image, x, y):#<built-in method Blit of Video object at 0x09A386E0>
		"""Blit(image, x, y[, blendmode])
		
		Deprecated. Use ika.Image.Blit instead.
		"""
		pass
	def ClearScreen():#<built-in method ClearScreen of Video object at 0x09A386E0>
		"""ClearScreen()
		
		Clears the screen. (with blackness)"""
		pass
	def ClipBlit(image, x, y, ix, iy, iw, ih):#<built-in method ClipBlit of Video object at 0x09A386E0>
		"""ClipBlit(image, x, y, ix, iy, iw, ih[, blendmode])
		
		Deprecated. Use ika.Image.ClipBlit instead.
		"""
		pass
	def ClipScreen(left=0, top=0, right=xres, bottom=yres):#<built-in method ClipScreen of Video object at 0x09A386E0>
		"""ClipScreen(left=0, top=0, right=xres, bottom=yres)
		
		Clips the video display to the rectangle specfied.  All drawing
		operations will be confined to this region.
		
		Calling ClipScreen with no arguments will reset the clipping rect
		to its default setting. (the whole screen)"""
		pass
	def DistortBlit(image, (upleftX, upleftY), (uprightX, uprightY), (downrightX, downrightY), (downleftX, downleftY)):#<built-in method DistortBlit of Video object at 0x09A386E0>
		"""DistortBlit(image, (upleftX, upleftY), (uprightX, uprightY), (downrightX, downrightY), (downleftX, downleftY)[, blendmode])
		
		Deprecated. Use ika.Image.DistortBlit instead.
		"""
		pass
	def DrawArc(cx, cy, rx, ry, irx, iry, start, end, colour):#<built-in method DrawArc of Video object at 0x09A386E0>
		"""DrawArc(cx, cy, rx, ry, irx, iry, start, end, colour[, filled, blendmode])
		
		Draws an arc, centred at (cx, cy), of radius rx and ry and inner radius irx and iry on the X and
		Y axis, respectively, from angle start to angle end, in degrees.  If filled is omitted or nonzero, the arc is filled in
		else it is drawn as an outline."""
		pass
	def DrawEllipse(cx, cy, rx, ry, colour):#<built-in method DrawEllipse of Video object at 0x09A386E0>
		"""DrawEllipse(cx, cy, rx, ry, colour[, filled, blendmode])
		
		Draws an ellipse, centred at (cx, cy), of radius rx and ry on the X and
		Y axis, respectively.  If filled is omitted or nonzero, the ellipse is filled in
		else it is drawn as an outline."""
		pass
	def DrawLine(x1, y1, x2, y2, colour):#<built-in method DrawLine of Video object at 0x09A386E0>
		"""DrawLine(x1, y1, x2, y2, colour[, blendmode])
		
		Draws a straight line from (x1, y1) to (x2, y2) in the colour specified."""
		pass
	def DrawLineList(pointlist):#<built-in method DrawLineList of Video object at 0x09A386E0>
		"""DrawLineList(pointlist[, drawmode, blendmode]])
		
		Draws a bunch of points onscreen.  Each argument of pointlist should be a tuple in the format (x,y,colour).Each point is drawn in the colour specified, and a gradient is applied between the points.
		There is no extra python overhead on this function, so it is much better suited for drawing a lot of lines thancalling DrawLine a bunch of times.
		Method of drawing depends on the value of drawmode as follows:
		0 - draws lines between each pair of points, so (p1,p2) (p3,p4) etc. (default)
		1 - draws lines between each point and the last point, so (p1,p2) (p2,p3) (p3,p4) etc.
		2 - draws lines between the first point and the other points, so (p1,p2) (p1,p3) (p1,p4) etc.
		3 - draws lines between each point and every other point."""
		pass
	def DrawPixel(x, y, colour):#<built-in method DrawPixel of Video object at 0x09A386E0>
		"""DrawPixel(x, y, colour[, blendmode])
		
		Draws a dot at (x, y) with the colour specified."""
		pass
	def DrawQuad((x, y, colour), (x, y, colour), (x, y, colour), (x, y, colour)):#<built-in method DrawQuad of Video object at 0x09A386E0>
		"""DrawQuad((x, y, colour), (x, y, colour), (x, y, colour), (x, y, colour)[, blendmode])
		
		Draws a quad onscreen.  Each point is drawn in the colour specified.
		(A quad is two triangles from (p1,p2,p3) and (p2,p3,p4).  Therefore, make sure p2 and p3 areopposite corners of the quad.)"""
		pass
	def DrawRect(x1, y1, x2, y2, colour):#<built-in method DrawRect of Video object at 0x09A386E0>
		"""DrawRect(x1, y1, x2, y2, colour[, fill, blendmode])
		
		Draws a rectangle with (x1, y1) and (x2, y2) as opposite corners.
		If fill is omitted or zero, an outline is drawn, else it is filled in."""
		pass
	def DrawTriangle((x, y, colour), (x, y, colour), (x, y, colour)):#<built-in method DrawTriangle of Video object at 0x09A386E0>
		"""DrawTriangle((x, y, colour), (x, y, colour), (x, y, colour)[, blendmode])
		
		Draws a filled triangle onscreen.  Each point is drawn in the colour specified, and a gradient is applied between the points."""
		pass
	def DrawTriangleList(pointlist):#<built-in method DrawTriangleList of Video object at 0x09A386E0>
		"""DrawTriangleList(pointlist[, drawmode, blendmode]])
		
		Draws a bunch of filled triangles onscreen.  Each argument of pointlist should be a tuple in the format (x,y,colour).Each point is drawn in the colour specified, and a gradient is applied between the points.
		There is no extra python overhead on this function, so it is much better suited for drawing a lot of triangles thancalling DrawTriangle a bunch of times.
		Method of drawing depends on the value of drawmode as follows:
		0 - draws triangles between each set of 3 points, so (p1,p2,p3) (p4,p5,p6) etc. (default)
		1 - draws triangles between each point and the last 2 points, so (p1,p2,p3) (p2,p3,p4) (p3,p4,p5) etc.
		2 - draws triangles between the first point, the previous point, and the current point, so (p1,p2,p3) (p1,p3,p4) (p1,p4,p5) etc."""
		pass
	def GetClipRect():#<built-in method GetClipRect of Video object at 0x09A386E0>
		"""GetClipRect() -> (x, y, x2, y2)
		
		Returns the current clipping rectangle."""
		pass
	def GrabCanvas(x1, y1, x2, y2):#<built-in method GrabCanvas of Video object at 0x09A386E0>
		"""GrabCanvas(x1, y1, x2, y2) -> canvas
		
		Grabs a rectangle from the screen, copies it to a canvas, and returns it."""
		pass
	def GrabImage(x1, y1, x2, y2):#<built-in method GrabImage of Video object at 0x09A386E0>
		"""GrabImage(x1, y1, x2, y2) -> image
		
		Grabs a rectangle from the screen, copies it to an image, and returns it."""
		pass
	def RotateBlit(image, x, y, angle):#<built-in method RotateBlit of Video object at 0x09A386E0>
		"""RotateBlit(image, x, y, angle, [scalex[, scaley [, blendmode]]])
		
		Deprecated. Use ika.Image.RotateBlit instead.
		"""
		pass
	def ScaleBlit(image, x, y, width, height):#<built-in method ScaleBlit of Video object at 0x09A386E0>
		"""ScaleBlit(image, x, y, width, height[, blendmode])
		
		Deprecated. Use ika.Image.ScaleBlit instead.
		"""
		pass
	def ShowPage():#<built-in method ShowPage of Video object at 0x09A386E0>
		"""ShowPage()
		
		Flips the back and front video buffers.  This must be called after the screen
		has been completely drawn, or the scene will never be presented to the player.
		This method is not guaranteed to preserve the contents of the screen, so it is
		advised to redraw the entire screen, instead of incrementally drawing."""
		pass
	def TileBlit(image, x, y, width, height):#<built-in method TileBlit of Video object at 0x09A386E0>
		"""TileBlit(image, x, y, width, height[, scalex[, scaley[, blendmode]]])
		
		Deprecated. Use ika.Image.TileBlit instead.
		"""
		pass
	def TintBlit(image, x, y, tintColour):#<built-in method TintBlit of Video object at 0x09A386E0>
		"""TintBlit(image, x, y, tintColour[, blendMode])
		
		Deprecated. Use ika.Image.TintBlit instead.
		"""
		pass
	def TintDistortBlit(image, (upleftX, upleftY, upleftTint), (uprightX, uprightY, uprightTint), (downrightX, downrightY, downrightTint), (downleftX, downleftY, downrightTint)):#<built-in method TintDistortBlit of Video object at 0x09A386E0>
		"""TintDistortBlit(image, (upleftX, upleftY, upleftTint), (uprightX, uprightY, uprightTint), (downrightX, downrightY, downrightTint), (downleftX, downleftY, downrightTint)[, blendmode])
		
		Deprecated. Use ika.Image.TintDistortBlit instead.
		"""
		pass
	def TintTileBlit(image, x, y, width, height, tintColour, scalex=1, scaley=1, blendmode=Normal):#<built-in method TintTileBlit of Video object at 0x09A386E0>
		"""TintTileBlit(image, x, y, width, height, tintColour, scalex=1, scaley=1, blendmode=Normal)
		
		Deprecated. Use ika.Image.TintTileBlit instead.
		"""
		pass
	class colors(object):
		"""Represents a colour registry object
		This can be accessed only through the Video interface."""
		# Error copy: can't extract properties from docstring. 
		# Error has_key: can't extract properties from docstring. 
		# Error items: can't extract properties from docstring. 
		# Error keys: can't extract properties from docstring. 
	class colours(object):
		"""Represents a colour registry object
		This can be accessed only through the Video interface."""
		# Error copy: can't extract properties from docstring. 
		# Error has_key: can't extract properties from docstring. 
		# Error items: can't extract properties from docstring. 
		# Error keys: can't extract properties from docstring. 
	xres=640
	yres=640
def Wait(time):#<built-in function Wait>
	"""Wait(time)
	
	Runs the engine for a number of ticks, disallowing player input.
	Unlike Delay, Wait causes entities to be processed, the tileset to be animated, and the map drawn."""
	pass
