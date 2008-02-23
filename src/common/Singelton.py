# Copyright (C) 2007-2008 Sebastian Ruml <sebastian.ruml@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 1, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.

#
# Singleton implements
#
class Singleton(object):
	#
	# Manage instance
	#
	# @var object
	__Instance = None
	
	#
	# Name of the child
	#
	# @var string
	__Name = 'Singleton'
	
	#
	# callback
	#
	def __new__(child,*args):
		if (not child.__Instance):
			child.__Instance = super(Singleton, child).__new__(child,*args)
		else:
			child.__init__ = child.__doNothing
		
		return child.__Instance


	def __doNothing(child,*args):
		'''
		This method do nothing. is used to override the __init__ method
		and then, do not re-declare values that may be declared at first
		use of __init__ (When no instance was made).
		'''
		pass

	#
	# Sets name of the child
	#
	def setName(child, value = 'Singleton'):
		child.__Name = value

	#
	# Returns name of the class
	#
	# @return string
	def getName(child):
		return child.__Name

	#
	# Returns Id of the object
	#
	# @return integer
	def getId(child):
		"""
		Returns singleton Id
		"""
		return id(child)

