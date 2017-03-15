
import numpy as np
###############################################################################
###############################################################################

def blockReduction(val1,size,val2):
  counter = 0
  value = []
  for l in size:
    valll1 = val1[counter:counter+l]
    valll2 = val2[counter:counter+l]
    value.append(np.einsum('ij,ij -> j',valll1 ,valll2))
    counter += l
  return np.array(value)

###############################################################################
###############################################################################

###############################################################################
#   KHATRI RAO PRODUCT RELATED FUNCTIONS                                      #
###############################################################################
def mkblocks(mat,size):
  """MAKING EM BLOCKS"""
  matrices = []
  currow = 0
  mat = np.array(mat)
  for nspecies in size[0]:
    curcol = 0
    for aspecies in size[1]:
      matrices.append(mat[currow:(currow+nspecies),curcol:(curcol+aspecies)])
      curcol += aspecies
    currow += nspecies
  return matrices
###############################################################################
def kr(mata, sizea, matb, sizeb):
  """
  mata and matb are the matrices that are multiplied. The sizes of these
  matrices are the block matrices. The blocks are defined as a list. Example:
  F_{NS,AS} -> size(F_{NS,AS}) = (1,1,2,2) x (1,1,2)
  """
  matsA, matsB = [mkblocks(mat,size) for (mat,size) in zip([mata,matb],[sizea,sizeb])]
  matrices = np.array([np.kron(A,B) for (A, B) in zip(matsA, matsB)])
  size = (len(sizea[0]),len(sizea[1]))
  mat = np.concatenate([np.concatenate(matrices[node*size[1]:node*size[1]+size[1]], axis = 1) for node in range(size[0])],axis = 0)
  return mat

###############################################################################
