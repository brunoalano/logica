# -*- coding: utf-8 -*-

"""
Logica Script Language
~~~~~~~~~~~~~~~~~~~~~~

A small parsing library and software that allows process
the propositional logic using the logical operators of
implication, and, or and not.

You can assign values as 0 or 1 to variables, meaning the
true and false.

:copyright: (c) 2015 by Bruno Alano Medina
:license: LGPL, see LICENSE file for more informations

"""

# Python Parsing Library
import pyparsing
from pyparsing import Word, alphas, Literal, oneOf, opAssoc, infixNotation
import collections

# Store the variables values
values = collections.defaultdict(lambda: 0)

class Operand(object):
  '''
  Manipulates the Variables

  This method will run when some variable are requested
  by the parser, looking for it value on our global values
  database

  '''

  def __init__(self, t):
    # Load the label name
    self.label = t[0]

    # Check if the label are a number, so, this number
    # represents its value
    if self.label in ['0', '1']:
      self.value = int(self.label)
    else:
      # Look for it value on the global storage
      self.value = values[t[0]]

  def __bool__(self):
    return self.value

  def __str__(self):
    return self.label

  __repr__ = __str__
  __nonzero__ = __bool__

class LogicalOperation(object):
  def __init__(self,t):
    self.args = t[0][0::2]
    self.apply(*self.args)

  def __str__(self):
    sep = " %s " % self.symbol
    return "(" + sep.join(map(str,self.args)) + ")"

  __repr__ = __str__

class LogicalAnd(LogicalOperation):
  # Setup the symbol
  symbol = '&&'

  def apply(self, a, b):
    return bool(a.value) and (b.value)

class LogicalOr(LogicalOperation):
  # Setup the symbol
  symbol = '||'

  def apply(self, a, b):
    return (bool(values[a]) or bool(values[b]))

class LogicalImplication(LogicalOperation):
  # Setup the symbol
  symbol = '->'
  evalop = any

class LogicalNot(LogicalOperation):
  # Setup the symbol
  symbol = '!'

  def __init__(self,t):
    self.var = t[0][1]

  def apply(self, a):
    v = bool(values[self.var])
    return not v

  def __bool__(self):
    v = bool(values[self.var])
    return not v

  def __str__(self):
    return "~" + str(self.var)

  __repr__ = __str__
  __nonzero__ = __bool__

# Setup variables containing only one character
_var = Word( alphas, max=1 )

# Allow values to be used as a binary representation
_val = Word( '01', max=1 )

# Operands
_operands = _var | _val
_operands.setParseAction(Operand)

# Precedence
booleanExpression = infixNotation( _operands, [
  ( LogicalNot.symbol,          1, opAssoc.RIGHT, LogicalNot ),
  ( LogicalAnd.symbol,          2, opAssoc.LEFT,  LogicalAnd ),
  ( LogicalOr.symbol,           3, opAssoc.LEFT,  LogicalOr  ),
  #( LogicalImplication.symbol,  4, opAssoc.LEFT,  LogicalImplication  ),
])

print( bool(booleanExpression.parseString("1 && 0")) )