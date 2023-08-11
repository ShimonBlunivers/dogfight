import pygame, random


class WorldGenerator:
    def __init__(self, world):
        self.world = world

        self.chunks = []

        self.new_world = True

        self.player_on_chunk = 0

        self.leftmost_chunk = None
        self.rightmost_chunk = None

        self.first_height = 0
        self.last_height = 0
        if self.new_world == True:
            self.generate_spawn()


    def generate_spawn(self):
            for i in range(3):
                chunk = Chunk(self.world, i, self.last_height)
                self.last_height = chunk.last_height
                self.chunks.append(chunk)
                self.rightmost_chunk = chunk
            self.first_height = self.chunks[0].previous_height
            self.leftmost_chunk = self.chunks[0]

    def update(self):

        self.player_on_index = int(-(self.world.position[0] - self.world.resolution[0]/2) // self.world.chunk_width)

        if self.player_on_index >= self.rightmost_chunk.index-2:
            chunk = Chunk(self.world, self.rightmost_chunk.index+1, self.rightmost_chunk.last_height)
            self.chunks.append(chunk)
            self.rightmost_chunk = chunk


class Chunk:
    def __init__(self, world, index: int, previous_height, points = []):
        self.world = world
        self.index = index
        self.points = points
        self.previous_height = previous_height



        self.active = False

        # self.color = [139, 69, 19]

        self.color = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]

        self.width = self.world.chunk_width
        self.scale = 1

        self.position_in_world = self.width * self.index

        if points == []:
            self.generate()

    def generate(self, intensity = 50):
        density = 10
        width = self.width

        width *= self.scale # Šířka chunku
        density *= self.scale # Počet výškových bodů
        intensity *= self.scale # Síla zdeformování každého bodu

        point_distance = width / density

        points = [[0, self.world.bedrock], [0, self.previous_height]]

        last = self.previous_height
        for i in range(int(density)):
            last += random.randint(0, intensity*2) - intensity
            if last > 600:
                last -= intensity

            points.append([(i +1) *point_distance, last])

        points.append([width, self.world.bedrock])

        self.last_height = last
        self.points = points


    def update(self, worldPosition):


        x0 = self.points[0][0] + worldPosition[0] + self.position_in_world
        x1 = self.points[-1][0] + worldPosition[0] + self.position_in_world


        if x0 > self.world.resolution[0]:
            self.active = False
        else:
            self.active = True

        if x1 < - self.world.resolution[0]/4:
            self.active = False
        else:
            self.active = True
        if self.active:
            self.draw(worldPosition)

    def draw(self, worldPosition):
        
        points = []

        for point in self.points:

            x = point[0] + worldPosition[0] + self.width * self.index
            y = point[1] + worldPosition[1]

            points.append([x, y])


        pygame.draw.polygon(self.world.screen, self.color, points)

            