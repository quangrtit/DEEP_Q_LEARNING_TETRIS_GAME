import pygame 
import numpy
import random

BLOCK_SIZE = 35
FRAMESPEED = 5000
DIS_WIDTH = 16 * BLOCK_SIZE
DIS_HEIGHT = 20 * BLOCK_SIZE
GAME_DIS_WIDTH = 10 * BLOCK_SIZE
GAME_DIS_HEIGHT = 20 * BLOCK_SIZE
YELLOW = (255, 255, 102)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)
PINK = (255,192,203) 
PURPLE = (128,0,128)
class Tetris:
    # 7 tetrominos include I, O, T, S, Z, J, L
    color_tetrominos = [
        (128,128,128),
        (255,0,0), 
        (0,255,0), 
        (0,0,255), 
        (255,255,0), 
        (0,255,255),
        (255,0,255)
    ]
    tetrominos = [
        [[1, 1, 1, 1]], # I

        [[2, 2],
         [2, 2]], # O

        [[0, 3, 0], 
         [3, 3, 3]], # T

        [[0, 4, 4],
         [4, 4, 0]], # S

        [[5, 5, 0],
         [0, 5, 5]], # Z

        [[6, 0, 0],
         [6, 6, 6]], # J

        [[0, 0, 7],
         [7, 7, 7]] # L  
    ]
    def __init__(self):
        self.width = 10
        self.height = 20
        self.fps = FRAMESPEED
        self.bag = []
        self.reset()
    def reset(self):
        pygame.init()
        self.clock = pygame.time.Clock() 
        self.display = pygame.display.set_mode((DIS_WIDTH, DIS_HEIGHT))
        pygame.display.set_caption("ANH QUẢNG")
        self.board = [[-1] * self.width for _ in range(self.height)]
        self.gameover = False
        self.complete_lines = 0
        self.rand_new_tetromino()
        # self.bag = [i for i in range(len(self.tetrominos))]
        # self.id_current_tetromino = random.randint(0, len(self.tetrominos) - 1)
        # self.current_tetromino = self.tetrominos[self.id_current_tetromino]
        # demo = self.random_action()
        self.block_size = BLOCK_SIZE
        self.x_tetromino = 0
        self.y_tetromino = 0
        self.score = 0
        self.num_tetrominos = 0
        self.lines = 0
        self.action_location = {
            0: "action 0 * BLOCK",
            1: "action 1 * BLOCK",
            2: "action 2 * BLOCK", 
            3: "action 3 * BLOCK",
            4: "action 4 * BLOCK", 
            5: "action 5 * BLOCK",
            6: "action 6 * BLOCK",
            7: "action 7 * BLOCK",
            8: "action 8 * BLOCK",
            9: "action 9 * BLOCK",
        }
        self.action_rotate = {
            0: "action rotate 0 * 90",
            1: "action rotate 1 * 90",
            2: "action rotate 2 * 90", 
            3: "action rotate 3 * 90"
        }
        # self.render()
        state, self.board, complete_lines = self.get_state(self.board)
        return state
        # we use list about 4 * 10 (action_rotate * action_location) 

    def draw_tetromino(self):
        for i in range(len(self.current_tetromino)):
            for j in range(len(self.current_tetromino[i])):
                if self.current_tetromino[i][j] != 0:
                    pygame.draw.rect(self.display, BLACK, (self.x_tetromino + BLOCK_SIZE * j, self.y_tetromino + BLOCK_SIZE * i, BLOCK_SIZE, BLOCK_SIZE)) 
                    pygame.draw.rect(self.display, self.color_tetrominos[self.id_current_tetromino], (self.x_tetromino + BLOCK_SIZE * j, self.y_tetromino + BLOCK_SIZE * i, BLOCK_SIZE - 1, BLOCK_SIZE - 1))
    def rotate_tetromino(self, num, tetromino_id): # rotate tetromino num round
        tetromino = [x[:] for x in tetromino_id]
        for _ in range(num):
            tetromino_after = []
            for j in range(len(tetromino[0])):
                tetromino_after.append([])
                for i in range(len(tetromino) - 1, -1, -1):
                    tetromino_after[j].append(tetromino[i][j])
            tetromino = tetromino_after
        return tetromino
    # def random_action(self): # purpose get action avaiable to example
    #     action_location = random.randint(0, self.width - 1)
    #     action_rotate = random.randint(0, 3)
    #     action = (action_location, action_rotate)
    #     while not self.check_action_accept(action):
    #         action_location = random.randint(0, self.width - 1)
    #         action_rotate = random.randint(0, 3)
    #         action = (action_location, action_rotate)
    #     return action
    # def check_action_accept(self, action):
    #     action_location, action_rotate = action[0], action[1]
    #     tetromino_tmp = self.rotate_tetromino(action_rotate, self.current_tetromino)
    #     if (action_location + len(tetromino_tmp[0]) <= self.width):
    #         return True 
    #     return False
    def rand_new_tetromino(self):
        if len(self.bag) == 0:
            self.bag = [i for i in range(len(self.tetrominos))]
            random.shuffle(self.bag)
        self.id_current_tetromino = self.bag[-1]
        self.current_tetromino = self.tetrominos[self.id_current_tetromino]
        self.bag.pop()
    def get_and_update_complete_lines(self, board_in):
        board = [x[:] for x in board_in]
        complete_lines = 0
        j = len(board) - 1
        while j >= 0:
            if -1 not in board[j]:
                complete_lines += 1
                board[j] = [-1 for _ in range(len(board[j]))]
                # we should copy data in j - 1 into j 
                id = j
                while id > 0: 
                    board[id] = board[id - 1]
                    id -= 1
                board[0] = [-1 for _ in range(len(board[j]))]
            else:
                j -= 1  
        
        # self.lines += complete_lines
        return complete_lines, board
    def get_holes(self, board): # get holes from board
        num_holes = 0
        for col in zip(*board):
            row = 0
            while row < len(board) and col[row] == -1:
                row += 1
            num_holes += len([x for x in col[row + 1:] if x == -1])
        return num_holes
    def get_aggregate_height_and_bumpiness(self, board):
        bumpiness = 0
        all_height = []
        for col in zip(*board):
            all_height.append(0)
            for i in range(len(col)):
                if col[i] != -1:
                    all_height[-1] = self.height - i
                    break
        # print("co cai con cak: ", all_height)
        for i in range(1, len(all_height)):
            bumpiness += abs(all_height[i] - all_height[i - 1])
        return sum(all_height), bumpiness
    def end_game(self): # compare board and curent tetromino location 
        for j in range(len(self.current_tetromino)):
            for i in range(len(self.current_tetromino[j])):
                if self.board[self.y_tetromino // BLOCK_SIZE + j][self.x_tetromino // BLOCK_SIZE + i] != -1 and self.current_tetromino[j][i] != 0:
                    return True 
        return False 
    def update_board(self, board_in, x_tetromino, y_tetromino, current_tetromino, id_current_tetromino):
        board = [x[:] for x in board_in]
        for j in range(len(current_tetromino)):
            for i in range(len(current_tetromino[j])):
                if current_tetromino[j][i] != 0:
                    # print("deo hieu sao sai nhi: ", y_tetromino // BLOCK_SIZE + j, x_tetromino // BLOCK_SIZE + i, y_tetromino // BLOCK_SIZE, x_tetromino // BLOCK_SIZE)
                    board[y_tetromino // BLOCK_SIZE + j][x_tetromino // BLOCK_SIZE + i] = id_current_tetromino + 1
        return board
    def check_collision(self, board, x_tetromino, y_tetromino, current_tetromino, id_current_tetromino): # check collision of y_height and tetromino and before tetromino
        for j in range(len(current_tetromino)):
            for i in range(len(current_tetromino[j])):
                if y_tetromino // BLOCK_SIZE + j + 1 > self.height - 1:
                    # board = self.update_board(board, x_tetromino, y_tetromino, current_tetromino, id_current_tetromino)
                    return True 
                # print("dit me cay deo chịu được: ", y_tetromino // BLOCK_SIZE, x_tetromino // BLOCK_SIZE, y_tetromino // BLOCK_SIZE + j + 1, x_tetromino // BLOCK_SIZE + i)
                if (board[y_tetromino // BLOCK_SIZE + j + 1][x_tetromino // BLOCK_SIZE + i] != -1 and current_tetromino[j][i] != 0):
                    # board = self.update_board(board, x_tetromino, y_tetromino, current_tetromino, id_current_tetromino)
                    return True 
        
        return False
    # aggregate height, complete lines, holes, and bumpiness
    def get_state(self, board_in):
        board = [x[:] for x in board_in]
        complete_lines, board = self.get_and_update_complete_lines(board)
        holes = self.get_holes(board)
        height, bumpiness = self.get_aggregate_height_and_bumpiness(board)
        state = [
            complete_lines, 
            holes, 
            height, 
            bumpiness
        ]
        # print("this is data use: ", state)
        return numpy.array(state, dtype=int), board, complete_lines
    def get_states(self): # get all state of tetromino 
        state = {}
        tetromino_tmp = [x[:] for x in self.current_tetromino]
        y_tetromino = 0
        id_tetromino = self.id_current_tetromino
        num_rotate = 1 # how many round rotate
        if id_tetromino == 0 or id_tetromino == 3 or id_tetromino == 4: # T, S, Z
            num_rotate = 2
        elif id_tetromino == 1:
            num_rotate = 1
        else:
            num_rotate = 4
        for n_r in range(num_rotate):
            tetromino_tmp_x = self.rotate_tetromino(n_r, tetromino_tmp)
            for i in range(0, self.width): # location x
                board_tmp = [x[:] for x in self.board]
                y_tetromino_tmp = y_tetromino
                if i + len(tetromino_tmp_x[0]) <= self.width:
                    # add y_tetromino 
                    while not self.check_collision(board_tmp, i * BLOCK_SIZE, y_tetromino_tmp, tetromino_tmp_x, id_tetromino):
                        y_tetromino_tmp += BLOCK_SIZE
                    board_tmp = self.update_board(board_tmp, i * BLOCK_SIZE, y_tetromino_tmp, tetromino_tmp_x, id_tetromino)
                    state[(i, n_r)], board_tmp, complete_lines = self.get_state(board_tmp)
                    # if complete_lines >= 1:
                    #     print("ket qua cuoi cung la: ", complete_lines, tetromino_tmp, x_tetromino, y_tetromino_tmp)
                    #     pygame.time.delay(2000)
                    
        return state
    def step(self, actions):
        next_state = None 
        reward = 0
        done = False 
        # state + action => next_state
        action, num_rotate = actions[0], actions[1]
        self.x_tetromino = action * BLOCK_SIZE
        self.y_tetromino = 0
        self.current_tetromino = self.rotate_tetromino(num_rotate, self.current_tetromino)
        done = self.end_game()
        if done: 
            next_state, self.board, complete_lines = self.get_state(self.board)
            reward = 1 + (complete_lines ** 2) * self.width
            # print("data is reward: ", reward, complete_lines)
            self.lines += complete_lines
            self.score += reward
            self.num_tetrominos += 1
            if done: 
                self.score -= 2
            return next_state, reward, done, self.score
        while not self.check_collision(self.board, self.x_tetromino, self.y_tetromino, self.current_tetromino, self.id_current_tetromino):
            self.y_tetromino += BLOCK_SIZE
            self.render()
        self.board = self.update_board(self.board, self.x_tetromino, self.y_tetromino, self.current_tetromino, self.id_current_tetromino)
        # self.id_current_tetromino = random.randint(0, len(self.tetrominos) - 1)
        # self.current_tetromino = self.tetrominos[self.id_current_tetromino]
        self.rand_new_tetromino()
        self.y_tetromino = 0
        # xx, yy = self.random_action()
        # self.x_tetromino = xx * BLOCK_SIZE
        # self.current_tetromino = self.rotate_tetromino(yy, self.current_tetromino)
        # if not self.check_collision(self.board, self.x_tetromino, self.y_tetromino, self.current_tetromino, self.id_current_tetromino):
        #     self.y_tetromino += BLOCK_SIZE
        # else: 
        #     self.board = self.update_board(self.board, self.x_tetromino, self.y_tetromino, self.current_tetromino, self.id_current_tetromino)
        #     # print("dit me may")
        #     self.id_current_tetromino = random.randint(0, len(self.tetrominos) - 1)
        #     self.current_tetromino = self.tetrominos[self.id_current_tetromino]
        #     xx, yy = self.random_action()
        #     self.x_tetromino = xx * BLOCK_SIZE
        #     self.current_tetromino = self.rotate_tetromino(yy, self.current_tetromino)
        #     self.y_tetromino = 0
        #     self.get_states()
        # check end game
        # print("fix mai deo duoc: ", environment.x_tetromino, environment.y_tetromino, environment.current_tetromino)
        next_state, self.board, complete_lines = self.get_state(self.board)
        reward = 1 + (complete_lines ** 2) * self.width
        self.lines += complete_lines
        self.score += reward
        self.num_tetrominos += 1
        if done: 
            reward -= 2
        return next_state, reward, done, self.score
    def render(self):
        self.display.fill(BLACK)
        # draw tetromino
        self.draw_tetromino()
        # draw score
        pygame.draw.rect(self.display, PINK, (self.width * BLOCK_SIZE, 0, self.width * BLOCK_SIZE, DIS_HEIGHT))
        font = pygame.font.SysFont("comicsansms", 35)
        value_score = font.render(f"Score: ", True, PURPLE)
        value_score_number = font.render(f"{self.score}", True, PURPLE)
        value_pieces = font.render(f"Pieces:", True, PURPLE)
        value_pieces_number = font.render(f"{self.num_tetrominos}", True, PURPLE)
        value_lines = font.render(f"Lines:", True, PURPLE)
        value_lines_number = font.render(f"{self.lines}", True, PURPLE)
        self.display.blit(value_score, [11 * BLOCK_SIZE, 0])  
        self.display.blit(value_score_number, [11 * BLOCK_SIZE, BLOCK_SIZE * 1.5])
        self.display.blit(value_pieces, [11 * BLOCK_SIZE, 4 * BLOCK_SIZE]) 
        self.display.blit(value_pieces_number, [11 * BLOCK_SIZE, 4 * BLOCK_SIZE + BLOCK_SIZE * 1.5])
        self.display.blit(value_lines, [11 * BLOCK_SIZE, 8 * BLOCK_SIZE]) 
        self.display.blit(value_lines_number, [11 * BLOCK_SIZE, 8 * BLOCK_SIZE + BLOCK_SIZE * 1.5])
        # draw board
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] != -1:
                    pygame.draw.rect(self.display, BLACK, (BLOCK_SIZE * j, BLOCK_SIZE * i, BLOCK_SIZE, BLOCK_SIZE))
                    pygame.draw.rect(self.display, self.color_tetrominos[self.board[i][j] - 1], (BLOCK_SIZE * j, BLOCK_SIZE * i, BLOCK_SIZE - 1, BLOCK_SIZE - 1))
        pygame.display.update()
        self.clock.tick(self.fps)
    def change_speed(self, frame_speed):
        self.fps = frame_speed
    def close_game(self):
        pygame.quit()
    def delay_game(self, time):
        pygame.time.delay(time)


    