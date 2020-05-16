import pyglet
from pyglet.window import mouse
import math

#GAMEPLAY CLASS
class game_play:
    #Names all the other classes to refer back to them
    def __init__(self):
        self.user=user()
        self.bullet = bullet()
        self.enemy=enemy()
        self.walls=walls()

    #Creates the window
    def window(self):
        window = pyglet.window.Window(width=1280, height=720, fullscreen=False)
        cursor = window.get_system_mouse_cursor(window.CURSOR_CROSSHAIR)
        window.set_mouse_cursor(cursor)
        self.background=pyglet.image.load("background.jpg")
        self.background.width = 1280
        self.background.height = 720
        self.background_sprite=pyglet.sprite.Sprite(self.background)

        #Loads all 3 classes
        @window.event
        def on_draw():
            window.clear()
            self.background_sprite.draw()
            self.user.load_tank(window,self.bullet,self.enemy)
            self.bullet.load_bullet(window,self.user,self.enemy)
            self.enemy.load_enemy(window,self.user,self.bullet)
            self.walls.load_wall(window,self.user,self.bullet,self.enemy)

        #Starts the movement once
        self.enemy.move_enemy(window,self.user,self.bullet)


#USER CLASS
class user:
    def __init__(self):
        self.tank_image = pyglet.resource.image("tank.png")
        self.tank_image.width = 100
        self.tank_image.height = 100
        self.tank_image.anchor_x = self.tank_image.width / 2
        self.tank_image.anchor_y = self.tank_image.height / 2
        self.tank_sprite = pyglet.sprite.Sprite(self.tank_image, x=1280/ 2, y=720/ 2)

        self.turret_image = pyglet.resource.image("turret.png")
        self.turret_image.width = self.tank_image.width / 3
        self.turret_image.height = (self.tank_image.height / 3) * 2
        self.turret_image.anchor_x = self.turret_image.width / 2
        self.turret_image.anchor_y = self.turret_image.height - 15
        self.turret_sprite = pyglet.sprite.Sprite(self.turret_image, x=self.tank_sprite.x, y=self.tank_sprite.y)

        self.steps = 10

    def load_tank(self,window,bullet,enemy):
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
                if self.tank_sprite.y<=720-(self.tank_image.height/2):
                    self.tank_sprite.y += self.steps
                    self.tank_sprite.rotation=0
            elif (motion == pyglet.window.key.MOTION_LEFT):
                if self.tank_sprite.x>=(self.tank_image.width/2):
                    self.tank_sprite.x -= self.steps
                    self.tank_sprite.rotation=270
            elif (motion == pyglet.window.key.MOTION_RIGHT):
                if self.tank_sprite.x<=1280-(self.tank_image.width/2):
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

    #Collision Positions
    def get_position(self):
        position_array=[self.tank_sprite.x,self.tank_sprite.y,self.tank_sprite]
        return (position_array)

#BULLET CLASS
class bullet:
    def __init__(self):
        self.bullet_image = pyglet.resource.image("bullet.png")
        self.bullet_image.width = 28
        self.bullet_image.height = 45
        self.bullet_image.anchor_x = self.bullet_image.width / 2
        self.bullet_image.anchor_y = 0
        self.bullet_sprite = pyglet.sprite.Sprite(self.bullet_image, x=1280 / 2, y=(720 * 3) / 4)
        self.bullet_sprite.visible = False

        self.reset_speed=0

    def load_bullet(self,window,user,enemy):
        self.bullet_sprite.draw()

        #Shooting
        @window.event
        def on_mouse_press(x, y, button, modifiers):
            if button == mouse.RIGHT:
                self.bullet_sprite.visible = True
                positions = user.get_position()
                tank_sprite_x=positions[0]
                tank_sprite_y = positions[1]
                self.bullet_sprite.x = tank_sprite_x
                self.bullet_sprite.y = tank_sprite_y
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
                if self.reset_speed==0:
                    def update(dt):
                        rad = math.radians(self.bullet_sprite.rotation)
                        cosAngle = math.cos(rad)
                        sinAngle = math.sin(rad)
                        self.bullet_sprite.y += cosAngle * 500*dt
                        self.bullet_sprite.x += sinAngle * 500*dt
                        self.reset_speed=self.reset_speed+1
                        position_array = [self.bullet_sprite.x, self.bullet_sprite.y, self.bullet_sprite]
                        enemy.collision(position_array)
                    pyglet.clock.schedule_interval(update, 1 / 60.0)
    
#ENEMY CLASS
class enemy:
    def __init__(self):
        self.enemy_image = pyglet.resource.image("enemy.png")
        self.enemy_image.width = 100
        self.enemy_image.height = 100
        self.enemy_image.anchor_x = self.enemy_image.width / 2
        self.enemy_image.anchor_y = self.enemy_image.height / 2
        self.enemy_sprite = pyglet.sprite.Sprite(self.enemy_image, x=190, y=75)

        self.enemy_turret_image = pyglet.resource.image("enemy_turret.png")
        self.enemy_turret_image.width = self.enemy_image.width / 3
        self.enemy_turret_image.height = (self.enemy_image.height / 3) * 2
        self.enemy_turret_image.anchor_x = self.enemy_turret_image.width / 2
        self.enemy_turret_image.anchor_y = self.enemy_turret_image.height - 15
        self.enemy_turret_sprite = pyglet.sprite.Sprite(self.enemy_turret_image, x=self.enemy_sprite.x, y=self.enemy_sprite.y)

        self.explode_image = pyglet.resource.image("explode.png")
        self.explode_image.width = 150
        self.explode_image.height = 150
        self.explode_image.anchor_x = self.explode_image.width / 2
        self.explode_image.anchor_y = self.explode_image.height / 2
        self.explode = pyglet.sprite.Sprite(self.explode_image, x=1280 / 5, y=720 / 5)
        self.explode.visible = False

        self.count=0
        self.speed=4

    def load_enemy(self,window,user,bullet):
        self.enemy_sprite.draw()
        self.enemy_turret_sprite.draw()
        self.explode.draw()
        positions = user.get_position()
        turret_x = self.enemy_turret_sprite.x
        turret_y = self.enemy_turret_sprite.y
        tank_sprite_x = positions[0]
        tank_sprite_y = positions[1]
        #Uses user tank as target instead of cursor
        x_length = tank_sprite_x - turret_x
        y_length = tank_sprite_y - turret_y
        if x_length > 0:
            angle = math.degrees(math.atan(y_length / x_length))
            angle = 270 - angle
            self.enemy_turret_sprite.rotation = angle
        else:
            angle = math.degrees(math.atan(y_length / x_length))
            angle = 90 - angle
            self.enemy_turret_sprite.rotation = angle



    def move_enemy(self,window,user,bullet):
        def tank_move(dt, control,value,direction,turn,enemy_turret_sprite):
            if direction=="y":
                control.y += value
                #Also moves turret vertically
                enemy_turret_sprite.y+=value
            elif direction=="x":
                control.x += value
                # Also moves turret vertically
                enemy_turret_sprite.x += value
            self.count=self.count+value
            if turn=="Up":
                if self.count<-380: # Turn Right
                    pyglet.clock.unschedule (tank_move)
                    self.count=0
                    pyglet.clock.schedule_interval(tank_move, 1/60, self.enemy_sprite, self.speed, "y","Right",self.enemy_turret_sprite)
            elif turn=="Right":
                if self.count>580: # Turn Down
                    pyglet.clock.unschedule (tank_move)
                    self.count=0
                    pyglet.clock.schedule_interval(tank_move, 1/60, self.enemy_sprite, self.speed, "x","Down",self.enemy_turret_sprite)
            elif turn=="Down":
                if self.count>380: # Turn Left
                    pyglet.clock.unschedule (tank_move)
                    self.count=0
                    pyglet.clock.schedule_interval(tank_move, 1/60, self.enemy_sprite, -1*self.speed, "y","Left",self.enemy_turret_sprite)
            elif turn=="Left":
                if self.count<-580: #Turn Up
                    pyglet.clock.unschedule (tank_move)
                    self.count=0
                    pyglet.clock.schedule_interval(tank_move, 1/60, self.enemy_sprite, -1*self.speed, "x","Up",self.enemy_turret_sprite)

        pyglet.clock.schedule_interval(tank_move, 1/60, self.enemy_sprite, self.speed, "y","Right",self.enemy_turret_sprite)



    def collision(self,positions):
        bullet_sprite_x=positions[0]
        bullet_sprite_y=positions[1]
        bullet_sprite=positions[2]
        if (bullet_sprite_y < (self.enemy_sprite.y + (self.enemy_image.height / 2))) and (bullet_sprite_y > (self.enemy_sprite.y - (self.enemy_image.height / 2)))and (bullet_sprite_x < (self.enemy_sprite.x + (self.enemy_image.width/ 2))) and (bullet_sprite_x > (self.enemy_sprite.x - (self.enemy_image.width/ 2))):
            self.enemy_sprite.visible = False
            #self.enemy_turret_sprite.visible = False
            bullet_sprite.visible = False
            self.explode.x = self.enemy_sprite.x
            self.explode.y = self.enemy_sprite.y
            self.explode.visible = True

#Walls CLASS
class walls:
    def __init__(self):
        self.wall_image = pyglet.resource.image("wall.png")
        self.wall_image.anchor_x = self.wall_image.width / 2
        self.wall_image.anchor_y = self.wall_image.height / 2

        self.wall_image.width = 20
        self.wall_image.height = 450
        self.wall_sprite_main1 = pyglet.sprite.Sprite(self.wall_image, x=300, y=360)
        self.wall_sprite_main2 = pyglet.sprite.Sprite(self.wall_image, x=1080, y=360)

        self.wall_image.width = 20
        self.wall_image.height = 240
        self.wall_image.anchor_x = 0
        self.wall_sprite_left1 = pyglet.sprite.Sprite(self.wall_image, x=500, y=360+100)
        self.wall_sprite_left2 = pyglet.sprite.Sprite(self.wall_image, x=500, y=360-100)
        self.wall_sprite_right1 = pyglet.sprite.Sprite(self.wall_image, x=1040, y=360+100)
        self.wall_sprite_right2 = pyglet.sprite.Sprite(self.wall_image, x=1040, y=360-100)
        self.wall_sprite_left1.rotation = 90
        self.wall_sprite_left2.rotation = 90
        self.wall_sprite_right1.rotation = 90
        self.wall_sprite_right2.rotation = 90

    def load_wall(self, window, user,bullet, enemy):
        self.wall_sprite_main1.draw()
        self.wall_sprite_main2.draw()
        self.wall_sprite_left1.draw()
        self.wall_sprite_left2.draw()
        self.wall_sprite_right1.draw()
        self.wall_sprite_right2.draw()


#RUNS gameplay
game=game_play()
game.window()
pyglet.app.run()

