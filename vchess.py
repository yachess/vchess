import copy

init_pos = "rnbqkbnrpppppppp................................PPPPPPPPRNBQKBNR"

q_atks=[]
b_atks=[]
r_atks=[]
n_atks=[]
k_atks=[]
bp_atks=[]
wp_atks=[]

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
#  0 - 1 - 2
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
        delta = -16-1
        if sq + delta >= 0 and sq % 8 > (sq + delta) % 8:
            n_atks[sq].append(sq + delta)
        delta = -16+1
        if sq + delta >= 0 and sq % 8 < (sq + delta) % 8:
            n_atks[sq].append(sq + delta)
        delta = -8-2
        if sq + delta >= 0 and sq % 8 > (sq + delta) % 8:
            n_atks[sq].append(sq + delta)
        delta = -8+2
        if sq + delta >= 0 and sq % 8 < (sq + delta) % 8:
            n_atks[sq].append(sq + delta)
        delta = +8-2
        if sq + delta < 64 and sq % 8 > (sq + delta) % 8:
            n_atks[sq].append(sq + delta)
        delta = +8+2
        if sq + delta < 64 and sq % 8 < (sq + delta) % 8:
            n_atks[sq].append(sq + delta)
        delta = +16-1
        if sq + delta < 64 and sq % 8 > (sq + delta) % 8:
            n_atks[sq].append(sq + delta)
        delta = +16+1
        if sq + delta < 64 and sq % 8 < (sq + delta) % 8:
            n_atks[sq].append(sq + delta)

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

class Move:
    def __init__(self, src, dst):
        self.src, self.dst = src, dst
        self.pgn = ""
    def __str__(self):
        return str(self.dst)
    def __repr__(self):
        return "{}>{}".format(sqr_to_pgn(self.src),sqr_to_pgn(self.dst))

# Castling rights constants
K=0b0001
Q=0b0010
k=0b0100
q=0b1000

class Chess:
    def __init__(self, fen = None):
        print("init")
        self.bb = {}
        self.t = 1
        self.ply = 0
        self.crights = K | Q | k | q
        self.ep_sqr = None
        # initialize bitboards
        for p in 'prnbqkrPRNBQKR':
            self.bb[p]=0
        for i in range(len(init_pos)):
            if init_pos[i] != '.':
                self.bb[init_pos[i]] |= 1 << i
         
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
        pass

    def put(self,sq,pc):
        self.bb[pc] |= 1 << sq
        pass

    def remove(self,sq,pc):
        self.bb[pc] &= ~(1 << sq)
        pass

    def get_all_moves(self):
        occ = [self.bb['p'] | self.bb['r'] | self.bb['n'] | self.bb['b'] | self.bb['q'] | self.bb['k'], 
            self.bb['P'] | self.bb['R'] | self.bb['N'] | self.bb['B'] | self.bb['Q'] | self.bb['K']]
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
                        if self.crights & k and empt & 1 << 5 and empt & 1 << 6:
                            yield Move(4, 6)
                        elif self.crights & q and empt & 1 << 3 and empt & 1 << 2:
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
                        if self.crights & K and empt & 1 << 61 and empt & 1 << 62:
                            yield Move(60, 62)
                        elif self.crights & Q and empt & 1 << 59 and empt & 1 << 58:
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
        c = copy.deepcopy(self)
        k_pos = c.bb['k' if c.t == 0 else 'K'].bit_length()-1
        c.make_move(mv)
        atks = 0
        for m in c.get_all_moves():
#           atks |= 1 << m.dst
            if m.dst == k_pos:
                return True
        return False 

    def move(self, piece, src, dst):
        self.bb[piece] &= ~(1 << src)
        self.bb[piece] |= 1 << dst

    def remove(self, piece, sqr):
        self.bb[piece] &= ~(1 << sqr)

    def make_move(self, mv):
        piece, capt = '',''
        for k,v in self.bb.items():
            if v & 1 << mv.dst:
                capt = k
                self.bb[capt] &= ~(1 << mv.dst)
        for k,v in self.bb.items():
            if v & 1 << mv.src:
                piece = k
                self.move(piece, mv.src, mv.dst)
        #castling
        if piece == 'k':
            if mv.src==4 and mv.dst==6:
                self.move('r',7,5)
            elif mv.src==4 and mv.dst==2:
                self.move('r',0,3)
            self.crights &= ~(k|q)
        elif piece is 'K':
            if mv.src==60 and mv.dst==62:
                self.move('R',63,61)
            elif mv.src==60 and mv.dst==58:
                self.move('R',56,59)
            self.crights &= ~(K|Q)
        #promotion
        elif piece is 'p':
            if mv.dst // 8 == 7:
                pass
            elif mv.dst == self.ep_sqr:  #ep capture
                self.remove('p', mv.dst - 8)
        elif piece is 'P':
            if mv.dst // 8 == 0:
                pass
            elif mv.dst == self.ep_sqr:
                self.remove('p', mv.dst + 8)
        #ep square set/unset
        if piece is 'p' and mv.dst - mv.src == 16:  #ep-sqr set
            self.ep_sqr = mv.src + 8
        elif piece is 'P' and mv.src - mv.dst == 16:
            self.ep_sqr = mv.src - 8
        else:
            self.ep_sqr = None
        self.t ^= 1
        self.ply += 1

build_atk_maps()
chess = Chess()

while True:
    chess.print()
    mvs = chess.get_all_moves()
    legal_moves = (list(filter(lambda x: not chess.is_self_checking_move(x),mvs)))
    pgn = input("{} to move,Enter your move:".format("Black" if chess.t==0 else "White"))
    handled = False
    for m in legal_moves:
        mv = Move(pgn_to_sqr(pgn[0:2]),pgn_to_sqr(pgn[2:4]))
        if mv.src == m.src and mv.dst == m.dst:
            chess.make_move(mv)
            handled = True
    if not handled:
        print("Wrong move.")


