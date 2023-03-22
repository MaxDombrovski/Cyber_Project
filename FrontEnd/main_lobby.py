import pygame
import sys
from PIL import Image
from random import randint
# from menu import menu


class Tree(pygame.sprite.Sprite):
    def __init__(self, position, group):
        super().__init__(group)
        self.image = pygame.image.load("environment_assets/tree.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=position)


class Player(pygame.sprite.Sprite):
    def __init__(self, position, group):
        super().__init__(group)
        # images for the player
        self.combine_images()
        self.image = pygame.image.load("player_assets/full_body.png").convert_alpha()
        self.rect = self.image.get_rect(center=position)

        # direction of player's movement and his velocity
        self.direction = pygame.math.Vector2()
        self.velocity = 5

    def movement_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            self.direction.y = -1
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pygame.K_LEFT]:
            self.direction.x = -1
        elif keys[pygame.K_RIGHT]:
            self.direction.x = 1
        else:
            self.direction.x = 0

    def update(self):
        self.movement_input()
        self.rect.center += self.direction * self.velocity

    def combine_images(self):
        images = []
        images.append(Image.open("player_assets/body.png"))
        images.append(Image.open("player_assets/TopHatSmall.png"))
        images.append(Image.open("player_assets/SuitSmall.png"))
        images.append(Image.open("player_assets/ShortsSmall.png"))
        images.append(Image.open("player_assets/CrocsSmall.png"))

        new_image = Image.new("RGBA", (100, 270))

        for i in range(len(images)):
            new_image = Image.alpha_composite(new_image, images[i])

        new_image.save("player_assets/full_body.png", format="png")


class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()

        # offset
        self.camera_offset = pygame.math.Vector2()
        self.half_w = self.display_surface.get_size()[0] // 2
        self.half_h = self.display_surface.get_size()[1] // 2

        # background
        self.bg = pygame.image.load("environment_assets/purple.png").convert_alpha()
        self.bg_rect = self.bg.get_rect(topleft=(0, 0))

    def custom_draw(self, player):

        # player elements
        self.camera_offset.x = player.rect.centerx - self.half_w
        self.camera_offset.y = player.rect.centery - self.half_h

        # background elements
        background_offset = self.bg_rect.topleft - self.camera_offset
        self.display_surface.blit(self.bg, background_offset)

        # active elements
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            active_offset = sprite.rect.topleft - self.camera_offset
            self.display_surface.blit(sprite.image, active_offset)

class Game(object):

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        parent.client_socket.send("hi".encode())

        pygame.init()
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption('lobby')
        clock = pygame.time.Clock()
        pygame.event.set_grab(True)

        camera_group = CameraGroup()
        player = Player((640,360), camera_group)

        # tree randomizer
        for i in range(20):
            random_x = randint(0, 1000)
            random_y = randint(0, 1000)
            Tree((random_x, random_y), camera_group)

        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

            screen.fill('skyblue')

            camera_group.update()
            camera_group.custom_draw(player)

            pygame.display.update()
            clock.tick(60)


if __name__ == '__main__':
    g = Game()
