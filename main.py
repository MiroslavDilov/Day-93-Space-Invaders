import pygame

pygame.init()

window = pygame.display.set_mode((640, 480))


running = True


class Spaceship:
    def __init__(self):
        self.x = 320
        self.y = 400

        self.move_speed = 4

        self.rect = pygame.Rect(self.x, self.y, 40, 40)

    def draw(self):
        self.rect.center = self.x, self.y
        pygame.draw.rect(window, (0,255,0), self.rect)

    def move(self, event):
        if event.key == pygame.K_LEFT and self.rect.left > 0:
            self.x -= self.move_speed
        if event.key == pygame.K_RIGHT and self.rect.right < 640:
            self.x += self.move_speed


class Invader:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.rect = pygame.Rect(self.x, self.y, 20, 20)

    def draw(self):
        self.rect.center = self.x, self.y
        pygame.draw.rect(window, (0,255,0), self.rect)


class Projectile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, 10, 40)

    def draw(self):
        pygame.draw.rect(window, (0,255, 0), self.rect)


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


spaceship = Spaceship()
invaders = spawn_invaders(3, 20)
projectile = None

while running:
    pygame.key.set_repeat(15)
    window.fill((0,0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            spaceship.move(event)
            if event.key == pygame.K_SPACE:
                projectile = Projectile(spaceship.x, spaceship.rect.top)


    for invader in invaders:
        invader.draw()

    if projectile is not None:
        projectile.draw()
        projectile.rect.y -= 2

    spaceship.draw()
    pygame.display.flip()
