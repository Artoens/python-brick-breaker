'''
Genetic Algo

Genome : list of (key, time)

key = left, rigt or None

'''
import game
import tkinter as tk
import threading
import random
import time

class Player():
    
    # Initialization of the window
    root = tk.Tk()
    root.title("Brick Breaker")
    root.resizable(0, 0)


    # Starting up of the game
    game = game.Game(root)
    
    def __init__(self, genome = None):
        if genome is not None:
            self.genome = genome

    def play(self):
        control_thread = threading.Thread(target=self.control)
        control_thread.start()
        self._initGame()

    def _initGame(self):
        self.root.mainloop()

    def control(self):
        while True:
            i = random.randint(0, 1)
            t = random.randint(100, 250)
            self.game.keyPressed[i] = True
            time.sleep(t / 1000)
            self.game.keyPressed[i] = False




p = Player()
p.play()
