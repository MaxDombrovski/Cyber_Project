import pygame
import sys
from PIL import Image
from random import randint
# from menu import menu


class Tree(pygame.sprite.Sprite):
    def __init__(self, position, group):
        super().__init__(group)
        self.image = pygame.image.load("FrontEnd/environment_assets/tree.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=position)


class Player(pygame.sprite.Sprite):
    def __init__(self, start_position, group):
        super().__init__(group)
        # player position
        self.x = start_position[0]
        self.y = start_position[1]
        # images for the player
        self.combine_images()
        self.image = pygame.image.load("FrontEnd/player_assets/full_body.png").convert_alpha()
        self.rect = self.image.get_rect(center=start_position)

    def get_rect_position(self):
        return str(self.x) + "," + str(self.y)

    def movement(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            self.y += -5
        elif keys[pygame.K_DOWN]:
            self.y += 5
        else:
            self.y += 0

        if keys[pygame.K_LEFT]:
            self.x += -5
        elif keys[pygame.K_RIGHT]:
            self.x += 5
        else:
            self.x += 0

        self.update((self.x, self.y))

    def update(self, update_position):
        self.rect.center = update_position

    def combine_images(self):
        images = []
        images.append(Image.open("FrontEnd/player_assets/body.png"))
        images.append(Image.open("FrontEnd/player_assets/TopHatSmall.png"))
        images.append(Image.open("FrontEnd/player_assets/SuitSmall.png"))
        images.append(Image.open("FrontEnd/player_assets/ShortsSmall.png"))
        images.append(Image.open("FrontEnd/player_assets/CrocsSmall.png"))

        new_image = Image.new("RGBA", (100, 270))

        for i in range(len(images)):
            new_image = Image.alpha_composite(new_image, images[i])

        new_image.save("FrontEnd/player_assets/full_body.png", format="png")


class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()

        # offset
        self.camera_offset = pygame.math.Vector2()
        self.half_w = self.display_surface.get_size()[0] // 2
        self.half_h = self.display_surface.get_size()[1] // 2

        # background
        self.bg = pygame.image.load("FrontEnd/environment_assets/purple.png").convert_alpha()
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

    def __init__(self, csocket=None):
        self.csocket = csocket
        self.main_player = int(self.csocket.recv(1024).decode('utf-8'))

        pygame.init()
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption('lobby')
        clock = pygame.time.Clock()
        pygame.event.set_grab(True)

        camera_group = CameraGroup()
        players = []
        for i in range(10):
            players.append(Player((640, 360), camera_group))
            i += 1

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

            players[self.main_player].movement()
            int_player_pos_list = self.server_data_conversion(players)
            for i in range(0, len(players)):
                players[i].update(int_player_pos_list[i])

            camera_group.custom_draw(players[self.main_player])

            pygame.display.update()
            clock.tick(60)

    def server_data_conversion(self, players):
        player_position_string = players[self.main_player].get_rect_position()
        self.csocket.send(player_position_string.encode('utf-8'))

        all_player_position_string = self.csocket.recv(1024).decode('utf-8')
        all_player_position_string = all_player_position_string.split(",")
        all_player_position_list = []
        for i in range(0, len(all_player_position_string), 2):
            all_player_position_string[i] = int(all_player_position_string[i])
            all_player_position_string[i+1] = int(all_player_position_string[i+1])
            all_player_position_list.append((all_player_position_string[i], all_player_position_string[i + 1]))

        return all_player_position_list


if __name__ == '__main__':
    g = Game()
