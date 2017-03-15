"""
..  module:: Operators
    :platform: Unix, Windows
    :synopsis: Template for executable code operators.

.. moduleauthor:: Arne Tobias Elve <arne.t.elve@ntnu.no>

.. date:: 2017-03-03

.. contents:: - Add
              - Subtract
              - Reduce product
              - Expand product
              - Khatri-Rao product
              - Power
              - Unitary functions::
                - sqrt
                - inv
                - sin
                - cos
                - abs
              - Select
              - Set

.. notes::    (2017-03-03) second version of operator file
              (2017-03-06) implemented unitary functions
"""

import numpy as np                                     # NUMPY numerical python
from objects import *           # Import variable, tempvariable and collections
from operatorImplementation import *           # Self made additional operators
import myerrors                                          # My error definitions

# --------------------------------------------------------------------------- #
# BINARY OPERATORS                                                            #
# --------------------------------------------------------------------------- #

# --------------------------------------------------------------------------- #
def add(var1, var2):
  """
  Adding two variables. Either by expressions or by value.

  Args:
    var1:  First variable
    var2:  Second variable

  Returns:
    Executable object  containing  expression   and index adding  the variables
  """
  instances = var1.instances+var2.instances
  if var1.index[0] == var2.index[0]:
    ex = lambda: np.add(var1.get(), var2.get())
  else:
    ex = lambda: np.add(var1.get(), np.transpose(var2.get()))
  return Executable(ex, var1.index, instances)
# --------------------------------------------------------------------------- #

# --------------------------------------------------------------------------- #
def subtract(var1, var2):
  """
  Subtracting a variables from another.  Either by expressions or by value.

  Args:
    var1:  First variable
    var2:  Second variable

  Returns:
    Executable object  containing expression  and index subtract  the variables
  """
  instances = var1.instances+var2.instances
  if var1.index[0] == var2.index[0]:                              # check shape
    ex = lambda: np.subtract(var1.get(), var2.get())
  else:
    ex = lambda: np.subtract(var1.get(), np.transpose(var2.get()))
  return Executable(ex, var1.index, instances)
# --------------------------------------------------------------------------- #

# --------------------------------------------------------------------------- #
def reduceproduct(var1, redSet, var2):
  """
  reduce -- one of the components of the space is eliminated, the space shrinks
  for the indicated dimension.

  red1  and red2  implement  standard matrix/vector multiplication rules though
  with  the index  order  not  to  be fixed.   This  approach is using Einstein
  indexing, with the reduction dimension explicitly shown in contrast  to being
  implied in standard paper linear algebra notation.
  red3 provides a block by block operation -- a blockwise scalar product.

  Args:
    var1:   First variable
    var2:   Second variable
    redSet: Space which is being reduced

  Returns:
    Executable object containing executable expression
  """
  instances = var1.instances+var2.instances

  index1 = var1.index
  index2 = var2.index
  trsp = np.transpose                       # Make functions fit within 79 chrs
  es = np.einsum                            # Make functions fit within 79 chrs

  if redSet not in index1 or redSet not in index2:
    ex = lambda: blockReduction(var1.get(), index1[0].blocking, var2.get())
    index = [index1[0].sets[0]]
    return Executable(ex, index, instances)

  elif set(index1) == set(index2) or len(index1) == 1 or len(index2) == 1:
    """Check if index sets are same set or the same,  or completely reduced."""
    if index1[0] == redSet:
      if index2[0] == redSet:
        ex = lambda: trsp(es('ri,ri -> i', var1.get(), var2.get())[np.newaxis])
      else:
        ex = lambda: trsp(es('ri,ir -> i', var1.get(), var2.get())[np.newaxis])
    else:
      if index2[0] == redSet:
        ex = lambda: trsp(es('ir,ri -> i', var1.get(), var2.get())[np.newaxis])
      else:
        ex = lambda: trsp(es('ir,ir -> i', var1.get(), var2.get())[np.newaxis])

  else:
    """Two matrices with different sets"""
    if index1[0] == redSet:
      if index2[0] == redSet:
        ex = lambda: np.einsum('ri,rj -> ij',var1.get(),var2.get())
      else:
        ex = lambda: np.einsum('ri,jr -> ij',var1.get(),var2.get())
    else:
      if index2[0] == redSet:
        ex = lambda: np.einsum('ir,rj -> ij',var1.get(),var2.get())
      else:
        ex = lambda: np.einsum('ir,jr -> ij',var1.get(),var2.get())

  setindex = filter(lambda ind: ind != redSet, var1.index+var2.index)
  index = []
  [index.append(ind) for ind in setindex if ind not in index]
  return Executable(ex, index, instances)

# --------------------------------------------------------------------------- #

def expandproduct(var1, var2):
  """
  Expand product

  The space  it expanded  to the maximal  space given  the two set of in dices.
  Patterns:
    N . N = N
    [] . X = X
    X . X,Y = X,Y
    X,Y . Y = X,Y

  Args:
    var1:  First variable
    var2:  Second variable

  Returns:
    Executable object containing expression and index set for  the expand prod.
  """
  instances = var1.instances+var2.instances
  # PATTERN 1 or 2
  if var1.index == var2.index or var1.index == [] or var2.index == []:
    ex = lambda: np.multiply(var1.get(),var2.get())
    if var1.index == []:                              # Which index do I select
      index = var2.index
    else:
      index = var1.index

  elif var1.index == reversed(var2.index):                     # Transpose last
    index = var1.index                                     # No change in index
    ex = lambda: np.multiply(var1.get(),np.transpose(var2.get()))

  # PATTERN 3 and 4
  else:
    """If pattern 3 or 4"""
    if var1.index[0] == var2.index[0]:
      """Share first dimension"""
      ex = lambda: np.array(var1.get())*np.array(var2.get())
      if len(var1.index) == 1:
        index = var2.index
      else:
        index = var1.index
    else:
      if len(var1.index) > 1:
        index = var1.index
        ex = lambda: np.einsum('ij,jk -> ij',var1.get(),var2.get())
      else:
        index = var2.index
        ex = lambda: np.einsum('ij,hi -> hi',var1.get(),var2.get())

  return Executable(ex, index, instances)
# --------------------------------------------------------------------------- #

# --------------------------------------------------------------------------- #
def khatriRaoProduct(var1, var2):
  """
  Khatri-Rao product, the block-by-block Kronecker product

  Since we  operate with  block matrices  and block equations  we introduce the
  Khatri-Rao in order to write the equations and products more elegantly.
  Patterns:
  N,A : NS,AS ==> NS,AS
  NS,A : N,AS ==> NS,AS

  N   : NS,AS ==> NS,AS
  NS,AS : N   ==> NS,AS
  A   : NS,AS ==> NS,AS
  NS,AS : A   ==> NS,AS

  A : AS      ==> AS
  AS : A      ==> AS

  Args:
    var1:  First variable
    var2:  Second variable

  Returns:
    Executable  object containing expres. and  index.  Block  Kronecker  multi.
  """

  flip = False                           # Flag for transposing second variable
  index = var2.index        # Index usually set to the last set for some reason
  # TODO make sure the product is correct! Appears to be wrong!

  instances = var1.instances+var2.instances
  # DETERMINE THE SIZES OF THE BLOCKING>>>
  sizea = [settet.blocking for settet in var1.index]
  sizeb = [settet.blocking for settet in var2.index]

  if len(var1.index) == 2 and len(var2.index) == 2:           # Pattern 1 and 2
    for i in [0, 1]:
      for j in [0, 1]:
        if var1.index[i] in var2.index[j].sets:
          # index[i] = var2.index[j] OBSOLETE
          if i != j:
            flip = True                            # Flipping the last variable
        elif var2.index[j] in var1.index[i].sets:
          index[i] = var1.index[j]
          if i != j:
            flip = True

          # continue
  elif len(var1.index) == 1 and len(var2.index) == 2: # Pattern 3, 4
    print('TEST THIS')
    # index = var2.index
    # for j in [0, 1]:
    if var1.index[0] in var2.index[0].sets:
      # index = var2.index
      pass
    elif  var2.index[0] in var1.index[0].sets:
      index[0] = var1.index[0]
    elif var1.index[0] in var2.index[1].sets:
      flip = True
      # index[1] = var2.index
    elif  var2.index[1] in var1.index[0].sets:
      index[1] = var1.index[0]
      flip = True

  elif len(var1.index) == 2 and len(var2.index) == 1:
    index = var1.index
    if var2.index[0] in var1.index[0].sets:
      # index = var1.index
      pass
    elif  var1.index[0] in var2.index[0].sets:
      index[0] = var2.index[0]
    elif var2.index[0] in var1.index[1].sets:
      flip = True
      # index[1] = var1.index
    elif  var1.index[1] in var2.index[0].sets:
      index[1] = var2.index[0]
      flip = True

  elif len(var1.index) == 1 and len(var2.index) == 1: # Pattern 5 and 6
    # index = var2.index
    if var1.index[0] in var2.index[0].sets:
      index = var2.index
    else:
      index = var1.index
  else:
    print('NOT CAPTURED ANY ALTERNATIVES')
  # print([ind.symbol for ind in index])
  # Making matrix out of single vectors:
  # TODO FIX USE TUPLES
  if len(sizea) == 1 and len(sizeb) == 1:
    sizea.append([1])
    sizeb.append([1])
  elif len(sizea) == 1 and len(sizeb) != 1:
    sizea.append([1])
    print('HERE')
    # THIS DOES NOT WORK for the current case
    sizeb[1] = list([sum(sizeb[1])])
  elif len(sizeb) == 1 and len(sizea) != 1:
    sizeb.append((1,))
    sizea[1] = list([sum(sizea[1])])
  if flip:
    print('WE ARE FLIPPIN!')
    index = reversed(index)
    ex = lambda: kr(var1.get(),sizea, np.transpose(var2.get()), sizeb[::-1])
  else:
    ex = lambda: kr(var1.get(),sizea, var2.get(), sizeb)

  return Executable(ex, index, instances)

# --------------------------------------------------------------------------- #
# --------------------------------------------------------------------------- #
#      SET OPERATORS                                                          #
# --------------------------------------------------------------------------- #

def sett(var):
  """
  Make a reference value of the variable

  Keep  the units of  the initial variable.  Make a reference value  containing
  only ones in the vector space.  Used  to remove the units  in the var object.

  Args:
    var: Variable object

  Returns:
    Executable object containing expression and index to make the set variable.
  """
  instances = [inst for inst in var.instances]
  ex = lambda: np.ones(np.shape(var.get()))
  index = var.index
  return Executable(ex, index, instances)

# --------------------------------------------------------------------------- #

def select(var, superset, subset):
  """
  Select a certain sub set of the superset.

  Selects the rows and columns of the variable  according to the the mapping of
  the subset with respect to the superset.

  Args:
    var:      The variable
    superset: The superset in which the mapping occurs.
    subset:   The subset describing which vector space to select.

  Returns:
    Executable object  containing  expression   and index adding  the variables
  """
  # Check and change index set if directly replaceable
  if superset in var.index:
    index = [indSet if indSet != superset else subset for indSet in var.index]
  else:                                         # If selecting in combined sets
    index = [ind for ind in var.index]
    for i,ind in enumerate(var.index):
      if superset in ind.sets:
        sets = list(map(lambda x:x if x!= superset else subset, ind.sets))
        index[i] = list(filter(lambda x: x.sets == sets, ind.indexingSets))[0]

  # If subset is empty
  if subset.mapping == []:
    ex = lambda: []                                 # No occurrence of this set

  # If first index is the superset
  elif var.index[0].superset == superset:
    selectionSet = []
    counter = 0
    for i,curlen in enumerate(var.index[0].blocking):
      if i in subset.mapping:
        selectionSet += range(counter,counter+curlen)
      counter += curlen
    ex = lambda: np.array(var.get())[selectionSet]

  # If matrix and second dimension is selected mapping
  elif var.index[1].superset == superset:
    selectionSet = []
    counter = 0
    for i,curlen in enumerate(var.index[1].blocking):
      if i in subset.mapping:
        selectionSet += range(counter,counter+curlen)
      counter += curlen
    ex = lambda: np.array(var.get())[:,np.array(selectionSet)]

  else:                                              # No alternatives captured
    raise myerrors.SetError(superset, subset)
    ex = lambda: 0

  instances = [inst for inst in var.instances]
  return Executable(ex, index, instances)


# --------------------------------------------------------------------------- #
# --------------------------------------------------------------------------- #
#      UNITARY FUNCTIONS                                                      #
# --------------------------------------------------------------------------- #

def abs(var):
  """
  Element absolute value

  Unitary function, require no units.

  Args:
    var: Variable

  Returns:
    Executable object with expression and index sets
  """
  ex = lambda: np.fabs(var.get())
  instances = [inst for inst in var.instances]
  return Executable(ex, var.index, instances)


# --------------------------------------------------------------------------- #

def exp(var):
  """
  Element exponential product

  Unitary function, require no units.

  Args:
    var: Variable

  Returns:
    Executable object with expression and index sets
  """
  ex = lambda: np.exp(var.get())
  instances = [inst for inst in var.instances]
  return Executable(ex, var.index, instances)

# --------------------------------------------------------------------------- #

def inv(var):
  """
  Element inv product

  Unitary function, require no units.

  Args:
    var: Variable

  Returns:
    Executable object with expression and index sets
  """
  ex = lambda: 1. / np.array(var.get())
  instances = [inst for inst in var.instances]
  return Executable(ex, var.index, instances)

  # print('inv index = ',var.index) return Executable(ex, var.index)

# --------------------------------------------------------------------------- #

def sign(var):
  """
  Element inv product

  Unitary function, require no units.

  Args:
    var: Variable

  Returns:
    Executable object with expression and index sets
  """
  ex = lambda: np.sign(var.get())
  instances = [inst for inst in var.instances]
  return Executable(ex, var.index, instances)


# --------------------------------------------------------------------------- #

def cos(var):
  """
  Element cos

  Unitary function, require no units.

  Args:
    var: Variable

  Returns:
    Executable object with expression and index sets
  """
  ex = lambda: np.cos(var.get())
  instances = [inst for inst in var.instances]
  return Executable(ex, var.index, instances)


# --------------------------------------------------------------------------- #

def sin(var):
  """
  Element sin

  Unitary function, require no units.

  Args:
    var: Variable

  Returns:
    Executable object with expression and index sets
  """
  ex = lambda: np.sin(var.get())
  instances = [inst for inst in var.instances]
  return Executable(ex, var.index, instances)


# --------------------------------------------------------------------------- #

def sqrt(var):
  """
  Element square root

  Unitary function, require no units.

  Args:
    var: Variable

  Returns:
    Executable object with expression and index sets
  """
  ex = lambda: np.sqrt(var.get())
  instances = [inst for inst in var.instances]
  return Executable(ex, var.index, instances)


# --------------------------------------------------------------------------- #

def ln(var):
  """
  Natural logarithm

  Unitary function, require no units.

  Args:
    var: Variable

  Returns:
    Executable object with expression and index sets
  """
  ex = lambda: np.log(var.get())
  instances = [inst for inst in var.instances]
  return Executable(ex, var.index, instances)


# --------------------------------------------------------------------------- #
#      Not fully implemented with math, but handle index and instancing       #
# --------------------------------------------------------------------------- #

# def diff(var1):
#   """
#   Natural logarithm
#
#   Unitary function, require no units.
#
#   Args:
#     var: Variable
#
#   Returns:
#     Executable object with expression and index sets
#   """
#   ex = lambda: np.log(var.get())
#   instances = [inst for inst in var.instances]
#   return Executable(ex, var.index, instances)

# --------------------------------------------------------------------------- #
#      Unit test                                                              #
# --------------------------------------------------------------------------- #

if __name__ == '__main__':
  N =  IndexSet( 'N', mapping = [0, 1, 2],blocking = [1, 1, 1])
  A =  IndexSet( 'A', mapping = [0, 1], blocking = [1, 1])
  S =  IndexSet( 'S', mapping = [0, 1], blocking = [1, 1])
  NS = IndexSet('NS', mapping = [0, 1, 2], blocking =[2, 2, 2], sets = [N, S], superset = N)
  AS = IndexSet('AS', mapping = [0,1], blocking = [2, 2], sets = [A, S], superset = A)
  Nv = IndexSet('Nv', mapping = [0, 2], blocking = [1, 1], superset = N)
  Av = IndexSet('Av', mapping = [1], blocking = [1], superset = A)
  NvS = IndexSet('NvS', mapping = [0, 2], blocking = [2, 2], sets = [Nv, S], superset = N)
  AvS = IndexSet('AvS', mapping = [1], blocking = [2], sets = [Av, S], superset = A)

  var1 = Variable('var1', 'testvariable', 'constant', [1]*8, [N])
  var2 = Variable('var2', 'testvariable', 'constant', [1]*8, [N])
  var3 = Variable('var3', 'testvariable', 'constant', [1]*8, [N, A])
  var4 = Variable('var4', 'testvariable', 'constant', [1]*8, [A, N])
  var5 = Variable('var5', 'testvariable', 'constant', [1]*8, [NS])
  var6 = Variable('var6', 'testvariable', 'constant', [1]*8, [NS, A])
  var7 = Variable('var7', 'testvariable', 'constant', [1]*8, [NS, AS])

  var1.value = np.array([[1],[2],[3]])
  var2.value = np.array([[1],[2],[3]])
  var3.value = np.array([[1,1],[2,2],[3,3]])
  var4.value = np.transpose([[-1,1],[2,2],[3,3]])
  var5.value = np.array([[1], [2], [3], [4], [5], [6]])
  var6.value = np.array([[1,1], [2,1], [3,1], [4,1], [5,1], [6,1]])
  var7.value = np.array([[1,1,1,1], [2,1,1,-1], [3,1,1,0], [4,1,1,2], [5,1,3,2], [6,1,1,4]])


  tmp = expandproduct(var4,add(var1,var2))
  print([i.symbol for i in tmp.index])
  print([v.symbol for v in tmp.instances])
  print(tmp.instances)
  print(tmp.ex())
