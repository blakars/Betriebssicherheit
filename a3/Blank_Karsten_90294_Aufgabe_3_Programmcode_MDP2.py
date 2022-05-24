import graphviz as gv
import numpy as np

class QSTATE:
    def __init__(self,source,destination,name):
        self.source=source
        self.destination=destination
        self.name=name

    def getSource(self):
        return self.source

    def getDestination(self):
        return self.destination

    def getName(self):
        return self.name
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
            P[t.getSource().getNum()][t.getDestination().getNum()]=t.getRate()
        i=0
        while i < runs:
            P0 = np.matmul(P0,P)
            i +=1
        return P0

    def getNodes(self):
        return self.nodes

    def getTransitions(self):
        return self.transitions

    def zeichnen(self):
        g=gv.Digraph(format='png')
        for e in self.getTransitions():
            g.edge(e.getSource().getName(),e.getDestination().getName(),label=str(round(e.getRate(),4)))
        return g

class MDP:
    def __init__(self,name):
        self.name=name
        self.actions=dict()

    def addMarkov(self,markov,action):
        if markov not in self.actions:
            self.actions[action]=markov

    def mdpProbability(self,runs):
        for m in self.actions:
            print(self.actions[m].probability(runs))
    
    def mdpZeichnen(self):
        g=gv.Digraph(strict=True, format='png')
        for m in self.actions:
            qsList=[]
            for t in self.actions[m].transitions:
                if t.getSource() != t.getDestination():
                    name="Q - "+t.getSource().getName()+" - "+m
                    qsList.append(QSTATE(t.getSource().getName(),t.getDestination().getName(),name))
            
            for q in qsList:
                g.node(q.getSource(),shape="triangle")
                g.node(q.getDestination(),shape="triangle")
                g.node(q.getName(),shape="ellipse")
                g.edge(q.getSource(),q.getName())
                g.edge(q.getName(),q.getDestination())
        return g

#Main
l=1/4380
wt=1/24
ft=1/12
ur=1/4
tg=1/87600
go=1/504
ab=1/175200

#Aufgabenteil a-c (einfaches Markov)
OK = STATE("System läuft",0)
W = STATE("Warnzustand",1)
F = STATE("Fehlerzustand",2)
T = STATE("Techniker da",3)
G = STATE("Generalüberholung",4)
A=STATE("Außer Betrieb",1)

T002=TRANSITION(G,G,"GenÜb->GenÜb",1-ab)
T012=TRANSITION(G,A,"GenÜb->AußBet",ab)
T112=TRANSITION(A,A,"AußBet->AußBet",1)

T01 = TRANSITION(OK,W,"OK->Warn",l)
T02 = TRANSITION(OK,F,"OK->Fehler",l)
T13 = TRANSITION(W,T,"Warn->Tec",wt)
T23 = TRANSITION(F,T,"Fehler->Tec",ft)
T30 = TRANSITION(T,OK,"Tec->OK",ur)
T34 = TRANSITION(T,G,"Tec->GenÜb",tg)
T40 = TRANSITION(G,OK,"GenÜb->OK",go)
T00 = TRANSITION(OK,OK,"OK->OK",1-2*l)
T11 = TRANSITION(W,W,"Warn->Warn",1-wt,)
T22 = TRANSITION(F,F,"Fehler->Fehler",1-ft,)
T33 = TRANSITION(T,T,"Tec->Tec",1-ur-tg,)
T44 = TRANSITION(G,G,"GenÜb->GenÜb",1-go,)

M1 = MARKOV("Markov-Modell1")

M1.addState(OK)
M1.addState(W)
M1.addState(F)
M1.addState(T)
M1.addState(G)

M1.addTransition(T01)
M1.addTransition(T02)
M1.addTransition(T13)
M1.addTransition(T23)
M1.addTransition(T30)
M1.addTransition(T34)
M1.addTransition(T40)
M1.addTransition(T00)
M1.addTransition(T11)
M1.addTransition(T22)
M1.addTransition(T33)
M1.addTransition(T44)

g1=M1.zeichnen()
g1.view()

res1 = M1.probability(87600)
print(res1)

M2 = MARKOV("Markov-Modell2")
G.num=0
M2.addState(G)
M2.addState(A)
M2.addTransition(T002)
M2.addTransition(T012)
M2.addTransition(T112)

g2 = M2.zeichnen()
g2.view()

Result = M2.probability(87600)
print(Result)

mdp1 = MDP("mdp1")

mdp1.addMarkov(M1,"betreiben")
mdp1.addMarkov(M2,"außer Betrieb setzen")

resgraph = mdp1.mdpZeichnen()

resgraph.view()