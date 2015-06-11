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
from pyparsing import Word, alphas, Literal, oneOf, opAssoc, infixNotation, Group, Forward, Or, Keyword, ZeroOrMore
import collections

# Store the variables values
values = collections.defaultdict(lambda: 0)

# Fetch the variable value
def parseVariable(tokens):
  return bool(values[tokens[0]])

# Parse a binary value (1 or 0)
def parseBinary(tokens):
  return bool(int(tokens[0]))

def parseNot(tokens):
  return not tokens[0]

# Parse an expression
def parseAnd(tokens):
  tokens = tokens[0]
  return tokens[0] and tokens[2]

def parseOr(tokens):
  tokens = tokens[0]
  return tokens[0] or tokens[2]

# Setup variables containing only one character
_var = Word( alphas, max=1 )
_var.setParseAction( parseVariable )

# Allow values to be used as a binary representation
_val = Word( '01', max=1 )
_val.setParseAction( parseBinary )

# Atom
_atom = ZeroOrMore( _var | _val )

# Operands
_and = Literal('&&')
_or = Literal('||')
_not = Literal('!')
_binary_operands = _and | _or

# Expression
_expression = infixNotation( _atom,
[
  ( _not, 1, opAssoc.RIGHT, parseNot),
  ( _and, 2, opAssoc.LEFT,  parseAnd),
  ( _or,  2, opAssoc.LEFT,  parseOr),
])


print( _expression.parseString("1 && 1 || 0 && 0") )