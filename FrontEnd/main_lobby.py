import pygame
import sys
from PIL import Image
from random import randint


class Tree(pygame.sprite.Sprite):
    def __init__(self, position, group):
        super().__init__(group)
        self.image = pygame.image.load("FrontEnd/environment_assets/tree.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=position)


class Chat:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.base_font = pygame.font.SysFont('Calibri', 72)
        self.bubble_font = pygame.font.SysFont('Comic Sans MS', 48)
        self.user_text = ""

        self.input = pygame.image.load("FrontEnd/player_assets/chatbox.png").convert_alpha()
        self.input.set_alpha(100)
        self.chatboxpos = (0, self.display_surface.get_size()[1] - self.input.get_height())
        self.input_rect = self.input.get_rect(topleft=self.chatboxpos)

        self.active = False
    def draw(self):
        self.display_surface.blit(self.input, self.chatboxpos)

        text_surface = self.base_font.render(self.user_text, True, (0, 0, 0))
        self.display_surface.blit(text_surface, (self.input_rect.x + 260, self.input_rect.y + 20))

    def check_mouse_collision(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.input_rect.collidepoint(event.pos):
                self.set_active_status(True)
            else:
                self.set_active_status(False)

    def writing(self, event):
        if self.active:
            if event.key == pygame.K_BACKSPACE:
                self.user_text = self.user_text[:-1]
            elif event.key == pygame.K_DOLLAR:
                pass
            else:
                self.user_text += event.unicode

    def bubble(self, text, x, y):
        text_surface = self.bubble_font.render(text, True, (0, 0, 0))
        self.display_surface.blit(text_surface, (x-text_surface.get_width()//2, y))

    def get_user_text(self):
        return self.user_text

    def get_active_status(self):
        return self.active

    def set_user_text(self, text):
        self.user_text = text

    def set_active_status(self, active):
        self.active = active
        if active:
            self.input.set_alpha(255)
        else:
            self.input.set_alpha(100)


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

        self.chat = Chat()

    def get_rect_position(self):
        return str(self.x) + "," + str(self.y)

    def movement(self):
        if self.chat.get_active_status():
            self.x += 0
            self.y += 0
        else:
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
        images.append(Image.open(f"FrontEnd/player_assets/body.png"))
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
        self.bg = pygame.image.load("FrontEnd/environment_assets/grass.png").convert_alpha()
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

    def __init__(self, csocket=None, appearance_list=None):
        self.csocket = csocket
        self.main_player = int(self.csocket.recv(1024).decode('utf-8'))

        # set up the screen
        pygame.init()
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption('lobby')
        clock = pygame.time.Clock()
        pygame.event.set_grab(True)

        # preposition all the possible players
        camera_group = CameraGroup()
        players = []
        for i in range(10):
            players.append(Player((0, 0), camera_group))
            i += 1

        # tree randomizer
        for i in range(10):
            for j in range(10):
                if i % 2 == 0:
                    Tree((j*300 + 150, i * 300), camera_group)
                else:
                    Tree((j * 300, i * 300), camera_group)

        # chat box
        chat = Chat()
        client_msg = ' '

        # game loop
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                chat.check_mouse_collision(event)

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_RETURN:
                        chat.set_active_status(False)
                        client_msg = chat.get_user_text()
                        chat.set_user_text('')
                    chat.writing(event)

                    if event.key == pygame.K_ESCAPE:
                        running = False
            screen.fill('skyblue')

            # show and send chat message
            if client_msg != '':
                chat.bubble(client_msg, screen.get_size()[0]//2, screen.get_size()[1]//2 - 150)
                full_msg = 'MSG,' + str(self.main_player) + '$' + client_msg
                csocket.send(full_msg.encode())

                # draw other player's messages
                every_message = csocket.recv(1024).decode()
                every_message = every_message.split('$')
                for i in range(0, len(players)):
                    bubble_position = players[i].get_rect_position().split(',')
                    bubble_position = [int(x) for x in bubble_position]
                    chat.bubble(every_message[i], bubble_position[0], bubble_position[1] - 150)

            # move main player and give its position to the server
            players[self.main_player].movement()
            main_player_position = players[self.main_player].get_rect_position()
            main_player_position += "," + str(self.main_player)
            self.csocket.send(main_player_position.encode('utf-8'))

            # get other player's position
            all_player_position_string = self.csocket.recv(1024).decode('utf-8')
            int_player_pos_list = self.server_data_conversion(all_player_position_string)

            # draw other players
            for i in range(0, len(players)):
                players[i].update(int_player_pos_list[i])

            # draw the main player so that camera follows him
            camera_group.custom_draw(players[self.main_player])

            # draw chat
            chat.draw()

            pygame.display.update()
            clock.tick(60)

        pygame.quit()
        sys.exit()

    # from a string to coordinates list:   '100,200,100,200' -> (100,200) , (100,200)
    def server_data_conversion(self, all_player_position_string):
        all_player_position_string = all_player_position_string.split(",")
        all_player_position_list = []
        for i in range(0, len(all_player_position_string), 2):
            all_player_position_string[i] = int(all_player_position_string[i])
            all_player_position_string[i+1] = int(all_player_position_string[i+1])
            all_player_position_list.append((all_player_position_string[i], all_player_position_string[i + 1]))

        return all_player_position_list


if __name__ == '__main__':
    g = Game()
