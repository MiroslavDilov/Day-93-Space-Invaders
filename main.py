import pygame
from random import randint

pygame.init()

window = pygame.display.set_mode((640, 480))


running = True


clock = pygame.time.Clock()


class Spaceship:
    def __init__(self):
        self.x = 320
        self.y = 400
        self.img = pygame.image.load('images/spaceship.png')

        self.move_speed = 1

        self.rect = pygame.Rect(self.x, self.y, 40, 40)

        self.moving = False
        self.direction = ''

    def draw(self):
        self.rect.center = self.x, self.y
        # pygame.draw.rect(window, (0,255,0), self.rect)
        window.blit(self.img, self.rect)

    def start_move(self, key):
        if key == pygame.K_LEFT:
            self.direction = 'left'
            self.moving = True
        elif key == pygame.K_RIGHT:
            self.direction = 'right'
            self.moving = True

    def stop_move(self):
        self.moving = False

    def move(self):
        if self.moving:
            if self.direction == 'left' and self.rect.left > 0:
                self.x -= self.move_speed
            if self.direction == 'right' and self.rect.right < 640:
                self.x += self.move_speed


class Invader:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.img = pygame.image.load('images/invader.png')

        self.rect = pygame.Rect(self.x, self.y, 20, 20)

    def draw(self):
        self.rect.center = self.x, self.y
        # pygame.draw.rect(window, (0,255,0), self.rect)
        window.blit(self.img, self.rect)

    def check_collision(self, proj_rect):
        return self.rect.colliderect(proj_rect)


class Projectile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, 10, 30)

    def draw(self):
        pygame.draw.rect(window, (255,255, 255), self.rect)


class Particle:
    def __init__(self, x, y):
        # Postition
        self.x = x
        self.y = y

        # Velocity
        self.x_velocity = randint(0, 20) / 10 - 1
        self.y_velocity = randint(-4,-1) / 2

        self.timer = 10
        self.time_delete = 0.1

        self.radius = randint(3,4)

    def draw(self):
        self.x += self.x_velocity
        self.y += self.y_velocity

        self.timer -= self.time_delete
        pygame.draw.circle(window, (255,255,255), (self.x, self.y), self.radius)


class SpaceshipParticle:
    def __init__(self, x, y):
        # Postition
        self.x = x
        self.y = y

        # Velocity
        self.x_velocity = randint(0, 20) / 10 - 1
        self.y_velocity = randint(1,2) / 2

        self.timer = 7
        self.time_delete = 0.1

        self.radius = randint(1,3)

    def draw(self):
        self.x += self.x_velocity
        self.y += self.y_velocity

        self.timer -= self.time_delete
        pygame.draw.circle(window, (252, 177, 3), (self.x, self.y), self.radius)


def spawn_invaders(row, col):
    invader_array = []

    space_for_invader = 640 / col
    x = space_for_invader / 2
    y = 60
    row_space = 50

    for i in range(row):
        for j in range(col):
            invader = Invader(x, y)
            x += space_for_invader
            invader_array.append(invader)
        x = space_for_invader / 2
        y += row_space

    return invader_array


def spawn_particles(x, y):
    array = []

    for i in range(5):
        array.append(Particle(x, y))

    return array


spaceship = Spaceship()
invaders = spawn_invaders(3, 10)
projectiles = []
particles = []
spaceship_particles = []
time = 0

while running:
    clock.tick(250)
    time += clock.get_time()
    # print(time//100)

    window.fill((0,0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            spaceship.start_move(event.key)
            if event.key == pygame.K_SPACE:
                projectiles.append(Projectile(spaceship.rect.center[0], spaceship.rect.top))
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                spaceship.stop_move()

    for invader in invaders:
        invader.draw()

    if len(projectiles) >= 1:
        for projectile in projectiles:
            projectile.draw()
            projectile.rect.y -= 2
            if len(invaders) >= 1:
                for invader in invaders:
                    if invader.check_collision(projectile.rect):
                        invaders.remove(invader)
                        projectiles.remove(projectile)
                        particles.append(spawn_particles(projectile.rect.midtop[0], projectile.rect.midtop[1]))

    if len(particles) >= 1:
        for particles_place in particles:
            for particle in particles_place:
                particle.draw()
                if particle.timer < 0:
                    particles_place.remove(particle)

    spaceship_particles.append(SpaceshipParticle(spaceship.rect.midbottom[0], spaceship.rect.midbottom[1]))
    for particle in spaceship_particles:
        particle.draw()
        if particle.timer < 0:
            spaceship_particles.remove(particle)

    spaceship.move()
    spaceship.draw()
    pygame.display.flip()
