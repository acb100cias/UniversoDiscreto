import pycxsimulator
from pylab import *

import networkx as nx

populationSize = 100
linkProbability = 0.01
initialInfectedRatio = 0.01
infectionProb = 0.4
recoveryProb = 0.2
linkCuttingProb = 0.1

susceptible = 0
infected = 1

def initialize():
    global time, network, positions, nextNetwork

    time = 0
    
    #network = nx.erdos_renyi_graph(populationSize, linkProbability)
    network = nx.algorithms.bipartite.preferential_attachment_graph(range(populationSize), linkProbability)

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
            cmap = cm.viridis,
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
                    else: # adaptive link cutting behavior
                        if random() < linkCuttingProb:
                            if nextNetwork.has_edge(i, j):
                                nextNetwork.remove_edge(i, j)
        else:
            if random() < recoveryProb:
                nextNetwork.node[i]['state'] = susceptible
            else:
                nextNetwork.node[i]['state'] = infected

    del network
    network = nextNetwork.copy()

pycxsimulator.GUI().start(func=[initialize, observe, update])
