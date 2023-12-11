from TSPAlgorithms import *
import tsplib95
import time
import csv


def main():
    instances = [
        ['eil51', 51, 426],
        ['berlin52', 52, 7542],
        ['st70', 70, 675],
        ['eil76', 76, 538],
        ['pr76', 76, 108159],
        ['rat99', 99, 1211],
        ['kroA100', 100, 21282],
        ['kroB100', 100, 22141],
        ['kroC100', 100, 20749],
        ['kroD100', 100, 21294],
        ['kroE100', 100, 22068],
        ['rd100', 100, 7910],
        ['eil101', 101, 629],
        ['lin105', 105, 14379],
        ['pr107', 107, 44303],
        ['pr124', 124, 59030],
        ['bier127', 127, 118282],
        ['ch130', 130, 6110],
        ['pr136', 136, 96772],
        ['pr144', 144, 58537],
    ]
    with open('resultados.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=' ',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(["Instance", "Algorithm", "Nodes", "Limiar", "Cost", "Time"])

        for instance, num_nodes, limiar in instances:
            problem = tsplib95.load('datasets/' + instance + '.tsp')
            G = problem.get_graph()
            tsp = TSP(G)
            start_time1 = time.time()
            sol1 = tsp.twice_around_the_three()
            t1 = time.time() - start_time1
            start_time2 = time.time()
            sol2 = tsp.christofides_algorithm()
            t2 = time.time() - start_time2
            #start_time3 = time.time()
            #sol3 = tsp.branch_and_bound()
            #t3 = time.time() - start_time3

            spamwriter.writerow([str(instance), 'TAT', str(num_nodes), str(limiar), str(sol1[1]), str(round(t1, 4))])
            spamwriter.writerow([str(instance), 'CHR', str(num_nodes), str(limiar), str(sol2[1]), str(round(t2, 4))])
            spamwriter.writerow([str(instance), 'BAB', str(num_nodes), str(limiar), '-', 'NA'])

main()
