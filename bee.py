import pygame
from random import randint
from os.path import join
pygame.init()

# window
WINDOW_X_Y = 512
display_surface = pygame.display.set_mode((WINDOW_X_Y, WINDOW_X_Y))
pygame.display.set_caption('bumblebee game')
clock = pygame.time.Clock()

running = True

class Bee(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load(join('images', 'bee48.png')).convert_alpha()
        self.rect = self.image.get_frect(center = (WINDOW_X_Y/2, WINDOW_X_Y/2))
        self.mask = pygame.mask.from_surface(self.image)
        self.direction = pygame.Vector2((0,0))
        self.speed = 200
        self.pollen_count = 5
        self.shoot_ability = True

    def shooting(self):
        if self.pollen_count <= 0:
            self.shoot_ability = False
        else:
            self.shoot_ability = True

    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.direction.x = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
        self.direction.y = keys[pygame.K_DOWN] - keys[pygame.K_UP]
        if self.direction:
            self.direction.normalize()
        else:
            self.direction
        self.rect.center += self.direction * self.speed * dt

        recent_keys = pygame.key.get_just_pressed()
        if recent_keys[pygame.K_SPACE] and self.shoot_ability == True:
            Pollen(pollen_surf, bee.rect.midtop, (all_sprites, pollen_sprites))
            if bee.pollen_count > 0:
                bee.pollen_count -=1
        self.shooting()
        collisions()

class Pollen(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(midbottom = pos)

    def update(self, dt):
        self.rect.centery -= 300 * dt
        if self.rect.bottom < 0:
            self.kill()

class Honey(pygame.sprite.Sprite):
    def __init__(self, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center = (randint(0, WINDOW_X_Y), randint(0,WINDOW_X_Y)))

class Flower(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(midbottom = pos)

class Seeds(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center = pos)
        self.speed = randint(100,200)

    def update(self, dt):
        self.rect.centery += self.speed * dt
        if self.rect.top > WINDOW_X_Y:
            self.kill()
        
def collisions():
    collision_bee_honey = pygame.sprite.spritecollide(bee, honey_sprites, True, pygame.sprite.collide_mask)
    if collision_bee_honey:
        bee.pollen_count += 1
    for pollen in pollen_sprites:
        collision_pollen_seed = pygame.sprite.spritecollide(pollen, seeds_sprites, True, pygame.sprite.collide_mask)
        if collision_pollen_seed:
            pollen.kill()
            Flower(flower_surf, pollen.rect.midtop, (all_sprites, flower_sprites))

# sprite groups
all_sprites = pygame.sprite.Group()
honey_sprites = pygame.sprite.Group()
pollen_sprites = pygame.sprite.Group()
flower_sprites = pygame.sprite.Group()
seeds_sprites = pygame.sprite.Group()
bee = Bee(all_sprites)

# imports
pollen_surf = pygame.image.load(join('images', 'pollen.png')).convert_alpha()
flower_surf = pygame.image.load(join ('images', 'flower.png')).convert_alpha()
honey_surf = pygame.image.load(join ('images', 'honey.png')).convert_alpha()
seeds_surf = pygame.image.load(join ('images', 'seeds.png')).convert_alpha()

# custom events
honey_event = pygame.event.custom_type()
pygame.time.set_timer(honey_event, randint(3000, 7000))
seeds_event = pygame.event.custom_type()
pygame.time.set_timer(seeds_event, 3000)

# game loop
while running:
    dt = clock.tick()/1000
    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == honey_event:
            Honey(honey_surf, (all_sprites, honey_sprites))
        if event.type == seeds_event:
            Seeds(seeds_surf, (randint(0, WINDOW_X_Y), randint(-150,-100)), (all_sprites, seeds_sprites))

    display_surface.fill((0,0,0))
    all_sprites.update(dt)
    all_sprites.draw(display_surface)
    collisions()
    pygame.display.update()

pygame.quit()