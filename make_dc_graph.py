import csv
import networkx as nx
import matplotlib.pyplot as plt
dcmetro = nx.MultiDiGraph()
x = 0
#Add Stations
line = []
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
nx.set_edge_attributes(dcmetro, 'traversal',0)


#Add numbers for people entering and exiting
with open('2012MayAMPeak.csv', 'rb') as csvfile:
		connectreader = csv.reader(csvfile, delimiter=',')
		for row in connectreader:
			line.append(row)


		stationnames = line[0]
		list_of_connections = []

		for x in range(1, len(line)):
			list_of_connections.append((line[x][0], line[x][1], line[x][2]))
			p = nx.shortest_path(dcmetro, source = line[x][0], target= line[x][1])
			dcmetro.node[line[x][0]]['source'] +=float(line[x][2])
			dcmetro.node[line[x][1]]['sink'] += float(line[x][2])
#			print p
			if (len(p) == 1):
				dcmetro[p[0]][p[0]][0]['traversal'] +=float(line[x][2])
			for y in range(0, len(p)-1):
				dcmetro[p[y]][p[y+1]][0]['traversal'] +=float(line[x][2])


posx = nx.fruchterman_reingold_layout(dcmetro, k= .15)
nx.draw_networkx(dcmetro, pos=posx, with_labels=True)
