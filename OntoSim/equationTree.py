"""
..  module:: Equation tree
    :platform: Unix, Windows
    :synopsis: Analyse the equation tree

.. moduleauthor:: Arne Tobias Elve <arne.t.elve@ntnu.no>

.. date:: 2017-03-03

.. contents:: - dept search first algorithm
              Equation: class representing the equation alternatives


.. notes::    (2017-03-09) second version of operator file
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

  def __str__(self):
    return self.symbol

class TreeVariable(object):
  """Representation of variable in tree"""
  def __init__(self, var):
    self.var = var
    self.symbol = var.symbol
    self.type = var.type
    self.equations = var.equations
    self.given = False                                 # Flag to check if given



class EquationsTree(object):
  """docstring for EquationsTree."""
  def __init__(self, treename, initialVar):
    self.treename = treename
    self.initialVar = initialVar
    self.tree = self.buildTree([],[TreeVariable(self.initialVar)],self.initialVar)

    # self.drawGraph()
    self.makeDotGraph()

  def buildTree(self, tree, curpath, next):
    """Tree builder"""
    equations = {}
    variables = {}
    if next.equations:
      for i,eq in enumerate(next.equations):
        eqsymbol = 'eq'+str(i)+next.symbol
        if eqsymbol not in equations.keys():
          equations[eqsymbol] = Equation(eqsymbol, i, eq)
        curpath.append(equations[eqsymbol])
        # curpath.append(Equation(eqsymbol, i, eq))
        # equations.append(eq)
        for var in eq.instances:
          # print('var.symbol = ', var.symbol)
          if var in curpath or var.type == 'state':
            if var.symbol not in variables.keys():
              variables[var.symbol] = TreeVariable(var)
            curpath.append(variables[var.symbol])
            tree.append([var for var in curpath])
            curpath.pop()
          else:
            if var.symbol not in variables.keys():
              variables[var.symbol] = TreeVariable(var)
            curpath.append(variables[var.symbol])
            self.buildTree(tree,curpath,curpath[-1])
        curpath.pop()
      curpath.pop()
    else:
      tree.append([var for var in curpath])
      curpath.pop()
    return tree

  def buildGraphTree(self, tree, curpath, next):
    variables = []
    equations = []
    thisTree = []
    for path in self.tree:
      thisPath = []
      for el in path:
        if el.type == 'equation':
          equa = Equation(el.symbol,el.alternative,el.ex)
          thisPath.append(equa)
          equations.append(equa)
        else: # Variable of some sort
          vara = TreeVariable(el.var)
          variables.append(vara)
          thisPath.append(vara)


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
          shape = 'ellipse'
          # if el.symbol in alEls:
            # print(el.symbol)
            # continue
          if el.type == 'equation':
            of.write(el.symbol+' [style = filled, label = ' + str(el.alternative) +', shape = box, fillcolor = DeepPink];\n')
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
            print(a,b)
            continue
          else:
            of.write(a.symbol+' -- '+b.symbol+';\n')
            allPaths.append((a.symbol,b.symbol))
      of.write('}')
