Each .npy file stores data for one episode
Loading the data will give you a numpy array of shape, Tx10x6
T is the no. of time steps, 10 corresponds to the 10 agents. First 5 are guards, last 5 are attackers.
The 6 observations are:

1) 1 means agent is alive, 0 means it is dead. If dead then the other info for this agent can be ignored.
2) x coordinate: -1 to 1
3) y coordinate: -1 to 1
4) orientation in angle
5) x component of velocity
6) y component of velocity