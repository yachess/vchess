import copy

init_pos = "rnbqkbnrpppppppp................................PPPPPPPPRNBQKBNR"
init_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

q_atks=[]
b_atks=[]
r_atks=[]
n_atks=[]
k_atks=[]
bp_atks=[]
wp_atks=[]

rays = []           # Three dimensional lists of directional rays.
for sq in range(64):
	rays.append([
		[i for i in range(sq+1, 64, +1) if sq/8 == i/8 and i < 64], 
		[i for i in range(sq+9, 64, +9) if sq%8 < i%8 and i < 64], 
		[i for i in range(sq+8, 64, +8) if i<64],
		[i for i in range(sq+7, 64, +7) if sq%8> i% 8 and i < 64], 
		[i for i in range(sq-1, -1, -1) if sq/8 == i/8 and i >= 0],
		[i for i in range(sq-9, -1, -9) if sq%8 > i%8 and i >= 0],
		[i for i in range(sq-8, -1, -8) if i >= 0],
		[i for i in range(sq-7, -1, -7) if sq%8 < i%8 and i >= 0],  
])   

# Initialize attack maps
for i in range(64):
    r_atks.append([])
    b_atks.append([])
    q_atks.append([])
    k_atks.append([])
    n_atks.append([])
    bp_atks.append([])
    wp_atks.append([])

# list indices
#  0   1   2
#    \ | / 
#  3 -sqr- 4
#    / | \
#  5   6   7

# convenience methods
def sqr_to_pgn(sqr):
    return "{}{}".format(chr(ord('a')+(sqr % 8)),8-sqr // 8)

def pgn_to_sqr(pgn):
    return (8-int(pgn[1]))*8 + ord(pgn[0]) - ord('a')

def build_atk_maps():
    for sq in range(64):
        delta=-9
        if sq + delta >= 0 and sq % 8 > (sq + delta) % 8:
            k_atks[sq].append(sq + delta)
        r = []
        while sq + delta >= 0 and sq % 8 > (sq + delta) % 8:
            r.append(sq + delta)
            delta-=9
        b_atks[sq].append(r)
        q_atks[sq].append(r)
        
        delta=-8
        if sq + delta >= 0:
            k_atks[sq].append(sq + delta)
        r = []
        while sq + delta >= 0:
            r.append(sq + delta)
            delta -= 8
        r_atks[sq].append(r)
        q_atks[sq].append(r)

        delta = -7
        if  sq + delta >= 0 and sq % 8 < (sq + delta) % 8:
            k_atks[sq].append(sq + delta)
        r = []
        while  sq + delta >= 0 and sq % 8 < (sq + delta) % 8:
            r.append(sq + delta)
            delta  -= 7
        b_atks[sq].append(r)
        q_atks[sq].append(r)

        delta=-1
        if sq + delta >= 0 and sq % 8 > (sq+delta) % 8:
            k_atks[sq].append(sq + delta)
        r = []
        while sq + delta >= 0 and sq % 8 > (sq+delta) % 8:
            r.append(sq + delta)
            delta -= 1
        r_atks[sq].append(r)
        q_atks[sq].append(r)

        delta = 1
        if sq + delta < 64 and sq % 8 < (sq+delta) % 8:
            k_atks[sq].append(sq + delta)
        r = []
        while sq + delta < 64 and sq % 8 < (sq+delta) % 8:
            r.append(sq + delta)
            delta += 1
        r_atks[sq].append(r)
        q_atks[sq].append(r)

        delta= 7
        if sq + delta < 64 and sq % 8 > (sq + delta) % 8:
            k_atks[sq].append(sq + delta)
        r = []
        while sq + delta < 64 and sq % 8 > (sq + delta) % 8:
            r.append(sq + delta)
            delta += 7
        b_atks[sq].append(r)
        q_atks[sq].append(r)

        delta = 8
        if sq + delta < 64:
            k_atks[sq].append(sq + delta)
        r = []
        while sq + delta < 64:
            r.append(sq + delta)
            delta += 8
        r_atks[sq].append(r)
        q_atks[sq].append(r)

        delta = 9
        if sq + delta < 64 and sq % 8 < (sq + delta) % 8:
            k_atks[sq].append(sq + delta)
        r = []
        while sq + delta < 64 and sq % 8 < (sq + delta) % 8:
            r.append(sq + delta)
            delta += 9 
        b_atks[sq].append(r)
        q_atks[sq].append(r)
         
        # knight maps
        for d in [-17,-15,-10,-6,6,10,15,17]:
            tsq = sq + d  
            if abs( sq // 8 - tsq // 8) + abs( sq % 8 - tsq %8 ) == 3 \
                and tsq >=0 and tsq < 64:
                n_atks[sq].append(sq + d)

        # pawn maps
        delta = 7
        if sq + delta < 64 and sq % 8 > (sq + delta) % 8:
            bp_atks[sq].append(sq + delta)
        delta = 9
        if sq + delta < 64 and sq % 8 < (sq + delta) % 8:
            bp_atks[sq].append(sq + delta)
        bp_atks.append(r)
        delta = -7
        if sq + delta >=0 and sq % 8 < (sq + delta) % 8:
            wp_atks[sq].append(sq + delta)
        delta = -9
        if sq + delta >=0 and sq % 8 > (sq + delta) % 8:
            wp_atks[sq].append(sq + delta)

class Move(object):
    def __init__(self, src, dst):
        self.src, self.dst = src, dst
        self.pgn = ""
    def __str__(self):
        return str(self.dst)
    def __repr__(self):
        return "{}>{}".format(sqr_to_pgn(self.src),sqr_to_pgn(self.dst))

# Castling rights constants
#r_K=0b0001
#r_Q=0b0010
#r_k=0b0100
#r_q=0b1000

cr_K= 1 << 0
cr_Q= 1 << 1
cr_k= 1 << 2
cr_q= 1 << 3

class Chess(object):
    def __init__(self):
        self.bb = {}
        self._fire_action = None
        self.t = -1
        self.ply = -1
        self.crights = -1
        self.ep_sqr = None

    def __copy__(self):
        cp = Chess()
        cp.bb=copy.deepcopy(self.bb)
        cp._fire_action = None
        cp.t = self.t
        cp.ply = self.ply
        cp.crights = self.crights
        cp.ep_sqr = self.ep_sqr
        return cp

    def setup(self, fen = None):
        self.t = 1
        self.ply = 0
        self.crights = cr_K | cr_Q | cr_k | cr_q
        self.ep_sqr = None
        # initialize bitboards
        for p in 'prnbqkrPRNBQKR':
            self.bb[p]=0

        if fen == None:
            fen = init_fen
        i=0
        tokens = fen.split()
        for c in tokens[0]:
            if c.isalpha():
                self.bb[c] |= 1 << i
                i+=1
            elif c.isdigit():
                i+=int(c)
        self.t = 1 if tokens[1] == "w" else "b"
    
        self.crights = 0
        if "K" in tokens[2]:
            self.crights |= cr_K
        if "Q" in tokens[2]:
            self.crights |= cr_Q
        if "k" in tokens[2]:
            self.crights |= cr_k
        if "q" in tokens[2]:
            self.crights |= cr_q
        
        self.ep_sqr = None if tokens[3]=="-" else tokens[3]

        if self._fire_action is not None:
            self._fire_action("<<setup>>",fen)

    def print(self):
        for sq in range(64):
            b = 1 << sq
            found = False
            for p in "prnbqkPRNBQK":
                if self.bb[p] & b:
                    print(" {}".format(p), end='')
                    found = True
            if not found:
                print(" .", end='')
            if sq % 8 == 7:
                print("")

    def fen(self):
        # encode FEN notation
        l=[]
        spc = 0
        for sq in range(64):
            b = 1 << sq
            found = False
            for p in "prnbqkPRNBQK":
                if self.bb[p] & b:
                    l.append(p)
                    found = True
            if not found:
                spc += 1
            if sq % 8 == 7 and sq != 63:
                if spc > 0:
                    l.append(str(spc))
                    spc = 0
                l.append("/")
        l.append(" ")
        l.append("b" if self.t == 0 else "w")
        l.append(" ")
        if self.crights == 0:
            l.append ("-")
        else:
            l.append("K" if self.crights & cr_K else "")
            l.append("Q" if self.crights & cr_Q else "")
            l.append("k" if self.crights & cr_k else "")
            l.append("q" if self.crights & cr_q else "")
        l.append(" ")
        l.append("-" if self.ep_sqr == None else sqr_to_pgn(self.ep_sqr))
        l.append(" 0 ")
        l.append(str(self.ply+1))
        return "".join(l)
        
#   def put(self,sq,pc):
#       self.bb[pc] |= 1 << sq

#   def remove(self,sq,pc):
#       self.bb[pc] &= ~(1 << sq)

    def get_all_moves(self):
        occ = [0,0]
        for x in 'prnbqk':
            occ[0] |= self.bb[x]
        for x in 'PRNBQK':
            occ[1] |= self.bb[x]
        empt = ~(occ[0] | occ[1])

        if self.t == 0:
            for sq in range(64):
                if self.bb['r'] & 1 << sq:
                    for ray in r_atks[sq]:
                        for tsq in ray:
                            if empt & 1 << tsq:
                                yield Move(sq, tsq)
                            elif occ[1] & 1 << tsq:
                                yield Move(sq, tsq)
                                break
                            else:
                                break
                elif self.bb['b'] & 1 << sq:
                    for ray in b_atks[sq]:
                        for tsq in ray:
                            if empt & 1 << tsq:
                                yield Move(sq, tsq)
                            elif occ[1] & 1 << tsq:
                                yield Move(sq, tsq)
                                break
                            else:
                                break
                elif self.bb['q'] & 1 << sq:
                    for ray in q_atks[sq]:
                        for tsq in ray:
                            if empt & 1 << tsq:
                                yield Move(sq, tsq)
                            elif occ[1] & 1 << tsq:
                                yield Move(sq, tsq)
                                break
                            else:
                                break
                elif self.bb['k'] & 1 << sq:
                    for tsq in k_atks[sq]:
                        if empt & 1 << tsq or occ[1] & 1 << tsq:
                            yield Move(sq, tsq)
                    if sq == 4:
                        if self.crights & cr_k and empt & 1 << 5 and empt & 1 << 6:
                            yield Move(4, 6)
                        elif self.crights & cr_q and empt & 1 << 3 and empt & 1 << 2:
                            yield Move(4, 2)
                elif self.bb['p'] & 1 << sq:
                    for tsq in bp_atks[sq]:
                        if occ[1] & 1 << tsq or tsq == self.ep_sqr:  # pawn capture
                            yield Move(sq, tsq)
                    if sq+8 < 64 and empt & 1 << sq + 8:  # pawn advance
                        yield Move(sq, sq + 8)
                    if sq//8 == 1 and empt & 1 << sq + 8 and empt & 1 << sq + 16:
                        yield Move(sq ,sq + 16)
                elif self.bb['n'] & 1 << sq:
                    for tsq in n_atks[sq]:
                        if empt & 1 << tsq or occ[1] & 1 << tsq:
                            yield Move(sq, tsq)
        else:
            for sq in range(64):
                if self.bb['R'] & 1 << sq:
                    for ray in r_atks[sq]:
                        for tsq in ray:
                            if empt & 1 << tsq:
                                yield Move(sq, tsq)
                            elif occ[0] & 1 << tsq:
                                yield Move(sq, tsq)
                                break
                            else:
                                break
                elif self.bb['B'] & 1 << sq:
                    for ray in b_atks[sq]:
                        for tsq in ray:
                            if empt & 1 << tsq:
                                yield Move(sq, tsq)
                            elif occ[0] & 1 << tsq:
                                yield Move(sq, tsq)
                                break
                            else:
                                break
                elif self.bb['Q'] & 1 << sq:
                    for ray in q_atks[sq]:
                        for tsq in ray:
                            if empt & 1 << tsq:
                                yield Move(sq, tsq)
                            elif occ[0] & 1 << tsq:
                                yield Move(sq, tsq)
                                break
                            else:
                                break
                elif self.bb['K'] & 1 << sq:
                    for tsq in k_atks[sq]:
                        if empt & 1 << tsq or occ[0] & 1 << tsq:
                            yield Move(sq, tsq)
                    if sq == 60:
                        if self.crights & cr_K and empt & 1 << 61 and empt & 1 << 62:
                            yield Move(60, 62)
                        elif self.crights & cr_Q and empt & 1 << 59 and empt & 1 << 58:
                            yield Move(60, 58)
                elif self.bb['P'] & 1 << sq:
                    for tsq in wp_atks[sq]:
                        if occ[0] & 1 << tsq or tsq == self.ep_sqr:  # pawn capture
                            yield Move(sq, tsq)
                    if sq+8 < 64 and empt & 1 << sq - 8:  # pawn advance
                        yield Move(sq, sq - 8)
                    if sq//8 == 6 and empt & 1 << sq - 8 and empt & 1 << sq - 16:
                        yield Move(sq, sq - 16)
                elif self.bb['N'] & 1 << sq:
                    for tsq in n_atks[sq]:
                        if empt & 1 << tsq or occ[0] & 1 << tsq:
                            yield Move(sq, tsq)

    def is_self_checking_move(self, mv):
        cp = copy.copy(self)
#       cp._fire_action = None

        k_pos = cp.bb['k' if cp.t == 0 else 'K'].bit_length()-1
        cp.move(mv)
        atks = 0
        for m in cp.get_all_moves():
#           atks |= 1 << m.dst
            if m.dst == k_pos:
                return True
        return False 

    def move(self, mv):
        piece, capt = '',''
        for k,v in self.bb.items():
            if v & 1 << mv.dst:
                capt = k
                self.bb[capt] &= ~(1 << mv.dst)
        for k,v in self.bb.items():
            if v & 1 << mv.src:
                piece = k
                self._move(piece, mv.src, mv.dst)
        #castling
        if piece == 'k':
            if mv.src==4 and mv.dst==6:
                self.move('r',7,5)
            elif mv.src==4 and mv.dst==2:
                self.move('r',0,3)
            self.crights &= ~(cr_k|cr_q)
        elif piece == 'K':
            if mv.src==60 and mv.dst==62:
                self.move('R',63,61)
            elif mv.src==60 and mv.dst==58:
                self.move('R',56,59)
            self.crights &= ~(cr_K|cr_Q)
        #promotion
        elif piece == 'p':
            if mv.dst // 8 == 7:
                pass
            elif mv.dst == self.ep_sqr:  #ep capture
                self._remove('p', mv.dst - 8)
        elif piece == 'P':
            if mv.dst // 8 == 0:
                pass
            elif mv.dst == self.ep_sqr:
                self._remove('p', mv.dst + 8)
        #ep square set/unset
        if piece == 'p' and mv.dst - mv.src == 16:  #ep-sqr set
            self.ep_sqr = mv.src + 8
        elif piece == 'P' and mv.src - mv.dst == 16:
            self.ep_sqr = mv.src - 8
        else:
            self.ep_sqr = None
        self.t ^= 1
        self.ply += 1

    def make(self, src, dst):
        print("MAKE--:{}->{}".format(src,dst))

        legal_moves = (list(filter(lambda x: not self.is_self_checking_move(x),
            self.get_all_moves())))
        for m in legal_moves:
            if src == m.src and dst == m.dst:
                print("MAKE-Move()")
                self.move(m)
                return True
        return False

    def _move(self, piece, src, dst):
        self.bb[piece] &= ~(1 << src)
        self.bb[piece] |= 1 << dst
        if self._fire_action is not None:
            self._fire_action("<<move>>",{"piece":piece,"src":src,"dst":dst})

    def _remove(self, piece, sqr):
        self.bb[piece] &= ~(1 << sqr)
        if self._fire_action is not None:
            self._fire_action("<<remove>>",[piece,sqr])

if __name__=="__main__":
    build_atk_maps()
    chess = Chess()
    chess.setup()
    
    while True:
        chess.print()
        pgn = input("{} to move,Enter your move(e2e4 etc):".format("Black" if chess.t==0 else "White"))
        if not chess.make(pgn_to_sqr(pgn[0:2]),pgn_to_sqr(pgn[2:4])):
            print("Wrong move.")



