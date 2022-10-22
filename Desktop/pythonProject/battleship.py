import tkinter as tk
import random
import time

height = 10
width = 10
cell = 40

cell2 = [[0 for row in range(height)] for col in range(width)]
messages = ["Fire", "You failed", "You damaged the ship", "The ship sunk", "You won!"]
name_ships = ["Black Pearl", "Flying Dutchman", "Interceptor", "Empress", "Troubadour"]
symbol = ["B", "F", "I", "Em", "T"]
length_ships = [5, 4, 3, 2, 1]
number_ships = [1, 1, 3, 3, 2]
ships = [[nm, lg, nb, sy] for nm, lg, nb, sy in zip(name_ships, length_ships, number_ships, symbol)]



def click_grid(event):
    global case
    case = canvas2.find_closest(event.x, event.y)[0]
    if case not in played_list:
        played_list.append(case)
        root.after(1000, fire)


def init_grid():
    grid = [["E" for i in range(10)] for j in range(10)]
    return grid


def initgrid_attempts():
    grid = [['_' for i in range(10)] for j in range(10)]
    return grid


def place_shiph(row, col, lg, grid, symbol):
    shipin_place = True
    if col+lg > 10:
            shipin_place = False
    else:
        for count in range(lg):
            if grid[row][col+count] != "E":
                shipin_place = False
    if shipin_place:
        for count in range(lg):
            grid[row][col+count] = symbol
    return shipin_place


def place_shipv(row, col, lg, grid, symbol):
    shipin_place = True
    if row+lg > 10:
            shipin_place = False
    else:
        for count in range(lg):
            if grid[row+count][col] != "E":
                shipin_place = False
    if shipin_place:
        for count in range(lg):
            grid[row+count][col] = symbol
    return shipin_place


def ship_location(lg, grid, symbol):
    indicel = random.randint(0, 9)
    indicec = random.randint(0, 9)
    pos_hor = random.randint(0, 1)
    if pos_hor == 0:
        shipin_place = place_shiph(indicel, indicec, lg, grid, symbol)
    else:
        shipin_place = place_shipv(indicel, indicec, lg, grid, symbol)
    return shipin_place


def grid_ships():
    global ships, grid, grid_attempts
    grid = init_grid()
    grid_attempts = initgrid_attempts()
    dic_ships = {}
    for ship in ships:
        for nb in range(ship[2]):
            shipin_place = False
            while not shipin_place:
                    shipin_place = ship_location(ship[1], grid, ship[3] + str(nb))
                    dic_ships[ship[3] + str(nb)] = ship[1]
    return dic_ships


def reset_lbl():
    global lbl
    lbl.configure(text=messages[0])


def winner():
    global end_time
    end_time = time.time()
    lbl.configure(text=messages[4])


def fire():
    global dic_ships, remaining_ships, lbl, frame, grid
    y = (case - 1) // 10
    x = (case - 1) % 10
    target = grid[x][y]
    if target == "E":
        lbl.configure(text=messages[1])
        coul = "blue"
    else:
        dic_ships[target] -= 1
        if dic_ships[target] > 0:
            lbl.configure(text=messages[2])
        else:
            lbl.configure(text=messages[3])
            remaining_ships -= 1
            lbl2.configure(text=str(remaining_ships) + " ships left")
        coul = "black"
    canvas2.itemconfig(cell2[x][y], fill=coul)
    if remaining_ships == 0:
        root.after(1000, winner)
    else:
        root.after(1000, reset_lbl)


def game():
    global dic_ships, played_list, start_time, remaining_ships, lbl2
    for y in range(height):
        for x in range(width):
            canvas2.itemconfig(cell2[x][y], fill="white")
    reset_lbl()
    remaining_ships = sum(number_ships)
    lbl2.configure(text="There are " + str(remaining_ships) + " ships")
    played_list = [0]
    dic_ships = grid_ships()


root = tk.Tk()
root.title("Battleship")
frame = tk.Frame(root)
frame.pack(side=tk.TOP)
lbl = tk.Label(frame, text=messages[0], font="Sylfean 18")
lbl.pack(side=tk.TOP)
frame2 = tk.Frame(root)
frame2.pack()
canvas2 = tk.Canvas(frame2, width=cell * width, height=cell * height, highlightthickness=0)
canvas2.pack()
for y in range(height):
    for x in range(width):
        cell2[x][y] = canvas2.create_rectangle((x * cell, y * cell, (x + 1) * cell, (y + 1) * cell), outline="black",
                                               fill="white")

canvas2.bind("<Button-1>", click_grid)
lbl2 = tk.Label(frame, text='', font="Sylfean 18")
lbl2.pack(side=tk.BOTTOM)
game()
root.mainloop()