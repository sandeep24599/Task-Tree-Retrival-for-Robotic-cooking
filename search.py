import pickle
import json
from FOON_class import FunctionalUnit, Object

# -----------------------------------------------------------------------------------------------------------------------------#

# Checks an ingredient exists in kitchen

def check_if_exist_in_kitchen(kitchen_items, ingredient):
    """
        parameters: a list of all kitchen items,
                    an ingredient to be searched in the kitchen
        returns: True if ingredient exists in the kitchen
    """

    for item in kitchen_items:
        if item["label"] == ingredient.label \
                and sorted(item["states"]) == sorted(ingredient.states) \
                and sorted(item["ingredients"]) == sorted(ingredient.ingredients) \
                and item["container"] == ingredient.container:
            return True

    return False


#--------------------------------------------------------------------------------------------------------------------#

# Traversing functional units having maximum success probability of motion

def search_heuristic_1(kitchen_items=[], goal_node=None):
    # list of indices of functional units
    reference_task_tree = []

    # list of object indices that need to be searched
    items_to_search = []

    # find the index of the goal node in object node list 
    items_to_search.append(goal_node.id)

    # list of item already explored
    items_already_searched = []

    while len(items_to_search) > 0:
        current_item_index = items_to_search.pop(0)  # pop the first element
        if current_item_index in items_already_searched:
            continue
        else:
            items_already_searched.append(current_item_index)

        current_item = foon_object_nodes[current_item_index]

        if not check_if_exist_in_kitchen(kitchen_items, current_item):

            candidate_units = foon_object_to_FU_map[current_item_index]

            # Adding each functional unit motion probability to dictionary as values 
            # Finding fu unit with greatest motion probability  
            heuristic={}
            maxi = -1
            keyRet = -1

            for i in candidate_units:
                heuristic[i]=foon_functional_units[i].motion_node
                if (motions[heuristic[i]] > maxi):
                    maxi = motions[heuristic[i]]
                    keyRet = i
               
            selected_candidate_idx=keyRet
            # if an fu is already taken, do not process it again
            if selected_candidate_idx in reference_task_tree:
                continue
            else:
                reference_task_tree.append(selected_candidate_idx)

            # all input of the selected FU need to be explored
            for node in foon_functional_units[selected_candidate_idx].input_nodes:
                node_idx = node.id
                if node_idx not in items_to_search:

                    # if in the input nodes, we have bowl contains {onion} and onion, chopped, in [bowl]
                    # explore only onion, chopped, in bowl
                    flag = True
                    if node.label in utensils and len(node.ingredients) == 1:
                        for node2 in foon_functional_units[selected_candidate_idx].input_nodes:
                            if node2.label == node.ingredients[0] and node2.container == node.label:

                                flag = False
                                break
                    if flag:
                        items_to_search.append(node_idx)

    # reverse the task tree
    reference_task_tree.reverse()

    # create a list of functional unit from the indices of reference_task_tree
    task_tree_units = []
    for i in reference_task_tree:
        task_tree_units.append(foon_functional_units[i])

    return task_tree_units

#---------------------------------------------------------------------------------------------------------------------------#

#Traversing fu based on the minimum number of input nodes considering respective ingredients

def search_heuristic_2(kitchen_items=[], goal_node=None):
    # list of indices of functional units
    reference_task_tree = []

    # list of object indices that need to be searched
    items_to_search = []

    # find the index of the goal node in object node list 
    items_to_search.append(goal_node.id)

    # list of item already explored
    items_already_searched = []

    while len(items_to_search) > 0:
        current_item_index = items_to_search.pop(0)  # pop the first element
        if current_item_index in items_already_searched:
            continue

        else:
            items_already_searched.append(current_item_index)

        current_item = foon_object_nodes[current_item_index]

        if not check_if_exist_in_kitchen(kitchen_items, current_item):

            candidate_units = foon_object_to_FU_map[current_item_index]

            # Counting the number of input_nodes,ingredients of a functional unit
            heuristic={}
            for i in candidate_units:
                heuristic[i]=len(foon_functional_units[i].input_nodes)
                for object in foon_functional_units[i].input_nodes:
                    #Checking each input nodes for ingredients and adding their count
                    heuristic[i]+=( len(object.ingredients)-1 if (len(object.ingredients) > 0)
                                             else len(object.ingredients))
            
            # Finding the functional unit with minimum no of inputs nodes
            min_input_nodes=min(heuristic.values())
            for key, value in heuristic.items():
                # comparing input nodes + ingredients with minimum for all the fu's
                 if value == min_input_nodes:  
                    selected_candidate_idx=key
                    break

            # if an fu is already taken, do not process it again
            if selected_candidate_idx in reference_task_tree:
                continue
            else:
                reference_task_tree.append(selected_candidate_idx)

            # all input of the selected FU need to be explored
            for node in foon_functional_units[selected_candidate_idx].input_nodes:
                node_idx = node.id
                if node_idx not in items_to_search:

                    # if in the input nodes, we have bowl contains {onion} and onion, chopped, in [bowl]
                    # explore only onion, chopped, in bowl
                    flag = True
                    if node.label in utensils and len(node.ingredients) == 1:
                        for node2 in foon_functional_units[selected_candidate_idx].input_nodes:
                            if node2.label == node.ingredients[0] and node2.container == node.label:

                                flag = False
                                break
                    if flag:
                        items_to_search.append(node_idx)

    # reverse the task tree
    reference_task_tree.reverse()

    # create a list of functional unit from the indices of reference_task_tree
    task_tree_units = []
    for i in reference_task_tree:
        task_tree_units.append(foon_functional_units[i])

    return task_tree_units

#---------------------------------------------------------------------------------------------------------------#

# Traversing functional units with bound depth by increasing depth level until getting the task
def search_IDDFS( kitchen_items=[],goal_node=None, Depth=None,reference_task_tree=[],items_already_searched=[]):
    #reference_task_tree=[]

    # list of indices of functional units
    iddfs_reference_task_tree = []
    # Checking Leaf nodes at lowest depth present in kitchen
    # appending True to fl if they are in kitchen else False
    if Depth == 0:  
        if check_if_exist_in_kitchen(kitchen_items, goal_node) :
            fl.append(True)        
        else:
            fl.append(False)

    if Depth>0:
        # list of object indices that need to be searched
        items_to_search = []

        # find the index of the goal node in object node list
        items_to_search.append(goal_node.id)

        # list of item already explored
        #items_already_searched = []
        current_item_index = items_to_search.pop(0)  # pop the first element
        if current_item_index in items_already_searched:
            pass

        else:
            items_already_searched.append(current_item_index)

            current_item = foon_object_nodes[current_item_index]

            if not check_if_exist_in_kitchen(kitchen_items, current_item):

                candidate_units = foon_object_to_FU_map[current_item_index]
                # selecting the first path
                selected_candidate_idx = candidate_units[0]

                # if an fu is already taken, do not process it again
                if selected_candidate_idx in reference_task_tree:
                    pass

                else:
                    reference_task_tree.append(selected_candidate_idx)
                    # all input of the selected FU need to be explored 
                            

                    for node in foon_functional_units[
                            selected_candidate_idx].input_nodes:
                        node_idx = node.id
                        if node_idx not in items_to_search:

                            # if in the input nodes, we have bowl contains {onion} and onion, chopped, in [bowl]
                            # explore only onion, chopped, in bowl
                            flag = True
                            if node.label in utensils and len(node.ingredients) == 1:
                                for node2 in foon_functional_units[
                                        selected_candidate_idx].input_nodes:
                                    if node2.label == node.ingredients[
                                            0] and node2.container == node.label:

                                        flag = False
                                        break
                        if flag is True:   

                            # Traversing the depth bound by making depth=depth-1                    
                            iddfs_reference_task_tree.extend(search_IDDFS(kitchen_items, node, 
                                    Depth-1,reference_task_tree,items_already_searched))
                    iddfs_reference_task_tree.append(selected_candidate_idx)

    # return the task tree
    return iddfs_reference_task_tree
#------------------------------------------------------------------------------------------------------------#

def output(reference_task_tree):
    #reference_task_tree.reverse()

    # create a list of functional unit from the indices of reference_task_tree
    task_tree_units = []
    for i in reference_task_tree:
        task_tree_units.append(foon_functional_units[i])

    return task_tree_units


#----------------------------------------------------------------------------------------------------------------------------#

def save_paths_to_file(task_tree, path):

    print('writing generated task tree to ', path)
    _file = open(path, 'w')

    _file.write('//\n')
    for FU in task_tree:
        _file.write(FU.get_FU_as_text() + "\n")
    _file.close()


# -----------------------------------------------------------------------------------------------------------------------------#

# creates the graph using adjacency list
# each object has a list of functional list where it is an output


def read_universal_foon(filepath='FOON.pkl'):
    """
        parameters: path of universal foon (pickle file)
        returns: a map. key = object, value = list of functional units
    """
    pickle_data = pickle.load(open(filepath, 'rb'))
    functional_units = pickle_data["functional_units"]
    object_nodes = pickle_data["object_nodes"]
    object_to_FU_map = pickle_data["object_to_FU_map"]

    return functional_units, object_nodes, object_to_FU_map


# ------------------------------------------------------------------------------------------------------------------------#

if __name__ == '__main__':
    foon_functional_units, foon_object_nodes, foon_object_to_FU_map = read_universal_foon(
    )
    fl=[]  # creating an empty list to track all the leaf nodes
    utensils = []
    """ creating a dictionary with 
     motion labels and their respective success rates as key value paires"""
    motions={} 
    with open("motion.txt",'r') as p:
        for line in p:
            if line=="\n":
                break
            else:
                (key,value)=line.split("\t")
                motions[key]=float(value.strip("\n"))
    with open('utensils.txt', 'r') as f:
        for line in f:
            utensils.append(line.rstrip())

    kitchen_items = json.load(open('kitchen.json'))

    goal_nodes = json.load(open("goal_nodes.json"))
    for node in goal_nodes:
        node_object = Object(node["label"])
        node_object.states = node["states"]
        node_object.ingredients = node["ingredients"]
        node_object.container = node["container"]
        for object in foon_object_nodes:
            if object.check_object_equal(node_object):
                output_task_tree = search_heuristic_1(kitchen_items, object)
                save_paths_to_file(output_task_tree,
                                   'output_Heuristic1_{}.txt'.format(node["label"]))
                output_task_tree = search_heuristic_2(kitchen_items, object)
                save_paths_to_file(output_task_tree,
                                   'output_Heuristic2_{}.txt'.format(node["label"]))
                depth=1      # Initially assuming depth as one
                while depth :
                    task_tree=(search_IDDFS(kitchen_items, object,depth,[],[]))
                    flagg=all(i for i in fl) #flagg is one if the leaf nodes are in the kitchen
                    fl.clear()
                    depth+=1   #Increasing the depth level if solution is not found
                    if flagg is True: # printing the task tree when the solution is found
                        output_task_tree=output(task_tree)
                        save_paths_to_file(output_task_tree,
                                    'output_IDDFS_{}.txt'.format(node["label"]))
                        break
                    task_tree.clear()

                break
        else:
            print("The goal node does not exist") # Printing if a goal node not in the Foon