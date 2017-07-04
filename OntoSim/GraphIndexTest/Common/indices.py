#!/usr/bin/env python3

"""
What:    Index set file.
Author:  Arne Tobias Elve
Since:   2017-06-30
Where:   Department of Chemical Engineering
Contact: arne.t.elve(at)ntnu.no
Why:     File to initiate the index sets
Update:  2017-06-30
"""


import OntoSim
import sys
sys.path.append('..')
import Common.configuration_file
from objects import *
from time import asctime, localtime, time                    # Library for time




def getIndexes():
  """This function returns index sets as a dictionary"""
  return Common.configuration_file.ConfigFile('Common/indices.cfg').read()


# from objects import *
def makeIndexFile():
  with open('indexSets.py','w') as indexFile:
    indexFile.write('#'*79+'\n')
    indexFile.write('#\t Purpose: Prepare the index sets\n')
    indexFile.write('#\t Author:  Arne Tobias Elve\n')
    indexFile.write('#\t Date:    '+str(asctime( localtime(time()) ))+'\n')
    indexFile.write('#\t Why:     To make the index sets with correct names\n')
    indexFile.write('#'*79+'\n')
    indices = getIndexes()
    for key in indices.keys():
      indexFile.write(indices[key]['aliases'][0][1]+' = IndexSet(indices["'+ key +'"])\n')
      # print(indices[key]['aliases'][0][1])
# node = IndexSet(test['node'])
# print(dir(OntoSim))
