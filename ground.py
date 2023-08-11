import pygame


class Ground(pygame.sprite.Sprite):

    def __init__(self, world, world_generator, startingPosition = None):
        self.world = world
        super().__init__(self.world.ground_group)
        if startingPosition == None:
            startingPosition = [0, self.world.resolution[1] - self.world.resolution[1]/3]

        self.startingPosition = startingPosition
        self.position = self.startingPosition

        self.world_generator = world_generator

        self.color = [80, 40, 0]
        self.width = self.world.resolution[0] * 10
        self.height = self.world.resolution[1] - self.position[1]

        self.hitbox_rect = pygame.Rect(self.startingPosition[0], self.startingPosition[1] + self.height/2, self.width, self.height/2)
        self.rect = pygame.Rect(self.startingPosition[0], self.startingPosition[1], self.width, self.height)
        self.originalImage = pygame.image.load("ground1.png")
        self.originalImage = pygame.transform.scale(self.originalImage, (self.width, self.height))


    def update(self):

        worldPosition = (self.position[0] + self.world.position[0], self.position[1] + self.world.position[1])

        self.draw_polygon(worldPosition)
        self.image = self.originalImage
        self.rect = self.image.get_rect()
        self.rect.topleft = worldPosition
        self.hitbox_rect.x = worldPosition[0]
        self.hitbox_rect.y = worldPosition[1]

        self.open_height_map()


    def open_height_map(self):


        intensity = 10

        file = open("ground_height_map.txt", mode="r")



        height_map = file.read()
        height_map = height_map.split("\n")


        point_distance = self.width / len(height_map)

        points = [[0,self.height], [0, 0]]


        for i in range(len(height_map)):

            points.append([point_distance*i, -int(height_map[i]) * intensity])

        points.append([self.width, 0])
        points.append([self.width, self.height])

        return points

    def draw_polygon(self, worldPosition):

        color = [139, 69, 19]

        points = []

        for point in self.polygon_points:

            x = point[0] + worldPosition[0]
            y = point[1] + worldPosition[1]

            points.append([x, y])


        pygame.draw.polygon(self.world.screen, color, points)


