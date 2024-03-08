# ==== Importing all necessary libraries
from tkinter import *
import random
import sqlite3
from itertools import cycle
from tkinter import simpledialog
# ==== creating main class
class Play_2048(Tk):

    # ==== adding necessary class variables
    game_board = []
    new_random_tiles = [2, 2, 2, 2, 2, 2, 4]
    score = 0
    high_score = 0
    game_score = 0
    highest_score = 0
    username = ""
    counter=0


    # ==== creating user window
    def __init__(self, *args, **kwargs):

        # Get username from user
        self.get_username()

        def pulsate_title_color_username():
            colors = ["#ffcc00", "#e68a00","Maroon1","LightGreen", "Pink", "SlateBlue2","white","MediumPurple1","IndianRed1","Blue","Salmon","LightBlue"]
            for color in cycle(colors):                
                user_label.config(fg=color)
                self.update_idletasks()
                self.after(200)  # Adjust the delay based on your preference
                self.update()


        Tk.__init__(self, *args, **kwargs)
        self.title("2048 Game")
        self.geometry("490x750")
        # Add the following lines to center the window
        window_width = 490
        window_height = 750
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x_coordinate = int((screen_width - window_width) / 2)
        y_coordinate = int((screen_height - window_height - 80) / 2)

        self.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")
        self.configure(bg="#3C3C3C")  # Set background color

        # Set custom fonts and colors
        title_font = ("Quicksand", 28, "bold")
        instruction_font = ("Helvetica", 12)
        button_font = ("Courier", 14, "bold")

        # Create user interface
        self.game_score = StringVar(self)
        self.game_score.set("0")
        self.highest_score = StringVar(self)
        self.highest_score.set("0")

        # Game Title Label
        title_label = Label(self, text="2048 Game", font=("Quicksand", 38, "bold"), bg="#3C3C3C", fg="#ffcc00", relief="ridge")
        title_label.grid(row=0, column=0, columnspan=6, pady=20)

        # Instructions Label
        instruction_label = Label(self, text="Slide tiles using arrow keys.Combine tiles to reach 2048!",font=("Helvetica", 14), bg="#3C3C3C", fg="white", relief="groove")
        instruction_label.grid(row=1, column=0, columnspan=6, pady=15, padx=3)

        # Adding new game, score, and highest score options
        self.button_frame = Frame(self, bg="#3C3C3C")
        self.button_frame.grid(row=2, column=0, columnspan=6, pady=10)

        # New Game button and Username in the same row
        new_game_button = Button(self.button_frame, text="New Game", font=button_font, command=self.new_game, bg="#6B8E23", fg="white")
        new_game_button.grid(row=0, column=0, padx=10)

        user_label = Label(self.button_frame, text=f"Welcome, {self.username}!", font=("Roboto Condensed", 16, "bold"), bg="#3C3C3C", fg="#ffcc00")
        user_label.grid(row=0, column=1, padx=10)

        # Score and Record in the row below
        score_label = Label(self.button_frame, text="Score: ", font=("Arial", 14), bg="#3C3C3C", fg="white")
        score_label.grid(row=1, column=0, pady=(10, 0))

        score_value_label = Label(self.button_frame, textvariable=self.game_score, font=("Arial", 14, "bold"), bg="#3C3C3C", fg="#6B8E23")
        score_value_label.grid(row=1, column=1, pady=(10, 0), padx=10)

        record_label = Label(self.button_frame, text="Record:", font=("Arial", 14), bg="#3C3C3C", fg="white")
        record_label.grid(row=2, column=0)

        record_value_label = Label(self.button_frame, textvariable=self.highest_score, font=("Arial", 14, "bold"), bg="#3C3C3C", fg="#6B8E23")
        record_value_label.grid(row=2, column=1, padx=10)

        self.canvas = Canvas(self, width=410, height=410, borderwidth=5, highlightthickness=0, bg="#eeeeee")
        self.canvas.grid(row=3, column=0, columnspan=6, pady=20)

        # Creates the database table
        self.create_score_table()

        # Fetch and display the user's high score
        self.display_user_high_score()

        # Create new game
        self.new_game()

        # Start the pulsating effect
        self.after(0, pulsate_title_color_username)

    def get_username(self):
        # Use tkinter simpledialog to get the username with an initial value
        self.username = simpledialog.askstring("2048", "Enter your username:")

        if not self.username:
            # If the user cancels or provides an empty username, set a default
            self.username = "GuestPlayer"

    def create_score_table(self):
        connection = sqlite3.connect("2048_scores.db")
        cursor = connection.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS scores (username TEXT, score INT, high_score INT)")
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {self.username} (id INTEGER PRIMARY KEY AUTOINCREMENT,score INT, high_score INT)")
        connection.commit()
        connection.close()


    def display_user_high_score(self):
        connection = sqlite3.connect("2048_scores.db")
        cursor = connection.cursor()

        cursor.execute("SELECT high_score FROM scores WHERE username=?", (self.username,))
        user_high_score = cursor.fetchone()

        if user_high_score is not None:
            self.high_score = user_high_score[0]
            self.highest_score.set(str(self.high_score))

        connection.close()


    # ==== add new tiles
    def new_tiles(self):
        index = random.randint(0, 6)
        x = -1
        y = -1

        # ==== check while game is not over
        while self.full() == False:
            x = random.randint(0, 3)
            y = random.randint(0, 3)

            if (self.game_board[x][y] == 0):
                self.game_board[x][y] = self.new_random_tiles[index]
                x1 = y * 105
                y1 = x * 105
                x2 = x1 + 105 - 5
                y2 = y1 + 105 - 5
                num = self.game_board[x][y]
                if num == 2:
                    self.square[x, y] = self.canvas.create_rectangle(x1, y1, x2, y2, fill="#e0f2f8", tags="rect",
                                                                     outline="", width=0)
                    self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, font=("Arial", 36), fill="#f78a8a", text="2")
                elif num == 4:
                    self.square[x, y] = self.canvas.create_rectangle(x1, y1, x2, y2, fill="#b8dbe5", tags="rect",
                                                                     outline="", width=0)
                    self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, font=("Arial", 36), fill="#f78a8a", text="4")

                break

    # ==== check board is full or not
    def full(self):
        for i in range(0, 4):
            for j in range(0, 4):
                if (self.game_board[i][j] == 0):
                    return False
        return True

    # ==== showing game board
    def show_board(self):
        cellwidth = 105
        cellheight = 105
        self.square = {}

        for column in range(4):
            for row in range(4):
                x1 = column * cellwidth
                y1 = row * cellheight
                x2 = x1 + cellwidth - 5
                y2 = y1 + cellheight - 5
                num = self.game_board[row][column]
                if num == 0:
                    self.show_number0(row, column, x1, y1, x2, y2)
                else:
                    self.show_number(row, column, x1, y1, x2, y2, num)

    # ==== show board block when it is empty
    def show_number0(self, row, column, a, b, c, d):
        self.square[row, column] = self.canvas.create_rectangle(a, b, c, d, fill="#f5f5f5", tags="rect", outline="")

    # ==== show board number
    def show_number(self, row, column, a, b, c, d, num):
        bg_color = {'2': '#eee4da', '4': '#ede0c8', '8': '#edc850', '16': '#edc53f', '32': '#f67c5f', '64': '#f65e3b', '128': '#edcf72', '256': '#edcc61', '512': '#f2b179', '1024': '#f59563', '2048': '#edc22e',}
        color = {'2': '#776e65', '4': '#f9f6f2', '8': '#f9f6f2', '16': '#f9f6f2', '32': '#f9f6f2', '64': '#f9f6f2', '128': '#f9f6f2', '256': '#f9f6f2', '512': '#776e65', '1024': '#f9f6f2', '2048': '#f9f6f2', }
        self.square[row, column] = self.canvas.create_rectangle(a, b, c, d, fill=bg_color[str(num)], tags="rect", outline="")
        self.canvas.create_text((a + c) / 2, (b + d) / 2, font=("Arial", 36), fill=color[str(num)], text=str(num))

    # ==== moves by user
    def moves(self, event):

        if event.keysym == 'Down':
            for j in range(0, 4):
                shift = 0
                for i in range(3, -1, -1):
                    if self.game_board[i][j] == 0:
                        shift += 1
                    else:
                        if i - 1 >= 0 and self.game_board[i - 1][j] == self.game_board[i][j]:
                            self.game_board[i][j] *= 2
                            self.score += self.game_board[i][j]
                            self.game_board[i - 1][j] = 0
                        elif i - 2 >= 0 and self.game_board[i - 1][j] == 0 and self.game_board[i - 2][j] == self.game_board[i][j]:
                            self.game_board[i][j] *= 2
                            self.score += self.game_board[i][j]
                            self.game_board[i - 2][j] = 0
                        elif i == 3 and self.game_board[2][j] + self.game_board[1][j] == 0 and self.game_board[0][j] == self.game_board[3][
                            j]:
                            self.game_board[3][j] *= 2
                            self.score += self.game_board[3][j]
                            self.game_board[0][j] = 0
                        if shift > 0:
                            self.game_board[i + shift][j] = self.game_board[i][j]
                            self.game_board[i][j] = 0
            self.show_board()
            self.new_tiles()
            self.game_over()
        elif event.keysym == 'Right':
            for i in range(0, 4):
                shift = 0
                for j in range(3, -1, -1):
                    if self.game_board[i][j] == 0:
                        shift += 1
                    else:
                        if j - 1 >= 0 and self.game_board[i][j - 1] == self.game_board[i][j]:
                            self.game_board[i][j] *= 2
                            self.score += self.game_board[i][j]
                            self.game_board[i][j - 1] = 0
                        elif j - 2 >= 0 and self.game_board[i][j - 1] == 0 and self.game_board[i][j - 2] == self.game_board[i][j]:
                            self.game_board[i][j] *= 2
                            self.score += self.game_board[i][j]
                            self.game_board[i][j - 2] = 0
                        elif j == 3 and self.game_board[i][2] + self.game_board[i][1] == 0 and self.game_board[0][j] == self.game_board[3][
                            j]:
                            self.game_board[i][3] *= 2
                            self.score += self.game_board[i][3]
                            self.game_board[i][0] = 0
                        if shift > 0:
                            self.game_board[i][j + shift] = self.game_board[i][j]
                            self.game_board[i][j] = 0
            self.show_board()
            self.new_tiles()
            self.game_over()
        elif event.keysym == 'Left':
            for i in range(0, 4):
                shift = 0
                for j in range(0, 4):
                    if self.game_board[i][j] == 0:
                        shift += 1
                    else:
                        if j + 1 < 4 and self.game_board[i][j + 1] == self.game_board[i][j]:
                            self.game_board[i][j] *= 2
                            self.score += self.game_board[i][j]
                            self.game_board[i][j + 1] = 0
                        elif j + 2 < 4 and self.game_board[i][j + 1] == 0 and self.game_board[i][j + 2] == self.game_board[i][j]:
                            self.game_board[i][j] *= 2
                            self.score += self.game_board[i][j]
                            self.game_board[i][j + 2] = 0
                        elif j == 0 and self.game_board[i][1] + self.game_board[i][2] == 0 and self.game_board[i][3] == self.game_board[i][
                            0]:
                            self.game_board[i][0] *= 2
                            self.score += self.game_board[i][0]
                            self.game_board[i][3] = 0
                        if shift > 0:
                            self.game_board[i][j - shift] = self.game_board[i][j]
                            self.game_board[i][j] = 0
            self.show_board()
            self.new_tiles()
            self.game_over()
        elif event.keysym == 'Up':
            for j in range(0, 4):
                shift = 0
                for i in range(0, 4):
                    if self.game_board[i][j] == 0:
                        shift += 1
                    else:
                        if i + 1 < 4 and self.game_board[i + 1][j] == self.game_board[i][j]:
                            self.game_board[i][j] *= 2
                            self.score += self.game_board[i][j]
                            self.game_board[i + 1][j] = 0
                        elif i + 2 < 4 and self.game_board[i + 1][j] == 0 and self.game_board[i + 2][j] == self.game_board[i][j]:
                            self.game_board[i][j] *= 2
                            self.score += self.game_board[i][j]
                            self.game_board[i + 2][j] = 0
                        elif i == 0 and self.game_board[1][j] + self.game_board[2][j] == 0 and self.game_board[3][j] == self.game_board[0][
                            j]:
                            self.game_board[0][j] *= 2
                            self.score += self.game_board[0][j]
                            self.game_board[3][j] = 0
                        if shift > 0:
                            self.game_board[i - shift][j] = self.game_board[i][j]
                            self.game_board[i][j] = 0
            self.show_board()
            self.new_tiles()
            self.game_over()

        self.game_score.set(str(self.score))
        if self.score > self.high_score:
            self.high_score = self.score
            self.highest_score.set(str(self.high_score))

    # ==== to create new game
    def new_game(self):
        self.score = 0
        self.game_score.set("0")
        self.game_board = []
        self.game_board.append([0, 0, 0, 0])
        self.game_board.append([0, 0, 0, 0])
        self.game_board.append([0, 0, 0, 0])
        self.game_board.append([0, 0, 0, 0])
        self.counter = 0  # Reset the counter to 0 for a new game

        while True:
            x = random.randint(0, 3)
            y = random.randint(0, 3)
            if (self.game_board[x][y] == 0):
                self.game_board[x][y] = 2
                break

        index = random.randint(0, 6)
        while self.full() == False:
            x = random.randint(0, 3)
            y = random.randint(0, 3)
            if (self.game_board[x][y] == 0):
                self.game_board[x][y] = self.new_random_tiles[index]
                break
        self.show_board()

    # ==== check for game over
    def game_over(self):
        for i in range(0, 4):
            for j in range(0, 4):
                if (self.game_board[i][j] == 2048):
                    self.game_won()
        for i in range(0, 4):
            for j in range(0, 4):
                if (self.game_board[i][j] == 0):
                    return False
        for i in range(0, 4):
            for j in range(0, 3):
                if (self.game_board[i][j] == self.game_board[i][j + 1]):
                    return False
        for j in range(0, 4):
            for i in range(0, 3):
                if self.game_board[i][j] == self.game_board[i + 1][j]:
                    return False
        gameover = [["G", "A", "M", "E", ], ["", "", "", ""], ["O", "V", "E", "R"], ["", "", "", ""]]
        cellwidth = 105
        cellheight = 105
        self.square = {}

        for column in range(4):
            for row in range(4):
                a = column * cellwidth
                b = row * cellheight
                c = a + cellwidth - 5
                d = b + cellheight - 5
                self.square[row, column] = self.canvas.create_rectangle(a, b, c, d, fill="#ede0c8", tags="rect",
                                                                        outline="")
                self.canvas.create_text((a + c) / 2, (b + d) / 2, font=("Arial", 36), fill="#494949",
                                        text=gameover[row][column])
                
        # Update scores in the database
        self.update_scores()
        return True
    
    def update_scores(self):
        
        connection = sqlite3.connect("2048_scores.db")
        cursor = connection.cursor()

        if self.counter==0:
            cursor.execute(f"INSERT INTO {self.username} (score,high_score) values (?,?) ",(self.score,self.high_score))

        # Fetch the existing high score for the user
        cursor.execute("SELECT high_score FROM scores WHERE username=?", (self.username,))
        existing_high_score = cursor.fetchone()

        # If the user doesn't exist, insert a new record; otherwise, update the high score
        if existing_high_score is None:
            cursor.execute("INSERT INTO scores (username, score, high_score) VALUES (?, ?, ?)", (self.username, self.score, self.high_score))
        else:
            if self.high_score > existing_high_score[0]:
                cursor.execute("UPDATE scores SET high_score=? WHERE username=?", (self.high_score, self.username))
                self.counter+=1
            else:
                cursor.execute("UPDATE scores SET score=? where username=?", (self.score,self.username))
                self.counter+=1

        connection.commit()
        connection.close()

    # ==== check for game won
    def game_won(self):
        gameover = [["Y", "O", "U", "", ], ["", "", "", ""], ["W", "O", "N", "!"], ["", "", "", ""]]
        cellwidth = 105
        cellheight = 105
        self.square = {}
        for column in range(4):
            for row in range(4):
                a = column * cellwidth
                b = row * cellheight
                c = a + cellwidth - 5
                d = b + cellheight - 5
                self.square[row, column] = self.canvas.create_rectangle(a, b, c, d, fill="#ede0c8", tags="rect",
                                                                        outline="")
                self.canvas.create_text((a + c) / 2, (b + d) / 2, font=("Arial", 36), fill="#494949",
                                        text=gameover[row][column])

if __name__ == "__main__":
    # ==== preparing main window
    app = Play_2048()
    app.bind_all('<Key>', app.moves)
    app.wm_title("2048 by PythonGeeks")
    app.minsize(430, 470)
    app.mainloop()