import pycxsimulator
from pylab import *

import networkx as nx

populationSize = 150
linkProbability = 0.2
initialInfectedRatio = 0.1
infectionProb = 0.5
recoveryProb = 0.1

susceptible = 0
infected = 1

def initialize():
    global time, network, positions, nextNetwork

    time = 0
    
    network = nx.erdos_renyi_graph(populationSize, linkProbability)

    positions = nx.random_layout(network)

    for i in network.nodes:
        if random() < initialInfectedRatio:
            network.node[i]['state'] = infected
        else:
            network.node[i]['state'] = susceptible

    nextNetwork = network.copy()

def observe():
    cla()
    nx.draw(network,
            pos = positions,
            node_color = [network.node[i]['state'] for i in network.nodes],
            cmap = cm.Wistia,
            vmin = 0,
            vmax = 1)
    axis('image')
    title('t = ' + str(time))

def update():
    global time, network, nextNetwork

    time += 1

    for i in network.nodes:
        if network.node[i]['state'] == susceptible:
            nextNetwork.node[i]['state'] = susceptible
            for j in network.neighbors(i):
                if network.node[j]['state'] == infected:
                    if random() < infectionProb:
                        nextNetwork.node[i]['state'] = infected
                        break
        else:
            if random() < recoveryProb:
                nextNetwork.node[i]['state'] = susceptible
            else:
                nextNetwork.node[i]['state'] = infected

    network, nextNetwork = nextNetwork, network

pycxsimulator.GUI().start(func=[initialize, observe, update])
