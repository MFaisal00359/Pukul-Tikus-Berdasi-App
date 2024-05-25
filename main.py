import pygame
import random
from pygame.locals import *
import math

# SETTING WINDOW GAME
width, height = 1200, 700
FPS = 60

# SETTING VARIABEL COLOUR/WARNA
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN_BG = (155, 255, 130)

# GRID MOLE HOLE
COL = 3
ROW = 3

print ("Logarithm(1+a) value of 14 is : ", end="")
print (math.log1p(14))

# Class yang merupakan class dasar yang mewakili object dalam game contoh Mole dan Hammer
class GameObject:
    def __init__(self, image_path, scale, hit_delay):
        self.image = pygame.transform.scale(pygame.image.load(image_path), scale)
        self.rect = self.image.get_rect()
        self.hit_image = pygame.transform.scale(pygame.image.load('Images/tikus_kena_hit.png'), scale)
        self.hit_image_rect = self.hit_image.get_rect()
        self.hit_delay = hit_delay
        self.position = 0

    def set_position(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def tampilkan_hit_image(self, screen):
        self.hit_image_rect.midtop = self.rect.midtop
        screen.blit(self.hit_image, self.hit_image_rect)

    def update(self):
        self.rect.y -= 10
        if self.rect.y <= self.position:
            self.rect.y = self.position

    # method draw pada kelas Mole dan Hammer digunakan untuk menggambar objek masing-masing dengan
    # meski implementasinya berbeda.
    def draw(self, screen):
        screen.blit(self.image, self.rect)


# class Mole yang merupakan turunan/pewarisan dari class GameObject
class Mole(GameObject):
    def __init__(self):
        super().__init__('Images/tikus.png', (80, 100), 1000)


# class hammer yang merupakan turunan/pewarisan dari class GameObject
class Hammer(GameObject):
    def __init__(self):
        super().__init__('Images/palu1.png', (160, 160), 1000)
        self.tanah = pygame.transform.scale(pygame.image.load('Images/tanah.png').convert_alpha(), (130, 100))
        self.animasi = [pygame.image.load(f'Images/palu{i}.png').convert_alpha() for i in range(1, 3)]

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()

        self.bg_img = pygame.transform.scale(pygame.image.load('Images/background.png'), (width, height))
        pygame.display.set_caption("Pukul Tikus Berdasi")
        pygame.mouse.set_visible(False)

        self.pop_sfx = pygame.mixer.Sound('Audios/uuh_tikus.mp3')
        pygame.mixer.music.load('Audios/iwanfals_tikus_berdasi.mp3')

        self.tanah_list_rect = []
        self.tanah = None
        self.mole = None
        self.hammer = None

        self._score = 0  # Enkapsulasi score
        self.countdown = 3
        self.last_update = pygame.time.get_ticks()
        self.countdown_finish = 57
        self.last_countdown_finish = pygame.time.get_ticks()

        self.posisi_mouse = (0, 0)
        self.position = 0
        self.start_time = None  # waktu mulai

        self.mole_last_hit = 0  # tikus terkena hit

        self.mole_spawn_delay = random.randint(1000, 3000)
        self.last_mole_spawn = pygame.time.get_ticks()
        self.spawn_speed_increase = 100  # meningkatkan delay tikus
        self.spawn_speed_increase_interval = 15000  # interval delay tikus (15 seconds)

        self.game_over = False

    # fungi start untuk menjalankan game, terdapat 3 call fungsi di dalamnya
    def start(self):
        self.load_assets()
        self.play_background_music()
        self.game_loop()

    # load assets seperti Mole dan Hammer dalam fungsi load assets
    def load_assets(self):
        self.mole = Mole()
        self.hammer = Hammer()

    # method untuk menampilkan tanah dengan col 3, row 3
    def draw_ground(self):
        self.tanah = pygame.transform.scale(pygame.image.load('Images/tanah.png').convert_alpha(), (130, 100))

        # menggambar row dan col tanah
        for row in range(ROW):
            for col in range(COL):
                x = col * 300 + 240
                y = row * 250 + 100
                self.screen.blit(self.tanah, (x, y))
                pygame.draw.rect(self.screen, GREEN_BG, (x, y + 68, 140, 100))
                rect = pygame.Rect(x, y - 53, 50, 100)
                self.tanah_list_rect.append(rect)

    # method untuk membuat random_mole_position
    def random_mole_position(self):
        random_tanah = random.choice(self.tanah_list_rect)
        self.mole.set_position(random_tanah.midbottom[0], random_tanah.midbottom[1] - 10)
        return random_tanah[1] - 10

    # method untuk
    def show_mole_hit(self):
        self.mole.tampilkan_hit_image(self.screen)

    # method untuk menggambar/menulis teks
    # noinspection PyTypeChecker
    def draw_text(self, text, font_size, font_color, x, y):
        font = pygame.font.SysFont(None, font_size)
        font_surface = font.render(text, True, font_color)
        self.screen.blit(font_surface, (x, y))

    def draw_countdown_finish(self):
        now = pygame.time.get_ticks()
        if now - self.last_countdown_finish > 1000:
            self.last_countdown_finish = now
            self.countdown_finish -= 1
        text_countdown_finish = str(self.countdown_finish)
        self.draw_text(f"Time Elapsed : {text_countdown_finish}", 60, WHITE, width // 1.45, 20)

    # method untuk memutar music
    @staticmethod
    def play_background_music():
        pygame.mixer.music.play(-1)

    def game_loop(self):
        running = True
        self.last_mole_spawn = pygame.time.get_ticks()
        self.mole_last_hit = 0

        # selama game berjalan :
        while running:
            self.screen.blit(self.bg_img, (0, 0))
            self.clock.tick(FPS)

            self.posisi_mouse = pygame.mouse.get_pos()
            self.hammer.rect.center = self.posisi_mouse

            for event in pygame.event.get():
                # jika user klik tanda silang windows maka game keluar
                if event.type == QUIT:
                    running = False

                # jika user klik tanda kiri mouse maka game maka akan terjadi event :
                # 1. pop_sfx.play = artinya menjalankan music background
                # 2. score +1 = artinya menambahkan score satire jika terkena hit
                # 3. menampilkan tikus terkena hit
                # 4. position di set ke random
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1 and not self.game_over:
                        if self.mole.rect.collidepoint(self.posisi_mouse):
                            self.pop_sfx.play()
                            self.score += 1  # Update score using the setter method
                            self.show_mole_hit()
                            self.position = self.random_mole_position()
                        else:
                            self.position = self.random_mole_position()
                        self.hammer.image = self.hammer.animasi[1]

                # event setelah mouse di klik maka akan tampil animasi hammer
                if event.type == MOUSEBUTTONUP:
                    if event.button == 1:
                        self.hammer.image = self.hammer.animasi[0]

                if event.type == KEYUP:
                    if event.key == K_r and self.game_over:
                        self._score = 0  # Enkapsulasi score
                        self.countdown = 3
                        self.last_update = pygame.time.get_ticks()
                        self.countdown_finish = 57
                        self.last_countdown_finish = pygame.time.get_ticks()

                        self.posisi_mouse = (0, 0)
                        self.position = 0
                        self.start_time = None  # waktu mulai

                        self.mole_last_hit = 0  # tikus terkena hit

                        self.mole_spawn_delay = random.randint(1000, 3000)
                        self.last_mole_spawn = pygame.time.get_ticks()
                        self.spawn_speed_increase = 100  # meningkatkan delay tikus
                        self.spawn_speed_increase_interval = 15000  # interval delay tikus (15 seconds)

                        self.game_over = False

            # set time dari pygame ke now
            now = pygame.time.get_ticks()
            if now - self.last_update > 1000 and self.countdown > 0:
                self.last_update = now
                self.countdown -= 1
                self.position = self.random_mole_position()

            if now - self.last_mole_spawn > self.mole_spawn_delay:
                self.position = self.random_mole_position()
                self.mole_spawn_delay = random.randint(1000, 3000)
                self.last_mole_spawn = now

            if now - self.mole_last_hit > self.mole.hit_delay:
                self.mole.update()
                if self.mole.rect.y <= self.position:
                    self.mole.rect.y = self.position

            if self.countdown > 0:
                pygame.mixer.music.load('Audios/iwanfals_tikus_berdasi.mp3')
                pygame.mixer.music.set_volume(0.2)
                pygame.mixer.music.play()
                self.draw_text(str(self.countdown), 60, WHITE, width // 2, height // 2 - 50)
            else:
                if self.start_time is None:
                    self.start_time = pygame.time.get_ticks()
                if not self.game_over:
                    self.draw_countdown_finish()
                    self.mole.draw(self.screen)
                    self.draw_text(f"Score: {self.score}", 60, WHITE, 80, 20)
                    # elapsed_time = (pygame.time.get_ticks() - self.start_time) // 1000
                    # self.draw_text(f"Time: {elapsed_time}s", 60, WHITE, width // 1.2, 20)

            self.draw_ground()

            if self.countdown_finish < 0:
                self.game_over = True
                self.draw_text("Game Over", 120, WHITE, width // 2 - 225, height // 2 - 140)
                self.draw_text(f"Score Anda : {self.score}", 60, WHITE, width // 2 - 152, height // 2 - 50)
                self.draw_text("Tekan 'R' untuk restart game", 60, WHITE, width // 2 - 292, height // 2 + 180)

            self.hammer.draw(self.screen)

            pygame.display.update()

        pygame.quit()

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, value):
        self._score = value


# Menjalankan permainan
game = Game()
game.start()
