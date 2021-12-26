import numpy as np
import torch
from environment.Gridworld import Gridworld
from IPython.display import clear_output
import random
from matplotlib import pylab as plt
from collections import deque
from tests.test_gw import *
from environment.MarketEnv import MarketEnv
from common.properties import *
from dqn_net import DQNNet

STATE_DIM = 2
ACTION_DIM = 101
DQNModel = DQNNet() # Market
# DQNModel = DQNNet(state_dim = STATE_DIM, output_size = ACTION_DIM)

target_net = copy.deepcopy(DQNModel.model)
target_net.load_state_dict(DQNModel.model.state_dict())

for i in range(epochs):
    marketEnv = MarketEnv()
    state1_ = marketEnv.reset()
    
    status = 1
    mov = 0

    while(status == 1): 
        j+=1
        mov += 1

        qval = DQNModel(state1)
        
        if not torch.cuda.is_available():
            qval_ = qval.data.numpy()
        else:
            qval_ = qval.data.cpu().numpy()
        
        if (random.random() < epsilon):
            action_ind = np.random.randint(0,4)
        else:
            action_ind = np.argmax(qval_)
        
        # Execute action and upate state, and get reward + boolTerminal
        action = action_ind
        marketEnv.step(action)
        state2, reward, done, info_dic = marketEnv.step(action)
        exp = (state1, action, reward, state2, done)
        
        replay.append(exp) #H
        state1 = state2
        
        if len(replay) > batch_size:
            minibatch = random.sample(replay, batch_size)
            Q1, Q2, X, Y, loss = DQNModel.batch_update(minibatch, target_net, STATE_DIM)

            print(i, loss.item())
            clear_output(wait=True)
            
            DQNModel.optimizer.zero_grad()
            loss.backward()
            losses.append(loss.item())
            DQNModel.optimizer.step()
            
            if j % sync_freq == 0: #C
                target_net.load_state_dict(DQNModel.model.state_dict())

        if done or mov > max_moves:
            status = 0
            mov = 0

losses = np.array(losses)

plt.figure(figsize=(10,7))
plt.plot(losses)
plt.xlabel("Epochs",fontsize=22)
plt.ylabel("Loss",fontsize=22)
