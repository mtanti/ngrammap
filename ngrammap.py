#!/usr/bin/env python

#The MIT License (MIT)
#
#Copyright (c) 2013 Marc Tanti http://www.marctanti.com
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in
#all copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#THE SOFTWARE.

"""
This is a data structure for storing and querying n-grams.

N-grams are ordered collections (with a defined length) of elements which must be hashable, although the collection used is irrelevant as it is not used internally.
NGramMap works by keeping a prefix tree of all elements in the provided n-grams where each path in the tree leads to a complete n-gram.
The last node in the path of an n-gram is called a terminating node, otherwise it is a non-terminating node.
Since n-grams can be of varying lengths, in order to distinguish n-grams which are a prefix of other n-grams, each node is given a boolean flag marking it a terminating node.

Here is a diagram illustrating how this data structure is stored, where "O" is a node in the prefix tree. It stores the n-grams (a,a,a), (a,a,b), (a,b,a), (b,a,a)

                     O
                    / \
                   a   b
                  /     \
                 O       O
                / \      |
               a   b     a
               |   |     |
               O   O     O
               |   |     |
               a   a     a
"""

__author__ = "Marc Tanti"
__copyright__ = "Copyright 2013, http://www.marctanti.com"
__credits__ = ["Marc Tanti"]
__license__ = "MIT"
__version__ = "0.2.0"
__maintainer__ = "Marc Tanti"
__status__ = "Prototype"

class NGramMap():
    """ Map n-grams to values. N-grams must consist of hashable elements and the container must be ordered and its length defined. The container used is irrelevant as it is not used internally. """
    
    def __init__(self):
        """ Create a new n-gram map. """
        self.root = _NGramMapNode()
        self.size_freqs = dict() #A dictionary recording the frequencies of each n-gram size.
        self.element_freqs = dict() #A dictionary recording the frequencies of all elements in all n-grams.

    def __setitem__(self, ngram, value):
        """ Assign a value to an n-gram, overwriting the existing value if the n-gram exists. 'ngram' must be hashable and in an ordered container whose length is defined. """
        ngram_size = len(ngram)
        if ngram not in self:
            #Record size of n-gram.
            if ngram_size not in self.size_freqs:
                self.size_freqs[ngram_size] = 0
            self.size_freqs[ngram_size] += 1

            #Record elements of n-gram.
            for element in ngram:
                if element not in self.element_freqs:
                    self.element_freqs[element] = 0
                self.element_freqs[element] += 1

        self.root.__setitem__(ngram, value)

    def pop(self, ngram):
        """ Remove an n-gram and associated value, returning the value. 'ngram' must be hashable and in an ordered container whose length is defined. """
        value = self.root.pop(ngram)

        #Dismiss size of n-gram.
        ngram_size = len(ngram)
        self.size_freqs[ngram_size] -= 1
        if self.size_freqs[ngram_size] == 0:
            self.size_freqs.pop(ngram_size)

        #Dismiss elements of n-gram.    
        for element in ngram:
            self.element_freqs[element] -= 1
            if self.element_freqs[element] == 0:
                self.element_freqs.pop(element)
        
        return value

    def __getitem__(self, ngram):
        """ Get the value associated with an n-gram. 'ngram' must be an ordered container whose length is defined and whose elements are hashable. """
        return self.root.__getitem__(ngram)

    def __contains__(self, ngram):
        """ Check if an n-ngram exists in the mapping. 'ngram' must be an ordered container whose length is defined and whose elements are hashable. """
        return ngram in self.root

    def ngrams(self):
        """ Get an iterator over all the n-grams in the mapping. Returned n-grams are tuples. """
        return self.root.ngrams()

    def sized_ngrams(self, size):
        """ Get an iterator over all the n-grams of a particular size in the mapping. Returned n-grams are tuples. """
        return self.root.sized_ngrams(size)

    def ngrams_with_eles(self, targets):
        """ Get an iterator over all the n-grams which contain all the given target elements in any order. 'targets' must be a set of elements. Returned n-grams are tuples. """
        return self.root.ngrams_with_eles(targets)

    def sized_ngrams_with_eles(self, targets, size):
        """ Get an iterator over all the n-grams of a particular size which contain all the given target elements in any order. 'targets' must be a set of elements. Returned n-grams are tuples. """
        return self.root.sized_ngrams_with_eles(targets, size)

    def ngrams_by_pattern(self, ngram_pattern, placeholder_indices):
        """ Get an iterator over all the n-grams which match an n-gram pattern consisting of elements, some of which will be ignored as placeholders. Placeholders are used to signify that any element can take their place. The indices of the placeholders must be specified. Returned n-grams are tuples. """
        return self.root.ngrams_by_pattern(ngram_pattern, placeholder_indices)

    def values(self):
        """ Get an iterator over all the values in the mapping. """
        return self.root.values()

    def items(self):
        """ Get an iterator over all (n-gram, value) pairs in the mapping. """
        return self.root.items()

    def elements(self):
        """ Get an iterator over all elements in all n-grams in the mapping. """
        return self.element_freqs.keys()

    def __iter__(self):
        """ Iterate over all the n-grams in the mapping. Returned n-grams are tuples. """
        return self.root.ngrams()

    def update(self, other):
        """ Add all n-grams from an n-gram map into this n-gram map. """
        for (ngram, value) in other.items():
            self[ngram] = value

    def clear(self):
        """ Clear n-gram map of all n-grams. """
        self.root = _NGramMapNode()
        self.size_freqs = dict()

    def __delitem__(self, ngram):
        """ Remove an n-gram and associated value. 'ngram' must be an ordered container whose length is defined and whose elements are hashable. """
        self.root.pop(ngram)

    def __len__(self):
        """ Get the number of ngrams in the mapping. """
        return sum(self.size_freqs.values())

    def len_of_size(self, size):
        """ Get the number of ngrams of a given size in the mapping. """
        return self.size_freqs[size]

    def ngram_sizes(self):
        """ Get the different sizes of n-grams contained in the mapping. """
        return self.size_freqs.keys()

    def __repr__(self):
        """ Return a string representation of this n-gram map. """
        return "{" + (", ".join(str(ngram)+": "+str(value) for (ngram, value) in self.items())) + "}"

    def __str__(self):
        """ Return a string representation of this n-gram map. """
        return repr(self)


#############################################################################


class _NGramMapNode():
    """ A node in an n-gram prefix tree. For internal use only. """
    
    def __init__(self):
        """ Create a new n-gram map node. """
        self.end_of_ngram = False #Flag marking whether this node is the end of an n-gram.
        self.value = None #Provided that the node marks the end of an n-gram, this refers to the value mapped by this n-gram.
        self.children = dict() #A dictionary which maps the next elements in the current path of the prefix tree to the respective node of the tree.
        
    def __setitem__(self, ngram, value):
        """ Assign a value to an n-gram, overwriting the existing value if the n-gram exists. """
        #N-gram is consumed element by element from first to last and each time this function will pass the rest of the n-gram to the next node.
        #When the n-gram is completely consumed, the current node will be marked a terminating node.
        
        #Base case: N-gram fully consumed and this node is at the end of the n-gram. Mark it as a terminating node.
        if len(ngram) == 0:
            self.end_of_ngram = True
            self.value = value
        #Recursive case: N-gram is still being consumed. Move on to next node.
        else:
            next_ele = ngram[0]
            rest_ngram = ngram[1:]

            #Create a new child node if the next element does not lead to anywhere and recurse on it.
            if next_ele not in self.children:
                self.children[next_ele] = _NGramMapNode()
            self.children[next_ele].__setitem__(rest_ngram, value)

    def pop(self, ngram):
        """ Remove an n-gram and associated value, returning the value. """
        #N-gram is consumed element by element from first to last and each time this function will pass the rest of the n-gram to the next node.
        #When the n-gram is completely consumed, the current node is marked a non-terminating node and the ansestors of the node are notified of the removal of elements from their descendents.

        #Base case: N-gram fully consumed and this node is at the end of the n-gram. Mark it as a non-terminating node.
        if len(ngram) == 0:
            #If n-gram does not exist then raise an error.
            if self.end_of_ngram:
                value = self.value
                
                self.end_of_ngram = False
                self.value = None
                
                return value
            else:
                raise KeyError(ngram)
        #Recursive case: N-gram is still being consumed. Move on to next node.
        else:
            next_ele = ngram[0]
            rest_ngram = ngram[1:]

            #If n-gram does not exist then raise an error.
            if next_ele in self.children:
                value = None
                try:
                    #Recursive line
                    value = self.children[next_ele].pop(rest_ngram)
                except KeyError:
                    raise KeyError(ngram)

                #The following code is for clean up after the terminating node of the n-gram in the descendents of this node was dealt with.

                #Remove the child node leading to the terminating node if it has no children of its own.
                if len(self.children[next_ele].children) == 0:
                    self.children.pop(next_ele)

                return value
            else:
                raise KeyError(ngram)

    def __getitem__(self, ngram):
        """ Get the value associated with an n-gram. """
        #N-gram is consumed element by element from first to last and each time this function will pass the rest of the n-gram to the next node.
        #When the n-gram is completely consumed, the value of the current node is returned.

        #Base case: N-gram fully consumed and this node is at the end of the n-gram. Return its value.
        if len(ngram) == 0:
            #If n-gram does not exist then raise an error.
            if self.end_of_ngram:
                return self.value
            else:
                raise KeyError(ngram)
        #Recursive case: N-gram is still being consumed. Move on to next node.
        else:
            next_ele = ngram[0]
            rest_ngram = ngram[1:]

            #If n-gram does not exist then raise an error.
            if next_ele in self.children:
                try:
                    return self.children[next_ele].__getitem__(rest_ngram)
                except KeyError:
                    raise KeyError(ngram)
            else:
                raise KeyError(ngram)

    def __contains__(self, ngram):
        """ Check if an n-ngram exists in the mapping. """
        #N-gram is consumed element by element from first to last and each time this function will pass the rest of the n-gram to the next node.
        #When the n-gram is completely consumed, whether or not the current node is a terminating node is returned.
        
        #Base case: N-gram fully consumed and this node is at the end of the n-gram. Return if its a terminating node.
        if len(ngram) == 0:
            if self.end_of_ngram:
                return True
            else:
                return False
        #Recursive case: N-gram is still being consumed. Move on to next node.
        else:
            next_ele = ngram[0]
            rest_ngram = ngram[1:]

            #If n-gram does not exist then return false.
            if next_ele in self.children:
                return self.children[next_ele].__contains__(rest_ngram)
            else:
                return False

    def ngrams(self):
        """ Get an iterator over all the n-grams in the mapping. Returned n-grams are tuples. """
        return self.__ngrams(())
    def __ngrams(self, partial_ngram):
        """ Helper method to ngrams(). """
        #An n-gram is constructed element by element and passed on to each of the child nodes.
        #When the current node is a terminating node, it will yield the complete n-gram which was passed to it by its parents.
        
        #If this is a terminating node then yield the n-gram constructed so far.
        if self.end_of_ngram:
            yield partial_ngram

        #For each next element, construct the new partial n-gram and pass it to that element's child node, yielding every n-gram it yields.
        for ele in self.children:
            new_ngram = partial_ngram+(ele,)
            for ngram in self.children[ele].__ngrams(new_ngram):
                yield ngram

    def sized_ngrams(self, size):
        """ Get an iterator over all the n-grams of a particular size in the mapping. Returned n-grams are tuples. """
        return self.__sized_ngrams(size, ())
    def __sized_ngrams(self, size_left, partial_ngram):
        """ Helper method to sized_ngrams(). """
        #An n-gram is constructed element by element and passed on to each of the child nodes.
        #When the current node is a terminating node, it will yield the complete n-gram which was passed to it by its parents.
        
        #If the size of the currently constructed n-gram is as requested then yield it if it is an existing n-gram.
        #Stop recursion since any further recursion can only lead to longer n-grams than requested.
        if size_left == 0:
            if self.end_of_ngram:
                yield partial_ngram
        else:
            #For each next element, construct the new partial n-gram and pass it to that element's child node, yielding every n-gram it yields.
            for ele in self.children:
                new_ngram = partial_ngram+(ele,)
                for ngram in self.children[ele].__sized_ngrams(size_left-1, new_ngram):
                    yield ngram

    def ngrams_with_eles(self, targets):
        """ Get an iterator over all the n-grams which contain all the given target elements in any order. 'targets' must be a set of elements. Returned n-grams are tuples. """
        return self.__ngrams_with_eles(targets, ())
    def __ngrams_with_eles(self, targets, partial_ngram):
        """ Helper method to ngrams_with_eles(). """
        #An n-gram is constructed element by element and passed on to each of the child nodes.
        #When every target element has been added to the constructed n-gram, it will yield the complete n-gram which was passed to it by its parents.
        
        #If all targets were added to the constructed n-gram and this is a terminating node then yield the n-gram constructed so far.
        if len(targets) == 0 and self.end_of_ngram:
            yield partial_ngram

        #For each next element, construct the new partial n-gram and pass it to that element's child node, yielding every n-gram it yields.
        for ele in self.children:
            new_targets = targets - { ele }
            new_ngram = partial_ngram+(ele,)
            for ngram in self.children[ele].__ngrams_with_eles(new_targets, new_ngram):
                yield ngram

    def sized_ngrams_with_eles(self, targets, size):
        """ Get an iterator over all the n-grams of a particular size which contain all the given target elements in any order. 'targets' must be a set of elements. Returned n-grams are tuples. """
        return self.__sized_ngrams_with_eles(targets, size, ())
    def __sized_ngrams_with_eles(self, targets, size, partial_ngram):
        """ Helper method to sized_ngrams_with_eles(). """
        #An n-gram is constructed element by element and passed on to each of the child nodes.
        #When every target element has been added to the constructed n-gram, it will yield the complete n-gram which was passed to it by its parents.
        
        #If the size of the currently constructed n-gram is as requested then yield it if it is an existing n-gram containing all required elements.
        #Stop recursion since any further recursion can only lead to longer n-grams than requested.
        if size == 0:
            if len(targets) == 0 and self.end_of_ngram:
                yield partial_ngram
        else:
            #For each next element, construct the new partial n-gram and pass it to that element's child node, yielding every n-gram it yields.
            for ele in self.children:
                new_targets = targets - { ele }
                new_ngram = partial_ngram+(ele,)
                for ngram in self.children[ele].__sized_ngrams_with_eles(new_targets, size - 1, new_ngram):
                    yield ngram

    def ngrams_by_pattern(self, ngram_pattern, placeholder_indices):
        """ Get an iterator over all the n-grams which match an n-gram pattern consisting of elements, some of which will be ignored as placeholders. Placeholders are used to signify that any element can take their place. The indices of the placeholders must be specified. Returned n-grams are tuples. """
        return self.__ngrams_by_pattern(ngram_pattern, placeholder_indices, 0, ())
    def __ngrams_by_pattern(self, ngram_pattern, placeholder_indices, curr_index, partial_ngram):
        """ Helper method to ngrams_by_pattern(). """
        #An n-gram is constructed element by element and passed on to each of the child nodes.
        #When the n-gram pattern has been followed completely, it will yield the complete n-gram which was passed to it by its parents.
        
        #If all the n-gram pattern was followed completely and this is a terminating node then yield the n-gram constructed so far.
        #Stop recursion since any further recursion can only lead to longer n-grams than the n-gram pattern.
        if curr_index == len(ngram_pattern):
            if self.end_of_ngram:
                yield partial_ngram
        else:
            next_ele = ngram_pattern[curr_index]
            
            #If the next element in the n-gram pattern is a placeholder, go through every child of the current node as the next element in the n-gram.
            if curr_index in placeholder_indices:
                #For each next element, construct the new partial n-gram and pass it to that element's child node, yielding every n-gram it yields.
                for ele in self.children:
                    new_ngram = partial_ngram+(ele,)
                    for ngram in self.children[ele].__ngrams_by_pattern(ngram_pattern, placeholder_indices, curr_index+1, new_ngram):
                        yield ngram
            #If the next element in the n-gram pattern is not a placeholder, go through the child which is associated with that element.
            elif next_ele in self.children:
                new_ngram = partial_ngram+(next_ele,)
                for ngram in self.children[next_ele].__ngrams_by_pattern(ngram_pattern, placeholder_indices, curr_index+1, new_ngram):
                    yield ngram

    def values(self):
        """ Get an iterator over all the values in the mapping. """
        #Recursively visit every node and yield the value of all terminating nodes.
        
        #If this is a terminating node then yield its value.
        if self.end_of_ngram:
            yield self.value

        #For each next element, search that element's child node, yielding every n-gram it yields.
        for ele in self.children:
            for value in self.children[ele].values():
                yield value

    def items(self):
        """ Get an iterator over all (n-gram, value) pairs in the mapping. """
        return self.__items(())
    def __items(self, partial_ngram):
        """ Helper method to items(). """
        #An n-gram is constructed element by element and passed on to each of the child nodes.
        #When the current node is a terminating node, it will yield the complete n-gram which was passed to it by its parents paired with the value of this node.
        
        #If this is a terminating node then yield the n-gram constructed so far together with this node's value.
        if self.end_of_ngram:
            yield (partial_ngram, self.value)
        #For each next element, construct the new partial n-gram and pass it to that element's child node, yielding every n-gram/value pair it yields.
        for ele in self.children:
            for item in self.children[ele].__items(partial_ngram+(ele,)):
                yield item

    def __iter__(self):
        """ Iterate over all the n-grams in the mapping. Returned n-grams are tuples. """
        return self.ngrams()

    def __delitem__(self, ngram):
        """ Remove an n-gram and associated value. """
        self.pop(ngram)
