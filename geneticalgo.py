'''
Genetic Algo

Genome : list of (key, time)

    key = left, rigt or None

    time = between 100 et 250 ms

indicators : score and time

Bestfit = sort by hihger score then lower time
    =>  highest score == highest advencement
        lowest time == most efficiant

'''
import game as g
import tkinter as tk
import threading
import random
import time
from collections import namedtuple
import argparse
import gameinfo
import json

class Master:
    def __init__(self, master, new_genes=[]):
        self.population = Population()
        self.master = master
        self.control_thread = threading.Thread(target=self.__control)
        self.control_thread.start()

        
        for i in range(len(new_genes)):
            root = tk.Tk()
            root.title("Brick Breaker")
            root.resizable(0, 0)
            game = g.Game(root)
            p = Player(game, genome=new_genes[i])
            self.population.add(p)
       
        for i in range(pop_size - len(new_genes)):
            root = tk.Tk()
            root.title("Brick Breaker")
            root.resizable(0, 0)
            game = g.Game(root)
            p = Player(game, genome=[])
            self.population.add(p)

    def __control(self):
        self.master.destroy()
        while any(p.playing for p in self.population.getPeoples()):
            # print('Running', [p.playing for p in self.population])
            time.sleep(1)
        for p in self.population.getPeoples():
            p.game.quit()


    def close_windows(self):
        pass

    def getPopulation(self):
        return self.population.get()


class Player():

    genetic_pool = ['Left', 'Right', None]

    def __init__(self, game, genome=[]):
        self.game = game
        self.playing = False

        self.genome = genome


        self.play()

    def play(self):
        self.playing = True
        control_thread = threading.Thread(target=self.__control)
        control_thread.start()
        # self.__control()

    def __control(self):
        # print(self.genome)
        while not(self.game.ballThrown):
            pass
        i = 0
        while self.game.running and i < len(self.genome):
            self.__applyGene(self.genome[i])
            i +=1
        while self.game.running:
            new_gene = self.createRandomGene()
            self.__applyGene(new_gene)
            self.genome.append(new_gene)
        self.playing = False

    def __applyGene(self, gene):
        if gene[0] == 'Left':
            self.game.keyPressed[0] = True
        elif gene[0] == 'Right':
            self.game.keyPressed[1] = True
        time.sleep(gene[1] / 100000)
        self.game.keyPressed[0:1] = [False, False]

    def createRandomGene(self):
        i = random.randint(0, len(self.genetic_pool)-1)
        key = self.genetic_pool[i]
        t = random.randint(10000, 25000)
        return [key, t]

    def getScore(self):
        return self.game.score

    def getTime(self):
        return self.game.seconds

class Population():
    def __init__(self):
        self.peoples =[]
        self.reproduction_rate = 0.5

    def add(self, player):
        self.peoples.append(player)

    def getPeoples(self):
        return self.peoples

    def sort(self):
        self.peoples.sort(key=lambda e : e.getTime(), reverse=False)
        self.peoples.sort(key=lambda e : e.getScore(), reverse=True)

        print([p.getScore() for p in self.peoples])
    
    def allSuccess(self, objective):
        for p in self.peoples:
            if p.getScore() != objective:
                return False
        return len(self.peoples)
    
    def selectBests(self):
        self.sort()
        return self.peoples[:len(self.peoples) // 2]
    
    def reporduce(self):
        reproducers = self.selectBests()
        newgenomes = [p.genome for p in reproducers]
        for i in range(len(reproducers)):
            parents = [reproducers[i], reproducers[i-1]]
            newgenome = parents[0].genome[:int(len(parents[0].genome)*self.reproduction_rate)] + parents[1].genome[int(len(parents[1].genome)*(1-self.reproduction_rate)):]
            newgenomes.append(newgenome)
        return newgenomes

    def save(self, file):
        genomes = json.dumps([p.genome for p in self.peoples])
        with open(file, 'w') as f:
            f.write(genomes)

    def getGenes(self):
        return [p.genome for p in self.peoples]



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('size', help='Size of the population (integer)')
    parser.add_argument('file', metavar='PATH',
                        help='path to the file where the bests candidates are stored')
    

    scoreMax = gameinfo.scoreMax()
    new_genes = []

    args = parser.parse_args()
    file = args.file

    try:
        pop_size = int(args.size)
        with open(file) as f:
            new_genes = json.loads(f.read())
    except Exception as e:
        print(e)
        print("-h to help")
        pop_size = 10
        file = 'a.txt'


    current_population = Population()

    if len(new_genes) != pop_size:
        print('not loaded')
        root = tk.Tk()
        app = Master(root)
        root.mainloop()
        app.control_thread.join()
        current_population = app.population
        current_population.save(file)
        new_genes = current_population.getGenes()
    
    
    while not(current_population.allSuccess(3)):
        root = tk.Tk()
        app = Master(root, new_genes)
        root.mainloop()
        app.control_thread.join()
        current_population= app.population
        current_population.save(file)
        new_genes = current_population.reporduce()
        # current_population.sort()

