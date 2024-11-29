from src import Tetris, Agent
import math
if __name__ == "__main__":
    environment = Tetris()
    environment.change_speed(50000)
    agent = Agent(0.001, 0.0, 0, 0.0, 0.99, 512, 30000)
    agent.load_model("D:\MY_PROJECT\DEEP_LEARNING\TETRIS_DEEP_Q_LEARNING\models\model16527-2025")
    while True:
        state = environment.reset()
        cnt = 0
        p_start = 0
        while True:
            act = agent.choose_action(environment) # one tuple (x_location, rotate) have q value max
            next_state, reward, done, score = environment.step(act)
            if int(math.sqrt((reward - 1) // 10)) >= 2:
                print("completes lines: ", int(math.sqrt((reward - 1) // 10)), "game: ", cnt, "denta: ", cnt - p_start)
                p_start = cnt
            if done: 
                print("game: ", environment.lines)
                break  
            cnt += 1
            state = next_state
        environment.delay_game(1000)
    environment.close_game()