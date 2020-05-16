import pyglet
from pyglet.window import mouse
import math
import time
window_w = 1280
window_h = 720
window = pyglet.window.Window(width=window_w, height=window_h)
cursor = window.get_system_mouse_cursor(window.CURSOR_CROSSHAIR)
window.set_mouse_cursor(cursor)

class game:
    def __init__(self):
        self.tank_image = pyglet.resource.image("tank.png")
        self.tank_image.width = 150
        self.tank_image.height = 150
        self.tank_image.anchor_x = self.tank_image.width / 2
        self.tank_image.anchor_y = self.tank_image.height / 2
        self.tank_sprite = pyglet.sprite.Sprite(self.tank_image, x=window_w / 2, y=window_h / 2)

        self.turret_image = pyglet.resource.image("turret.png")
        self.turret_image.width = self.tank_image.width / 3
        self.turret_image.height = (self.tank_image.height / 3) * 2
        self.turret_image.anchor_x = self.turret_image.width / 2
        self.turret_image.anchor_y = self.turret_image.height - 15
        self.turret_sprite = pyglet.sprite.Sprite(self.turret_image, x=self.tank_sprite.x, y=self.tank_sprite.y)

        self.bullet_image = pyglet.resource.image("bullet.png")
        self.bullet_image.width = 42
        self.bullet_image.height = 67
        self.bullet_image.anchor_x = self.bullet_image.width / 2
        self.bullet_image.anchor_y = 0
        self.bullet_sprite = pyglet.sprite.Sprite(self.bullet_image, x=window_w / 2, y=(window_h * 3) / 4)
        self.bullet_sprite.visible = False

        self.steps = 10
        self.reset_speed=0

    def load_tank(self):
        self.tank_sprite.draw()
        self.turret_sprite.draw()

        #Tank Movement
        @window.event
        def on_text_motion(motion):
            if motion == pyglet.window.key.MOTION_DOWN:
                if self.tank_sprite.y>=(self.tank_image.height/2):
                    self.tank_sprite.y -=self.steps
                    self.tank_sprite.rotation=180
            elif (motion == pyglet.window.key.MOTION_UP):
                if self.tank_sprite.y<=window_h-(self.tank_image.height/2):
                    self.tank_sprite.y += self.steps
                    self.tank_sprite.rotation=0
            elif (motion == pyglet.window.key.MOTION_LEFT):
                if self.tank_sprite.x>=(self.tank_image.width/2):
                    self.tank_sprite.x -= self.steps
                    self.tank_sprite.rotation=270
            elif (motion == pyglet.window.key.MOTION_RIGHT):
                if self.tank_sprite.x<=window_w-(self.tank_image.width/2):
                    self.tank_sprite.x +=  self.steps
                    self.tank_sprite.rotation=90
            self.turret_sprite.x = self.tank_sprite.x
            self.turret_sprite.y = self.tank_sprite.y

        #Turret Rotation
        @window.event
        def on_mouse_motion(x, y, dx, dy):
            turret_x = self.turret_sprite.x
            turret_y = self.turret_sprite.y
            mouse_x = x
            mouse_y = y
            x_length = mouse_x - turret_x
            y_length = mouse_y - turret_y
            if x_length > 0:
                angle = math.degrees(math.atan(y_length / x_length))
                angle = 270 - angle
                self.turret_sprite.rotation = angle
            else:
                angle = math.degrees(math.atan(y_length / x_length))
                angle = 90 - angle
                self.turret_sprite.rotation = angle

    def load_bullet(self):
        self.load_tank()
        self.bullet_sprite.draw()

        #Shooting
        @window.event
        def on_mouse_press(x, y, button, modifiers):
            if button == mouse.RIGHT:
                self.bullet_sprite.visible = True
                self.bullet_sprite.x = self.tank_sprite.x
                self.bullet_sprite.y = self.tank_sprite.y
                bullet_x = self.bullet_sprite.x
                bullet_y = self.bullet_sprite.y
                mouse_x = x
                mouse_y = y
                x_length = mouse_x - bullet_x
                y_length = mouse_y - bullet_y
                #Bullet rotation
                if x_length > 0:
                    angle = math.degrees(math.atan(y_length / x_length))
                    angle = 90 - angle
                    self.bullet_sprite.rotation = angle
                else:
                    angle = math.degrees(math.atan(y_length / x_length))
                    angle = 270 - angle
                    self.bullet_sprite.rotation = angle
                
                #Bullet movement
                #Checks to see if a new bullet can be fired
                if self.reset_speed==0:
                    #Function to move bullet
                    def update(dt):
                        #Calculates rotation in radians
                        rad = math.radians(self.bullet_sprite.rotation)
                        #Finds the angle with the vertical and horizontal components
                        cosAngle = math.cos(rad)
                        sinAngle = math.sin(rad)
                        #Adds the component to the vertical and hoizontal distances
                        self.bullet_sprite.y += cosAngle * 500 * dt
                        self.bullet_sprite.x += sinAngle * 500 * dt
                        #Prevents acceleration of bullet
                        self.reset_speed = self.reset_speed + 1
                        #Checks for collision
                        enemy_object.collision()
                    #Runs movement function
                    pyglet.clock.schedule_interval(update, 1 / 60.0)


                
    #Collision Positions
    def get_position(self):
        position_array=[self.bullet_sprite.x,self.bullet_sprite.y,self.bullet_sprite]
        return (position_array)
    

class enemy:
    def __init__(self):
        self.enemy_image = pyglet.resource.image("enemy.png")
        self.enemy_image.width = 150
        self.enemy_image.height = 150
        self.enemy_image.anchor_x = self.enemy_image.width / 2
        self.enemy_image.anchor_y = self.enemy_image.height / 2
        self.enemy_sprite = pyglet.sprite.Sprite(self.enemy_image, x=window_w / 5, y=window_h / 5)

        self.enemy_turret_image = pyglet.resource.image("enemy_turret.png")
        self.enemy_turret_image.width = self.enemy_image.width / 3
        self.enemy_turret_image.height = (self.enemy_image.height / 3) * 2
        self.enemy_turret_image.anchor_x = self.enemy_turret_image.width / 2
        self.enemy_turret_image.anchor_y = self.enemy_turret_image.height - 15
        self.enemy_turret_sprite = pyglet.sprite.Sprite(self.enemy_turret_image, x=self.enemy_sprite.x, y=self.enemy_sprite.y)

        self.enemy_bullet_image = pyglet.resource.image("bullet.png")
        self.enemy_bullet_image.width = 42
        self.enemy_bullet_image.height = 67
        self.enemy_bullet_image.anchor_x = self.enemy_bullet_image.width / 2
        self.enemy_bullet_image.anchor_y = 0
        self.enemy_bullet_sprite = pyglet.sprite.Sprite(self.enemy_bullet_image, x=window_w / 2, y=(window_h * 3) / 4)
        self.enemy_bullet_sprite.visible = False

        self.explode_image = pyglet.resource.image("explode.png")
        self.explode_image.width = 150
        self.explode_image.height = 150
        self.explode_image.anchor_x = self.explode_image.width / 2
        self.explode_image.anchor_y = self.explode_image.height / 2
        self.explode = pyglet.sprite.Sprite(self.explode_image, x=window_w / 5, y=window_h / 5)
        self.explode.visible = False

        self.count=0
        

    def load_enemy(self):
        self.enemy_sprite.draw()

        self.explode.draw()
        

    def move_enemy(self):
        def tank_move(dt, control,value,direction,turn):
            #2-Decides wether to change y or x axis
            if direction=="y":
                control.y=control.y+ value
            elif direction=="x":
                control.x=control.x+ value
            #Counts up
            self.count=self.count+1
            if turn=="Up":
                if self.count>100: # Turn Right
                    pyglet.clock.unschedule (tank_move)
                    self.count=0
                    pyglet.clock.schedule_interval(tank_move, 1/60, self.enemy_sprite, 2, "y","Right")
            #3-Turns right when the counter is high enough
            elif turn=="Right":
                if self.count>100: # Turn Down
                    #4- Stops moving up, resets counter and turns right
                    pyglet.clock.unschedule (tank_move)
                    self.count=0
                    pyglet.clock.schedule_interval(tank_move, 1/60, self.enemy_sprite, 2, "x","Down")
            #4-Process repeats with other directions
            elif turn=="Down":
                if self.count>100: # Turn Left
                    pyglet.clock.unschedule (tank_move)
                    self.count=0
                    pyglet.clock.schedule_interval(tank_move, 1/60, self.enemy_sprite, -2, "y","Left")
            elif turn=="Left":
                if self.count>100: #Turn Up
                    pyglet.clock.unschedule (tank_move)
                    self.count=0
                    pyglet.clock.schedule_interval(tank_move, 1/60, self.enemy_sprite, -2, "x","Up")
        #1-Goes up
        pyglet.clock.schedule_interval(tank_move, 1/60, self.enemy_sprite, 1, "y","Right")

    def collision(self):
        positions=bullet_object.get_position()
        bullet_sprite_x=positions[0]
        bullet_sprite_y=positions[1]
        bullet_sprite=positions[2]
        if (bullet_sprite_y < (self.enemy_sprite.y + (self.enemy_image.height / 2))) and (bullet_sprite_y > (self.enemy_sprite.y - (self.enemy_image.height / 2)))and (bullet_sprite_x < (self.enemy_sprite.x + (self.enemy_image.width/ 2))) and (bullet_sprite_x > (self.enemy_sprite.x - (self.enemy_image.width/ 2))):
            self.enemy_sprite.visible = False
            bullet_sprite.visible = False
            self.explode.x = self.enemy_sprite.x
            self.explode.y = self.enemy_sprite.y
            self.explode.visible = True




@window.event
def on_draw():
    window.clear()
    bullet_object.load_bullet()
    enemy_object.load_enemy()
    
    
    

tank_object = game()
bullet_object = game()
enemy_object=enemy()
enemy_object.move_enemy()
pyglet.app.run()
