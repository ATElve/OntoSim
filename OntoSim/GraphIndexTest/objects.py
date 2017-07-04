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

from time import strftime, time                    # Library for time
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
    self.dotfile = 'DOT/test.dot'
    self.pdffile = 'DOT/test.pdf'
    self.tokenMass = 'mass'
    self.tokenEnergy = 'energy'


  def makeDot(self):
    with open(self.dotfile, 'w') as dotfile:
      # PREAMBLE
      dotfile.write('#'*79+'\n')
      dotfile.write('#\t Purpose: Dot graph for equation tree.\n')
      dotfile.write('#\t Author:  Arne Tobias Elve\n')
      dotfile.write('#\t Date:    {0}\n'.format(strftime("%Y-%m-%d %H:%M:%S")))
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

  def produceDot(self):
    os.system('dot -Tpdf {0} > {1}'.format(self.dotfile, self.pdffile))

  def injectSpecies(self, reservoir, species):
    """
    Inject a species in a reservoir

    Args:
      reservoir: The reservoir where the injection takes place
      species: List of species which is injected in this reservoir

    This is  used to inject species in the graph.  The injection can only occur
    in an reservoir.  This function  does only inject the species.  It does not
    propogate at this location. That is carried out in other functions.
    """

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
  indices = Common.indices.getIndexes() # Read in the complete index dictionary
  # def __init__(self,  symbol,                                 # UNIQUE SYMBOL
  #                     mapping = [],             # MAPPING OVER TO TO SUPERSET
  #                     sets = [],                  # COMBINATION OF WHICH SETS
  #                     blocking = [],                       # BLOCK DEFINITION
  #                     superset = None,               # PART OF WITCH SUPERSET
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
      indexSet: Index dict

    Generate  the basic  implementation  of the index set.  The index  sets are
    generated  from  the configuration  file representing  the ontology  of the
    model.
    """
    self.___refs___.append(self)                  # Making a list of references
    self.name = indexSet['aliases'][0][1]   # Used in this programming language
    self.aliases = indexSet['aliases']                            # All aliases
    self.symbol = indexSet['symbol']             # Symbol in configuration file
    self.layer = indexSet['layer']                      # Valid in which layers
    self.type = indexSet['type']               # What type is this: its a index
    # The following is a bit of a hack.  Do not like it, but it is not terrible
    try:                     # This the string representation of this index set
      self.str = indexSet['str']
    except:
      self.str = ''
    try:                                    # Maps over to which index set type
      self.super = eval(self.indices[indexSet['super']]['aliases'][0][1])
    except:
      self.super = None
    try:                                                              # Subsets
      self.sub = eval(self.indices[indexSet['sub']]['aliases'][0][1])
    except:
      self.sub = None
    try:                                                       # Inner blocking
      self.inner = eval(self.indices[indexSet['inner']]['aliases'][0][1])
    except:
      self.inner = None
    try:                                                      # Outher blocking
      self.outher = eval(self.indices[indexSet['outher']]['aliases'][0][1])
    except:
      self.outher = None
    # The rest is preparing what to come
    self.blocking = []               # Size of the inner blocking in the outher
    self.mapping = []              # Representation into the superset or itself


  def makeBlocking(blocking = []):
    """
    Define sizes of the inneer blocks.

    Args:
      blocking: List with the sizes of the inner blocks

    Populate the blocking variable. This maps over to the mapping
    """
    pass

  def makeMapping(mapping = []):
    """
    Make mapping over to super set.

    Args:
      mapping: List with the indices into the superset

    If no super set the set is defined as its own super set.
    """
    pass

  def __str__(self):                         # The name in the current language
    return self.name

  def __repr__(self):                      # The name in the configuration file
    return self.symbol


class Node(Graph):
  """inner
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


  #
  nodeType = {'dimensionality':'0', 'dynamics':'lumped', 'token':'mass'}
  arcType = {'token':'mass', 'mechanism':'volumetic'}
  # # n1 = Node('a',type1)
  # # n2 = Node('b',type1)
  nodes = [Node('a', nodeType), Node('b', nodeType), Node('c', nodeType),
  Node('d', nodeType), Node('e', nodeType)]
  arcs = [Arc('ab',arcType,nodes[0],nodes[1]),
  Arc('bc', arcType, nodes[1], nodes[2]), Arc('bd',arcType, nodes[1],nodes[3]),
  Arc('cd', arcType, nodes[2], nodes[3]), Arc('de',arcType, nodes[3],nodes[4])]
  g = Graph('grafen',nodes, arcs)
  g.makeDot()
  g.produceDot()
  # g.makeTokenSet()
  # # print(g.tokenset)
  # g.makeMatrices()


  # a1 = Arc('a|b', type1, n1, n2)
