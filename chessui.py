
import tkinter as tk
import chess

class ChessBoard(tk.Canvas):

    def __init__(self, master = None):
        super().__init__(master,width = 64*8, height = 64*8)
        self.master = master
        
        for sq in range(64):
            i,j = sq % 8, sq // 8
            x,y = i * 64, j * 64
            self.create_rectangle(
                    x, y, x+64, y+64, width=0, 
                    fill= "green" if (i+j)%2 == 1 else "light green")
        self.create_image(32, 32, image=pieces['P'], anchor="center")
        self.pack()

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.chessboard = ChessBoard(self)
        self.chess = chess.Chess(self)
        self.chess._fire_action= self._action
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

    def _action(self, action, args):
        if action == "<<move>>":
            pass
        elif action == "<<move>>":
            print("<<move>>")
            pass
        elif action == "<<remove>>":
            print("<<remove>>")
            pass
        pass
root = tk.Tk()
pieces={}
for a in "PRNBQK":
    pieces[a] = tk.PhotoImage(file = "data/PIECE/Mono/{}.png".format(a))
app = Application(master=root)
app.mainloop()

