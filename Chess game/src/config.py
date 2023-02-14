import pygame
import os
from sound import sound
from theme import theme


class config:

    def __init__(self):
        self.themes=[]
        self._add_themes()
        self.idx=0
        self.theme=self.themes[self.idx]
        self.font=pygame.font.SysFont('monospace',12,True)
        self.move_sound=sound(
            os.path.join('assets/sounds/move.wav')
        )
        self.capture_sound=sound(
            os.path.join('assets/sounds/capture.wav')
        )

    def change_theme(self):
        self.idx+=1
        self.idx%=len(self.themes)
        self.theme=self.themes[self.idx]


    def _add_themes(self):
        green=theme((234,235,200),(119,154,88),(244,247,116),(172,195,51),'#c86464','#c84646')
        black=theme((255,255,255),(0,0,0),(244,247,116),(172,195,51),'#c86464','#c84646')
        blue=theme((229,220,200),(60,95,135),(123,90,227),(43,190,191),'#c86464','#c84646')
        red=theme((255,0,0),(255,255,0),(244,247,116),(172,195,51),'#c86464','#c84646')

        self.themes=[green,black,blue,red]

