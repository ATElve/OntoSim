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
from time import strftime, time                              # Library for time

def getIndexes():
  """This function returns index sets as a dictionary"""
  return Common.configuration_file.ConfigFile('Common/indices.cfg').read()

def makeIndexFile():
  with open('Common/indexSets.py','w') as indexFile:
    # Introduction to the file
    purpose = '#\t Purpose: Prepare the index sets'
    author =  '#\t Author:  Arne Tobias Elve'
    date =    '#\t When:    {}'.format(strftime("%Y-%m-%d %H:%M:%S"))
    reason =  '#\t Why:     To make the index sets with correct names'
    indexFile.write('#'*79+'\n')
    indexFile.write('{0:78}#\n'.format(purpose))
    indexFile.write('{0:78}#\n'.format(author))
    indexFile.write('{0:78}#\n'.format(date))
    indexFile.write('{0:78}#\n'.format(reason))
    indexFile.write('#'*79+'\n')
    indices = getIndexes()                            # Retrieve the index file
    for key in indices.keys():
      indexset = indices[key]['aliases'][0][1]
      indexFile.write('{} = IndexSet(indices["{}"])\n'.format(indexset, key))
      # indexFile.write(indices[key]['aliases'][0][1]+' = IndexSet(indices["'+ key +'"])\n')
      # print(indices[key]['aliases'][0][1])
# node = IndexSet(test['node'])
# print(dir(OntoSim))
