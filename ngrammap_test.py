from ngrammap import NGramMap

import unittest

class GeneralTests(unittest.TestCase):

    def testGet(self):
        obj = NGramMap()

        i = 0
        obj[()] = i
        for a in range(3):
            i += 1
            obj[(a,)] = i
        for a in range(3):
            for b in range(3):
                i += 1
                obj[(a,b)] = i
        for a in range(3):
            for b in range(3):
                for c in range(3):
                    i += 1
                    obj[(a,b,c)] = i

        i = 0
        self.assertEqual(obj[()], i)
        for a in range(3):
            i += 1
            self.assertEqual(obj[(a,)], i)
        for a in range(3):
            for b in range(3):
                i += 1
                self.assertEqual(obj[(a,b)], i)
        for a in range(3):
            for b in range(3):
                for c in range(3):
                    i += 1
                    self.assertEqual(obj[(a,b,c)], i)

    def testIn(self):
        obj = NGramMap()

        obj[()] = True
        for a in range(3):
            obj[(a,)] = True
        for a in range(3):
            for b in range(3):
                obj[(a,b)] = True
        for a in range(3):
            for b in range(3):
                for c in range(3):
                    obj[(a,b,c)] = True

        self.assertTrue(() in obj)
        for a in range(3):
            self.assertTrue((a,) in obj)
        self.assertFalse((3,) in obj)
        for a in range(3):
            for b in range(3):
                self.assertTrue((a,b) in obj)
        self.assertFalse((3,1) in obj)
        self.assertFalse((1,3) in obj)
        for a in range(3):
            for b in range(3):
                for c in range(3):
                    self.assertTrue((a,b,c) in obj)
        self.assertFalse((3,1,1) in obj)
        self.assertFalse((1,3,1) in obj)
        self.assertFalse((1,1,3) in obj)

        self.assertFalse((1,1,1,1) in obj)
        self.assertFalse((1,1,3,1) in obj)

    def testInSparse(self):
        obj = NGramMap()

        obj[(1,2)] = True
        obj[(2,1)] = True
        obj[(1,2,3)] = True
        obj[(3,2,3)] = True
        obj[(1,1,3)] = True
        obj[(1,1,2)] = True
        obj[(3,2,1)] = True

        self.assertTrue((1,2) in obj)
        self.assertTrue((2,1) in obj)
        self.assertTrue((1,2,3) in obj)
        self.assertTrue((3,2,3) in obj)
        self.assertTrue((1,1,3) in obj)
        self.assertTrue((1,1,2) in obj)
        self.assertTrue((3,2,1) in obj)

        self.assertFalse(() in obj)
        self.assertFalse((1,) in obj)
        self.assertFalse((1,3,2) in obj)
        self.assertFalse((1,2,2) in obj)
        self.assertFalse((1,2,2,3) in obj)

    def testElements(self):
        obj = NGramMap()

        obj[(1,2)] = True
        obj[(2,1)] = True
        obj[(1,2,3)] = True
        obj[(4,2,3)] = True
        obj[(1,5,3)] = True
        obj[(1,1,2)] = True
        obj[(3,2,1)] = True

        self.assertEqual(set(obj.elements()), { 1, 2, 3, 4, 5 })

    def testNgrams(self):
        obj = NGramMap()

        ngrams = [()]
        obj[()] = True
        for a in range(3):
            ngrams.append((a,))
            obj[(a,)] = True
        for a in range(3):
            for b in range(3):
                ngrams.append((a,b))
                obj[(a,b)] = True
        for a in range(3):
            for b in range(3):
                for c in range(3):
                    ngrams.append((a,b,c))
                    obj[(a,b,c)] = True

        assert len(ngrams) == len(set(ngrams))
        self.assertEqual(set(obj.ngrams()), set(ngrams))

    def testSizedNgrams(self):
        obj = NGramMap()

        ngrams = []
        obj[()] = True
        for a in range(3):
            obj[(a,)] = True
        for a in range(3):
            for b in range(3):
                ngrams.append((a,b))
                obj[(a,b)] = True
        for a in range(3):
            for b in range(3):
                for c in range(3):
                    obj[(a,b,c)] = True

        assert len(ngrams) == len(set(ngrams))
        self.assertEqual(set(obj.sized_ngrams(2)), set(ngrams))

    def testNgramsWithElesShort(self):
        obj = NGramMap()

        ngrams = []
        obj[()] = True
        for a in range(5):
            if a == 2:
                ngrams.append((a,))
            obj[(a,)] = True
        for a in range(5):
            for b in range(5):
                if a == 2 or b == 2:
                    ngrams.append((a,b))
                obj[(a,b)] = True
        for a in range(5):
            for b in range(5):
                for c in range(5):
                    if a == 2 or b == 2 or c == 2:
                        ngrams.append((a,b,c))
                    obj[(a,b,c)] = True

        assert len(ngrams) == len(set(ngrams))
        self.assertEqual(set(obj.ngrams_with_eles({ 2 })), set(ngrams))

    def testNgramsWithElesLong(self):
        obj = NGramMap()

        ngrams = []
        obj[()] = True
        for a in range(5):
            obj[(a,)] = True
        for a in range(5):
            for b in range(5):
                obj[(a,b)] = True
        for a in range(5):
            for b in range(5):
                for c in range(5):
                    if { a, b, c }.issuperset({ 2, 3, 4 }):
                        ngrams.append((a,b,c))
                    obj[(a,b,c)] = True
        for a in range(5):
            for b in range(5):
                for c in range(5):
                    for d in range(5):
                        if { a, b, c, d }.issuperset({ 2, 3, 4 }):
                            ngrams.append((a,b,c,d))
                        obj[(a,b,c,d)] = True
        for a in range(5):
            for b in range(5):
                for c in range(5):
                    for d in range(5):
                        for e in range(5):
                            if { a, b, c, d, e }.issuperset({ 2, 3, 4 }):
                                ngrams.append((a,b,c,d,e))
                            obj[(a,b,c,d,e)] = True

        assert len(ngrams) == len(set(ngrams))
        self.assertEqual(set(obj.ngrams_with_eles({ 2, 3, 4 })), set(ngrams))

    def testSizedNgramsWithEles(self):
        obj = NGramMap()

        ngrams = []
        obj[()] = True
        for a in range(5):
            obj[(a,)] = True
        for a in range(5):
            for b in range(5):
                obj[(a,b)] = True
        for a in range(5):
            for b in range(5):
                for c in range(5):
                    obj[(a,b,c)] = True
        for a in range(5):
            for b in range(5):
                for c in range(5):
                    for d in range(5):
                        if { a, b, c, d }.issuperset({ 2, 3, 4 }):
                            ngrams.append((a,b,c,d))
                        obj[(a,b,c,d)] = True
        for a in range(5):
            for b in range(5):
                for c in range(5):
                    for d in range(5):
                        for e in range(5):
                            obj[(a,b,c,d,e)] = True

        assert len(ngrams) == len(set(ngrams))
        self.assertEqual(set(obj.sized_ngrams_with_eles({ 2, 3, 4 }, 4)), set(ngrams))

    def testNgramsByPatternShort(self):
        obj = NGramMap()

        ngrams = []
        obj[()] = True
        for a in range(5):
            obj[(a,)] = True
        for a in range(5):
            for b in range(5):
                obj[(a,b)] = True
        for a in range(5):
            for b in range(5):
                for c in range(5):
                    if a == 1 and c == 2:
                        ngrams.append((a,b,c))
                    obj[(a,b,c)] = True

        assert len(ngrams) == len(set(ngrams))
        self.assertEqual(set(obj.ngrams_by_pattern(( 1, None, 2 ), { 1 })), set(ngrams))

    def testNgramsByPatternLong(self):
        obj = NGramMap()

        ngrams = []
        obj[()] = True
        for a in range(5):
            obj[(a,)] = True
        for a in range(5):
            for b in range(5):
                obj[(a,b)] = True
        for a in range(5):
            for b in range(5):
                for c in range(5):
                    obj[(a,b,c)] = True
        for a in range(5):
            for b in range(5):
                for c in range(5):
                    for d in range(5):
                        obj[(a,b,c,d)] = True
        for a in range(5):
            for b in range(5):
                for c in range(5):
                    for d in range(5):
                        for e in range(5):
                            if b == 1 and d == 2:
                                ngrams.append((a,b,c,d,e))
                            obj[(a,b,c,d,e)] = True
        for a in range(5):
            for b in range(5):
                for c in range(5):
                    for d in range(5):
                        for e in range(5):
                            for f in range(5):
                                obj[(a,b,c,d,e,f)] = True

        assert len(ngrams) == len(set(ngrams))
        self.assertEqual(set(obj.ngrams_by_pattern(( None, 1, None, 2, None ), { 0, 2, 4 })), set(ngrams))

    def testValues(self):
        obj = NGramMap()

        i = 0
        values = [i]
        obj[()] = i
        for a in range(3):
            i += 1
            values.append(i)
            obj[(a,)] = i
        for a in range(3):
            for b in range(3):
                i += 1
                values.append(i)
                obj[(a,b)] = i
        for a in range(3):
            for b in range(3):
                for c in range(3):
                    i += 1
                    values.append(i)
                    obj[(a,b,c)] = i

        assert len(values) == len(set(values))
        self.assertEqual(set(obj.values()), set(values))

    def testItems(self):
        obj = NGramMap()

        i = 0
        items = [((), i)]
        obj[()] = i
        for a in range(3):
            i += 1
            items.append(((a,), i))
            obj[(a,)] = i
        for a in range(3):
            for b in range(3):
                i += 1
                items.append(((a,b), i))
                obj[(a,b)] = i
        for a in range(3):
            for b in range(3):
                for c in range(3):
                    i += 1
                    items.append(((a,b,c), i))
                    obj[(a,b,c)] = i

        assert len(items) == len(set(items))
        self.assertEqual(set(obj.items()), set(items))

    def testLen(self):
        obj = NGramMap()

        i = 0
        obj[()] = i
        self.assertEqual(len(obj), i+1)
        for a in range(3):
            i += 1
            obj[(a,)] = i
            self.assertEqual(len(obj), i+1)
        for a in range(3):
            for b in range(3):
                i += 1
                obj[(a,b)] = i
                self.assertEqual(len(obj), i+1)
        for a in range(3):
            for b in range(3):
                for c in range(3):
                    i += 1
                    obj[(a,b,c)] = i
                    self.assertEqual(len(obj), i+1)
        i += 1
        obj[()] = i
        self.assertEqual(len(obj), i)

    def testPop(self):
        obj = NGramMap()

        i = 0
        obj[()] = i
        n = 1
        for a in range(3):
            i += 1
            obj[(a,)] = i
            n += 1
        for a in range(3):
            for b in range(3):
                i += 1
                obj[(a,b)] = i
                n += 1
        for a in range(3):
            for b in range(3):
                for c in range(3):
                    i += 1
                    obj[(a,b,c)] = i
                    n += 1
        
        i = 0
        self.assertEqual(obj.pop(()), i)
        n -= 1
        self.assertEqual(len(obj), n)
        self.assertFalse(() in obj)
        for a in range(3):
            i += 1
            self.assertEqual(obj.pop((a,)), i)
            n -= 1
            self.assertEqual(len(obj), n)
            self.assertFalse((a,) in obj)
        for a in range(3):
            for b in range(3):
                i += 1
                self.assertEqual(obj.pop((a,b)), i)
                n -= 1
                self.assertEqual(len(obj), n)
                self.assertFalse((a,b) in obj)
        for a in range(3):
            for b in range(3):
                for c in range(3):
                    i += 1
                    self.assertEqual(obj.pop((a,b,c)), i)
                    n -= 1
                    self.assertEqual(len(obj), n)
                    self.assertFalse((a,b,c) in obj)
                    
        assert n == 0

    def testPopInterpersed(self):
        obj = NGramMap()

        #N-gram of 0
        
        i = 0
        j = i
        k = i
        obj[()] = i
        n = 1
        
        self.assertEqual(obj.pop(()), j)
        n -= 1
        self.assertEqual(len(obj), n)
        self.assertFalse(() in obj)
        
        obj[()] = k
        n += 1

        #N-gram of 1
        
        j = i
        k = i
        for a in range(3):
            i += 1
            obj[(a,)] = i
            n += 1
        
        for a in range(3):
            j += 1
            self.assertEqual(obj.pop((a,)), j)
            n -= 1
            self.assertEqual(len(obj), n)
            self.assertFalse((a,) in obj)
        
        for a in range(3):
            k += 1
            obj[(a,)] = k
            n += 1

        #N-gram of 2
            
        j = i
        k = i
        for a in range(3):
            for b in range(3):
                i += 1
                obj[(a,b)] = i
                n += 1
        
        for a in range(3):
            for b in range(3):
                j += 1
                self.assertEqual(obj.pop((a,b)), j)
                n -= 1
                self.assertEqual(len(obj), n)
                self.assertFalse((a,b) in obj)
        
        for a in range(3):
            for b in range(3):
                k += 1
                obj[(a,b)] = k
                n += 1

        #N-gram of 3
                
        j = i
        k = i
        for a in range(3):
            for b in range(3):
                for c in range(3):
                    i += 1
                    obj[(a,b,c)] = i
                    n += 1
        
        for a in range(3):
            for b in range(3):
                for c in range(3):
                    j += 1
                    self.assertEqual(obj.pop((a,b,c)), j)
                    n -= 1
                    self.assertEqual(len(obj), n)
                    self.assertFalse((a,b,c) in obj)


try:
    unittest.main()
except:
    pass

import time
import random

num_ngrammaps = 500

for max_ngram_size in [3, 10]:
    for max_ele_value in [3, 10]:
        print()
        print("====================================")
        print("max ngram size", max_ngram_size)
        print("max ele value", max_ele_value)
        print()

        ngrams = [ [tuple( random.randint(1,max_ele_value) for _ in range(random.randint(1,max_ngram_size)) ) for _ in range(2000)] for _ in range(num_ngrammaps) ]
        ngrammaps = [ None for _ in range(num_ngrammaps) ]

        t = time.clock()
        for i in range(num_ngrammaps):
            ngrammaps[i] = NGramMap()
            for ngram in ngrams[i]:
                ngrammaps[i][ngram] = True
        print("__setitem__ timing:", round(time.clock() - t, 2))

        items = [ None for _ in range(num_ngrammaps) ]

        t = time.clock()
        for i in range(num_ngrammaps):
            items[i] = list(ngrammaps[i].items())
        print("items timing:", round(time.clock() - t, 2))

        t = time.clock()
        for i in range(num_ngrammaps):
            for (ngram, value) in items[i]:
                ngrammaps[i][ngram]
        print("__getitem__ timing:", round(time.clock() - t, 2))
    
        t = time.clock()
        for i in range(num_ngrammaps):
            list(ngrammaps[i].ngrams_with_eles({ random.randint(1,max_ele_value) }))
        print("ngrams_with_eles short timing:", round(time.clock() - t, 2))

        t = time.clock()
        for i in range(num_ngrammaps):
            list(ngrammaps[i].ngrams_with_eles({ random.randint(1,max_ele_value) for _ in range(random.randint(1,max_ngram_size)) }))
        print("ngrams_with_eles long timing:", round(time.clock() - t, 2))

        t = time.clock()
        for i in range(num_ngrammaps):
            ngram = random.choice(ngrams[i])
            list(ngrammaps[i].ngrams_by_pattern(ngram, { j for j in range(len(ngram)) if random.random() > 0.5 } ))
        print("ngrams_by_pattern timing:", round(time.clock() - t, 2))

        t = time.clock()
        for i in range(num_ngrammaps):
            for (ngram, value) in items[i]:
                ngrammaps[i].pop(ngram)
        print("pop timing:", round(time.clock() - t, 2))
