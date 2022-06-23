import uuid
from datetime import datetime



class Node:
    def __init__(self, elem="", my_id=0.0, parent_id=None, child_id=None):
        self.elem = elem
        self.my_id = my_id
        self.parent_id = parent_id
        self.child_id = child_id

    def get_elem(self):
        return self.elem

    def get_id(self):
        return self.id

    def get_parent_id(self):
        return self.parent_id

    def get_child_id(self):
        return self.child_id

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

class TextSeq:

    def __init__(self):
        self.charPosCharr = [[], []]
        self.charIdPos = {}  # dict()?

    def add_char_here(self, elem, posx, posy, mnUserTany=0, id=None):
        wATCHOUT_NEWLINE = 0

        if mnUserTany:
            my_id = id
        else:
            my_id = datetime.timestamp(datetime.now())

        # my_id = datetime.timestamp(datetime.now())

        # if elem == '\n':
        #     print('yes')


        if posy == 0: # 2wl 7rf
            # try:
            #     self.charPosCharr[posx]
            # except IndexError:
            #     self.charPosCharr.append([])
                # actually should compare posx w/ len might do more appends

            if len(self.charPosCharr[posx]) == 0:  # 2wl 7rf w l line fady
                child_id = None
                parent_id = None
                c = Node(elem, my_id, parent_id, child_id)
                self.charPosCharr[posx].insert(posy, c)
                self.charIdPos[my_id] = [posx, posy]
                if elem == '\n':
                    self.charPosCharr.append([])
            else: # 2wl 7rf bs l line msh fady. hyb2a li child
                if elem == '\n':  # lw \n yb2a no child
                    child_char = self.charPosCharr[posx][posy]
                    child_char.parent_id = None # b2a f new line
                    print("LOOK HERE"+child_char.elem)
                    # if child_char.elem == '\n':
                    print("LOOK ENTERED IT")
                    wATCHOUT_NEWLINE = 1
                    newline_child = child_char.my_id

                    self.shift_lines_below(child_char, posx, posy)

                    child_id = None
                    parent_id = None # 34an da awl 7rf
                    c = Node(elem, my_id, parent_id, child_id)
                    self.charPosCharr[posx].insert(posy, c)
                    self.charIdPos[my_id] = [posx, posy]
                    self.shift_child_chars(posx, posy)

                else:
                    child_char = self.charPosCharr[posx][posy]
                    child_char.parent_id = my_id
                    child_id = child_char.my_id
                    parent_id = None
                    c = Node(elem, my_id, parent_id, child_id)
                    self.charPosCharr[posx].insert(posy, c)
                    self.charIdPos[my_id] = [posx, posy]
                    self.shift_child_chars(posx, posy)
        else: # msh awl 7rf
            if posy < len(self.charPosCharr[posx]): # msh 2a5r 7rf. liha children
                if elem == '\n':
                    child_char = self.charPosCharr[posx][posy]
                    parent_char = self.charPosCharr[posx][posy - 1]
                    child_char.parent_id = None # b2a f new line
                    self.shift_lines_below(child_char, posx, posy)

                    parent_char.child_id = my_id
                    child_id = None
                    parent_id = parent_char.my_id
                    c = Node(elem, my_id, parent_id, child_id)
                    self.charPosCharr[posx].insert(posy, c)
                    self.charIdPos[my_id] = [posx, posy]
                    self.shift_child_chars(posx, posy)
                else:
                    child_char = self.charPosCharr[posx][posy]
                    parent_char = self.charPosCharr[posx][posy - 1]
                    child_char.parent_id = my_id
                    parent_char.child_id = my_id
                    child_id = child_char.my_id
                    parent_id = parent_char.my_id
                    c = Node(elem, my_id, parent_id, child_id)
                    self.charPosCharr[posx].insert(posy, c)
                    self.charIdPos[my_id] = [posx, posy]
                    self.shift_child_chars(posx, posy)
            else: # 2a5r 7rf
                if elem == '\n':
                    parent_char = self.charPosCharr[posx][posy - 1]
                    parent_char.child_id = my_id
                    child_id = None
                    parent_id = parent_char.my_id
                    self.shift_lines_below2(posx, posy)

                    c = Node(elem, my_id, parent_id, child_id)
                    self.charPosCharr[posx].insert(posy, c)
                    self.charIdPos[my_id] = [posx, posy]
                    # self.shift_child_chars(posx, posy)
                else:
                    parent_char = self.charPosCharr[posx][posy - 1]
                    parent_char.child_id = my_id
                    child_id = None
                    parent_id = parent_char.my_id
                    c = Node(elem, my_id, parent_id, child_id)
                    self.charPosCharr[posx].insert(posy, c)
                    self.charIdPos[my_id] = [posx, posy]
                    # self.shift_child_chars(posx, posy)

        # elem, parent_id, child_id, id
        if not mnUserTany: #AAAADDDDD 3ND D
            if wATCHOUT_NEWLINE:
                print("CAME HERE")
                wATCHOUT_NEWLINE = 0
                return ("1&" + elem + "&" + str(parent_id) + "&" + str(newline_child) + "&" + str(my_id))

            else:
                 return ("1&"+elem+"&"+str(parent_id)+"&"+str(child_id)+"&"+str(my_id))
        else:
            return -1
        #     pos = str(posx) + '.' + str(posy)
        #     txt.insertThere(pos, elem)

        # send_char_over(c) or register_add(c aw elem, id, pid) BL PARENT ID BS MSH POS HWA Y7SB L POS

    def shift_child_chars(self, posx, posy):

        for i in range(posy, len(self.charPosCharr[posx])):
            self.charIdPos[self.charPosCharr[posx][i].my_id] = [posx, i]
        return

    def shift_lines_below(self, child_char, posx, posy):
        self.charPosCharr.insert(posx+1, [])
        self.charPosCharr[posx+1].extend(self.charPosCharr[posx][posy:])
        del self.charPosCharr[posx][posy:]

        # update charIdPos

        for i in range(posx+1, len(self.charPosCharr)):
            for j in range(0, len(self.charPosCharr[i])):
                self.charIdPos[self.charPosCharr[i][j].my_id] = [i, j]
        return

    def shift_lines_below2(self, posx, posy):
        self.charPosCharr.insert(posx+1, [])
        # self.charPosCharr[posx+1].extend(self.charPosCharr[posx][posy:])
        # del self.charPosCharr[posx][posy:]

        # update charIdPos

        for i in range(posx+1, len(self.charPosCharr)):
            for j in range(0, len(self.charPosCharr[i])):
                self.charIdPos[self.charPosCharr[i][j].my_id] = [i, j]
        return

    def printList(self):
        for i in range(1, len(self.charPosCharr)):
            for j in range(0, len(self.charPosCharr[i])):
                print(str(str(i) + str(',') + str(j)) + str(self.charPosCharr[i][j]))



