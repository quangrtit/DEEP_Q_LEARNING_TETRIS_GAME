from . import NeuralNetwork as dn
import numpy as np
import random
import torch
from collections import deque
import torch.nn as nn
import torch.optim as optim
import os
import torch.nn.functional as F
# from . import Tetris as g

class Agent:
    def __init__(self, learning_rate, epsilon, num_epsilon_decay, epsilon_min, gamma, batch_size, replay_size):
        self.learning_rate = learning_rate
        self.epsilon = epsilon
        self.epsilon_min = epsilon_min
        self.num_epsilon_decay = num_epsilon_decay
        self.gamma = gamma
        self.batch_size = batch_size
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.replay_size = replay_size
        self.replay_buffer = deque(maxlen=replay_size)
        self.main_NN = dn.NN(4, 1).to(self.device)
        self.target_NN = dn.NN(4, 1).to(self.device)
        self.criterion = nn.MSELoss()
        self.optimizer_main = optim.Adam(self.main_NN.parameters(), lr=self.learning_rate)
        self.update_target_NN()
    def update_target_NN(self):
        self.target_NN.load_state_dict(self.main_NN.state_dict())
    def save_experience(self, state, action, reward, next_state, done):
        self.replay_buffer.append((state, action, reward, next_state, done))
    def get_batch_from_buffer(self):
        return random.sample(self.replay_buffer, self.batch_size)
    def save_model(self, path):
        torch.save(self.main_NN.state_dict(), path)
    def load_model(self, path):
        self.main_NN.load_state_dict(torch.load(path, weights_only=True)) 
        self.update_target_NN()
    def choose_action(self, environment):
        action_and_state = environment.get_states() # get all state when adjust x_tetromino and rotate it 
        actions, states = zip(*action_and_state.items())
        # print("this this: ", actions)
        # print("owow ow ow : ", self.epsilon)
        if np.random.uniform(0, 1) <= self.epsilon:
            actions_use = actions[random.randint(0, len(actions) - 1)]
            rotate_rand = actions_use[1]
            action_rand = random.randint(0, environment.width - len(environment.rotate_tetromino(rotate_rand, environment.current_tetromino)[0]))
            # print("hahahaha: ", action_rand, rotate_rand)
            return (action_rand, rotate_rand)
        states = np.array(states, dtype=int)
        states = torch.FloatTensor(states).to(self.device) # 1 x input_size
        self.main_NN.eval()
        with torch.no_grad():
            q_values = self.main_NN(states)[:, 0]
            # print("data use: ", q_values)
        # print("use use use : ", environment.current_tetromino, environment.id_current_tetromino, actions[np.argmax(q_values.cpu().numpy())], actions, len(actions))
        # print("iu em: ", q_values)
        return actions[np.argmax(q_values.cpu().numpy())]
    def train_one_bacth(self):
        # print("hacnakcbjkascanclans, ", len(self.replay_buffer), self.batch_size)
        if len(self.replay_buffer) < self.batch_size:
            return 
        mini_batch = self.get_batch_from_buffer()
        state, action, reward, next_state, done = zip(*mini_batch) # map value from mini_batch
        state = torch.FloatTensor(np.array(state)).to(self.device)
        action = torch.LongTensor(action).to(self.device)
        reward = torch.FloatTensor(reward).to(self.device)
        next_state = torch.FloatTensor(np.array(next_state)).to(self.device)
        done = torch.LongTensor(done).to(self.device)

        q_values = self.main_NN(state)
        self.main_NN.eval()
        with torch.no_grad():
            next_q_values = self.main_NN(next_state)[:, 0]
        # q_values = q_values.gather(1, action.unsqueeze(1)).squeeze(1) # map q_values with action
        # next_q_values = next_q_values.max(1)[0]
        self.main_NN.train()
        target_q_values = reward + (self.gamma * next_q_values * (1 - done))
        # print("hohohoho: ", target_q_values.shape)
        target_q_values = torch.tensor(target_q_values).view(-1, 1)
        # print("iu em iu em: ", q_values.shape, target_q_values.shape, next_q_values.shape)
        # print(target_q_values, q_values)
        # print("hihigigigigig: ", next_q_values.shape, q_values.shape, target_q_values.shape)
        self.optimizer_main.zero_grad()
        loss = F.mse_loss(q_values, target_q_values)  
        loss.backward()
        self.optimizer_main.step()
    