from direct.showbase.ShowBase import ShowBase

from direct.actor.Actor import Actor

import numpy as np


class SwarmShow(ShowBase):
    """
    A class for producing 3D animated representation of swarm behavior
    """

    def __init__(self, numGuards, numEnemies, states):
        """
        numGuards - number of guards
        numEnemies - number of enemies
        states - numpy array of game states - Tx(numGuards+numEnemies)x6
        """

        # Set up window, camera, etc.
        ShowBase.__init__(self)

        self.gameStates = states

        # Set the background color to black
        self.win.setClearColor((0,0,0,1))

        # Load the environment
        self.environ = loader.loadModel("models/world")
        self.environ.reparentTo(render)
        self.environ.setPos((-5,-5,-5))

        # Create a set of guards and enemies
        self.guards = [self.createGuard(self.gameStates[0,i,:]) for i in range(numGuards)]
        self.enemies = [self.createEnemy(self.gameStates[0,i,:]) for i in range(numGuards,numGuards+numEnemies)]
        self.agents = self.guards + self.enemies
        self.anim_state = [0]*len(self.agents)

        # The target is the thing that the guards are guarding.  Nominally, it's a door,
        # but it could be a flag.  Right now, I have a model for a robot
        self.target = Actor("models/flag")
        self.target.reparentTo(render)
        self.target.setScale(0.01)
        self.target.setPos((0.5, 1.0, 0))
        self.target.setHpr((0,0,0))


        print (len(self.guards), len(self.enemies), len(self.agents))

        self.disableMouse()
        self.camera.setPos((3,-1.5,1))
#        self.camera.setHpr((0,-90,0))
        self.camera.lookAt((0,0,0))

        self.frame = 0

        self.moveTask = taskMgr.doMethodLater(0.2, self.moveAgents, 'moveTask')


    def moveAgents(self, task):

        # Move the guards
        for i in range(len(self.agents)):
            x = self.gameStates[self.frame, i, 1]
            y = self.gameStates[self.frame, i, 2]
            angle = self.gameStates[self.frame, i, 3]
            angle = (angle*180./np.pi) + 90.0

            velocity = np.sqrt(self.gameStates[self.frame,i,4] ** 2 + self.gameStates[self.frame,i,5] ** 2)

            alive = self.gameStates[self.frame, i, 0]
            dead_angle = 0 if alive == 1 else 90.0

            self.agents[i].setPos((x,y,0))
            self.agents[i].setHpr((angle,dead_angle,dead_angle))

            if velocity < 0.05:
                self.agents[i].stop()
            elif velocity < 0.5:
                self.agents[i].pose("walk", self.frame % self.agents[i].getNumFrames("walk"))
            else:
                self.agents[i].pose("run", self.frame % self.agents[i].getNumFrames("run"))

            if alive==0:
                self.agents[i].stop()


        self.frame += 1

        if self.frame < self.gameStates.shape[0]:
            return task.again
        else:
            return task.done


    def createGuard(self, initial_state):
        x = initial_state[1]
        y = initial_state[2]
        angle = initial_state[3]

        angle = (angle*180./np.pi) + 90.
        print (x,y,angle)

        guard = Actor("models/ralph", 
    		          {"run": "models/ralph-run", 
    		           "walk": "models/ralph-walk"})

        guard.reparentTo(render)
        guard.setScale(0.05)
        guard.setPos((x, y, 0))
        guard.setHpr((angle,0,0))
        guard.setColorScale(0.5,0.5,1.0,1.0)

        return guard


    def createEnemy(self, initial_state):
        x = initial_state[1]
        y = initial_state[2]
        angle = initial_state[3]
        angle = (angle*180./np.pi) + 90.
        print (x,y,angle)

        enemy = Actor("models/ralph", 
    		          {"run": "models/ralph-run", 
    		           "walk": "models/ralph-walk"})
        enemy.reparentTo(render)
        enemy.setScale(0.05)
        enemy.setPos((x, y, 0))
        enemy.setHpr((angle,0,0))
        enemy.setColorScale(1.0,0.5,0.5,1.0)

        return enemy


if __name__=='__main__':
	states = np.load('out_files/attacker_win.npy')
	show = SwarmShow(5,5,states)
	show.run()
