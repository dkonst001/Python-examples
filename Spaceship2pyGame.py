# Spaceship Game

try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import math
import random

# global/constants
WIDTH = 800
HEIGHT = 600
score = 0
lives = 5
time = 0
started = False
FRICTION = 0.03
SHIP_SIZE = [90,90]
SHIP_RADIUS = 35
ROCK_SIZE = [90, 90]
ROCK_RADIUS = 40
MISSILE_SIZE = [10,10]
MISSILE_RADIUS = 3
MISSILE_LIFESPAN = 50
ROCK_RADIUS = 40
ROCK_VEL_FACTOR = 1
ROCK_AVEL_FACTOR = .4
MISSILE_VEL_FACTOR = 6

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated     
        
    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop
    
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# Images
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

SHIP_CENTER = [SHIP_SIZE[0] / 2, SHIP_SIZE[1] / 2]
ship_info = ImageInfo(SHIP_CENTER, SHIP_SIZE, SHIP_RADIUS)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

MISSILE_CENTER = [MISSILE_SIZE[0] / 2, MISSILE_SIZE[1] / 2]
missile_info = ImageInfo(MISSILE_CENTER, MISSILE_SIZE, MISSILE_RADIUS, MISSILE_LIFESPAN)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

ROCK_CENTER = [ROCK_SIZE[0] / 2, ROCK_SIZE[1] / 2]
asteroid_info = ImageInfo(ROCK_CENTER, ROCK_SIZE, ROCK_RADIUS)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# Sounds
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.ogg")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.ogg")
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.ogg")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.ogg")

missile_sound.set_volume(.5)

# Classes
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0], pos[1]]
        self.vel = [vel[0], vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        
    def draw(self,canvas):
        if self.thrust:
            canvas.draw_image(self.image, [self.image_center[0] + self.image_size[0], self.image_center[1]] , self.image_size,
                              self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size,
                              self.pos, self.image_size, self.angle)
        
    def update(self):
        # update angle
        self.angle += self.angle_vel
        # update position
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        # update velocity
        if self.thrust:
            acc = angle_to_vector(self.angle)
            self.vel[0] += acc[0] * .1
            self.vel[1] += acc[1] * .1
            
        self.vel[0] *= .99
        self.vel[1] *= .99

    def set_thrust(self, on):
        self.thrust = on
        if on:
            ship_thrust_sound.rewind()
            ship_thrust_sound.play()
        else:
            ship_thrust_sound.pause()
       
    def increment_angle_vel(self):
        self.angle_vel += .05
        
    def decrement_angle_vel(self):
        self.angle_vel -= .05
        
    def shoot(self):
        global missiles_group
        forward = angle_to_vector(self.angle)
        missile_pos = [self.pos[0] + self.radius * forward[0], self.pos[1] + self.radius * forward[1]]
        missile_vel = [self.vel[0] + MISSILE_VEL_FACTOR * forward[0], self.vel[1] + MISSILE_VEL_FACTOR * forward[1]]
        missiles_group.add(Sprite(missile_pos, missile_vel, self.angle, 0, missile_image, missile_info, missile_sound))
        
    def get_pos(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
       
    
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = list(info.get_center())
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):         
        canvas.draw_image(self.image, self.image_center, self.image_size,
                          self.pos, self.image_size, self.angle)

    def update(self):
        self.age += 1     
        # update explosion
        if self.animated and self.age < self.lifespan:
            self.image_center[0] += self.image_size[0]           
        # update angle
        self.angle += self.angle_vel
        # update position
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        return self.age > self.lifespan
    
    def get_lifespan(self):
        return self.lifespan
            
    def get_pos(self):
        return self.pos
    
    def get_vel(self):
        return self.vel
    
    def get_angle(self):
        return self.angle
    
    def get_angle_vel(self):
        return self.angle_vel
    
    def get_radius(self):
        return self.radius
    
    def collide(self, other):
        return dist(self.get_pos(), other.get_pos()) < self.get_radius() + other.get_radius()
    
    def get_animated(self):
        return self.animated
       
# Helper functions
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def process_sprite_group(sprite_group,canvas):
    for a_sprite in set(sprite_group):
        a_sprite.draw(canvas)
        if a_sprite.update():
            sprite_group.discard(a_sprite)

def dist(p, q):
    return math.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)

def group_collide(sprite_group, other):
    global explosions_group
    collision = False
    for a_sprite in set(sprite_group):
        if a_sprite.collide(other):
            explosions_group.add(Sprite(a_sprite.get_pos(), a_sprite.get_vel(), a_sprite.get_angle(), a_sprite.get_angle_vel(), explosion_image, explosion_info, explosion_sound))
            sprite_group.discard(a_sprite)
            collision = True
    return collision
    
def group_group_collide(sprite_group1, sprite_group2):
    collisions = 0
    for a_sprite1 in set(sprite_group1):
        if group_collide(sprite_group2, a_sprite1):
            collisions += 1
            sprite_group1.discard(a_sprite1)
    return collisions 
            
    
# Key/Mouse/Timer Handlers
def keydown(key):
    if key == simplegui.KEY_MAP['left']:
        my_ship.decrement_angle_vel()
    elif key == simplegui.KEY_MAP['right']:
        my_ship.increment_angle_vel()
    elif key == simplegui.KEY_MAP['up']:
        my_ship.set_thrust(True)
    elif key == simplegui.KEY_MAP['space']:
        my_ship.shoot()
        
def keyup(key):
    if key == simplegui.KEY_MAP['left']:
        my_ship.increment_angle_vel()
    elif key == simplegui.KEY_MAP['right']:
        my_ship.decrement_angle_vel()
    elif key == simplegui.KEY_MAP['up']:
        my_ship.set_thrust(False)
        
def click(pos):
    global started, lives, score
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        started = True
        lives = 3
        score = 0
        soundtrack.rewind()
        soundtrack.play()         

def draw(canvas):
    global time, started, lives, score, my_ship, rock_group, missiles_group, explosions_group
    
    time += 1
    wtime = (time / 4) % WIDTH
    
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    # draw UI
    canvas.draw_text("Lives", [50, 50], 22, "White")
    canvas.draw_text("Score", [680, 50], 22, "White")
    canvas.draw_text(str(lives), [50, 80], 22, "White")
    canvas.draw_text(str(score), [680, 80], 22, "White")

    # draw ship and sprites
    my_ship.draw(canvas)
    my_ship.update()
    # check collisions only 8 times per second to improve performance
    if time % 12 == 0:
        if group_collide(rock_group, my_ship):
            if lives > 0:
                lives -= 1
                if lives == 0:
                    started = False
                    soundtrack.pause()
                    # initialize ship and two sprites
                    my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
                    rock_group = set([])
                    explosions_group = set([])
                    missiles_group = set([])

        score += group_group_collide(missiles_group, rock_group)
    process_sprite_group(rock_group,canvas)
    process_sprite_group(missiles_group,canvas)
    process_sprite_group(explosions_group,canvas)

    # draw splash screen if not started
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          splash_info.get_size())

# timer handler    
def rock_spawner():
    global rock_group
    if started:
        if len(rock_group) < 12:
            rock_pos = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]
            rock_vel = [random.random() * ROCK_VEL_FACTOR - ROCK_VEL_FACTOR / 2, random.random() * ROCK_VEL_FACTOR - ROCK_VEL_FACTOR / 2]
            rock_avel = random.random() * ROCK_AVEL_FACTOR - ROCK_AVEL_FACTOR / 2
            a_rock = Sprite(rock_pos, rock_vel, 0, rock_avel, asteroid_image, asteroid_info)
            # add rock to group only if its not colliding with the ship
            if not a_rock.collide(my_ship):
                rock_group.add(a_rock)           
    
# Main part          
# Declare frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)
# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
rock_group = set([])
explosions_group = set([])
missiles_group = set([])

# register handlers
frame.set_keyup_handler(keyup)
frame.set_keydown_handler(keydown)
frame.set_mouseclick_handler(click)
frame.set_draw_handler(draw)

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()
