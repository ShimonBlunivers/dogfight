import pygame, time

from ground import Ground
from plane import Plane
from world import WorldGenerator

pygame.init()

def update_world(world):
    world.world_generator.update()
    for chunk in world.world_generator.chunks:
        chunk.update(world.position)


class World:

    def __init__(self):
        self.running = True
        self.resolution = (1280,720)
        self.screen = pygame.display.set_mode([self.resolution[0], self.resolution[1]])
        self.main_clock = pygame.time.Clock()
        self.FPS = 60
        self.background_color = [160, 230, 255]
        self.position = [0, 0]
        self.prev_time = time.time()
        self.mouse_position = pygame.mouse.get_pos()

        self.bedrock = 1600 # Konec mapy v Y souřadnici
        self.chunk_width = 400 # Šířka jednoho chunku



        self.plane_group = pygame.sprite.Group()
        self.ground_group = pygame.sprite.Group()
        self.projectile_group = pygame.sprite.Group()
        # WORLD INIT

        self.world_generator = WorldGenerator(self)
        self.ground1 = Ground(self, self.world_generator)
        self.plane1 = Plane(self, [100, 350])


    def update(self):

        self.screen.fill(self.background_color)

        #   TIME   
        self.main_clock.tick(self.FPS)
        self.now = time.time()
        self.deltaTime = (self.now - self.prev_time) * 100
        self.prev_time = self.now

        self.mouse_position = pygame.mouse.get_pos()

        update_world(self)
        # self.ground_group.draw(self.screen)
        self.plane_group.update()
        self.plane_group.draw(self.screen)
        self.projectile_group.update()


        pygame.display.flip()


world = World()



while world.running:

    world.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            world.running = False



