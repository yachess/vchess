import tkinter as tk
import chess

cs = 80
class ChessBoard(tk.Canvas):

    def __init__(self, master = None):
        super().__init__(master,width = cs*8, height = cs*8)
        self.master = master
        self.pieces = {}        
        for sq in range(64):
            i,j = sq % 8, sq // 8
            x,y = i * cs, j * cs
            =self.create_rectangle(
                    x, y, x+cs, y+cs, width=0, 
                    fill= "green" if (i+j)%2 == 1 else "light green")
#       self.create_image(cs/2, cs/2, image=pieces['P'], anchor="center")
        self.pack()

    def setup (self, fen):
        tokens = fen.split()[0]
        i=0
        for c in tokens:
            if c.isalpha():
                x, y = i%8, i//8
                self.pieces[i]=self.create_image(x*cs+cs/2, y*cs+cs/2, image=pieces[c],
                anchor="center")
                i+=1
            elif c.isdigit():
                i+=int(c)

    def set (self, pc, sq):
        x, y = sq%8, sq//8
        self.pieces[i]=self.create_image(x*cs+cs/2, y*cs+cs/2,
                image=pieces[pc], anchor="center")
    
    def remove (self, sq):
        i = sq // 8 + sq % 8
        self.remove(self.pieces[i])
        del self.pieces[i]

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.chessboard = ChessBoard(self)
        self.chess = chess.Chess()
        self.chess._fire_action = self._handle_action
        self.chess.setup() 

        self.hi_there = tk.Button(self)
        self.hi_there["text"] = "Hello World\n(click me)"
        self.hi_there["command"] = self.say_hi
        self.hi_there.pack(side="top")
        self.quit = tk.Button(
                self, text="QUIT", fg="red",
                command=self.master.destroy)
        self.quit.pack(side="bottom")

    def say_hi(self):
        print("hi there, everyone!")

    def _handle_action(self, action, args):
        print(action)
        if action == "<<setup>>":
            self.chessboard.setup(args)
            pass
        elif action == "<<move>>":
            pass
        elif action == "<<move>>":
            print("<<move>>")
            pass
        elif action == "<<remove>>":
            print("<<remove>>")
            pass
        pass


from PIL import Image, ImageEnhance, ImageTk



def resize_image(img, w, h):
    img2 = img.resize((w,h), Image.ANTIALIAS)
    return img2

def darker_image(img, ratio):
    pxls = img.load()
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            alpha = ratio   # 0..1 :  0 is darkest
            beta = -30
            pxls[i,j] = (
                    int(pxls[i,j][0] * alpha + beta),
                    int(pxls[i,j][1] * alpha + beta),
                    int(pxls[i,j][2] * alpha + beta),
                    pxls[i,j][3])
    return img
import PIL
from PIL import Image

root = tk.Tk()
pieces={}
for a in "PRNBQK":
#   pieces[a] = tk.PhotoImage(file = "data/PIECE/Dyche/{}.png".format(a))
    img = resize_image(Image.open("data/PIECE/Dyche/{}.png".format(a)), cs, cs)
    pieces[a] = ImageTk.PhotoImage(img)
    pieces[a.lower()] = ImageTk.PhotoImage(darker_image(img, 0.5))

app = Application(master=root)
app.mainloop()

