---
description: Some concepts and practices when analyzing communities
---

# Community detection

## Python packages:

```sh
pip install networkx
pip install python-louvain
```


## Concepts

**Graph**

A set of nodes V and edges E

**Node degree**

Number of connections that involve a node

```py
nx.degree(G_symmetric, 'Dev Anand')
```

**Clustering Coefficient**

It is observed that people who share connections in a social network tend to form associations. In other words, there is a tendency in a social network to form clusters. We can determine the clusters of a node, Local Clustering Coefficient, which is the fraction of pairs of the node's friends (that is connections) that are connected with each other. To determine the local clustering coefficient, we make use of `nx.clustering(Graph, Node)` function.

The average clustering coefficient (sum of all the local clustering coefficients divided by the number of nodes) for the symmetric Actor-network is 0.867. We can obtain it using:

```
nx.average_clustering(G_symmetric)
```

**Distance**

We can also determine the shortest path between two nodes and its length in NetworkX using `nx.shortest_path(Graph, Node1, Node2)` and `nx.shortest_path_length(Graph, Node1, Node2)` functions respectively.

Executing

```py
nx.shortest_path(G_symmetric, 'Dev Anand', 'Akshay Kumar')
```

**Eccentricity**

Eccentricity of a node A is defined as the largest distance between A and all other nodes. It can be found using `nx.eccentricity()` function.

**Degree Centrality**

The people most popular or more liked usually are the ones who have more friends. Degree centrality is a measure of the number of connections a particular node has in the network. It is based on the fact that important nodes have many connections. NetworkX has the function `degree_centrality()` to calculate the degree centrality of all the nodes of a network.

**Eigenvector Centrality**

It is not just how many individuals one is connected too, but the type of people one is connected with that can decide the importance of a node. In Delhi Roads whenever the traffic police capture a person for breaking the traffic rule, the first sentence that traffic police hears is "Do you know whom I am related to?".

Eigenvector centrality is a measure of exactly this. It decides that a node is important if it is connected to other important nodes. We can use the `eigenvector_centrality()` function of NetworkX to calculate eigenvector centrality of all the nodes in a network.

**Betweenness Centrality**

The Betweenness Centrality is the centrality of control. It represents the frequency at which a point occurs on the geodesic (shortest paths) that connected pair of points. It quantifies how many times a particular node comes in the shortest chosen path between two other nodes. The nodes with high betweenness centrality play a significant role in the communication/information flow within the network. The nodes with high betweenness centrality can have a strategic control and influence on others. An individual at such a strategic position can influence the whole group, by either withholding or coloring the information in transmission.

Networkx has the function `betweenness_centrality()` to measure it for the network. It has options to select if we want betweenness values to be normalized or not, weights to be included in centrality calculation or not, and to include the endpoints in the shortest path counts or not.

```py
betCent = nx.betweenness_centrality(G_fb, normalized=True, endpoints=True)
sorted(betCent, key=betCent.get, reverse=True)[:5]
```



## References

## 

- Vincent D Blondel, Jean-Loup Guillaume, Renaud Lambiotte, Etienne Lefebvre, Fast unfolding of communities in large networks, in Journal of Statistical Mechanics: Theory and Experiment 2008 (10), P1000

- [Network: Politics-UK](http://mlg.ucd.ie/networks/politics-uk.html)

- [Sigma js](http://sigmajs.org/)