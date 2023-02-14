import pygame
import sys

#user class
from const import *
from game import *
from dragger import *
from square import *
from board import *
class Main:
    def __init__(self):

        pygame.init()#this method is called first 
        self.screen=pygame.display.set_mode( (width,height) ) # any variable in init is defined using keyword self
        pygame.display.set_caption("Chess")
        self.game=game()

    def mainloop(self):
        game=self.game
        screen=self.screen
        board=self.game.board
        dragger=self.game.dragger

        while True: #no nedd to use bracket in.py use indentation carefully
            game.bg_color(screen)
            game.show_last_move(screen )
            game.show_moves(screen)
            game.show_piece(screen)
            game.show_hover(screen)

            if dragger.dragging:
                dragger.update_blit(screen)

            for event in pygame.event.get():#to check mouse event
                
                #clicking of pieces
                if event.type==pygame.MOUSEBUTTONDOWN:
                    dragger.updatemouse(event.pos)
 
                    clicked_row=dragger.mouseY//sqsize
                    clicked_col=dragger.mouseX//sqsize

                    if board.squares[clicked_row][clicked_col].has_piece():
                        piece=board.squares[clicked_row][clicked_col].piece

                        if piece.color==game.next_player:
                            board.calc_moves(piece,clicked_row,clicked_col,bool=True)
                            dragger.save_initial(event.pos)
                            dragger.drag_piece(piece)
                            game.bg_color(screen)
                            game.show_last_move(screen )
                            game.show_moves(screen)
                            game.show_piece(screen)

                #moving of dragger
                elif event.type==pygame.MOUSEMOTION:
                    motion_row=event.pos[1]//sqsize
                    motion_col=event.pos[0]//sqsize
                    game.set_hover(motion_row,motion_col)

                    if dragger.dragging:
                        dragger.updatemouse(event.pos)
                        game.bg_color(screen) 
                        game.show_last_move(screen )
                        game.show_moves(screen)
                        game.show_piece(screen)
                        game.show_hover(screen)
                        dragger.update_blit(screen)

                #release of click
                elif event.type==pygame.MOUSEBUTTONUP:

                    if dragger.dragging:
                        dragger.updatemouse(event.pos)

                        released_row=dragger.mouseY//sqsize
                        released_col=dragger.mouseX//sqsize

                        initial=square(dragger.initial_row,dragger.initial_col)
                        final=square(released_row,released_col)
                        move_=move(initial,final)


                        if board.valid_move(dragger.piece,move_):
                            captured=board.squares[released_row][released_col].has_piece()
                            board.move(dragger.piece,move_)
                            board.only_for_one_move(dragger.piece)
                            game.sound_effect(captured)
                            game.bg_color(screen)    
                            game.show_last_move(screen )
                            game.show_piece(screen)
                            game.next_turn( ) 

                    dragger.undrag_piece()

                #keypress
                elif event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_t:
                        game.change_theme()

                    if event.key==pygame.K_r:
                        game.reset()
                        game=self.game
                        board=self.game.board   
                        dragger=self.game.dragger


                #quit
                elif event.type==pygame.QUIT:
                    pygame.quit()
                    sys.exit

            pygame.display.update()
main=Main() 
main.Main=main.mainloop()