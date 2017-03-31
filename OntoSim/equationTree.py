"""
..  module:: Equation tree
    :platform: Unix, Windows
    :synopsis: Analyse the equation tree

.. moduleauthor:: Arne Tobias Elve <arne.t.elve@ntnu.no>

.. date:: 2017-03-03
.. update:: 2017-03-30

.. contents:: - dept search first algorithm
              Equation: class representing the equation alternatives
              TreeVariable: class representing variables in the tree


.. notes::    (2017-03-09) second version of operator file
              (2017-03-30) added subclass of tree
"""

import matplotlib.pyplot as plt                                    # Matplotlib
# import networkx as nx                                              # Networkx
from time import asctime, localtime, time                    # Library for time

class Equation(object):
  """Equation representation in the equation graph"""
  def __init__(self, symbol, alternative, exe):
    self.symbol = symbol
    self.alternative = alternative
    self.ex = exe
    self.type = 'equation'
    self.select = True                                # Flag to select equation

  def __str__(self):
    return self.symbol

class TreeVariable(object):
  """Representation of variable in tree"""
  def __init__(self, var, given = False):
    self.var = var
    self.symbol = var.symbol
    self.type = var.type
    self.equations = var.equations
    self.given = given                                 # Flag to check if given

class EquationsTree(object):
  """docstring for EquationsTree."""
  def __init__(self, treename, initialVar):
    self.treename = treename
    self.initialVar = initialVar
    self.equations = {}
    self.variables = {}
    self.variables[self.initialVar.symbol] = self.initialVar
    self.tree = self.buildTree([],[TreeVariable(self.initialVar)],self.initialVar)
    self.allElements = {**self.equations, **self.variables}
    # print(self.allElements.keys())
    # self.drawGraph()

    # self.makeDotGraph()
  def buildTree(self, tree, curpath, next):
    """Tree builder"""
    # equations = {}
    # self.variables = {}
    if next.equations:
      for i,eq in enumerate(next.equations):
        eqsymbol = 'eq'+str(i)+next.symbol
        if eqsymbol not in self.equations.keys():
          self.equations[eqsymbol] = Equation(eqsymbol, i, eq)
        curpath.append(self.equations[eqsymbol])
        # curpath.append(Equation(eqsymbol, i, eq))
        # self.equations.append(eq)
        for var in eq.instances:
          # print('var.symbol = ', var.symbol)
          if var in curpath or var.type == 'state':
            if var.symbol not in self.variables.keys():
              self.variables[var.symbol] = TreeVariable(var)
            curpath.append(self.variables[var.symbol])
            tree.append([var for var in curpath])
            curpath.pop()
          else:
            if var.symbol not in self.variables.keys():
              self.variables[var.symbol] = TreeVariable(var)
            curpath.append(self.variables[var.symbol])
            self.buildTree(tree,curpath,curpath[-1])
        curpath.pop()
      curpath.pop()
    else:
      tree.append([var for var in curpath])
      curpath.pop()
    # self.tree = tree
    return tree

  def drawGraph(self):
    """
    Make visual simple networkx Graph

    Uses the networkx library to generate a graph representing the variable and
    equation connections.
    THIS IS NOW OBSOLETE SINCE makeDotGraph is better.
    """
    G = nx.Graph()
    for path in self.tree:

      for a,b in zip(path[:-1], path[1:]):
        G.add_edge(a.symbol, b.symbol)

    pos=nx.spring_layout(G,iterations = 1000) # positions for all nodes

    # nodes
    nx.draw_networkx_nodes(G, pos, node_size=800)

    # edges
    nx.draw_networkx_edges(G,pos,edgelist=G.edges(),width=2)
    # nx.draw_networkx_edges(G,pos,edgelist=esmall,
                      # width=6,alpha=0.5,edge_color='b',style='dashed')

    # labels
    # nx.draw(G)
    nx.draw_networkx_labels(G,pos,font_size=10,font_family='sans-serif')

    plt.axis('off')
    # plt.savefig("weighted_graph.png") # save as png
    plt.show() # display

  def makeDotGraph(self):
    filename = './DOT/' + self.treename + '.dot'
    with open(filename,'w') as of:
      of.write('#'*79+'\n')
      of.write('#\t Purpose: Dot graph for equation tree.\n')
      of.write('#\t Author:  Arne Tobias Elve\n')
      of.write('#\t Date:    '+str(asctime( localtime(time()) ))+'\n')
      of.write('#\t Why:     Output to dot language \n')
      of.write('#'*79+'\n')
      of.write('graph G {\n')

      # INITIATE NODES
      alEls = []
      for path in self.tree:
        for el in path:
          if el.symbol in alEls:
            # print(el.symbol)
            continue
          shape = 'ellipse'
          if el.type == 'equation':
            of.write(el.symbol+' [style = filled, label = ' + str(el.alternative) +', shape = box, fillcolor = DeepPink];\n')
            alEls.append(el.symbol)
            continue
          if el.given:
            shape = 'doubleoctagon'
          if el.type == 'constant':
            of.write(el.symbol+' [style = filled, fillcolor = Tomato, shape = '+shape+'];\n')
          elif el.type == 'state':
            of.write(el.symbol+' [style = filled, fillcolor = Navy, fontcolor = White, shape = '+shape+'];\n')
          elif el.type == 'transport':
            of.write(el.symbol+' [style = filled, fillcolor = Cyan, shape = '+shape+'];\n')
          elif el.type == 'diffstate':
            of.write(el.symbol+' [style = filled, fillcolor = LawnGreen, shape = '+shape+'];\n')
          elif el.type == 'network':
            of.write(el.symbol+' [style = filled, fillcolor = Gold, shape = '+shape+'];\n')
          elif el.type == 'frame':
            of.write(el.symbol+' [style = filled, fillcolor = Red, shape = '+shape+'];\n')
          elif el.type == 'closure':
            of.write(el.symbol+' [style = filled, fillcolor = AntiqueWhite, shape = '+shape+'];\n')
          else:
            of.write(el.symbol+' [style = filled, fillcolor = White, shape = '+shape+'];\n')
          alEls.append(el.symbol)

      allPaths = []
      for path in self.tree:
        for a,b in zip(path[:-1], path[1:]):
          if (a.symbol,b.symbol) in allPaths:
            # print(a,b)
            continue
          else:
            of.write(a.symbol+' -- '+b.symbol+';\n')
            allPaths.append((a.symbol,b.symbol))
      of.write('}')

  def variableIndex(self):
    """
    Add a calculation index for each variable

    Args:
      None

    Results:
      Assign a selection vector to the index set of a variable
    """

class SubTree(EquationsTree):
  """
  Tree for a node or an arc
  """
  def __init__(self, treename, initialVar):

    self.treename = treename
    self.initialVar = initialVar
    self.equations = {}
    self.variables = {}
    self.variables[self.initialVar.symbol] = self.initialVar
    self.yggdrasil = self.buildTree([],[TreeVariable(self.initialVar)],self.initialVar)
    # self.allElements = {}                  # Collection of all elements in tree
    self.allElements = {**self.equations, **self.variables}
    print(self.allElements.keys())
    self.tree = [path for path in self.yggdrasil]

    self.buildGraphTree()
    # self.makeDotGraph()


  def buildGraphTree(self, tree = None):
    """make subtree"""
    variables = []
    equations = []
    # alElements = {}
    # print(self.allElements.keys())
    thisTree = []
    if not tree:
      tree = self.tree
    for path in tree:
      thisPath = []
      for el in path:
        thisPath.append(el)
        if el.type == 'equation':
          # if el.symbol not in alElements.keys():
            # self.allElements[el.symbol] = Equation(el.symbol, el.alternative, el.ex)
          # thisPath.append(alElements[el.symbol])
          if el.select == False:
            thisPath.pop()
            break
          equations.append(self.allElements[el.symbol])
          continue
        else: # Variable of some sort
          # if el.symbol not in self.allElements.keys():
            # self.allElements[el.symbol] = TreeVariable(el.var, el.given)
          # equations.append(self.allElements[el.symbol])
          # vara = TreeVariable(el.var)
          variables.append(self.allElements[el.symbol])
          # thisPath.append(vara)
        # thisPath.append(alElements[el.symbol])
        if el.type == 'constant' or el.type == 'network' or el.given:
          # Ensure that last element in path is constant or given.
          break
      if thisPath not in thisTree:
        thisTree.append([var for var in thisPath])
    self.tree = [path for path in thisTree]
    # self.alElements = alElements
    # return thisTree, variables, equations

  def setGivenVariableByName(self, symbol):
    """
    Select a variable to be given

    Args:
      symbol:  Unique symbol of the given variable

    Returns:
      Updated equation tree for this element.
    """
    self.allElements[symbol].given = True
    self.buildGraphTree()
    self.makeDotGraph()

  def unsetGivenVariableByName(self, symbol):
    """
    Select a variable to be given

    Args:
      symbol:  Unique symbol of the given variable

    Returns:
      Updated equation tree for this element.
    """
    self.allElements[symbol].given = False
    self.buildGraphTree(tree = self.yggdrasil)
    self.makeDotGraph()

  def selectEquationAlternative(self, var, alternative):
    """
    Select the equation alternative variable

    Args:
      var - variable
      alternative - alternative number

    Return:
      sets the equation locally as selected
    """
    pass
