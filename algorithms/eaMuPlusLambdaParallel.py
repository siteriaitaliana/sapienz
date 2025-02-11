import random
import time
import pickle
import multiprocessing as mp

from deap import tools
import os
# from devices import emulator
import settings

# global results for mp callback
results = []
# idle_devices = []

def process_results(data):
	indi_index, fitness = data
	results.append((indi_index, fitness))
	# idle_devices.append(device)

def evaluate_in_parallel(eval_suite_parallel, individuals, gen):
	""" Evaluate the individuals fitnesses and assign them to each individual
	:param eval_fitness: The fitness evaluation fucntion
	:param individuals: The individuals under evaluation
	:param pool_size:
	:return: When all individuals have been evaluated
	"""

	# init global states
	# while len(results) > 0:
	# 	results.pop()
	# while len(idle_devices) > 0:
	# 	idle_devices.pop()

	# 1. get idle devices
	# idle_devices.extend(emulator.get_devices())

	# 2. assign tasks to devices
	print('length individuals: ' + repr(len(individuals)))
	pool = mp.Pool(processes=1)
	for i in range(0, len(individuals)):
		# while len(idle_devices) == 0:
		# 	time.sleep(0.5)
	# eval_suite_parallel(individuals[0],0,gen)
		pool.apply_async(eval_suite_parallel, args=(individuals[i], gen, i),
						callback=process_results)

	print ("### evaluate_in_parallel is waiting for all processes to finish ... ")
	# should wait for all processes to finish
	pool.close()
	pool.join()

	print ("### ... evaluate_in_parallel finished")
	# assign results
	while len(results) > 0:
		i, fitness = results.pop(0)
		# print (i, fitness)
		individuals[i]["fitness"]["values"] = fitness
		individuals[i]["fitness"]["valid"] = True

def evolve(population, toolbox, mu, lambda_, cxpb, mutpb, ngen, apk_dir, stats=None, halloffame=None, verbose=__debug__):
	
	logbook = tools.Logbook()
	logbook.header = ['gen', 'nevals'] + (stats.fields if stats else [])	
	# for ind in population:
	# 	print(ind["fitness"]["valid"])
	# Evaluate the individuals with an invalid fitness
	invalid_ind = [ind for ind in population if not ind["fitness"]["valid"]]
	# print('invalid_ind: ', invalid_ind)
	# fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
	# for ind, fit in zip(invalid_ind, fitnesses):
	# 	ind["fitness"]["values"] = fit	
	evaluate_in_parallel(toolbox.evaluate, invalid_ind, 0)
	# print('population', population)
	# discard invalid population individual
	for i in range(len(population) - 1, -1, -1):
		if not population[i]["fitness"]["valid"]:
			del population[i]
	if halloffame is not None:
		halloffame.update(population)
	# print ('arrive here!! need to mark valid them now')
	record = stats.compile(population) if stats is not None else {}
	logbook.record(gen=0, nevals=len(invalid_ind), **record)
	if verbose:
		print (logbook.stream)

	# Begin the generational process
	for gen in range(1, ngen + 1): 
		# Vary the population
		offspring = varOr(population, toolbox, lambda_, cxpb, mutpb)
		for i in range(len(offspring)):
			offspring[i]["fitness"]["valid"] = False
		# Evaluate the individuals with an invalid fitness
		invalid_ind = [ind for ind in offspring if not ind["fitness"]["valid"]]
		# this function will eval and match each invalid_ind to its fitness
		evaluate_in_parallel(toolbox.evaluate, invalid_ind, gen)
		if settings.DEBUG:
			for indi in invalid_ind:
				print (indi["fitness"]["values"])
		# discard invalid offspring individual
		for i in range(len(offspring) - 1, -1, -1):
			if not offspring[i]["fitness"]["valid"]:
				print ("### Warning: Invalid Fitness")
				del offspring[i]
		# print ("here1")
		# Update the hall of fame with the generated individuals
		print ("### Updating Hall of Fame ...")
		if halloffame is not None:
			halloffame.update(offspring)

		# assert fitness
		invalid_ind_post = [ind for ind in population + offspring if not ind["fitness"]["valid"]]
		# print ("### assert len(invalid_ind) == 0, len = ", len(invalid_ind_post))
		assert len(invalid_ind_post) == 0

		# Select the next generation population
		population[:] = toolbox.select(population + offspring, mu)

		# Update the statistics with the new population
		record = stats.compile(population) if stats is not None else {}
		logbook.record(gen=gen, nevals=len(invalid_ind), **record)
		if verbose:
			print (logbook.stream)
   
		# in case interrupted
		logbook_file = open(apk_dir + "/intermediate/logbook.pickle", 'wb')
		pickle.dump(logbook, logbook_file)
		logbook_file.close()

	return population, logbook


def varOr(population, toolbox, lambda_, cxpb, mutpb):
	assert (cxpb + mutpb) <= 1.0, ("The sum of the crossover and mutation "
								   "probabilities must be smaller or equal to 1.0.")

	offspring = []
	for _ in range(lambda_):
		op_choice = random.random()
		if op_choice < cxpb:  # Apply crossover
			ind1, ind2 = map(toolbox.clone, random.sample(population, 2))
			# print(ind1)
			# print(ind2)
			ind1, ind2 = toolbox.mate(ind1, ind2)
			del ind1["fitness"]["values"]
			offspring.append(ind1)
		elif op_choice < cxpb + mutpb:  # Apply mutation
			ind = toolbox.clone(random.choice(population))
			ind, = toolbox.mutate(ind)
			del ind["fitness"]["values"]
			offspring.append(ind)
		else:  # Apply reproduction
			offspring.append(random.choice(population))

	return offspring
