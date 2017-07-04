#!/usr/bin/env python3

"""r
What:    Objects for topology representation
Author:  Arne Tobias Elve
Since:   2017-06-28
Where:   Department of Chemical Engineering
Contact: arne.t.elve(at)ntnu.no
Why:     This is the test version to be presented to Heinz before this is
         implemented into the project itself. This consist of the graph class
         that is the parent of the node class and the arc class. Together these
         form the building blocks for the network representation.
Update:  2017-06-28
"""

from time import asctime, localtime, time                    # Library for time
import os                                                    # Operating system
import numpy as np
import OntoSim
import Common.indices

class Graph(object):
  """Object representation of the topology of the model"""
  def __init__(self,name, nodes, arcs):
    super(Graph, self).__init__()
    self.name = name                                        # Name of the model
    self.nodes = nodes                                          # List of nodes
    self.arcs = arcs                                             # List of arcs

    # STORAGE CONTAINERS #
    self.dotfile = 'main.dot'
    self.tokenMass = 'mass'
    self.tokenEnergy = 'energy'


  def makeDot(self):
    with open(self.dotfile, 'w') as dotfile:
      # PREAMBLE
      dotfile.write('#'*79+'\n')
      dotfile.write('#\t Purpose: Dot graph for equation tree.\n')
      dotfile.write('#\t Author:  Arne Tobias Elve\n')
      dotfile.write('#\t Date:    '+str(asctime( localtime(time()) ))+'\n')
      dotfile.write('#\t Why:     Output to dot language \n')
      dotfile.write('#'*79+'\n')
      dotfile.write('graph G {\n')
      dotfile.write('rankdir = "LR"\n')
      # NODES
      for node in self.nodes:
        dotfile.write(node.label +' [style = filled, fillcolor = Tomato];\n')
      # EDGES
      for arc in self.arcs:
        dotfile.write(arc.head.label + ' -- ' + arc.tail.label +
        '[ label = ' + arc.label +'];\n')
      # FINISH FILE
      dotfile.write('}')

  def makeTokenSet(self):
    """
    Loop through  all the nodes and arc and find the tokens.  Preparing for the
    index sets.
    """
    self.tokenset = set()
    for node in nodes:
      self.tokenset |= {node.type['token']}


  def makeIndex(self):
    """
    Not sure on how to do this one...
    Idea is to generate in fundamentally as objects. So list of objects is not
    fundamental enought.

    Should this function be an object itself? Could be fun in that case...

    How does it work as a function?
    List of indices?

    I do not know...

    After sleeping on it I figured out that the indexsets already exist. It is
    "just" the size of the index sets that are missing. The sizes must be
    determined by the already generated graph.
    """
    nmap = []
    # n
    for i,node in enumerate(nodes):
      nmap.append(i)
      # if

    # self.N = IndexSet('N',nmap,)

  def makeMatrices(self):
    """
    Fucntion that generate all the network matrices possible based on the size
    of the index sets. All incidence matrices required and the corresponging
    projection matrices.
    """
    self.matrices = {}
    for token in self.tokenset:
      matrix = []
      # local

  def produceDot(self):
    os.system('dot -Tpdf main.dot > main.pdf')

class IndexSet(object):
  """
  The index set class.

  To be combined  with the index set  already in OntoSim.  Started from scratch
  just because  it can provide some extra inspiration and the structure  of the
  original class is really simple. So that migth be easier.

  Day 2:
  Figured out that the index sets are (of course) defined before this file is
  used. At this stage the job is to define the size of the index set and that
  is done according to the nodes and the arcs.
  """
  ___refs___ = []                               # All indexing sets in sequence
  # def __init__(self,  symbol,                                   # UNIQUE SYMBOL
  #                     mapping = [],               # MAPPING OVER TO TO SUPERSET
  #                     sets = [],                    # COMBINATION OF WHICH SETS
  #                     blocking = [],                         # BLOCK DEFINITION
  #                     superset = None,                 # PART OF WITCH SUPERSET
  #             ):
  #   self.blocking = blocking
  #   self.superset = superset
  #   self.symbol = symbol
  #   self.mapping = mapping
  #   self.sets = sets
  #   if superset == None:
  #     self.superset = self

  def __init__(self, indexSet):
    """
    Init set from index dict

    Args:
      ..: indexSet: Index dict

    Produces:
      ..: populate object
    """
    self.___refs___.append(self)
    self.aliases = indexSet['aliases']
    self.symbol = indexSet['symbol']
    self.layer = indexSet['layer']
    self.type = indexSet['type']
    self.name = indexSet['aliases'][0][1]
    try:
      self.str = indexSet['str']
    except:
      self.str = ''
    try:
      self.super = indexSet['super']
    except:
      self.super = None
    try:
      self.sub = indexSet['sub']
    except:
      self.sub = None
    try:
      self.inner = indexSet['inner']
    except:
      self.inner = None
    try:
      self.outher = indexSet['outher']
    except:
      self.outher = None


  def populateSet(self):
    pass

  def printSet(self):
    print('symbol = ', self.symbol)

  def __str__(self):
    return self.symbol


class Node(Graph):
  """
  Each node included in the graph.
  """
  ___refs___ = []

  def __init__(self, label, type):
    self.___refs___.append(self)
    self.label = label
    self.type = type

class Arc(Graph):
  """
  Each arc included in the graph.
  """
  ___refs___ = []
  def __init__(self, label, type, head, tail):
    self.___refs___.append(self)
    self.label = label
    self.type = type
    self.head = head
    self.tail = tail


if __name__ == '__main__':


  # Generate the index sets file:
  indices = Common.indices.getIndexes()
  Common.indices.makeIndexFile()
  exec(open('Common/indexSets.py').read())
  # print(N.type)
  # for ind in N.___refs___:
    # print(ind.name)

  #
  # nodeType = {'dimensionality':'0', 'dynamics':'lumped', 'token':'mass'}
  # arcType = {'token':'mass', 'mechanism':'volumetic'}
  # # n1 = Node('a',type1)
  # # n2 = Node('b',type1)
  # nodes = [Node('a', nodeType), Node('b', nodeType), Node('c', nodeType),
  # Node('d', nodeType), Node('e', nodeType)]
  # arcs = [Arc('ab',arcType,nodes[0],nodes[1]),
  # Arc('bc', arcType, nodes[1], nodes[2]), Arc('bd',arcType, nodes[1],nodes[3]),
  # Arc('cd', arcType, nodes[2], nodes[3]), Arc('de',arcType, nodes[3],nodes[4])]
  # g = Graph('grafen',nodes, arcs)
  # g.makeDot()
  # g.makeTokenSet()
  # # print(g.tokenset)
  # g.makeMatrices()


  # a1 = Arc('a|b', type1, n1, n2)
