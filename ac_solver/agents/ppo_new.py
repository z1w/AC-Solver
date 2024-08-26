"""
Implementation of PPO for AC graph.

# TODO: include some examples here.

"""
import numpy as np
import torch
from torch.optim import Adam
from torch import nn
import gymnasium as gym

import random
import time
import uuid
import wandb
from collections import deque
from os import makedirs
from os.path import join
from ac_solver.agents.utils import (
    Agent,
    make_env,
    get_curr_lr,
    load_initial_states_from_text_file,
    convert_relators_to_presentation,
    change_max_relator_length_of_presentation,
)
from ac_solver.agents.args import parse_args
from ac_solver.agents.environment import get_env
from ac_solver.agents.training import train_ppo

def main():
    args = parse_args()

    random.seed(args.seed)
    np.random.seed(args.seed)
    torch.manual_seed(args.seed)
    torch.backends.cudnn.deterministic = args.torch_deterministic

    device = torch.device("cuda" if torch.cuda.is_available() and args.cuda else "cpu")

    envs, initial_states, curr_states, success_record, ACMoves_hist, states_processed = get_env(args)

    agent = Agent(envs, args.nodes_counts).to(device)
    optimizer = Adam(agent.parameters(), lr=args.learning_rate, eps=args.epsilon)

    train_ppo(envs, args, device, optimizer, agent, curr_states, success_record, ACMoves_hist, states_processed, initial_states)

    envs.close()

if __name__ == "__main__":
    main()
