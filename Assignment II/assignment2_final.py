import sys
import math
import time

B = 4

def main():
    """
    def main() will run 
    1. Import data points from Dataset for R-Tree Construction.txt
    2. Construct R-tree
    3. Import 200 range queries from text file 
    4. Run def sequential_scan()
    5. Run query data using R-tree
    """
    
    #Set empty list for storing data points
    points = []

    with open("Dataset for R-Tree Construction.txt", 'r') as dataset: #https://www.w3schools.com/python/ref_file_readlines.asp
        #To iterate over each line from dataset.
        for data in dataset.readlines():
            #Seperate the line into seperate pieces of data (id, x-coordinate, y-coordinate).
            data = data.split() #https://www.w3schools.com/python/ref_string_split.asp
            #Append data point to points list.
            points.append({ #https://www.w3schools.com/python/ref_list_append.asp
                'id': int(data[0]),
                'x': int(data[1]),
                'y': int(data[2])
                   })     

    # build R-Tree
    rtree = RTree()
    print("Building the R-Tree: Please wait...\n")
    
    #To record the start time of construction R-Tree
    R_tree_start=time.time() 
 

    
    for point in points: #insert data points from the root one by one 
        rtree.insert(rtree.root, point) 

    

    #To record the end time of construction R-Tree.
    R_tree_end = time.time() 
    #To find out how long it took to build the R-Tree.
    Used_time= R_tree_end -  R_tree_start
    
    print("R-Tree construction completed\n")
    print("The time-cost of building up the R-Tree is",Used_time,"seconds.\n")


    #Set up empty brackets
    queries=[]
    
    with open("200 Range Queries.txt", 'r') as queries_dataset:
        #To iterate over each line in the queries file.
        for data in queries_dataset.readlines():
            #Split each line into queries list.
            data = data.split()
            #Append querie to queries list.
            queries.append({
                'range': int(data[0]), # set range for each query
                'x1': int(data[1]), #set 'x1' for datapoint
                'x2': int(data[2]), #set 'x2' for datapoint
                'y1': int(data[3]), #set 'y1' for datapoint
                'y2': int(data[4]) #set 'y2' for datapoint
                })
    
    print("The current query is",queries)
    
    
    #To start the sequential-based scan of data points
    print("Sequential-based scan Data Point: Please wait...\n")
    
    #To record the start time of sequential-based scan.
    sequential_based_start = time.time()
    
    #Run a sequential scan on all data points for each query.
    results = sequential_scan(points, queries)
    
    #To record the end time of the sequential-based scan.
    sequential_based_end = time.time()
    
    #To find out how long it took to sequential scan.
    sequential_based_time = sequential_based_end - sequential_based_start
    #Calculate average time taken for sequential-based scan.
    average_sequential_based_time = sequential_based_time / len(queries)

    print("There are",results,"data points included in the query.\n")
    print("Total sequential scan time is", sequential_based_time, "seconds.")
    print("The average sequential scan time is ", average_sequential_based_time, "seconds.")

    #To start querting data using R-tree.
    print("Query data by R-Tree: Please wait...\n")
    
    results = []
    #To record the start time of the R-tree query process.
    Answer_query_start = time.time()
    #To process each query using R-tree
    for query in queries:
        results.append(rtree.query(rtree.root, query))
      #To record the end time of the R-tree query process.  
    Answer_query_end = time.time()
    #To find out how long it took tothe R-tree query process.
    Query_processing_time = Answer_query_end - Answer_query_start
    
    #Calculate average time taken for  R-tree query process.
    average_processing_time = Query_processing_time / len(queries)
    
    #To find how many times the R-tree query process is faster than the sequential-based scan. 
    speed = average_sequential_based_time / average_processing_time

    print ("There are",results,"data points included in the query.\n")
    print ("The R-Tree's processing time is", Query_processing_time,"seconds.")
    print ("The average R-Tree's processing time is", average_processing_time, " seconds.")
    print ("The average R-Tree's processing time is", speed, " times faster than the sequential scan.")

def sequential_scan(points, queries):
    """ Perform a sequential scan of all data points for each query.

    Args:
        points (list): Each data point consists of x and y coordinates
        queries (list): Each query consists of coordinate for a rectangle which are x1, x2, y1, and y2

    Returns:
        list: Produces a list showing the count of data points that fall within each query's range.
    """

    #Set empty list to store number of data points that match each query
    datapoints = []
    #To iterate over each query
    for query in queries:
        
        #To start a counter to keep track of matching points for query 
        num_datapoints = 0
        
        #Set x and y coordinate boundries base on the query
        range_x = range(query['x1'], query['x2']+1) # Using +1 to make the range inclusive for x2 and y2
        range_y = range(query['y1'], query['y2']+1)
        
        #To inspect each point to determine if it lies within the current query's range.
        for point in points:
            if point['x'] in range_x and point['y'] in range_y:
                num_datapoints += 1
        
        #Store the count of matching points in the list.
        datapoints.append(num_datapoints)
    return datapoints
        

class Node(object): #node class
    def __init__(self):
        self.id = 0
        # for internal nodes
        self.child_nodes = []
        # for leaf nodes
        self.data_points = []
        self.parent = None
        self.MBR = {
            'x1': -1,
            'y1': -1,
            'x2': -1,
            'y2': -1,
        }
    def perimeter(self):
        # only calculate the half perimeter here
        return (self.MBR['x2'] - self.MBR['x1']) + (self.MBR['y2'] - self.MBR['y1'])

    def is_overflow(self):
        if self.is_leaf():
            if self.data_points.__len__() > B: #Checking overflows of data points, B is the upper bound.
                return True
            else:
                return False
        else:
            if self.child_nodes.__len__() > B: #Checking overflows of child nodes, B is the upper bound.
                return True
            else:
                return False

    def is_root(self):
        if self.parent is None:
            return True
        else:
            return False

    def is_leaf(self):
        if self.child_nodes.__len__() == 0:
            return True
        else:
            return False

class RTree(object): #R tree class
    def __init__(self):
        self.root = Node() #Create a root

    def query(self, node, query): #run to answer the query
        num = 0
        if node.is_leaf(): #check if a data point is included in a leaf node
            for point in node.data_points:
                if self.is_covered(point, query):
                    num = num + 1
            return num
        else:
            for child in node.child_nodes: #If it is an MBR, check all the child nodes to see whether there is an interaction
                if self.is_intersect(child, query): #If there is an interaction, keep continue to check the child nodes in the next layer till the leaf nodes
                    num = num + self.query(child, query)
            return num

    def is_covered(self, point, query):
        x1, x2, y1, y2 = query['x1'], query['x2'], query['y1'], query['y2']
        if x1 <= point['x'] <= x2 and y1 <= point['y'] <= y2:
            return True
        else:
            return False    

    def is_intersect(self, node, query): #https://stackoverflow.com/questions/9734821/how-to-find-the-center-coordinate-of-rectangle
        # if two mbrs are intersected, then:
        # |center1_x - center2_x| <= length1 / 2 + length2 / 2 and:
        # |center1_y - center2_y| <= width1 / 2 + width2 / 2
        center1_x = (node.MBR['x2'] + node.MBR['x1']) / 2
        center1_y = (node.MBR['y2'] + node.MBR['y1']) / 2
        length1 = node.MBR['x2'] - node.MBR['x1']
        width1 = node.MBR['y2'] - node.MBR['y1']
        center2_x = (query['x2'] + query['x1']) / 2
        center2_y = (query['y2'] + query['y1']) / 2
        length2 = query['x2'] - query['x1']
        width2 = query['y2'] - query['y1'] 
        if abs(center1_x - center2_x) <= length1 / 2 + length2 / 2 and\
                abs(center1_y - center2_y) <= width1 / 2 + width2 / 2:  #we check the absolute value
            return True
        else:
            return False                    


    def insert(self, u, p): # insert p(data point) to u (MBR)
        if u.is_leaf(): 
            self.add_data_point(u, p) #add the data point and update the corresponding MBR
            if u.is_overflow():
                self.handle_overflow(u) #handel overflow for leaf nodes
        else:
            v = self.choose_subtree(u, p) #choose a subtree to insert the data point to miminize the perimeter sum
            self.insert(v, p) #keep continue to check the next layer recursively
            self.update_mbr(v) #update the MBR for inserting the data point

    def choose_subtree(self, u, p): 
        if u.is_leaf(): #find the leaf and insert the data point
            return u
        else:
            min_increase = sys.maxsize #set an initial value
            best_child = None
            for child in u.child_nodes: #check each child to find the best node to insert the point 
                if min_increase > self.peri_increase(child, p):
                    min_increase = self.peri_increase(child, p)
                    best_child = child
            return best_child

    def peri_increase(self, node, p): # calculate the increase of the perimeter after inserting the new data point
        # new perimeter - original perimeter = increase of perimeter
        origin_mbr = node.MBR
        x1, x2, y1, y2 = origin_mbr['x1'], origin_mbr['x2'], origin_mbr['y1'], origin_mbr['y2']
        increase = (max([x1, x2, p['x']]) - min([x1, x2, p['x']]) +
                    max([y1, y2, p['y']]) - min([y1, y2, p['y']])) - node.perimeter()
        return increase


    def handle_overflow(self, u):
        u1, u2 = self.split(u) #u1 u2 are the two splits returned by the function "split"
        # if u is root, create a new root with s1 and s2 as its' children
        if u.is_root():
            new_root = Node()
            self.add_child(new_root, u1)
            self.add_child(new_root, u2)
            self.root = new_root
            self.update_mbr(new_root)
        # if u is not root, delete u, and set s1 and s2 as u's parent's new children
        else:
            w = u.parent
            # copy the information of s1 into u
            w.child_nodes.remove(u)
            self.add_child(w, u1) #link the two splits and update the corresponding MBR
            self.add_child(w, u2)
            if w.is_overflow(): #check the parent node recursively
                self.handle_overflow(w)
            
    def split(self, u):
        # split u into s1 and s2
        best_s1 = Node()
        best_s2 = Node()
        best_perimeter = sys.maxsize
        # u is a leaf node
        if u.is_leaf():
            m = u.data_points.__len__()
            # create two different kinds of divides
            divides = [sorted(u.data_points, key=lambda data_point: data_point['x']),
                       sorted(u.data_points, key=lambda data_point: data_point['y'])] #sorting the points based on X dimension and Y dimension
            for divide in divides:
                for i in range(math.ceil(0.4 * B), m - math.ceil(0.4 * B) + 1): #check the combinations to find a near-optimal one
                    s1 = Node()
                    s1.data_points = divide[0: i]
                    self.update_mbr(s1)
                    s2 = Node()
                    s2.data_points = divide[i: divide.__len__()]
                    self.update_mbr(s2)
                    if best_perimeter > s1.perimeter() + s2.perimeter(): 
                        best_perimeter = s1.perimeter() + s2.perimeter()
                        best_s1 = s1
                        best_s2 = s2

        # u is an internal node
        else:
            # create four different kinds of divides
            m = u.child_nodes.__len__()
            divides = [sorted(u.child_nodes, key=lambda child_node: child_node.MBR['x1']), #sorting based on MBRs
                       sorted(u.child_nodes, key=lambda child_node: child_node.MBR['x2']),
                       sorted(u.child_nodes, key=lambda child_node: child_node.MBR['y1']),
                       sorted(u.child_nodes, key=lambda child_node: child_node.MBR['y2'])]
            for divide in divides:
                for i in range(math.ceil(0.4 * B), m - math.ceil(0.4 * B) + 1): #check the combinations
                    s1 = Node()
                    s1.child_nodes = divide[0: i]
                    self.update_mbr(s1)
                    s2 = Node()
                    s2.child_nodes = divide[i: divide.__len__()]
                    self.update_mbr(s2)
                    if best_perimeter > s1.perimeter() + s2.perimeter():
                        best_perimeter = s1.perimeter() + s2.perimeter()
                        best_s1 = s1
                        best_s2 = s2

        for child in best_s1.child_nodes:
            child.parent = best_s1
        for child in best_s2.child_nodes:
            child.parent = best_s2

        return best_s1, best_s2


    def add_child(self, node, child):
        node.child_nodes.append(child) #add child nodes to the current parent (node) and update the MBRs. It is used in handeling overflows
        child.parent = node
        if child.MBR['x1'] < node.MBR['x1']:
            node.MBR['x1'] = child.MBR['x1']
        if child.MBR['x2'] > node.MBR['x2']:
            node.MBR['x2'] = child.MBR['x2']
        if child.MBR['y1'] < node.MBR['y1']:
            node.MBR['y1'] = child.MBR['y1']
        if child.MBR['y2'] > node.MBR['y2']:
            node.MBR['y2'] = child.MBR['y2']
    # return the child whose MBR requires the minimum increase in perimeter to cover p

    def add_data_point(self, node, data_point): #add data points and update the the MBRS
        node.data_points.append(data_point)
        if data_point['x'] < node.MBR['x1']:
            node.MBR['x1'] = data_point['x']
        if data_point['x'] > node.MBR['x2']:
            node.MBR['x2'] = data_point['x']
        if data_point['y'] < node.MBR['y1']:
            node.MBR['y1'] = data_point['y']
        if data_point['y'] > node.MBR['y2']:
            node.MBR['y2'] = data_point['y']


    def update_mbr(self, node): #update MBRs when forming a new MBR. It is used in checking the combinations and update the root
        x_list = []
        y_list = []
        if node.is_leaf():
            x_list = [point['x'] for point in node.data_points]
            y_list = [point['y'] for point in node.data_points]
        else:
            x_list = [child.MBR['x1'] for child in node.child_nodes] + [child.MBR['x2'] for child in node.child_nodes]
            y_list = [child.MBR['y1'] for child in node.child_nodes] + [child.MBR['y2'] for child in node.child_nodes]
        new_mbr = {
            'x1': min(x_list),
            'x2': max(x_list),
            'y1': min(y_list),
            'y2': max(y_list)
        }
        node.MBR = new_mbr


if __name__ == '__main__':
    main()
