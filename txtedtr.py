import tkinter as tk
from threading import Thread
from tkinter.filedialog import askopenfilename, asksaveasfilename
from idlelib.redirector import WidgetRedirector

from ConnectionManager import *

from AWSLambdaConnectionManager import connection_manager

import node

import json

import time

lastRcvdChnge = -1


def open_file():
    """Open a file for editing."""

    txt_edit.delete(1.0, tk.END)
    filepath = "D:/New folder (2)/dstrbtd text file/dst.txt"
    # filepath = askopenfilename(
    #     filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    # )
    if not filepath:
        return
    txt_edit.delete(1.0, tk.END)
    with open(filepath, "r") as input_file:
        text = input_file.read()
        txt_edit.insert(tk.END, text)
    window.title(f"Text Editor Application - {filepath}")

    print(filepath)
    txt_edit.edit_modified(0)


def save_file():
    """Save the current file as a new file."""
    filepath = "D:/New folder (2)/dstrbtd text file/dst.txt"
    # filepath = asksaveasfilename(
    #     defaultextension="txt",
    #     filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
    # )
    if not filepath:
        return
    with open(filepath, "w") as output_file:
        text = txt_edit.get(1.0, tk.END)
        output_file.write(text)
    window.title(f"Text Editor Application - {filepath}")
    txt_edit.edit_modified(0)


def btndplcte():
    print(txt_edit.get(1.0, "end-1c"))
    print(txt_edit.index(tk.INSERT))
    x = txt_edit.index(tk.INSERT)

    txt11 = txt_edit.get(1.0, "end-1c")
    txt_edit.delete(1.0, tk.END)
    txt_edit.insert(tk.END, txt11)

    print(x.split('.')[0])
    print(x.split('.')[1])
    txt_edit.mark_set("insert", "%d.%d" % (int(x.split('.')[0]), int(x.split('.')[1])))


def btn2crsr():
    print(txt_edit.index(tk.INSERT))
    txt_edit.mark_set("insert", "%d.%d" % (1, 2))


def btn3sndbtn():
    print(txt_edit.get(1.0, "end-1c"))
    print('hi')
    txt_msg = txt_edit.get(1.0, "end-1c")
    cm.BroadCast(txt_msg)

# buffEnable = 0
# def senderBuffHandler():
#     while 1:
#         if buffEnable:
#
#         pass

def btn4cnct():
    # cm.Connect()
    print("connected")
    Thread(target=changeOccured).start()
    # Thread(target=senderBuffHandler).start()


def btn5dscnct():
    mg = 0


counter = 0;


def btn6edted(e):
    global counter
    counter += 1
    print(counter)
    btn3sndbtn()


def btn7addchar():
    # get position l cursor
    print(txt_edit.index(tk.INSERT))
    x = txt_edit.index(tk.INSERT)

    posx = int(x.split('.')[0])
    posy = int(x.split('.')[1]) - 1
    print(posx)
    print(posy)

    ind = str(posx) + '.' + str(posy)
    # print(txt_edit.get(txt_edit.index(tk.INSERT)))
    print(txt_edit.get(ind))
    elem = txt_edit.get(ind)
    # print(n.charPosCharr)
    print(n.charIdPos)
    n.add_char_here(elem, posx, posy)
    print(n.charIdPos)
    # print(n.charPosCharr)
    n.printList()


def btn8addmrk():
    txt_edit.tag_add('c', 1.2, 1.3)
    txt_edit.tag_configure('c', background='red')


def btn9addmrk():
    txt_edit.tag_delete('c')
    txt_edit.tag_add('c', txt_edit.index(tk.INSERT))
    txt_edit.tag_configure('c', background='red')


arr = []
prob = 0
seq_ind = 0


def btn10edted(e):
    global arr
    global prob
    global seq_ind
    print('RELEASED')
    # txt_edit.configure(state="disabled")

    # btn10chckmod()
    arr.append(txt_edit.index(tk.INSERT))
    print(arr)
    # UNDERLINE! lw prob = 1
    if len(arr) > 1:
        if (int(arr[-1].split('.')[1]) - int(arr[-2].split('.')[1])) != 1:
            print(int(arr[-2].split('.')[1]))
            print(int(arr[-1].split('.')[1]))
            print("HOLD ONNNN")
            prob = 1
            btn_11.config(bg='red')
            if seq_ind == 0:
                seq_ind = arr[-2]

    if prob == 1:
        addUnderline(seq_ind)

        # 23mlha marra w7da
        # disable lw new line
        # mayb blink l button
        # another thing what id 3ml new line w kammel?
        # lw 3ml new line. disable w 2ollo updating wait w h3mlha mn nfsy ana


def btn10chckmod():
    print(txt_edit.edit_modified())
    if txt_edit.edit_modified() == 1:
        print("CALLED")
        btn7addchar()
        save_file()
    # txt_edit.configure(state="normal")


def btn11fixprob():
    global seq_ind
    global arr
    global prob
    if prob == 1:
        prob = 0
        print("There is a problem starting from " + seq_ind)
        btn_11.config(bg='#f0f0f0')
        arr = []
        seq_ind = 0
        # call function t update l sequence
        removeUnderline()


def addUnderline(ind):
    txt_edit.tag_delete('notUpdatedInDict')
    txt_edit.tag_add('notUpdatedInDict', ind, 'end')
    txt_edit.tag_configure('notUpdatedInDict', underline=True)


def removeUnderline():
    txt_edit.tag_delete('notUpdatedInDict')


start_writing = 0


def btn12strtwrtng():
    global start_writing
    start_writing = 1
    # mayb check consistency first as well
    # print(old_insert)


def btn13stpwrtng():
    global start_writing
    start_writing = 0


mnUserTany = 0
charId = '400'


class Application(tk.Frame):

    def __init__(self, master):
        self.master = master
        tk.Frame.__init__(self)
        self.chngeBuffer = list()
        self.localBuffer = list()
        self.chngesBroadcastByMe = {} #JSONDUMPS lw l msg list b awl id aw 2a5r id which?

        self._after_id = None

        self.counter = 0
        self.end = 0
        self.justSent = ""

    def handle_wait(self):
        # cancel the old job
        if self._after_id is not None:
            self.after_cancel(self._after_id)

        # create a new job
        self._after_id = self.after(1000, self.send_change)

    def sendNow(self, i):
        print(i)
        print(self.localBuffer[i:i + 4])

        # i = self.counter
        # if self.counter < len(self.localBuffer):
        #     print("LOOOOK", self.localBuffer[i:i + 4])
        # how h len = 9
        # 0:4
        # 4:8
        # 8:12
        # 0 4
        if (len(self.localBuffer) - i) >= 4:
            lastChnge = json.loads(self.localBuffer.pop(i+3))
            lastChnge["lastBrdcstChnge"] = list(self.chngesBroadcastByMe)[-1] if len(
                list(self.chngesBroadcastByMe)) > 0 else -1
            # self.chngeBuffer.append(json.dumps(lastChnge))
            self.localBuffer.insert(i+3, json.dumps(lastChnge))

            cm.BroadCast(self.localBuffer[i:i + 4])
            # 23MLHA REGISTER FL SENT
            self.justSent = json.loads(self.localBuffer[i+3])["change_id"]
            print(self.justSent)

            self.chngesBroadcastByMe[json.loads(self.localBuffer[i + 3])["change_id"]] = self.localBuffer[i:i + 4]
        else:
            lastChnge = json.loads(self.localBuffer.pop(len(self.localBuffer)-1))
            lastChnge["lastBrdcstChnge"] = list(self.chngesBroadcastByMe)[-1] if len(
                list(self.chngesBroadcastByMe)) > 0 else -1
            self.localBuffer.append(json.dumps(lastChnge))

            cm.BroadCast(self.localBuffer[i:len(self.localBuffer)])
            # 23MLHA REGISTER FL SENT
            self.justSent = json.loads(self.localBuffer[len(self.localBuffer)-1])["change_id"]
            print(self.justSent)

            self.chngesBroadcastByMe[json.loads(self.localBuffer[len(self.localBuffer)-1])["change_id"]] = self.localBuffer[i:len(self.localBuffer)]
            print("DIIIICCCTTTT", self.chngesBroadcastByMe)
            # clear localBuffer now
        #     self.counter += 4
        # else:
        #     self.counter = 0

    def send_change(self):
        if len(self.localBuffer) == 0 or (len(self.localBuffer) != 0 and (float(json.loads(self.localBuffer[-1])["change_id"]) <= float(self.justSent))):
            if len(self.chngeBuffer) > 4:
                i = 0
                j = 0
                self.localBuffer = self.chngeBuffer.copy()
                while i < len(self.localBuffer):
                    # self.after(j, self.sendNow)
                    self.after(j, lambda x=i: self.sendNow(x))
                    i += 4
                    j += 700
                self.end = i - 4
            else:
                #2bl l broadcast. h7ot l lastBrdcstChnge
                if len(self.chngeBuffer) != 0:
                    lastChnge = json.loads(self.chngeBuffer.pop(-1)) # watch HEEEEREEE KAN EMPTY
                    lastChnge["lastBrdcstChnge"] = list(self.chngesBroadcastByMe)[-1] if len(list(self.chngesBroadcastByMe)) > 0 else -1
                    self.chngeBuffer.append(json.dumps(lastChnge))

                    cm.BroadCast(self.chngeBuffer)
                    self.chngesBroadcastByMe[json.loads(self.chngeBuffer[-1])["change_id"]] = self.chngeBuffer[0:]

                    #23MLHA REGISTER FL SENT
                    print(self.chngeBuffer)
                    print(self.chngesBroadcastByMe)
            self.chngeBuffer.clear()
        else:
            print("need to WAIT")
            self.after(500, self.send_change)

        # if float(json.loads(self.localBuffer[-1])["change_id"]) > float(self.justSent):
        #     print("need to WAIT")
        #     self.after(500, self.send_change)
        # else:
        #
        #     if len(self.chngeBuffer) > 4:
        #         i = 0
        #         j = 0
        #         self.localBuffer = self.chngeBuffer.copy()
        #         while i < len(self.localBuffer):
        #             # self.after(j, self.sendNow)
        #             self.after(j, lambda x=i: self.sendNow(x))
        #             i += 4
        #             j += 700
        #         self.end = i - 4
        #     else:
        #
        #         if float(json.loads(self.localBuffer[-1])["change_id"]) > float(self.justSent):
        #             print("need to WAIT")
        #         print("local[-1]>justSent?", float(json.loads(self.localBuffer[-1])["change_id"]), " and ", float(self.justSent))
        #         cm.BroadCast(self.chngeBuffer)
        #         print(self.chngeBuffer)
        #             # time.sleep(0.6)
        #     self.chngeBuffer.clear()




def btnaddchar(indx1, indx2):
    global lastRcvdChnge
    global mnUserTany
    global charId

    # get position l cursor
    # print(txt_edit.index(tk.INSERT))
    x = indx1

    posx = int(x.split('.')[0])
    posy = int(x.split('.')[1])
    # print(posx)
    # print(posy)

    ind = str(posx) + '.' + str(posy)
    # print(txt_edit.get(ind))
    elem = txt_edit.get(ind)

    # print(n.charIdPos)
    if mnUserTany:
        n.add_char_here(elem, posx, posy, 1, charId)
        mnUserTany = 0
    else:
        newChange = n.add_char_here(elem, posx, posy)
        newChange['lastRcvdChnge'] = str(lastRcvdChnge)
        print(newChange)
        app.chngeBuffer.append(json.dumps(newChange))
        app.handle_wait()
        # cm.BroadCast(json.dumps(newChange))
    # print(n.charIdPos) RAGGA3
    # n.printList() RAGGA3


def on_insert(*args):
    # print("INS:", txt_edit.index(args[0]))
    indx1 = txt_edit.index(args[0])
    old_insert(*args)
    # print(txt_edit.index(args[0]))
    indx2 = txt_edit.index(args[0])
    btnaddchar(indx1, indx2)


def btndelchar(indx):
    global mnUserTany
    global charId
    global lastRcvdChnge

    # get position l cursor
    # print(txt_edit.index(tk.INSERT))
    x = indx

    posx = int(x.split('.')[0])
    posy = int(x.split('.')[1])
    # print(posx)
    # print(posy)

    # mfish fl del msh h3rf l elem
    # ind = str(posx) + '.' + str(posy)
    # print(txt_edit.get(ind))
    # elem = txt_edit.get(ind)

    # print(n.charIdPos) RAGGA3
    if mnUserTany:
        n.del_char_here(posx, posy, 1, charId)
        mnUserTany = 0
    else:
        newChange = n.del_char_here(posx, posy)
        newChange['lastRcvdChnge'] = str(lastRcvdChnge)
        print(newChange)
        app.chngeBuffer.append(json.dumps(newChange))
        app.handle_wait()
        # cm.BroadCast(json.dumps(newChange))
    # print(n.charIdPos) RAGGA3
    # n.printList()


def on_delete(*args):
    # print("DEL:", list(map(txt_edit.index, args)))
    indx = list(map(txt_edit.index, args))
    old_delete(*args)
    # print("hi, ", indx[0])
    # l index l tany indx[1]
    btndelchar(indx[0])
    # DOESN'T HANDLE MORE THAN ONE CHAR DEL YET. ALSO ADD CAN GET THE INDEX BUT NOT HANDLED


def btn13anthr():
    # n.add_char_here('h', 1, 0, 1, '500')
    receiveChange('h', None, None, '500')


def insertThere(pos, elem):
    txt_edit.insert(pos, elem)


def deleteThere(pos):
    txt_edit.delete(pos)


def deleteThereTest():
    txt_edit.delete('1.2')


lastChngeRcvdFromThisUsr = {}

sendAgainSent = {}
sendAgainCntr = {}

def changeOccured():
    global sendAgainSent
    global sendAgainCtr
    global lastChngeRcvdFromThisUsr
    global lastRcvdChnge
    while 1:
        change = cm.ws.recv()
        print(change)
        change = json.loads(change)
        if "delta" in change:  # and (chnge["freeze"] !="false"):
            senderIDD = "-1"
            if "senderID" in change:
                senderIDD = change["senderID"]
                print("LOOOK SENDER ID", senderIDD)
                if senderIDD in lastChngeRcvdFromThisUsr:
                    pass
                else:
                    # lastChngeRcvdFromThisUsr[senderIDD] = "-1"
                    lastChngeRcvdFromThisUsr[senderIDD] = []
                    lastChngeRcvdFromThisUsr[senderIDD].append("-1")

            change = change["delta"]
            if change == "sendText":
                print("GAAAAAAAAAAALYYYYYYYYYYYYYYYYYY SEEEEEEEEEEEEEEENNNNNDDDDDDDD TEEEEEEEEEXXXXXXXXXXTTTTTTTT")
                pass
            if change == "getDocument":
                pass
            if change == "None":
                pass
            # maza lw b -1???????????????????????? hb3t kollo
            if isinstance(change, str) and change.split()[0] == "sendAgain":
                print("REQUEST TO SEND AGAAAAIIIINNNN")
                print(change)
                print("sendAgain eh???? ", change.split()[1])
                delay = 500
                if change.split()[1].lstrip().rstrip() == "-1":
                    print("d5lt hna?")
                    for i in range(0, len(list(app.chngesBroadcastByMe))):
                        # for j in range(0, len(app.chngesBroadcastByMe[list(app.chngesBroadcastByMe)[i]])):
                        #     #app.chngeBuffer.append(app.chngesBroadcastByMe[list(app.chngesBroadcastByMe)[i]][j]) # JSON DUMPSSSSSSS????????
                        #     #print(app.chngeBuffer)
                        #
                        #     #cm.BroadCast(app.chngesBroadcastByMe[list(app.chngesBroadcastByMe)[i]])
                        app.after(delay, lambda x=i: cm.BroadCast(app.chngesBroadcastByMe[list(app.chngesBroadcastByMe)[x]]))
                        delay+=800
                        print("resending: ", app.chngesBroadcastByMe[list(app.chngesBroadcastByMe)[i]])
                else:
                    print("tyb hna?")
                    indOfLastChangeUserRcvd = list(app.chngesBroadcastByMe).index(change.split()[1].lstrip().rstrip())
                    print("last rcvd by that usr: ", indOfLastChangeUserRcvd)
                    for i in range(indOfLastChangeUserRcvd + 1, len(list(app.chngesBroadcastByMe))):
                        app.after(delay, lambda x=i: cm.BroadCast(app.chngesBroadcastByMe[list(app.chngesBroadcastByMe)[x]]))
                        delay+=800
                        print("resending: ", app.chngesBroadcastByMe[list(app.chngesBroadcastByMe)[i]])
                        # app.chngeBuffer.append(app.chngesBroadcastByMe[list(app.chngesBroadcastByMe)[i]]) # JSON DUMPSSSSSSS????????

            if isinstance(change, list):
                print("entered heeeeeeeeeere22")
                # EL AWL IF str(json.loads(change[-1])["lastBrdcstChnge"] AW str(json.loads(change[-1])["CHANGE_ID"] IN LIST str(lastChngeRcvdFromThisUsr[senderIDD]
                # THEN IGNORE ITS A CHANGE I IMPLEMENTED
                if str(json.loads(change[-1])["change_id"]).rstrip().lstrip() in lastChngeRcvdFromThisUsr[senderIDD]: #mmkn 2a check lw less than 2a5r 7aga 3mltha
                    print("3MLTHA 2BL KDA. IGNORE") # ignore l2enny 3mlto
                else:
                    if str(lastChngeRcvdFromThisUsr[senderIDD][-1]).rstrip().lstrip() != str(json.loads(change[-1])["lastBrdcstChnge"]).rstrip().lstrip():
                        print(lastChngeRcvdFromThisUsr[senderIDD], " ", json.loads(change[-1])["lastBrdcstChnge"])
                        print("ERRRORRRRRORRRRORRRR FI 7AGA MGTSH FL NOSSSS*****************")
                        # DONT CALL RECEIVE CHNGE
                        # EB3T MN AWL: MSG = str(lastChngeRcvdFromThisUsr[senderIDD][-1]).rstrip().lstrip()
                        msg = "sendAgain " + str(lastChngeRcvdFromThisUsr[senderIDD][-1]).rstrip().lstrip()

                        if senderIDD in sendAgainSent:
                            if sendAgainSent[senderIDD] == 3:
                                sendAgainSent[senderIDD] = 0
                                sendAgainCtr[senderIDD] = 'reset'
                        else:
                            sendAgainSent[senderIDD] = 0
                            sendAgainCtr[senderIDD] = 'reset'

                        if sendAgainCtr[senderIDD] == 'done':
                            sendAgainSent[senderIDD] += 1
                        else:
                            app.after(500, lambda j=msg: cm.BroadCast(j))
                            sendAgainSent[senderIDD] = 0
                            sendAgainCtr[senderIDD] = 'done'
                        #app.after(500, lambda j=msg: cm.BroadCast(j))
                        #sendAgainCtr[senderIDD] = 'done'


                    else:
                        print("MFIIIIIIIISHHHHH LOSSS")
                        sendAgainSent[senderIDD] = 0
                        sendAgainCtr[senderIDD] = 'reset'
                        # H3MML L CHANGE
                        lastChngeRcvdFromThisUsr[senderIDD].append(json.loads(change[-1])["change_id"])
                        print("LAST RCVD DICT: ", lastChngeRcvdFromThisUsr)

                        for chnge in change:
                            chnge = json.loads(chnge)

                            if "operation" in chnge:

                                # if chnge["operation"] == "ins" or chnge["operation"] == "del":
                                receiveChange(chnge["operation"],
                                              chnge["elem"],
                                              chnge["parent_id"] if chnge["parent_id"] == 'None' else float(chnge["parent_id"]),
                                              chnge["child_id"] if chnge["child_id"] == 'None' else float(chnge["child_id"]),
                                              float(chnge["my_id"]))
                                lastRcvdChnge = chnge["change_id"]
            else:
                print("entered heeeeeeeeeere")



def receiveChange(op, elem, parent_id, child_id, id):
    global mnUserTany
    global charId
    charId = id
    mnUserTany = 1

    if op == "ins":  # add not delete
        if child_id == 'None':
            if parent_id == 'None':
                # insertThere('1.0', elem)
                # insertThere(str('1')+'.'+str('0'), elem) # 25ALLY DI 1,0 34AN MSH HA HANDLEHA FL DELETE
                insertThere(str(len(n.charPosCharr) - 1) + '.' + str('0'), elem)
            else:
                parent_pos = n.charIdPos[parent_id]
                # parentposx = int(parent_pos.split('.')[0])
                # parentposy = int(parent_pos.split('.')[1])
                posy = parent_pos[1] + 1
                pos = str(parent_pos[0]) + '.' + str(posy)
                insertThere(pos, elem)
        else:
            child_pos = n.charIdPos[child_id]
            pos = str(child_pos[0]) + '.' + str(child_pos[1])
            insertThere(pos, elem)
    else:
        # don't need parent/child. only id
        # mmkn ml2ihush??? try except
        charDelPos = n.charIdPos[id]
        pos = str(charDelPos[0]) + '.' + str(charDelPos[1])
        deleteThere(pos)


def brdcstDct():
    brdcstDct = n.charPosCharr.copy()
    n.printList()

    for i in range(1, len(brdcstDct)):
        #WALLA 23ML COPY KDA KDA????
        # if len(n.charPosCharr[i]) > 0:
        brdcstDct[i] = n.charPosCharr[i].copy()
        for j in range(0, len(brdcstDct[i])):
            if brdcstDct[i][j] is not None:
                brdcstDct[i][j] = {
                                "elem": str(n.charPosCharr[i][j].elem),
                                "my_id": str(n.charPosCharr[i][j].my_id),
                                "parent_id": str(n.charPosCharr[i][j].parent_id),
                                "child_id": str(n.charPosCharr[i][j].child_id)
                            }
    print(brdcstDct)
    cm.BroadCast(brdcstDct)
    n.printList()
    # print(n.charPosCharr[1][2]['parent_id'])



# cm = ConnectionManager()
cm = connection_manager()

n = node.TextSeq()

window = tk.Tk()
window.title("Text Editor Application")
window.rowconfigure(0, minsize=800, weight=1)
window.columnconfigure(1, minsize=800, weight=1)

txt_edit = tk.Text(window, wrap="word", bg="light yellow")
fr_buttons = tk.Frame(window, relief=tk.RAISED, bd=2)
btn_open = tk.Button(fr_buttons, text="Open", command=open_file)
btn_save = tk.Button(fr_buttons, text="Save As...", command=save_file)
btn_1 = tk.Button(fr_buttons, text="Duplicate", command=btndplcte)
btn_2 = tk.Button(fr_buttons, text="Cursor", command=btn2crsr)
btn_3 = tk.Button(fr_buttons, text="Send All", command=btn3sndbtn)
btn_4 = tk.Button(fr_buttons, text="Connect", command=btn4cnct)
btn_5 = tk.Button(fr_buttons, text="Disconnect", command=btn5dscnct)
btn_7 = tk.Button(fr_buttons, text="Add This Char To Dict", command=btn7addchar)
btn_8 = tk.Button(fr_buttons, text="Add Mark for Cursor", command=btn8addmrk)
btn_9 = tk.Button(fr_buttons, text="Add Mark for Cursor2", command=btn9addmrk)
btn_10 = tk.Button(fr_buttons, text="Modified?", command=btn10chckmod)
btn_11 = tk.Button(fr_buttons, text="Consistency Prob?", command=btn11fixprob)
btn_12 = tk.Button(fr_buttons, text="Start writing", command=btn12strtwrtng)
btn_13 = tk.Button(fr_buttons, text="USER TANY 7T H", command=btn13anthr)
btn_14 = tk.Button(fr_buttons, text="delete pos 1.2", command=deleteThereTest)
btn_15 = tk.Button(fr_buttons, text="broadcast dict", command=brdcstDct)

btn_open.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
btn_save.grid(row=1, column=0, sticky="ew", padx=5)
btn_1.grid(row=2, column=0, sticky="ew", padx=5)
btn_2.grid(row=3, column=0, sticky="ew", padx=5)
btn_3.grid(row=4, column=0, sticky="ew", padx=5)
btn_4.grid(row=5, column=0, sticky="ew", padx=5)
btn_5.grid(row=6, column=0, sticky="ew", padx=5)
btn_7.grid(row=7, column=0, sticky="ew", padx=5)
btn_8.grid(row=8, column=0, sticky="ew", padx=5)
btn_9.grid(row=9, column=0, sticky="ew", padx=5)
btn_10.grid(row=10, column=0, sticky="ew", padx=5)
btn_11.grid(row=11, column=0, sticky="ew", padx=5)
btn_12.grid(row=12, column=0, sticky="ew", padx=5)
btn_13.grid(row=13, column=0, sticky="ew", padx=5)
btn_14.grid(row=14, column=0, sticky="ew", padx=5)
btn_15.grid(row=15, column=0, sticky="ew", padx=5)

# lw l text deleted cursor position????

fr_buttons.grid(row=0, column=0, sticky="ns")
txt_edit.grid(row=0, column=1, sticky="nsew")

redir = WidgetRedirector(txt_edit)
old_insert = redir.register("insert", on_insert)
old_delete = redir.register("delete", on_delete)

# NOT NOW DONT BIND
# txt_edit.bind("<KeyRelease>", btn6edted)

# txt_edit.bind("<KeyRelease>", btn10edted)

app = Application(window)
app.mainloop()