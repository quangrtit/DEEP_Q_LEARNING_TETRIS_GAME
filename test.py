from src import Tetris, Agent
if __name__ == "__main__":
    environment = Tetris()
    environment.change_speed(50000)
    agent = Agent(0.001, 0.0, 0, 0.0, 0.99, 512, 30000)
    agent.load_model("models_demo/bach_duong_best.pth161123")
    while True:
        state = environment.reset()
        while True:
            act = agent.choose_action(environment) # one tuple (x_location, rotate) have q value max
            next_state, reward, done, score = environment.step(act)
            if done: 
                print("game: ", environment.lines)
                break  
            state = next_state
        environment.delay_game(1000)
    environment.close_game()