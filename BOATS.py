from tkinter import *
from PIL import Image, ImageTk
import random as rn


def generate_board(height, width, c, f, s, t, origin):  # carrier(5), fighter(4), sub(3), torpedo(2)
    board = []
    score = 0

    try:
        c = int(c)
    except ValueError:
        c = 0
    try:
        f = int(f)
    except ValueError:
        f = 0
    try:
        s = int(s)
    except ValueError:
        s = 0
    try:
        t = int(t)
    except ValueError:
        t = 0

    for i in range(height):
        board.append(['-']*width)
    for i in range(c):
        ort = rn.choice(['hor', 'ver'])
        if ort == 'hor':
            score += 5*place_hor(board, height, width, 5, 'C', origin)
        elif ort == 'ver':
            score += 5*place_ver(board, height, width, 5, 'C', origin)
    for i in range(f):
        ort = rn.choice(['hor', 'ver'])
        if ort == 'hor':
            score += 4*place_hor(board, height, width, 4, 'F', origin)
        elif ort == 'ver':
            score += 4*place_ver(board, height, width, 4, 'F', origin)
    for i in range(s):
        ort = rn.choice(['hor', 'ver'])
        if ort == 'hor':
            score += 3*place_hor(board, height, width, 3, 'S', origin)
        elif ort == 'ver':
            score += 3*place_ver(board, height, width, 3, 'S', origin)
    for i in range(t):
        ort = rn.choice(['hor', 'ver'])
        if ort == 'hor':
            score += 2*place_hor(board, height, width, 2, 'T', origin)
        elif ort == 'ver':
            score += 2*place_ver(board, height, width, 2, 'T', origin)
    return board, int(score)


def place_hor(board, height, width, length, typ, origin):
    global my_boats_list
    x, y = find_spot_hor(board, height, width, length)
    if x is False:
        return 0
    else:
        near = 'o'
        for i in range(length):
            board[y][x+i] = typ

        if origin == 'me':
            my_boats_list.append([typ, 'hor', x, y])

        if x != 0 and y != 0:  # lavy horny
            board[y][x-1] = near
            for i in range(length+1):
                board[y-1][x-1+i] = near
        if x+length != width and y != 0:  # pravy horny
            board[y][x+length] = near
            for i in range(length+1):
                board[y-1][x+i] = near
        if x != 0 and y != height-1:  # lavy dolny
            board[y][x-1] = near
            for i in range(length+1):
                board[y+1][x-1+i] = near
        if x+length != width and y != height-1:  # pravy dolny
            board[y][x+length] = near
            for i in range(length+1):
                board[y+1][x+i] = near
        return 1


def place_ver(board, height, width, length, typ, origin):
    global my_boats_list
    x, y = find_spot_ver(board, height, width, length)
    if x is False:
        return 0
    else:
        near = 'o'
        for i in range(length):
            board[y+i][x] = typ

        if origin == 'me':
            my_boats_list.append([typ, 'ver', x, y])

        if x != 0 and y != 0:  # lavy horny
            board[y-1][x] = near
            for i in range(length+1):
                board[y-1+i][x-1] = near
        if x != width-1 and y != 0:  # pravy horny
            board[y-1][x] = near
            for i in range(length+1):
                board[y-1+i][x+1] = near
        if x != 0 and y+length != height:  # lavy dolny
            board[y+length][x] = near
            for i in range(length+1):
                board[y+i][x-1] = near
        if x != width-1 and y+length != height:  # pravy dolny
            board[y+length][x] = near
            for i in range(length+1):
                board[y+i][x+1] = near
        return 1


def find_spot_hor(board, height, width, length):
    count = 0
    while count < 200:
        isgood = True
        x = rn.randint(0, width-length)
        y = rn.randint(0, height-1)
        for i in range(length):  # x-posun
            if board[y][x+i] == 'o' or board[y][x+i] == 'C' or board[y][x+i] == 'F' or board[y][x+i] == 'S' or board[y][x+i] == 'T':
                isgood = False
                count += 1
        if isgood is True:
            return x, y
    return False, False


def find_spot_ver(board, height, width, length):
    count = 0
    while count < 200:
        isgood = True
        x = rn.randint(0, width-1)
        y = rn.randint(0, height-length)
        for i in range(length):  # y-posun
            if board[y+i][x] == 'o' or board[y+i][x] == 'C' or board[y+i][x] == 'F' or board[y+i][x] == 'S' or board[y+i][x] == 'T':
                isgood = False
                count += 1
        if isgood is True:
            return x, y
    return False, False


def draw_boat(boat_list):  # vykreslenie lodi zo zoznamu
    boats_img = Image.new('RGBA', (50 * 10, 50 * 10))
    for info in boat_list:
        if info[0] == 'C':
            img = Image.open('my_files/carrier.png')
        elif info[0] == 'F':
            img = Image.open('my_files/fighter.png')
        elif info[0] == 'S':
            img = Image.open('my_files/submarine.png')
        else:
            img = Image.open('my_files/torpedo.png')
        if info[1] == 'ver':
            img = img.rotate(270, expand=True)
        boats_img.paste(img, (50 * int(info[2]), 50 * int(info[3])))
    return ImageTk.PhotoImage(boats_img)


def rules():
    title_background.pack_forget()
    rules_button.place_forget()
    start_button.place_forget()
    rules_txt.pack(expand=1, fill=Y)
    back_button.place(x=root.winfo_width()//2, y=root.winfo_width()-15, anchor=CENTER)

    with open('rules.txt', 'r', encoding='utf-8') as f1:
        rules_txt.config(text=f1.read())


def back():
    rules_txt.pack_forget()
    back_button.place_forget()

    title_background.pack()
    rules_button.place(x=widnow_x // 2 + 90, y=window_y // 4, height=35)
    start_button.place(x=widnow_x // 2, y=window_y // 4, height=35)


def start():
    global my_board_img
    maxx, maxy = 570, 570
    root.geometry(f'{maxx}x{maxy+200}')

    title_background.pack_forget()
    rules_button.pack_forget()
    start_button.pack_forget()

    platno.pack()
    radnomize_boats.place(x=10, y=maxy+160, width=165, height=30)

    C_label.place(x=10, y=maxy, width=100, height=30)
    C_entry.place(x=10+100+5, y=maxy, width=60, height=30)

    F_label.place(x=10, y=maxy+40, width=100, height=30)
    F_entry.place(x=10+100+5, y=maxy+40, width=60, height=30)

    S_label.place(x=10, y=maxy+80, width=100, height=30)
    S_entry.place(x=10+100+5, y=maxy+80, width=60, height=30)

    T_label.place(x=10, y=maxy+120, width=100, height=30)
    T_entry.place(x=10+100+5, y=maxy+120, width=60, height=30)

    P_label.place(x=10+165+10, y=maxy, width=200, height=30)
    P_text_entry.place(x=10+165+10, y=maxy+40, width=200, height=110)
    P_button.place(x=10+165+10, y=maxy+160, width=200, height=30)
    example = 'C ver D 8\nF hor G 0\nS ver G 5\nS hor B 4\nT ver B 0'
    P_text_entry.delete(1.0, 'end')
    P_text_entry.insert(1.0, example)

    start_game_button.place(x=10+165+10+200+10, y=maxy, width=165, height=190)

    platno.create_image(10, 10, image=my_board_img, anchor=NW)
    my_score_display.place(x=10+25, y=10+25, anchor=CENTER)
    my_score_display.config(text=my_score)


def random_boats():
    global my_board, my_score, opponent_board, opponent_score, my_boats_list, my_board_img, my_boats_img
    my_boats_list = []
    platno.delete('all')

    my_board, my_score = generate_board(10, 10, C_entry.get(), F_entry.get(), S_entry.get(), T_entry.get(), 'me')
    opponent_board, opponent_score = generate_board(10, 10, C_entry.get(), F_entry.get(), S_entry.get(), T_entry.get(), 'opponent')

    platno.create_image(10, 10, image=my_board_img, anchor=NW)

    my_boats_img = draw_boat(my_boats_list)
    platno.create_image(10+50, 10+50, image=my_boats_img, anchor=NW)

    my_score_display.config(text=my_score)


def place_boats():
    global my_board, my_score, my_boats_list, my_board_img, my_boats_img, my_score, opponent_score, my_board, opponent_board
    platno.delete('all')

    platno.create_image(10, 10, image=my_board_img, anchor=NW)

    my_boats_list = list(P_text_entry.get(1.0, END).strip())
    while True:
        try:
            my_boats_list.remove(' ')
        except ValueError:
            try:
                my_boats_list.remove('\n')
            except ValueError:
                break
    for i in range(int(len(my_boats_list)/6)):
        try:
            new_boat = [my_boats_list[0], f'{my_boats_list[1]}{my_boats_list[2]}{my_boats_list[3]}', int(my_boats_list[5]),
                        int(ord(my_boats_list[4])-65)]
            my_boats_list[:6] = ''
            my_boats_list.append(new_boat)
        except ValueError:
            pass

    my_board = []
    for i in range(10):
        my_board.append(['-']*10)

    def place(lenght, typ, array, board):
        global my_boats_list
        try:
            x_start, x_end, y_start, y_end = 0, 0, 0, 0
            y = int(array[3])
            x = int(array[2])
            if array[1] == 'hor':  # horizontalne
                if x == 0:
                    x_start = 0
                    x_end = x+lenght
                elif x+lenght == 9:
                    x_start = x-1
                    x_end = 9
                else:
                    x_start = x-1
                    x_end = x+lenght
                if y == 0:
                    y_start = 0
                    y_end = y+1
                elif y == 9:
                    y_start = y-1
                    y_end = y
                else:
                    y_start = y-1
                    y_end = y+1
                for j in range(x_start, x_end+1):
                    for k in range(y_start, y_end+1):
                        if board[k][j] != '-':
                            my_boats_list[my_boats_list.index(array)] = []
                            return board
                for j in range(lenght):
                    board[y][x+j] = typ
            else:  # vertikalne
                if x == 0:
                    x_start = 0
                    x_end = x+1
                elif x == 9:
                    x_start = x-1
                    x_end = x
                else:
                    x_start = x-1
                    x_end = x+1
                if y == 0:
                    y_start = 0
                    y_end = y+lenght
                elif y+lenght == 9:
                    y_start = y-1
                    y_end = 9
                else:
                    y_start = y-1
                    y_end = y+lenght
                for j in range(x_start, x_end+1):
                    for k in range(y_start, y_end+1):
                        if board[k][j] != '-':
                            my_boats_list[my_boats_list.index(array)] = []
                            return board
                for j in range(lenght):
                    board[y+j][x] = typ
        except IndexError:
            my_boats_list[my_boats_list.index(array)] = []
        return board

    c, f, s, t = 0, 0, 0, 0
    my_score = 0

    for boat in my_boats_list:
        if boat[0] == 'C':
            my_board = place(5, 'C', boat, my_board)
        elif boat[0] == 'F':
            my_board = place(4, 'F', boat, my_board)
        elif boat[0] == 'S':
            my_board = place(3, 'S', boat, my_board)
        else:
            my_board = place(2, 'T', boat, my_board)

    while 1:
        try:
            my_boats_list.remove(my_boats_list[my_boats_list.index([])])
        except ValueError:
            break

    for boat in my_boats_list:
        if boat[0] == 'C':
            my_score += 5
            c += 1
        elif boat[0] == 'F':
            my_score += 4
            f += 1
        elif boat[0] == 'S':
            my_score += 3
            s += 1
        else:
            my_score += 2
            t += 1

    opponent_board, opponent_score = generate_board(10, 10, c, f, s, t, 'opponent')
    my_boats_img = draw_boat(my_boats_list)
    platno.create_image(10+50, 10+50, image=my_boats_img, anchor=NW)
    my_score_display.config(text=my_score)


def start_game():
    global my_board_img, opponent_board_img, my_score, opponent_score, my_boats_list, my_boats_img, ai_cords
    if my_score == 0:
        return
    ai_cords = []
    for i in range(10):
        for j in range(10):
            ai_cords.append(f'{i}{j}')
    rn.shuffle(ai_cords)
    maxx = 570*2
    maxy = 570
    root.geometry(f'{maxx}x{maxy+30}')
    platno.delete('all')

    platno.config(width=maxx)

    radnomize_boats.place_forget()
    C_label.place_forget()
    C_entry.place_forget()
    F_label.place_forget()
    F_entry.place_forget()
    S_label.place_forget()
    S_entry.place_forget()
    T_label.place_forget()
    T_entry.place_forget()
    P_label.place_forget()
    P_text_entry.place_forget()
    P_button.place_forget()
    start_game_button.place_forget()

    shots_input.place(x=maxx/2, y=maxy+10, height=30, width=160, anchor=CENTER)

    reset_button.place(x=10+80, y=maxy+10, height=30, width=160, anchor=CENTER)

    platno.create_image(10, 10, image=opponent_board_img, anchor=NW)
    platno.create_image(maxx/2+10, 10, image=my_board_img, anchor=NW)

    opponent_score_display.place(x=10+25, y=10+25, anchor=CENTER)
    my_score_display.place(x=maxx/2+10+25, y=10+25, anchor=CENTER)

    opponent_score_display.config(text=opponent_score)
    my_score_display.config(text=my_score)

    my_boats_img = draw_boat(my_boats_list)
    platno.create_image(maxx/2+60, 10+50, image=my_boats_img, anchor=NW)


def win_lose():
    global my_score, opponent_score, img_tk
    my_score_display.place_forget()
    opponent_score_display.place_forget()
    shots_input.place_forget()

    root.geometry('570x570')
    platno.delete('all')
    platno.config(bg='black')
    reset_button.place(x=570/2, y=570-50, height=30, anchor=CENTER)

    if opponent_score <= 0:
        img = Image.open('my_files/you_win.png')
        img_tk = ImageTk.PhotoImage(img)
    else:
        img = Image.open('my_files/you_lose.png')
    img_tk = ImageTk.PhotoImage(img)
    platno.create_image(570/2, 570/2, image=img_tk, anchor=CENTER)


def my_move(self):
    global opponent_board, opponent_score, my_score, my_board_shots, opponent_transparent
    try:
        if ord(shots_input.get()[0]) > 75:
            y = ord(shots_input.get()[0])-97
        else:
            y = ord(shots_input.get()[0])-65
        x = int(shots_input.get()[1])
    except ValueError:
        shots_input.delete(0, 'end')
    except IndexError:
        pass
    else:
        shots_input.delete(0, 'end')
        if opponent_board[y][x] == 'a':
            return False
        else:
            if opponent_board[y][x] == '-' or opponent_board[y][x] == 'o':
                opponent_board[y][x] = 'a'
                result = False
            else:
                result = True
                opponent_score -= 1

            if result is False:
                img = Image.open('opponent_files/MISS.png')
            else:
                img = Image.open('opponent_files/HIT.png')
            opponent_transparent.paste(img, (50 * x, 50 * y))
            my_board_shots = ImageTk.PhotoImage(opponent_transparent)
            platno.create_image(60, 60, anchor=NW, image=my_board_shots)
            opponent_score_display.configure(text=opponent_score)
        if result is False:
            ai()

        if my_score == 0 or opponent_score == 0:
            platno.update()
            platno.after(1000)
            win_lose()


def ai():
    global my_board, my_score, opponent_board_shots, my_transparent, ai_cords, hit_cords, hit_counter, boat_hp, past_shot, orientation
    result = True
    while result is True:
        platno.update()
        platno.after(500)

        if boat_hp == 0:  # reset po zniceni
            hit_counter = 0
            hit_cords = []
            past_shot = ''
            boat_hp = -1

        if hit_counter == 0:  # nahodne strielanie
            x, y = int(str(ai_cords[0])[0]), int(str(ai_cords[0])[1])
            ai_cords.remove(ai_cords[0])

            if my_board[y][x] == '-' or my_board[y][x] == 'o':
                result = False
            else:
                result = True
                my_score -= 1

                past_shot = f'{x}{y}'

                hit_counter = 1
                hit_cords = []
                if x != 0:
                    if x == 1:  # vlavo
                        hit_cords.append(f'0{y}')
                    else:
                        hit_cords.append(f'{x-1}{y}')
                if x != 9:  # vpravo
                    hit_cords.append(f'{x+1}{y}')
                if y != 0:  # hore
                    hit_cords.append(f'{x}{y-1}')
                if y != 9:  # dolu
                    hit_cords.append(f'{x}{y+1}')

                for i in range(len(hit_cords)):
                    if hit_cords[i] not in ai_cords:
                        hit_cords[i] = []
                while 1:
                    try:
                        hit_cords.remove(hit_cords[hit_cords.index([])])
                    except ValueError:
                        break

                if my_board[y][x] == 'C':
                    boat_hp = 4
                elif my_board[y][x] == 'F':
                    boat_hp = 3
                elif my_board[y][x] == 'S':
                    boat_hp = 2
                else:
                    boat_hp = 1

        elif hit_counter == 1:  # strielanie okolo miesta posledneho zasahu
            x, y = int(str(hit_cords[0])[0]), int(str(hit_cords[0])[1])
            ai_cords.remove(ai_cords[ai_cords.index(hit_cords[0])])
            hit_cords.remove(hit_cords[0])

            if my_board[y][x] == '-' or my_board[y][x] == 'o':
                result = False
            else:
                result = True
                my_score -= 1
                hit_counter = 2
                boat_hp -= 1

                if x == int(past_shot[0]):  # otocena vertikalne
                    hit_cords = []
                    for i in range(1, boat_hp+2):
                        y1 = y+i*(-1)**(i+1)
                        y2 = y+i*(-1)**i

                        hit_cords.append(f'{x}{y1}')
                        hit_cords.append(f'{x}{y2}')
                    orientation = 'ver'

                else:  # otocena horizontalne
                    hit_cords = []
                    for i in range(1, boat_hp+3):
                        x1 = x+i*(-1)**(i+1)
                        x2 = x+i*(-1)**i

                        hit_cords.append(f'{x1}{y}')
                        hit_cords.append(f'{x2}{y}')
                    orientation = 'hor'

                for i in range(len(hit_cords)):
                    if hit_cords[i] not in ai_cords:
                        hit_cords[i] = []
                while 1:
                    try:
                        hit_cords.remove(hit_cords[hit_cords.index([])])
                    except ValueError:
                        break

                past_shot = f'{x}{y}'

        else:  # strielanie v smere orientacie lode
            x, y = int(str(hit_cords[0])[0]), int(str(hit_cords[0])[1])
            ai_cords.remove(ai_cords[ai_cords.index(hit_cords[0])])
            hit_cords.remove(hit_cords[0])

            if my_board[y][x] == '-' or my_board[y][x] == 'o':
                result = False

                hit_cords = []
                if orientation == 'ver':
                    if y > int(past_shot):  # smerom nahor
                        for i in range(y, 0-1, -1):
                            hit_cords.append(f'{x}{i}')
                    else:  # smerom nadol
                        for i in range(y, 10):
                            hit_cords.append(f'{x}{i}')
                elif orientation == 'hor':
                    if x > int(past_shot):  # smerom vlavo
                        for i in range(x, 0-1, -1):
                            hit_cords.append(f'{i}{y}')
                    else:  # smerom vpravo
                        for i in range(x, 10):
                            hit_cords.append(f'{i}{y}')

                for i in range(len(hit_cords)):
                    if hit_cords[i] not in ai_cords:
                        hit_cords[i] = []
                while 1:
                    try:
                        hit_cords.remove(hit_cords[hit_cords.index([])])
                    except ValueError:
                        break

            else:
                result = True
                my_score -= 1
                boat_hp -= 1

        if result is False:
            img = Image.open('opponent_files/MISS.png')
        else:
            img = Image.open('opponent_files/HIT2.png')

        my_transparent.paste(img, (50 * x, 50 * y))
        opponent_board_shots = ImageTk.PhotoImage(my_transparent)
        platno.create_image(platno.winfo_width()/2+60, 60, anchor=NW, image=opponent_board_shots)
        my_score_display.configure(text=my_score)


def reset():
    global my_transparent, opponent_transparent, my_score, opponent_score
    platno.delete('all')
    my_score, opponent_score = 0, 0
    my_transparent = Image.new('RGBA', (50 * 10, 50 * 10))
    opponent_transparent = Image.new('RGBA', (50 * 10, 50 * 10))
    shots_input.place_forget()
    reset_button.place_forget()
    root.config(bg='#2e2e2e')
    platno.config(bg='#2e2e2e')
    start()


# nastavenie premennych
widnow_x = 570
window_y = 570

my_boats_list = []
my_board, my_score = [], 0
opponent_board, opponent_score = [], 0

ai_cords = []
hit_counter = 0
hit_cords = []
past_shot = 0
boat_hp = -1
orientation = 'hor'

root = Tk()
root.title('BOATS')
root.resizable(False, False)
root.iconphoto(True, PhotoImage(file='art_work/logo.png'))
root.geometry(f'{widnow_x}x{window_y}')
root.configure(bg='#2e2e2e')

root.bind('<Return>', my_move)

title_img_tk = PhotoImage(file='art_work/title_screen.png')
title_background = Label(root, width=widnow_x, height=window_y, bg='white', image=title_img_tk)
title_background.pack()
rules_button = Button(root, font=('Arial', 17), bg='white', anchor=CENTER, text='RULES', cursor='hand2', relief='groove', command=rules)
rules_button.place(x=widnow_x // 2 + 90, y=window_y // 4, height=35)
start_button = Button(root, font=('Arial', 17), bg='white', anchor=CENTER, text='START', cursor='hand2', relief='groove', command=start)
start_button.place(x=widnow_x // 2, y=window_y // 4, height=35)

rules_txt = Label(root, width=570, font=('Arial', 14), bg='white', text='', fg='black')
rules_txt.pack_forget()

back_button = Button(root, font=('Arial', 11, 'bold'), bg='white', width=30, text='OK', cursor='hand2', relief='groove', command=back)
back_button.place_forget()

platno = Canvas(root, height=window_y, width=window_y, bg='#2e2e2e', highlightthickness=0)
platno.pack_forget()

radnomize_boats = Button(root, font=('Arial', 11), bg='white', text='RANDOMIZE', cursor='hand2', relief='groove', command=random_boats)
radnomize_boats.pack_forget()

C_label = Label(root, font=('Arial', 11), bg='white', anchor=CENTER, text='Počet C(5):')
C_label.place_forget()
C_entry = Entry(root, font=('Arial', 11), bg='white', textvariable=IntVar())
C_entry.place_forget()

F_label = Label(root, font=('Arial', 11), bg='white', anchor=CENTER, text='Počet F(4):')
F_label.place_forget()
F_entry = Entry(root, font=('Arial', 11), bg='white', textvariable=IntVar())
F_entry.place_forget()

S_label = Label(root, font=('Arial', 11), bg='white', anchor=CENTER, text='Počet S(3):')
S_label.place_forget()
S_entry = Entry(root, font=('Arial', 11), bg='white', textvariable=IntVar())
S_entry.place_forget()

T_label = Label(root, font=('Arial', 11), bg='white', anchor=CENTER, text='Počet T(2):')
T_label.place_forget()
T_entry = Entry(root, font=('Arial', 11), bg='white', textvariable=IntVar())
T_entry.place_forget()

P_label = Label(root, font=('Arial', 11), bg='white', anchor=CENTER, text='Manuálne umiestnenie lodí:')
P_label.place_forget()
P_text_entry = Text(root, font=('Arial', 11), bg='white')
P_text_entry.place_forget()
P_button = Button(root, font=('Arial', 11), bg='white', text='PLACE', cursor='hand2', relief='groove', command=place_boats)
P_button.place_forget()

start_game_button = Button(root, font=('Arial', 15, 'bold'), bg='red', fg='#2e2e2e', text='START', justify='center', cursor='hand2', relief='groove', command=start_game)
start_game_button.place_forget()

# zobrazenie skore
opponent_score_display = Label(platno, font=('Arial', 15), text=opponent_score, fg='#37ff05', bg='black')
opponent_score_display.place_forget()

my_score_display = Label(platno, font=('Arial', 15), text=my_score, fg='#269ed2', bg='black')
my_score_display.place_forget()

shots_input = Entry(root, font=('Arial', 20), bg='#2e2e2e', fg='#37ff05', justify=CENTER)
shots_input.place_forget()

reset_button = Button(root, font=('Arial', 15, 'bold'), bg='black', fg='white', text='RESET', justify='center', cursor='hand2', relief='groove', command=reset)
reset_button.place_forget()

# obraz mojej hracej plochy
board_img = Image.new('RGB', (50 * 11, 50 * 11))
img1 = Image.open('my_files/frame2.png')
board_img.paste(img1, (0, 0))
for m in range(10):
    img1 = Image.open(f'my_files/{m}.png')
    board_img.paste(img1, (50 * (m + 1), 0))
for m in range(10):
    img1 = Image.open(f'my_files/{chr(65+m)}.png')
    board_img.paste(img1, (0, 50 * (m + 1)))
    for n in range(10):
        img1 = Image.open('my_files/frame.png')
        board_img.paste(img1, (50 * (n + 1), 50 * (m + 1)))
my_board_img = ImageTk.PhotoImage(board_img)

# obraz superovej hracej plochy
board_img = Image.new('RGB', (50 * 11, 50 * 11))
img1 = Image.open('opponent_files/frame2.png')
board_img.paste(img1.resize((50, 50)), (0, 0))
for m in range(10):
    img1 = Image.open(f'opponent_files/{m}.png')
    board_img.paste(img1, (50 * (m + 1), 0))
for m in range(10):
    img1 = Image.open(f'opponent_files/{chr(65+m)}.png')
    board_img.paste(img1, (0, 50 * (m + 1)))
    for n in range(10):
        img1 = Image.open('opponent_files/frame2.png')
        board_img.paste(img1, (50 * (n + 1), 50 * (m + 1)))
opponent_board_img = ImageTk.PhotoImage(board_img)

# obrazy na vykreslenie strelby
my_transparent = Image.new('RGBA', (50 * 10, 50 * 10))
opponent_transparent = Image.new('RGBA', (50 * 10, 50 * 10))

root.mainloop()
