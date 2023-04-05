import math
import pygame
import sys
from random import randint

# Initialize pygame
pygame.init()

##########################################       GAME CONFIG          ##################################################

# Set up the screen size
screen_width = 1600
screen_height = 900

# Set up the display mode
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Ecosystem")

# # Defining value for the FPS, oftherwise the game will run with speed depending on the computer speed (with is a lot)
FPS = 60

# Set up game Scale in pixels for 1 tile
scale = 5

# set up the text font
test_font = pygame.font.Font(None, 150)

# set the clock function
clock = pygame.time.Clock()

timer = 0

# time between plant reproduce
plant_spawn_time = 1200

# starting plants
starting_plants = 30

# starting herbivores
starting_herbivores = 30

# starting herbivores
starting_carnivores = 2

carnivore_limit = 40
tree_limit = 200
herbivore_limit = 120

# default walking speed
walk = 1


# # create the border of the game
empty_rect = pygame.Rect(0, 0, screen_width, screen_height)


##########################################    DEFINE THE GAME COLORS  ##################################################

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
light_green = (0, 141, 85)
dark_green = (51, 85, 0)
BLUE = (15, 82, 186)
RED = (255, 0, 0)

##########################################   DEFINE THE GAME Classes  ##################################################

class create_plant(pygame.sprite.Sprite):
    def __init__(self, x, y, scale, plant_spawn_time):
        super().__init__()
        self.radius = scale
        self.image = pygame.Surface((self.radius, self.radius), pygame.SRCALPHA) # Set the surface to have an alpha channel
        pygame.draw.circle(self.image, light_green, (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.time = randint(plant_spawn_time // 100, plant_spawn_time // 2)
        self.state = 1

    def collision_test(self, plants):
        for plant in plants:
            if self.rect.colliderect(plant.rect):
                return True
        for tree in plants:
            if self.rect.colliderect(tree.rect):
                return True
        return False

class create_Tree(pygame.sprite.Sprite):
    def __init__(self, x, y, plant_spawn_time, scale):
        super().__init__()
        self.radius = scale
        self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA) # Set the surface to have an alpha channel
        pygame.draw.circle(self.image, dark_green, (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.state = 2
        self.life = 2500
        self.time = plant_spawn_time

    def tree_update(self):
        self.life += 1


    def collision_test(self, plants):
        for sprite in plants:
            if self.rect.colliderect(sprite.rect):
                return True
        return False

def new_plant(x, y, scale, plants, plant_spawn_time):
    direction = randint(1, 4)
    distance = randint(scale * 2 + scale, scale * 25 + scale)
    if direction == 1:
        plant = create_plant(x + distance, y + (randint(scale * -5, scale * 5,)), scale, plant_spawn_time)
    if direction == 2:
        plant = create_plant(x - distance, y + (randint(scale * -5, scale * 5,)), scale, plant_spawn_time)
    if direction == 3:
        plant = create_plant(x + (randint(scale * -5, scale * 5,)), y - distance, scale, plant_spawn_time)
    if direction == 4:
        plant = create_plant(x + (randint(scale * -5, scale * 5,)), y + distance, scale, plant_spawn_time)
    plant.collision_test(plants)
    if plant.collision_test(plants) == True or plant.rect.x > (screen_width - scale * 3) or \
            plant.rect.x < 0 + scale * 3 or plant.rect.y > (screen_height - scale * 3) or \
            plant.rect.y < 0 + scale * 3:
        plant.kill()
    else:
        plants.add(plant)

class create_herbivore(pygame.sprite.Sprite):
    def __init__(self, x, y, scale, walk, state):
        super().__init__()
        self.state = state
        if self.state == 1:
            self.radius = scale // 1.9
        if self.state == 2:
            self.radius = scale // 1.5
        if self.state == 3:
            self.radius = scale // 1.1
        self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA) # Set the surface to have an alpha channel
        pygame.draw.circle(self.image, BLUE, (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect()
        self.walk = randint(walk, walk * 2)
        self.max_hunger = 3000
        self.hunger = randint(0, self.max_hunger // 2)
        self.rect.x = x
        self.rect.y = y
        self.time = randint(0, 100)
        self.life = 0
        self.max_life = 1000 + randint(0, 1000)
        self.plant_list = ()
        self.xsearch_distance = 0
        self.ysearch_distance = 0
        self.target_x = randint(0, screen_width)
        self.target_y = randint(0, screen_height)
        self.up = 0
        self.down = 0
        self.right = 0
        self.left = 0
        self.random_move_x = 0
        self.random_move_y = 0
        self.danger = 0
        self.looking = randint(scale * 15, scale * 55)

    def update(self, something):
        self.plant_list = (something)

    def play_herbivore(self, carniroves, herbivore_limit, herbivores, scale):
        self.hunger += 1
        self.time += 1
        self.life += 1
        self.list = (self.plant_list)

        # REPRODUCE:
        if self.state == 2 or self.state == 3:
            if self.hunger < self.max_hunger // 2 and self.time > 500 and self.danger == 0:
                closest_sprite = None
                closest_distance = math.inf
                x = screen_width // 2
                y = screen_height // 2
                for herbivore in herbivores:
                    if herbivore != self and herbivore.state != 1:
                        herbivore_pos = (self.rect.x, self.rect.y)
                        sprite_pos = (herbivore.rect.x, herbivore.rect.y)
                        distance = math.dist(sprite_pos, herbivore_pos)
                        if distance < closest_distance:
                            closest_sprite = herbivore
                            closest_distance = distance
                            x = closest_sprite.rect.x
                            y = closest_sprite.rect.y
                            if self.rect.colliderect(herbivore.rect):
                                offsprings = randint(0, 4)
                                delta = 0
                                while delta != offsprings:
                                    delta += 1
                                    herbivore_number = len(herbivores)
                                    if herbivore_number < herbivore_limit:
                                        herbivore = create_herbivore(self.rect.x, self.rect.y, scale, walk, 1)
                                        herbivores.add(herbivore)

        # GROW UP

        if self.life >= self.max_life and self.state == 1:
            herbivore = create_herbivore(self.rect.x, self.rect.y, scale, walk, 2)
            herbivores.add(herbivore)
            self.kill()

        if self.life >= self.max_life and self.state == 2:
            herbivore = create_herbivore(self.rect.x, self.rect.y, scale, walk, 3)
            herbivores.add(herbivore)
            self.kill()



        # EAT

        if self.hunger > self.max_hunger // 4 and self.danger == 0 and self.life > self.max_life // 5:

            closest_sprite = None
            closest_distance = math.inf
            x = self.target_x
            y = self.target_y
            self.random_move_x = 0
            self.random_move_y = 0

            for tree in self.plant_list:
                if tree.state == 2:
                    herbivore_pos = (self.rect.x, self.rect.y)
                    sprite_pos = (tree.rect.x, tree.rect.y)
                    distance = math.dist(sprite_pos, herbivore_pos)
                    if distance < closest_distance:
                        closest_sprite = tree
                        closest_distance = distance
                        x = closest_sprite.rect.x
                        y = closest_sprite.rect.y
                        if self.rect.colliderect(tree.rect):
                            if self.state == 1:
                                tree.life -= 1000
                                self.hunger -= self.max_hunger // 2
                            if self.state == 2:
                                tree.life -= 500
                                self.hunger -= self.max_hunger // 2


            if x > self.rect.x:
                self.rect.x += self.walk
            if x < self.rect.x:
                self.rect.x -= self.walk
            if y > self.rect.y:
                self.rect.y += self.walk
            if y < self.rect.y:
                self.rect.y -= self.walk


        # Random movement
        else:
            random_x = randint(-10000, 10000)
            random_y = randint(-10000, 10000)
            random_c = randint(-10000, 10000)
            self.random_move_x += random_x
            self.random_move_y += random_y
            if self.random_move_x > random_c and self.rect.x < screen_width - scale * 2:
                if  self.life > self.max_life // 5:
                    self.rect.x += self.walk / 3
            if self.random_move_x < random_c and self.rect.x < 0 + scale * 2:
                if self.life > self.max_life // 5:
                    self.rect.x -= self.walk / 3
            if self.random_move_y > random_c and self.rect.y < screen_height - scale * 2:
                if self.life > self.max_life // 5:
                    self.rect.y += self.walk / 3
            if self.random_move_y < random_c and self.rect.y < 0 + scale * 2:
                if self.life > self.max_life // 5:
                    self.rect.y -= self.walk / 3


        # die if too hungry
        if self.hunger == self.max_hunger:
            for herbivore in herbivores:
                if herbivore == self:
                    herbivore.kill()

        # Run from carnivores and screen borders
        closest_carnivore = None
        x = screen_width // 2
        y = screen_height // 2
        closest_distance_carnivore = math.inf
        distance_from_edge = min(self.rect.x, screen_width - self.rect.x, self.rect.y,
                                         screen_height - self.rect.y)
        if distance_from_edge < closest_distance_carnivore:
            closest_distance_carnivore = distance_from_edge
            xcent = screen_width // 2 if self.rect.x >= screen_width // 2 else -screen_width // 2
            ycent = screen_height // 2 if self.rect.y >= screen_height // 2 else -screen_height // 2
        for carnivore in carnivores:
            herbivore_pos = (self.rect.x, self.rect.y)
            sprite_pos = (carnivore.rect.x, carnivore.rect.y)
            distance = math.dist(sprite_pos, herbivore_pos)
            if distance < closest_distance_carnivore:
                closest_carnivore = carnivore
                closest_distance_carnivore = distance
                x = closest_carnivore.rect.x
                y = closest_carnivore.rect.y
                if distance < self.looking:
                    self.danger = 1

                    if self.danger == 1:
                        if x > self.rect.x:
                            self.rect.x -= self.walk
                        if x < self.rect.x:
                            self.rect.x += self.walk
                        if y > self.rect.y:
                            self.rect.y -= self.walk
                        if y < self.rect.y:
                            self.rect.y += self.walk

            else:
                self.danger = 0


class create_carnivore(pygame.sprite.Sprite):
    def __init__(self, x, y, scale, walk):
        super().__init__()
        self.image = pygame.Surface((scale, scale))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.walk = walk * 2
        self.run = 3
        self.max_hunger = 2000
        self.hunger = randint(0, self.max_hunger // 4)
        self.rect.x = x
        self.rect.y = y
        self.time = randint(0, 100)
        self.life = 0
        self.max_life = 10000
        self.state = 0
        self.tree_list = ()
        self.xsearch_distance =screen_width // 2
        self.ysearch_distance = screen_height // 2
        self.state = 0
        self.up = 0
        self.down = 0
        self.right = 0
        self.left = 0
        self.random_move_x = 0
        self.random_move_y = 0
        self.food_list = ()
        self.hunting = 0
        self.v1 = 0
        self.v2 = 0

    def update(self, herbivores):
        self.food_list = (herbivores)

    def play_carnivore(self, carnivores, carnivore_limit, herbivores, scale):
        self.hunger += 1
        self.time += 1
        self.life += 1
        self.list = (self.food_list)

        if self.hunger > self.max_hunger // 3:

            closest_sprite = None
            closest_distance = math.inf
            x = screen_width // 2
            y = screen_height // 2
            self.random_move_x = 0
            self.random_move_y = 0
            self.hunting = 1

            for herbivore in self.list:
                herbivore_pos = (self.rect.x, self.rect.y)
                sprite_pos = (herbivore.rect.x, herbivore.rect.y)
                distanceg = math.dist(sprite_pos, herbivore_pos)
                if distanceg < closest_distance:
                    closest_sprite = herbivore
                    closest_distance = distanceg
                    x = closest_sprite.rect.x
                    y = closest_sprite.rect.y
                    self.v1 = distanceg
                    if self.rect.colliderect(herbivore.rect):
                        herbivore.kill()
                        self.hunger -= self.max_hunger // 2
                        self.hunting = 0


            if x > self.rect.x:
                self.rect.x += self.walk
            if x < self.rect.x:
                self.rect.x -= self.walk
            if y > self.rect.y:
                self.rect.y += self.walk
            if y < self.rect.y:
                self.rect.y -= self.walk

        elif self.hunger < self.max_hunger // 3 and self.time > 1000 and self.hunting == 0:
            closest_sprite = None
            closest_distance = math.inf
            x = screen_width // 2
            y = screen_height // 2

            for carnivore in carnivores:
                if carnivore != self:
                    herbivore_pos = (self.rect.x, self.rect.y)
                    sprite_pos = (carnivore.rect.x, carnivore.rect.y)
                    distanceh = math.dist(sprite_pos, herbivore_pos)
                    if distanceh < closest_distance:
                        closest_sprite = carnivore
                        closest_distance = distanceh
                        x = closest_sprite.rect.x
                        y = closest_sprite.rect.y
                        self.v2 = distanceh
                        if self.rect.colliderect(carnivore.rect):
                            offsprings = randint(0, 2)
                            delta = 0
                            while delta != offsprings:
                                delta += 1
                                carnivore_number = len(carnivores)
                                if carnivore_number < carnivore_limit:
                                    carnivore = create_carnivore(self.rect.x, self.rect.y, scale, walk)
                                    carnivores.add(carnivore)
                                self.time = 0

            if x > self.rect.x:
                self.rect.x += self.walk
            if x < self.rect.x:
                self.rect.x -= self.walk
            if y > self.rect.y:
                self.rect.y += self.walk
            if y < self.rect.y:
                self.rect.y -= self.walk

        else:
            random_x = randint(-10000, 10000)
            random_y = randint(-10000, 10000)
            random_c = randint(-10000, 10000)
            self.random_move_x += random_x
            self.random_move_y += random_y
            if self.random_move_x > random_c:
                self.rect.x += self.walk / 2
            if self.random_move_x < random_c:
                self.rect.x -= self.walk / 2
            if self.random_move_y > random_c:
                self.rect.y += self.walk / 2
            if self.random_move_y < random_c:
                self.rect.y -= self.walk / 2




        if self.rect.x >= screen_width - scale * 2:
            self.rect.x -= 1
        if self.rect.x <= 0 + scale :
            self.rect.x += 1
        if self.rect.y >= screen_height - scale * 2:
            self.rect.y -= 1
        if self.rect.y <= 0 + scale * 2:
            self.rect.y += 1

        if self.hunger == self.max_hunger or self.life == self.max_life:
            for carnivore in carnivores:
                if carnivore == self:
                    carnivore.kill()


class border(pygame.sprite.Sprite):
    def __init__(self, scale, x, y):
        super().__init__()
        self.image = pygame.Surface((scale, scale))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.useless = 0

    def update(self, herbivores):
            self.food_list = (herbivores)
            self.useless += 1

    def play_carnivore(self, carnivores, carnivore_limit, herbivores, scale):
            self.useless += 1


##########################################   DEFINE THE GAME sprites  ##################################################

all_sprites = pygame.sprite.Group()

carnivores = pygame.sprite.Group()

herbivores = pygame.sprite.Group()

plants = pygame.sprite.Group()

camera_group = pygame.sprite.Group()

borders = pygame.sprite.Group()


##########################################           TESTING          ##################################################

all_sprites.add(carnivores)
all_sprites.add(herbivores)
all_sprites.add(plants)
all_sprites.add(borders)
##########################################       MAIN GAME LOOP       ##################################################

counter = 0
while counter != starting_plants:
    counter += 1
    x = randint(0 + scale * 6, screen_width - scale * 6)
    y = randint(0 + scale * 6, screen_height - scale * 6)
    new_plant(x, y, scale, plants, plant_spawn_time)

counter = 0
while counter != starting_herbivores:
    counter += 1
    x = randint(0 + scale * 6, screen_width - scale * 6)
    y = randint(0 + scale * 6, screen_height - scale * 6)
    herbivore = create_herbivore(x, y, scale, walk, 1)
    herbivores.add(herbivore)

for sprite in herbivores:
    herbivore.hunger -= herbivore.max_hunger

counter = 0
while counter != starting_carnivores:
    counter += 1
    x = randint(0 + scale * 6, screen_width - scale * 6)
    y = randint(0 + scale * 6, screen_height - scale * 6)
    carnivore = create_carnivore(x, y, scale, walk)
    carnivores.add(carnivore)

counter = 0
timer = screen_width / 10




timer = 0

Game = True
while Game == True:

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            quit()

        # closing the game on ESCAPE press
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sys.exit()
                quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_i:
                if inventory == 1:
                    inventory = 0
                else:
                    inventory = 1
            if event.key == pygame.K_SPACE:
                if game_paused == 1:
                    game_paused = 0
                    print("game unpaused")
                else:
                    game_paused = 1
                    print("gamepaused")

    # GAME LOGIC HERE:

    timer += 1

    # update plants:
    for sprite in plants:
        sprite.time += 1
        tree_number = len(plants)
        if sprite.state == 2:
            tree.tree_update()
            if sprite.life <= 0:
                sprite.kill()
            if sprite.life >= 5000:
                sprite.life = 5000
        if sprite.time >= plant_spawn_time * 2:
            if sprite.state == 1:
                tree = create_Tree(sprite.rect.x, sprite.rect.y, plant_spawn_time, scale)
                plants.add(tree)
                sprite.kill()
            if sprite.state == 2 and tree_number < tree_limit:
                tree_number = len(plants)
                saplings = randint(2, 25)
                counter = 0
                while counter != saplings:
                    counter += 1
                    new_plant(sprite.rect.x, sprite.rect.y, scale, plants, plant_spawn_time)
                    sprite.time = 0

    # uptade herbivors:
    for herbivore in herbivores:
        herbivore.play_herbivore(carnivores, herbivore_limit, herbivores, scale)
        herbivores.update(plants)

    # uptade carnivores:
    for carnivore in carnivores:
        if carnivore.rect.x < screen_width and carnivore.rect.y < screen_height:
            carnivore.play_carnivore(carnivores, carnivore_limit, herbivores, scale)
            carnivore.update(herbivores)

    # fps = str(int(clock.get_fps()))
    all_sprites.add(carnivores)
    all_sprites.add(herbivores)
    all_sprites.add(plants)

    #Refresh the screen:
    screen.fill(WHITE)
    pygame.draw.rect(screen, (BLACK), empty_rect, scale)
    for sprite in all_sprites:
        screen.blit(sprite.image, sprite.rect)
    # all_sprites.draw(screen)
    pygame.display.update()
    clock.tick(FPS)