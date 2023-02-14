from const import *
from square import square
from piece import *
from move import *
from dragger import *
from sound import sound
import os
import copy


class board:
    def __init__(self):
        self.c=0
        self.squares=[[0,0,0,0,0,0,0,0] for col in range(cols)]
        self.last_move=None
        self._create()
        self._add_pieces('white')
        self._add_pieces('black')

    def move(self,piece,move,sound_test=False):
        
        initial=move.initial
        final=move.final

        en_empty=self.squares[final.row][final.col].isempty()

        self.squares[initial.row][initial.col].piece=None
        self.squares[final.row][final.col].piece=piece

        

        #pawn promotion and en passant
        if isinstance(piece,pawn):
            diff=final.col-initial.col
            if  diff!=0 and en_empty:
                
                self.squares[initial.row][initial.col+diff].piece=None
                self.squares[final.row][final.col].piece=piece
                if not sound_test:
                    sound_=sound (os.path.join('assets/sounds/capture.wav'))
                    sound_.play()
            else:
                self.check_promotion(piece,final)

        

        if isinstance(piece,king):
            if self.castling(initial,final) and not sound_test:
                diff=final.col-initial.col
                rook=piece.left_rook if (diff<0) else piece.right_rook    
                self.move(rook, rook.moves[-1])

        piece.moved=True
        piece.clearmoves()

        self.last_move=move

    def only_for_one_move(self,piece):# en passant is valid for only one move
        
        if not isinstance(piece,pawn):
            return
        for row in range(rows):
            for col in range(cols):
                if isinstance(self.squares[row][col].piece,pawn):    
                    self.squares[row][col].piece.en_passant=False
        piece.en_passant=True


    

    def valid_move(self,piece,move):
        return move in piece.moves
    
    def check_promotion(self,piece,final):
        if final.row==0 or final.row==7:
            self.squares[final.row][final.col].piece=queen(piece.color)
        
        # p44=self.squares[4][4].piece
        # p43=self.squares[4][3].piece
        # p42=self.squares[4][2].piece
        # p41=self.squares[4][1].piece
        # if final.row==0 or final.row==7:
        #     self.squares[4][4].piece=knight(piece.color)
        #     self.squares[4][3].piece=queen(piece.color)
        #     self.squares[4][2].piece=bishop(piece.color)
        #     self.squares[4][1].piece=rook(piece.color)

            

        #     if pygame.event.get()==pygame.MOUSEBUTTONDOWN:
        #         dragger.updatemouse(pygame.event.get().pos)
 
        #         clicked_row=dragger.mouseY//sqsize
        #         clicked_col=dragger.mouseX//sqsize

        #         if clicked_col==4:
        #             self.squares[final.row][final.col]=knight(piece.color)

        #         elif clicked_col==3:
        #             self.squares[final.row][final.col]=queen(piece.color)

        #         elif clicked_col==2:
        #             self.squares[final.row][final.col]=bishop(piece.color)

        #         elif clicked_col==1:
        #             self.squares[final.row][final.col]=rook(piece.color)
        #         self.squares[4][4].piece=p44
        #         self.squares[4][3].piece=p43
        #         self.squares[4][2].piece=p42
        #         self.squares[4][1].piece=p41
                
    def castling(self,initial,final):
        return abs(initial.col-final.col)==2
    

    def in_check(self,piece,move):
        temp_piece=copy.deepcopy(piece)
        temp_board=copy.deepcopy(self)
        temp_board.move(temp_piece,move,sound_test=True)

        for row in range(rows):
            for col in range(cols):
                if temp_board.squares[row][col].has_rival_piece(piece.color):
                    p=temp_board.squares[row][col].piece
                    #checking illegal moves i.e moving a piece results in check
                    temp_board.calc_moves(p,row,col,bool=False)
                    for m in p.moves:
                        if isinstance(m.final.piece,king):
                            return True
        return False



    def calc_moves(self,piece,row,col,bool=True):

        def king_moves():
            adjs=[
                (row-1,col+0),
                (row-1,col-1),
                (row-1,col+1),
                (row+0,col+1),
                (row+0,col-1),
                (row+1,col+0),
                (row+1,col+1),
                (row+1,col-1)

            ]

            for possible_move in adjs:
                possible_row,possible_col=possible_move

                if square.in_range(possible_row,possible_col):
                    if self.squares[possible_row][possible_col].isempty_or_rival(piece.color):
                        initial=square(row,col)
                        final=square(possible_row,possible_col)
                        move_ = move(initial,final)
                        if bool:
                            if not self.in_check(piece,move_):
                                piece.add_move(move_)
                            else:break
                        else:
                            piece.add_move(move_)

            if not piece.moved:
                #queenside castling
                left_rook=self.squares[row][0].piece
                if isinstance(left_rook,rook):
                    if not left_rook.moved:
                        for c in range(1,4):
                            if self.squares[row][c].has_piece():
                                break
                        if c==3:
                            piece.left_rook=left_rook

                            initial=square(row,0)
                            final=square(row,3)
                            move_R = move(initial,final)
                            

                            initial=square(row,col)
                            final=square(row,2)
                            move_K = move(initial,final)


                            if bool:
                                 if not self.in_check(piece,move_K) and not self.in_check(piece,move_R):
                                     left_rook.add_move(move_R)
                                     piece.add_move(move_K)
                            else:
                                 left_rook.add_move(move_R)
                                 piece.add_move(move_K)
                #king side castling
                right_rook=self.squares[row][7].piece
                if isinstance(right_rook,rook):
                    if not right_rook.moved:
                        for c in range(6,8):
                            if self.squares[row][c].has_piece():
                                break
                        if c==7:
                            piece.right_rook=right_rook

                            initial=square(row,7)
                            final=square(row,5)
                            move_R = move(initial,final)
                            
                            initial=square(row,col)
                            final=square(row,6)
                            move_K = move(initial,final)


                            if bool:
                                 if not self.in_check(piece,move_K) and not self.in_check(piece,move_R):
                                    right_rook.add_move(move_R)
                                    piece.add_move(move_K)
                            else:
                                right_rook.add_move(move_R)
                                piece.add_move(move_K)


                        pass
                pass

        def straightline_moves(incrs):
            for incr in incrs:
                row_incr,col_incr=incr
                possible_move_row=row+row_incr
                possible_move_col=col+col_incr



                while True:
                    if square.in_range(possible_move_row,possible_move_col):

                        initial=square(row,col)
                        final_piece=self.squares[possible_move_row][possible_move_col].piece
                        final=square(possible_move_row,possible_move_col,final_piece)

                        move_=move(initial,final)

                        if self.squares[possible_move_row][possible_move_col].isempty():
                            if bool:
                             if not self.in_check(piece,move_):
                                piece.add_move(move_)
                             else:break
                            else:
                                piece.add_move(move_)

                        elif self.squares[possible_move_row][possible_move_col].has_rival_piece(piece.color):
                            if bool:
                             if not self.in_check(piece,move_):
                                piece.add_move(move_)
                             else:break
                            else:
                                piece.add_move(move_)
                            break

                        elif self.squares[possible_move_row][possible_move_col].has_team_piece(piece.color):
                            break

                    else:
                         break

                    possible_move_row=possible_move_row+row_incr
                    possible_move_col=possible_move_col+col_incr



        def pawn_moves():
            steps = 1 if piece.moved else 2

            #vertical moves
            start= row+piece.dir
            end=row+(piece.dir*(1+steps))
            for possible_move_row in range(start,end,piece.dir):
                if square.in_range(possible_move_row):
                    if self.squares[possible_move_row][col].isempty():
                        initial =square(row,col)
                        final =square(possible_move_row,col)
                        move_=move(initial,final)

                        if bool:
                            if not self.in_check(piece,move_):
                                piece.add_move(move_)
                        else:
                            piece.add_move(move_)
                    else:
                        break
                else:
                    break

            #diagonal moves
            possible_move_row=row+piece.dir
            possible_move_cols=[col-1,col+1]
            for possible_move_col in possible_move_cols:
                if square.in_range(possible_move_row,possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].has_rival_piece(piece.color):
                        initial=square(row,col)
                        final_piece=self.squares[possible_move_row][possible_move_col].piece
                        final=square(possible_move_row,possible_move_col,final_piece)
                        move_=move(initial,final)
                        if bool:
                            if not self.in_check(piece,move_):
                                piece.add_move(move_)
                        else:
                            piece.add_move(move_)

            #en passant moves
            r=3 if piece.color=='white' else 4
            final_r=2 if piece.color=='white' else 5
            #left side
            if square.in_range(col-1) and row==r:
                self.c=0
                if self.squares[row][col-1].has_rival_piece(piece.color):
                    p=self.squares[row][col-1].piece
                    if isinstance(p,pawn):
                        if p.en_passant:
                            initial=square(row,col)
                            final=square(final_r,col-1,p)
                            move_=move(initial,final)
                            if bool:
                                if not self.in_check(piece,move_):
                                    piece.add_move(move_)
                            else:
                                piece.add_move(move_)
            #right side
            if square.in_range(col+1) and row==r:
                self.c=0
               
                if self.squares[row][col+1].has_rival_piece(piece.color):
                    p=self.squares[row][col+1].piece
                    if isinstance(p,pawn):
                        if p.en_passant:
                            initial=square(row,col)
                            final=square(final_r,col+1,p)
                            move_=move(initial,final)
                            if bool:
                                if not self.in_check(piece,move_):
                                    piece.add_move(move_)
                            else:
                                piece.add_move(move_)


        def knight_moves():
            possible_moves=[
                (row-2,col+1),
                (row-1,col+2),
                (row+1,col+2),
                (row+2,col+1),
                (row+2,col-1),
                (row+1,col-2),
                (row-1,col-2),
                (row-2,col-1)
            ]
            for possible_move in possible_moves:
                possible_row,possible_col=possible_move

                if square.in_range(possible_row,possible_col):
                    if self.squares[possible_row][possible_col].isempty_or_rival(piece.color):
                        initial=square(row,col)
                        final_piece=self.squares[possible_row][possible_col].piece
                        final=square(possible_row,possible_col,final_piece)
                        move_ = move(initial,final)
                        if bool:
                            if not self.in_check(piece,move_):
                                piece.add_move(move_)
                            else:break
                        else:
                            piece.add_move(move_)
            


        if isinstance(piece,pawn):
            pawn_moves()

        elif isinstance(piece,knight):
            knight_moves()

        elif isinstance(piece,bishop):
            straightline_moves([
                (-1,1),#upright
                (-1,-1),#upleft
                (1,1),#downright
                (1,-1)#downleft
            
            ])

        elif isinstance(piece,rook): 
            straightline_moves([
                (-1,0),
                (0,1),
                (1,0),
                (0,-1)
            ])

        elif isinstance(piece,queen):
            straightline_moves([
                (-1,1),
                (-1,-1),
                (1,1),
                (1,-1),
                (-1,0),
                (0,1),
                (1,0),
                (0,-1)
            ])

           

        elif isinstance(piece,king):
            king_moves()

        

    def _create(self): #_ before method name shows that they are private
        
        for row in range(rows):
            for col in range(cols):
                self.squares[row][col]=square(row,col)

      
    def _add_pieces(self,color):
        
        row_pawn,row_other= (6,7) if color=='white' else (1,0)
        #Pawns
        for col in range(cols):
            self.squares[row_pawn][col]=square(row_pawn,col,pawn(color))
       
        #knigths
        self.squares[row_other][1]=square(row_other,1,knight(color))
        self.squares[row_other][6]=square(row_other,6,knight(color))  

        #Bishops
        self.squares[row_other][2]=square(row_other,2,bishop(color))
        self.squares[row_other][5]=square(row_other,5,bishop(color))
        

        #Rook
        self.squares[row_other][0]=square(row_other,0,rook(color)) 
        self.squares[row_other][7]=square(row_other,7,rook(color))


        #queen
        self.squares[row_other][3]=square(row_other,3,queen(color))

        #king
        self.squares[row_other][4]=square(row_other,4,king(color))
        