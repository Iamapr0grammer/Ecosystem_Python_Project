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
scale = 20

# set up the text font
test_font = pygame.font.Font(None, 150)

# set the clock function
clock = pygame.time.Clock()

timer = 0

# time between plant reproduce
plant_spawn_time = 200

# starting plants
starting_plants = 20

# starting herbivores
starting_herbivores = 6

# starting herbivores
starting_carnivores = 2

carnivore_limit = 10
tree_limit = 100
herbivore_limit = 30



##########################################    DEFINE THE GAME COLORS  ##################################################

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
light_green = (0, 141, 85)
dark_green = (51, 85, 0)
BLUE = (15, 82, 186)
RED = (255, 0, 0)

# # create the border of the game
empty_rect = pygame.Rect(0, 0, screen_width, screen_height)

##########################################   DEFINE THE GAME Classes  ##################################################

class create_plant(pygame.sprite.Sprite):
    def __init__(self, x, y, scale, plant_spawn_time):
        super().__init__()
        self.image = pygame.Surface((scale, scale))
        self.image.fill(light_green)
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
    def __init__(self, x, y, scale):
        super().__init__()
        self.image = pygame.Surface((scale, scale))
        self.image.fill(dark_green)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.state = 2
        self.time = 0

    def collision_test(self, plants):
        for sprite in plants:
            if self.rect.colliderect(sprite.rect):
                return True
        return False

def new_plant(x, y, scale, plants, plant_spawn_time):
    direction = randint(1, 4)
    distance = randint(scale * 2 + scale, scale * 5 + scale)
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
    def __init__(self, x, y, scale):
        super().__init__()
        self.image = pygame.Surface((scale, scale))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.walk = randint(1,2)
        self.run = 3
        self.max_hunger = 2000
        self.hunger = randint(0, self.max_hunger // 2)
        self.rect.x = x
        self.rect.y = y
        self.time = randint(0, 100)
        self.state = 0
        self.tree_list = ()
        self.xsearch_distance = 0
        self.ysearch_distance = 0
        self.state = 0
        self.up = 0
        self.down = 0
        self.right = 0
        self.left = 0
        self.random_move_x = 0
        self.random_move_y = 0
        self.danger = 0
        self.looking = randint(scale * 15, scale * 25)

    def update(self, something):
        self.tree_list = (something)

    def play_herbivore(self, carniroves, herbivores, scale):
        self.hunger += 1
        self.time += 1
        self.list = (self.tree_list)

        if self.hunger > self.max_hunger // 4 and self.danger == 0:

            closest_sprite = None
            closest_distance = math.inf
            x = 0
            y = 0
            self.random_move_x = 0
            self.random_move_y = 0

            for tree in self.list:
                herbivore_pos = (self.rect.x, self.rect.y)
                sprite_pos = (tree.rect.x, tree.rect.y)
                distance = math.dist(sprite_pos, herbivore_pos)
                if distance < closest_distance:
                    closest_sprite = tree
                    closest_distance = distance
                    x = closest_sprite.rect.x
                    y = closest_sprite.rect.y
                    if self.rect.colliderect(tree.rect):
                        tree.kill()
                        self.hunger -= self.max_hunger // 2

            # for other_herbivore in herbivores:
            #     if other_herbivore != self:
            #         herbivore_pos = (self.rect.x, self.rect.y)
            #         other_herbivore_pos = (other_herbivore.rect.x, other_herbivore.rect.y)
            #         distance = math.dist(herbivore_pos, other_herbivore_pos)
            #         if distance < scale:  # adjust this value to set the minimum distance between herbivores
            #             if other_herbivore.rect.x > self.rect.x:
            #                 other_herbivore.rect.x -= scale
            #             if other_herbivore.rect.x < self.rect.x:
            #                 self.rect.x += scale
            #             if other_herbivore.rect.y > self.rect.y:
            #                 other_herbivore.rect.y -= scale
            #             if other_herbivore.rect.y < self.rect.y:
            #                 self.rect.y += scale

            if x > self.rect.x:
                self.rect.x += self.walk
            if x < self.rect.x:
                self.rect.x -= self.walk
            if y > self.rect.y:
                self.rect.y += self.walk
            if y < self.rect.y:
                self.rect.y -= self.walk

        elif self.hunger < self.max_hunger // 2 and self.time > 500 and self.danger == 0:
            closest_sprite = None
            closest_distance = math.inf
            x = 0
            y = 0

            for other_herbivore in herbivores:
                if other_herbivore != self:
                    herbivore_pos = (self.rect.x, self.rect.y)
                    sprite_pos = (other_herbivore.rect.x, other_herbivore.rect.y)
                    distance = math.dist(sprite_pos, herbivore_pos)
                    if distance < closest_distance:
                        closest_sprite = other_herbivore
                        closest_distance = distance
                        x = closest_sprite.rect.x
                        y = closest_sprite.rect.y
                        if self.rect.colliderect(other_herbivore.rect):
                            offsprings = randint(0, 3)
                            delta = 0
                            while delta != offsprings:
                                delta += 1
                                herbivore = create_herbivore(self.rect.x, self.rect.y, scale)
                                herbivores.add(herbivore)
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
                self.rect.x += self.walk / 3
            if self.random_move_x < random_c:
                self.rect.x -= self.walk / 3
            if self.random_move_y > random_c:
                self.rect.y += self.walk / 3
            if self.random_move_y < random_c:
                self.rect.y -= self.walk / 3

        if self.hunger == self.max_hunger:
            for herbivore in herbivores:
                if herbivore == self:
                    herbivore.kill()

        closest_carnivore = None
        closest_distance_carnivore = math.inf
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
                        if closest_carnivore.rect.x > self.rect.x:
                            self.rect.x -= self.walk
                        if closest_carnivore.rect.x < self.rect.x:
                            self.rect.x += self.walk
                        if closest_carnivore.rect.y > self.rect.y:
                            self.rect.y -= self.walk
                        if closest_carnivore.rect.y < self.rect.y:
                            self.rect.y += self.walk

            else:
                self.danger = 0




class create_carnivore(pygame.sprite.Sprite):
    def __init__(self, x, y, scale):
        super().__init__()
        self.image = pygame.Surface((scale, scale))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.walk = 2
        self.run = 3
        self.max_hunger = 2000
        self.hunger = randint(0, self.max_hunger // 4)
        self.rect.x = x
        self.rect.y = y
        self.time = randint(0, 100)
        self.state = 0
        self.tree_list = ()
        self.xsearch_distance = 0
        self.ysearch_distance = 0
        self.state = 0
        self.up = 0
        self.down = 0
        self.right = 0
        self.left = 0
        self.random_move_x = 0
        self.random_move_y = 0
        self.food_list = ()

    def update(self, herbivores):
        self.food_list = (herbivores)

    def play_carnivore(self, carnivores, scale):
        self.hunger += 1
        self.time += 1
        self.list = (self.food_list)
        print(self.hunger)

        if self.hunger > self.max_hunger // 3:

            closest_sprite = None
            closest_distance = math.inf
            x = 0
            y = 0
            self.random_move_x = 0
            self.random_move_y = 0

            for herbivore in self.list:
                herbivore_pos = (self.rect.x, self.rect.y)
                sprite_pos = (herbivore.rect.x, herbivore.rect.y)
                distance = math.dist(sprite_pos, herbivore_pos)
                if distance < closest_distance:
                    closest_sprite = herbivore
                    closest_distance = distance
                    x = closest_sprite.rect.x
                    y = closest_sprite.rect.y
                    if self.rect.colliderect(herbivore.rect):
                        herbivore.kill()
                        self.hunger -= self.max_hunger // 2

            # for other_carnivore in carnivores:
            #     if other_carnivore != self:
            #         herbivore_pos = (self.rect.x, self.rect.y)
            #         other_herbivore_pos = (other_carnivore.rect.x, other_carnivore.rect.y)
            #         distance = math.dist(herbivore_pos, other_herbivore_pos)
            #         if distance < scale:  # adjust this value to set the minimum distance between herbivores
            #             if other_carnivore.rect.x > self.rect.x:
            #                 other_carnivore.rect.x -= scale
            #             if other_carnivore.rect.x < self.rect.x:
            #                 self.rect.x += scale
            #             if other_carnivore.rect.y > self.rect.y:
            #                 other_carnivore.rect.y -= scale
            #             if other_carnivore.rect.y < self.rect.y:
            #                 self.rect.y += scale

            if x > self.rect.x:
                self.rect.x += self.walk
            if x < self.rect.x:
                self.rect.x -= self.walk
            if y > self.rect.y:
                self.rect.y += self.walk
            if y < self.rect.y:
                self.rect.y -= self.walk

        elif self.hunger < self.max_hunger // 3 and self.time > 1000:
            closest_sprite = None
            closest_distance = math.inf
            x = 0
            y = 0

            for other_carnivore in carnivores:
                if other_carnivore != self:
                    herbivore_pos = (self.rect.x, self.rect.y)
                    sprite_pos = (other_carnivore.rect.x, other_carnivore.rect.y)
                    distance = math.dist(sprite_pos, herbivore_pos)
                    if distance < closest_distance:
                        closest_sprite = other_carnivore
                        closest_distance = distance
                        x = closest_sprite.rect.x
                        y = closest_sprite.rect.y
                        if self.rect.colliderect(other_carnivore.rect):
                            offsprings = randint(0, 2)
                            delta = 0
                            while delta != offsprings:
                                delta += 1
                                carnivore = create_carnivore(self.rect.x, self.rect.y, scale)
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
                self.rect.x += self.walk / 3
            if self.random_move_x < random_c:
                self.rect.x -= self.walk / 3
            if self.random_move_y > random_c:
                self.rect.y += self.walk / 3
            if self.random_move_y < random_c:
                self.rect.y -= self.walk / 3

        if self.hunger == self.max_hunger:
            for carnivore in carnivores:
                if carnivore == self:
                    carnivore.kill()





##########################################   DEFINE THE GAME sprites  ##################################################

all_sprites = pygame.sprite.Group()

carnivores = pygame.sprite.Group()

herbivores = pygame.sprite.Group()

plants = pygame.sprite.Group()

camera_group = pygame.sprite.Group()

##########################################           TESTING          ##################################################

all_sprites.add(carnivores)
all_sprites.add(herbivores)
all_sprites.add(plants)
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
    herbivore = create_herbivore(x, y, scale)
    herbivores.add(herbivore)

counter = 0
while counter != starting_carnivores:
    counter += 1
    x = randint(0 + scale * 6, screen_width - scale * 6)
    y = randint(0 + scale * 6, screen_height - scale * 6)
    carnivore = create_carnivore(x, y, scale)
    carnivores.add(carnivore)

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
        if sprite.time == plant_spawn_time:
            if sprite.state == 1:
                tree = create_Tree(sprite.rect.x, sprite.rect.y, scale)
                plants.add(tree)
                plants.remove(sprite)
                sprite.kill()
                sprite.time = 0
            if sprite.state == 2:
                tree_number = len(plants)
                if tree_number < tree_limit:
                    new_plant(sprite.rect.x, sprite.rect.y, scale, plants, plant_spawn_time)
                    sprite.time = 0

    # uptade herbivors:
    for herbivore in herbivores:
        herbivore.play_herbivore(carnivores, herbivores, scale)
        herbivores.update(plants)

    # uptade carnivores:
    for carnivore in carnivores:
        carnivore.play_carnivore(carnivores, scale)
        carnivore.update(herbivores)

    # prevent creatures from moving out of the screen
    for sprite in all_sprites:
        if sprite.rect.x < scale:
            sprite.rect.x = screen_width - (scale * 2)
        if sprite.rect.x > screen_width - scale:
            sprite.rect.x = 0 + scale * 2
        if sprite.rect.y < scale:
            sprite.rect.y = screen_height - (scale * 2)
        if sprite.rect.y > screen_height - scale:
            sprite.rect.y = scale * 2

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