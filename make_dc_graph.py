import csv
import networkx as nx
import matplotlib.pyplot as plt
dcmetro = nx.MultiDiGraph()
x = 0
#Add Stations
line = []
stationnames = []

posx={}


with open('connectivity.csv', 'rb') as csvfile:
		connectreader = csv.reader(csvfile, delimiter=',')
		#Parse Each row in the files
		for row in connectreader:
			line.append(row)

		#Get rid of Headers
		stationnames = line[0]
		#Add stations to graph. 
		dcmetro.add_nodes_from(stationnames[1::], source = 0, sink = 0, xpos=0, ypos=0)
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
nx.set_node_attributes(dcmetro, 'xpos', 0)
nx.set_node_attributes(dcmetro, 'ypos', 0)
nx.set_edge_attributes(dcmetro, 'traversal', 0)

with open('station_locations.csv', 'rb') as csvfile:
    positions = csv.reader(csvfile, delimiter=',')
    for row in positions:
    	posx[row[0]] = [int(row[1]),int(row[2])*-1]
    	dcmetro.node[row[0]]['xpos'] = int(row[1])
    	dcmetro.node[row[0]]['ypos'] = int(row[2])
# print(posx)


#Add numbers for people entering and exiting
with open('2012MayAMPeak.csv', 'rb') as csvfile:
		connectreader = csv.reader(csvfile, delimiter=',')
		for row in connectreader:
			line.append(row)



		for x in range(1, len(line)):

			p = nx.shortest_path(dcmetro, source = line[x][0], target= line[x][1])
			dcmetro.node[line[x][0]]['source'] += float(line[x][2])
			dcmetro.node[line[x][1]]['sink'] += float(line[x][2])
#			P is the shortest path -> [source .. .. .. target] if The source == Target, then shortest path p = [source]
			#Entering and Exiting same station
			if (len(p) == 1):
				dcmetro[p[0]][p[0]][0]['traversal'] += float(line[x][2])
			#Parse through each node in shortest path
			for y in range(0, len(p)-1):
				#P is the shortest path:
				dcmetro[p[y]][p[y+1]][0]['traversal'] += float(line[x][2])


edge_labels = nx.get_edge_attributes(dcmetro, 'traversal')
edges,traversal = zip(*nx.get_edge_attributes(dcmetro,'traversal').items())

node_labels = {}

# print edge_labels

##########################################
############## This code removes the extra 0 in the tuple. Why does it need to be there in the first place????
newTuple = ()
edges = {}
print traversal

for key, value in edge_labels.items():
  newTuple = (key[0], key[1])
  # print newTuple
  edges[newTuple] = value

edge_labels = edges
print edge_labels
########################################### 


#for y in range(0, len(list_of_connections)):
	# print dcmetro[list_of_connections[y][0]][list_of_connections[y][1]][0]['traversal']
	# print "\n"

 	#edge_labels[(list_of_connections[y][0],list_of_connections[y][1])] = str(dcmetro.get_edge_data(list_of_connections[y][0], list_of_connections[y][1], {'traversal':0}['traversal']))
 	#print dcmetro.get_edge_data(list_of_connections[y][0], list_of_connections[y][1], {'traversal':0}['traversal'])


 #	rounded_traversal = list_of_connections
# 	print rounded_traversal[y]
	# print type(int(dcmetro[list_of_connections[y][0]][list_of_connections[y][1]][0]['traversal']))
	# print list_of_connections[y][0]
	# print list_of_connections[y][1]
pos={}
for x in range(0, len(stationnames[1::])):
	pos[stationnames[x+1]] = (0,0)
nx.draw_networkx_edge_labels(dcmetro, pos = posx, edge_labels = edge_labels)
nx.draw_networkx(dcmetro, pos = posx, with_labels = False, node_size = 1, arrows = False, edge_color=traversal,width=4,edge_cmap=plt.cm.hot)
nx.write_gml(dcmetro, 'fnwftw.gml', stringizer=None)
#nx.draw_networkx_edge_labels(dcmetro, pos=posx)
#for z in range(0, len(posx)):
#	x,y = posx[stationnames[z+1]]
#plt.text(x-.025,y+.025, s=str(node_labels[stationnames[z+1]]))
plt.show()