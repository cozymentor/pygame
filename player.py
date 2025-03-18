import pygame

import settings
from settings import *

class player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT
        self.x = PLAYER_X
        self.y = PLAYER_Y
        self.speed = PLAYER_SPEED
        self.dir = "/home/tasberry/Documents/PyCharm/Pygame/Player Sprites/"
        self.facing_left = False

        #self.image.fill(BLUE)

        self.current_frame = 0

        self.animation_running = [pygame.image.load(f"{self.dir}Running/run_{i}.png") for i in range(1,7)]
        self.animation_jumping = [pygame.image.load(f"{self.dir}Jumping/jump_{i}.png") for i in range(1,3)]
        self.animation_idle = pygame.image.load(f"{self.dir}Idle/idle_1.png")
        self.animation_prone = pygame.image.load(f"{self.dir}Prone/prone_1.png")
        self.animation_aimUp = pygame.image.load(f"{self.dir}Shooting_Up/su_1.png")
        self.animation_runningShooting = [pygame.image.load(f"{self.dir}Running_Shooting/rs_{i}.png") for i in range(1,3)]
        self.animation_runShootingDown = [pygame.image.load(f"{self.dir}Running_Shooting_Down/rsd_{i}.png") for i in range(1,3)]
        self.animation_runShootingUp = [pygame.image.load(f"{self.dir}Running_Shooting_Up/rsu_{i}.png") for i in range(1,3)]
        self.prone = False

        self.bullets = pygame.sprite.Group()

        self.animation = {"running": self.animation_running,
                        "jumping": self.animation_jumping,
                         "idle": self.animation_idle,
                            "prone": self.animation_prone,
                          "aiming_up": self.animation_aimUp,}

        self.state = {"idle": True,
                       "jumping": False,
                       "running": False,
                      "prone":False,
                      "aiming_up":False,
                      "aiming_down":False,
                      "shooting":False}

        self.image = self.animation_running[self.current_frame]
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.last_update = pygame.time.get_ticks()
        self.last_shot = pygame.time.get_ticks()
        self.frame_delay = 100
        self.shot_delay = 200

        self.position = pygame.math.Vector2(self.x,self.y)
        self.velocity = pygame.math.Vector2(0,0)
        self.acceleration = pygame.math.Vector2(0,0)

        self.on_ground = False

    def jump(self):
        if self.on_ground:
            self.velocity.y = JUMP_STRENGTH
            self.on_ground = False
            self.state["jumping"] = True

    def apply_gravity(self):
        #now = pygame.time.get_ticks()
        if not self.on_ground:
            self.velocity.y += GRAVITY
            #print("gravity")

    def move(self, keys):
        self.acceleration = pygame.math.Vector2(0,0)
        now = pygame.time.get_ticks()

        if keys[pygame.K_s]:
            if not self.prone:
                self.prone = True
            if not self.state["running"] and not self.state["jumping"]:
                self.state["prone"] = True
                self.state["idle"] = False
            else:
                self.state["aiming_down"] = True
        else:
            self.prone = False
            self.state["prone"] = False
            self.state["aiming_down"] = False

        if keys[pygame.K_w]:
            if not self.state["aiming_up"]:
                self.state["aiming_up"] = True
                self.state["idle"] = False
            if not self.state["jumping"]:
                self.state["aiming_up"] = True
        else:
            self.state["aiming_up"] = False
            self.state["idle"] = True

        if keys[pygame.K_a] and self.rect.x > 0:
            self.acceleration.x = -self.speed
            if not self.state["jumping"]:
                self.state["running"] = True
            self.state["idle"] = False
            self.state["prone"] = False
            self.facing_left = True

        elif keys[pygame.K_d] and self.rect.x < SCREEN_WIDTH - self.width:
            self.acceleration.x = self.speed
            if not self.state["jumping"]:
                self.state["running"] = True
            self.state["idle"] = False
            self.state["prone"] = False
            self.facing_left = False
        else:
            if not self.state["prone"] or not self.state["aiming_up"]:
                self.state["idle"] = True
                self.state["running"] = False

        if keys[pygame.K_SPACE]:
            self.jump()

        if keys[pygame.K_p]:
            self.state["shooting"] = True
        else:
            self.state["shooting"] = False

        self.acceleration.x += self.velocity.x * -GROUND_FRICTION

        self.velocity += self.acceleration
        self.position += self.velocity +0.5 * self.acceleration

        self.rect.topleft = (int(self.position.x), int(self.position.y))

    def update(self, keys, platforms):
        self.apply_gravity()
        self.move(keys)
        self.state_machine(keys)
        self.check_collisions(platforms)
        for bullet in self.bullets:
            bullet.fire()

    def check_collisions(self, platforms):
        self.on_ground = False  # Assume sprite is in air until proven otherwise

        for platform in platforms:
            if self.rect.colliderect(platform.rect) and self.velocity.y > 0:

                # Check if the sprite is actually falling
                if self.rect.bottom + self.velocity.y >= platform.rect.top:

                    # Ensure the correction is only applied once
                    if not self.on_ground:
                        if self.state["prone"]:
                            self.rect.bottom = int(platform.rect.top + 20)
                        elif self.state["aiming_up"] and not self.state["running"]:
                            self.rect.bottom = int(platform.rect.top - 10)
                        else:
                            self.rect.bottom = int(platform.rect.top)

                        self.velocity.y = 0  # Stop falling
                        self.on_ground = True
                        self.position.y = int(self.rect.y)
                        self.state["jumping"] = False


    def state_machine(self, keys):
        now = pygame.time.get_ticks()
        if self.state["running"] and self.state["aiming_down"] and(
                not self.state["jumping"] or not self.state["aiming_up"]):

            if self.facing_left:
                if now - self.last_update > self.frame_delay and not self.state["jumping"]:
                    self.current_frame = (self.current_frame + 1) % len(self.animation_runShootingDown)
                    self.image = pygame.transform.flip(self.animation_runShootingDown[self.current_frame], True, False)
                    self.last_update = now
            else:
                if now - self.last_update > self.frame_delay and not self.state["jumping"]:
                    self.current_frame = (self.current_frame + 1) % len(self.animation_runShootingDown)
                    self.image = self.animation_runShootingDown[self.current_frame]
                    self.last_update = now

        elif self.state["running"] and self.state["aiming_up"]  and (
                not self.state["jumping"] or not self.state["prone"]):

            if self.facing_left:
                if now - self.last_update > self.frame_delay and not self.state["jumping"]:
                    self.current_frame = (self.current_frame + 1) % len(self.animation_runShootingUp)
                    self.image = pygame.transform.flip(self.animation_runShootingUp[self.current_frame], True, False)
                    self.last_update = now
            else:
                if now - self.last_update > self.frame_delay and not self.state["jumping"]:
                    self.current_frame = (self.current_frame + 1) % len(self.animation_runShootingUp)
                    self.image = self.animation_runShootingUp[self.current_frame]
                    self.last_update = now

        elif self.state["running"] and self.state["shooting"]  and (
                not self.state["jumping"] or not self.state["prone"] or not self.state["aiming_up"]):

            if self.facing_left:
                if now - self.last_update > self.frame_delay and not self.state["jumping"]:
                    self.current_frame = (self.current_frame + 1) % len(self.animation_runningShooting)
                    self.image = pygame.transform.flip(self.animation_runningShooting[self.current_frame], True, False)
                    self.last_update = now
            else:
                if now - self.last_update > self.frame_delay and not self.state["jumping"]:
                    self.current_frame = (self.current_frame + 1) % len(self.animation_runningShooting)
                    self.image = self.animation_runningShooting[self.current_frame]
                    self.last_update = now

        elif self.state["running"] and (not self.state["jumping"] or not self.state["prone"] or not self.state["aiming_up"]):

            if self.facing_left:
                if now - self.last_update > self.frame_delay and not self.state["jumping"]:
                    self.current_frame = (self.current_frame + 1) % len(self.animation_running)
                    self.image = pygame.transform.flip(self.animation_running[self.current_frame], True, False)
                    self.last_update = now
            else:
                if now - self.last_update > self.frame_delay and not self.state["jumping"]:
                    self.current_frame = (self.current_frame + 1) % len(self.animation_running)
                    self.image = self.animation_running[self.current_frame]
                    self.last_update = now

        elif self.state["jumping"]:
            if self.facing_left:
                if now - self.last_update > self.frame_delay:
                    self.current_frame = (self.current_frame + 1) % len(self.animation_jumping)
                    self.image = pygame.transform.flip(self.animation_jumping[self.current_frame], True, False)
                    self.last_update = now
            else:
                if now - self.last_update > self.frame_delay:
                    self.current_frame = (self.current_frame + 1) % len(self.animation_jumping)
                    self.image = self.animation_jumping[self.current_frame]
                    self.last_update = now

        elif self.state["aiming_up"]:
            if self.facing_left:
                self.image = pygame.transform.flip(self.animation_aimUp, True, False)

            else:
                self.image = self.animation_aimUp

        elif self.state["prone"]:
            if self.facing_left:
                self.image = pygame.transform.flip(self.animation_prone, True, False)
            else:
                self.image = self.animation_prone
        else:
            self.current_frame = 1
            if self.facing_left:
                pass
                self.image = pygame.transform.flip(self.animation_idle, True, False)
            else:
                self.image = self.animation_idle
                self.last_update = now

        if self.state["shooting"]:
            if now - self.last_shot > self.shot_delay:

                if self.state["prone"]:
                    if self.facing_left:
                        self.bullets.add(bullet(self.position.x -0, self.position.y + 3, -BULLET_SPEED, 0))
                        self.last_shot = now
                    else:
                        self.bullets.add(bullet(self.position.x + 30, self.position.y + 3, BULLET_SPEED, 0))
                        self.last_shot = now

                elif self.state["aiming_up"] and not self.state["running"]:
                    if self.facing_left:
                        self.bullets.add(bullet(self.position.x ,self.position.y -10, 0,-BULLET_SPEED))
                        self.last_shot = now
                    else:
                        self.bullets.add(bullet(self.position.x +5 ,self.position.y -10, 0,-BULLET_SPEED))
                        self.last_shot = now

                elif self.state["aiming_up"] and self.state["running"]:
                    if self.facing_left:
                        self.bullets.add(bullet(self.position.x - 20, self.position.y - 7, -BULLET_SPEED, -BULLET_SPEED))
                        self.last_shot = now
                    else:
                        self.bullets.add(bullet(self.position.x + 23, self.position.y - 7, BULLET_SPEED, -BULLET_SPEED))
                        self.last_shot = now

                elif self.state["aiming_down"] and self.state["running"]:
                    if self.facing_left:
                        self.bullets.add(bullet(self.position.x -0, self.position.y + 7, -BULLET_SPEED* 1.5, BULLET_SPEED))
                        self.last_shot = now
                    else:
                        self.bullets.add(bullet(self.position.x + 15, self.position.y + 7, BULLET_SPEED* 1.5, BULLET_SPEED))
                        self.last_shot = now

                elif self.facing_left:
                    self.bullets.add(bullet(self.position.x - 20,self.position.y +7, -BULLET_SPEED,0))
                    self.last_shot = now
                else:
                    self.bullets.add(bullet(self.position.x + 20,self.position.y +7, BULLET_SPEED,0))
                    self.last_shot = now



class bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, velocity_x, velocity_y):
        super().__init__()
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT
        self.x = x
        self.y = y
        self.speed_x = velocity_x
        self.speed_y = velocity_y
        self.dir = "/home/tasberry/Documents/PyCharm/Pygame/Player Sprites/"

        self.image = pygame.image.load(f"{self.dir}Bullets/bullet_1.png")
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.last_update = pygame.time.get_ticks()
        self.frame_delay = 100

        self.position = pygame.math.Vector2(self.x, self.y)
        self.velocity = pygame.math.Vector2(0, 0)
        self.acceleration = pygame.math.Vector2(0, 0)

    def fire(self):
        #self.acceleration.x = self.speed_x
        #self.acceleration.y = self.speed_y

        #self.acceleration.x += self.velocity.x * -GROUND_FRICTION
        #self.acceleration.y += self.velocity.y * -GROUND_FRICTION

        self.velocity.x = self.speed_x
        self.velocity.y = self.speed_y
        self.position += self.velocity

        self.rect.topleft = (int(self.position.x), int(self.position.y))

        if self.position.x > settings.SCREEN_WIDTH or self.position.x < 0 or self.position.y > settings.SCREEN_HEIGHT or self.position.y < 0:
            self.kill()

