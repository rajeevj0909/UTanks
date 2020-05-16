import pyglet
from pyglet.window import mouse
import math
import random
import time
from tkinter import *

class menu:
    def __init__(self):
        self.game_play=game_play()
        self.leaderboard=leaderboard()

    def window(self):
        window_menu = pyglet.window.Window(width=1000, height=800, fullscreen=False)
        self.menu_image = pyglet.image.load("menu.png")
        self.menu_image.width = 1280
        self.menu_image.height = 720
        self.menu_sprite = pyglet.sprite.Sprite(self.menu_image)

        @window_menu.event
        def on_draw():
            window_menu.clear()
            self.menu_sprite.draw()

        @window_menu.event
        def on_mouse_motion(x, y, dx, dy):
            if (150<x and x<840 and 370<y and y<460)or (150 < x and x < 840 and 250 < y and y < 340) or (150 < x and x < 840 and 85 < y and y < 205):
                cursor = window_menu.get_system_mouse_cursor(window_menu.CURSOR_HAND)
                window_menu.set_mouse_cursor(cursor)
            else:
                cursor = window_menu.get_system_mouse_cursor(window_menu.CURSOR_DEFAULT)
                window_menu.set_mouse_cursor(cursor)

        @window_menu.event
        def on_mouse_press(x, y, button, modifiers):
            if button == mouse.LEFT:
                if 150 < x and x < 840 and 370 < y and y < 460:
                    self.play_game_button(window_menu)
                elif 150 < x and x < 840 and 250 < y and y < 340:
                    self.leaderboard_button(window_menu)
                elif 150 < x and x < 840 and 85 < y and y < 205:
                    self.help_button(window_menu)

    def play_game_button(self,window_menu):
        print("Play game")
        #window_menu.close()
        
        #RUNS gameplay
        self.game_play.window()

    def leaderboard_button(self,window_menu):
        print("Leaderboard")
        #window_menu.close()
        #Runs the leaderboard_window in leaderboard class
        self.leaderboard.leaderboard_window()

    def help_button(self,window_menu):
        print("Help")
        #window_menu.close()

class leaderboard:
    def __init__(self):
        #Allows list of scores to be kept inside
        self.leaderboard_list=[]
        self.score=40

    #Creates the window and draws it
    def leaderboard_window(self):
        leaderboard_window = pyglet.window.Window(width=1000, height=800, fullscreen=False)
        
        
      #Opens the window
        self.leaderboard_list=[]
        file = open("Leaderboard.txt","r")
        column  = file.readlines()
        for line in column:
            line = line.split("\n")
            line.pop(1)
            separated=line[0].split("@@")
            (separated[0])=int(separated[0])
            self.leaderboard_list.append(separated)
        file.close()
        #Sorts the list
        print("\n\n")
        self.leaderboard_list.sort(reverse=True)
        while len(self.leaderboard_list)>10:
            self.leaderboard_list.pop()

        #Creates one label to draw onto the leaderbaord
        label = ""
        #Goes through each person's name and score and joins it to the label
        for entry in self.leaderboard_list:
            name=str(entry[1])
            score=str(entry[0])
            label=label+name+": "+score+"\n"
        #Creates a title
        leaderboard_title = pyglet.text.Label("Leaderboard:", font_name="Arial", font_size=100, x=500, y=700,
                                              anchor_x="center", anchor_y="center")
        #Creates the list of names, multiline lists each item
        entries = pyglet.text.Label(label, font_name="Arial", font_size=33, x=600, y=330, anchor_x="center",
                                    anchor_y="center", width=500, multiline=True)
        @leaderboard_window.event #Draws title and leaderboard list onto window
        def on_draw():
            leaderboard_window.clear()
            leaderboard_title.draw()
            entries.draw()

#GAMEPLAY CLASS
class game_play:
    #Names all the other classes to refer back to them
    def __init__(self):
        self.user=user()
        self.bullet = bullet()
        self.enemy=enemy()
        self.walls=walls()
        self.leaderboard=leaderboard()

        self.user_health = 100
        self.score=0

    #Creates the window
    def window(self):
        window = pyglet.window.Window(width=1280, height=720, fullscreen=False)
        cursor = window.get_system_mouse_cursor(window.CURSOR_CROSSHAIR)
        window.set_mouse_cursor(cursor)
        self.background=pyglet.image.load("background.jpg")
        self.background.width = 1280
        self.background.height = 720
        self.background_sprite=pyglet.sprite.Sprite(self.background)
        #Consistantly updates score and health
        pyglet.clock.schedule_interval(self.update_attributes, 1 / 60.0)

        #Loads all 3 classes
        @window.event
        def on_draw():
            window.clear()
            self.background_sprite.draw()
            self.user.load_tank(window,self.bullet,self.enemy,self.user_health,self.score)
            self.bullet.load_bullet(window,self.user,self.enemy,self.leaderboard,self.user_health,self.score)
            self.enemy.load_enemy(window,self.user,self.bullet,self.user_health,self.score)
            self.walls.load_wall(window,self.user,self.bullet,self.enemy,self.user_health,self.score)
            #Creates labels wit the content, font, size, position and anchor
            health1 = pyglet.text.Label("Health:", font_name="Ariel", font_size=30, x=80, y=670, anchor_x="center", anchor_y="center")
            health2 = pyglet.text.Label(str(self.user_health), font_name="Ariel", font_size=30, x=180, y=670, anchor_x="center", anchor_y="center")
            score1 = pyglet.text.Label("Score:", font_name="Ariel", font_size=30, x=80, y=600, anchor_x="center", anchor_y="center")
            score2 = pyglet.text.Label(str(self.score), font_name="Ariel", font_size=30, x=180, y=600, anchor_x="center", anchor_y="center")
            health1.draw()
            health2.draw()
            score1.draw()
            score2.draw()

        #Starts the movement
        enemy_list=self.enemy.get_enemies()
        enemies=enemy_list[0]
        enemy_turrets = enemy_list[1]
        #Goes through every enemy to send into the move enemy and fireback methods
        for number in range(4):
            enemy_sprite=enemies[number]
            enemy_turret_sprite=enemy_turrets[number]
            self.enemy.move_enemy(window,self.user,self.bullet,enemy_sprite,enemy_turret_sprite,number,self.user_health,self.score)
            self.enemy.fire_back(window,self.user,self.bullet,enemy_sprite,enemy_turret_sprite,self.leaderboard,self.user_health,self.score)
            
    def update_attributes(self,dt):
        self.user_health=self.enemy.health
        self.score = self.enemy.score

    
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

    def load_tank(self,window,bullet,enemy,user_health,score):
        self.tank_sprite.draw()
        self.turret_sprite.draw()

        #Tank Movement
        @window.event
        def on_text_motion(motion):
            def wall_check(tank_sprite,tank_image,x_steps,y_steps,rotate,sign):
                if   (tank_sprite.x+tank_image.width/2>250  and tank_sprite.x-tank_image.width/2<270)  and  (tank_sprite.y+tank_image.height/2>135 and tank_sprite.y-tank_image.height/2<585):#Main1
                    if x_steps==0:
                        y_steps += 10
                    if y_steps==0:
                        x_steps += 10
                    sign = sign * -1
                elif (tank_sprite.x+tank_image.width/2>1030 and tank_sprite.x-tank_image.width/2<1050) and  (tank_sprite.y+tank_image.height/2>135 and tank_sprite.y-tank_image.height/2<585):#Main2
                    if x_steps==0:
                        y_steps += 10
                    if y_steps==0:
                        x_steps += 10
                    sign = sign * -1
                elif (tank_sprite.x+tank_image.width/2>260  and tank_sprite.x-tank_image.width/2<510)  and  (tank_sprite.y+tank_image.height/2>440 and tank_sprite.y-tank_image.height/2<460):#Left2
                    if x_steps==0:
                        y_steps += 10
                    if y_steps==0:
                        x_steps += 10
                    sign = sign * -1
                elif (tank_sprite.x+tank_image.width/2>260  and tank_sprite.x-tank_image.width/2<510)  and  (tank_sprite.y+tank_image.height/2>240 and tank_sprite.y-tank_image.height/2<260):#Left1
                    if x_steps==0:
                        y_steps += 10
                    if y_steps==0:
                        x_steps += 10
                    sign = sign * -1
                elif (tank_sprite.x+tank_image.width/2>800  and tank_sprite.x-tank_image.width/2<1050) and  (tank_sprite.y+tank_image.height/2>440 and tank_sprite.y-tank_image.height/2<460):#Right2
                    if x_steps==0:
                        y_steps += 10
                    if y_steps==0:
                        x_steps += 10
                    sign = sign * -1
                elif (tank_sprite.x+tank_image.width/2>800  and tank_sprite.x-tank_image.width/2<1050) and  (tank_sprite.y+tank_image.height/2>240 and tank_sprite.y-tank_image.height/2<260):#Right1
                    if x_steps==0:
                        y_steps += 10
                    if y_steps==0:
                        x_steps += 10
                    sign = sign * -1
                self.tank_sprite.x =self.tank_sprite.x+(x_steps*sign)
                self.tank_sprite.y =self.tank_sprite.y+(y_steps*sign)
                self.tank_sprite.rotation=rotate
            
            if motion == pyglet.window.key.MOTION_DOWN:
                if self.tank_sprite.y>=(self.tank_image.height/2):
                    wall_check(self.tank_sprite,self.tank_image,0,10,180,-1)
            elif (motion == pyglet.window.key.MOTION_UP):
                if self.tank_sprite.y<=720-(self.tank_image.height/2):
                    wall_check(self.tank_sprite,self.tank_image,0,10,0,1)
            elif (motion == pyglet.window.key.MOTION_LEFT):
                if self.tank_sprite.x>=(self.tank_image.width/2):
                    wall_check(self.tank_sprite,self.tank_image,10,0,270,-1)
            elif (motion == pyglet.window.key.MOTION_RIGHT):
                if self.tank_sprite.x<=1280-(self.tank_image.width/2):
                    wall_check(self.tank_sprite,self.tank_image,10,0,90,1)
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
            elif x_length < 0:
                angle = math.degrees(math.atan(y_length / x_length))
                angle = 90 - angle
                self.turret_sprite.rotation = angle
            else:
                pass

    #Collision Positions
    def get_position(self):
        position_array=[self.tank_sprite.x,self.tank_sprite.y,self.tank_sprite]
        return (position_array)

    def get_user(self):
        sprites=[self.tank_sprite,self.turret_sprite,self.tank_image]
        return (sprites)


#BULLET CLASS
class bullet:
    def __init__(self):
        self.bullet_image = pyglet.resource.image("bullet.png")
        self.bullet_image.width = 14
        self.bullet_image.height = 22
        self.bullet_image.anchor_x = self.bullet_image.width / 2
        self.bullet_image.anchor_y = 0
        self.speed = 500

        self.bullet_batch = pyglet.graphics.Batch()
        self.bullet_no = -1
        self.bullets = []
        self.new_bullet = pyglet.sprite.Sprite(self.bullet_image, -50, -50, batch=self.bullet_batch)

    def shoot(self):
        self.bullet_no += 1
        self.bullets.append(pyglet.sprite.Sprite(self.bullet_image, -50, -50, batch=self.bullet_batch))
        self.bullet_batch.draw()
        return(self.bullets[self.bullet_no])

    def load_bullet(self,window,user,enemy,leaderboard,user_health,score):
        self.shoot()
        #Shooting
        @window.event
        def on_mouse_press(x, y, button, modifiers):
            if button == mouse.LEFT:
                current_bullet = bullet.shoot(self)
                positions = user.get_position()
                tank_sprite_x=positions[0]
                tank_sprite_y = positions[1]
                current_bullet.x = tank_sprite_x
                current_bullet.y = tank_sprite_y
                bullet_x = current_bullet.x
                bullet_y = current_bullet.y
                mouse_x = x
                mouse_y = y
                x_length = mouse_x - bullet_x
                y_length = mouse_y - bullet_y
                #Bullet rotation
                if x_length > 0:
                    angle = math.degrees(math.atan(y_length / x_length))
                    angle = 90 - angle
                    current_bullet.rotation = angle
                elif x_length < 0:
                    angle = math.degrees(math.atan(y_length / x_length))
                    angle = 270 - angle
                    current_bullet.rotation = angle
                #Bullet movement
                def update(dt):
                    bullet_life=True
                    rad = math.radians(current_bullet.rotation)
                    cosAngle = math.cos(rad)
                    sinAngle = math.sin(rad)
                    current_bullet.y += cosAngle * self.speed * dt
                    current_bullet.x += sinAngle * self.speed * dt
                    position_array = [current_bullet.x, current_bullet.y, current_bullet]
                    enemy.collision(position_array,user,"user",window,leaderboard,user_health,score)
                    self.wall_collision(update,current_bullet,cosAngle,sinAngle,bullet_life)
                    self.block_collision(update,current_bullet,cosAngle,sinAngle,bullet_life)
                pyglet.clock.schedule_interval(update, 1 / 60.0)

    def wall_collision(self,update,current_bullet,cosAngle,sinAngle,bullet_life):
        def stop(update,current_bullet):
            pyglet.clock.unschedule(update)
            current_bullet.x=-100
            current_bullet.y=-100
        if current_bullet.x<self.bullet_image.height:#Left wall
            if bullet_life==False:
                stop(update,current_bullet)
            else:
                pyglet.clock.unschedule(update)
                bullet_life=False
                def update(dt):
                    position_array = [current_bullet.x, current_bullet.y, current_bullet]
                    current_bullet.y += cosAngle * self.speed * dt
                    current_bullet.x -= sinAngle * self.speed * dt
                    #enemy.collision(position_array)
                    self.wall_collision(update,current_bullet,cosAngle,sinAngle,bullet_life)
                    self.block_collision(update,current_bullet,cosAngle,sinAngle,bullet_life)
                pyglet.clock.schedule_interval(update, 1 / 60.0)
        elif current_bullet.x>1280-self.bullet_image.height:#Right wall
            if bullet_life==False:
                stop(update,current_bullet)
            else:
                pyglet.clock.unschedule(update)
                bullet_life=False
                def update(dt):
                    position_array = [current_bullet.x, current_bullet.y, current_bullet]
                    current_bullet.y += cosAngle * self.speed * dt
                    current_bullet.x -= sinAngle * self.speed * dt
                    #enemy.collision(position_array)
                    self.wall_collision(update,current_bullet,cosAngle,sinAngle,bullet_life)
                    self.block_collision(update,current_bullet,cosAngle,sinAngle,bullet_life)
                pyglet.clock.schedule_interval(update, 1 / 60.0)
        elif current_bullet.y<0:#Bottom wall
            if bullet_life==False:
                stop(update,current_bullet)
            else:
                pyglet.clock.unschedule(update)
                bullet_life=False
                def update(dt):
                    position_array = [current_bullet.x, current_bullet.y, current_bullet]
                    current_bullet.y -= cosAngle * self.speed * dt
                    current_bullet.x += sinAngle * self.speed * dt
                    #enemy.collision(position_array)
                    self.wall_collision(update,current_bullet,cosAngle,sinAngle,bullet_life)
                    self.block_collision(update,current_bullet,cosAngle,sinAngle,bullet_life)
                pyglet.clock.schedule_interval(update, 1 / 60.0)
        elif current_bullet.y>720:#Top wall
            if bullet_life==False:
                stop(update,current_bullet)
            else:
                pyglet.clock.unschedule(update)
                bullet_life=False
                def update(dt):
                    position_array = [current_bullet.x, current_bullet.y, current_bullet]
                    current_bullet.y -= cosAngle * self.speed * dt
                    current_bullet.x += sinAngle * self.speed * dt
                    #enemy.collision(position_array)
                    self.wall_collision(update,current_bullet,cosAngle,sinAngle,bullet_life)
                    self.block_collision(update,current_bullet,cosAngle,sinAngle,bullet_life)
                pyglet.clock.schedule_interval(update, 1 / 60.0)
            


    def block_collision(self,update,current_bullet,cosAngle,sinAngle,bullet_life):
        def stop(update,current_bullet):
            pyglet.clock.unschedule(update)
            current_bullet.x=-100
            current_bullet.y=-10
        if (current_bullet.x>250 and current_bullet.x<270) and  (current_bullet.y>135 and current_bullet.y<585):#Main1
            if bullet_life==False:
                stop(update,current_bullet)
            else: 
                pyglet.clock.unschedule(update)
                bullet_life=False
                def update(dt):
                    position_array = [current_bullet.x, current_bullet.y, current_bullet]
                    current_bullet.y += cosAngle * self.speed * dt
                    current_bullet.x -= sinAngle * self.speed * dt
                    #enemy.collision(position_array)
                    self.wall_collision(update,current_bullet,cosAngle,sinAngle,bullet_life)
                    self.block_collision(update,current_bullet,cosAngle,sinAngle,bullet_life)
                pyglet.clock.schedule_interval(update, 1 / 60.0)
        elif (current_bullet.x>1030 and current_bullet.x<1050) and  (current_bullet.y>135 and current_bullet.y<585):#Main2
            if bullet_life==False:
                stop(update,current_bullet)
            else:
                pyglet.clock.unschedule(update)
                bullet_life=False
                def update(dt):
                    position_array = [current_bullet.x, current_bullet.y, current_bullet]
                    current_bullet.y += cosAngle * self.speed * dt
                    current_bullet.x -= sinAngle * self.speed * dt
                    #enemy.collision(position_array)
                    self.wall_collision(update,current_bullet,cosAngle,sinAngle,bullet_life)
                    self.block_collision(update,current_bullet,cosAngle,sinAngle,bullet_life)
                pyglet.clock.schedule_interval(update, 1 / 60.0)
        elif (current_bullet.x>260 and current_bullet.x<510) and  (current_bullet.y>440 and current_bullet.y<460):#Left2
            if bullet_life==False:
                stop(update,current_bullet)
            else:
                pyglet.clock.unschedule(update)
                bullet_life=False
                def update(dt):
                    position_array = [current_bullet.x, current_bullet.y, current_bullet]
                    current_bullet.y -= cosAngle * self.speed * dt
                    current_bullet.x += sinAngle * self.speed * dt
                    #enemy.collision(position_array)
                    self.wall_collision(update,current_bullet,cosAngle,sinAngle,bullet_life)
                    self.block_collision(update,current_bullet,cosAngle,sinAngle,bullet_life)
                pyglet.clock.schedule_interval(update, 1 / 60.0)
        elif (current_bullet.x>260 and current_bullet.x<510) and  (current_bullet.y>240 and current_bullet.y<260):#Left1
            if bullet_life==False:
                stop(update,current_bullet)
            else:
                pyglet.clock.unschedule(update)
                bullet_life=False
                def update(dt):
                    position_array = [current_bullet.x, current_bullet.y, current_bullet]
                    current_bullet.y -= cosAngle * self.speed * dt
                    current_bullet.x += sinAngle * self.speed * dt
                    #enemy.collision(position_array)
                    self.wall_collision(update,current_bullet,cosAngle,sinAngle,bullet_life)
                    self.block_collision(update,current_bullet,cosAngle,sinAngle,bullet_life)
                pyglet.clock.schedule_interval(update, 1 / 60.0)
        elif (current_bullet.x>800 and current_bullet.x<1050) and  (current_bullet.y>440 and current_bullet.y<460):#Right2
            if bullet_life==False:
                stop(update,current_bullet)
            else:
                pyglet.clock.unschedule(update)
                bullet_life=False
                def update(dt):
                    position_array = [current_bullet.x, current_bullet.y, current_bullet]
                    current_bullet.y -= cosAngle * self.speed * dt
                    current_bullet.x += sinAngle * self.speed * dt
                    #enemy.collision(position_array)
                    self.wall_collision(update,current_bullet,cosAngle,sinAngle,bullet_life)
                    self.block_collision(update,current_bullet,cosAngle,sinAngle,bullet_life)
                pyglet.clock.schedule_interval(update, 1 / 60.0)
        elif (current_bullet.x>800 and current_bullet.x<1050) and  (current_bullet.y>240 and current_bullet.y<260):#Right1
            if bullet_life==False:
                stop(update,current_bullet)
            else:
                pyglet.clock.unschedule(update)
                bullet_life=False
                def update(dt):
                    position_array = [current_bullet.x, current_bullet.y, current_bullet]
                    current_bullet.y -= cosAngle * self.speed * dt
                    current_bullet.x += sinAngle * self.speed * dt
                    #enemy.collision(position_array)
                    self.wall_collision(update,current_bullet,cosAngle,sinAngle,bullet_life)
                    self.block_collision(update,current_bullet,cosAngle,sinAngle,bullet_life)
                pyglet.clock.schedule_interval(update, 1 / 60.0)


#ENEMY CLASS
class enemy:
    def __init__(self):
        self.enemy_image = pyglet.resource.image("enemy.png")
        self.enemy_image.width = 100
        self.enemy_image.height = 100
        self.enemy_image.anchor_x = self.enemy_image.width / 2
        self.enemy_image.anchor_y = self.enemy_image.height / 2
        self.enemy_batch = pyglet.graphics.Batch()
        self.enemies = []
        self.enemy_sprite = pyglet.sprite.Sprite(self.enemy_image, -50, -50, batch=self.enemy_batch)
        self.enemies.append(pyglet.sprite.Sprite(self.enemy_image, 190, 75, batch=self.enemy_batch))
        self.enemies.append(pyglet.sprite.Sprite(self.enemy_image, 190, 645, batch=self.enemy_batch))
        self.enemies.append(pyglet.sprite.Sprite(self.enemy_image, 730, 75, batch=self.enemy_batch))
        self.enemies.append(pyglet.sprite.Sprite(self.enemy_image, 730, 645, batch=self.enemy_batch))

        self.enemy_turret_image = pyglet.resource.image("enemy_turret.png")
        self.enemy_turret_image.width = self.enemy_image.width / 3
        self.enemy_turret_image.height = (self.enemy_image.height / 3) * 2
        self.enemy_turret_image.anchor_x = self.enemy_turret_image.width / 2
        self.enemy_turret_image.anchor_y = self.enemy_turret_image.height - 15
        self.enemy_turret_batch = pyglet.graphics.Batch()
        self.enemy_turrets = []
        self.enemy__turret_sprite = pyglet.sprite.Sprite(self.enemy_turret_image, x=self.enemy_sprite.x, y=self.enemy_sprite.y, batch=self.enemy_turret_batch)
        self.enemy_turrets.append(pyglet.sprite.Sprite(self.enemy_turret_image,x=self.enemies[0].x, y=self.enemies[0].y, batch=self.enemy_turret_batch))
        self.enemy_turrets.append(pyglet.sprite.Sprite(self.enemy_turret_image,x=self.enemies[1].x, y=self.enemies[1].y, batch=self.enemy_turret_batch))
        self.enemy_turrets.append(pyglet.sprite.Sprite(self.enemy_turret_image,x=self.enemies[2].x, y=self.enemies[2].y, batch=self.enemy_turret_batch))
        self.enemy_turrets.append(pyglet.sprite.Sprite(self.enemy_turret_image,x=self.enemies[3].x, y=self.enemies[3].y, batch=self.enemy_turret_batch))

        self.tank_speed=4
        self.bullet_speed=200
        self.score =0
        self.health=100

    def load_enemy(self,window,user,bullet,user_health,score):
        self.enemy_batch.draw()
        self.enemy_turret_batch.draw()
        for number in range(4):
            enemy_turret_sprite = self.enemy_turrets[number]
            positions = user.get_position()
            turret_x = enemy_turret_sprite.x
            turret_y = enemy_turret_sprite.y
            tank_sprite_x = positions[0]
            tank_sprite_y = positions[1]
            x_length = tank_sprite_x - turret_x
            y_length = tank_sprite_y - turret_y
            if x_length > 0:
                angle = math.degrees(math.atan(y_length / x_length))
                angle = 270 - angle
                enemy_turret_sprite.rotation = angle
            elif x_length < 0:
                angle = math.degrees(math.atan(y_length / x_length))
                angle = 90 - angle
                enemy_turret_sprite.rotation = angle
            else:
                pass
            

    def move_enemy(self,window,user,bullet,enemy_sprite,enemy_turret_sprite,number,user_health,score):
        count_x= enemy_sprite.x
        count_y= enemy_sprite.y
        number+=1
        def tank_move(dt, enemy_sprite,value,direction,enemy_turret_sprite,count_x,count_y,number):
            if number % 2 == 0:
                start=0
            else:
                start=580
            if direction == "y":
                enemy_sprite.y += value
                enemy_turret_sprite.y += value
                if enemy_sprite.y - count_y > start:  # Turn right
                    pyglet.clock.unschedule(tank_move)
                    pyglet.clock.schedule_interval(tank_move, 1 / 60, enemy_sprite, self.tank_speed, "x",enemy_turret_sprite, count_x, count_y, number)
                    enemy_sprite.rotation = 90
                elif enemy_sprite.y - count_y < start-580:  # Turn left
                    pyglet.clock.unschedule(tank_move)
                    pyglet.clock.schedule_interval(tank_move, 1 / 60, enemy_sprite, -1 * self.tank_speed, "x",enemy_turret_sprite, count_x, count_y, number)
                    enemy_sprite.rotation = 270
            elif direction == "x":
                enemy_sprite.x += value
                enemy_turret_sprite.x += value
                if enemy_sprite.x - count_x > 384:  # Turn down
                    pyglet.clock.unschedule(tank_move)
                    pyglet.clock.schedule_interval(tank_move, 1 / 60, enemy_sprite, -1 * self.tank_speed, "y",enemy_turret_sprite, count_x, count_y, number)
                    enemy_sprite.rotation = 180
                elif enemy_sprite.x - count_x < 0:  # Turn up
                    pyglet.clock.unschedule(tank_move)
                    pyglet.clock.schedule_interval(tank_move, 1 / 60, enemy_sprite, self.tank_speed, "y",enemy_turret_sprite, count_x, count_y, number)
                    enemy_sprite.rotation = 0
        pyglet.clock.schedule_interval(tank_move, 1 / 60, enemy_sprite, self.tank_speed, "y", enemy_turret_sprite,count_x, count_y, number)

    def fire_back(self,window,user,bullet,enemy_sprite,enemy_turret_sprite,leaderboard,user_health,score):
        self.random_int = random.randint(2, 5)
        user_sprites=user.get_user()
        tank_sprite=user_sprites[0]
        def fire(dt,tank_sprite):
            if enemy_sprite.visible==True:
                current_bullet = bullet.shoot()
                positions = user.get_position()
                current_bullet.x = enemy_sprite.x
                current_bullet.y = enemy_sprite.y
                bullet_x = current_bullet.x
                bullet_y = current_bullet.y
                tank_sprite_x = positions[0]
                tank_sprite_y = positions[1]
                x_length = tank_sprite_x - bullet_x
                y_length = tank_sprite_y - bullet_y
                # Bullet rotation
                if x_length > 0:
                    angle = math.degrees(math.atan(y_length / x_length))
                    angle = 90 - angle
                    current_bullet.rotation = angle
                elif x_length< 0:
                    angle = math.degrees(math.atan(y_length / x_length))
                    angle = 270 - angle
                    current_bullet.rotation = angle
                # Bullet movement
                def update(dt):
                    bullet_life=True
                    rad = math.radians(current_bullet.rotation)
                    cosAngle = math.cos(rad)
                    sinAngle = math.sin(rad)
                    current_bullet.y += cosAngle * self.bullet_speed * dt
                    current_bullet.x += sinAngle * self.bullet_speed * dt
                    position_array = [current_bullet.x, current_bullet.y, current_bullet]
                    bullet.wall_collision(update,current_bullet,cosAngle,sinAngle,bullet_life)
                    bullet.block_collision(update,current_bullet,cosAngle,sinAngle,bullet_life)
                    self.collision(position_array,user,"enemy",window,leaderboard,user_health,score)
                pyglet.clock.schedule_interval(update, 1 / 60.0)
        pyglet.clock.schedule_interval(fire, self.random_int,tank_sprite)


    def collision(self,positions,user,bullet_origin,window,leaderboard,user_health,score):
        bullet_sprite_x=positions[0]
        bullet_sprite_y=positions[1]
        bullet_sprite=positions[2]
        if bullet_origin=="user":
            for number in range(4):
                enemy_sprite=self.enemies[number]
                enemy_turret_sprite = self.enemy_turrets[number]
                if (bullet_sprite_y < (enemy_sprite.y + (self.enemy_image.height / 2))) and (bullet_sprite_y > (enemy_sprite.y - (self.enemy_image.height / 2)))and (bullet_sprite_x < (enemy_sprite.x + (self.enemy_image.width/ 2))) and (bullet_sprite_x > (enemy_sprite.x - (self.enemy_image.width/ 2)))and (enemy_sprite.visible==True):
                    enemy_sprite.visible = False
                    enemy_turret_sprite.visible = False
                    bullet_sprite.visible = False
                    self.score=self.score+10
                    #If the game has started and all the 4 tanks are dead in 1 level
                    if self.score%40==0 and self.score>0:
                        #Pause the game for a second
                        time.sleep(1)
                        #Make all the enemies visible
                        for count in range(4):
                            enemy=self.enemies[count]
                            turret=self.enemy_turrets[count]
                            enemy.visible=True
                            turret.visible=True
        else:
            user_sprites=user.get_user()
            tank_sprite=user_sprites[0]
            turret_sprite=user_sprites[1]
            tank_image=user_sprites[2]
            if (bullet_sprite_y < (tank_sprite.y + (tank_image.height / 2))) and (bullet_sprite_y > (tank_sprite.y - (tank_image.height / 2))) and (bullet_sprite_x < (tank_sprite.x + (tank_image.width / 2))) and (bullet_sprite_x > (tank_sprite.x - (tank_image.width / 2))):
                self.health=self.health#-1
                if self.health<1:
                    self.health=0
                    tank_sprite.visible = False
                    turret_sprite.visible = False
                    bullet_sprite.visible = False
                    window.close()
    
                    top = Tk()
                    # Creates label
                    Label1 = Label(top, text=" Enter User Name")
                    #  Creates textbox with string input
                    textbox = Entry(top, bd=5, textvariable=StringVar())

                    def callback():
                        global username  # Allows me to user username anywhere
                        username = textbox.get()  # Output from textbox
                        top.destroy()  # Closes window

                    # When button clicked, run function callback
                    submit = Button(top, text="Submit", width=10, command=callback)

                    Label1.pack(side=LEFT)  # Puts text on screen
                    textbox.pack()  # Puts textbox on screen
                    submit.pack()  # Puts button on screen
                    top.mainloop()  # Runs the window
                    print(username)

                    #Opens in append mode
                    file = open("Leaderboard.txt","a")
                    file.write(str(self.score)+"@@"+username)#Turned into string
                    print(str(self.score)+"@@"+username)
                    file.write("\n")
                    file.close()

                    leaderboard.leaderboard_window()
                    
    def get_enemies(self):
        #Creates 2D array of lists to send back to gameplay
        enemy_list=[self.enemies,self.enemy_turrets]
        return (enemy_list)
    

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

    def load_wall(self, window, user, bullet, enemy,user_health,score):
        self.wall_sprite_main1.draw()
        self.wall_sprite_main2.draw()
        self.wall_sprite_left1.draw()
        self.wall_sprite_left2.draw()
        self.wall_sprite_right1.draw()
        self.wall_sprite_right2.draw()


start = menu()
start.window()
pyglet.app.run()

