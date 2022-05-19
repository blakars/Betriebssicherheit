import graphviz as gv
import numpy as np

class STATE:
    def __init__(self,name,num):
        self.name=name
        self.num=num

    def getNum(self):
        return self.num

    def getName(self):
        return self.name

class TRANSITION:
    def __init__(self,source,destination,name,rate):
        self.source=source
        self.destination=destination
        self.name=name
        self.rate=rate

    def getSource(self):
        return self.source

    def getDestination(self):
        return self.destination

    def getRate(self):
        return self.rate

class MARKOV:
    def __init__(self,name,dt=1.0):
        self.nodes=[]
        self.transitions=[]
        self.name=name

    def addState(self,state):
        self.nodes.append(state)
        return

    def addTransition(self,transition):
        self.transitions.append(transition)
        return

    def probability(self,runs):
        P0=np.zeros(len(self.nodes))
        P0[0]=1.0
        P=np.zeros((len(self.nodes),len(self.nodes)))          
        for t in self.transitions:
            P[t.getSource()][t.getDestination()]=t.getRate()

        i=0
        while i < runs:
            P0 = np.matmul(P0,P)
            i +=1
        return P0

    def getNodes(self):
        return self.nodes

    def getTransitions(self):
        return self.transitions

def zeichnen(markov):
    g=gv.Graph(format='png')
    for e in markov.getNodes():
        g.node(str(e.getNum()),shape="circle",label=e.getName())
    
    for e in markov.getTransitions():
        g.edge(str(e.getSource()),str(e.getDestination()),dir="forward",label=str(round(e.getRate(),4)))
    return g

#Main
l=1/4380
wt=1/24
ft=1/12
ur=1/4
tg=1/87600
go=1/504


#Aufgabenteil a-c (einfaches Markov)
OK = STATE("System läuft",0)
W = STATE("Warnzustand",1)
F = STATE("Fehlerzustand",2)
T = STATE("Techniker da",3)
G = STATE("Generalüberholung",4)

T01 = TRANSITION(0,1,"OK->Warn",l)
T02 = TRANSITION(0,2,"OK->Fehler",l)
T13 = TRANSITION(1,3,"Warn->Tec",wt)
T23 = TRANSITION(2,3,"Fehler->Tec",ft)
T30 = TRANSITION(3,0,"Tec->OK",ur)
T34 = TRANSITION(3,4,"Tec->GenÜb",tg)
T40 = TRANSITION(4,0,"GenÜb->OK",go)
T00 = TRANSITION(0,0,"OK->OK",1-2*l)
T11 = TRANSITION(1,1,"Warn->Warn",1-wt)
T22 = TRANSITION(2,2,"Fehler->Fehler",1-ft)
T33 = TRANSITION(3,3,"Tec->Tec",1-ur-tg)
T44 = TRANSITION(4,4,"GenÜb->GenÜb",1-go)

M = MARKOV("Markov-Modell")

M.addState(OK)
M.addState(W)
M.addState(F)
M.addState(T)
M.addState(G)

M.addTransition(T01)
M.addTransition(T02)
M.addTransition(T13)
M.addTransition(T23)
M.addTransition(T30)
M.addTransition(T34)
M.addTransition(T40)
M.addTransition(T00)
M.addTransition(T11)
M.addTransition(T22)
M.addTransition(T33)
M.addTransition(T44)

g = zeichnen(M)
g.view()

Result = M.probability(87600)
print(Result)