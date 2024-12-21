from flask import Flask, render_template, request, redirect, url_for
import random

app = Flask(__name__)

# Nastavenie hernej mriežky
GRID_SIZE = 8
EMPTY = "."
SANTA = "🎅"
GIFT = "🎁"
HOME = "🏠"
OBSTACLE = "❄"

# Inicializácia hernej mriežky a stav hry
grid = [[EMPTY for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
santa_pos = [0, 0]
grid[santa_pos[0]][santa_pos[1]] = SANTA
gift_count = 3

# Generovanie darčekov
for _ in range(gift_count):
    while True:
        x, y = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
        if grid[x][y] == EMPTY:
            grid[x][y] = GIFT
            break

# Generovanie cieľového domčeka
while True:
    x, y = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
    if grid[x][y] == EMPTY:
        grid[x][y] = HOME
        break

# Generovanie prekážok
for _ in range(5):
    while True:
        x, y = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
        if grid[x][y] == EMPTY:
            grid[x][y] = OBSTACLE
            break

@app.route("/")
def game():
    """Zobrazenie hernej mriežky."""
    return render_template("game.html", grid=grid, santa_pos=santa_pos, gift_count=gift_count)

@app.route("/move/<direction>")
def move(direction):
    """Spracovanie pohybu Santu."""
    global santa_pos, gift_count
    x, y = santa_pos

    # Zmažeme aktuálnu pozíciu Santu
    grid[x][y] = EMPTY

    # Výpočet novej pozície
    if direction == "up" and x > 0:
        x -= 1
    elif direction == "down" and x < GRID_SIZE - 1:
        x += 1
    elif direction == "left" and y > 0:
        y -= 1
    elif direction == "right" and y < GRID_SIZE - 1:
        y += 1

    # Správanie na novom políčku
    if grid[x][y] == GIFT:
        gift_count -= 1
    elif grid[x][y] == OBSTACLE:
        return "Narazil si na ❄! Hra končí."
    elif grid[x][y] == HOME:
        if gift_count == 0:
            return "Vyhral si! 🎉"
        return "Najprv nazbieraj všetky darčeky 🎁."

    # Aktualizácia pozície Santu
    santa_pos = [x, y]
    grid[x][y] = SANTA

    return redirect(url_for("game"))

if __name__ == "__main__":
    app.run(debug=True)