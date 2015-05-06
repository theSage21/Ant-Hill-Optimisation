from graph import Graph,roulette
import random

class Ant:
    """An ant. Subclass this to implement various methods of the ant"""
    def __init__(self,name,position):
        self.name=name
        self.position=position
        self.alive=True
        self.path=[self.position]
        self.found=False#found end. analogus to found food
    def found_end(self):self.found=True
    def kill(self):
        if not self.alive:raise Exception("You cannot kill a dead ant.")
        self.alive=False
    def is_alive(self):return self.alive
    def get_path(self):return self.path
    def get_name(self):return self.name
    def get_position(self):return self.position
    def set_position(self,pos):
        self.position=pos
        self.path.append(pos)
    def move_to_next_node(self,nodes_with_weights,alpha,beta):
        """Expects a dictionary of nodes:(edge length,pheromone)
        at nodes_with_weights"""
        acceptable=[]
        weight_list=[]
        for node in nodes_with_weights.keys():
            if node not in self.path:#if not traversed earlier
                acceptable.append(node)
                length,pheromone=nodes_with_weights[node]
                weight=(pheromone**alpha)*((1.0/length)**beta)
                weight_list.append(weight)
        if len(weight_list)==0:
            #No node can be traversed
            self.kill()
            return
        total=sum(weight_list)
        probability_of_selection=[i/total for i in weight_list]
        chosen_node=acceptable[roulette(probability_of_selection)]
        #print('Chosen',chosen_node)
        self.set_position(chosen_node)

class AntHill:
    """Additional methods provided on the graph class to impolement
    an ant hill optimisation technique"""
    def __init__(self,graph,start,end,number_of_ants=100,evaporation_rate=0.1):
        self.graph=graph
        self.start=start
        self.end=end
        self.number_of_ants=number_of_ants
        self.evaporation_rate=evaporation_rate
        self.pheromones=self.__initial_pheromone()
    def __evaporate(self):
        """Evaporates pheromone from the entire graph"""
        for edge in self.pheromones.keys():
            self.pheromones[edge]-=self.evaporation_rate
            if self.pheromones[edge]<0:self.pheromones[edge]=0.01
    def __initial_pheromone(self):
        """Deposits initial level of pheromone on the entire map"""
        pheromone={}
        deposit=self.number_of_ants/self.graph.get_shortest_path(self.start,self.end)
        #print('Default deposit',deposit)
        for edge in self.graph.get_edges():
            pheromone[edge]=deposit
        return pheromone
    def __wave_of_ants(self,ants):
        end_found=False
        found_path=[]
        while True in (ant.is_alive() for ant in ants):
            self.__evaporate()
            #print('Pheromones',self.pheromones)
            for ant in (i for i in ants if i.is_alive()):
                pos=ant.get_position()
                #conditions to kill ants
                if pos==self.end:
                    end_found=True
                    path=ant.get_path()
                    self.__deposit_pheromone(path)
                    found_path.append(path)
                    ant.found_end()
                    ant.kill()
                    continue
                adjacent=self.graph.get_adjacent(pos)
                #print('adjacent',ant.name,adjacent)
                if adjacent=={}:
                    ant.kill()
                    continue
                #we have adjacent edges
                weights={}
                for vertex in adjacent.keys():
                    edge_weight=adjacent[vertex]
                    edge=frozenset((vertex,pos))
                    phero_weight=self.pheromones[edge]
                    weights[vertex]=(edge_weight,phero_weight)
                ant.move_to_next_node(weights,self.alpha,self.beta)
        #---all ants are dead
        return found_path,end_found
    def __deposit_pheromone(self,path):
        """Deposits pheromone on the path specified"""
        length=self.graph.get_path_length(path)
        if length!=0: value= self.number_of_ants/length
        else:value=0
        #----deposit on path
        last=None
        #print(path)
        for node in path:
            #print('Node',node)
            if last!=None:
                edge=frozenset((last,node))
                self.pheromones[edge]+=value
            last=node
    def __generate_ants(self):
        ants=[]
        for i in range(self.number_of_ants):
            ant=Ant(i,self.start)
            ants.append(ant)
        return ants
    def run(self,beta=1,alpha=1,rho=0.5):
        self.alpha=alpha
        self.beta=beta
        self.rho=rho
        #----------
        iteration=0
        while True:
            ants=self.__generate_ants()
            paths,end_found=self.__wave_of_ants(ants)
            #--------
            lengths=[self.graph.get_path_length(i) for i in paths]
            try:
                print(iteration,min(lengths),end_found)
            except:print(iteration,end_found)
            iteration+=1
def test():
    g=Graph(70,0.8,10)
    vertices=g.get_nodes()
    start=random.choice(vertices)
    end=random.choice(vertices)
    while end==start:
        end=random.choice(vertices)
    print('djikstras: ',g.get_shortest_path(start,end))
    hill=AntHill(g,start,end)
    hill.run()
if __name__=='__main__':
    test()
