#!/usr/bin/env python
# coding: utf-8


#We will be considering colorings of signed grpahs, graphs where 
#all edges are positive or negative. 
#If an edge uv is positive then the color at u must be different than the color at v. 
#If an edge uv is negative then the color at u must not be the negative of that color at v. 
#We will explore the signed color function (and its dual), which is the minimum (maximum) 
#number of colorings over all choices of signs for the edges. 
import timeit




def print_signed_graph(g,signs):
    """
    Given a graph g and a list of signs for the edges we will show 
    the graph g with positive edges as blue and negative edges as red. 
    """
    EC = {}
    EC[(0,0,1)] = []#the blues associated to 1's
    EC[(1,0,0)] = []#the reds associated to 0's
    for i in range(len(signs)):
        s = signs[i]
        e = g.edges()[i]
        if s == 0:
            EC[(1,0,0)] += [[e[0],e[1]]]
        else:
            EC[(0,0,1)] += [[e[0],e[1]]]
    g.show(edge_colors=EC,figsize=2,vertex_labels=False,vertex_size=10,)
    return 0



def number_signed_colorings(g,signs,k):
    """
    Given a graph g with the signs of edges given by signs,
    we return the number of k-colorings of the signed graph. 
    
    For ease, we are working with signed-k colorings where k is a positive integer.
    The noneasy part is the association to the definition , which is as follows:
    Suppose k is even like 6. In general along pos edges colors can't be the same
    along neg edges we don't want pairs -3,3 or -2,2 or -1,1, but we translate this to
    no pairs 0,3 or 1,4 or 2,5. In general no pairs i,i+k/2.
    
    Suppose k is odd like 5. In general along pos edges colors can't be the same
    along neg edges we don't want pairs -2,2 or -1,1, but we translate this to
    no pairs 1,3 or 2,4. In general no pairs i,i+floor(k/2)
    """
    n = g.order()
    odd = True
    kk = 0
    if k%2==0:
        kk = k/2
        odd = False
    else:
        kk = (k-1)/2
    count = 0
    for c in Words(alphabet=[i for i in range(k)], length=n):
        do_count = True
        for i in range(len(signs)):
            if do_count == True:
                c1 = c[g.edges()[i][0]]
                c2 = c[g.edges()[i][1]]
                #pos edge
                if signs[i]==1 and c1==c2:
                    do_count = False
                #neg edge
                elif signs[i]==0 and odd == False:# when k is even
                    if c1==c2+kk or c1==c2-kk:
                        do_count = False
                elif signs[i]==0 and odd == True:# when k is odd
                    if (c1==0 and c1==c2) or (c1>0 and c1==c2+kk) or (c2>0 and c1==c2-kk):
                        do_count = False
        if do_count == True:
            count += 1         
    return count

def print_all_signed_information(g,k):
    """
    Given a graph g we run through all choices of signs on its edges. 
    We print out the number of colorings for each signed graph. 
    At the end we highlight the highest number of colorings and the lowest number of colorings. 
    """
    m = g.size()
    MAX = 0
    MIN = 0
    first = True
    for signs in Words(alphabet=[0,1], length=m):
        count = number_signed_colorings(g,signs,k)
        if first == True:
            MAX = count
            MIN = count
            first = False
        else:
            if count>MAX:
                MAX = count
            if count<MIN:
                MIN = count
        #Here we print the info for the signed graph
        print_signed_graph(g,signs)
        print(count,"= the number of signed",k,"-colorings.")
    #now we print the info taken over all signed colorings
    print()
    print(MAX,"= the maximum number of signed",k,"-colorings over all signed versions of g.")
    print(MIN,"= the minimum number of signed",k,"-colorings over all signed versions of g.")
    return [MAX,MIN]

def print_signed_information_sequence(g,K):
    """
    Given a graph g we will find the sequence of the maximums and minimums
    for the number of colorings over all signed graphs of g. We will calculate
    these sequences from 0 colors up to and including K colors. 
    We print some other information along the way. 
    """
    m = g.size()
    MAX_SEQ = []
    MIN_SEQ = []
    for k in range(0,K+1):
        MAX = 0
        MIN = 0
        first = True
        for signs in Words(alphabet=[0,1], length=m):
            count = number_signed_colorings(g,signs,k)
            if first == True:
                MAX = count
                MIN = count
                first = False
            else:
                if count>MAX:
                    MAX = count
                if count<MIN:
                    MIN = count
            #Here we print the info for the signed graph
            print_signed_graph(g,signs)
            print(count,"= the number of signed",k,"-colorings.")
        MAX_SEQ += [MAX]
        MIN_SEQ += [MIN]
        #now we print the info taken over all signed colorings
        print()
        print(MIN,"= the minimum number of signed",k,"-colorings over all signed versions of g.")
        print(MAX,"= the maximum number of signed",k,"-colorings over all signed versions of g.")
        print("________________________________________________________________________________")
    print("The sequence of minimums over all signed versions of g starting with 0-colorings.")
    print(MIN_SEQ)
    print("The sequence of maximums over all signed versions of g starting with 0-colorings.")
    print(MAX_SEQ)
    return [MIN_SEQ,MAX_SEQ]

def signed_information_sequence(g,K):
    """
    Given a graph g we will find the sequence of the maximums and minimums
    for the number of colorings over all signed graphs of g. We will calculate
    these sequences from 0 colors up to and including K colors. 
    """
    m = g.size()
    MAX_SEQ = []
    MIN_SEQ = []
    for k in range(0,K+1):
        MAX = 0
        MIN = 0
        first = True
        for signs in Words(alphabet=[0,1], length=m):
            count = number_signed_colorings(g,signs,k)
            if first == True:
                MAX = count
                MIN = count
                first = False
            else:
                if count>MAX:
                    MAX = count
                if count<MIN:
                    MIN = count
        MAX_SEQ += [MAX]
        MIN_SEQ += [MIN]
    return [MIN_SEQ,MAX_SEQ]





def signed_information_sequence_all_graphs(n,K):
    """
    We look at all connected graphs on n vertices and their sequences of 
    the maximums and minimums
    for the number of colorings over all signed graphs of g. We will calculate
    these sequences from 0 colors up to and including K colors. 
    We print some additional information along the way. 
    """
    START = timeit.default_timer()
    maxs = []
    mins = []
    for g in graphs.nauty_geng("{} -c".format(n)):
        info = print_signed_information_sequence(g,K)
        mins += [info[0]]
        maxs += [info[1]]
    print("***********SUMMARY************")
    index = 0
    for g in graphs.nauty_geng("{} -c".format(n)):
        g.show(figsize = 2,vertex_labels=False,vertex_size=10,)
        print("The min sequence:", mins[index])
        print("The max sequence:", maxs[index])
        index += 1
    END = timeit.default_timer()
    print("Time:", END-START)
    return 0

def signed_information_sequence_all_graphs_simplified(n,K):
    """
    We look at all connected graphs on n vertices and their sequences of 
    the maximums and minimums
    for the number of colorings over all signed graphs of g. We will calculate
    these sequences from 0 colors up to and including K colors. 
    """
    START = timeit.default_timer()
    maxs = []
    mins = []
    for g in graphs.nauty_geng("{} -c".format(n)):
        start = timeit.default_timer()
        info = signed_information_sequence(g,K)
        g.show(figsize = 2,vertex_labels=False,vertex_size=10,)
        print("The min sequence:", info[0])
        print("The max sequence:", info[1])
        end = timeit.default_timer()
        print("Time:", end-start)
    END = timeit.default_timer()
    print("Total time:", END-START)
    return 0





