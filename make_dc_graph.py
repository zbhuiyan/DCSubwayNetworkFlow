import csv
import networkx as nx
import matplotlib.pyplot as plt
dcmetro = nx.MultiDiGraph()
x = 0
line = []
with open('connectivity.csv', 'rb') as csvfile:
		connectreader = csv.reader(csvfile, delimiter=',')
		for row in connectreader:
			line.append(row)

		stationnames = line[0]
#		print stationnames
		dcmetro.add_nodes_from(stationnames[1::])
		list_of_connections = []
		print line[0][0]
		for x in range(0, len(line)):
			for y in range(0, len(line)):
				print y
				if(line[x][y] == '1'):
					print 'hello'
					list_of_connections.append((stationnames[x], stationnames[y]))
		dcmetro.add_edges_from(list_of_connections)

		posx = nx.fruchterman_reingold_layout(dcmetro, k= .15)
		nx.draw_networkx(dcmetro, pos=posx, with_labels=True)
		print list_of_connections
		plt.show()
		#for x in range(1, len(stationnames)):
		#	dcmetro.add_node
		#for x in range(1, len(line)):
		#	print(x)