#!/usr/bin/env python3

"""
What:    Graph object implemention
Author:  Arne Tobias Elve
Since:   2017-06-28
Where:   Department of Chemical Engineering
Contact: arne.t.elve(at)ntnu.no
Why:     To test the new object stucture before implemention into OntoSim.  The
         idea is to generate the index sets automatically based on the list of
         nodes and list of arcs. This can be used for the automatic model
         reduction that eventually will come.
Update:  2017-06-28
"""

from objects import *
import json

"""comment"""


fileLoc = 'Common/batch_01_tokens.json'

with open(fileLoc) as data_file:
  data = json.load(data_file)
  print(data['nodes'])
