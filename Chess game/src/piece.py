import os


class piece:
    def  __init__(self,name,color,value,texture=None,texture_rect=None):
        self.name=name
        self.color=color
        value_sign=1 if color=='white' else -1
        self.value=value*value_sign

        self.moves=[]
        self.moved=False

        
        self.texture=texture
        self.set_texture()
        self.texture_rect=texture_rect


    def set_texture(self,size=80):
        self.texture=os.path.join(f'assets/images/imgs-{size}px/{self.color}_{self.name}.png')#acccesing image in assets folder

    def add_move(self,move):
        self.moves.append(move)   

    def clearmoves(self):
        self.moves=[]

class pawn(piece):
    def __init__(self,color):# pawns move only in one direction
        if(color=='white'):
            self.dir=-1#white pwn move upward
        else:
            self.dir=1
        self.en_passant=False
        super().__init__('pawn',color,1.0)#super means the parent class


class knight(piece):
    def __init__(self,color):
        super().__init__('knight',color,3.0)

        
class bishop(piece):
    def __init__(self,color):
        super().__init__('bishop',color,3.0)

        
class rook(piece):
    def __init__(self,color):
        super().__init__('rook',color,5.0)

        
class queen(piece):
    def __init__(self,color):
        super().__init__('queen',color,9.0)

class king(piece):
    def __init__(self,color):
        self.left_rook=None
        self.right_rook=None

        super().__init__('king',color,10000.0)