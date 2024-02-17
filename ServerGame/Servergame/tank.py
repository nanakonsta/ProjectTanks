import pygame
import sys
import math
from enum import Enum
from tankEnum import *
class Tank(pygame.sprite.Sprite):
    def __init__(self, xPos, yPos):
        self.x_pos = xPos
        self.y_pos = yPos
        self.tank_components = []

    def add_child(self, tank_component):
        self.tank_components.append(tank_component)
    def removeChild(self, reference):
        if reference in self.tank_components:
            self.tank_components.remove(reference)
    def updateState(self):
        for tank_component in self.tank_components:
            tank_component.updateState()


        
    def drawTank(self, screen):
        for tank_component in self.tank_components:
            tank_component.drawTank(screen)

class TankBase(Tank):#to h vash tou tank pws kounietai kai pws purovolaei
    def __init__(self, xPos, yPos, spritePath, moveSpeed, rotateSpeed, tankType, stopDistance, health, gameManager):
        super().__init__(xPos, yPos)
        image_pre_rotated = pygame.image.load(spritePath)
        self.sprite_surface = pygame.transform.rotate(image_pre_rotated, 90)
        self.rect = pygame.Rect(xPos, yPos, self.sprite_surface.get_width(), self.sprite_surface.get_height())
        self.speed = moveSpeed
        self.rotate_speed = rotateSpeed
        self.angle = 0
        self.drawed_sprite = self.sprite_surface
        self.rect_turret_pos = pygame.Rect(self.rect.x , self.rect.y , 40, 40)
        self.transparent_surface = pygame.Surface((50, 50))
        self.transparent_surface.fill((100, 0, 0, 0))
        self.transparent_surface_drawed = self.transparent_surface
        self.tank_turret = None
        self.tankType = tankType    
        self.angle_enemy = 0
        self.stop = False
        self.stopDistance = stopDistance
        self.health = health
        self.dead = False
        self.game_manager = gameManager
        
            
    def updateState(self, moveForward, moveBackwards, rotatingClockwise, rotatingAntiClockwise):
        super().updateState()
        
        move_vector = pygame.math.Vector2(0, 0)
     
        if moveForward:
            if self.tankType == TankEnum.E1 or self.tankType == TankEnum.E2 and self.stop == False:
                self.angle_enemy = math.degrees(math.atan2(300 - self.rect.centery, 400 - self.rect.centerx))
                self.angle_enemy %= 360
                move_vector = pygame.math.Vector2(self.speed, 0).rotate(self.angle_enemy)
            else:
                move_vector = pygame.math.Vector2(self.speed, 0).rotate(-self.angle)
        elif moveBackwards:
            move_vector = pygame.math.Vector2(-self.speed, 0).rotate(-self.angle)

        if self.tankType == TankEnum.E1 or self.tankType == TankEnum.E2:
            pass
        if self.tankType == TankEnum.E1 or self.tankType == TankEnum.E2:
            if self.stop == False:
                self.rect.x += move_vector.x
                self.rect.y += move_vector.y
                self.rect_turret_pos.x += move_vector.x
                self.rect_turret_pos.y += move_vector.y
        else:
            self.rect.x += move_vector.x
            self.rect.y += move_vector.y
            self.rect_turret_pos.x += move_vector.x
            self.rect_turret_pos.y += move_vector.y
            
            
        distanceFromTarget = self.distanceToTheCenter()
        if distanceFromTarget < self.stopDistance:
            self.stop = True
            move_vector = pygame.math.Vector2(0,0)
            
        if rotatingClockwise:
            self.angle += self.rotate_speed
        elif rotatingAntiClockwise:
            self.angle -= self.rotate_speed

        for tank_component in self.tank_components:
            tank_component.parent_x_pos = self.rect_turret_pos.x
            tank_component.parent_y_pos = self.rect_turret_pos.y

        self.angle %= 360

        if self.tankType == TankEnum.E1 or self.tankType == TankEnum.E2:
            self.angle_enemy = math.degrees(math.atan2(300 - self.rect.centery, 400 - self.rect.centerx))
            self.angle_enemy %= 360
            self.drawed_sprite = pygame.transform.rotate(self.sprite_surface, -self.angle_enemy)
            self.rect = self.drawed_sprite.get_rect(center=self.rect.center)

        else:
            self.drawed_sprite = pygame.transform.rotate(self.sprite_surface, self.angle)
            self.rect = self.drawed_sprite.get_rect(center=self.rect.center)


    def drawTank(self, screen):
        screen.blit(self.drawed_sprite, self.rect.topleft)
        super().drawTank(screen)

    def distanceToTheCenter(self):
        screen_center_x, screen_center_y = 800 // 2, 600 // 2
        return math.sqrt((screen_center_x - self.rect.centerx)**2 + (screen_center_y - self.rect.centery)**2)
    

        
class TankTurret(Tank): #to kanoni pws kounietai kai pws purovolontai
    def __init__(self, tank_base, spritePath, fireRate = 200):
        super().__init__(tank_base.x_pos, tank_base.y_pos)
        image_pre_rotated_turret = pygame.image.load(spritePath)
        self.sprite_surface_turret = pygame.transform.rotate(image_pre_rotated_turret, 90)
        self.rect_turret = pygame.Rect(tank_base.x_pos +8.5, tank_base.y_pos +5, self.sprite_surface_turret.get_width(), self.sprite_surface_turret.get_height())
        self.drawed_sprite_turret = self.sprite_surface_turret
        self.parent_x_pos, self.parent_y_pos = tank_base.x_pos, tank_base.y_pos
        self.angle = 0
        self.tank_base = tank_base
        self.bulletInstatiatedTimer = False
        self.last_creation_time = 0
        self.creation_interval = fireRate
        self.x_lookAt, self.y_lookAt = 0, 0
        
        
    def bulletInstatiated(self):
        self.canFireBullet = False
        current_time = pygame.time.get_ticks()
        if current_time - self.last_creation_time >= self.creation_interval:
            self.last_creation_time = current_time
            self.bulletInstatiatedTimer = False #stamataei
    
    
    def fireCannon(self):
        if self.bulletInstatiatedTimer == False:
            self.last_creation_time = pygame.time.get_ticks()
            self.bulletInstatiatedTimer = True
            angle_to_fire = 0
            if self.tank_base.tankType == TankEnum.E1 or self.tank_base.tankType == TankEnum.E2:
                angle_to_fire = math.degrees(math.atan2(300 - self.rect_turret.centery, 400 - self.rect_turret.centerx))
            else:
                angle_to_fire = self.angle
            bullet = Bullet(self.rect_turret.centerx, self.rect_turret.centery,angle_to_fire,"Sprites/tank_Shell.png", 8, self)
            self.tank_base.add_child(bullet)
                       
    def updateState(self):
        if (self.tank_base.tankType == TankEnum.E1 or self.tank_base.tankType == TankEnum.E2) and self.tank_base.stop == True:
            self.fireCannon()
        if self.bulletInstatiatedTimer == True:
            self.bulletInstatiated()
            
        self.rect_turret = pygame.Rect(self.parent_x_pos , self.parent_y_pos , self.sprite_surface_turret.get_width(), self.sprite_surface_turret.get_height())

        #mouse_x, mouse_y = pygame.mouse.get_pos()
        if self.tank_base.tankType == TankEnum.E1 or self.tank_base.tankType == TankEnum.E2:
            angleInitial = math.degrees(math.atan2(300 - self.rect_turret.centery, 400 - self.rect_turret.centerx))
            self.drawed_sprite_turret = pygame.transform.rotate(self.sprite_surface_turret, -angleInitial)
            self.rect_turret = self.drawed_sprite_turret.get_rect(center=self.rect_turret.center)
        else:
            self.angle = math.degrees(math.atan2(self.y_lookAt - self.rect_turret.centery, self.x_lookAt - self.rect_turret.centerx))
            self.drawed_sprite_turret = pygame.transform.rotate(self.sprite_surface_turret, -self.angle)
            self.rect_turret =  self.drawed_sprite_turret.get_rect(center=self.rect_turret.center)

        
    def drawTank(self, screen):
        screen.blit(self.drawed_sprite_turret, self.rect_turret.topleft)

    
    
class Bullet(Tank):  #h sfaira
    def __init__(self, x, y, angle, spritePath, speed, turret):
        super().__init__(x, y)
        self.speed = speed
        self.angle = angle
        image_pre_rotated_bullet = pygame.image.load(spritePath)
        self.sprite_surface_bullet = pygame.transform.rotate(image_pre_rotated_bullet, -90)
        self.rect = self.sprite_surface_bullet.get_rect(center=(x, y))
        self.turret = turret
        
         
    def updateState(self):
        self.rect.x += self.speed * math.cos(math.radians(self.angle))
        self.rect.y += self.speed * math.sin(math.radians(self.angle))
        self.collisionDetection()
    def drawTank(self, screen):
        screen.blit(pygame.transform.rotate(self.sprite_surface_bullet, -self.angle), self.rect.topleft)


    def collisionDetection(self): #sfaires
        if self.turret.tank_base.tankType == TankEnum.E1 or self.turret.tank_base.tankType == TankEnum.E2:
            if self.rect.colliderect(self.turret.tank_base.game_manager.castle_rect):
                if self.turret.tank_base.dead == False:
                    self.turret.tank_base.removeChild(self)
            for tank in self.turret.tank_base.game_manager.players:
                if self.rect.colliderect(tank.rect):
                    tank.health -= 10
                    if tank.health <=0:
  
                        tank.dead = True
                        self.turret.tank_base.game_manager.removePlayer(tank)
                        
          
                    if self.turret.tank_base.dead == False:
                        self.turret.tank_base.removeChild(self)
            if self.rect.x > 800 or self.rect.x < 0 or self.rect.y > 600 or self.rect.y < 0:
                self.turret.tank_base.removeChild(self)
                
        else:
            for tank in self.turret.tank_base.game_manager.enemies:
                 if self.rect.colliderect(tank.rect):
                    tank.health -= 10     
                    if tank.health <=0:
                        tank.dead = True
                        self.turret.tank_base.game_manager.removeEnemy(tank)
                    
                    if self.turret.tank_base.dead == False:
                        self.turret.tank_base.removeChild(self)
                        #self = None
            
                         
            if self.rect.x > 800 or self.rect.x < 0 or self.rect.y > 600 or self.rect.y < 0:
                self.turret.tank_base.removeChild(self)
