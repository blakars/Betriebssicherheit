from graphviz import Digraph
# Klassen
class ANDNODE: # Und-Verknüpfungselement
    def __init__(self, name):
        self.name = name
        self.nodes = []
    def add(self, node):
        self.nodes.append(node)
        return
    def availability(self):
        av = 1
        for el in self.nodes:
              av *= el.availability()
        self.avail = 1 - av
        return self.avail
    def __repr__(self):
        return "{} ({})".format(self.name, "&")

class ORNODE: # Oder-Verknüpfungselement
    def __init__(self, name):
        self.name = name
        self.nodes = []
    def add(self, node):
        self.nodes.append(node)
        return
    def availability(self):
        av = 1
        for el in self.nodes:
            av *= el.availability()
        av = 1 - av
        self.avail = 1 - av
        return self.avail
        
    def __repr__(self):
        return "{} ({})".format(self.name, ">=1")
    
class NOTNODE: # Nicht-Vernüpfungselement
    def __init__(self, name):
        self.name = name
        self.nodes = []
    def add(self, node):
        self.nodes.append(node)
        return
    def availability(self):
        # Ich gehe hier davon aus dass es maximal nur ein Child-Node geben kann
        self.avail = 1 - self.nodes[0].availability()
        return self.avail
    def __repr__(self):
        return "{} ({})".format(self.name, "NOT")
    
class EVENT: # Standardeingang
    def __init__(self, name, la, mu):
        self.name = name
        self.la = la
        self.mu = mu
        #..
    def add(self, node):
        self.nodes.append(node)
        return
    def availability(self):
        self.avail = 1 - self.notavailability()
        return self.avail
    def notavailability(self):
        self.navail = self.la / (self.la+self.mu)
        return self.navail
    def __repr__(self):
        return "{}".format(self.name)

# Baum Struktur (Aus dem Aufgabenblatt)
TOP = ANDNODE('TOP')
A = ORNODE('A')
B = ORNODE('B')
C = NOTNODE('C')
E1 = EVENT('1', 1/1000, 1/4)
E2 = EVENT('2', 1/1000, 1/4)
E3 = EVENT('3', 1/1000, 1/4)
E4 = EVENT('4', 1/1000, 1/4)

TOP.add(A)
TOP.add(B)
A.add(C)
A.add(E2)
C.add(E1)
B.add(E3)
B.add(E4)

# TOP = NOTNODE('TOP')
# C = ANDNODE('C')
# A = ORNODE('A')
# B = ORNODE('B')
# E1 = EVENT('1',1/1000,1/4)
# E2 = EVENT('2',1/1000,1/4)
# E3 = EVENT('3',1/1000,1/4)
# E4 = EVENT('4',1/1000,1/4)
# TOP.add(C)
# C.add(A)
# C.add(B)
# A.add(E1)
# A.add(E2)
# B.add(E3)
# B.add(E4)

# Baum Struktur (Aus der Abnahme)
# TOPa = NOTNODE("TOP")
# Ca = ORNODE("C")
# Aa = ORNODE("A")
# Ba = ORNODE("B")
# E1a = EVENT("1", 1/(365*24.0), 1/4.0)
# E2a = EVENT("2", 2/(365*24.0), 1/4.0)
# E3a = EVENT("3", 2/(365*24.0), 1/4.0)
# E4a = EVENT("4", 2/(365*24.0), 1/4.0)
# TOPa.add(Ca)
# Ca.add(Aa)
# Ca.add(Ba)
# Aa.add(E1a)
# Aa.add(E2a)
# Ba.add(E3a)
# Ba.add(E4a)

# Baum Visuell Aufbauen
def add_childs(tree, dot):
    if not hasattr(tree, 'nodes'):
        return dot
    for el in tree.nodes:
        if(type(el).__name__ == "EVENT"):
            dot.node(name=str(el), shape="circle", label=str(el))
        else:
            dot.node(name=str(el), shape="box", label=str(el))
        dot.edge(str(tree), str(el), arrowhead="none")
        dot = add_childs(el, dot)
    return dot

def visualize(root):
    dot = Digraph(format="png")
    dot.node(name=str(root), shape="box", label=str(root), fillcolor="wheat", style="filled")
    dot = add_childs(root, dot)
    dot.render('Baum.png', view=True)
    print("Der Graph wurde als 'Baum.png' im aktuellen Verzeichnis gespeichert!")


# ============ Ausgabe =================
print("="*20)

# Baum ausgeben
visualize(TOP)

# Vefügbarkeit
print("Die Verfügbarkeit ist:", TOP.availability())
print("="*20)