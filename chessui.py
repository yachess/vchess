import tkinter as tk
from PIL import Image, ImageEnhance, ImageTk
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
            self.create_rectangle(
                    x, y, x+cs, y+cs, width=0, 
                    fill= "green" if (i+j)%2 == 1 else "light green")
#       self.create_image(cs/2, cs/2, image=pieces['P'], anchor="center")
        self.bind("<Button-1>",self._handle_click)
        self.bind("<MouseWheel>",self._wheel)
        self.pack()

        self.selected_sqrs = []
        self.selected_squares_objs = []

        self._fire_action = None

    def setup (self, fen):
        tokens = fen.split()[0]
        sq=0
        for c in tokens:
            if c.isalpha():
                x, y = sq%8, sq//8
                self.pieces[sq]=self.create_image(
                        x*cs+cs/2, y*cs+cs/2, image=pieces[c],
                        anchor="center")
                sq+=1
            elif c.isdigit():
                sq+=int(c)
    
    def _handle_click(self, evt):
        x, y = evt.x // cs, evt.y // cs
        sq = y*8 + x

        if len(self.selected_sqrs) < 2:
            self.selected_sqrs.append(sq)
            self.select_square(sq)
            if len(self.selected_sqrs) >= 2:
                if self._fire_action is not None:
                    self._fire_action("<<request_move>>", self.selected_sqrs)
                for o in self.selected_squares_objs:
                    self.delete(o)
                self.selected_squares_objs = []
                self.selected_sqrs = []


    def _wheel(self, evt):
        print("wheel:{}".format(evt))

    def set (self, pc, sq):
        x, y = sq%8, sq//8
        self.pieces[sq]=self.create_image(
                x*cs+cs/2, y*cs+cs/2,
                image=pieces[pc], anchor="center")
    
    def remove (self, sq):
        try:
            self.delete(self.pieces[sq])
            del self.pieces[sq]
        except KeyError:
            pass

    def select_square (self, sq):
        x, y = sq%8, sq//8
        i=self.create_rectangle(
                x*cs, y*cs,(x+1)*cs-1,(y+1)*cs-1,
                outline = "red" )
        self.selected_squares_objs.append(i)
    

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.chessboard = None
        self.chess =None
        self.create_widgets()

    def create_widgets(self):
        self.chessboard = ChessBoard(self)
        self.chess = chess.Chess()
        self.chess._fire_action = self._handle_action
        self.chessboard._fire_action = self._handle_action
        self.chess.setup() 

        self.hi_there = tk.Button(self)
        self.hi_there["text"] = "Hello World\n(click me)"
        self.hi_there.pack(side="top")
        self.quit = tk.Button(
                self, text="QUIT", fg="red",
                command=self.master.destroy)
        self.quit.pack(side="bottom")

    def _handle_action(self, action, args):
        if action == "<<setup>>":
            self.chessboard.setup(args)
        elif action == "<<move>>":
            print(" ### Move ### {} -> {}".format(args["src"],args["dst"]))
            self.chessboard.remove(args["src"])
            self.chessboard.set(args["piece"], args["dst"])
            print("<<move>>")
        elif action == "<<remove>>":
            print("<<remove>>")
        elif action == "<<request_move>>":
            if self.chess.make(args[0],args[1]):
                pass
            else:
                print("illegal move:{}->{}".format(args[0],args[1]))


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

root = tk.Tk()
pieces={}
for a in "PRNBQK":
#   pieces[a] = tk.PhotoImage(file = "data/PIECE/Dyche/{}.png".format(a))
    img = resize_image(Image.open("data/PIECE/Dyche/{}.png".format(a)), cs, cs)
    pieces[a] = ImageTk.PhotoImage(img)
    pieces[a.lower()] = ImageTk.PhotoImage(darker_image(img, 0.5))

app = Application(master=root)
app.mainloop()

