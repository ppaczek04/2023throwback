import pygame
from sys import exit
from random import randint
import math #for now just to use cos() ans sin() function in track_player for fly-mob

pygame.init()
main_screen=pygame.display.set_mode((1200,800)) #width,height
pygame.display.set_caption("Gunpan")
main_clock=pygame.time.Clock()


#GLOBAL VARIABLES:
game_status=2 #0-lost 1-running 2-menu
is_sth_pressed=False #Variable for controlling player_animation
curr_room_x=1
curr_room_y=1
max_room_x = 2 # x is horizontal, so upper line of screen
max_room_y = 2 # y is vertical, so left side of screen

intro_timer=0

#FONTS
RioGrande_font=pygame.font.Font('fonts/RioGrande.ttf',72)
Somer_font=pygame.font.Font('fonts/Somer.ttf',36)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_up0=pygame.image.load("graphics/player/player_gun/player_up0_gun.png").convert_alpha()
        player_up1=pygame.image.load("graphics/player/player_gun/player_up1_gun.png").convert_alpha()
        player_up2=pygame.image.load("graphics/player/player_gun/player_up2_gun.png").convert_alpha()
        self.player_up=[player_up0,player_up1,player_up2]
        self.player_up_index=0

        player_down0=pygame.image.load("graphics/player/player_gun/player_down0_gun.png").convert_alpha()
        player_down1=pygame.image.load("graphics/player/player_gun/player_down1_gun.png").convert_alpha()
        player_down2=pygame.image.load("graphics/player/player_gun/player_down2_gun.png").convert_alpha()
        self.player_down=[player_down0,player_down1,player_down2]
        self.player_down_index=0

        player_left1=pygame.image.load("graphics/player/player_gun/player_left1_gun.png").convert_alpha()
        player_left2=pygame.image.load("graphics/player/player_gun/player_left2_gun.png").convert_alpha()
        self.player_left=[player_left1,player_left2]
        self.player_left_index=0

        player_right1=pygame.image.load("graphics/player/player_gun/player_right1_gun.png").convert_alpha()
        player_right2=pygame.image.load("graphics/player/player_gun/player_right2_gun.png").convert_alpha()
        self.player_right=[player_right1,player_right2]
        self.player_right_index=0
       
        self.image=self.player_down[self.player_down_index]
        self.rect=self.image.get_rect(midbottom=(600,400))  

        #parameters of spawned player
        self.direction="down"
        self.player_x_speed=5
        self.player_y_speed=5
        self.reload_time=20
        self.max_hp=3
        self.hp=self.max_hp

    def player_shoot(self):
        keys=pygame.key.get_pressed()

        if self.reload_time>0:
            self.reload_time-=1
        if keys[pygame.K_SPACE] and self.reload_time<=0:
            flying_player_shells.add(Shell(self)) #slef to get player.rect in shell.rect.postion declaration
            self.reload_time=20

    def player_input(self):
        keys=pygame.key.get_pressed()
        if keys[pygame.K_UP] and keys[pygame.K_DOWN]==False and keys[pygame.K_LEFT]==False and keys[pygame.K_RIGHT]==False:
            self.rect.y-=self.player_y_speed
            self.direction="up"
        if keys[pygame.K_UP]==False and keys[pygame.K_DOWN] and keys[pygame.K_LEFT]==False and keys[pygame.K_RIGHT]==False:
            self.rect.y+=self.player_y_speed
            self.direction="down"
        if keys[pygame.K_UP]==False and keys[pygame.K_DOWN]==False and keys[pygame.K_LEFT] and keys[pygame.K_RIGHT]==False:
            self.rect.x-=self.player_x_speed
            self.direction="left"
        if keys[pygame.K_UP]==False and keys[pygame.K_DOWN]==False and keys[pygame.K_LEFT]==False and keys[pygame.K_RIGHT]:
            self.rect.x+=self.player_x_speed
            self.direction="right"
        if keys[pygame.K_UP] and keys[pygame.K_DOWN]==False and keys[pygame.K_LEFT] and keys[pygame.K_RIGHT]==False:
            self.rect.x-=self.player_x_speed*0.71
            self.rect.y-=self.player_y_speed*0.71
            self.direction="top-left" #STRZELANIE W GORE W LEWO NIE DZIALA  !!!!!!!!!!!!!!
        if keys[pygame.K_UP] and keys[pygame.K_DOWN]==False and keys[pygame.K_LEFT]==False and keys[pygame.K_RIGHT]:
            self.rect.x+=self.player_x_speed*0.71
            self.rect.y-=self.player_y_speed*0.71
            self.direction="top-right"
        if keys[pygame.K_UP]==False and keys[pygame.K_DOWN] and keys[pygame.K_LEFT] and keys[pygame.K_RIGHT]==False:
            self.rect.x-=self.player_x_speed*0.71
            self.rect.y+=self.player_y_speed*0.71
            self.direction="bottom-left"
        if keys[pygame.K_UP]==False and keys[pygame.K_DOWN] and keys[pygame.K_LEFT]==False and keys[pygame.K_RIGHT]:
            self.rect.x+=self.player_x_speed*0.71
            self.rect.y+=self.player_y_speed*0.71
            self.direction="bottom-right"

    def animation_state(self):
        #if self.last_pressed_button==pygame.K_DOWN:
        #    self.image=self.player_front[self.player_front_index]
        keys=pygame.key.get_pressed()

        if keys[pygame.K_UP] and keys[pygame.K_DOWN]==False:
            self.player_up_index+=0.1
            if self.player_up_index >= len(self.player_up):
                self.player_up_index=0
            self.image=self.player_up[int(self.player_up_index)]

        if keys[pygame.K_DOWN] and keys[pygame.K_UP]==False:
            self.player_down_index+=0.1
            if self.player_down_index >= len(self.player_down):
                self.player_down_index=0
            self.image=self.player_down[int(self.player_down_index)]

        if keys[pygame.K_LEFT] and keys[pygame.K_RIGHT]==False:
            self.player_left_index+=0.1
            if self.player_left_index >= len(self.player_right):
                self.player_left_index=0
            self.image=self.player_left[int(self.player_left_index)]

        if keys[pygame.K_RIGHT] and keys[pygame.K_LEFT]==False:
            self.player_right_index+=0.1
            if self.player_right_index >= len(self.player_right):
                self.player_right_index=0
            self.image=self.player_right[int(self.player_right_index)]
    
    def player_change_room(self): #a is left top point, b is bottom right point
        global curr_room_x, curr_room_y
        if  self.rect.center[0] >= 500 and self.rect.center[0] <= 700 and self.rect.top <=10:
            if room_doors_exist[curr_room_x][curr_room_y][0]==1: #updoor exists in this room?
                self.rect.x=500
                self.rect.y=700
                curr_room_y-=1
        elif  self.rect.center[0] >= 500 and self.rect.center[0] <= 700 and self.rect.bottom >= 790:
            if room_doors_exist[curr_room_x][curr_room_y][1]==1:#downdoor exists in this room?
                self.rect.x=500
                self.rect.y=100
                curr_room_y+=1
        elif  self.rect.left <= 10 and self.rect.center[1] >= 310  and self.rect.center[1] <= 440:
            if room_doors_exist[curr_room_x][curr_room_y][2]==1: #leftdoor exists in this room?
                self.rect.x=1100
                self.rect.y=370
                curr_room_x-=1
        elif  self.rect.right >= 1190 and self.rect.center[1] >= 310  and self.rect.center[1] <= 440:
            if room_doors_exist[curr_room_x][curr_room_y][3]==1: #rightdoor exists in this room?
                self.rect.x=100
                self.rect.y=370
                curr_room_x+=1
        
        if has_been_spawn_yet_in_room[curr_room_x][curr_room_y]:
                    spawn_enemies_in_room(curr_room_x,curr_room_y)
                    has_been_spawn_yet_in_room[curr_room_x][curr_room_y]=0

    def stay_in_room(self):
        if self.rect.left<0:
            self.rect.left=0
        if self.rect.right>1200:
            self.rect.right=1200
        if self.rect.top<0:
            self.rect.top=0
        if self.rect.bottom>800:
            self.rect.bottom=800

    def take_dmg(self,enemies):
        for mob in enemies:
            if pygame.sprite.collide_rect(self,mob) and mob.time_till_agro_possible<=0:
                self.hp-=mob.attack_power
                mob.time_till_agro_possible=15 # 15 element period after attack when mob moves in opposite direction to player
                if calc_dist_mob_point(self,mob.rect.centerx,mob.rect.centery)!=0:
                    x_dist_to_player=self.rect.centerx-mob.rect.centerx
                    y_dist_to_player=self.rect.centery-mob.rect.centery
                    mob.x_speed = -(x_dist_to_player / calc_dist_mob_point(self,mob.rect.centerx,mob.rect.centery))*5
                    mob.y_speed = -(y_dist_to_player / calc_dist_mob_point(self,mob.rect.centerx,mob.rect.centery))*5
            #print(mob.bounce_time)
            #print(mob.just_attacked)           
            if mob.time_till_agro_possible>0:
                mob.time_till_agro_possible-=1

    def take_dmg_from_shells(self,shells):
        for shell in shells:
            if pygame.sprite.collide_rect(self,shell):
                self.hp-=shell.damage
                shell.kill()
                       
        if self.hp<=0:
            #self.kill()
            global game_status
            game_status=0 
 
    def update(self): #we write function that updates all under-class-functions in one line only.
        self.player_input()
        self.animation_state()
        self.player_change_room()
        self.stay_in_room()
        self.player_shoot()
        self.take_dmg(enemies_from_room[curr_room_x][curr_room_y])
        self.take_dmg_from_shells(flying_enemy_shells)
       
        
class Shell(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()
        shell_def_0=pygame.image.load("graphics/shell/shell_0.png").convert_alpha()
        shell_def_1=pygame.image.load("graphics/shell/shell_1.png").convert_alpha()
        shell_def_2=pygame.image.load("graphics/shell/shell_2.png").convert_alpha()
        shell_def_3=pygame.image.load("graphics/shell/shell_3.png").convert_alpha()
        self.shell_def=[shell_def_0,shell_def_1,shell_def_2,shell_def_3]
        self.shell_def_index=0
        self.timer=20
        self.image=self.shell_def[self.shell_def_index]
        self.rect=self.image.get_rect(center=(player.rect.centerx,player.rect.centery))


        if player.direction=="up":
            self.shot_speed_x=0
            self.shot_speed_y=-20
        elif player.direction=="down":
            self.shot_speed_x=0
            self.shot_speed_y=+20
        elif player.direction=="left":
            self.shot_speed_x=-20
            self.shot_speed_y=0
        elif player.direction=="right":
            self.shot_speed_x=20
            self.shot_speed_y=0
        elif player.direction=="top-left":
            self.shot_speed_x=-20*0.71
            self.shot_speed_y=-20*0.71
        elif player.direction=="top-right":
            self.shot_speed_x=20*0.71
            self.shot_speed_y=-20*0.71
        elif player.direction=="bottom-left":
            self.shot_speed_x=-20*0.71
            self.shot_speed_y=+20*0.71
        elif player.direction=="bottom-right":
            self.shot_speed_x=20*0.71
            self.shot_speed_y=20*0.71


    def animation_state(self):
        if self.shell_def_index <= len(self.shell_def)-0.2:
            self.shell_def_index+=0.2
        self.image=self.shell_def[int(self.shell_def_index)]

    
    def move(self):
        self.rect.x+=self.shot_speed_x
        self.rect.y+=self.shot_speed_y
    

    def still_in_air(self):
        self.timer-=1
        if self.timer<=0:
            self.kill()
        if self.rect.left < 0 or  self.rect.right > 1200 or self.rect.top < 0 or self.rect.bottom > 800:
            self.kill()
    
    def update(self): #we write function that updates all under-class-functions in one line only.
        self.animation_state()
        self.move()
        self.still_in_air()
        

class Fly(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        fly_up_1=pygame.image.load("graphics/enemies/fly/fly_up_1.png").convert_alpha()
        fly_up_2=pygame.image.load("graphics/enemies/fly/fly_up_2.png").convert_alpha()
        self.fly_up=[fly_up_1,fly_up_2]
        self.fly_up_index=0 
        fly_down_1=pygame.image.load("graphics/enemies/fly/fly_down_1.png").convert_alpha()
        fly_down_2=pygame.image.load("graphics/enemies/fly/fly_down_2.png").convert_alpha()
        self.fly_down=[fly_down_1,fly_down_2]
        self.fly_down_index=0 
        fly_left_1=pygame.image.load("graphics/enemies/fly/fly_left_1.png").convert_alpha()
        fly_left_2=pygame.image.load("graphics/enemies/fly/fly_left_2.png").convert_alpha()
        self.fly_left=[fly_left_1,fly_left_2]
        self.fly_left_index=0 
        fly_right_1=pygame.image.load("graphics/enemies/fly/fly_right_1.png").convert_alpha()
        fly_right_2=pygame.image.load("graphics/enemies/fly/fly_right_2.png").convert_alpha()
        self.fly_right=[fly_right_1,fly_right_2]
        self.fly_right_index=0

        self.image=self.fly_down[self.fly_down_index]
        self.rect=self.image.get_rect(center=(100,100))

        #parameters of spawned fly
        self.max_speed=2.5
        self.x_speed=0
        self.y_speed=0
        self.max_hp=3
        self.hp=self.max_hp
        self.attack_power=0.5
        self.time_till_agro_possible=0 # variable being timer for when object attacks player

    
    def track_player(self, player):
        x_dist_to_player=player.rect.centerx-self.rect.centerx
        y_dist_to_player=player.rect.centery-self.rect.centery
       
        if calc_dist_mob_point(self,player.rect.centerx,player.rect.centery)!=0 and self.time_till_agro_possible<=0:
            self.x_speed = (x_dist_to_player / calc_dist_mob_point(self,player.rect.centerx,player.rect.centery)) * self.max_speed
            self.y_speed = (y_dist_to_player / calc_dist_mob_point(self,player.rect.centerx,player.rect.centery)) * self.max_speed

        
        self.rect.centerx+=self.x_speed
        self.rect.centery+=self.y_speed
        #print(f"{(self.x_speed**2+self.y_speed**2)**0.5}")
        #print(f"x:{self.x_speed}")
        #print(f"y=={self.y_speed}")
        #print(self.y_speed)
    

    def animation_state(self,  player):
        x_dist_to_player=player.rect.centerx-self.rect.centerx
        y_dist_to_player=player.rect.centery-self.rect.centery
        if  x_dist_to_player>=0:
            if abs(x_dist_to_player)>=abs(y_dist_to_player):
                self.fly_right_index+=0.1
                if self.fly_right_index >= len(self.fly_right):
                    self.fly_right_index=0
                self.image=self.fly_right[int(self.fly_right_index)]
            elif y_dist_to_player>0:
                self.fly_down_index+=0.1
                if self.fly_down_index >= len(self.fly_down):
                    self.fly_down_index=0
                self.image=self.fly_down[int(self.fly_down_index)]
            else:
                self.fly_up_index+=0.1
                if self.fly_up_index >= len(self.fly_up):
                    self.fly_up_index=0
                self.image=self.fly_up[int(self.fly_up_index)]
        else:
            if abs(x_dist_to_player)>=abs(y_dist_to_player):
                self.fly_left_index+=0.1
                if self.fly_left_index >= len(self.fly_left):
                    self.fly_left_index=0
                self.image=self.fly_left[int(self.fly_left_index)]
            elif y_dist_to_player>0:
                self.fly_down_index+=0.1
                if self.fly_down_index >= len(self.fly_down):
                    self.fly_down_index=0
                self.image=self.fly_down[int(self.fly_down_index)]
            else:
                self.fly_up_index+=0.1
                if self.fly_up_index >= len(self.fly_up):
                    self.fly_up_index=0
                self.image=self.fly_up[int(self.fly_up_index)]


    def take_dmg(self,player_shells):
        for element in player_shells:
            if pygame.sprite.collide_rect(self,element):
                self.hp-=1
                element.kill()
        if self.hp<=0:
            self.kill() 
   

    def update(self):
        self.track_player(player.sprite)
        self.animation_state(player.sprite)
        self.take_dmg(flying_player_shells)


class Snail(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        snail_up_1=pygame.image.load("graphics/enemies/snail/snail_up_1.png").convert_alpha()
        snail_up_2=pygame.image.load("graphics/enemies/snail/snail_up_2.png").convert_alpha()
        self.snail_up=[snail_up_1,snail_up_2]
        self.snail_up_index=0 
        snail_down_1=pygame.image.load("graphics/enemies/snail/snail_down_1.png").convert_alpha()
        snail_down_2=pygame.image.load("graphics/enemies/snail/snail_down_2.png").convert_alpha()
        self.snail_down=[snail_down_1,snail_down_2]
        self.snail_down_index=0 
        snail_left_1=pygame.image.load("graphics/enemies/snail/snail_left_1.png").convert_alpha()
        snail_left_2=pygame.image.load("graphics/enemies/snail/snail_left_2.png").convert_alpha()
        self.snail_left=[snail_left_1,snail_left_2]
        self.snail_left_index=0 
        snail_right_1=pygame.image.load("graphics/enemies/snail/snail_right_1.png").convert_alpha()
        snail_right_2=pygame.image.load("graphics/enemies/snail/snail_right_2.png").convert_alpha()
        self.snail_right=[snail_right_1,snail_right_2]
        self.snail_right_index=0

        self.image=self.snail_down[self.snail_down_index]
        self.rect=self.image.get_rect(center=(100,100))

        #parameters of spawned snail
        self.max_speed=3.5
        self.x_speed=0
        self.y_speed=0
        self.max_hp=5
        self.hp=self.max_hp
        self.attack_power=1

        self.time_till_agro_possible=0
        self.target_tracker_reload_time=40
        self.target_tracker_timer=0 


    def take_dmg(self,player_shells):
        for element in player_shells:
            if pygame.sprite.collide_rect(self,element):
                self.hp-=1
                element.kill()
        if self.hp<=0:
            self.kill() 


    def track_player(self, player):
        x_dist_to_player=player.rect.centerx-self.rect.centerx
        y_dist_to_player=player.rect.centery-self.rect.centery

       
        if self.target_tracker_timer<=0:
            self.target_tracker_timer=self.target_tracker_reload_time
            if abs(x_dist_to_player)>=abs(y_dist_to_player):
                if x_dist_to_player>0:
                    self.x_speed=self.max_speed
                    self.y_speed=0
                else:
                    self.x_speed=-self.max_speed
                    self.y_speed=0
            elif abs(x_dist_to_player)<abs(y_dist_to_player):
                if y_dist_to_player>0:
                    self.x_speed=0
                    self.y_speed=self.max_speed
                else:
                    self.x_speed=0
                    self.y_speed=-self.max_speed

        self.target_tracker_timer-=1
        self.rect.centerx+=self.x_speed
        self.rect.centery+=self.y_speed


    def animation_state(self):
        if self.x_speed>0:
            self.snail_right_index+=0.1
            if self.snail_right_index >= len(self.snail_right):
                self.snail_right_index=0
            self.image=self.snail_right[int(self.snail_right_index)]
        elif self.x_speed<0:
            self.snail_left_index+=0.1
            if self.snail_left_index >= len(self.snail_left):
                self.snail_left_index=0
            self.image=self.snail_left[int(self.snail_left_index)]
        elif self.y_speed<0:
            self.snail_up_index+=0.1
            if self.snail_up_index >= len(self.snail_up):
                self.snail_up_index=0
            self.image=self.snail_up[int(self.snail_up_index)]
        elif self.y_speed>0:
            self.snail_down_index+=0.1
            if self.snail_down_index >= len(self.snail_down):
                self.snail_down_index=0
            self.image=self.snail_down[int(self.snail_down_index)]
        

    def update(self):
        self.track_player(player.sprite)
        self.animation_state()
        self.take_dmg(flying_player_shells)


class Mage(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        mage_boss_up_1=pygame.image.load("graphics/enemies/mage_boss/mage_boss_up1.png").convert_alpha()
        mage_boss_up_2=pygame.image.load("graphics/enemies/mage_boss/mage_boss_up2.png").convert_alpha()
        self.mage_boss_up=[mage_boss_up_1,mage_boss_up_2]
        self.mage_boss_up_index=0
        
        self.mage_boss_down_default=pygame.image.load("graphics/enemies/mage_boss/mage_boss_down0.png").convert_alpha() 
        
        mage_boss_down_1=pygame.image.load("graphics/enemies/mage_boss/mage_boss_down1.png").convert_alpha()
        mage_boss_down_2=pygame.image.load("graphics/enemies/mage_boss/mage_boss_down2.png").convert_alpha()
        self.mage_boss_down=[mage_boss_down_1,mage_boss_down_2]
        self.mage_boss_down_index=0 
        mage_boss_left_1=pygame.image.load("graphics/enemies/mage_boss/mage_boss_left1.png").convert_alpha()
        mage_boss_left_2=pygame.image.load("graphics/enemies/mage_boss/mage_boss_left2.png").convert_alpha()
        self.mage_boss_left=[mage_boss_left_1,mage_boss_left_2]
        self.mage_boss_left_index=0 
        mage_boss_right_1=pygame.image.load("graphics/enemies/mage_boss/mage_boss_right1.png").convert_alpha()
        mage_boss_right_2=pygame.image.load("graphics/enemies/mage_boss/mage_boss_right2.png").convert_alpha()
        self.mage_boss_right=[mage_boss_right_1,mage_boss_right_2]
        self.mage_boss_right_index=0

        self.image=self.mage_boss_down_default
        self.rect=self.image.get_rect(center=(100,100))

        #parameters of spawned mage_boss
        self.max_speed=1
        self.x_speed=0
        self.y_speed=0
        self.max_hp=20
        self.hp=self.max_hp
        self.attack_power=3 #damage of direct melee hit
        self.time_till_agro_possible=0

        #timers
        self.reload_time_max=150
        self.reload_status=self.reload_time_max
        self.firing_time_max=300
        self.firing_status=0
        self.status="reloading" #has statuses: firing, reloading

        self.walkAway_time_max=120
        self.walkAway_time=0
        self.walkInLine_time_max=120
        self.walkInLine_time=0

        self.between_shots_time_max=30
        self.between_shots_timer=0

        self.magazine_size=10 # advised firig_time+max/between_shots_time_max
        self.magazine_left=self.magazine_size

    def track_player(self, player):
        x_dist_to_player=player.rect.centerx-self.rect.centerx
        y_dist_to_player=player.rect.centery-self.rect.centery
        whole_dist_to_player=calc_dist_mob_point(self,player.rect.centerx,player.rect.centery)
        
        if self.status=="reloading":
            self.reload_status-=1
        if self.status=="firing":
            self.firing_status-=1
        if self.firing_status<=0 and self.status=="firing":
            self.status="reloading"
            self.reload_status=self.reload_time_max
        if self.reload_status<=0 and self.status=="reloading":
            self.magazine_left=self.magazine_size #literal reload 
            self.status="firing"
            self.firing_status=self.firing_time_max
        if self.walkAway_time>0:
            self.walkAway_time-=1
        if self.walkInLine_time>0:
            self.walkInLine_time-=1
        

        if whole_dist_to_player<=200 and self.status=="reloading" and self.walkAway_time<=0:
            self.walkAway_time=self.walkAway_time_max
            self.x_speed = -(x_dist_to_player / calc_dist_mob_point(self,player.rect.centerx,player.rect.centery)) * self.max_speed
            self.y_speed = -(y_dist_to_player / calc_dist_mob_point(self,player.rect.centerx,player.rect.centery)) * self.max_speed
        if  whole_dist_to_player>200 and self.status=="reloading" and self.walkAway_time<=0:
            if abs(x_dist_to_player)>abs(y_dist_to_player):
                if x_dist_to_player>0 and self.walkInLine_time==0:
                    self.x_speed=self.max_speed
                    self.y_speed=0
                elif x_dist_to_player<0 and self.walkInLine_time==0:
                    self.x_speed=-self.max_speed
                    self.y_speed=0
                self.walkInLine_time=self.walkAway_time_max
            else:
                if y_dist_to_player>0  and self.walkInLine_time==0:
                    self.x_speed=0
                    self.y_speed=self.max_speed
                elif y_dist_to_player<0 and self.walkInLine_time==0:
                    self.x_speed=0
                    self.y_speed=-self.max_speed
                self.walkInLine_time=self.walkAway_time_max
        if self.status=="firing":
            self.x_speed=0
            self.y_speed=0


        self.rect.centerx+=self.x_speed
        self.rect.centery+=self.y_speed

    
    def stay_in_room(self):
        if self.rect.left<0:
            self.rect.left=0
        if self.rect.right>1200:
            self.rect.right=1200
        if self.rect.top<0:
            self.rect.top=0
        if self.rect.bottom>800:
            self.rect.bottom=800
    

    def animation_state(self):
        if self.x_speed==0 and self.y_speed==0:
            self.image=self.mage_boss_down_default #state for shooting
        if self.x_speed>0:
            self.mage_boss_right_index+=0.05
            if self.mage_boss_right_index >= len(self.mage_boss_right):
                self.mage_boss_right_index=0
            self.image=self.mage_boss_right[int(self.mage_boss_right_index)]
        elif self.x_speed<0:
            self.mage_boss_left_index+=0.05
            if self.mage_boss_left_index >= len(self.mage_boss_left):
                self.mage_boss_left_index=0
            self.image=self.mage_boss_left[int(self.mage_boss_left_index)]
        elif self.y_speed<0:
            self.mage_boss_up_index+=0.05
            if self.mage_boss_up_index >= len(self.mage_boss_up):
                self.mage_boss_up_index=0
            self.image=self.mage_boss_up[int(self.mage_boss_up_index)]
        elif self.y_speed>0:
            self.mage_boss_down_index+=0.05
            if self.mage_boss_down_index >= len(self.mage_boss_down):
                self.mage_boss_down_index=0
            self.image=self.mage_boss_down[int(self.mage_boss_down_index)]


    def shooting_mech(self):
        if self.status=="firing" and self.magazine_left>=1 and self.between_shots_timer<=0:
            flying_enemy_shells.add(Mage_shell(player.sprite))
            self.magazine_left-=1
            self.between_shots_timer=self.between_shots_time_max

        if self.between_shots_timer>0 and self.status=="firing":
            self.between_shots_timer-=1

    def take_dmg(self,player_shells):
        for element in player_shells:
            if pygame.sprite.collide_rect(self,element):
                self.hp-=1
                element.kill()
        if self.hp<=0:
            self.kill() 

    def update(self):
        self.track_player(player.sprite)
        self.stay_in_room()
        self.animation_state()
        self.take_dmg(flying_player_shells)
        self.shooting_mech()
        

class Mage_shell(pygame.sprite.Sprite):
    def __init__(self,player):
        super().__init__()
        shell_def_0=pygame.image.load("graphics/enemies/mage_boss/mage_boss_shell/fireball_1.png").convert_alpha()
        shell_def_1=pygame.image.load("graphics/enemies/mage_boss/mage_boss_shell/fireball_2.png").convert_alpha()
        shell_def_2=pygame.image.load("graphics/enemies/mage_boss/mage_boss_shell/fireball_3.png").convert_alpha()
        self.shell_def=[shell_def_0,shell_def_1,shell_def_2]
        self.shell_def_index=0
        self.timer=30 #time in air, decreased in function still_in_air()
        self.image=self.shell_def[self.shell_def_index]

        #parameters
        self.max_speed=18
        self.damage=2
        self.x_speed=0
        self.y_speed=0

        if enemies_from_room[0][2]: #if not empty
            mob_boss_list=enemies_from_room[0][2].sprites() # 0,2 are cords, 0 means there is only one element
            mob_boss=mob_boss_list[0] # spirtes() not supscripable xD have to take 1st el of list
            self.rect=self.image.get_rect(center=(mob_boss.rect.centerx,mob_boss.rect.centery))

            x_dist_to_player=player.rect.centerx-mob_boss.rect.centerx
            y_dist_to_player=player.rect.centery-mob_boss.rect.centery

            if calc_dist_mob_point(mob_boss,player.rect.centerx,player.rect.centery)!=0:
                self.x_speed = (x_dist_to_player / calc_dist_mob_point(mob_boss,player.rect.centerx,player.rect.centery)) * self.max_speed
                self.y_speed = (y_dist_to_player / calc_dist_mob_point(mob_boss,player.rect.centerx,player.rect.centery)) * self.max_speed
      
    def animation_state(self):
        if self.shell_def_index <= len(self.shell_def)-0.2:
            self.shell_def_index+=0.2
        self.image=self.shell_def[int(self.shell_def_index)]

    def move(self):
        self.rect.x+=self.x_speed
        self.rect.y+=self.y_speed
    
    def still_in_air(self):
        self.timer-=1
        if self.timer<=0:
            self.kill()
        if self.rect.left < 0 or  self.rect.right > 1200 or self.rect.top < 0 or self.rect.bottom > 800:
            self.kill()
    
    def update(self): #we write function that updates all under-class-functions in one line only.
        self.animation_state()
        self.move()
        self.still_in_air()
            
#GLOBAL FUNCTIONS:

def set_game(player):

    global has_been_spawn_yet_in_room
 
    has_been_spawn_yet_in_room[1][1]=0 #there are enemies in room x:1 y:1 to spawn
    has_been_spawn_yet_in_room[0][0]=1 #there are enemies in room x:0 y:0 to spawn
    has_been_spawn_yet_in_room[0][1]=1 
    has_been_spawn_yet_in_room[0][2]=1

    list_of_en_spawned_in_room[0][0]=[Snail(),Snail()]
    list_of_en_spawned_in_room[0][1]=[Fly(),Fly(),Fly(),Fly()]
    list_of_en_spawned_in_room[0][2]=[Mage()]


    global curr_room_x, curr_room_y, game_status
    curr_room_x=1
    curr_room_y=1
    game_status=1

    #parameters of spawned player
    player.direction="down"
    player.player_x_speed=5
    player.player_y_speed=5
    player.reload_time=20
    player.max_hp=3
    player.hp=player.max_hp
    player.rect.centerx=400
    player.rect.midbottom=(600,400)

    global enemies_from_room
    for x in range(0,max_room_x+1):
        for y in range(0,max_room_y+1):
            for mob in enemies_from_room[x][y]:
                 pygame.sprite.Sprite.remove(mob, enemies_from_room[x][y])
    
def display_intro():
    main_screen.fill((135, 78, 50))

    top_intro_text=RioGrande_font.render(f"Gunpan",False,(0,0,0))
    top_intro_text_rect=top_intro_text.get_rect(center=(600,50))
    main_screen.blit(top_intro_text,top_intro_text_rect)

    player_img_1 = pygame.image.load("graphics/player/player_gun/player_left1_gun.png").convert_alpha()
    player_img_2 = pygame.image.load("graphics/player/player_gun/player_left2_gun.png").convert_alpha()
    player_img_1 = pygame.transform.scale(player_img_1,(140,200))
    player_img_2 = pygame.transform.scale(player_img_2,(140,200))
    player_rect_1 = player_img_1.get_rect(center=(600,350))
    player_rect_2 = player_img_2.get_rect(center=(600,350))

    global intro_timer
    intro_timer+=0.1
    if intro_timer>=2:
        intro_timer=0
    if intro_timer <= 1:
        main_screen.blit(player_img_1,player_rect_1)
    else:
        main_screen.blit(player_img_2,player_rect_2)

    #MECHANICS OF YELLOW-GLOWING BUTTON WHEN POINTED BY MOUSE
    temp_rect1=top_intro_text.get_rect(center=(690,620)) #we create a temporary rectangle to chceck whether mouse is in it, to know if it should be marked yellow
    if pygame.Rect.collidepoint(temp_rect1,pygame.mouse.get_pos()):
        bottom_intro_text1=Somer_font.render(f"Start",False,(244, 249, 109))
        if pygame.mouse.get_pressed()[0]: #MECHANIC OF STARTING A GAME BY PRESSING START
            set_game(player.sprite)     
    else:
        bottom_intro_text1=Somer_font.render(f"Start",False,(40, 242, 26))
    bottom_intro_text1_rect=top_intro_text.get_rect(center=(690,620))
    main_screen.blit(bottom_intro_text1,bottom_intro_text1_rect)

    temp_rect2=top_intro_text.get_rect(center=(695,720)) #we create a temporary rectangle to chceck whether mouse is in it, to know if it should be marked yellow
    if pygame.Rect.collidepoint(temp_rect2,pygame.mouse.get_pos()):
        bottom_intro_text2=Somer_font.render(f"Exit",False,(244, 249, 109))
        if pygame.mouse.get_pressed()[0]: #MECHANIC OF EXITING A GAME BY PRESSING EXIT
            pygame.quit()
            exit()  
    else:
        bottom_intro_text2=Somer_font.render(f"Exit",False,(40, 242, 26))    
    bottom_intro_text2_rect=top_intro_text.get_rect(center=(695,720))
    main_screen.blit(bottom_intro_text2,bottom_intro_text2_rect)

def display_outro():
    main_screen.fill((120, 120, 90))

    top_intro_text=RioGrande_font.render(f"Game Over!",False,(0,0,0))
    top_intro_text_rect=top_intro_text.get_rect(center=(600,50))
    main_screen.blit(top_intro_text,top_intro_text_rect)

    #MECHANICS OF YELLOW-GLOWING BUTTON WHEN POINTED BY MOUSE
    temp_rect1=top_intro_text.get_rect(center=(680,620)) #we create a temporary rectangle to chceck whether mouse is in it, to know if it should be marked yellow
    if pygame.Rect.collidepoint(temp_rect1,pygame.mouse.get_pos()):
        bottom_intro_text1=Somer_font.render(f"Play again",False,(244, 249, 109))
        if pygame.mouse.get_pressed()[0]: #MECHANIC OF STARTING A GAME BY PRESSING START
            set_game(player.sprite)
    else:
        bottom_intro_text1=Somer_font.render(f"Play again",False,(40, 242, 26))
    bottom_intro_text1_rect=top_intro_text.get_rect(center=(700,620))
    main_screen.blit(bottom_intro_text1,bottom_intro_text1_rect)

    temp_rect2=top_intro_text.get_rect(center=(680,720)) #we create a temporary rectangle to chceck whether mouse is in it, to know if it should be marked yellow
    if pygame.Rect.collidepoint(temp_rect2,pygame.mouse.get_pos()):
        bottom_intro_text2=Somer_font.render(f"Exit",False,(244, 249, 109))
        if pygame.mouse.get_pressed()[0]: #MECHANIC OF EXITING A GAME BY PRESSING EXIT
            pygame.quit()
            exit()  
    else:
        bottom_intro_text2=Somer_font.render(f"Exit",False,(40, 242, 26))    
    bottom_intro_text2_rect=top_intro_text.get_rect(center=(750,720))
    main_screen.blit(bottom_intro_text2,bottom_intro_text2_rect)

def calc_dist_mob_point(mob1,x_cord,y_cord):
    return ((mob1.rect.centerx-x_cord)**2+(mob1.rect.centery-y_cord)**2)**0.5  

def spawn_enemies_in_room(x_cord_of_room, y_cord_of_room):
    for sp_mob in list_of_en_spawned_in_room[x_cord_of_room][y_cord_of_room]:
        x_start_cord=randint(0,1200)
        y_start_cord=randint(0,800)
        while not(calc_dist_mob_point(player.sprite,x_start_cord,y_start_cord)>=100 and x_start_cord>=50 and x_start_cord<=1150 and y_start_cord>=50 and y_start_cord<=750):
            x_start_cord=randint(0,1200)
            y_start_cord=randint(0,800)  # mob cannot spawn closer than 100 length to player and close to wall of room
        mob=sp_mob
        mob.rect.centerx=x_start_cord
        mob.rect.centery=y_start_cord
        enemies_from_room[x_cord_of_room][y_cord_of_room].add(mob)

#heart_hp_status

heart_full_surf=pygame.image.load('graphics/heart_icon/heart_full.png').convert_alpha()
heart_half_surf=pygame.image.load('graphics/heart_icon/heart_half.png').convert_alpha()
heart_empty_surf=pygame.image.load('graphics/heart_icon/heart_empty.png').convert_alpha()
def show_player_hp_status(player):
    for iter_1 in range(0,math.floor(player.hp)):
        heart_full_rect=heart_full_surf.get_rect(topleft=(iter_1*50,0))
        main_screen.blit(heart_full_surf,heart_full_rect)
    for iter_2 in range(math.ceil(player.hp),player.max_hp):
        heart_empty_rect=heart_empty_surf.get_rect(topleft=(iter_2*50,0))
        main_screen.blit(heart_empty_surf,heart_empty_rect)
    if player.hp%1==0.5:
        heart_half_rect=heart_half_surf.get_rect(topleft=(math.floor(player.hp)*50,0))
        main_screen.blit(heart_half_surf,heart_half_rect)

#rooms_surface_load

room_doors_exist=[[[0, 0, 0, 0] for _ in range(max_room_x+1)] for _ in range(max_room_y+1)]
has_been_spawn_yet_in_room=[[0 for _ in range(max_room_x+1)] for _ in range(max_room_y+1)]
room_surface= [[0 for _ in range(max_room_x+1)] for _ in range(max_room_y+1)]
mobs_left_in_room = [[1 for _ in range(max_room_x+1)] for _ in range(max_room_y+1)] 

room_surface[1][1]=pygame.image.load('graphics/room11.png').convert_alpha()
room_doors_exist[1][1]=(0,0,1,0) #does this doors exist in this room :up, down, left, right
has_been_spawn_yet_in_room[1][1]=0 #there are enemies in room x:1 y:1 to spawn

room_surface[0][0]=pygame.image.load('graphics/room00.png').convert_alpha()
room_doors_exist[0][0]=(0,1,0,0) #does this doors exist in this room :up, down, left, right
has_been_spawn_yet_in_room[0][0]=1 #there are enemies in room x:0 y:0 to spawn

room_surface[0][1]=pygame.image.load('graphics/room01.png').convert_alpha()
room_doors_exist[0][1]=(1,1,0,1) 
has_been_spawn_yet_in_room[0][1]=1 

room_surface[0][2]=pygame.image.load('graphics/room02.png').convert_alpha()
room_doors_exist[0][2]=(1,0,0,0) 
has_been_spawn_yet_in_room[0][2]=1

#list of enemies to be spawned when entering a certain room

list_of_en_spawned_in_room=[[[] for _ in range(max_room_x+1)] for _ in range(max_room_y+1)]
list_of_en_spawned_in_room[0][0]=[Snail(),Snail()]
list_of_en_spawned_in_room[0][1]=[Fly(),Fly(),Fly(),Fly()]
list_of_en_spawned_in_room[0][2]=[Mage()]

#Groups

player=pygame.sprite.GroupSingle()
player.add(Player())

flying_player_shells=pygame.sprite.Group()
flying_enemy_shells=pygame.sprite.Group()

enemies_from_room=[[pygame.sprite.Group() for _ in range(max_room_x+1)] for _ in range(max_room_y+1)]

while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            exit() #if x in the top-right corner pressed, exit the game
 
    if game_status==0:
        display_outro()
    
    elif game_status==1:
        main_screen.blit(room_surface[curr_room_x][curr_room_y],(0,0))

        player.draw(main_screen)
        player.update()
        show_player_hp_status(player.sprite)
        
        flying_player_shells.draw(main_screen)
        flying_player_shells.update()
        flying_enemy_shells.draw(main_screen)
        flying_enemy_shells.update()

        enemies_from_room[curr_room_x][curr_room_y].draw(main_screen)
        enemies_from_room[curr_room_x][curr_room_y].update()
    
    elif game_status==2:
       display_intro()

    pygame.display.update()
    main_clock.tick(60) #maximum framerate
      