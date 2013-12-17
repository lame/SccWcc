import sys
import unittest
import sets
def main():
	recursion = sys.getrecursionlimit()
	sys.setrecursionlimit(100000)
	L = []
	M = []

	wccEdges = 0
	sccEdges = 0
	
	V = set(map(int, open('web-Stanford.txt').read().split()))
	File = open('web-Stanford.txt', 'r')
	edges = []
	dirAdjList = {}
	undirAdjList = {}
	for line in File:
		a = [int(n) for n in line.split()]
		edges.append(a)
	
	for v in V:
		dirAdjList[v] = []
		undirAdjList[v] = []

	for e in edges:
		dirAdjList[e[0]].append(e[1])
		undirAdjList[e[0]].append(e[1])
		undirAdjList[e[1]].append(e[0])

	for scc in SCC(V, dirAdjList):
		if len(L) < len(scc):
			L = scc
	'''		
	for wcc in SCC(V, undirAdjList):
		if len(M) < len(wcc):
			M = wcc
	'''
	out = WCC(undirAdjList)
	M = max(map(int, out))
	
	print "Nodes: ",len(V)
	print "Edges: ",len(edges)
	print "Nodes in largest WCC: ",M
	print "Edges in largest WCC: ", #edgeCount(undirAdjList, M)
	print "Nodes in largest SCC: ",len(L)
	print "Edges in largest SCC: ", edgeCount(dirAdjList, L)

	sys.setrecursionlimit(recursion)

def SCC(vert, E):
	
	I = set()
	stk = []
	index = {}
	ll = {}

	def depthFirst(verts):
		index[verts] = len(stk)
		stk.append(verts)
		ll[verts] = index[verts]

		for x in E[verts]:	##DFS
			if x not in index:
				for scc in depthFirst(x):
					yield scc
				ll[verts] = min(ll[verts], ll[x])
			elif x not in I:
				ll[verts] = min(ll[verts], ll[x])
		if ll[verts] == index[verts]:
			scc = set(stk[index[verts]:])
			del stk[index[verts]:]
			I.update(scc)
			yield scc

	for verts in vert:		#find strongly connected
		if verts not in index:
			for scc in depthFirst(verts):
				yield scc

def WCC(undirAdjList):
	def findRoot(N, R):
		while N != R[N][0]:
			N = R[N][0]
		return (N, R[N][1])
	myR = {}
	for myN in undirAdjList.keys():
		myR[myN] = (myN, 0)
	for I in undirAdjList:
		for J in undirAdjList[I]:
			(myR_I, xI) = findRoot(I, myR)
			(myR_J, xJ) = findRoot(J, myR)
			if myR_I != myR_J:
				Min = myR_I
				Max = myR_J
				if xI > xJ:
					Min = myR_J
					Max = myR_I
				myR[Max] = (Max, max(myR[Min][1]+1, myR[Max][1]))
				myR[Min] = (myR[Max][0], -1)
	Return = {}
	for I in undirAdjList:
		if myR[I][0] == I:
			Return[I] = []
	for myI in undirAdjList:
		Return[findRoot(I, myR)[0]].append(I)
	return Return

def edgeCount(dirAdjList,connected_path):
	count = 0
	List = []#dirAdjList]
	adjListDict = {}#connected_path}
	for I in connected_path:
		#List = adjListDict[I]
		for J in dirAdjList[I]:
			if J in connected_path:
				count = count+1
	return count

if __name__ == '__main__':
	main()
