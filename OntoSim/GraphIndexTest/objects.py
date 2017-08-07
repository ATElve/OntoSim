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
         2017-08-01: Introduced the JSON format for storage of the graph.
"""

from time import strftime, time                              # Library for time
import os                                                    # Operating system
import numpy as np
import OntoSim
import Common.indices
import json                                               # JSON format library



###############################################################################
#                                    Graph                                    #
###############################################################################

class Graph(object):
  """Object representation of the topology of the model"""
  def __init__(self,name):
    super(Graph, self).__init__()
    self.graphFile = 'AutoGenFiles/batch_01_tokens.json'
    self.typedTokensFile = 'AutoGenFiles/typed_tokens.json'
    self.name = name                                        # Name of the model
    # self.nodes = nodes                                        # List of nodes
    # self.arcs = arcs                                           # List of arcs

    self.loadGraphFromJson()             # Load in the graph from the JSON file
    self.loadTypedTokens()        # Load in the typed tokens from the JSON file

    self.makeTypedTokens()


    # STORAGE CONTAINERS #
    self.dotfile = 'DOT/test.dot'
    self.pdffile = 'DOT/test.pdf'
    # self.tokenMass = 'mass'
    # self.tokenEnergy = 'energy'

  def loadGraphFromJson(self):
    """Read in graph file from JSON file"""
    with open(self.graphFile) as data_file:
      self.graph = json.load(data_file)          # Store dictionary into object

  def loadTypedTokens(self):
    """
    Read  in the automatically generated typed token file and upload  it to the
    graph.
    """
    with open(self.typedTokensFile) as data_file:
      self.typedTokens = json.load(data_file)    # Store dictionary into object


  def makeNodes(self):
    """
    Loop trough all the nodes and generate node object.
    """
    self.nodes = {}                    # Use a dictionary for storing the nodes
    for node in self.graph['nodes'].items():
      self.nodes[node[0]] = Node(*node)               # Label and dict unpacked

  def makeArcs(self):
    """
    Generate the arc objects
    """
    self.arcs = {}
    for arc in self.graph['arcs'].items():
      self.arcs[arc[0]] = Arc(*arc)                   # Label and dict unpacked

  def makeTypedTokens(self):
    """
    Loop  trough  ALL  the typed  tokens  and then  load in  the instances  and
    possible conversions.
    """
    self.species = {}
    # print(self.typedTokens['species']['instances'])
    for species in self.typedTokens['species']['instances']:
      self.species[species] = Species(species)

    self.speciesConversion = {}
    for conversion in self.typedTokens['species']['conversions']:
      print(conversion)
      label = '{} -> {}'.format(', '.join(conversion['reactants']), *conversion['products'])
      # label = '{} -> {}'.format([', '.join[i for i in conversion]))
      print(label)
    # for label,species in self.typedTokens['species'].items():
      # print(label)
      # self.species[label] = Species(label,species)                # Label and dict



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
      dotfile.write('digraph G {\n')
      # dotfile.write('rankdir = "LR"\n')
      # NODES
      for label, node in self.nodes.items():
        # if node[1]
        style = 'filled'                                        # Default shape
        marking = ''                                            # Default label
        fillcolor = 'Tomato'                                    # Default color
        if node.type == 'node_composite':
          continue                                          # Check if grouping
        elif node.type == 'constant':                               # Reservoir
          fillcolor = 'Gold1'
        elif node.type == 'event':                       # Event-dynamic system
          fillcolor = 'Snow4'

        dotfile.write('{} [style = {}, label = "{}" fillcolor = {}];\n' \
        .format(label, style, node.name, fillcolor))
      # EDGES
      for label, arc in self.arcs.items():
        arcColor = 'Black'
        arrowtype = 'arrowhead = normal'
        if arc.token == 'energy':
          arcColor = 'Firebrick1'
        if arc.type == 'bi-directional':
          arrowtype = 'arrowtail = onormal, dir = both'
        dotfile.write('{} -> {} [label = "{}", {}, color = {}];\n' \
        .format(arc.source, arc.sink, arc.name, arrowtype, arcColor))
      # FINISH FILE
      dotfile.write('}')

  def produceDot(self):
    os.system('dot -Tpdf {} > {}'.format(self.dotfile, self.pdffile))


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
    nmap = []
    nmapNode = []
    nmass = []
    nmassNode = []

    # Arc references
    amap = []
    amapArc = []
    amass = []
    amassArc = []

    # n
    for i, (label, node) in enumerate(self.nodes.items()):
      nmap.append(i)
      nmapNode.append(node)          # This is a strict copy of Node.___refs___
      print(node.tokens)
      if 'mass' in node.tokens:
        nmass.append(i)
        nmassNode.append(node)

    for i, (label, arc) in enumerate(self.arcs.items()):
      amap.append(i)
      amapArc.append(arc)
      if 'mass' == arc.token:
        amass.append(i)
        amassArc.append(arc)
      # if
    # Prepare the set sizes
    A.makeMapping(amap)
    A.makeBlocking([1] * np.size(amap))
    N.makeMapping(nmap)
    N.makeBlocking([1] * np.size(nmap))

    F  = self.makeMatrix(self.nodes, self.arcs)
    Fm = self.makeMatrix(nmassNode, amassArc)
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
    # print(indexSet)
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


class Arc(Graph):
  """
  Each arc included in the graph.
  """
  ___refs___ = []
  def __init__(self, label, dict):
    """
    Initiation of an arc object

    Args:
      label: The name of the arc used in the program
      dict:  Dictionary containing all the defined properties.
    """
    self.___refs___.append(self)
    self.label = label
    self.__dict__.update(**dict)


  def keys(self):
    self.__dict__.keys()

  def makeJsonObj(self):
    return json.dumps(self.__dict__)

class Species(Graph):
  """
  This class contain information about species in the graph
  """
  ___refs___ = []
  def __init__(self, label):
    self.___refs___.append(self)
    self.label = label


class Conversion(Graph):
  """
  This class contain information about token conversion in the graph
  """
  ___refs___ = []
  def __init__(self, reactants, products):
    self.___refs___.append(self)
    self.reactants = reactants
    self.products = products


###############################################################################
#                                 TESTING                                     #
###############################################################################

if __name__ == '__main__':
  # Common.indices.makeIndexFile()
  indices = Common.indices.getIndexes()
  exec(open('Common/indexSets.py').read())
  # print(A.aliases)
  g = Graph('TESTGRAPH')
  g.makeNodes()
  g.makeArcs()
  # g.makeIndex()
  g.makeDot()
  g.produceDot()
