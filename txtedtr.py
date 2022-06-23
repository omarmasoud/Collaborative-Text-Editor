import tkinter as tk
from threading import Thread
from tkinter.filedialog import askopenfilename, asksaveasfilename
from idlelib.redirector import WidgetRedirector

from ConnectionManager import *

import node

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
    x=txt_edit.index(tk.INSERT)

    txt11 = txt_edit.get(1.0, "end-1c")
    txt_edit.delete(1.0, tk.END)
    txt_edit.insert(tk.END, txt11)

    print(x.split('.')[0])
    print(x.split('.')[1])
    txt_edit.mark_set("insert", "%d.%d" % (int(x.split('.')[0]), int(x.split('.')[1])))







def btn2crsr():
    print(txt_edit.index(tk.INSERT))
    txt_edit.mark_set("insert", "%d.%d" % (1,2))


def btn3sndbtn():
    print(txt_edit.get(1.0, "end-1c"))
    print('hi')
    txt_msg = txt_edit.get(1.0, "end-1c")
    cm.SendMsg(txt_msg)

def btn4cnct():
    cm.Connect()
    Thread(target=changeOccured).start()


def btn5dscnct():
    cm.Disconnect()

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
    if len(arr)>1:
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



            #23mlha marra w7da
            #disable lw new line
            #mayb blink l button
            #another thing what id 3ml new line w kammel?
            #lw 3ml new line. disable w 2ollo updating wait w h3mlha mn nfsy ana



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

def btnaddchar(indx1, indx2):
    global mnUserTany
    global charId
    # get position l cursor
    #print(txt_edit.index(tk.INSERT))
    x = indx1

    posx = int(x.split('.')[0])
    posy = int(x.split('.')[1])
    print(posx)
    print(posy)

    ind = str(posx) + '.' + str(posy)
    print(txt_edit.get(ind))
    elem = txt_edit.get(ind)

    print(n.charIdPos)
    if mnUserTany:
        n.add_char_here(elem, posx, posy, 1, charId)
        mnUserTany = 0
    else:
        newChange = n.add_char_here(elem, posx, posy)
        print(newChange)
        cm.SendMsg(newChange)
    print(n.charIdPos)
    n.printList()



def on_insert(*args):
    print ("INS:", txt_edit.index(args[0]))
    indx1 = txt_edit.index(args[0])
    old_insert(*args)
    print(txt_edit.index(args[0]))
    indx2 = txt_edit.index(args[0])
    btnaddchar(indx1, indx2)

def on_delete(*args):
    print ("DEL:", list(map(txt_edit.index, args)))
    old_delete(*args)


def btn13anthr():
    # n.add_char_here('h', 1, 0, 1, '500')
    receiveChange('h', None, None, '500')


def insertThere(pos, elem):
    txt_edit.insert(pos, elem)

def changeOccured():
    while 1:
        chnge = cm.ReceiveMsg()
        if chnge is not None:
            print(chnge)
            if len(chnge.split('&')) == 5:
                receiveChange(chnge.split('&')[1],
                              chnge.split('&')[2] if chnge.split('&')[2] == 'None' else float(chnge.split('&')[2]),
                              chnge.split('&')[3] if chnge.split('&')[3] == 'None' else float(chnge.split('&')[3]),
                              float(chnge.split('&')[4]))


def receiveChange(elem, parent_id, child_id, id):
    global mnUserTany
    global charId
    charId = id
    mnUserTany = 1

    if child_id == 'None':
        if parent_id == 'None':
            # insertThere('1.0', elem)
            insertThere(str(len(n.charPosCharr)-1)+'.'+str('0'), elem)
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




cm = ConnectionManager()

n = node.TextSeq()

window = tk.Tk()
window.title("Text Editor Application")
window.rowconfigure(0, minsize=800, weight=1)
window.columnconfigure(1, minsize=800, weight=1)

txt_edit = tk.Text(window, wrap="word", bg = "light yellow")
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

#lw l text deleted cursor position????

fr_buttons.grid(row=0, column=0, sticky="ns")
txt_edit.grid(row=0, column=1, sticky="nsew")


redir = WidgetRedirector(txt_edit)
old_insert=redir.register("insert", on_insert)
old_delete=redir.register("delete", on_delete)


# NOT NOW DONT BIND
# txt_edit.bind("<KeyRelease>", btn6edted)

# txt_edit.bind("<KeyRelease>", btn10edted)

window.mainloop()