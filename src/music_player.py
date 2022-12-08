import pygame
from settings import Settings


class MusicPlayer:
    def __init__(self):
        self.currently_playing = None

    def load_play_music(self, music_path):
        if self.currently_playing != music_path:
            self.currently_playing = music_path
            pygame.mixer_music.load(music_path)
            pygame.mixer_music.set_volume(Settings.music_volume/100)
            pygame.mixer_music.play(-1)

    @staticmethod
    def pause():
        pygame.mixer_music.pause()

    @staticmethod
    def resume():
        pygame.mixer_music.play(-1)
