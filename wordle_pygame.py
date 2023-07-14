import random
import pygame
from settings import *
from other import *


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        self.create_word_list()
        self.letters_text = UIElement(170, 70, "Not enough letters", white)

    def create_word_list(self):
        with open('allowed.txt') as file:
            self.words_list = file.read().splitlines()

    def new(self):
        self.word = random.choice(self.words_list).upper()
        self.text =''
        self.current_row = 0
        self.tiles = []
        self.create_tiles()
        self.flip = True
        self.not_enough_letters = False
        self.timer = 0

    def create_tiles(self):
        for row in range(6):
            self.tiles.append([])
            for col in range(5):
                self.tiles[row].append(Tile((col * (tile_size + gap_size)) + x_margin, (row * (tile_size + gap_size)) + y_margin))

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        self.add_letter()

    def add_letter(self):
        for tile in self.tiles[self.current_row]:
            tile.letter = ""

        for i, letter in enumerate(self.text):
            self.tiles[self.current_row][i].letter = letter
            self.tiles[self.current_row][i].create_font()

    def draw_tiles(self):
        for row in self.tiles:
            for tile in row:
                tile.draw(self.screen)

    def draw(self):
        self.screen.fill(bgcolor)
        if self.not_enough_letters:
            self.timer += 1
            self.letters_text.fade_in()
            if self.timer > 90:
                self.not_enough_letters = False
                self.timer = 0
        else:
            self.letters_text.fade_out()
        self.letters_text.draw(self.screen)

        self.draw_tiles()

        pygame.display.flip()

    def row_animation(self):
        self.not_enough_letters = True
        start_pos = self.tiles[0][0].x
        amount_move = 4
        move = 3
        screen_copy = self.screen.copy()
        screen_copy.fill(bgcolor)
        for row in self.tiles:
            for tile in row:
                if row != self.tiles[self.current_row]:
                    tile.draw(screen_copy)

        while True:
            while self.tiles[self.current_row][0].x < start_pos + amount_move:
                self.screen.blit(screen_copy, (0, 0))
                for tile in self.tiles[self.current_row]:
                    tile.x += move
                    tile.draw(self.screen)
                self.clock.tick(FPS)
                pygame.display.flip()

            while self.tiles[self.current_row][0].x > start_pos - amount_move:
                self.screen.blit(screen_copy, (0, 0))
                for tile in self.tiles[self.current_row]:
                    tile.x -= move
                    tile.draw(self.screen)
                self.clock.tick(FPS)
                pygame.display.flip()

            amount_move -= 2
            if amount_move < 0:
                break

    def box_animation(self):
        for tile in self.tiles[self.current_row]:
            if tile.letter == "":
                screen_copy = self.screen.copy()
                for start, end, step in ((0, 6, 1), (0, -6, -1)):
                    for size in range(start, end, 2*step):
                        self.screen.blit(screen_copy, (0, 0))
                        tile.x -= size
                        tile.y -= size
                        tile.width += size * 2
                        tile.height += size * 2
                        surface = pygame.Surface((tile.width, tile.height))
                        surface.fill(bgcolor)
                        self.screen.blit(surface, (tile.x, tile.y))
                        tile.draw(self.screen)
                        pygame.display.flip()
                        self.clock.tick(FPS)
                    self.add_letter()
                break

    def reveal_animation(self, tile, colour):
        screen_copy = self.screen.copy()

        while True:
            surface = pygame.Surface((tile.width + 5, tile.height + 5))
            surface.fill(bgcolor)
            screen_copy.blit(surface, (tile.x, tile.y))
            self.screen.blit(screen_copy, (0, 0))
            if self.flip:
                tile.y += 6
                tile.height -= 12
                tile.font_y += 4
                tile.font_height = max(tile.font_height - 8, 0)
            else:
                tile.colour = colour
                tile.y -= 6
                tile.height += 12
                tile.font_y -= 4
                tile.font_height = min(tile.font_height + 8, tile.font_size)
            if tile.font_height == 0:
                self.flip = False

            tile.draw(self.screen)
            pygame.display.update()
            self.clock.tick(FPS)

            if tile.font_height == tile.font_size:
                self.flip = True
                break

    def check_letters(self):
        copy_word = [x for x in self.word]
        for i, user_letter in enumerate(self.text):
            colour = light_gray
            for j, letter in enumerate(copy_word):
                if user_letter == letter:
                    colour = yellow
                    if i == j:
                        colour = green
                    copy_word[j] = ""
                    break
            self.reveal_animation(self.tiles[self.current_row][i], colour)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit(0)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if len(self.text) == 5:
                        self.check_letters()
                        if self.text == self.word or self.current_row + 1 == 6:
                            if self.text != self.word:
                                self.end_screen_text = UIElement(80, 700, f"Wrong, the answer was : {self.word}", white)
                            else:
                                self.end_screen_text = UIElement(80, 700, "Congratulations! You guessed correct", white)

                            self.playing = False
                            self.end_screen()
                            break

                        self.current_row += 1
                        self.text = ""

                    else:
                        self.row_animation()

                elif event.key == pygame.K_BACKSPACE:
                    if len(self.text)>0:
                        self.text = self.text[:-1]

                else:
                    if len(self.text) < 5 and event.unicode.isalpha():
                        self.text += event.unicode.upper()
                        self.box_animation()

    def end_screen(self):
        play_again = UIElement(80,740, "Press enter to play again!!", white, 30)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit(0)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return

            self.screen.fill(bgcolor)
            self.draw_tiles()
            self.end_screen_text.fade_in()
            self.end_screen_text.draw(self.screen)
            play_again.fade_in()
            play_again.draw(self.screen)
            pygame.display.flip()


game = Game()
while True:
    game.new()
    game.run()