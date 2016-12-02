import csv
import networkx as nx
import matplotlib.pyplot as plt
dcmetro = nx.MultiDiGraph()
x = 0
#Add Stations
line = []
stationnames = []
with open('connectivity.csv', 'rb') as csvfile:
		connectreader = csv.reader(csvfile, delimiter=',')
		#Parse Each row in the files
		for row in connectreader:
			line.append(row)

		#Get rid of Headers
		stationnames = line[0]
		#Add stations to graph. 
		dcmetro.add_nodes_from(stationnames[1::], source = 0, sink = 0)
		list_of_connections = []

		#Add edges for each graph by parsing
		for x in range(0, len(line)):
			for y in range(0, len(line)):
				if(line[x][y] == '1'):
					list_of_connections.append((stationnames[x], stationnames[y]))
		#Add edges
		dcmetro.add_edges_from(list_of_connections, traversal = 0)


line = []
#Unsure if needed, but should set initial variables
nx.set_node_attributes(dcmetro, 'source', 0)
nx.set_node_attributes(dcmetro, 'sink', 0)
nx.set_edge_attributes(dcmetro, 'traversal', 0)


#Add numbers for people entering and exiting
with open('2012MayAMPeak.csv', 'rb') as csvfile:
		connectreader = csv.reader(csvfile, delimiter=',')
		for row in connectreader:
			line.append(row)



		for x in range(1, len(line)):
			p = nx.shortest_path(dcmetro, source = line[x][0], target= line[x][1])
			dcmetro.node[line[x][0]]['source'] += float(line[x][2])
			dcmetro.node[line[x][1]]['sink'] += float(line[x][2])
#			print p
			if (len(p) == 1):
				dcmetro[p[0]][p[0]][0]['traversal'] += float(line[x][2])
			for y in range(0, len(p)-1):
				dcmetro[p[y]][p[y+1]][0]['traversal'] += float(line[x][2])



node_labels = {}
edge_labels = {}
for x in range(0, len(dcmetro.nodes())):
	 node_labels[stationnames[x+1]] = dcmetro.node[stationnames[x+1]]['source']



 
for y in range(0, len(list_of_connections)):
#	rounded_traversal = list_of_connections
#	print rounded_traversal[y]
	print int(dcmetro[list_of_connections[y][0]][list_of_connections[y][1]][0]['traversal'])
	print list_of_connections[y][0]
	print list_of_connections[y][1]
	edge_labels[list_of_connections[y][0]][list_of_connections[y][1]] = int(dcmetro[list_of_connections[y][0]][list_of_connections[y][1]][0]['traversal'])




posx = nx.fruchterman_reingold_layout(dcmetro, k = .15)
# posx={}

# for x in range(0, len(stationnames[1::])):
# 	posx[stationnames[x+1]] = (0,0)

nx.draw_networkx_labels(dcmetro, pos = posx, labels = node_labels, edge_labels=edge_labels, font_size = 10)
nx.draw_networkx(dcmetro, pos = posx, with_labels = True)
#nx.draw_networkx_edge_labels(dcmetro, pos=posx)
#for z in range(0, len(posx)):
#	x,y = posx[stationnames[z+1]]
#	plt.text(x-.025,y+.025, s=str(node_labels[stationnames[z+1]]))




plt.show()