"""This is a demo showcasing private variables in a python class. As you might know, python does not have
private variables in a class. The closest you can achieve is by using the __ operator before a variable like __foo.
In doing so, python automatically renames the variable as _<class-name>__foo. So, if __foo belongs to a class MyClass,
it becomes _MyClass__foo. This however isn't data encapsulation like what other higher level languages provide.

In the example below, a clever method is used to check if the __getattribute__() (and several other methods) is being
called from within the class or from outside of it. As python does not differentiate between method calls from within
the class or at runtime, implementing such a feature requires checking for some "identification factor" in the stack.
This is done by inspecting the stack and checking if it contains the word "self." in it. If it does, we can conclude
that the method was called from within the declaration. If not, then it was called from outside, or at run-time.



Issues:-

The error handling isn't perfect: I'm yet to discover a way to raise custom errors to fully mimick python's 'raise'
statement.
(Right now, errors are thrown by making use of the traceback module. Functions are terminated using a blank return 
statement. However, this does not return an exit code like how python's default raise statements does. In case one attempts to
use the sys.exit(1) option or any similar function, it works while in script mode, however upon usage in the interactive 
mode, the program exits out of the interactive mode on incurring sys.exit().

The reason behind using custom errors is because using the raise statement causes the traceback to point to the exact line 
throwing the error, aka, the raise statement itself. This is a problem to be found even in professional third-party modules.
However, python's built-in modules do not have this kind of a drawback. My intentions are to mimick that feature.)


Another big existing issue is that, in the way the concerned methods (__delattr__(), __getattribute__(), __setattr__())
are defined, it makes use of declaring the class as a sub-class of the builtin-in 'object' class. As I had said above,
since python does not natively differentiate method calls from within the class or outside of it, it is possible to bypass
the restrictions set up in this code to still access these "private" variables. For example, if one wishes to access the 
variable 'foo' of an object, say 'bar', of the class 'MyClass' (which is a sub-class of the built-in class 'object'), they 
can simply use object.__getattribute__(bar, 'foo') and access the value of the variable. This is a very simple workaround
which is yet to be fixed."""



import traceback
import sys
import inspect


class funny(object):
	"""A demo class created to showcase an implementation of private variables in a python class. Accepts one argument
	which can be numeric or alphanumeric. The class has two methods, judge() and decorate()."""

	__all__ = ['judge()', 'decorate()']

	vars = {}

	privates = ['privates', '__dict__']		# The list storing the names of all the variables that are supposed to be private
	
	def __init__(self, a):
		self.a = a
		self.privates.append('a')		# The variable name needs to be added to self.privates to make it private

	def __setattr__(self, *a):
		# Following if statement checks the stack to make sure it isn't empty
		if inspect.stack()[1][4]:
			# The following if statement checks the stack for the word 'self.'
			if 'self.' in inspect.stack()[1][4][0].strip():
				object.__setattr__(self, *a)		# The method is supposed to behave regularly in case it was called from within the class
				return

		# Checks if the variable is referenced in self.privates
		if a[0] in self.privates:
			self.vars[a[0]] = 'var_' + a[0]
			a = ('var_' + a[0],) + a[1::]
			self.privates.append(a[0])

		try:
			object.__setattr__(self, *a)
		except:
			print(traceback.format_exc().splitlines(keepends=True)[0] + ''.join(traceback.format_stack()[:-1]) + traceback.format_exc().splitlines()[-1], file=sys.stderr)
			return

	def __delattr__(self, a):
		# Following if statement checks the stack to make sure it isn't empty
		if inspect.stack()[1][4]:
			# The following if statement checks the stack for the word 'self.'
			if 'self.' in inspect.stack()[1][4][0].strip():
				object.__delattr__(self, a)		# The method is supposed to behave regularly in case it was called from within the class
				return
		
		# Checks if the variable is referenced in self.privates
		if a in self.vars.keys():
			b, a = a, self.vars[a]
			self.vars.pop(b)
		elif a in self.privates:
			try:
				raise AttributeError("'funny' object has no attribute '" + a + "'")
			except AttributeError:
				print(traceback.format_exc().splitlines(keepends=True)[0] + ''.join(traceback.format_stack()[:-1]) + traceback.format_exc().splitlines()[-1], file=sys.stderr)
				return

		try:
			object.__delattr__(self, a)
		except:
			print(traceback.format_exc().splitlines(keepends=True)[0] + ''.join(traceback.format_stack()[:-1]) + traceback.format_exc().splitlines()[-1], file=sys.stderr)
			return

	def __getattribute__(self, a):
		# Following if statement checks the stack to make sure it isn't empty
		if inspect.stack()[1][4]:
			# The following if statement checks the stack for the word 'self.'
			if 'self.' in inspect.stack()[1][4][0].strip():
				return object.__getattribute__(self, a)		# The method is supposed to behave regularly in case it was called from within the class
		
		# Checks if the variable is referenced in self.privates
		if a in self.vars.keys():
			a = self.vars[a]
		elif a in self.privates:
			try:
				raise AttributeError("'funny' object has no attribute '" + a + "'")
			except AttributeError:
				print(traceback.format_exc().splitlines(keepends=True)[0] + ''.join(traceback.format_stack()[:-1]) + traceback.format_exc().splitlines()[-1], file=sys.stderr)
				return

		try:
			return object.__getattribute__(self, a)
		except:
			print(traceback.format_exc().splitlines(keepends=True)[0] + ''.join(traceback.format_stack()[:-1]) + traceback.format_exc().splitlines()[-1], file=sys.stderr)
			return
	
	def judge(self):
		"""Returns 'nice' in case the entered argument was a number, 69; or None in case it wasn't"""

		print(('nice', '')[self.a != 69])

	def decorate(self):
		"""Prints the entered argument 69 times, back-to-back"""
	
		print(69 * str(self.a))

	# Redeclaring __dir__() to remove all references of the private variables (agreed, it can be done in a more 'python'way)
	def __dir__(self):
		return ['__module__', '__init__', '__weakref__', '__doc__', '__repr__', '__hash__', '__str__', '__getattribute__', '__setattr__', '__delattr__', '__lt__', '__le__', '__eq__', '__ne__', '__gt__', '__ge__', '__new__', '__reduce_ex__', '__reduce__', '__subclasshook__', '__init_subclass__', '__format__', '__sizeof__', '__dir__', '__class__']
