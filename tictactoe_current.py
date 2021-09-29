from tkinter import *
from tkinter.messagebox import askretrycancel
from math import floor, inf
from functools import partial


class Application(Tk):
    def __init__(self, dimension):
        super().__init__()
        # Mechanics
        self.cells = {}
        self.choices = {}
        self.button_color = ''
        self.dimension = dimension
        self.player = ''
        self.AI = ''

        # Window Specs
        self.title('Tic-Tac-Toe')
        self.create_layout()
        self.resizable(height=False, width=False)

    def create_layout(self):
        i = 0
        self.insert_space(i, 0)

        greeting = Label(self, text=f"Hi! Let's play Tic-Tac-Toe!\nDo you want to play")
        greeting.grid(row=1, column=1, columnspan=self.dimension)

        self.insert_space(1, self.dimension+1)

        self.choices['x'] = Button(self,
                                   height=2,
                                   width=4,
                                   text='X',
                                   command=lambda: self.player_choice('x'))
        self.choices['x'].grid(row=2, column=1, sticky='E')
        Label(self, text=' OR ').grid(row=2, column=self.dimension-1)
        self.choices['o'] = Button(self,
                                   height=2,
                                   width=4,
                                   text='O',
                                   command=lambda: self.player_choice('o'))

        self.button_color = self.choices['o'].cget("bg")

        self.choices['o'].grid(row=2, column=self.dimension, sticky='W')

        self.insert_space(3, 1)

        self.insert_board()

        self.insert_space(self.dimension**2, 1)

    def insert_space(self, row, column):
        Label(self, text='     ').grid(row=row, column=column)

    def insert_board(self):
        h_grid_offset = self.dimension
        v_grid_offset = 1
        for i in range(self.dimension ** 2):
            self.cells[f"cell{i}"] = {'owner': '', 'button': Button(self,
                                                                    height=5,
                                                                    width=10,
                                                                    state=DISABLED,
                                                                    command=partial(self.player_turn, i))}
            self.cells[f"cell{i}"]['button'].grid(row=floor(i / self.dimension) + 1 + h_grid_offset,
                                                  column=i % self.dimension + v_grid_offset)

    def player_choice(self, choice):
        # Highlights pressed button green, saves value to self.player, highlights the other one red
        choices = ['x', 'o']
        choices.remove(choice)
        self.AI = choices[0]
        # Save selected value to self.player
        self.player = choice

        # Highlight button green
        self.choices[choice]['bg'] = '#69ff6e'
        # Highlight the other one red
        self.choices[self.AI]['bg'] = '#ff6969'
        # Disable selection buttons
        for k, v in self.choices.items():
            v['state'] = DISABLED
        for k, v in self.cells.items():
            v['button']['state'] = NORMAL
        self.play_game()  # X always goes first

    def play_game(self):
        if self.AI == 'x':
            self.AI_turn()

    def player_turn(self, index):
        # player makes a selection, assign player as new button owner
        if self.cells[f"cell{index}"]['owner'] == '':
            self.cells[f"cell{index}"]['owner'] = self.player
            self.cells[f"cell{index}"]['button']['text'] = self.player.upper()
            self.cells[f"cell{index}"]['button']['bg'] = '#69ff6e'
            self.cells[f"cell{index}"]['button']['state'] = DISABLED
            if self.assess_win(self.cells)[0]:
                self.reset('You won!')
            else:
                self.AI_turn()

    def AI_turn(self):
        moves = self.find_legal_moves(self.cells, self.AI)
        score = -inf
        for move in moves:
            minimax = self.minimax(move, len(moves)-1, False)
            if minimax >= score:
                score = minimax
                best_move = move
        try:
            for k, v in best_move.items():
                if v['owner'] == self.AI:
                    self.cells[k]['owner'] = self.AI
                    self.cells[k]['button']['text'] = self.AI.upper()
                    self.cells[k]['button']['bg'] = '#ff6969'
                    self.cells[k]['button']['state'] = DISABLED
            if self.assess_win(self.cells)[0]:
                self.reset('AI won!')
        except UnboundLocalError:
            self.reset("It's a draw!")
            return
        if self.draw(self.cells):
            self.reset("It's a draw!")


    def minimax(self, move, depth, maximizing_player):  # AI is the maximizer, human is the minimizer
        someone_won, who_won = self.assess_win(move)
        if depth == 0 or someone_won:
            # return static evaluation
            if who_won == self.AI:
                return 1
            if who_won == self.player:
                return -1
            if not someone_won:
                return 0
        if maximizing_player:
            legal_moves = self.find_legal_moves(move, self.AI)  # creating branches
            max_eval = -inf
            for move in legal_moves:
                if max_eval == 1:
                    return max_eval
                score = self.minimax(move, depth-1, False)
                max_eval = max(score, max_eval)
            return max_eval
        else:
            legal_moves = self.find_legal_moves(move, self.player)  # creating branches
            min_eval = inf
            for move in legal_moves:
                if min_eval == -1:  # Pruning
                    return min_eval
                score = self.minimax(move, depth-1, True)
                min_eval = min(score, min_eval)
            return min_eval

    def print_board(self, board_state):
        for i in range(self.dimension):
            for j in range(self.dimension):
                if j == 0:
                    print("\n")
                    print(board_state[f"cell{i + j * self.dimension}"]['owner'], end="_ ")
                else:
                    print(board_state[f"cell{i+j*self.dimension}"]['owner'], end="_ ")
        print('\n------')

    def find_legal_moves(self, board_state, player):
        # This should include a previous move
        legal_moves = []
        # Count unassigned cells
        for k, v in board_state.items():
            if v['owner'] == '':
                # Create a dictionary for each key that is empty, assigning a new spot to AI
                # k = 'cell#
                move = {}
                for i in range(self.dimension ** 2):
                    move[f"cell{i}"] = {'owner': ''}  # creates an empty board, should copy the existing one
                    if board_state[f"cell{i}"]['owner'] != '':
                        move[f"cell{i}"] = {'owner': board_state[f"cell{i}"]['owner']}
                    if k == f"cell{i}":
                        move[k]['owner'] = player
                legal_moves.append(move)
        return legal_moves

    def win_paths(self, board_state):
        # board state is a dictionary, use coordinates to check if there is a win anywhere
        rows = [[] for i in range(self.dimension)]
        columns = [[] for i in range(self.dimension)]
        diags = [[] for i in range(2)]
        for k, v in board_state.items():
            coordinate = int(k[-1])
            rows[int(coordinate/self.dimension)].append(v['owner'])
            columns[int(coordinate % self.dimension)].append(v['owner'])
            if coordinate in [(x+1)*(self.dimension-1) for x in range(self.dimension)]:
                diags[0].append(v['owner'])
            if coordinate in [x*(self.dimension+1) for x in range(self.dimension)]:
                diags[1].append(v['owner'])
        return rows+columns+diags

    def assess_win(self, board_state):
        for path in self.win_paths(board_state):
            if len(set(path)) == 1 and '' not in path:  # path is occupied by the same 3 symbols
                return True, path[0]
        return False, ''

    def draw(self, board_state):
        draw = True
        for k, v in board_state.items():
            if v['owner'] == '':
                draw = False
        return draw

    def reset(self, condition):
        answer = askretrycancel(title='GAME OVER!', message=f"{condition}. Wanna play again?")
        if answer:
            for i in range(self.dimension**2):
                self.cells[f"cell{i}"]['owner'] = ''
                self.cells[f"cell{i}"]['button']['bg'] = self.button_color
                self.cells[f"cell{i}"]['button']['text'] = ''
                self.cells[f"cell{i}"]['button']['state'] = DISABLED
            for i in ['x', 'o']:
                self.choices[i]['bg'] = self.button_color
                self.choices[i]['state'] = NORMAL
        else:
            self.destroy()

app = Application(3)  # Adjust geometry for it to work with >3
app.mainloop()