# DPcoloring

This project contains code in SAGEMATH to calculate the DP function for graphs. DP coloring is a generalization of list coloring. For a full intoduction see the paper [A Polynomial Method for Counting Colorings of S-labeled Graphs](https://arxiv.org/abs/2312.11744) for the particular approach we are using to calculate the DP function. 

All the code in this project has been done in [SageMath](https://www.sagemath.org/), which is a python based language. 

To calculate the DP function of a graph G at k we first search through all k-fold covers of G. This is essentially a m-tuple of permutations of {1,2,...,k} where m is the number of edges of G. We have an underlying fixed order of our edges so that each permutation in the m-tuple is associated to a specific edge. Given a m-tuple of permutations we count the number of colorings of the vertices using k colors with the following restriction. We require that if permutation pi is associated with the edge from vertex i to vertex j (supposing that i<j), vertex i is colored a and vertex j is colored b then our restriction is that pi(a) is not equal to b. Note that the traditional notion of coloring is when all permutations in the m-tuple are the identity. To find the DP function of G at k we find the minimum count of colorings with the stated restriction over all m-tuples of permutations. 
