"""
..  module:: Errors
    :platform: Unix, Windows
    :synopsis: Error check and exception handling

.. moduleauthor:: Arne Tobias Elve <arne.t.elve@ntnu.no>

.. date:: 2017-03-07

.. contents:: - SetError

.. notes::    (2017-03-07) second version of operator file
"""

class SetError(Exception):
  """Something wrong with the index combinations"""
  def __init__(self, superset, subset = None, msg=None):
    if msg is None:
        # Set some default useful error message
        if subset:
          msg = "An error occurred in combination with set %s and %s" % superset, subset
        else:
          msg = "An error occurred in combination with set %s" % superset
    super(SetError, self).__init__(msg)
    self.set = set
