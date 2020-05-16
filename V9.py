import pyglet
from pyglet.window import mouse
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
        #Starts with nothing there
        self.bullet_sprite.visible = False

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
            if button == mouse.RIGHT:
                #Only becomes visible after mouse press
                self.bullet_sprite.visible = True
                self.bullet_sprite.x=self.tank_sprite.x
                self.bullet_sprite.y=self.tank_sprite.y
                bullet_x=self.bullet_sprite.x
                bullet_y=self.bullet_sprite.y
                mouse_x=x
                mouse_y=y
                x_length = mouse_x - bullet_x
                y_length = mouse_y - bullet_y
                if x_length>0:
                    angle = math.degrees(math.atan(y_length / x_length))
                    angle = 90 - angle
                    self.bullet_sprite.rotation = angle
                else:
                    angle = math.degrees(math.atan(y_length / x_length))
                    angle = 270- angle
                    self.bullet_sprite.rotation = angle
                # I've set a temporary speed for testing purposes
                self.speed = 1.6
                # These set the speed of the x and y
                # Distance between cursor and tank determine speed
                self.bullet_sprite.dx = x_length * self.speed
                self.bullet_sprite.dy = y_length * self.speed
                #Updates the window with the new positions of the bullet
                def update(dt):
                    # Equation to calculate the speed of bullet for both x and y
                    self.bullet_sprite.x += self.bullet_sprite.dx * dt
                    self.bullet_sprite.y += self.bullet_sprite.dy * dt
                # Updates window at 60Hz
                pyglet.clock.schedule_interval(update, 1 / 60.0)

    @window.event
    def on_draw():
        window.clear()
        tank_object.load_tank()
        bullet_object.load_bullet()


tank_object=game()
bullet_object=game()
pyglet.app.run()
