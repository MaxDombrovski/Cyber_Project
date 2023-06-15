import pygame
import sys
from PIL import Image
import tcp_by_size
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
    def __init__(self, start_position, group, number):
        super().__init__(group)
        self.display_surface = pygame.display.get_surface()
        #player's number
        self.number = number
        # player position
        self.x = start_position[0]
        self.y = start_position[1]
        # images for the player
        self.combine_images()
        self.rect = self.image.get_rect(center=start_position)
        # chat interactions
        self.chat = Chat()
        self.bubble_font = pygame.font.SysFont('Comic Sans MS', 48)
        self.name_font = pygame.font.SysFont('Candara Bold Italic', 48)

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

    def update(self, update_position, name="", text="", camerax=0, cameray=0):
        self.rect.center = update_position
        bubble_surface = self.bubble_font.render(text, True, (0, 0, 0))
        self.display_surface.blit(bubble_surface, (update_position[0] - camerax - bubble_surface.get_width()//2, update_position[1] - 150 - cameray))

        name_surface = self.name_font.render(name, True, (255, 255, 255))
        name_surface_outline = self.name_font.render(name, True, (0, 0, 0))

        self.display_surface.blit(name_surface_outline, (update_position[0] - camerax - name_surface_outline.get_width() // 2 + 2, update_position[1] + 152 - cameray))
        self.display_surface.blit(name_surface_outline, (update_position[0] - camerax - name_surface_outline.get_width() // 2 - 2, update_position[1] + 152 - cameray))
        self.display_surface.blit(name_surface_outline, (update_position[0] - camerax - name_surface_outline.get_width() // 2 + 2, update_position[1] + 148 - cameray))
        self.display_surface.blit(name_surface_outline, (update_position[0] - camerax - name_surface_outline.get_width() // 2 - 2, update_position[1] + 148 - cameray))
        self.display_surface.blit(name_surface, (update_position[0] - camerax - name_surface.get_width()//2, update_position[1] + 150 - cameray))


    def combine_images(self, appearance_list=["", "TopHat", "Suit", "Shorts", "Crocs"]):
        images = []
        images.append(Image.open("FrontEnd/player_assets/body.png"))
        images.append(Image.open(f"FrontEnd/player_assets/{appearance_list[1]}Small.png"))
        images.append(Image.open(f"FrontEnd/player_assets/{appearance_list[2]}Small.png"))
        images.append(Image.open(f"FrontEnd/player_assets/{appearance_list[3]}Small.png"))
        images.append(Image.open(f"FrontEnd/player_assets/{appearance_list[4]}Small.png"))

        new_image = Image.new("RGBA", (100, 270))

        for i in range(len(images)):
            new_image = Image.alpha_composite(new_image, images[i])

        new_image.save(f"FrontEnd/player_assets/full_body{self.number}.png", format="png")
        self.image = pygame.image.load(f"FrontEnd/player_assets/full_body{self.number}.png").convert_alpha()


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

    def __init__(self, csocket=None):
        self.csocket = csocket
        # self.main_player = int(self.csocket.recv(1024).decode('utf-8'))
        self.main_player = int(tcp_by_size.recv_by_size(self.csocket))

        # set up the screen
        pygame.init()
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption('lobby')
        clock = pygame.time.Clock()
        pygame.time.set_timer(pygame.USEREVENT, 1000)
        pygame.event.set_grab(True)

        # preposition all the possible players
        camera_group = CameraGroup()
        players = []
        for i in range(10):
            players.append(Player((480, 360), camera_group, i))
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
        client_msg = ''

        # game loop
        running = True
        while running:
            # move main player and give its position and its message to the server
            players[self.main_player].movement()
            main_player_position = players[self.main_player].get_rect_position()
            main_player_position_and_message = main_player_position + "$" + str(self.main_player) + "$" + client_msg
            # self.csocket.send(main_player_position_and_message.encode('utf-8'))
            tcp_by_size.send_with_size(self.csocket, main_player_position_and_message)

            # get other player's position
            # server_data = self.csocket.recv(1024).decode('utf-8')
            server_data = tcp_by_size.recv_by_size(self.csocket)
            server_data = server_data.split("$")
            appearance_list = server_data[:10]
            message_list = server_data[10:-10]
            position_list = server_data[-10:]

            position_list = self.string_list_to_tuple_list_convertion(position_list)
            print(message_list)
            print(position_list)

            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                chat.check_mouse_collision(event)

                if event.type == pygame.USEREVENT:
                    print("\n", appearance_list, "\n")
                    for i in range(10):
                        players[i].combine_images(appearance_list[i].split(","))

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_RETURN:
                        chat.set_active_status(False)
                        client_msg = chat.get_user_text()
                        chat.set_user_text('')
                    chat.writing(event)

                    if event.key == pygame.K_ESCAPE:
                        running = False

            screen.fill('skyblue')

            # draw the main player so that camera follows him
            camera_group.custom_draw(players[self.main_player])
            offsetx = players[self.main_player].rect.centerx - screen.get_size()[0] // 2
            offsety = players[self.main_player].rect.centery - screen.get_size()[1] // 2

            # draw other players
            for i in range(0, len(players)):
                players[i].update(position_list[i], appearance_list[i].split(",")[0], message_list[i], offsetx, offsety)

            # draw chat
            chat.draw()

            pygame.display.update()
            clock.tick(60)

        pygame.quit()
        sys.exit()

    # conversion from a string list to a tuple
    def string_list_to_tuple_list_convertion(self, position_list):
        for i in range(len(position_list)):
            position_list[i] = eval(position_list[i])

        return position_list


if __name__ == '__main__':
    g = Game()
