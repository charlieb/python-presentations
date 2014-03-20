## C-like Looping

list1 = [1,2,3,4,5,6]

# Bad:
result = False
for i in range(len(list1)):
    if list1[i] == 1:
        result = True
        break

# Better:
result = False
for val in list1:
    if val == 1:
        result = True
        break

# Best:
result = 1 in list1

# "in" checks for membership in a list
# it can also be used for other iterables

# Dict:
dict1 = {"a":1, "b":2, "c":3}
"a" in dict1
# >>> True

# Tuple:
tpl = (1,2,3,4,5)
3 in tpl
# >>> True

# What if you need the index?
list1 = ['a', 'b', 'c']
for i, val in enumerate(list1):
    print i, val

# >>> 
# 0 a
# 1 b
# 2 c

## Truth , Falsity and None
# in C FALSE == 0 == NULL and everything else is TRUE
#
# In python False <> None <> True
False == None
# >>> False
 
True == None
# >>> False

# The rules are the same as C but the values are different
if False:
    print False
# >>>  (prints nothing)

if None:
    print None
# >>>  (prints nothing)

if True:    
    print True
# >>> True (duh)

# good practices
# Just as in C avoid comparison to True:
val = True
if val == True:
    print "naughty"

if val: 
    print "nice"

# In python also avoid comparison to None:
val = None
if val == None:
    print "naughty"

if val is None:
    print "nice"

# Why "is"?
# None is a singletyon and there is only ever one value for None
# "==" tests for equality
# "is" tests for identity (a pointer comparison if you like)
[1] == [1]
# >>> True
[1] is [1]
# >>> False

# Practically there's not that much difference but 
# the key difference is that classes can redefine "=="
# but they cannot redefine "is"

# Advanced Example:
class A:
    def __eq__(self, other):
        return True

foo = A()
foo == None
# >>> True


## Strings and Concatenation
# In python strings are concatenated with +
"one " + "two"
# >>> "one two"

# Repeated Concatenatuion

# Bad:
cpd_lst = ["one", "two", "three", "four"]
cpds = ""
for cpd in cpd_lst:
    cpds += ", " + cpd

# Better:
", ".join(cpd_lst) 
# >>> "one, two, three, four"

" and ".join(cpd_lst)
# >>> "one and two and three and four"

## Docstrings
# docstrings are just a special comment that the user of the 
# function, class , module etc. can access at runtime
# They're very useful for exploration of unfamiliar modules
# Start a docstring wuth 3 quotes
def docstring_test():
    """Docstring testing function. """
    return None

print docstring_test.__doc__

# >>>
#    Docstring testing function.

# the docstring for a class is the docstring for the __init__ method
class DString:
    """DString class.  Very useful"""

print DString.__doc__

# >>>
#     DString class.
#     Very useful


## Assignment
# multiple assignment is awesome
a,b = 1,2
# example: swap two variables
# Bad:
tmp = a
a = b
b = tmp

# Better
a,b = b,a

# Unpacking multiple assignment
lst = [1,2,3]
# Bad: 
a, b, c = lst[0], lst[1], lst[2]
# Better:
a,b,c = lst

# (I told you it was awesome)

# Destructuring multiple assignment:
lst = [1,2,[3,4], 5]
a,b,c,d = lst
print "%s,%s,%s,%s"%(a,b,c,d)
# >>> 1,2,[3,4],5

a,b,(c,d),e = lst
print "%s,%s,%s,%s,%s"%(a,b,c,d,e)
# >>> 1,2,3,4,5

# (Pretty cool eh?)

# Destructuring multiple assignment from an iterator:
a,b,c,d = range(4)
print "%s,%s,%s,%s"%(a,b,c,d)
# >>> 1,2,4,5

d,e,f = {"a":1, "b":2, "c":3}
print "%s,%s,%s"%(d,e,f)
# >>> a,b,c

# (what is this sorcery?!)

## Filtering and Mapping Iterables (lists)

# Bad:
lst = [1,2,3,4]
lst2 = []
for a in lst:
    lst2.append(a*2)

print lst2
# >>> [2,4,6,8]

# Also bad:
lst2 = []
for a in lst:
    if a%2 == 0:
        lst2.append(a*2)

print lst2
# >>> [4,8]


# Better:
# The syntax for this looks weird but it's quite nice once you get used to it
lst = [1,2,3,4]
[a*2 for a in lst]
# >>> [2,4,6,8]
#a*2 <-- mapping part, can use any python expression
#    for a in lst <-- iteration part, defines a for use in expression

[a*2 for a in lst if a%2 == 0]
# >>> [4,8]
#                 if a%2 == 0 <-- filter part, a's that evaluate to True are kept

# Just like "in" you can also use this syntax for other iterables
 
# Dict:
dict1 = {"a":1, "b":2, "c":3}
{k+'z': v+1 for k,v in dict1.iteritems()}

# >>> {'az': 2, 'cz': 4, 'bz': 3} 

# Tuple: tuple syntax is a little different and the tuple is
# converted to a list by the comprehension and then back again by us
tpl = (1,2,3,4,5)
tuple([t + 1 for t in tpl])

# >>> (2,3,4,5,6)

