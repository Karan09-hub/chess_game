import pygame


from const import *
from board import*
from dragger import *
from piece import *
from config import *
from square import *


class game:
    def __init__(self):
        self.next_player='white'
        self.hovered_square=None
        self.board=board()
        self.dragger=dragger()
        self.config=config()



    #show surface


    def bg_color(self,surface):

        theme=self.config.theme

        
        
        for row in range(rows):
            for col in range(cols):
                color=theme.bg.ligth if(row+col)%2==0 else theme.bg.dark
                rect=(col*sqsize,row*sqsize,sqsize,sqsize)
                
                pygame.draw.rect(surface,color,rect)

                if col==0:
                    color=theme.bg.dark if row%2==0 else theme.bg.ligth
                    lbl=self.config.font.render(str(rows-row),1,color)
                    lbl_pos=(5,5+row*sqsize)
                    surface.blit(lbl,lbl_pos)

                if row==7:
                    color=theme.bg.dark if (row+col)%2==0 else theme.bg.ligth
                    lbl=self.config.font.render(square.get_alphacols(col),1,color)
                    lbl_pos=(col*sqsize+sqsize-10,height-10)
                    surface.blit(lbl,lbl_pos)
                
                    
    def show_piece(self,surface):

        #piece exists?
        for row in range(rows):
            for col in range(cols):
                if self.board.squares[row][col].has_piece():
                    piece=self.board.squares[row][col].piece

                    
                    if piece is not self.dragger.piece:
                        piece.set_texture(size=80)
                        img=pygame.image.load(piece.texture)
                        img_center=col*sqsize+sqsize//2,row*sqsize+sqsize//2 #centering img
                        piece.texture_rect=img.get_rect(center=img_center)
                        surface.blit(img,piece.texture_rect)#blit will put img in texture_rect that is already centered


    def show_moves(self,surface):
        theme=self.config.theme
        if self.dragger.dragging:
            piece=self.dragger.piece

            for move in piece.moves:
                color=theme.moves.ligth if (move.final.row+move.final.col)%2==0 else theme.moves.dark
                rect=(move.final.col*sqsize,move.final.row*sqsize,sqsize,sqsize)
                pygame.draw.rect(surface,color,rect)

    def show_hover(self,surface):
        if self.hovered_square:
            color=(180,180,180)
            rect=(self.hovered_square.col*sqsize,self.hovered_square.row*sqsize,sqsize,sqsize)
            pygame.draw.rect( surface ,color,rect,width=3)

        pass


    def set_hover(self,row,col):
        self.hovered_square=self.board.squares[row][col]
        


    def show_last_move(self,surface):
        theme=self.config.theme
        if self.board.last_move:
            initial=self.board.last_move.initial
            final=self.board.last_move.final

            for pos in [initial,final]:

                color=theme.trace.ligth if (pos.row+pos.col)%2==0 else theme.trace.dark
                rect=(pos.col*sqsize,pos.row*sqsize,sqsize,sqsize)
                pygame.draw.rect( surface ,color,rect)
                



    def next_turn(self):
        self.next_player='white' if self.next_player=='black' else 'black'

    def change_theme(self):
        self.config.change_theme()

    def sound_effect(self,captured=False):
        if captured:
            self.config.capture_sound.play()
        else:
            self.config.move_sound.play()
    
    
    def reset(self):
        self.__init__()
