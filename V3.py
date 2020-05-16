import pyglet
window_w=1280
window_h=720
window=pyglet.window.Window(width=window_w,height=window_h)
class game:
    def __init__(self):
        self.tank_image=pyglet.resource.image("tank.jpg")
        self.tank_image.width=150
        self.tank_image.height=150
        #Sets anchor point to sprite centre
        self.tank_image.anchor_x=self.tank_image.width/2
        self.tank_image.anchor_y=self.tank_image.height/2
        #Draws sprite to avoid redrawing in same place
        self.tank_sprite=pyglet.sprite.Sprite(self.tank_image,x=window_w/2,y=window_h/2)
        self.steps=100
        
    #2-Function to load tank
    def load_tank(self):
        #Draws tank
        self.tank_sprite.draw()

        #Event caused in window
        @window.event
        #Inbuilt function, attribute is the key pressed
        def on_text_motion(motion):
            #If key pressed in Down Key
            if motion == pyglet.window.key.MOTION_DOWN:
                #Print down and move y co-ordinate of sprite down
                print("DOWN!")
                self.tank_sprite.y -=self.steps
            elif (motion == pyglet.window.key.MOTION_UP):
                print("UP!")
                self.tank_sprite.y += self.steps
            elif (motion == pyglet.window.key.MOTION_LEFT):
                print("LEFT!")
                self.tank_sprite.x -=  self.steps
            elif (motion == pyglet.window.key.MOTION_RIGHT):
                print("RIGHT!")
                self.tank_sprite.x +=  self.steps

    #1-Runs the on_draw
    @window.event
    def on_draw():
        window.clear()
        #Causes function to load tank to run
        tank_object.load_tank()

tank_object=game()
pyglet.app.run()
