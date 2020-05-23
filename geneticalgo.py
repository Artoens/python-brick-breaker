'''
Genetic Algo

Genome : list of (key, time)

key = left, rigt or None

'''
import game as g
import tkinter as tk
import threading
import random
import time
from collections import namedtuple
import argparse


class Master:
    def __init__(self, master):
        self.population = []
        self.master = master
        control_thread = threading.Thread(target=self.__control)
        control_thread.start()
        for i in range(pop_size):
            root = tk.Tk()
            root.title("Brick Breaker")
            root.resizable(0, 0)
            game = g.Game(root)
            p = Player(game)
            p.play()
            self.population.append(p)

    def __control(self):
        self.close_windows()
        while any(p.playing for p in self.population):
            print('Running', [p.playing for p in self.population])

        for p in self.population:
            p.game.quit()
        for p in self.population:
            print(p.score)

    def close_windows(self):
        self.master.destroy()


class Player():

    genetic_pool = ['Left', 'Right', None]

    def __init__(self, game, genome=None):
        self.game = game
        self.playing = False
        if genome is not None:
            self.genome = genome
        else:
            self.genome = []

    def play(self):
        self.playing = True
        control_thread = threading.Thread(target=self.__control)
        control_thread.start()
        # self.__control()
        self.score = self.game.score
        self.time = self.game.seconds

    def __control(self):
        while self.game.running:
            for gene in self.genome:
                self.__applyGene(gene)

            new_gene = self.createRandomGene()
            self.__applyGene(new_gene)
            self.genome.append(new_gene)
        self.playing = False

    def __applyGene(self, gene):
        if gene.Key == 'Left':
            self.game.keyPressed[0] = True
        elif gene.Key == 'Right':
            self.game.keyPressed[1] = True
        time.sleep(gene.Time / 1000)
        self.game.keyPressed[0:1] = [False, False]

    def createRandomGene(self):
        Gene = namedtuple('Gene', 'Key Time')
        i = random.randint(0, len(self.genetic_pool)-1)
        key = self.genetic_pool[i]
        t = random.randint(100, 250)
        return Gene(key, t)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('size', help='Size of the population (integer)')
    parser.add_argument('-f', '--file', metavar='PATH',
                        help='path to the file where the bests candidates are stored')
    args = parser.parse_args()

    try:
        pop_size = int(args.size)
    except:
        print("enter an int")

    root = tk.Tk()
    app = Master(root)
    root.mainloop()

