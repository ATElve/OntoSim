'''=============================================================================
    cofiguration_file
   =============================================================================

 a facility to handle configuration files

@author: Preisig, H A
@since: 2007-10-29
@change: 2014-12-09 Preisig, H A  ordered dictionary
@change: 2014-12-09 Preisig, H A  allow for comments #comment
@change: 2014-12-09 Preisig, H A  allow for . in section name
@change: 2015-01-07 Elve, A T     added write member function
@change: 2015-05-04 Elve, A T     added option function 
@change: 2016-02-16 Preisig, H A  added evaluation option
@change: 2016-04-09 Preisig, H A  changed to rhs of item either string or
                                    list of strings

'''

# imports ------------------- -------------------------------------------------

# from __future__ import with_statement
import os as OS
from collections import OrderedDict
import re as RE

SECTION_PATTERN = RE.compile('\[.*\]')   # HAP 2016-04-03 generalised
LIST_PATTERN = RE.compile('\[.*\]')   # HAP 2016-04-09 generalised
TOKEN_EQUAL = RE.compile('=')
TOKEN_COMMENT = RE.compile('#')



# error handling --------------------------------------------------------------
class ConfigError(Exception):
  '''
  Exception reporting
  '''

  def __init__(self, msg):
    self.msg = msg

  def __str__(self):
    return ">>> %s" % self.msg


# body ------------------------------------------------------------------------


class ConfigFile():
  def __init__(self, file_spec,  eval_variables=False):

    """
    A rewrite of the configuration file utility using ordered dictionaries
    and providing the option to evaluate the rhs os the variable definition.

    @param eval_variables: logical controlling evaluation of the rhs
    """
    self.eval_variables = eval_variables
    self.dictionary = OrderedDict()
    self.file_spec = file_spec

  def read(self):
    file_spec = self.file_spec
    if not OS.path.isfile(file_spec):
      raise ConfigError('no such initialisation file :' + file_spec)
    dictionary = OrderedDict()
    count = 0
    with open(file_spec) as file_spec:
      for line in file_spec:
        count = count + 1
        line.strip(' \n')
        if '#' in line:
          line = str(TOKEN_COMMENT.split(line)[0])
          # LOGGER.info('>>>>>>>> %s' % line)
        s = SECTION_PATTERN.match(line)
        if s != None:
          sec = s.group().strip('[]')
          # LOGGER.info('section %s' % sec)
          dictionary[sec] = OrderedDict()  # start a new section
        else:
          if count == 1:
            ConfigError('first line must be a section %s' % line)
            return
          l = TOKEN_EQUAL.split(line)
          if l == None:
            ConfigError('no such line', line)
          else:
            if len(l) == 2:
              k = l[0].strip(' ')
              v = l[1].strip(' \n')
              s_ = LIST_PATTERN.match(v)
              if s_ or self.eval_variables:
                dictionary[sec][k] = eval(v)
              else:
                dictionary[sec][k] = v
    return dictionary

  def options(self, section):
    """Return a list of option names for the given section name."""
    try:
      opts = self.read(self.file_spec)[section]
    except KeyError:
      raise ConfigError("No section in file named: %s" % (section))
    return [opt for opt in opts]

  def sections(self):
    """Return a list of section names for the given file."""
    try:
      sections = self.read(self.file_spec)
    except IOError:
      raise ConfigError("No initiation file named: %s" % (self.file_spec))
    return [section for section in sections]

  def write(self):
    with open(self.file_spec, 'w') as configfile:
      if self.dictionary:
        # LOGGER.info('Saving to file: %s' % self.file_spec)
        for section in self.dictionary:
          configfile.write("[%s]\n" % section)
          for (key, value) in self.dictionary[section].items():
            nkey = " = ".join((str(key), str(value).replace('\n', '\n\t')))
            configfile.write("%s\n" % (nkey))
            # configfile.write("\n")
      else:
        ConfigError('Empty configuration dictionary')


if __name__ == '__main__':
  config = ConfigFile('process-modeller.ini')

  try:
    ini_config = config.read()
    for i in ini_config:
      print('\nsection: ', i)
      for j in ini_config[i]:
        print('  item : ', j)
  except ConfigError as m:
    print('failed :', m)

