import pygame, math


class Plane(pygame.sprite.Sprite):

    def __init__(self, world, startingPosition):
        self.world = world
        super().__init__(self.world.plane_group)
        
        self.startingPosition = startingPosition
        self.position = self.startingPosition
        self.size = 1
        self.width = self.size * 472
        self.height = self.size * 161

        self.speed = 10

        self.velocity = [0, 0]
        self.acceleration = [0, 0]
        self.force = [0, 0]

        self.angle = 0
        self.mass = 10

        self.grounded = True

        self.wheel_position = [round(self.width*(183/236)),round(self.height*(21/23))]

        self.wings_position = [self.width/2, self.height/2]

        self.originalImage = pygame.image.load("plane1.png")
        self.originalImage = pygame.transform.scale(self.originalImage, (self.width, self.height))


    def update(self):
        self.angle = self.angle % 360
        worldPosition = (self.position[0], self.position[1])
        self.image = self.originalImage
        self.rect = self.image.get_rect()
        self.rect.topleft = worldPosition

        # self.acceleration = [0, self.mass/10]

        if self.rect.colliderect(self.world.ground1.hitbox_rect):
            self.grounded = True
        else:
            self.grounded = False



        if self.grounded:
            plane_center = [self.rect.center[0] + self.wheel_position[0], self.rect.center[1] + self.wheel_position[1]]
            self.image, self.rect = rotate_around_pivot(self.image, plane_center, self.wheel_position, self.angle)
        else:
            plane_center = [self.rect.center[0] + self.wings_position[0], self.rect.center[1] + self.wings_position[1]]
            self.image, self.rect = rotate_around_pivot(self.image, plane_center, self.wings_position, self.angle)

        keys = pygame.key.get_pressed()


        nose_angle = self.angle + 12

        if keys[pygame.K_w]:
            self.force[0] += calculate_force(nose_angle, self.speed)[0]
            self.force[1] += calculate_force(nose_angle, self.speed)[1]

        if keys[pygame.K_s]:
            self.force[0] -= calculate_force(nose_angle, self.speed)[0]
            self.force[1] -= calculate_force(nose_angle, self.speed)[1]

        turn_speed = 2
        if keys[pygame.K_a]:
            if self.angle > 180 or  self.angle + turn_speed >= 20 or not self.grounded:
                self.angle += turn_speed

        if keys[pygame.K_d]:
            if self.angle <180 or self.angle - turn_speed >= 345 or not self.grounded:
                self.angle -= turn_speed

        if self.grounded and self.velocity[1] > 0:
            self.velocity[1] = 0


        self.world.position[0] -= self.velocity[0] * self.world.deltaTime
        self.world.position[1] -= self.velocity[1] * self.world.deltaTime

        self.velocity[0] += self.acceleration[0]
        self.velocity[1] += self.acceleration[1]

        self.velocity[0] += self.force[0] / self.mass
        self.velocity[1] += self.force[1] / self.mass
        self.force = [0, 0]



def calculate_force(angle, force):


    xForce = math.cos(math.radians(180-angle))*force
    yForce = math.sin(math.radians(angle))*force


    return [-xForce, -yForce]

def rotate_around_pivot(originalImage, position, pivot, angle):

    image_rect = originalImage.get_rect(topleft = (position[0]-pivot[0], position[1]-pivot[1]))
    offset_center_to_pivot = pygame.math.Vector2([position[0], position[1]]) - image_rect.center

    rotated_offset = offset_center_to_pivot.rotate(-angle)

    rotated_image_center = (position[0] - rotated_offset.x, position[1] - rotated_offset.y)

    image = pygame.transform.rotate(originalImage, angle)
    rect = image.get_rect()
    rect.center = rotated_image_center

    return image, rect