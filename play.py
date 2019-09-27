from dlgo.agent import naive
from dlgo import goboard_slow
from dlgo import gotypes
from tkinter import Canvas
import random
import tkinter as tk
import tkinter.font as tkfont
import time
import copy
import sys

class Simulation(tk.Frame):
    '''Simulation of a game of Go'''

    def __init__(self, master=None):
        super().__init__(master)

        self.master = master
        self.pack()
        self.init()

        self.started = False
        self.wantsStep = False
        self.wantsQuit = False

        self.agent1Runs = 0
        self.agent1Time = 0.0
        self.agent2Runs = 0
        self.agent2Time = 0.0

    def init(self):
        default_font = tk.font.Font(font='TkDefaultFont')
        size = default_font['size']
        sizetwo = 2*size
        self.h1font = tkfont.Font(family="PragmataPro", size=sizetwo)
        self.h2font = tkfont.Font(family="PragmataPro", size=size)
        self.gamefont = tkfont.Font(family="PragmataPro", size=sizetwo)
        tk.Label(self, text="GoBot", font=self.h1font).pack(fill=tk.X)
        tk.Label(self, text="Computer Go", font=self.h2font).pack(fill=tk.X)
        tk.Label(self, text="agents by Jay Byam", font=self.h2font).pack(fill=tk.X)
        self.controlsFrame = tk.Frame(self)
        self.controlsFrame.pack()
        tk.Frame(self, height=2, bd=1, relief=tk.SUNKEN).pack(fill=tk.X, padx = 5, pady = 5)
        self.scoresFrame = tk.Frame(self)
        self.scoresFrame.pack()
        tk.Frame(self, height=2, bd=1, relief=tk.SUNKEN).pack(fill=tk.X, padx = 5, pady = 5)
        self.gameFrame = tk.Frame(self, background='#F5DEB3', highlightbackground='#DEB887', highlightcolor='#DEB887', highlightthickness=0.5)
        self.gameFrame.pack(padx=10, pady=5)
        tk.Frame(self, height=2, bd=1, relief=tk.SUNKEN).pack(fill=tk.X, padx = 5, pady = 5)
        self.optionsFrame = tk.Frame(self)
        self.optionsFrame.pack()
        tk.Frame(self, height=2, bd=1, relief=tk.SUNKEN).pack(fill=tk.X, padx = 5, pady = 5)
        self.statusFrame = tk.Frame(self)
        self.statusFrame.pack()

        self.startStopButton = tk.Button(self.controlsFrame, text="Step", command=self.step)
        self.startStopButton.pack(side="left")
        self.startStopButton = tk.Button(self.controlsFrame, text="Start", command=self.startStop)
        self.startStopButton.pack(side="left")
        self.quitButton = tk.Button(self.controlsFrame, text="Reset", command=self.reset)
        self.quitButton.pack(side="left")
        self.quitButton = tk.Button(self.controlsFrame, text="Quit", command=self.quit)
        self.quitButton.pack(side="left")
        self.startStopLabel = tk.Label(self.statusFrame, text="stopped")
        self.startStopLabel.pack(side="left")

        # Options

        self.team1AgentType = tk.StringVar(value="Random")
        self.team1AgentType.trace('w', self.agentTypeChanged)
        self.team2AgentType = tk.StringVar(value="Random")
        self.team2AgentType.trace('w', self.agentTypeChanged)
        tk.Label(self.optionsFrame, text="Team 1 Agent Type").grid(column = 0, row = 0)
        self.team1Type = tk.OptionMenu(self.optionsFrame, self.team1AgentType, "Human", "Random")
        tk.Label(self.optionsFrame, text="Team 2 Agent Type").grid(column = 0, row = 1)
        self.team2Type = tk.OptionMenu(self.optionsFrame, self.team2AgentType, "Random", "Human")
        self.team1Type.grid(column = 1, row = 0)
        self.team2Type.grid(column = 1, row = 1)

        self.started = False
        self.wantsStep = False

        self.gameCountLabel = tk.Label(self.scoresFrame, text="# Games")
        self.gameCountValue = tk.Label(self.scoresFrame, text="0")
        self.gameCountLabel.grid(row=0, column=0)
        self.gameCountValue.grid(row=1, column=0)

        self.drawsCountLabel = tk.Label(self.scoresFrame, text="Draws")
        self.drawsCountValue = tk.Label(self.scoresFrame, text="0")
        self.drawsCountLabel.grid(row=0, column=1)
        self.drawsCountValue.grid(row=1, column=1)

        self.team1CountLabel = tk.Label(self.scoresFrame, text="Team 1")
        self.team1CountValue = tk.Label(self.scoresFrame, text="0")
        self.team2CountLabel = tk.Label(self.scoresFrame, text="Team 2")
        self.team2CountValue = tk.Label(self.scoresFrame, text="0")
        self.team1CountLabel.grid(row=0, column=2)
        self.team1CountValue.grid(row=1, column=2)
        self.team2CountLabel.grid(row=0, column=3)
        self.team2CountValue.grid(row=1, column=3)

        # Build initial board
        self.gameInnerFrame = tk.Frame(self.gameFrame, borderwidth=0)
        self.gameInnerFrame.pack(padx=12.5, pady=12.5)

        self.game = goboard_slow.GameState.new_game(19)
        self.drawnBoard = []
        self.stones = [
            [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
            [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
            [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
            [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
            [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
            [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
            [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
            [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
            [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
            [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
            [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
            [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
            [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
            [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
            [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
            [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
            [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
            [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ],
            [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None ]
        ]

        for r in range(19):
            rowArray = [ [ 0 ], [ 0 ], [ 0 ], [ 0 ], [ 0 ], [ 0 ], [ 0 ], [ 0 ], [ 0 ], [ 0 ], [ 0 ], [ 0 ], [ 0 ], [ 0 ], [ 0 ], [ 0 ], [ 0 ], [ 0 ], [ 0 ] ]
            for i in range(19):
                rowArray[i] = Canvas(self.gameInnerFrame, width=25, height=25, background='#F5DEB3', borderwidth=0, highlightthickness=0)
                if r == 0 or r == 18:
                    if r == 0:
                        rowArray[i].create_line(12.5, 12.5, 12.5, 25.5)
                    else:
                        rowArray[i].create_line(12.5, -0.5, 12.5, 12.5)  
                else:
                    rowArray[i].create_line(12.5, -0.5, 12.5, 25.5)

                if i == 0:
                    rowArray[i].create_line(12.5, 12.5, 25.5, 12.5)
                elif i == 18:
                    rowArray[i].create_line(-0.5, 12.5, 12.5, 12.5)
                else:
                    rowArray[i].create_line(-0.5, 12.5, 25.5, 12.5)

                if (r == 3 or r == 9 or r == 15) and (i == 3 or i == 9 or i == 15):
                    rowArray[i].create_oval(11, 11, 15, 15, fill='black')
                    
                cellCoords = { "r": r, "c": i }
                rowArray[i].bind("<Button-1>", lambda event, args=cellCoords: self.cellClicked(event, args))
                rowArray[i].grid(row=r, column=i)
            self.drawnBoard.append(rowArray)

        self.reset()
        self.gameloop()

    def agentTypeChanged(self, *args):
        self.started = False
        self.reset()

    def cellClicked(self, event, args):
        if (self.turn == 0 and self.team1AgentType.get() == "Human") or (self.turn == 1 and self.team2AgentType.get() == "Human"):
            human = self.agents[self.turn]
            human.percepts = args

            if not hasattr(human.cellClicked, 'r'):
                if self.game.board[human.percepts['r']][human.percepts['c']].startswith(human.teamLetter):
                    human.cellClicked = human.percepts
                    return

            if self.game.board[human.percepts['r']][human.percepts['c']] == "E":
                # Check if it's a legal move
                legalBoards = self.game.legalNextBoards(self.game.board, human.team)
                legalBoard = []
                for board in legalBoards:
                    if board[human.cellClicked['r']][human.cellClicked['c']] == "E" and board[human.percepts['r']][human.percepts['c']].startswith(human.teamLetter):
                        legalBoard = board
                        break
                if len(legalBoard) > 0:
                    human.nextMove = legalBoard
                    human.cellClicked = {}


    def startStop(self):
        if self.started:
            self.started = False
            self.startStopLabel["text"] = "stopped"
            self.startStopButton["text"] = "Start"
        else:
            self.started = True
            self.startStopLabel["text"] = "started"
            self.startStopButton["text"] = "Stop"

    def step(self):
        self.wantsStep = True

    def newAgent(self, type):
        if type == "Random":
            return naive.RandomBot()
        if type == "Human":
            return agent.human.Human()
        return naive.RandomBot()

    def drawBoard(self):
        # Update drawn stones on the board
        for row in range(19):
            for col in range(19):
                stone = self.game.board.get(gotypes.Point(row = row + 1, col = col + 1))
                if self.stones[row][col] is not None:
                    self.drawnBoard[row][col].delete(self.stones[row][col])
                    self.stones[row][col] = None
                if stone is not None:
                    fill = 'black'
                    if stone == gotypes.Player.white:
                        fill = 'white'
                    self.stones[row][col] = self.drawnBoard[row][col].create_oval(5, 5, 20, 20, fill = fill, width = 0.5)


    def reset(self):
        self.gamecount = 0
        self.wincounts = [0, 0, 0]
        self.game = goboard_slow.GameState.new_game(19)
        self.winner = 0
        self.count = 0
        self.turn = 0

        self.agents = {
            gotypes.Player.black: self.newAgent(self.team1AgentType.get()),
            gotypes.Player.white: self.newAgent(self.team2AgentType.get())
        }

        self.drawBoard()

    def takeTurn(self):
        '''runs a turn of the simulation'''

        if (self.turn == 0 and self.team1AgentType.get() == "Human") or (self.turn == 1 and self.team2AgentType.get() == "Human"):
            if len(self.agents[self.turn].nextMove) == 0: # Only continue if the move is ready
                return

        bot_move = self.agents[self.game.next_player].select_move(self.game)
        self.game = self.game.apply_move(bot_move)
        self.drawBoard()

        self.count = self.count + 1
        self.turn = 1 - self.turn

    def update(self):
        '''Update simulation'''
        if not self.started and not self.wantsStep:
            return

        if self.gamecount >= 10:
            self.startStop()
            print("Agent 1 average turn time: " + str(self.agent1Time / self.agent1Runs) + " ms")
            print("Agent 2 average turn time: " + str(self.agent2Time / self.agent2Runs) + " ms")
            return

        self.takeTurn()
        self.wantsStep = False

        # Reset agents if the game is over
        if self.game.is_over():
            self.wincounts[self.winner] = self.wincounts[self.winner] + 1
            self.gamecount = self.gamecount + 1
            if self.team1AgentType.get() != "Human":
                self.agent1Runs += 1
                self.agent1Time += self.agents[0].runTime / self.agents[0].runs * 1000
            if self.team2AgentType.get() != "Human":
                self.agent2Runs += 1
                self.agent2Time += self.agents[1].runTime / self.agents[1].runs * 1000
            self.winner = 0
            self.count = 0
            self.turn = 0
            self.reset()
            self.drawBoard()

    def draw(self):
        '''Draw simulation'''
        if not self.started and not self.wantsStep:
            return
        
        self.gameCountValue["text"] = self.gamecount
        self.drawsCountValue["text"] = self.wincounts[0]
        self.team1CountValue["text"] = self.wincounts[1]
        self.team2CountValue["text"] = self.wincounts[2]

    def gameloop(self):
        self.update()
        self.draw()
        if (self.started):
            if (self.turn == 0 and self.team1AgentType.get() != "Human" and self.team2AgentType.get() == "Human") or (self.turn == 1 and self.team2AgentType.get() != "Human" and self.team1AgentType.get() == "Human"):
                delay = 100
                if (self.turn == 0 and self.team1AgentType.get() == "Random") or (self.turn == 1 and self.team1AgentType.get() == "Random"):
                    delay = 1000
                self.master.after(delay, self.gameloop)
            else:
                self.master.after_idle(self.gameloop)
        else:
            self.master.after(100, self.gameloop)

root = tk.Tk()
sim = Simulation(master=root)
sim.mainloop()
