from graph import Graph,roulette
import random

def line(string):
    print(' '*40,end='\r')
    print(string,end='\r')

class Ant:
    def __init__(self,name,position):
        self.name=name
        self.position=position
        self.alive=True
        self.path=[]
        self.found=False
    def found_end(self):self.found=True
    def kill(self):
        if not self.alive:raise Exception("You cannot kill a dead ant")
        self.alive=False
    def is_alive(self):return self.alive
    def get_path(self):return self.path
    def get_name(self):return self.name
    def get_position(self):return self.position
    def set_position(self,pos):
        self.position=pos
        self.path.append(pos)
    def select_next_node(self,nodes_with_pheromones):
        acceptable_nodes=[]
        weight_list=[]
        for node in nodes_with_pheromones.keys():
            if node not in self.path:
                acceptable_nodes.append(node)
                weight_list.append(nodes_with_pheromones[node])
        if len(weight_list)==0:return None#No node can be traversed
        chosen_node=acceptable_nodes[roulette(weight_list)]
        return chosen_node

class AntHill:
    def __init__(self,graph,ant_pheromone_deposit,evaporation_rate):
        """Maps a graph to an anthill"""
        self.graph=graph
        self.wave_number=0
        self.ant_deposit=ant_pheromone_deposit
        self.evaporation_rate=evaporation_rate
        self.pheromone=self.__generate_pheromone_trail()
    def __get_path_length(self,path):
        length=0.0
        for index,node in enumerate(path):
            if index==0:continue
            last=path[index-1]
            edge=frozenset((node,last))
            length+=self.graph.edges[edge]
        return length
    def __generate_pheromone_trail(self):
        pheromone={}
        for edge in self.graph.get_edges():
            pheromone[edge]=0.0
        return pheromone
    def optimize(self,start,end):
        """Runs the optimization"""
        paths=[]
        for i in range(1000):
            path,found_end=self.__explorer_wave(start,end)
            path_length=0.0
            print("Wave: ",i,"Length: ",path,found_end,end='\r')
            paths.append(path)
        return paths
    def __get_deposit(self,ant_or_path):
        if type(ant_or_path)==Ant: path=ant.get_path()
        else:path=ant_or_path
        length=self.__get_path_length(path)
        if len(path)==1:return 1
        return self.ant_deposit/length
    def __update_pheromone(self,paths):
        head=0
        while True:
            all_complete=True
            deposits=[]
            for path in paths:
                if head>len(path):continue#Path has been completed
                else:
                    all_complete=False#This path is left
                    path=path[:head]#This is the path where the ant is at
                    try:
                        last=path[-1]
                        second_last=path[-2]
                    except IndexError: continue
                    else:
                        edge=frozenset((last,second_last))
                        deposit=self.__get_deposit(path)
                        deposits.append((edge,deposit))
            for edge,deposit in deposits:
                self.pheromone[edge]+=deposit
            for edge in self.pheromone.keys():
                self.pheromone[edge]-=self.evaporation_rate
            if all_complete:break
            head+=1

    def __explorer_wave(self,start,end):
        "Release a wave of ants from start, \
        looking for end"
        ants=[Ant(i,start) for i in range(100)]
        found_end=False
        iteration=0
        while True in (ant.is_alive() for ant in ants):#An ant is still alive
            iteration+=1
            for ant in ants:
                if not ant.is_alive():continue#Skip dead ants
                pos=ant.get_position()
                adjacent=self.graph.get_adjacent(pos)
                if len(adjacent)==0:
                    ant.kill()#Reached pendent vertex
                    continue
                pheromone_data={}
                for node in adjacent:
                    edge=frozenset((pos,node))
                    pheromone_data[node]=self.pheromone[edge]
                    pheromone_data[node]+=1.0/self.graph.edges[edge]
                next_node=ant.select_next_node(pheromone_data)
                #----------switch position
                if next_node==None: ant.kill()
                elif next_node==end:
                    ant.kill()
                    found_end=True
                    ant.found_end()
                else: 
                    ant.set_position(next_node)#Move ant
                    edge=frozenset((next_node,pos))
            #All ants have moved a step
            #Update pheromone
            paths=[]
            for ant in (i for i in ants if i.found):
                paths.append(ant.get_path())
            self.__update_pheromone(paths)
        #All ants have either reached the destination or have died
        all_paths=[]
        for ant in ants:
            if not ant.found:continue
            path=ant.get_path()
            path_length=self.__get_path_length(path)
            all_paths.append(path_length)
        #--------------find shortest_path and return
        shortest=min(all_paths)
        return shortest,found_end

def test(size,connectivity):
    graph=Graph(size,connectivity,1)
    hill=AntHill(graph,0.3,0.1)
    vertex=graph.get_nodes()
    start=random.choice(vertex)
    end=random.choice(vertex)
    while end==start:
        end=random.choice(vertex)
    path=graph.get_shortest_path(start,end)
    print('Graph size,connectivity: ',len(graph.get_nodes()),graph.get_connectivity())
    print('Connectivity',graph.get_connectivity())
    print('Approximate shortest',graph.get_shortest_path(start,end))
    paths=hill.optimize(start,end)

if __name__=='__main__':
    test(20,0.8)
