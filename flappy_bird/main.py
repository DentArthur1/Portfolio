import random
import pygame 

class Bird():

    def __init__(self):
        self.bird_imgs = [pygame.image.load("imgs/flappy_bird.png").convert_alpha(),\
                          pygame.image.load("imgs/flappy_flying.png").convert_alpha()]
        self.bird_rect = pygame.rect.Rect(0,0,37,37)
        self.img_index = 0
        self.count = 0
        self.dead = False
        self.change_time = 100
        self.bird_x = 200
        self.bird_y = 200
        self.max_vel = 5
        self.bird_flapping = False
        self.max_angle = 50
        self.inclination = 0
        self.rot_angle_coeff = 2
        self.bird_y_vel = 0

    
        

    def blit_bird(self, rot_angle, bird_img, x, y ,screen):
        #rotates the bird img by the requested amount #changes the rect position  #blits the img correctly rotated
        rot_bird = pygame.transform.rotate(bird_img, rot_angle)
        self.bird_rect.center = x , y - rot_bird.get_height() / 2
        screen.blit(rot_bird, (x - int(rot_bird.get_width() / 2),y - int(rot_bird.get_height())))
        



    def check_collisions(self, rects, bird_rect, y, bg_speed, floor_speed, count):
        #checks for collisions among all the drawn rects
        for rect in rects:
            for part in rect:
                if part.colliderect(bird_rect):     
                   bg_speed, floor_speed,self.dead,self.rot_angle_coeff, self.max_vel = self.die()
                   if abs(bird_rect.bottom -part.top) < 5: #for collisions on the upper side of obstacles
                      y -= (bird_rect.bottom -part.top)
                   if abs(bird_rect.top - part.bottom) < 5: #for collisions on the lower side of obstacles
                      y -= (bird_rect.top - part.bottom)
            #checks for points
            if bird_rect.x == rect[0].x:
                    count += 1
        #checks for collisions with the floor or the roof
        if y <= 55: 
            y = 55
            bg_speed, floor_speed,self.dead,self.rot_angle_coeff, self.max_vel = self.die()
        if y >= 455:
            y = 455
            bg_speed, floor_speed,self.dead,self.rot_angle_coeff, self.max_vel = self.die()

        return bird_rect,y, bg_speed, floor_speed, count

    def die(self):
        bg_speed, floor_speed = 0,0
        die = True
        rot_coeff, max_vel = 0,0
        return bg_speed, floor_speed, die, rot_coeff, max_vel

    def get_img(self, current_time, set_time, n):
        if current_time >= set_time:
            if n == 0:
                n = 1
            elif n == 1:
                n = 0
            set_time += self.change_time
        return  set_time, n

class Scenary():

    def __init__(self):
        self.background_speed = 0.5
        self.floor = pygame.image.load("imgs/floor.png").convert()
        self.pipe = pygame.image.load("imgs/pipe.png").convert_alpha()
        self.pipe_rot = pygame.transform.rotate(self.pipe, 180)
        self.floor.set_colorkey((0,0,0,0))
        self.obstacles = []
        self.bird_gateway = 120
        self.bg_xs = [0,700]
        self.floor_speed = 2
        self.floor_xs = [0,700]
       

    def move_background(self, bg_speed, bg_x):
        bg_x -= bg_speed
        return bg_x

    def blit_background(self, screen, bg, x, y):
        screen.blit(bg,(x,y))
        
    def make_parallax(self, screen, bg, bg_xs, speed, bg_y):
        for bg_x in bg_xs:  #loops trough all the 2 values of the 2 backgrounds and creates a seemless loop
               bg_xs[bg_xs.index(bg_x)] = self.move_background(speed, bg_x)
               self.blit_background(screen, bg, bg_x, bg_y)
               #resets the positions of the given bg if it has reached minus 700
               if -700 in bg_xs:      #Available for speeds under 2
                      bg_xs[bg_xs.index(-700)] = 700

    def pos_obstacle(self, obsts = list):
        #binds the 2 part of the obstacle to the floor and the roof respectively
        obsts[0].x -= self.floor_speed
        obsts[0].y = 0
        obsts[1].y = 445 - obsts[1].height 
        obsts[1].x = obsts[0].x
        return obsts

    def gen_obstacle(self,x, obsts = list):
          
        obst_1 = pygame.rect.Rect(0,0,60, random.randint(50, 300)) #randomly generates the upper half of the obstacle
        obst_1.x = x
        obst_2 = pygame.rect.Rect(0,0,60, ((445 - self.bird_gateway) - obst_1.height)) #creates the lower half correspondly to the gateway and the upper half height
        obsts.append([obst_1,obst_2])
    

        return obsts
       
    def display_obstacles(self, screen):

        for obst in self.obstacles:
            self.obstacles[self.obstacles.index(obst)] = self.pos_obstacle(obst)
            for part in obst:
                  if obst.index(part) == 0:
                        screen.blit(self.pipe_rot, (part.x, part.y), (0,369 - part.height, 60, part.height))
                  else:
                        screen.blit(self.pipe, (part.x, part.y), (0,0, 60, part.height))
    

    def udpate_obstacles(self, obsts):
        #loops through all the obstacles and positions the correctly
        for obst in obsts:
           if obst[0][0] <= -100:
               obsts.remove(obst)
               obsts = self.gen_obstacle(700, obsts)
   
        return obsts




class Game():

    def __init__(self):
        self.width = 400
        self.height = 500
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.icon = pygame.image.load("imgs/bird.png").convert()
        self.bg = pygame.image.load("imgs/bg.png").convert()
        pygame.font.init()
        self.set_time = 100
        self.font = pygame.font.Font("fonts/Flappy-Bird.ttf", 70)
        self.restart_ = self.font.render("Menu", True, (255,255,255))
        self.start_ = self.font.render("Start", True, (255,255,255))
        self.start_rect = self.start_.get_rect()
        self.restart_rect = self.restart_.get_rect()
        self.FPS = 75
        self.start = False
        self.begin = True
        self.gravity_coeff = 0.22
        self.running = True
        self.bird = Bird()
        self.scenary = Scenary()
        self.clock = pygame.time.Clock()
        pygame.display.set_icon(self.icon)
        pygame.display.set_caption("Flappy bird")

    def handle_bird(self):

            current_time = pygame.time.get_ticks()
            #bird rotation in decreasing as it goes up
            self.bird.inclination -= self.bird.rot_angle_coeff  
            #if input has been pressed it reverts the direction of the bird
            if self.bird.bird_flapping:
                  self.bird.bird_y_vel = - self.bird.max_vel
                  self.bird.bird_flapping = False
            #adds the simulate effect of gravity to the bird
            if self.bird.bird_y_vel < self.bird.max_vel: #bird is still going up
                self.bird.bird_y_vel += self.gravity_coeff  
                self.set_time, self.bird.img_index = self.bird.get_img(current_time, self.set_time,self.bird.img_index)
            else:
                self.bird.bird_y_vel = self.bird.max_vel 
             #stops the img from rotating if it has reached the maximum level
            if self.bird.inclination <= -self.bird.max_angle: 
                self.bird.inclination = -self.bird.max_angle
            
            
             
        
         
    def update_screen(self):
            #renders the user count
            count = self.font.render(f"{self.bird.count}", True, (255,255,255))
            #creates the parallax for floor and background
            self.scenary.make_parallax(self.screen, self.bg,self.scenary.bg_xs,self.scenary.background_speed,-50)
            self.scenary.make_parallax(self.screen, self.scenary.floor,self.scenary.floor_xs,self.scenary.floor_speed,0)     
            self.bird.bird_y += self.bird.bird_y_vel
            #removes obstacles below x = -100 and replaces them at x = 700
            self.scenary.obstacles = self.scenary.udpate_obstacles(self.scenary.obstacles)
            self.scenary.display_obstacles(self.screen)
            #Checks for any collision concerning the bird
            self.bird.bird_rect, self.bird.bird_y,self.scenary.background_speed,\
            self.scenary.floor_speed,self.bird.count = self.bird.check_collisions(self.scenary.obstacles, self.bird.bird_rect, self.bird.bird_y,\
                                                                                  self.scenary.background_speed, self.scenary.floor_speed,self.bird.count)

            self.bird.blit_bird(self.bird.inclination,  self.bird.bird_imgs[self.bird.img_index], self.bird.bird_x, self.bird.bird_y,self.screen)
            self.clock.tick(self.FPS)
            #blits the user count
            self.screen.blit(count, (200,100))

    def restart(self):
        self.scenary.obstacles, self.start,self.bird.count,self.scenary.background_speed, \
        self.scenary.floor_speed, self.bird.dead,self.begin,self.bird.bird_x, self.bird.bird_y,\
        self.bird.rot_angle_coeff,self.bird.max_vel, self.bird.max_angle = [], False, 0, 0.5, 2, False, True, 200, 200, 2, 4, 20

    def start_game(self):
        
        if self.begin:
            self.screen.blit(self.start_, (130, 350))
            self.start_rect.center = 130 + self.start_.get_width() / 2, 350 + self.start_.get_height() / 2
            self.bird.max_vel, self.bird.max_angle = 0,0
        
    def main_loop(self):

        while self.running:
            self.screen.blit(self.bg,(0,0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONUP:  #checks for mouse input 
                        if self.bird.dead:
                            if self.restart_rect.collidepoint(pygame.mouse.get_pos()):
                                self.restart()
                        else:
                            self.bird.bird_flapping = True
                            self.bird.inclination = self.bird.max_angle
                        if self.start_rect.collidepoint(pygame.mouse.get_pos()):
                            if self.begin:
                                #if variable is true it removes the start button and starts generating the pipes
                                self.start = True
                                self.bird.max_vel, self.bird.max_angle = 5, 50
                                self.begin = False

            self.handle_bird()
            #draws user count and handles all the objects and backgrounds on screen
            self.update_screen()
            #on the first run or after a reset 
            if self.start:
                for n in range(4):
                     self.scenary.obstacles = self.scenary.gen_obstacle(800 + (200 * n),self.scenary.obstacles)
                self.start = False
            #handles the start input by the mouse
            self.start_game()
            #checks if bird is dead
            if self.bird.dead:
                self.screen.blit(self.restart_, (150,200))
                self.restart_rect.center = 130 + self.restart_.get_width() / 2,200 + self.restart_.get_height() / 2

            pygame.display.flip()


game = Game()
game.main_loop()

