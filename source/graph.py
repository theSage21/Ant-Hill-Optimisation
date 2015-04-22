import random
from itertools import combinations

def roulette(weights):
    """Roulette selection from a set of weights"""
    m=min(weights)
    wts=[i-m for i in weights]#weights are now >=0
    total=sum(wts)
    mark=random.random()*total#mark is 0<=mark<=max(wts)
    total=0
    for i,v in enumerate(wts):
        total+=v
        if total>=mark:return i
    #if for some reason this fails
    return random.choice(range(len(weights)))

class Vertex:
    def __init__(self,name):
        self.name=name
    def __repr__(self):return str(self.name)
class Graph:
    def __init__(self,number_of_nodes,connectivity,max_weight):
        """Create a network with 
            number_of_nodes=controls number of nodes in the network
            connectivity=controls connectivity of network. 1=fully connected
            max_weight=max weight of any edge
        """
        self.max_weight=max_weight
        self.nodes=self.__generate_nodes(number_of_nodes)#list
        self.edges=self.__generate_edges(connectivity)#dictionary
    def get_shortest_path(self,a,b):
        "implementation of djikstras"
        S=set([a])
        L={}
        for v in self.nodes:
            L[v]=self.max_weight*1e30#Assume infinity
        L[a]=0.0
        recent_addition=[a]
        #Initialization complete
        while b not in S:
            u=recent_addition[-1]
            adjacent=set(self.get_adjacent(u))
            adjacent_not_visited=adjacent-S
            #print("S: ",S," u: ",u)
            #print('Adjacent: ',adjacent)
            #print('Adjacent -S: ',adjacent_not_visited)
            for v in adjacent_not_visited:
                if L[u]+self.edges[frozenset((u,v))]<L[v]:
                    L[v]=L[u]+self.edges[frozenset((u,v))]
            names=list(set(L.keys())-S)
            #print(names)
            weights=[L[i] for i in names]
            #print(weights)
            least=weights.index(min(weights))
            least=names[least]
            #print('Least: ',least)
            S.add(least)
            recent_addition.append(least)
            #print('-'*40)
        return L[b]
    def get_nodes(self): return self.nodes
    def get_edges(self):return self.edges
    def get_adjacent(self,vertex):
        "Return a dict of adjacent nodes and the weights to get there"
        def get_other(edge,vertex):
            a=list(edge)
            a.remove(vertex)
            return a[0]
        adjacent={}
        for edge in self.edges.keys():
            if vertex in edge:
                other=get_other(edge,vertex)
                adjacent[other]=self.edges[edge]
        return adjacent
    def get_degree(self,vertex):
        degree=0
        for edge in self.edges.keys():
            if vertex in edge:degree+=1
        return degree
    def get_no_of_nodes(s):return len(s.nodes)
    def get_connectivity(s):
        no_of_nodes=len(s.nodes)
        no_of_possible_edges=sum((1 for i in combinations(s.nodes,2)))
        no_of_edges=len(s.edges.keys())
        return no_of_edges/no_of_possible_edges
    def __generate_nodes(self,no_of_nodes):
        n=[]
        for i in range(no_of_nodes):
            n.append(Vertex(i))
        return n
    def __generate_edges(self,connectivity):
        """Generates a list of edges targeting the connectivity required
        edges are of type
            { (v1,v2): weight,
              (v1,v2):weight,}
        """
        #no of edges in a fully connected graph of v vertices
        fully_connected=sum((1 for i in combinations(self.nodes,2)))
        edges_needed=connectivity*fully_connected
        edges_needed=int(edges_needed)#make integer
        #print("Needed",edges_needed)
        #print("Complete",fully_connected)
        edges={}
        for edge in range(edges_needed):
            edge=self.__generate_edge()
            while edge in edges.keys():
                edge=self.__generate_edge()
            wt=round(random.random()*self.max_weight,4)
            while wt==0:
                wt=round(random.random()*self.max_weight,4)
            edges[edge]=wt
        return edges
    def __generate_edge(self):
        a=random.choice(self.nodes)
        b=random.choice(self.nodes)
        while b==a:#To make sure we do not have loops in the network
            b=random.choice(self.nodes)
        edge=frozenset((a,b))
        return edge

def test_djikstras():
    graph=Graph(6,0,7)
    nodes=graph.get_nodes()
    named_nodes={}
    for n in nodes:
        named_nodes[(n.name)+1]=n
    nodes=named_nodes
    graph.edges={frozenset((nodes[1],nodes[2])):2,
                frozenset((nodes[1],nodes[3])):3,
                frozenset((nodes[2],nodes[4])):5,
                frozenset((nodes[2],nodes[5])):2,
                frozenset((nodes[3],nodes[5])):5,
                frozenset((nodes[4],nodes[5])):1,
                frozenset((nodes[6],nodes[5])):7,
                frozenset((nodes[6],nodes[4])):2,
                }
    start=nodes[1]
    end=nodes[4]
    path=graph.get_shortest_path(start,end)
    expected_path=[nodes[1],nodes[2],nodes[5],nodes[4]]
    print(path==5)
test_djikstras()
