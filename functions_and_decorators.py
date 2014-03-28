## Function Definition

# The most basic function definition:

def function_name(arg_one):
    print arg_one

# by convention function names are lower case underscore separated
# so are their arguments

# Functions that should not be used outside the module or class 
# are marked with a leading underscore, this is just convention
# it's not enforced by the language

def _dont_use_me():
    print "Please don't use this function again"

# Don't start function or argument names with a number

def 1_this_will_fail(): pass
def this_will_fail(1arg): pass

# Arguments with default values

def print_stuff(message, prefix="Here goes:", suffix="... and that's it"):
    print prefix, message, suffix

# Now we have lots and lots of different ways to call this function

# leave the optional arguments out
print_stuff("this is my message")
# >>> Here goes: this is my message ... and that's it

# fill one of the optional arguments using a keyword
print_stuff("this is my message", suffix="END")
# >>> Here goes: this is my message END

# fill all the arguments using keywords, in the wrong order
print_stuff(suffix="END", prefix="START", message="this is my message")
# >>> START this is my message END

# fill one of the optional arguments positionally
print_stuff("this is my message", "START")
# >>> START this is my message ... and that's it

# fill the optional arguments positionally
print_stuff("this is my message", "START", "END")
# >>> START this is my message END

# mix and match
print_stuff("this is my message", "START", suffix="END")
# >>> START this is my message END

# mix and match with an easy to make mistake
print_stuff("this is my message", "START", prefix="END")
# >>> TypeError: print_stuff() got multiple values for keyword argument 'prefix'

# positional arguments must come first when you mix and match
print_stuff("this is my message", prefix="START", "END")
# >>> SyntaxError: non-keyword arg after keyword arg

## Unnamed, unspecified and multiple arguments

# You can use *arg to get an arbitrary list of non-keyword arguments
def print_args(*words):
        print ", ".join(words)

print_args("one", "two", "three")
# >>> one, two, three

# but remember that normal arguments have to come before keyword arguments
def print_args(prefix="START", suffix="END", *middle):
    print prefix, " ".join(middle), suffix

print_args(prefix="GO", suffix="STOP", "low", "med", "high")
# >>> SyntaxError: non-keyword arg after keyword arg

# You can still use the optional args positionally
print_args("one", "two", "three", "four", "five")
# >>> one three four five two

# So there's limited utility for mixing and matching here and quite
# a bit of opportunity for mistakes.

# You can do a similar thing with unspecified keyword arguments
# which packs the given arguments into a dictionary
def print_pairs(**kwargs):
    for k,v in kwargs.iteritems():
        print "%s : %s"%(k,v)

print_pairs(one=1, two=2, three=3) 
# >>> 
# three : 3
# one : 1
# two : 2

# Don't forget dictionaries are not ordered

# The same things apply here that applied to the non-keyword arguments.
# It's easy to make mistakes both in implementation and use of these functions.
# However if you have some crazy function that might actually need to take 40
# arguments then this idiom is an option.

# Unpacking Arguments

# Sometimes you want to do the opposite and pass a list as a set of normal
# arguments
# Prefixing the argument with a * will automatically unpack the list or tuple
# into a normal argument list
lst = ["one", "two", "three", "four", "five"]
print_args(*lst)
# >>> one three four five two

# Which is exactly the same as this previous example
print_args("one", "two", "three", "four", "five")
# >>> one three four five two

# Notice how we're filling the arguments positionally in this example

# The same trick works with dictionaries and **
dct = {"one":1, "two":2, "three":3}
print_pairs(**dct)
# >>> 
# three : 3
# one : 1
# two : 2

# Which again is equivalent to
print_pairs(one=1, two=2, three=3) 
# >>> 
# three : 3
# one : 1
# two : 2

# A better example of that would be
def numbers(one=1, two=2, three=3):
    print one, two, three
dct["three"] = 5
numbers(**dct)
# >>> 1 2 5

# Again not super useful and pretty error prone. Use with care iff you really
# have to.

## Nesting Functions and Scope

# Functions can be nested in python
def func1():
    def internal_abstraction(message):
        print "Internal", message
    internal_abstraction("print this")

func1()
# >>> Internal print this
internal_abstraction("break")
# >>> NameError: name 'internal_abstraction' is not defined

# You can even return functions that can be used later
def make_adder(x):
    def adder(n):
        return n + x
    return adder

plus2 = make_adder(2)
plus2(2)
# >>> 4

# what you can't do is change the value of a variable in an outer scope
def make_accumulator():
    val = 0
    def accum(n):
        val += n
        return val
    return accum

acc = make_accumulator()
acc(2)
# >>> UnboundLocalError: local variable 'val' referenced before assignment

# This is a bit subtle. 
# When the python evaluator sees that you're assigning to val it creates val as
# an lvalue i.e. a variable that can be changed. It then detects that you're
# using that variable before you're initializing it and that's not allowed.
# ("val += n" expands to "val = val + n" the val in "val + n" is not
# initialized)
# What you're doing is masking the outer val with the inner version then
# breaking the rules with the inner version.

# The same thing happens with arguments except that they're never uninitialized
def plus1(val):
    val += 1
    return val

one = 1
plus1(one)
# >>> 2
one
# >>> 1

# And globals (you're not using globals are you?!)
# The global scope is just the outermost scope.
# The rules are exactly the same.
accum = 1
def accumulate(n):
    accum += 1
    return accum

accumulate(2)
# >>> UnboundLocalError: local variable 'accum' referenced before assignment

# Now we really put the b in subtle. 

# All the preceeding stuff is not really about values it's all about bindings.
# Python creates a new binding when you indicate that you want to do
# assignment. Then when you reference that variable python looks in the inner
# scope and finds the binding you just created.

# If you never try to assign to the variable, a new binding won't be
# created and when you reference the variable the first instance python finds
# will be the version in the outer scope.

# The fact that you can't change the outer value is a side effect of the
# binding rules in the evaluator.  

# So how can we create a variable who's binding isn't changed in the inner
# scope when it's assigned to? The answer is that we can't but I said above
# that all this isn't about values. Python doesn't care if you change the value
# of something you just have to do it without creating a new binding.
def make_accumulator():
    val = [0]
    def accum(n):
        val[0] += n
        return val[0]
    return accum

acc = make_accumulator()
acc(2)
# >>> 2
acc(3)
# >>> 5

# Here we never change the binding of val. In C terms val is a pointer and all
# we're doing in the inner function is de-referencing it and incedentally
# changing the value stored in the memory it points to. 
# I don't necessarily recommend you do this. Creating an accumulator class is
# by faaaar a better solution to this problem but I include it because it shows
# how you have to reason about binding and how python operates your code.

## Function Objects and Anonymous Functions

# You've seen how in python functions are first class objects.  You can assign
# them to variables and call those variables as if you'd created them with def.

# def doesn't really do anything special, it just creates a binding between the
# name you give it and the function object it creates from the rest of your
# code. 
# When python calls a function nothing special happens. It looks for the
# function name in its inner scope dictionary and then the outer scope
# dictionary and so on up to the uppermost global scope dictionary.

# When it finds a matching name it will look at the object it finds and see if
# it is a callable object.
# A callable object is simply an object that implements the __call__ member.
class Accumulator:
    def __init__(self):
        print "creating accumulator"
        self.val = 0
    def __call__(self, acc):
        self.val += acc
        return self.val

f = Accumulator()
# >>> creating accumulator
f(2)
# >>> 2
f.__call__(2)
# >>> 4

# Again, not really useful knowledge but interesting, I think.

# Sometimes you don't want to go through the hassle of creating a function with
# def. For example if you just want to wrap an expression that you can then
# pass to another function.
# The sorted and list.sort functions both take a keyword parameter called key
# that expects a function that yields a result that can be compared with >, <
# or ==.
# You can use this keyword to do all sorts of interesting things:
lst = [-1, -2, -3, 0, 3, 2, 1]
sorted(lst, key=abs)
# >>> [0, -1, 1, -2, 2, -3, 3]
from random import random
sorted(lst, key=random)
# >>> TypeError: random() takes no arguments (1 given)

# Oops, well since I've apparently forgotten about random.shuffle lets try to
# make this work.
def random_no_args(_): return random()

sorted(lst, key=random_no_args)
# >>> [1, -3, -2, 0, -1, 3, 2]

# That's sort of a rubbish solution, it's just an expression. Why pollute our
# global scope with that?
# What we need is a way to create an function that is unbound, an anonymous
# function i.e. not using def.
sorted(lst, key=lambda _: random())
# >>> [1, 3, -2, -3, 0, 2, -1]

# A less contrived example:
python_group = [
        { "fname" : "John", "lname" : "Clease" },
        { "fname" : "Micheal", "lname" : "Palin" },
        { "fname" : "Eric", "lname" : "Idle" },
        { "fname" : "Graham", "lname" : "Chapman", "status" : "deceased" },
        { "fname" : "Terry", "lname" : "Jones" },
        { "fname" : "Terry", "lname" : "Gilliam" } ]
python_group.sort(key=lambda python: python["lname"])
python_group # list.sort is in-place and doesn't return anything
# >>> [{'lname': 'Chapman', 'status': 'deceased', 'fname': 'Graham'}, {'lname': 'Clease', 'fname': 'John'}, {'lname': 'Gilliam', 'fname': 'Terry '}, {'lname': 'Idle', 'fname': 'Eric'}, {'lname': 'Jones', 'fname': 'Terry'}, {'lname': 'Palin', 'fname': 'Micheal'}]
python_group.sort(key=lambda python: python["fname"])
python_group 
# >>> [{'lname': 'Idle', 'fname': 'Eric'}, {'lname': 'Chapman', 'status': 'deceased', 'fname': 'Graham'}, {'lname': 'Clease', 'fname': 'John'}, {'lname': 'Palin', 'fname': 'Micheal'}, {'lname': 'Gilliam', 'fname': 'Terry'}, {'lname': 'Jones', 'fname': 'Terry'}]


# In some other langauges lambda expressions are really powerful and function
# definition is just a wrapper that binds a lambda expression to a name in the
# scope.
# (defun fn (arg1 (line1 arg) (line2 arg)) ==>
# (setq 'fn (lambda (arg) (line1 arg) (line2 arg)))
#
# In python they can only be used to turn an expression into a function.
# There's no such thing as a multi-line lambda. For that you have to use a
# function just as in the random_no_args example.
# Even limited as they are lambdas are really useful and generally the ability
# to pass functions as arguments enables whole classes of programs that a
# impossible express eleganly in languages that lack first class functions.

## Decorators (finally!)

# Decorators are just functions that take other functions are arguments and
# return a replacement function. If python were a functional language this
# wouldn't even have a name let alone a special syntax.
# When a decorator is invoked the function being decorated is created but not
# bound to a name. It is then passed to the decorating function and the result
# of that function is bound to the original function's name.

def fn_plus_one(fn):
    return lambda: fn() + 1

def one(): return 1
one = fn_plus_one(one)

one()
# >>> 2

# Which is perfectly equivalent to the python decorator syntactic sugar:

@fn_plus_one
def one(): return 1

one()
# >>> 2

# The function returned by the decorator *must* be a drop in replacement for
# the original function. That means it must have the same arguments and even
# argument names.

def pair_abs(fn):
    def inner_pair_abs(a,b):
        return (abs(a), abs(b))
    return inner_pair_abs

@pair_abs
def double_pair(pair):
    return (pair[0] * 2, pair[1] * 2)

# This can result in some particularly difficult to debug error messages.

double_pair((-1, -2))
# >>> TypeError: inner_pair_abs() takes exactly 2 arguments (1 given)

# What the hell in inner_pair_abs?! If you're just using a decorator from a
# library and aren't familiar with the source code then this error will not
# help you.
# It makes perfect sense to python though because the name double_pair
# was bound to the result of the decorator function which python correctly
# names as inner_pair_abs

# For specific uses decorators of this type can be a useful abstraction.
# However where they actually shine is in comination with the *args and
# **kwargs syntax.
# The following is a classic example of a decorator:

def logger(fn):
    def inner_logger(*args, **kwargs):
        print "%s(%s : %s)"%(fn.__name__, args, kwargs)
        return fn(*args, **kwargs)
    return inner_logger

@logger
def string_stuff(message, prefix="Here goes:", suffix="... and that's it"):
    return prefix +  message + suffix

string_stuff("my message", prefix="START", suffix="END")
# >>>
# string_stuff(('my message',) : {'prefix': 'START', 'suffix': 'END'})
# 'STARTmy messageEND'

# Note that now the way the function is called now has an impact on the
# contents of the each argument.

string_stuff("my_message", "S ", " E")
# >>>
# string_stuff(('my_message', 'S ', ' E') : {})
# 'S my_message E'

## Decorator Classes

# When more complicated decoration is needed it is good to start to use
# decorator classes instead of simple decorator functions.
# Recall that a normal function is already a class with a __call__ method so
# really you're already using decorator classes. Now we're just making it
# explicit.

class Logger:
    def __init__(self, fn):
        self.func = fn
    def __call__(self, *args, **kwargs):
        print "%s(%s : %s)"%(self.func.__name__, args, kwargs)
        return self.func(*args, **kwargs)

@Logger
def string_stuff(message, prefix="Here goes:", suffix="... and that's it"):
    return prefix +  message + suffix

string_stuff("my message", prefix="START", suffix="END")
# >>>
# string_stuff(('my message',) : {'prefix': 'START', 'suffix': 'END'})
# 'STARTmy messageEND'

# Here we've replicated logger example above using a class.

# This is interesting because it seperates the notion of decoration time and
# runtime. The constructor is run at decoration time and __call__ is run at
# runtime.
# Decoration time happens when the code or bytecode is being read by python.
# First the function is created, then it is passed to decorator object
# constructor and that object is bound to the name of the original function.
# At runtime the object's __call__ method is executed just like any other
# function object's would be.

## Decorators with Arguments

# Sometimes it is useful to pass data into the decorator at decoration time.
# This is the only way to change the internal state of the decorating object
# before the decorated function is executed.
# The confusing part of this is that passing arguments to the decorator changes
# the semantics of what you're doing and different parts of the decorator get
# executed at different times than they would be without arguments.

from sys import stdout

class Logger:
    def __init__(self, file_handle):
        self.file_handle = file_handle
    def __call__(self, fn):
        def inner_logger(*args, **kwargs):
            self.file_handle.write("%s(%s : %s)\n"%(fn.__name__, args, kwargs))
            return fn(*args, **kwargs)
        return inner_logger

@Logger(stdout)
def string_stuff(message, prefix="Here goes:", suffix="... and that's it"):
    return prefix +  message + suffix

string_stuff("my message", prefix="START", suffix="END")
# >>>
# string_stuff(('my message',) : {'prefix': 'START', 'suffix': 'END'})
# 'STARTmy messageEND'

# What's happening is that the Logger instance is created using it's arguments.
# Then that instance is __call__ed with the function as the argument and that
# __call__ has to return the replacement function.

# If you look at the syntax and think about what each part means I think you'll
# see that it is remarkably consistent.

# Considering that @ is just syntactic sugar:
@Logger 
def func(): pass
# expands to:
def func(): pass
func = Logger(func)
# so func is now bound to an instance that's created at decoration time.

# As opposed to
@Logger(stdout)
def func(): pass
# Which would expand to:
def func(): pass
func = Logger(stdout)(func)
# Which we know is eqivalent to:
func = Logger(stdout).__call__(func)
# so func is bound to the result of __call__ from the instance that is created
# with the argument

## Summary

# There are lots of different ways to pass arguments to functions. 
# - Positional
# - Keyword
# - Default
# - All of the above
# The different ways you pass arguments result in different argument handling
# - *args va **kwargs
# - Hopefully you never have to notice this
# Some ordering of different types of arguments are valid and others are not
# - Invalid orderings are usually invalid because they are ambiguous
# Python can destructure positional and keyword arguments for you
# - using * before the argument iterator for positional
# - and ** before the argument dictionary for keyword
# - You can mix and match this destructuring but be careful
# Functions are first class in python
# - You can pass them like variables
# - You can create them from an expression using lambda
# Assigning to a variable in an outer scope creates a new binding
# - You cannot alter the binding in the outer scope
# - You can fake it if you have to using a data structure but don't
# - Use a class instead if you have trouble like this

# Decorators are just functions that take other functions as arguments
# - They're really nothing special in a language with first class functions
# - It does expose some functional programming goodies we can exploit
# - @ is just syntactic sugar for a function application and a rebinding
# - Keep that in mind and you should be able to reason effectively about how
# decorators will execute.
