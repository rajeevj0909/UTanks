import pyglet
#This line recognises mouse clicks
from pyglet.window import mouse
window_w=1280
window_h=720
window=pyglet.window.Window(width=window_w,height=window_h)
class game:
    def __init__(self):
        self.tank_image=pyglet.resource.image("tank.png")
        self.tank_image.width=150
        self.tank_image.height=150
        self.tank_image.anchor_x=self.tank_image.width/2
        self.tank_image.anchor_y=self.tank_image.height/2
        self.tank_sprite=pyglet.sprite.Sprite(self.tank_image,x=window_w/2,y=window_h/2)

        self.bullet_image = pyglet.resource.image("bullet.png")
        self.bullet_image.width = 42
        self.bullet_image.height =67
        self.bullet_image.anchor_x = self.tank_image.width / 2
        self.bullet_image.anchor_y = 0
        self.bullet_sprite = pyglet.sprite.Sprite(self.bullet_image,x=window_w/2,y=(window_h*3)/4)

        self.steps=10

    def load_tank(self):
        self.tank_sprite.draw()

        @window.event
        def on_text_motion(motion):
            if motion == pyglet.window.key.MOTION_DOWN:
                self.tank_sprite.y -=self.steps
                self.tank_sprite.rotation=180
            elif (motion == pyglet.window.key.MOTION_UP):
                self.tank_sprite.y += self.steps
                self.tank_sprite.rotation=0
            elif (motion == pyglet.window.key.MOTION_LEFT):
                self.tank_sprite.x -=  self.steps
                self.tank_sprite.rotation=270
            elif (motion == pyglet.window.key.MOTION_RIGHT):
                self.tank_sprite.x +=  self.steps
                self.tank_sprite.rotation=90

    def load_bullet(self):
        self.bullet_sprite.draw()

        #This function prints when the right key is clicked
        @window.event
        def on_mouse_press(x, y, button, modifiers):
            if button == mouse.RIGHT:
                print("RIGHT CLICK!")

    @window.event
    def on_draw():
        window.clear()
        tank_object.load_tank()
        bullet_object.load_bullet()

tank_object=game()
bullet_object=game()
pyglet.app.run()
