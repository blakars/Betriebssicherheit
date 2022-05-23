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

    def probability2(self,runs):
        P0=np.zeros(len(self.nodes))
        P0[0]=1.0
        P=np.zeros((len(self.nodes),len(self.nodes)))          
        for t in self.transitions:
            P[t.getSource()-9][t.getDestination()-9]=t.getRate()
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
        g=gv.Graph(format='png')
        for e in self.getNodes():
            if str(type(e)) == "<class '__main__.STATE'>":
                g.node(str(e.getNum()),shape="triangle",label=e.getName())
            elif str(type(e)) == "<class '__main__.QSTATE'>":
                g.node(str(e.getNum()),shape="ellipse",label=e.getName())
        for e in self.getTransitions():
            g.edge(str(e.getSource()),str(e.getDestination()),dir="forward",label=str(round(e.getRate(),4)))
        return g

class QSTATE:
    def __init__(self,name,num):
        self.name=name
        self.num=num

    def getNum(self):
        return self.num

    def getName(self):
        return self.name

class MDP:
    def __init__(self,markov1,action1,markov2,action2):
        self.markov1=markov1
        self.action1=action1
        self.markov2=markov2
        self.action2=action2

    def zeichnen(self):
        g=gv.Graph(format='png')
        for e in self.markov1.getNodes():
            if str(type(e)) == "<class '__main__.STATE'>":
                g.node(str(e.getNum()),shape="triangle",label=e.getName())
            elif str(type(e)) == "<class '__main__.QSTATE'>":
                g.node(str(e.getNum()),shape="ellipse",label="Q -"+e.getName()+"-"+str(self.action1))
        for e in self.markov2.getNodes():
            if e in self.markov1.getNodes():
                pass
            else:
                if str(type(e)) == "<class '__main__.STATE'>":
                    g.node(str(e.getNum()),shape="triangle",label=e.getName())
                elif str(type(e)) == "<class '__main__.QSTATE'>":
                    g.node(str(e.getNum()),shape="ellipse",label="Q -"+e.getName()+"-"+str(self.action2))
        for e in self.markov1.getTransitions():
            if e.getSource() == e.getDestination():
                pass
            else:
                g.edge(str(e.getSource()),str(e.getDestination()),dir="forward")
        for e in self.markov2.getTransitions():
            if e in self.markov1.getTransitions():
                pass
            if e.getSource() == e.getDestination():
                pass
            else:
                g.edge(str(e.getSource()),str(e.getDestination()),dir="forward")
        return g

#Main
l=1/4380
wt=1/24
ft=1/12
ur=1/4
tg=1/87600
go=1/504
ab=1/175200

OK = STATE("OK",0)
QOK = QSTATE("OK",1)
W = STATE("Warn",2)
QW = QSTATE("Warn",3)
F = STATE("Fehler",4)
QF = QSTATE("Fehler",5)
T = STATE("Techniker",6)
QT = QSTATE("Techniker",7)
G = STATE("GeneralÜb",8)
QG1 = QSTATE("GeneralÜb",9)
QG2 = QSTATE("GeneralüÜb",10)
A = STATE("Außer Betrieb",11)

T00 = TRANSITION(0,0,"OK->OK",0)
T01 = TRANSITION(0,1,"OK->QOK",1)
T12 = TRANSITION(1,2,"QOK->Warn",l)
T14 = TRANSITION(1,4,"QOK->Tec",l)
T11 = TRANSITION(1,1,"QOK->QOK",1-2*l)
T23 = TRANSITION(2,3,"Warn->QWarn",1)
T22 = TRANSITION(2,2,"Warn->Warn",0)
T45 = TRANSITION(4,5,"Fehler->QFehler",1)
T44 = TRANSITION(4,4,"Fehler-Fehler",0)
T36 = TRANSITION(3,6,"QWarn->Tec",wt)
T33 = TRANSITION(3,3,"QWarn->QWarn",1-wt)
T56 = TRANSITION(5,6,"QFehler->Tec",ft)
T55 = TRANSITION(5,5,"QFehler->QFehler",1-ft)
T67 = TRANSITION(6,7,"Tec->QTec",1)
T66 = TRANSITION(6,6,"Tec->Tec",0)
T70 = TRANSITION(7,0,"QTec->OK",ur)
T78 = TRANSITION(7,8,"QTec->Gen",tg)
T77 = TRANSITION(7,7,"QTec->QTec",1-ur-tg)
T89 = TRANSITION(8,9,"GenÜb->QGenÜb1",go)
T810 = TRANSITION(8,10,"GenÜb->QGenÜb2",ab)
T88m1 = TRANSITION(8,8,"GenÜb->GenÜb (Markov 1)",1-go)
T88m2 = TRANSITION(8,8,"GenÜb->GenÜb (Markov2)",1-ab)
T90 = TRANSITION(9,0,"QGenÜb1->OK",1)
T99 = TRANSITION(9,9,"QGenÜb1->QGenÜb1",0)
T1011 = TRANSITION(10,11,"QGenÜb2->Außer Betrieb",1)
T1010 = TRANSITION(10,10,"QGenÜb2->QGenÜb2",0)
T1111= TRANSITION(11,11,"Außer Betrieb->Außer Betrieb",1)

M1 = MARKOV("Markov-Modell1")

M1.addState(OK)
M1.addState(QOK)
M1.addState(W)
M1.addState(QW)
M1.addState(F)
M1.addState(QF)
M1.addState(T)
M1.addState(QT)
M1.addState(G)
M1.addState(QG1)

M1.addTransition(T00)
M1.addTransition(T01)
M1.addTransition(T11)
M1.addTransition(T12)
M1.addTransition(T14)
M1.addTransition(T22)
M1.addTransition(T23)
M1.addTransition(T44)
M1.addTransition(T45)
M1.addTransition(T33)
M1.addTransition(T36)
M1.addTransition(T55)
M1.addTransition(T56)
M1.addTransition(T66)
M1.addTransition(T67)
M1.addTransition(T77)
M1.addTransition(T70)
M1.addTransition(T78)
M1.addTransition(T88m1)
M1.addTransition(T89)
M1.addTransition(T99)
M1.addTransition(T90)

M2 = MARKOV("Markov-Modell2")
M2.addState(G)
M2.addState(QG2)
M2.addState(A)
M2.addTransition(T88m2)
M2.addTransition(T810)
M2.addTransition(T1010)
M2.addTransition(T1011)
M2.addTransition(T1111)

mdp1 = MDP(M1,"betreiben",M2,"außer Betrieb setzen")

mdp = mdp1.zeichnen()
mdp.view()

#g1 = M1.zeichnen()
#g1.view()

#Result1 = M1.probability(87600)
#print(sum(Result1))
#print(Result1)

#Result2 = M2.probability2(87600)
#print(sum(Result2))
#print(Result2)
#g2 = M2.zeichnen()
#g2.view()




#Result = M.probability(87600)
#print(Result)

#print(type(OK))