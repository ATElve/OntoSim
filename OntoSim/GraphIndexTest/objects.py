#!/usr/bin/env python3

"""r
What:    Objects for topology representation
Author:  Arne Tobias Elve
Since:   2017-06-28
Where:   Department of Chemical Engineering
Contact: arne.t.elve(at)ntnu.no
Why:     This is  the test version  to be presented  to  Heinz  before  this is
         implemented  into the project itself.  This consist of the graph class
         that is the parent of the node class and the arc class. Together these
         form the building blocks for the network representation.
Update:  2017-06-28: Started
         2017-08-01: Introduced the json format for storage of the graph.
"""

from time import strftime, time                              # Library for time
import os                                                    # Operating system
import numpy as np
import OntoSim
import Common.indices
import json                                               # JSON format library

class Graph(object):
  """Object representation of the topology of the model"""
  def __init__(self,name):
    super(Graph, self).__init__()
    self.graphFile = 'Common/batch_01_tokens.json'
    self.name = name                                        # Name of the model
    # self.nodes = nodes                                        # List of nodes
    # self.arcs = arcs                                           # List of arcs

    self.loadGraphFromJson()


    # STORAGE CONTAINERS #
    self.dotfile = 'DOT/test.dot'
    self.pdffile = 'DOT/test.pdf'
    # self.tokenMass = 'mass'
    # self.tokenEnergy = 'energy'

  def loadGraphFromJson(self):
    """Read in graph file from JSON file"""
    with open(self.graphFile) as data_file:
      self.graph = json.load(data_file)          # Store dictionary into object

  def makeNodes(self):
    """
    Loop trough all the nodes and generate node object.
    """
    self.nodes = {}                    # Use a dictionary for storing the nodes
    for node in self.graph['nodes'].items():
      self.nodes[node[0]] = Node(*node)

  def makeArcs(self):
    """
    Generate the arc objects
    """
    self.arcs = {}
    for arc in self.graph['arcs'].items():
      self.arcs[arc[0]] = Arc(*arc)


  def makeDot(self):
    with open(self.dotfile, 'w') as dotfile:
      # PREAMBLE
      purpose = '#\t Purpose: Dot graph for equation tree'
      author =  '#\t Author:  Arne Tobias Elve'
      date =    '#\t When:    {}'.format(strftime("%Y-%m-%d %H:%M:%S"))
      reason =  '#\t Why:     Output to dot language'
      dotfile.write('#'*79+'\n')
      dotfile.write('{0:78}#\n'.format(purpose))
      dotfile.write('{0:78}#\n'.format(author))
      dotfile.write('{0:78}#\n'.format(date))
      dotfile.write('{0:78}#\n'.format(reason))
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
    propagate at this location. That is carried out in other functions.
    """
    pass


  def propagateToken(self):
    pass
  # def makeTokenSet(self):
  #   """
  #   Loop through  all the nodes and arc and find the tokens.  Preparing for the
  #   index sets.
  #   """
  #   self.tokenset = set()
  #   for node in nodes:
  #     self.tokenset |= {node.type['token']}

  # def getTokenSet(self):
  #   """Retrieve the available token set"""
  #   try:
  #     return self.tokenset
  #   except Exception as e:
  #     print(e.args[0])
  #     print('Token set does not exist, returning empty set')
  #     return set()


  def makeIndex(self):
    """
    Not sure on how to do this one...
    Idea is to generate in fundamentally as objects.  So list of objects is not
    fundamental enough.

    Should this function be an object itself? Could be fun in that case...

    How does it work as a function?
    List of indexes?

    I do not know...

    After sleeping on it I figured out that the index sets already exist. It is
    "just" the dimensions of the index sets that are missing. The sizes must be
    determined by the already generated graph.
    """
    # Node references
    self.nmap = []
    self.nmapNode = []
    self.nmass = []
    self.nmassNode = []

    # Arc references
    self.amap = []
    self.amapArc = []
    self.amass = []
    self.amassArc = []

    # n
    for i, node in enumerate(self.nodes):
      self.nmap.append(i)
      self.nmapNode.append(node)          # This is a strict copy of self.nodes
      print(node.tokens)
      if 'mass' in node.tokens:
        self.nmass.append(i)
        self.nmassNode.append(node)

    for i, arc in enumerate(self.arcs):
      self.amap.append(i)
      self.amapArc.append(Arc)             # This is a strict copy of self.arcs
      if 'mass' in arc.tokens:
        self.amass.append(i)
        self.amassArc.append(arc)
      # if
    # Prepare the set sizes
    A.makeMapping(self.amap)
    A.makeBlocking([1] * np.size(self.amap))
    N.makeMapping(self.nmap)
    N.makeBlocking([1] * np.size(self.nmap))

    F  = self.makeMatrix(self.nodes, self.arcs)
    Fm = self.makeMatrix(self.nmassNode, self.amassArc)
    # self.N = IndexSet('N',nmap,)
    print(F)
    print(Fm)


  def makeMatrices(self):
    """
    Function that generates all the network matrices possible based on the size
    of  the index sets.  All incidence matrices required  and the corresponding
    projection matrices.
    """
    self.matrices = {}
    for token in self.tokens:
      matrix = []
      # local

  def makeMatrix(self, nodelist, arclist):
    """
    Produce incidence matrix based on nodelist and arclist

    Args:
      nodelist: Local nodelist in this matrix
      arclist:  Local arclist in this matrix
    Returns:
      matrix: Produced
    """
    mat = np.zeros((np.size(nodelist),np.size(arclist)))
    for i,node in enumerate(nodelist):                          # For every row
      for j,arc in enumerate(arclist):                 # For column in that row
        if arc.tail == node:                     # Check if tail is current row
          mat[i,j] = -1
        elif arc.head == node:                   # Check if head is current row
          mat[i,j] = 1
    return mat                        # Return the value of the produced matrix



###############################################################################
#                                  INDEXSETS                                  #
###############################################################################
class IndexSet(object):
  """
  The index set class.

  To be combined  with the index set  already in OntoSim.  Started from scratch
  just because  it can provide some extra inspiration and the structure  of the
  original class is really simple. So that might be easier.

  Day 2:
  Figured out  that the index sets are  (of course) defined before this file is
  used. At this stage  the job is to define the size of  the index set and that
  is done according to the nodes and the arcs.
  """
  ___refs___ = []                               # All indexing sets in sequence
  indices = Common.indices.getIndexes() # Read in the complete index dictionary

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
    try:                                                       # Outer blocking
      self.outher = eval(self.indices[indexSet['outher']]['aliases'][0][1])
    except:
      self.outher = None
    # The rest is preparing what to come
    self.blocking = []                # Size of the inner blocking in the outer
    self.mapping = []              # Representation into the superset or itself


  def makeBlocking(self, blocking = []):
    """
    Define sizes of the inner blocks.

    Args:
      blocking: List with the sizes of the inner blocks

    Populate the blocking variable. This maps over to the mapping
    """
    self.blocking = blocking

  def makeMapping(self, mapping = []):
    """
    Make mapping over to super set.

    Args:
      mapping: List with the indices into the superset

    If no super set the set is defined as its own super set.
    """
    self.mapping = mapping

  def __str__(self):                         # The name in the current language
    return self.name

  def __repr__(self):                      # The name in the configuration file
    return self.symbol


class Node(Graph):
  """
  Each node included in the graph.
  """
  ___refs___ = []

  def __init__(self, label, dict):
    self.___refs___.append(self)
    self.label = label
    self.__dict__.update(**dict)

  def makeJson(self):
    return json.dumps(self.__dict__)

  def addMechanism(self, mechanism):
    self.mechanisms = list(set(self.mechanisms).union(set([mechanism])))

  def addToken(self, tokens):
    self.tokens = list(set(self.tokens).union(set(tokens)))

class Arc(Graph):
  """
  Each arc included in the graph.
  """
  ___refs___ = []
  def __init__(self, label, dict):
    self.___refs___.append(self)
    self.label = label
    self.__dict__.update(**dict)


    print(self.__dict__)

  def addMechanismToNodes(self, mechanism):
    """Prepare subsets to head and tail nodes"""
    self.head.addMechanism(mechanism)
    self.tail.addMechanism(mechanism)

  def addTokenToNodes(self):
    """Prepare subsets to head and tail nodes"""
    self.head.addToken(self.tokens)
    self.tail.addToken(self.tokens)

  def keys(self):
    self.__dict__.keys()

  def makeJsonObj(self):
    return json.dumps(self.__dict__)

if __name__ == '__main__':
  g = Graph('TESTGRAPH')
  g.makeNodes()
  g.makeArcs()
