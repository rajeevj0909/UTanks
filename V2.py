import pyglet
#Sets window dimensions
window_w=1280
window_h=720
window=pyglet.window.Window(width=window_w,height=window_h)
#Creates a class for my objects
class game:
    def __init__(self, width,height):
        #Opens my image from the same folder code file is stored in
        self.tank_image=pyglet.resource.image("tank.jpg")
        #Sets the width and height as variables to be used throughout class
        self.width = width
        self.height = height
        
    #Method specifically to load tank
    def load_tank(self):
        window.clear()
        #Sets the size of tank to what I chose, 150x150
        self.tank_image.width=self.width
        self.tank_image.height=self.height
        #Sets anchor points at centre
        self.tank_image.anchor_x=self.tank_image.width/2
        self.tank_image.anchor_y=self.tank_image.height/2
        #Creates a sprite at centre of window
        self.tank_sprite=pyglet.sprite.Sprite(self.tank_image,x=window_w/2,y=window_h/2)
        #Runs draw method
        self.tank_sprite.draw()

    #Runs function when there is any event in window
    @window.event
    def on_draw():
        #Removes everything from window
        window.clear()
        #Inserts tank sprite
        tank_object.load_tank()

#Creates an object for the tank, size goes into parameters
tank_object=game(150,150)

#Run Window
pyglet.app.run()
