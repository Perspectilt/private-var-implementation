# private-var-implementation
An implementation of private variables in python

This is a demo showcasing private variables in a python class. As you might know, python absolutely does not have
private variables in a class. The closest you can achieve is by using the `__` operator before a variable like `__foo`.
In doing so, python automatically renames the variable as `_<class-name>__foo`. So, if `__foo` belongs to a class MyClass,
the nomenclature becomes `_MyClass__foo`. This however isn't data abstraction like what other higher level languages provide.

In the example below, a clever method is used to check if the `__getattribute__()` (and several other methods) is being
called from within the class or from outside of it. As python does not differentiate between method calls from within
the class or at runtime, implementing such a feature requires checking for some "identification factor" in the stack.
This is done by inspecting the stack and checking if it contains the word "self." in it. If it does, we can conclude
that the method was called from within the declaration. If not, then it was called from outside, or at run-time.
