from src import Tetris, Agent
if __name__ == "__main__":
    environment = Tetris()
    environment.change_speed(5000)
    agent = Agent(0.001, 1.0, 2000, 0.001, 0.99, 512, 30000)
    best_score = 0
    count = 1
    epoch = 0
    epochs = 3000
    while epoch < epochs:
        state = environment.reset()
        while True:
            act = agent.choose_action(environment) # one tuple (x_location, rotate) have q value max
            next_state, reward, done, score = environment.step(act)
            agent.save_experience(state, act, reward, next_state, done)
            # print("reward: ", reward)
            if done: 
                # if epoch % 16 == 0:
                #     agent.update_target_NN()
                if environment.lines > best_score: 
                    best_score = environment.lines
                    agent.save_model("models/bach_duong_best.pth" + str(environment.lines))
                break  
            print("epochs:", epoch, "count: ", count, "lines:", environment.lines, "epsilon: ", agent.epsilon)
            count += 1
            state = next_state
        if len(agent.replay_buffer) < agent.replay_size / 10: #  we can enought state to trainning NOTICE if we take too few states to train it will be ineffective
            continue  
        agent.train_one_bacth()
        agent.epsilon = agent.epsilon_min + (max(agent.num_epsilon_decay - epoch, 0) * (1 - agent.epsilon_min) / agent.num_epsilon_decay)
        print("epochs_last: ", epoch, "new line complete: ", environment.lines)
        epoch += 1
    agent.save_model("models/anh_quang.pth")
    environment.close_game()
