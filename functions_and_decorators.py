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

# fill both of the optional arguments using keywords, in the wrong order
print_stuff("this is my message", suffix="END", prefix="START")
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
class fun:
    def __init__(self): print "creating fun"
    def __call__(self): print "Fun!"

f = fun()
# >>> creating fun
f()
# >>> Fun!
f.__call__()
# >>> Fun!

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

# Oops, well since I've forgotten about random.shuffle lets try to make this
# work.
def random_no_args(_): return random()

sorted(lst, key=random_no_args)
# >>> [1, -3, -2, 0, -1, 3, 2]

# That's sort of a rubbish solution, it's just an expression. Why pollute the
# scope with that?
# What we need is a way to create an function that is unbound i.e. not using
# def.
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
