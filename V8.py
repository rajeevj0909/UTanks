import pyglet
from pyglet.window import mouse
#Allows me to run math functions
import math
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
        self.bullet_image.anchor_x = self.bullet_image.width / 2
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

        @window.event
        def on_mouse_press(x, y, button, modifiers):
            #Puts the bullet coming out of the tank
            self.bullet_sprite.x=self.tank_sprite.x
            self.bullet_sprite.y=self.tank_sprite.y
            #Co-ordinates of the bullet position
            bullet_x=self.bullet_sprite.x
            bullet_y=self.bullet_sprite.y
            # Co-ordinates of the mouse cursor
            mouse_x=x
            mouse_y=y
            #Find the different in length in both axis
            x_length = mouse_x - bullet_x
            y_length = mouse_y - bullet_y
            #Right Side
            if x_length>0:
                #Works out the angle to fire at using trigonometry
                angle = math.degrees(math.atan(y_length / x_length))
                angle = 90 - angle
                #Sets the rotation of the bullet to the angle
                self.bullet_sprite.rotation = angle
            #Left side
            else:
                # Works out the angle to fire at using trigonometry
                angle = math.degrees(math.atan(y_length / x_length))
                angle = 270- angle
                # Sets the rotation of the bullet to the angle
                self.bullet_sprite.rotation = angle

            if button == mouse.RIGHT:
                self.bullet_sprite.dx = 50.0
                def update(dt):
                    self.bullet_sprite.x += self.bullet_sprite.dx * dt
                pyglet.clock.schedule_interval(update, 1 / 60.0)

    @window.event
    def on_draw():
        window.clear()
        tank_object.load_tank()
        bullet_object.load_bullet()


tank_object=game()
bullet_object=game()
pyglet.app.run()
