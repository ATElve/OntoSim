"""
Purpose:  Collection of objects required in  the simulator and  the initiation.
Author:   Arne Tobias Elve
Contact:  arne.t.elve@ntnu.no
Since:    2016-11-24
Update:   2017-03-09
Contents: Variables()                             - Keep track of all variables
          Variable()                          - Keep track of a single variable
          Executable()                                   - A temporary variable
          IndexSet()                                    - A Index set framework


Comments: (2017-02-09) added  the  variables  class keeping track  of all the
          variables.
          (2017-02-27) added sequential list of the equations.
          (2017-03-03) removed the node and arc object.  They  were obsolete.
          (2017-03-09)
"""
import numpy as np

class Variables(object):
  """
  Collection of all variables

  This class is the collection of the variables. List of all types of variables
  and all equations sorted after type in sequence.
  """
  transports = []
  diffstates = []
  equations = []
  constants = []
  variables = []
  networks = []
  closures = []
  dynamics = []
  symbols = []
  states = []
  frames = []
  rest = []

  seqtransports = []
  seqdiffstates = []
  seqequations = []
  seqconstants = []
  seqvariables = []
  seqnetworks = []
  seqclosures = []
  seqdynamics = []
  seqsymbols = []
  seqstates = []
  seqframes = []
  seqrest = []

  def addVar(self, var):
    """
    Add variables to list of all variables.

    Evaluate  in which  variable group each variable belong.  Symbols added for
    practical purposes. Variables to keep the calculation sequence
    """
    self.symbols.append(var.symbol)
    self.variables.append(var)
    if var.type == 'transport':
      self.transports.append(var)
    elif var.type == 'diffstate':
      self.diffstates.append(var)
    elif var.type == 'constant':
      self.constants.append(var)
    elif var.type == 'network':
      self.networks.append(var)
    elif var.type == 'closure':
      self.closures.append(var)
    elif var.type == 'dynamic':
      self.dynamics.append(var)
    elif var.type == 'symbol':
      self.symbols.append(var)
    elif var.type == 'state':
      self.states.append(var)
    elif var.type == 'frame':
      self.frames.append(var)
    else:
      self.rest.append(var)

  def addEquation(self, var):
    """
    Add list of equations 
    """
    self.symbols.append(var.symbol)
    self.seqvariables.append(var)
    if var.type == 'transport':
      self.seqtransports.append(var)
    elif var.type == 'diffstate':
      self.seqdiffstates.append(var)
    elif var.type == 'constant':
      self.seqconstants.append(var)
    elif var.type == 'network':
      self.seqnetworks.append(var)
    elif var.type == 'closure':
      self.seqclosures.append(var)
    elif var.type == 'dynamic':
      self.seqdynamics.append(var)
    elif var.type == 'symbol':
      self.seqsymbols.append(var)
    elif var.type == 'state':
      self.seqstates.append(var)
    elif var.type == 'frame':
      self.seqframes.append(var)
    else:
      self.seqrest.append(var)

class Variable(Variables):
  """A variable"""
  variable = True       # Flag to separate variables from intermediate variable
  def __init__(self, symbol, documentation, type, units, index):
    self.documentation = documentation
    self.symbol = symbol
    self.index = index
    self.units = units
    self.selector = 0
    self.value = None
    self.get = lambda: self.value
    self.type = type
    self.ex = []
    self.instances = [self]           # Adds the variable to the instances list
    self.equations = []

    self.addVar(self)

  def makeExecuteable(self, exe):
    if self.index == exe.index:
      self.ex.append(exe.ex)
    else:
      self.ex.append(lambda : np.transpose(exe.ex()))
    self.addEquation(self)                  # Add equation to list of equations
    self.equations.append(exe)

  def updateValue(self):
    self.value = self.ex[self.selector]()

  def __str__(self):
    return self.symbol

class Executable(object):
  """Intermidiate variables"""
  variable = False

  def __init__(self, ex, index, instances):
    self.index = index
    self.ex = ex
    self.get = ex
    self.instances = instances

  def __str__(self):
    return 'Termporary variable with the index sets: '+ str([ind.symbol for ind in self.index])


class IndexSet(object):
  """Each index set connected to the variable"""
  indexingSets = []                             # All indexing sets in sequence
  def __init__(self,  symbol,                                   # UNIQUE SYMBOL
                      mapping = [],               # MAPPING OVER TO TO SUPERSET
                      superset = None,                 # PART OF WITCH SUPERSET
                      sets = [],                    # COMBINATION OF WHICH SETS
                      blocking = [],                         # BLOCK DEFINITION
              ):
    self.blocking = blocking
    self.superset = superset
    self.symbol = symbol
    self.mapping = mapping
    self.sets = sets
    if superset == None:
      self.superset = self
    self.indexingSets.append(self)

  def printSet(self):
    print('symbol = ', self.symbol)

  def __str__(self):
    return self.symbol
