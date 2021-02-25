import game as g
import agent as ag
import matplotlib.pylab as plt
import numpy as np


def plot_agent_reward(rewards):
    """ Fonction dessiner le graphe reward « plot_agent_reward»"""
    plt.plot(np.cumsum(rewards))
    plt.title('le graphe reward Reward vs. Iteration')
    plt.ylabel('Reward')
    plt.xlabel('Iteration')
    plt.show()


class GameLearning:
    def __init__(self):

        print('\nChoisissez le mode du jeu:')
        type = input('1. Agent RL vs Human\n2. Agent RL vs Agent AI\n3. Agent Rl vs Agent RL\nVotre choix = ')
        self.game = g.Game(type)
        self.games_played = 0

    def beginPlaying(self, episodes):
        self.game.play(episodes)


if __name__ == '__main__':
    gl = GameLearning()
    gl.beginPlaying(1000)
