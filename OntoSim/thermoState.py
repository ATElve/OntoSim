"""
..  module:: Thermo Library
    :platform: Unix, Windows
    :synopsis: Template for executable code operators.

.. moduleauthor:: Arne Tobias Elve <arne.t.elve@ntnu.no>

.. date:: 2017-05-02

.. contents:: -

.. notes::    (2017-05-02) Thermo now
"""
import cantera as ct
import numpy as np                                     # NUMPY numerical python

R_gas = 8.3145119843087
# --------------------------------------------------------------------------- #
# BINARY OPERATORS                                                            #
# --------------------------------------------------------------------------- #

# --------------------------------------------------------------------------- #
class Helmholtz(object):
  """
  Helmholtz energy surface object

  This object  defines  a Helmholtz energy surface based on  a canonical set of
  variables.
  """
  def __init__(self, species, phase):
    self.species = species          # Species as a list of strings ['Al','CO2']
    self.phase = phase                                        # Phase as string

  def stateIG(self, T, V, N):
    """
    Calculate state of phase based  on T, V, N - ensemble using ideal  gas  law

    Calculation of thermodynamic state using ideal gas law as equation of
    state.

    Args:
      T:  Temperature
      V:  Volume
      N:  Amount vector in moles

    Returns:
      Calculate entropy, pressure,  chemical potential, Helmholtz--energy using
      ideal gas law.
    """
    self.T = T
    self.V = V
    self.N = N
    self.pig = sum(N)*T*R_gas/V
    self.muig = self.mu_0 \
              + np.multiply(R_gas*T,np.log(np.multiply(N,(R_gas*T/(V*self.p_o)))))
    self.Aig = -self.pig*self.V+sum(np.multiply(self.muig, self.N))
    self.Sig = sum(N) * R_gas * np.log(sum(N) * R_gas * T / V * self.p_o)
# --------------------------------------------------------------------------- #


# --------------------------------------------------------------------------- #
#      Unit test                                                              #
# --------------------------------------------------------------------------- #

if __name__ == '__main__':
  gas = Helmholtz(['A','B'],'gas')
  gas.p_o = 100000
  gas.mu_0 = np.array([[10000],[12000]])
  gas.stateIG(298,1,np.array([[2400],[2500]]))
  print(gas.Aig)
  print(gas.Sig)
  print(gas.muig)
