import pyglet
window_w=1280
window_h=720
window=pyglet.window.Window(width=window_w,height=window_h)
class game:
    def __init__(self):
        self.tank_image=pyglet.resource.image("tank.jpg")
        self.tank_image.width=150
        self.tank_image.height=150
        self.tank_image.anchor_x=self.tank_image.width/2
        self.tank_image.anchor_y=self.tank_image.height/2
        self.tank_sprite=pyglet.sprite.Sprite(self.tank_image,x=window_w/2,y=window_h/2)
        self.steps=100
        
    def load_tank(self):
        self.tank_sprite.draw()

        @window.event
        def on_text_motion(motion):
            if motion == pyglet.window.key.MOTION_DOWN:
                self.tank_sprite.y -=self.steps
                #Rotates to look down
                self.tank_sprite.rotation=180
            elif (motion == pyglet.window.key.MOTION_UP):
                self.tank_sprite.y += self.steps
                #Rotates to look up
                #This one is needed if rotation goes from any other direction back to looking up.
                self.tank_sprite.rotation=0
            elif (motion == pyglet.window.key.MOTION_LEFT):
                self.tank_sprite.x -=  self.steps
                #Rotates to look left
                self.tank_sprite.rotation=270
            elif (motion == pyglet.window.key.MOTION_RIGHT):
                self.tank_sprite.x +=  self.steps
                #Rotates to look right
                self.tank_sprite.rotation=90

    @window.event
    def on_draw():
        window.clear()
        tank_object.load_tank()

tank_object=game()
pyglet.app.run()
