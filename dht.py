class Node():
    def __init__(self, name, value):
        self.name = name
        self.value = value
        self.head = None
        self.tail = None
        self.data = {}
    
    def put(self, k, v):
        self.data[k] = v
        
    def get(self, k):
        return self.data[k]

def leave(leaving_node):
    """a node can leave the dht.
    
    leaving a dht means: (1) updating its successor and
    predecessor and (2) reallocating its data, if it 
    exists.
    """
    # get its data first
    temp_data = leaving_node.data

    # fetch its successor
    successor_node = leaving_node.tail

    # remove it from dht by updating its successor and predecessor
    _remove_node(leaving_node)

    # if necessary, reinject data through successor
    if temp_data:
        for k in temp_data.keys():
            put(successor_node, k, temp_data[k])
            
def join(entry_node, new_node):
    """
    a node joins a dht through an entry node.
    """
    
    # identify the appropriate successor for the new node
    successor_node = _find_successor(entry_node, new_node)
    
    # join dht by updating successor and predecessor
    _add_node(successor_node, new_node)
    
    # reallocate successor data if necessary
    successors_data = successor_node.data
    if successors_data:
    
        # reset successor's database since we'll reinject data into dht
        successor_node.data = {}

        # reinject data into dht through new node
        for k in successors_data.keys():
            put(new_node, k, successors_data[k])
    
def _add_node(successor_node, new_node):
    """insert node between successor and precedessor.
    """
    # get predecessor
    predecessor_node = successor_node.head
    
    # update predecessor
    predecessor_node.tail = new_node

    # insert new node
    new_node.head = predecessor_node
    new_node.tail = successor_node
    
    # update successor
    successor_node.head = new_node


def _remove_node(leaving_node):
    """remove node by annealing its successor and predecessor.
    """
    predecessor_node = leaving_node.head
    successor_node = leaving_node.tail
    
    # update predecessor's tail
    predecessor_node.tail = successor_node
    
    # update successor's head
    successor_node.head = predecessor_node
    print(">> removed {}".format(leaving_node.name))
    

def put(entry_node, k, v):
    """store k, v in dht.
    """
    
    # generate temp node because _find_successor uses node objects
    temp_node = Node("temp", k)

    # find successor, which will hold data
    successor_node = _find_successor(entry_node, temp_node)
    successor_node.put(k, v)


def get(entry_node, k):
    """retrieve v from dht with k.
    """
    # generate temp node
    temp_node = Node("temp", k)

    # find successor, which holds data
    successor_node = _find_successor(entry_node, temp_node)

    # then fetch value from successor 
    return successor_node.get(k)


    
def _find_successor(curr, new):
    """recursively identify successor node, given new node.
    """
    
    # scenario 1: edge case, wrap around
    if (new.value > curr.value) and (curr.tail.value < curr.value):
        return curr.tail
    
    # scenario 2: normal case, predecessor -> new node -> successor
    elif (new.value > curr.value) & (curr.tail.value >= new.value):
        return curr.tail
    
    elif (new.value < curr.tail.value) and (new.value < curr.value) and (curr.value > curr.tail.value):
        return curr.tail

    # keep traversing until we find base case
    else:
        return _find_successor(curr.tail, new)
    
def inspect(entry_node):
    """print dht.
    """
    start = entry_node
    
    while entry_node.tail.value != start.value:
        print(entry_node.name, entry_node.value, entry_node.data)
        entry_node = entry_node.tail
    print(entry_node.name, entry_node.value, entry_node.data)