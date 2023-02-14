from color import *


class theme:

    def __init__(self,ligth_bg,dark_bg,ligth_trace,dark_trace,ligth_moves,drak_moves):
        self.bg=color(ligth_bg,dark_bg)
        self.trace=color(ligth_trace,dark_trace)
        self.moves=color(ligth_moves,drak_moves)
        