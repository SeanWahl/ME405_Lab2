#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb  4 11:56:09 2023

@author: nathandodd
"""

# Define a generator function for producing numbers associated with the
# Collatz conjecture
def collatz(n):
    # Check for invalid seeds first
    if type(n) is not int:
        raise TypeError('Input must be an integer')
    if n < 1:
        raise ValueError('Input must be positive')
    
    # Start by yielding the initial seed value
    yield n
    
    # Apply the collatz "function" until hitting the stopping condition
    while n != 1:

        # Even values of n
        if n % 2 == 0:
            n //= 2
        # Odd Values of n
        else:
            n = 3*n + 1      
        
        # Yield the general case
        yield n

if __name__ == "__main__":
    # This first example shows how to convert the generator to a list
    # which will run the generator as many times as needed until the generator
    # function exists (the while loop ends)
    #print(list(collatz(11)))
    
    # This next example shows how to loop through the numbers in the generator
    # using a for loop similar to how we iterate through lists
    #for num in collatz(11):
    #    print("The num is", num)
    
    # You can also call next() manually, but the above methods are generally
    # more useful
    seq = collatz(8)
    print(next(seq))
    print(next(seq))
    print(next(seq))
    print(next(seq))
    print(next(seq))  #<---- notice that this line reaches the end of the
                      #      while loop causing a StopIteration exception
