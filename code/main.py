from graph import Graph
import networkx as nx
import matplotlib.pyplot as plt
import sys
import getopt
import random
import time

def usage():
    print("Usage: python3 main.py \n\t-t <test more graphs with given solutions: no argument>\n\t-g <generate random graph with N vertices: int>")

if __name__ == "__main__":
    # initialization of random variables
    num_vertices = None
    testing_flag = False

    try:
        opts, args = getopt.getopt(sys.argv[1:], "htg:", ["help", "output="])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(str(err))  # will print something like "option -a not recognized"
        usage()
        sys.exit(2)

    for o, a in opts:
        
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o == "-t":
            testing_flag = True
        elif o == "-g":
            try:
                num_vertices = int(a)
                assert int(a)>1, "Number of vertices bigger than 1"
            except:
                usage()
                sys.exit()

    # Call in random graph generator
    if num_vertices != None:
        # Added in from networkx
        # Time doesnt start here, since this is only for testing purposes
        G=nx.Graph()
        G.add_nodes_from([x for x in range(0, num_vertices)])

        tic = time.time()
        graph = Graph(num_vertices)
        for i in range(0,num_vertices):
            n_iters = random.choice([x for x in range(0,num_vertices)])
            used_vertices = []
            for iteration in range(0, n_iters):
                j = list( set([ x for x in range(num_vertices) if x != i]) - set(used_vertices))
                j = random.choice(j)
                #print("Creating edge: G[%d][%d]" %  (i,j))
                graph.add_edge(i,j)
                G.add_edge(i,j)
                used_vertices.append(j)
        toc = time.time()
        print("Created Graph with %d nodes and %d edges in %.3f ms" % (num_vertices, len(G.edges), 1000*(toc-tic)))
        result = graph.color_matrix()
        # Available functions for visualizing matrixes 

        if testing_flag:
            nx.draw(G, with_labels=True)
            plt.savefig("images/generated_graph.png") # save as png
            plt.show() # display
            sys.exit()

    # Testing mode - OPTARG
    # Test the scenarios we know are working
    else:
        # Graph Creation and definition, by adding edges
        # Test nº 1
        graph = Graph(4)
        graph.add_edge(0,1)
        graph.add_edge(0,2)
        graph.add_edge(1,2)
        graph.add_edge(2,3)

        result = graph.color_matrix()
        print("Chromatic Index calculated correctly? %s\n" % (3==result))

        # Available functions for visualizing matrixes
        print("Analyzing graph:")
        graph.print_adj_matrix()    
        graph.print_colors_matrix()  



        if testing_flag:
            print("\n---------------------------------------------------\nConducting extra tests:\n")
            # Test nº 2
            graph = Graph(5)
            graph.add_edge(0,1)
            graph.add_edge(0,2)
            graph.add_edge(0,3)
            graph.add_edge(0,4)

            graph.add_edge(1,2)
            graph.add_edge(1,4)

            graph.add_edge(2,3)

            graph.add_edge(0,2)

            result = graph.color_matrix()
            print("Chromatic Index calculated correctly? %s\n" % (4==result))

            # Test nº 3
            graph = Graph(3)
            graph.add_edge(0,1)
            graph.add_edge(0,2)
            graph.add_edge(1,2)

            result = graph.color_matrix()
            print("Chromatic Index calculated correctly? %s\n" % (3==result))
