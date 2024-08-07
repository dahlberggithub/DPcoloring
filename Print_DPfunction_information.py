#!/usr/bin/env python
# coding: utf-8




#In the following code we will go through all connected graphs on n vertices
#and print off the DP function at k, the dual DP function at k, 
#whether the graph has a linear version of a cover for the DP function or dual DP function, 
#and also print an example of a linear cover as well as a list of edges in the
#same order as the cover. 


import timeit
import numpy as np
from sage.graphs.graph_coloring import number_of_n_colorings
from sage.graphs.independent_sets import IndependentSets




def permutation_decrease(pi):
    """
    Will take a permutation pi of 1,2,...,n and decerase all values
    so we have a permutation of 0,1,...,n-1
    """
    return [pi[i]-1 for i in range(len(pi))]

def permutation_increase(pi):
    """
    Will take a permutation pi of 0,1,...,n-1 and increase all values
    so we have a permutation of 1,2,...,n
    """
    return [pi[i]+1 for i in range(len(pi))]


def permutations(n):
    """
    We will use the iterator Permutations to create
    an iterator of permutations on 0,1,...,n-1
    """
    current = Permutation([i+1 for i in range(n)])
    while(not current == False):
        yield permutation_decrease(current)
        current = current.next()
    return 0

def permutation_tuple_decrease(L):
    """
    We will turn a tuple of permutations on 1,2,...n
    into a tuple of permutations on 0,1,...,n-1
    """
    return [permutation_decrease(pi) for pi in L]

def permutation_tuples(n,k):
    """
    This will be an iterator for k-tuples of permutations on 0,1,...,n-1
    """
    current = [Permutation([i+1 for i in range(n)]) for j in range(k)]
    while(True):
        yield permutation_tuple_decrease(current)
        for i in range(k):
            if not (current[i].next()==False):
                current[i] = current[i].next()
                for j in range(0,i):
                    current[j] = Permutation([i+1 for i in range(n)])
                break
            if i == k-1:
                return 0
    return 0
def tuple_iterator(n,k):
    """
    This is an iterator of tuples length n that contain numbers 0,1,...,k-1
    """
    current = [0 for i in range(n)]
    while(True):
        yield current
        for j in range(n):
            if not current[j]==k-1:
                current[j] += 1
                for i in range(j):
                    current[i]=0
                break
            if j==n-1:
                return 0
    return 0

def round_to_place(x,k):
    """
    Will round a number to k decimal places.
    """
    return float(int(x*10^k)/10^k)

def is_cover_coloring(g, PI, c):
    """
    Given a graph g, a list of permutations PI associated to edges of g (i.e. a cover)
    and a coloring choice c for the vertices,
    we will check that pi[c[a-1]] is not equal to pi[c[b-1]]
    for all edges ab in the graph
    """
    index = 0
    for e in g.edges():
        a = e[0]
        b = e[1]
        pi = PI[index]
        index += 1
        if pi[c[a]]==c[b]:
            return False
    return True

def number_cover_colorings(g,PI,k):
    """
    For a graph g and a list of permutations PI (i.e. the k-cover) 
    we will count the number of possible colorings.
    """
    n = g.order()
    count = 0
    for c in tuple_iterator(n,k):
        if is_cover_coloring(g, PI, c):
            count += 1
    return count

def DP(g,k):
    """
    We calculate the DP function of g at k. This is the smallest number of 
    colorings over all k-covers. 
    """
    n = g.order()
    m = g.size()
    first = True
    dp = 0
    for PI in permutation_tuples(k,m):
        new_dp = number_cover_colorings(g,PI,k)
        if first == True:
            dp = new_dp
            first = False
        elif new_dp<dp:
                dp = new_dp
    return dp
def dual_DP(g,k):
    """
    We calculate the dual DP function of g at k.
    This is the largest number of 
    colorings over all k-covers. 
    """
    n = g.order()
    m = g.size()
    first = True
    dp = 0
    for PI in permutation_tuples(k,m):
        new_dp = number_cover_colorings(g,PI,k)
        if first == True:
            dp = new_dp
            first = False
        elif new_dp>dp:
                dp = new_dp
    return dp

def info(g,k):
    """
    We calculate the DP function of g at k and the
    the dual DP function of g at k.
    """
    n = g.order()
    m = g.size()
    first = True
    dp = 0
    dual = 0
    dp_cover = []
    dual_cover = []
    length = 0
    for PI in permutation_tuples(k,m):
        new_dp = number_cover_colorings(g,PI,k)
        length += 1
        if first == True:
            dp = new_dp
            dual = new_dp
            dp_cover = [PI]
            dual_cover = [PI]
            first = False
        else:
            if new_dp<dp:
                dp = new_dp
                dp_cover = [PI]
            if new_dp>dual:
                dual = new_dp
                dual_cover = [PI]
    return [[dp,dp_cover], [dual,dual_cover]]

def info_using_tree(g,k):
    """
    We calculate the DP function of g at k and the
    the dual DP function of g at k using the fact that a sub-tree
    of edges can always have the identity.
    """
    n = g.order()
    m = g.size()
    if n-1==m:#i.e. we have a tree
        cover = [[i for i in range(k)] for j in range(m)]
        cc = number_of_n_colorings(g, k)
        return [[cc,[cover]],[cc,[cover]]]
    T_edges = g.min_spanning_tree()
    first = True
    dp = 0
    dual = 0
    dp_covers = []
    dual_covers = []
    identity = [i for i in range(k)]
    for P in permutation_tuples(k,m-n+1):
        PI = []
        index = 0
        for e in g.edges():
            if e in T_edges:
                PI += [identity]
            else:
                PI += [P[index]]
                index += 1
        new_dp = number_cover_colorings(g,PI,k)
        if first == True:
            dp = new_dp
            dual = new_dp
            dp_covers = [PI]
            dual_covers = [PI]
            first = False
        else:
            if new_dp == dp:
                dp_covers += [PI]
            if new_dp<dp:
                dp = new_dp
                dp_covers = [PI]
            if new_dp==dual:
                dual_covers += [PI]
            if new_dp>dual:
                dual = new_dp
                dual_covers = [PI]
    return [[dp,dp_covers], [dual,dual_covers]]

def is_linear(pi):
    """
    We check if a permutation is linear, but this only works for k=3,4,5.
    Linear is not defined well for n=6.
    """
    k = len(pi)
    if k<4:
        return True
    if k==4:
        return Permutation(permutation_increase(pi)).is_even()
    m = (pi[1]-pi[0])%k
    for i in range(1,k-1):
        if not ((pi[i+1]-pi[i])%k) ==m:
            return False
    if not ((pi[k-1]+m)%k)==pi[0]:
        return False
    return True

def is_linear_tuple(L):
    """
    Check if the whole tuple of permutations is linear.
    """
    for pi in L:
        if is_linear(pi)==False:
            return False
    return True
def has_linear_cover(covers):
    """
    Given a list of good k-covers we will return the first full linear cover
    or return false. 
    """
    for PI in covers:
        if is_linear_tuple(PI)==True:
            return PI
    return False
pi = [0,3,2,1]
is_linear(pi)


def print_all_info(n,k):
    """
    We look at all connected graphs on n vertices and print off
    the dp function at k, the dual dp function at k, and the covers
    associated to these functions. We particularly note a linear cover if one exists. 
    """
    for m in range(n-1,n*(n-1)/2+1):# so that graphs with quicker calculations go first. 
        for g in graphs.nauty_geng("{} -c".format(n)):
            if g.size()==m:
                info = info_using_tree(g,k)
                info_dp = info[0]
                info_dual = info[1]
                dp = info_dp[0]
                dp_covers = info_dp[1]
                dual = info_dual[0]
                dual_covers = info_dual[1]
                ###now we print info
                g.show(figsize=2)
                print("Edges: ", g.edges())
                print()
                print("DP function (",k,") = ", dp)
                linear = has_linear_cover(dp_covers)
                if linear == False:
                    print("NO LINEAR COVER")
                    print("A best cover: ", dp_covers[0])
                else: print("Has linear cover: ", linear)
                print()
                print("Dual function (",k,") = ", dual)
                linear = has_linear_cover(dual_covers)
                if linear == False:
                    print("NO LINEAR COVER")
                    print("A best cover: ", dual_covers[0])
                else: print("Has linear cover: ", linear)
                print("____________________________")
    return 0
def print_info(g,k):
    """
    We look at all on graph and print off
    the dp function at k, the dual dp function at k, and the covers
    associated to these functions. We particularly note a linear cover if one exists.
    """
    info = info_using_tree(g,k)
    info_dp = info[0]
    info_dual = info[1]
    dp = info_dp[0]
    dp_covers = info_dp[1]
    dual = info_dual[0]
    dual_covers = info_dual[1]
    ###now we print info
    g.show(figsize=2)
    print("Edges: ", g.edges())
    print()
    print("DP function (",k,") = ", dp)
    linear = has_linear_cover(dp_covers)
    if linear == False:
        print("NO LINEAR COVER")
        print("A best cover: ", dp_covers[0])
    else: print("Has linear cover: ", linear)
    print()
    print("Dual function (",k,") = ", dual)
    linear = has_linear_cover(dual_covers)
    if linear == False:
        print("NO LINEAR COVER")
        print("A best cover: ", dual_covers[0])
    else: print("Has linear cover: ", linear)
    print("____________________________")
    return 0
                

