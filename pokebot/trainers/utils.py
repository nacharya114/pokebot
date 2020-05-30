##########################
# Author: Neil Acharya 
# 
# Trainer helper funcs
##########################

def dqn_training(player, dqn, nb_steps):
    dqn.fit(player, nb_steps=nb_steps)

    # This call will finished eventual unfinshed battles before returning
    player.complete_current_battle()

def dqn_evaluation(player, dqn, nb_episodes):
    # Reset battle statistics
    player.reset_battles()
    dqn.test(player, nb_episodes=nb_episodes, visualize=False, verbose=False)

    print(
        "DQN Evaluation: %d victories out of %d episodes"
        % (player.n_won_battles, nb_episodes)
    )
