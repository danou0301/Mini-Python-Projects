#############################################################
# FILE : ex10.py
# WRITERS : Dan Boujenah , danou0301 , 341339901
# EXERCISE : intro2cs ex10 2017-2018
# DESCRIPTION : Decision Tree, Find illness
#############################################################
from collections import Counter
import itertools

MOST_COMMON_ILLNESS = 1
START_LEVEL = 1
START_SYMPTOM = 0


class Node:
    """This class represent a node in the tree, every node have a positive
    and negative child corresponding of a Yes or No answer (if a person have
     or don't have a certain symptom)
    or None of them, it's a leaf (illness)"""

    def __init__(self, data="", pos=None, neg=None):
        """initialize the node with no data and no positive or negative
        child"""
        self.data = data
        self.positive_child = pos
        self.negative_child = neg


class Record:
    """This class represent a record, each record have illness and symptoms"""
    def __init__(self, illness, symptoms):
        self.illness = illness
        self.symptoms = symptoms


def parse_data(filepath):#Use this to replace the parse data function in the original file.
    """

    :param filepath:A string type,designates a file destination
    on the system.
    :return:
    """
    with open(filepath) as data_file:
        records = []
        symptoms = []
        for line in data_file:
            words = line.split()
            records.append(Record(words[0], words[1:]))
            for word in words[1:]:
                if word not in symptoms:
                    symptoms.append(word)
        return records,symptoms


class Diagnoser:
    """This class contain several functions that help to diagnose"""

    def __init__(self, root):
        """This class take root of a decision tree as parameter"""
        self.__root = root

    def most_common_illness_test(self, records, symptoms):
        commonnality_record = {}
        most_common = None
        for record in records:
            good_for_use = True
            for symptom in symptoms:
                if symptom not in record.symptoms:
                    good_for_use = False
                    break
            if good_for_use:
                diagnosis = self.diagnose(record.symptoms)
                if diagnosis not in commonnality_record:
                    commonnality_record[diagnosis] = 1
                else:
                    commonnality_record[diagnosis] += 1
        max = 0
        print(commonnality_record)
        for diagnosis in commonnality_record:
            if commonnality_record[diagnosis] > max:
                max = commonnality_record[diagnosis]
                most_common = diagnosis
        return most_common

    def get_root(self):
        return self.__root

    def diagnose(self, symptoms):
        """This function takes symptoms and return the illness thanks to a
        decision tree"""

        def check_symptom(node):
            """Recursive function that check on every node if the patient have
             this symptom and return the illness which corresponds to these
             symptoms """

            if not node.positive_child:
                # if it don't have child return the data who are a illness
                return node.data
            else:
                if node.data in symptoms:
                    # continue on the tree with a positive answer
                    return check_symptom(node.positive_child)
                else:
                    # continue on the tree with a negative answer
                    return check_symptom(node.negative_child)

        # then return the value of a check_symptom() function
        return check_symptom(self.__root)

    def calculate_error_rate(self, records):
        """This function find the ratio of good diagnose with decision tree
         and records"""
        diagnose_error = 0
        for record in records:
            if record.illness != self.diagnose(record.symptoms):
                diagnose_error += 1
        return diagnose_error / len(records)

    def all_illnesses(self):
        """Find all illnesses in a certain decision tree"""

        def all_illnesses_helper(node, all_illnesses_list):
            """This is a recursive function that append to a list all
            illnesses of a decision tree"""
            if not node.positive_child:
                # check if the illness already in the list
                if node.data not in all_illnesses_list:
                    all_illnesses_list.append(node.data)
            else:
                # continue on the tree with positive and negative answers
                all_illnesses_helper(node.positive_child, all_illnesses_list)
                all_illnesses_helper(node.negative_child, all_illnesses_list)
            return sorted(all_illnesses_list)

        return all_illnesses_helper(self.__root, [])

    def most_common_illness(self, records):
        """This function find the most common illness that we diagnose with
         a function diagnose on every list of record"""
        all_illness = []
        for record in records:

            all_illness.append(self.diagnose(record.symptoms))

        count_illness = Counter(all_illness)
        return count_illness.most_common(MOST_COMMON_ILLNESS)[0][0]

    def paths_to_illness(self, illness):
        """Find all paths on a decision tree to a definite illness"""

        def paths_to_illness_helper(node, path, all_paths):
            """This is a recursive function that create a list of paths to
             a illness"""

            if not node.positive_child:
                # check if the leaf correspond to our illness
                if illness == node.data:
                    all_paths.append(path)

            else:
                # continue on the tree and update the path
                paths_to_illness_helper(node.positive_child, path + [True],
                                        all_paths)
                paths_to_illness_helper(node.negative_child, path + [False],
                                        all_paths)

            return all_paths

        return paths_to_illness_helper(self.__root, [], [])


def build_tree(records, symptoms):
    """This function build a tree, every node with child correspond to a
    symptom of a symptoms list and every leaf correspond to a most common
    illness on the record with these symptoms"""

    def find_illness(my_symptoms):
        """This function return the most common illness on the record with a
        certain list of symptoms"""

        illnesses = []
        for record in records:

            symptoms_not_tested = set(record.symptoms).difference(symptoms)
            # add to our symptoms list the symptom on the record we doesn't
            # check
            if set(record.symptoms) == \
                    set(my_symptoms).union(symptoms_not_tested):

                illnesses.append(record.illness)

        if illnesses:
            count_illness = Counter(illnesses)
            return count_illness.most_common(MOST_COMMON_ILLNESS)[0][0]
        else:
            # if no one illness corresponding return the first illness on the
            # record list
            return records[0].illness

    def build_tree_helper(node, len_root, list_symptoms_true):
        """This is a recursive function that create a node on every recursion
         until the last symptom's node then add the illness
         And create a list of symptoms that the patient have on every leaf"""

        if len_root < len(symptoms):

            node.positive_child = Node(symptoms[len_root])
            node.negative_child = Node(symptoms[len_root])

            build_tree_helper(node.positive_child, len_root+1,
                              list_symptoms_true + [node.data])
            build_tree_helper(node.negative_child, len_root+1,
                              list_symptoms_true)

        else:
            # add the illness thanks to find illness function
            node.positive_child = Node(find_illness(list_symptoms_true +
                                                    [node.data]))
            node.negative_child = Node(find_illness(list_symptoms_true))
    # create the root with the first symptom to check
    tree_root = Node(symptoms[START_SYMPTOM])
    build_tree_helper(tree_root, START_LEVEL, [])
    return tree_root


def optimal_tree(records, symptoms, depth):
    """This function take a list of symptoms, records and depth (number of
    symptom that we have to return)
    And return a list of symptoms that we have to take in order to
    have a minimum error rate"""

    trees_count = dict()
    # check for all subset combination of symptoms
    for subset in itertools.combinations(symptoms, depth):

        tree = build_tree(records, list(subset))  # build tree
        # find error rate and append to a dict
        error_rate = Diagnoser(tree).calculate_error_rate(records)
        trees_count[Diagnoser(tree).get_root()] = error_rate

    # return the root with the minimal error rate
    return min(trees_count, key=trees_count.get)


records = parse_data("big_data.txt")[0]
symptoms = parse_data("big_data.txt")[1]
root = optimal_tree(records,symptoms,len(symptoms))
diagnoser = Diagnoser(root)
error_counter = 0
all_error_counter = 0
for record in records:
    diagnosis = diagnoser.diagnose(record.symptoms)
    if record.illness != diagnosis and  diagnosis != diagnoser.most_common_illness_test(records,record.symptoms):
        error_counter += 1
print(error_counter)