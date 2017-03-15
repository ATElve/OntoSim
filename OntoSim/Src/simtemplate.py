from time import asctime, localtime, time                    # Library for time


def generateClassTemplates(varlist, eqlist, filename):
  with open(filename,'w') as of:
    of.write('#'*79+'\n')
    of.write('#\t Purpose: Equation/initiation file for model\n')
    of.write('#\t Author:  Arne Tobias Elve\n')
    of.write('#\t Date:    '+str(asctime( localtime(time()) ))+'\n')
    of.write('#\t Why:     I want to make money on this\n')
    of.write('#\t Class:   '+filename+'\n')
    of.write('#'*79+'\n\n# VARIABLES THAT HAVE TO BE INITIATED:\n')

    for var in varlist:
      if var in eqlist:
        pass
      else:
        of.write(var.symbol +'.value = \n')
    of.write('\n# EQUATIONS IN SEQUENCE \n')
    for eq in eqlist:
      of.write(eq.symbol +'.value = '+eq.symbol+'.ex['+str(eq.selector)+']()\n')


# generateClassTemplates(varspace.transports,varspace.seqtransports,'VariableGroups/transport.py')
# generateClassTemplates(varspace.diffstates,varspace.seqdiffstates,'VariableGroups/diffstate.py')
# generateClassTemplates(varspace.constants,varspace.seqconstants,'VariableGroups/constant.py')
# generateClassTemplates(varspace.networks,varspace.seqnetworks,'VariableGroups/network.py')
# generateClassTemplates(varspace.closures,varspace.seqclosures,'VariableGroups/closure.py')
# generateClassTemplates(varspace.dynamics,varspace.seqdynamics,'VariableGroups/dynamic.py')
# generateClassTemplates(varspace.frames,varspace.seqframes,'VariableGroups/frame.py')
# generateClassTemplates(varspace.states,varspace.seqstates,'VariableGroups/state.py')
# generateClassTemplates(varspace.rest,varspace.seqrest,'VariableGroups/rest.py')
