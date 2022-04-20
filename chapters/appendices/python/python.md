---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.10.3
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

# Python Primer

+++

:::{admonition} Work in progress!
:class: warning

This section isn't complete yet.
:::

+++

This section aims to provide *just enough* info to demystify the weird symbols and to get started with the Python [Python](https://www.python.org) programming language.

To make sense of the code throughout this handbook see, it helps to be familiar with four main things:

* **Comments** - which help explain what's happening
* **Variables** - which store values
* **Functions** - which do stuff with variables
* **Modules** - which need to be imported to use the useful stuff (like functions) they contain

This is far from everything you need to know to master programming, but it might just be enough to get started - and getting started if often the hardest part.

I think it's fair to say that experienced programmers pick up most of what they know as they go along: aided by a great deal of googling* along the way.

*-Or the use of some other preferred search engine.

+++

## Comments

Comments are explanations added to code that help explain what is going on.
They aren't essential for the code to *run*, but often are essential to make sense of it.
It's a very good idea to add comments to your own code - either for others to read, or for yourself in the future.

In Python, a typical comment starts with a `#`

```{code-cell} ipython3
# This is a comment.
# Each line needs a separate # to begin with.
# If I run this code, nothing much will happen - because it's all comment and no action.
```

## Variables

Variables provide a place to store stuff: numbers, text, images and so on.

You can think of it as a bit like algebra.
If you see

$$
x + 5
$$

then *x* is the variable.

When programming, you'll likely use variables all the time for different purposes and to represent different things.
The type of the variable will determine what you can do with it.
Some examples are given below.

+++

### Numbers

A variable might be used to represent a number.
You *assign* the number to the variable using `=`.

```{code-cell} ipython3
# Create a variable called 'x' and assign a value
x = 10

# Create a variable called 'y' and assign a value (by adding 5 to 'x')
y = x + 5

# Including a variable as the last line in a Jupter cell will mean it
# is displayed when the cell is run
y
```

It's important to note that `=` doesn't really mean 'is equal to' in this case.
Rather, when I see
```
x = 10
```
in my mind I read *'x becomes 10'* or alternatively *'set x to 10'*.

The order is important: the variable being set is on the left and the value it is being set to is on the right.
Switching the order can give an error - or a result you might not expect.

```{code-cell} ipython3
# Remove the # from the line below and try to run it (it will give an error)
# x + 5 = y
```

```{code-cell} ipython3
x = 10
y = 20

# Note that order maters - only x is being changed here!
# The value of x becomes 20, while y remains unchanged (i.e. still 20)
x = y

x
```

If you want to test if a variable is equal to something, you need to use `==` instead.
The output of that will be either `True` or `False`.

```{code-cell} ipython3
x = 10
x == 10
```

```{code-cell} ipython3
x = 20
x == 10
```

Note that, when using `==`, the order doesn't matter like it does with `=`.

```{code-cell} ipython3
x = 10
10 == x
```

You aren't restricted to testing whether a variable itself is equal to a specific value.
Rather, you can incorporate extra calculations and compare the results of these calculations to other values or variables.

```{code-cell} ipython3
x = 20
y = x - 10
x / 2 == y
```

### Strings

In computer parlance, a piece of text tends to be called a *string*.

You can create a string by enclosing the text in some quotation marks.

```{code-cell} ipython3
s = 'This is my string variable'
s
```

In Python, both single and double quotation marks can be used.

You can then do things like add strings together using the `+` symbol, which has the effect of concatenating them to create a new string.

```{code-cell} ipython3
s1 = 'First string'  # Define one string
s2 = "Second string" # Doesn't matter if we use single or double quotation marks
s3 = s1 + s2
s3
```

It doesn't *usually* matter whether you use single or double quotes, but it can matter if you want to include the other kind of quotation mark *within* the string.

```{code-cell} ipython3
# Remove the # from the line below and try to run it (it will give an error)
# s = 'I wouldn't like this string to end early'
```

In the example above, the `'` within 'wouldn't' was misinterpreted as the end of the string, and an error is the result.

There are two ways to get around that:
1. Use double-quotes
2. Use `\'` to 'escape' the first quotation mark

```{code-cell} ipython3
s = "I wouldn't like this string to end early"
s2 = 'I wouldn\'t like this string to end early'
```

Another way to generate an error is to try to create a string that spans multiple lines.

```{code-cell} ipython3
# Remove # from the following lines and try to run them
# s = "a string
# that tries to go across lines"
```

One way to get around that is to define the string using *3* double quotation marks `"""`.

You can use multiline strings like this as an alternative to comments, to avoid needing to add `#` at the beginning.

```{code-cell} ipython3
"""
This is a string that isn't assigned to any variable.
It can span multiple lines.
I can use it like a comment.
"""
```

### Lists

+++

### Tuples

+++

### Numpy arrays

+++

### Dictionaries

+++

## Functions

+++

### Defining functions

+++

## Modules

```{code-cell} ipython3

```
