import sys
import time
class Graph:
    def __init__(self, num_vertices):
        # Initialize array and declare num_vertices
        self.num_vertices = num_vertices
        self.adjecency_matrix = [0] * num_vertices
        self.colors_matrix = [0] * num_vertices
        self.cromatic_index = 0
        self.basic_operations = 0
        # maximum colors is always (num_vertices-1) factorial

        # Initialize matrix
        for i in range(0, num_vertices):
            self.adjecency_matrix[i] = [0] * num_vertices
            self.colors_matrix[i] = [0] * num_vertices

    def add_edge(self, e1 , e2):
        self.adjecency_matrix[e1][e2] = 1
        self.adjecency_matrix[e2][e1] = 1 # graphs are undirected

    def color_matrix(self):
        # we iterate every vertice by ascending order
        # this doesnt result in the least amount of colors possible, but this is NP-Complete
        # this way we only iterate the top side of the matrix
        tic = time.time()
        for row_id in range(0,self.num_vertices):
            # used colors for each vertice
            used_colors = []
            available_colors = [x for x in range(1, self.num_vertices+1)]

            for column_id in range(0,self.num_vertices):
                # diagonal values of matrix
                if row_id == column_id or self.adjecency_matrix[row_id][column_id] == 0:
                    continue

                curr_value = self.colors_matrix[row_id][column_id]

                # first iteration and available values
                if curr_value == 0 and row_id == 0:
                    # we get the color 1 if there's no used color, otherwise we get color + 1, which is the next color
                    color = min( list( set(available_colors) - set(used_colors)))
                    self.basic_operations += 1 # since this is the most costy operation, we count it as a basic operation

                    # then we fill the matrix with the color
                    self.colors_matrix[row_id][column_id] = color
                    self.colors_matrix[column_id][row_id] = color
                    used_colors.append(color)

                elif curr_value == 0:
                    # used_colors = used_colors + neighbours_used_colors
                    neighbour_colors = list(set(self.colors_matrix[row_id]) | set(self.colors_matrix[column_id]))   # these are temp   
                    #print("Analyzing G[%d][%d]" % (row_id, column_id))
                    #print("Neighbours_colors: ", neighbour_colors)

                    # Since these neighbour colors are temporary for the edge we are looking at, we cant add them to the used colors. Since these used colors are ones we used on this vertice
                    tmp_colors = list( set(available_colors) - set(used_colors) - set(neighbour_colors))
                    color = max(available_colors + used_colors + neighbour_colors)+1 if len(tmp_colors) == 0 else min(tmp_colors)
                    self.basic_operations += 1 # since this is the most costy operation, we count it as a basic operation

                    # then we fill the matrix with the color
                    self.colors_matrix[row_id][column_id] = color
                    self.colors_matrix[column_id][row_id] = color
                    used_colors.append(color)
                
                # at the end of each array we verify if the cromatic index is bigger, so we dont have to iterate over the array later
                if color > self.cromatic_index:
                    self.cromatic_index = color
        toc = time.time()
        print("Cromatic index for given graph is: %d\n\nTime elapsed for coloring: %.3f ms\nNumber of basic operations: %d" % (self.cromatic_index, 1000*(toc-tic), self.basic_operations))
        return self.cromatic_index

                
    def get_max(self, list1):
        for i in list1:
            if type(i)==list:
                get_max(i)
            else:
                    list2.append(i)
        return max(list2)

    def print_colors_matrix(self):
        print("Colors Matrix: ", self.colors_matrix)


    # Print matrix for debugging purposes
    def print_adj_matrix(self):
        print("Adjacency Matrix: ",self.adjecency_matrix)
