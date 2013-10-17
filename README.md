ngrammap
========

A python data structure class for storing and querying n-grams.

To add n-grams
--------------
Adding the n-grams (a,a,a), (a,a,b), (a,b,a), (b,a,a) which map to None

    x = NGramMap()
    x[('a','a','a')] = None
    x[('a','a','b')] = None
    x[('a','b','a')] = None
    x[('b','a','a')] = None

To count n-gram frequency
-------------------------
Adding the n-grams (a,a,a), (a,a,b), (a,b,a), (b,a,a) several times which map to the number of times they were encountered.

    ngrams = [ ('a','a','a'), ('a','a','b'), ('a','a','a'), ('a','a','b'), ('a','b','a'), ('b','a','a'), ('a','b','a'), ('b','a','a'), ('a','b','a'), ('a','b','a') ]
        
    x = NGramMap()
    for ngram in ngrams:
        if ngram not in x:
            x[ngram] = 0
        x[ngram] += 1
        
    for ngram in x.ngrams():
        print(ngram, x[ngram])

To find n-grams which contain particular elements
-------------------------------------------------
Adding the n-grams (a,a,a), (a,a,b), (a,b,a), (b,a,a) several times which map to the number of times they were encountered.

    ngrams = [ ('a','x','y'), ('x','a','y'), ('a','x','y'), ('b','x','y'), ('c','x','z')  ]
        
    x = NGramMap()
    for ngram in ngrams:
        if ngram not in x:
            x[ngram] = 0
        x[ngram] += 1
        
    for ngram in x.ngrams_with_eles({ 'a', 'y' }):
        print(ngram, x[ngram])

To find n-grams which follow a particular pattern
-------------------------------------------------
Adding the n-grams (a,a,a), (a,a,b), (a,b,a), (b,a,a) several times which map to the number of times they were encountered.

    ngrams = [ ('a','x','y'), ('x','a','y'), ('a','x','y'), ('b','x','y'), ('c','x','z')  ]
        
    x = NGramMap()
    for ngram in ngrams:
        if ngram not in x:
            x[ngram] = 0
        x[ngram] += 1
        
    for ngram in x.ngrams_by_pattern(( None, 'x', 'y' ), { 0 }):
        print(ngram, x[ngram])

To find elements which share similar contexts
---------------------------------------------
You can find elements which occur in the same context in their n-grams, for example 'a' and 'b' share a context in the n-grams (a, x, y) and (b, x, y) as do 'p' and 'q' in the n-grams (x, p, y) and (x, q, y).

    ngrams = [ ('a','x','y'), ('x','a','y'), ('a','x','y'), ('b','x','y'), ('c','x','z')  ]
        
    x = NGramMap()
    for ngram in ngrams:
        if ngram not in x:
            x[ngram] = 0
        x[ngram] += 1
        
    for element in x.elements():
        print(element)
        for ngram in x.ngrams_with_eles({ element }):
            ele_index = ngram.index(element)
            for ngram_ in x.ngrams_by_pattern(ngram, { ele_index }):
                if ngram_[ele_index] != element:
                    print("\t", ngram_[ele_index])
