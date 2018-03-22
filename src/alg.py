#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8
#
# GA: RWA with GOF
# Genetic Algorithm
# Routing and Wavelength Assignment
# General Objective Function
#
# Author: Apr 2016
# Cassio Trindade Batista - cassio.batista.13@gmail.com
# Federal University of Pará (UFPA). Belém, Brazil.
#
# Last edited on March 2018
#
# References:
# - random 'biased' choice: https://stackoverflow.com/q/25507558
# - import from parent dir: https://stackoverflow.com/a/30536516
# - multiple inheritance:   https://stackoverflow.com/q/3277367

import sys
import os

import numpy as np
import info
import networkx as nx
import itertools # TODO ??

#FIXME
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class Routing(object):
	def __init__(self):
		pass

	# https://networkx.github.io/documentation/networkx-1.10/...
	# ... reference/algorithms.shortest_paths.html
	# FIXME
	def dijkstra(self, adj_mtx, s, d):
		""" Certainly does something """
		if any([s,d])<0 or any([s,d])>adj_mtx.shape[0] or s == d:
			print 'Error: source (%d) or destination (%d) indexes are invalid' % (s,d)
			return None
		G = nx.from_numpy_matrix(adj_mtx, create_using=nx.Graph())
		hops, path = nx.bidirectional_dijkstra(G, s, d, weight=None)
		return path

	# https://networkx.github.io/documentation/networkx-1.10/...
	# ... reference/algorithms.simple_paths.html
	# FIXME
	def yen(self, mat, (s,d), k):
		if any([s,d])<0 or any([s,d])>mat.shape[0] or k<0:
			print 'Error'
			return None
		G = nx.from_numpy_matrix(mat, create_using=nx.Graph())
		paths = list(nx.shortest_simple_paths(G, s, d, weight=None))
		return paths[:k]

class WavelengthAssignment(object):
	def __init__(self):
		pass

	# local knowledge first fit wavelength assignment
	# FIXME
	def first_fit(self, N, R, num_channels):
		""" Certainly does something """
		rcurr, rnext = R[0], R[1] # look at the source node only (1st link)
		# Check whether each wavelength w is available 
		# on the first link of route R (only at the 1st link)
		for w in xrange(num_channels):
			if N[rcurr][rnext][w]:
				# automatically checks if the wavelength is available 
				# * ONLY at the output of the node *
				return self.check_local_availability(N, R, w)

		return None # block

	# https://networkx.github.io/documentation/development/...
	# ... reference/algorithms.coloring.html
	# FIXME
	def greedy_color(self, H, colors, strategy=nx.coloring.strategy_largest_first):
		G = nx.from_numpy_matrix(H, create_using=nx.Graph())
		if len(G):
			# set to keep track of colors of neighbours
			neighbour_colors = set()
			node = G.nodes()[-1] # last node added
			for neighbour in G.neighbors_iter(node):
				if neighbour in colors:
					neighbour_colors.add(colors[neighbour])
	
			for color in itertools.count():
				if color not in neighbour_colors:
					break
			# assign the node the newly found color
			#colors[node] = color
			return color
		#return colors

class RWAAlgorithm(Routing, WavelengthAssignment):
	""" This class certainly does something """
	def __init__(self):
		super(RWAAlgorithm, self).__init__()
		self.block_count = 0  # to store the number of blocked calls
		self.block_dict  = {} # store percentage of blocked calls per generation

	def routing(self):
		""" This method will be overriden """
		pass

	def wavelength_assignment(self):
		""" This method will be overriden """
		pass

	# FIXME
	def check_global_availability(self):
		# GLOBAL KNOWLEDGE first fit wavelength assignment
		color = None
		for R in routes:
			avail = 2**info.NSF_NUM_CHANNELS-1
			for r in xrange(len(R)-1):
				rcurr = R[r]
				rnext = R[r+1]

				avail &= N[rcurr][rnext]

				if avail == 0:
					break

			if avail > 0:
				color = format(avail, '0%db' % info.NSF_NUM_CHANNELS)[::-1].index('1')
				break

	# FIXME
	def check_local_availability(self, wave_mtx, route, wavelength):
		""" local knowledge wavelength assignment """
		# check if the λ chosen at the first link is availble on all links of R
		length = len(route)
		for r in xrange(length-1):
			rcurr = route[r]
			rnext = route[r+1]

			# if not available in any of the next links, block
			if not N[rcurr][rnext][wavelength]:
				return None # blocked

		return wavelength

	def save_blocks_to_file(self,):
		filename = '' % (self.name)

	def plot_fits(self, fits, PT_BR=False):
		""" This method plots """
		if PT_BR:
			import sys
			reload(sys)  
			sys.setdefaultencoding('utf8') # for plot in PT_BR

		import matplotlib.pyplot as plt
		import matplotlib.animation as anim
		from matplotlib.ticker import EngFormatter

		# do not interrupt program flow to plot
		plt.interactive(True) 

		fig, ax = plt.subplots()
		ax.set_xscale('linear')

		formatter = EngFormatter(unit='', places=1)
		ax.xaxis.set_major_formatter(formatter)

		if PT_BR:
			ax.set_xlabel(u'Gerações', fontsize=20)
			ax.set_ylabel(u'Número de chamadas atendidas', fontsize=20)
		else:
			ax.set_xlabel(u'Generations', fontsize=20)
			ax.set_ylabel(u'Number of attended calls', fontsize=20)
	
		ax.grid()
		ax.plot(fits, linewidth=2.0)
	
		x = range(0, 0, 5) # FIXME
		y = np.arange(0, 8, 1)
	
		if PT_BR:
			title =  u'Melhores fits de %d indivíduos por geração' % 0
		else:
			title =  u'Best fit values of %d individuals per generation' % 0

		fig.suptitle(title, fontsize=20)

		#plt.margins(0.02)
		plt.subplots_adjust(bottom=0.12)
	
		#plt.xticks(x)
		plt.yticks(y)
		plt.draw()
		plt.show(block=True)

	# TODO
	def plot_bp(self, net):
		if PT_BR:
			import sys
			reload(sys)  
			sys.setdefaultencoding('utf8') # for plot in PT_BR

		import matplotlib.pyplot as plt
		import matplotlib.animation as anim
		from matplotlib.ticker import EngFormatter

		# do not interrupt program flow to plot
		plt.interactive(True) 

		fig, ax = plt.subplots()
		ax.set_xscale('linear')

		formatter = EngFormatter(unit='', places=1)
		ax.xaxis.set_major_formatter(formatter)

class DijkstraFirstFit(RWAAlgorithm):
	def __init__(self):
		super(DijkstraFirstFit).__init__(self)
		self.name     = 'DFF'
		self.fullname = 'Dijkstra and First Fit'

	def routing(self, adj_mtx, source, destination):
		return self.dijkstra(adj_mtx, source, destination)

	def wavelength_assignment(self):
		return self.first_fit()

	def rwa(self, N, A, T, s, d, holding_time):
		""" This method RWAs """
		# call the routing method
		route = self.routing(A, s, d)

		# call the wavelength assignment method
		# TODO
		wavelength = self.wavelength_assignment(route, N, route, CHANNELS FIXME)

		if wavelength is not None:
			# if available on all links of R, alloc net resources for the call
			length = len(route)
			for r in xrange(length-1):
				rcurr = route[r]
				rnext = route[r+1]

				# make λ NOT available on all links of the path 
				# do not forget to make the wavelength matrix symmetrical
				N[rcurr][rnext][wavelength] = 0
				N[rnext][rcurr][wavelength] = N[rcurr][rnext][wavelength] # symm.
		
				# assign a time for it to be free again (released)
				# do not forget to make the traffic matrix symmetrical
				T[rcurr][rnext][wavelength] = holding_time
				T[rnext][rcurr][wavelength] = T[rcurr][rnext][wavelength] # symm.
	
			return 0 # allocated
		else:
			return 1 # block

# FIXME FIXME FIXME
class DijkstraGraphColoring(RWAAlgorithm):
	def rwa_dij_graph(N, A, T, holding_time, paths):
		SD = (info.NSF_SOURCE_NODE, info.NSF_DEST_NODE)
		R = dijkstra(A,SD)
		paths.append([R, None])
	
		H = np.zeros((len(paths), len(paths)), dtype=np.int)
		if len(paths) > 1:
			for i in xrange(len(paths)): # cross compare paths on i and j
				for j in xrange(i+1, len(paths)):
					for m in xrange(1,len(paths[i][0])): # cross compare routers on m and n
						for n in xrange(1,len(paths[j][0])):
							if (paths[i][0][m-1] == paths[j][0][n-1] and \
								paths[i][0][m]   == paths[j][0][n]) \
								or \
								(paths[i][0][m]  == paths[j][0][n-1] and \
								paths[i][0][m-1] == paths[j][0][n]):
								H[i][j] = 1
								H[j][i] = 1
	
		colors = {}
		for i in xrange(len(paths)):
			if paths[i][1] is not None:
				colors[i] = paths[i][1]
	
		color = greedy_color(H, colors)
	
		if color < info.NSF_NUM_CHANNELS:
			for r in xrange(len(R)-1):
				rcurr = R[r]
				rnext = R[r+1]
	
				if not get_wave_availability(color, N[rcurr][rnext]):
					color = None
					break
		else:
			color = None
	
		# update NSF graph
		if color is not None:
			for r in xrange(len(R)-1):
				rcurr = R[r]
				rnext = R[r+1]
	
				N[rcurr][rnext] -= 2**color
				N[rnext][rcurr] = N[rcurr][rnext] # make it symmetric
	
				T[rcurr][rnext][color] = holding_time
				T[rnext][rcurr][color] = T[rcurr][rnext][color]
	
			paths[-1][1] = color  # update color of the last route
			return 0 # allocated
		else:
			paths.pop(-1)
			return 1 # blocked

# FIXME FIXME FIXME
class YenFirstFit(N, A, T, holding_time):
	SD = (info.NSF_SOURCE_NODE, info.NSF_DEST_NODE)

	# alternate k shortest paths
	routes = yen(A, SD, info.K)

	for R in routes:

		# LOCAL KNOWLEDGE first fit wavelength assignment
		color = None
		rcurr, rnext = R[0], R[1] # get the first two nodes from route R
		# Check whether each wavelength ...
		for w in xrange(info.NSF_NUM_CHANNELS):
			# ... is available on the first link of route R
			if get_wave_availability(w, N[rcurr][rnext]):
				color = w
				break

		if color is not None:
			# LOCAL KNOWLEDGE assure the color chosen at the first link is
			# availble on all links of the route R
			for r in xrange(len(R)-1):
				rcurr = R[r]
				rnext = R[r+1]

				# if not available in any of the next links, block
				if not get_wave_availability(color, N[rcurr][rnext]):
					color = None
					break # block for this route, give chance for the alternate

			if color is not None:
				# if available on all links of R, alloc net resources for the
				# call
				for r in xrange(len(R)-1):
					rcurr = R[r]
					rnext = R[r+1]

					N[rcurr][rnext] -= 2**color
					N[rnext][rcurr] = N[rcurr][rnext] # make it symmetric
		
					T[rcurr][rnext][color] = holding_time
					T[rnext][rcurr][color] = T[rcurr][rnext][color]

				return 0 # allocated

	return 1 # blocked

# FIXME FIXME FIXME
class YenGraphColoring(N, A, T, holding_time, paths):
	SD = (info.NSF_SOURCE_NODE, info.NSF_DEST_NODE)

	routes = yen(A, SD, info.K)

	for R in routes:
		paths.append([R, None])

		H = np.zeros((len(paths), len(paths)), dtype=np.int)
		if len(paths) > 1:
			for i in xrange(len(paths)): # cross compare paths on i and j
				for j in xrange(i+1, len(paths)):
					for m in xrange(1,len(paths[i][0])): # cross compare routers on m and n
						for n in xrange(1,len(paths[j][0])):
							if (paths[i][0][m-1] == paths[j][0][n-1] and \
								paths[i][0][m]   == paths[j][0][n]) \
								or \
								(paths[i][0][m]  == paths[j][0][n-1] and \
								paths[i][0][m-1] == paths[j][0][n]):
								H[i][j] = 1
								H[j][i] = 1

		colors = {}
		for i in xrange(len(paths)):
			if paths[i][1] is not None:
				colors[i] = paths[i][1]

		color = greedy_color(H, colors)

		if color < info.NSF_NUM_CHANNELS:
			for r in xrange(len(R)-1):
				rcurr = R[r]
				rnext = R[r+1]

				if not get_wave_availability(color, N[rcurr][rnext]):
					color = None
					break
		else:
			color = None

		# update NSF graph
		if color is not None:
			for r in xrange(len(R)-1):
				rcurr = R[r]
				rnext = R[r+1]

				N[rcurr][rnext] -= 2**color
				N[rnext][rcurr] = N[rcurr][rnext] # make it symmetric

				T[rcurr][rnext][color] = holding_time
				T[rnext][rcurr][color] = T[rcurr][rnext][color]

			paths[-1][1] = color  # update color of the last route
			return 0 # allocated
		else:
			paths.pop(-1)
			# try another route insted of blocking immediately

	return 1 # blocked

# TODO: Main Genetic Algorithm Function
def GeneticAlgorithm(N, A, T, holding_time):
	# generates initial population with random but valid chromosomes
	population = [] # [ [[chrom], [L], wl_avail, r_len], [[chrom], [L], wl_avail, r_len], ..., ]
	trials = 0
	while len(population) < info.GA_SIZE_POP and trials < 300:
		allels = range(info.NSF_NUM_NODES) # router indexes
		chromosome = make_chromosome(A, info.NSF_SOURCE_NODE, info.NSF_DEST_NODE, allels)
		individual = [chromosome, [], 0, 0]
		if chromosome and individual not in population:
			population.append(individual)
			trials = 0
		else:
			trials += 1

	fits = []
	# <GeneticAlgorithm> ------------------------------------------------------
	for generation in range(info.GA_MIN_GEN):
		# perform evaluation (fitness calculation)
		for ind in xrange(len(population)):
			L, wl_avail, r_len = evaluate(population[ind][0], N)
			population[ind][1] = L
			population[ind][2] = wl_avail
			population[ind][3] = r_len

		# perform selection
		mating_pool = select(list(population), info.GA_MAX_CROSS_RATE)

		# perform crossover
		offspring = cross(mating_pool)
		if offspring:
			for child in offspring:
				population.pop()
				population.insert(0, [child, [], 0, 0])

		# perform mutation
		for i in xrange(int(math.ceil(info.GA_MIN_MUT_RATE*len(population)))):
			normal_ind = random.choice(population)
			trans_ind = mutate(N, normal_ind[0]) # X MEN
			if trans_ind != normal_ind:
				population.remove(normal_ind)
				population.insert(0, [trans_ind, [], 0, 0])

		# rearrange: sort population according to length .:. shortest paths first
		population.sort(key=itemgetter(2), reverse=True)

		# sort population according to wavelength availability
		population = insertion_sort(population)

		fit = 0
		for ind in population:
			if ind[2]:
				fit += 1
		fits.append(fit)

		#print generation, population[0]
	# </GeneticAlgorithm> -----------------------------------------------------

	# perform evaluation (fitness calculation)
	for ind in xrange(len(population)):
		L, wl_avail, r_len = evaluate(population[ind][0], N)
		population[ind][1]  = L
		population[ind][2]  = wl_avail
		population[ind][3]  = r_len

	# sort population according to length: shortest paths first
	population.sort(key=itemgetter(2), reverse=True)

	# sort population according to wavelength availability
	population = insertion_sort(population)
	
	fit = 0
	for ind in population:
		if ind[2]:
			fit += 1
	fits.append(fit)

	# update NSF graph
	best_route = population[0][0]
	len_route  = population[0][3]
	
	if population[0][2] > 0:
		color = population[0][1].index(1)
		for i in xrange(len_route-1):
			rcurr = best_route[i]
			rnext = best_route[i+1]

			N[rcurr][rnext] -= 2**color
			N[rnext][rcurr] = N[rcurr][rnext] # make it symmetric

			T[rcurr][rnext][color] = holding_time
			T[rnext][rcurr][color] = T[rcurr][rnext][color]

		return 0 # allocated
	else:
		return 1 # blocked

### EOF ###