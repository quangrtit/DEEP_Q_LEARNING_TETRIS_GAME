from src import Tetris, Agent
if __name__ == "__main__":
    environment = Tetris()
    environment.change_speed(5000)
    agent = Agent(0.001, 0.0, 0, 0.0, 0.99, 512, 30000)
    agent.load_model("models/bach_duong_best.pth47117")
    for i in range(2):
        state = environment.reset()
        while True:
            act = agent.choose_action(environment) # one tuple (x_location, rotate) have q value max
            next_state, reward, done, score = environment.step(act)
            # print("reward: ", reward)
            if done: 
                break  
            state = next_state
    environment.close_game()
