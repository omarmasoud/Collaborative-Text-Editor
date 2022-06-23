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
                change_id = datetime.timestamp(datetime.now())
    
                obj={
                "operation":"ins",
                "elem":str(elem),
                "parent_id":str(parent_id),
                "child_id":str(newline_child),
                "my_id":str(my_id),
                "change_id":str(change_id),
                "lastRcvdChnge": " "
                }
                
                # return ("1&" + elem + "&" + str(parent_id) + "&" + str(newline_child) + "&" + str(my_id))
                return obj

            else:
                change_id = datetime.timestamp(datetime.now())
                obj={
                "operation":"ins",
                "elem":str(elem),
                "parent_id":str(parent_id),
                "child_id":str(child_id),
                "my_id":str(my_id),
                "change_id":str(change_id),
                "lastRcvdChnge": " "
                }
                
                # return ("1&" + elem + "&" + str(parent_id) + "&" + str(newline_child) + "&" + str(my_id))
                return obj
                #return ("1&"+elem+"&"+str(parent_id)+"&"+str(child_id)+"&"+str(my_id))
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



    def del_char_here(self, posx, posy, mnUserTany=0, id=None):
        # wATCHOUT_NEWLINE = 0


        charToDel = self.charPosCharr[posx][posy]
        elemToDel = self.charPosCharr[posx][posy].elem
        myidToDel = self.charPosCharr[posx][posy].my_id
        parentidToDel = self.charPosCharr[posx][posy].parent_id
        childidToDel = self.charPosCharr[posx][posy].child_id

        # COMPARE ID(CHAR ID) B ELEMTODEL

        # self.elem = elem
        # self.my_id = my_id
        # self.parent_id = parent_id
        # self.child_id = child_id

        # PROBLEMMMMMMMMMM NEED TO UPDATE CHARIDPOS
        if charToDel.elem != '\n':
            # lw l char l w7id fl line (2a5r 7rf fl txt). la parent wla child
            if charToDel.parent_id == None and charToDel.child_id == None:
                self.charPosCharr[posx].pop(posy) # that's it
                self.charIdPos.pop(myidToDel, None) # OPTION HERE. 5OD L ID MN CHARPOSCHARR 2BL L POP. AW TB2A = .POP()
                # NOT HANDLNG IF NOT FOUND THNG. da msh mn user tany tho
            # li parent bs no child. 2a5r char 5als. kda l parent bta3o b2a 2a5r char 5als
            elif charToDel.parent_id != None and charToDel.child_id == None:
                # set l parent l child bta3o le none
                parentPos = self.charIdPos[parentidToDel]
                self.charPosCharr[parentPos[0]][parentPos[1]].child_id = None
                self.charPosCharr[posx].pop(posy)  # that's it
                self.charIdPos.pop(myidToDel, None)
            # mlush parent (awl 7rf fl doc) bs li child HERE L CHILDREN BYT7RKO FA M7TAG 2A UPDATE CHARIDPOS mn CHARPOSCHARR
            elif charToDel.parent_id == None and charToDel.child_id != None:
                # set l parent bta3 l child le none
                childPos = self.charIdPos[childidToDel]
                self.charPosCharr[childPos[0]][childPos[1]].parent_id = None

                self.charPosCharr[posx].pop(posy)  # that's it
                self.charIdPos.pop(myidToDel, None)
                #SHIFT CHILDREN FUNCTION. UPDATE POS IN ROW(POSX)************************
                self.update_pos_in_row(posx, posy)

                # ana m7tag 2a shaffet l children btu3 l row bs.. self.charPosCharr[posx] mmkn yb2a fi \n bs aw 7ruf bs aw 7ruf w \n
                # ha call function y3dy 3l length bta3 self.charPosCharr[posx] w y update charIdPos

            else: # li child w li parent. anyway brdo ha shift l child bs
                # dont forget en l parent yb2a l child bta3o l child.
                # wl child yb2a l parent bta3o l parent
                childPos = self.charIdPos[childidToDel]
                parentPos = self.charIdPos[parentidToDel]
                self.charPosCharr[childPos[0]][childPos[1]].parent_id = self.charPosCharr[parentPos[0]][parentPos[1]].my_id
                self.charPosCharr[parentPos[0]][parentPos[1]].child_id = self.charPosCharr[childPos[0]][childPos[1]].my_id

                self.charPosCharr[posx].pop(posy)  # that's it
                self.charIdPos.pop(myidToDel, None)
                # SHIFT CHILDREN FUNCTION. UPDATE POS IN ROW(POSX)************************
                self.update_pos_in_row(posx, posy)
        # lw deleted new line \n
        # mmkn mlush child wla parent (BS ANA BA APPEND [] FL DICT. ASHLHA? MAYB NO NEED?)
        # I THINK NO NEED
        # lw no parent. but child. lma 2a delete. ha extend l row
        # lw parent but no child. pop 3ady (may delete l list l 25ira mayb)
        # lw parent and child. l parent l child bta3o hwa l child wl child l p bta3 l p. ha extend row l \n w 2shft kollo fo2
        else: # \n L CHILD B NONE 3LA TUL
            # \n f str lw7dha
            if charToDel.parent_id == None:
                self.charPosCharr[posx].pop(posy)
                self.charIdPos.pop(myidToDel, None) # OPTION HERE. 5OD L ID MN CHARPOSCHARR 2BL L POP. AW TB2A = .POP()

                # not done yet. delete l list bt3to 34an tshaffet kollo fo2
                self.charPosCharr.pop(posx)  # delete l list bt3tha
                self.update_all_pos_in_rows(posx, posy)

                # NOT HANDLNG IF NOT FOUND THNG. da msh mn user tany tho
            # li parent bs no child. 2a5r char 5als. kda l parent bta3o b2a 2a5r char 5als
            else:
                # set l parent l child bta3o le none
                parentPos = self.charIdPos[parentidToDel]
                if len(self.charPosCharr[posx+1]) != 0:
                    self.charPosCharr[posx+1][0].parent_id = self.charPosCharr[posx][posy-1].my_id
                    self.charPosCharr[posx][posy-1].child_id = self.charPosCharr[posx+1][0].my_id
                    self.charPosCharr[posx].pop(posy)
                    self.charIdPos.pop(myidToDel, None)
                    # newL[1].extend(newL[1 + 1][0:])
                    self.charPosCharr[posx].extend(self.charPosCharr[posx + 1][0:])
                    self.charPosCharr.pop(posx + 1)  # delete l row l b3dha w shft fo2 kollo

                    self.update_pos_in_row(posx, posy)
                    self.update_all_pos_in_rows(posx + 1, posy)
                else:
                    self.charPosCharr[posx][posy - 1].child_id = None
                    self.charPosCharr[posx].pop(posy)
                    self.charIdPos.pop(myidToDel, None)
                    # newL[1].extend(newL[1 + 1][0:])
                    # self.charPosCharr[posx].extend(self.charPosCharr[posx + 1][0:])
                    self.charPosCharr.pop(posx + 1)  # delete l row l b3dha w shft fo2 kollo

                    # self.update_pos_in_row(posx, posy)
                    # self.update_all_pos_in_rows(posx + 1, posy)


                    # charToDel = self.charPosCharr[posx][posy]
                    # elemToDel = self.charPosCharr[posx][posy].elem
                    # myidToDel = self.charPosCharr[posx][posy].my_id
                    # parentidToDel = self.charPosCharr[posx][posy].parent_id
                    # childidToDel = self.charPosCharr[posx][posy].child_id

        if not mnUserTany:  # AAAADDDDD 3ND D
                    # TIMESTAAAMMMMPPPP
                    # change_id = datetime.timestamp(datetime.now())
            change_id = datetime.timestamp(datetime.now())
            obj={
                "operation":"del",
                "elem":str(elemToDel),
                "parent_id":str(parentidToDel),
                "child_id":str(childidToDel),
                "my_id":str(myidToDel),
                "change_id":str(change_id),
                "lastRcvdChnge": " "
                }
                
                # return ("1&" + elem + "&" + str(parent_id) + "&" + str(newline_child) + "&" + str(my_id))
            return obj
            # return ("5&" + elemToDel + "&" + str(parentidToDel) + "&" + str(childidToDel) + "&" + str(myidToDel))
        else:
            return -1
                #     pos = str(posx) + '.' + str(posy)
                #     txt.insertThere(pos, elem)

                # send_char_over(c) or register_add(c aw elem, id, pid) BL PARENT ID BS MSH POS HWA Y7SB L POS

    def update_pos_in_row(self, posx, posy):
        for j in range(posy, len(self.charPosCharr[posx])):
            self.charIdPos[self.charPosCharr[posx][j].my_id] = [posx, j]
        return


    def update_all_pos_in_rows(self, posx, posy):
        #2frd fi rows fdya fl 2a5r?
        for i in range(posx, len(self.charPosCharr)):
            if len(self.charPosCharr[i]) != 0:
                for j in range(0, len(self.charPosCharr[i])):
                    self.charIdPos[self.charPosCharr[i][j].my_id] = [i, j]
        return






