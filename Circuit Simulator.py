# BY : MARIO MEDHAT
# GITHUB REPOSITORY LINK : https://github.com/MarioMedhat/Basic-Circuit-Simulator

# first we have to import the libraries
# we are going to need in our work

from sympy import *

# define some global variables,
# these are lists that could be used
# by many functions, they are a list of
# components which contains the data of
# every component in the netlist, and
# the other on is the node list and it
# contains every node in the netlist
comp_list = []
nodes_list = []


class Comp:
    # then we have to define a class for the
    # components, and this is better than using
    # an array for every component, as it could
    # cause some problems in adding any new
    # parameters to our components, and in the
    # usage there could happen some mistakes
    # in index matching between the parameters arrays,
    # so its better to use a dynamic allocation
    # and a linked list

    # and this is clear in using the append()
    # instruction as it helps in index matching
    # problems and also do not consume redundant
    # memory or gives a redundant maximum number
    # of components as in normal arrays

    # then we have to define the
    # initialization function of the class
    def __init__(self, name, value, np, nn):

        # define the kind of the component
        # describing if it is a resistor,
        # capacitor, source, etc
        self.kind = name[0]

        # define the name of the component
        # entered by the user in the netlist
        self.name = name

        # define the symbol of the component
        # it could be used later, in more complicated
        # symbolic calculations, but here
        # in this code it is not used
        self.sym = symbols(name)

        # define the value of the component
        self.value = 0

        # and it needs some work as the user
        # can write in the netlist "9K" for "9000"
        # so we have to make this conversion
        # we are going to check if the last character
        # in the value string is a term for power
        # like "K", "M" etc or "e*3", etc and then
        # multiply the number before it to the 10^...
        if value.endswith('K'):
            self.value = float(value[:-1])*10**3
        elif value.endswith('MEG'):
            self.value = float(value[:-1])*10**6
        elif value.endswith('G'):
            self.value = float(value[:-1])*10**9
        elif value.endswith('M'):
            self.value = float(value[:-1])*10**-3
        elif value.endswith('U'):
            self.value = float(value[:-1])*10**-6
        elif value.endswith('N'):
            self.value = float(value[:-1])*10**-9
        elif value.endswith('P'):
            self.value = float(value[:-1])*10**-12

        # this case is a little bit confusing as
        # our handling will deffer if the user entered
        # a numerical value then "E..." or if
        # only the component va;ue is "E...",
        # so first we do this check and then
        # multiply the numerical value by
        # 10^..." or  save it equal to 10^..."
        elif value.find('E') != -1:
            if value.index('E') != 0:

                # if there is a numerical value before "E...",
                # multiply the numerical value by from the start
                # to the character before "E",
                # by 10^ the rest of the string
                self.value = float(value[:value.index('E')])*10**float(value[value.index('E')+1:])

            else:

                # if there is no numerical value before "E...",
                # then save the value of 10^...
                # after the "E" character
                self.value = 10**float(value[1:])

        # if there is no term for power,
        # then copy the value string as it is
        else:
            self.value = float(value)

        # define the positive node of the component
        self.np = np
        # define the negative node of the component
        self.nn = nn


def parse(path):
    # then we must have a function that takes
    # the address of the netlist and then
    # extracts the data of the circuit from it
    # so the parameter that this function takes
    # as input is the path of the netlist

    # open the circuit netlist
    # "r", means that we are going
    # to read only the file
    circuit_file = open(path, "r")

    # create a list containing each
    # line of the netlist file
    lines = circuit_file.readlines()

    # close the file as we do not need
    # it now, this step is very important
    # as opening the file without closing
    # it will cause some errors during
    # editing the netlist of while opening
    # it with other programs
    circuit_file.close()

    # start parsing, by doing some
    # processes on each singe line
    for line in lines:

        # first strip the line on whitespaces,
        # which means to delete the redundant
        # empty lines caused by "\n" at
        # the end of each line in the netlist
        line = line.strip().upper()

        # then if the text file itself
        # contains blank lines we have to ignore them
        if line == "":

            continue

        # then in we find a comment key "*"
        if line.find("*") != -1:

            # then skip this iteration
            continue

        # then in we find a command key ".",
        elif line.startswith("."):
            # then skip the iteration for now
            continue

        # else the line must be a component definition
        else:

            # first strip the line on whitespaces,
            # which means to make like an array of
            # string and every element is a word
            # separated by the other one with a white
            # space, and the convert all of them
            # to the upper case as to make easier
            # while handling every thing in the netlist
            m_line = line.split()

            # then create a new component instance
            # in the linked list called comp_list,
            # and then assign to it all the parameters
            comp_list.append(Comp(m_line[0].upper(), m_line[3], m_line[1].upper(), m_line[2].upper()))


def compute_circuit():
    # then we must have a function
    # that arranges the matrices

    # we must define a counter that contains
    # the number of nodes (except the ground node)
    # and voltages sources, and this is the
    # length of the rows and columns in the
    # G_matrix and the other ones
    counter = 0

    # first we add to the node list a zero,
    # which is the ground node only to have
    # a size for the list larger than 0 to
    # be able to start making iterations and
    # we are not going to increment the counter
    # by 1 here
    nodes_list.append(str(0))

    # then we start reading every component
    # in the component list
    for inst_comp in comp_list:

        # check if there is a new node,
        # which is not in the node list
        if inst_comp.np not in nodes_list:

            # then add a new element to the list with the same name of the node
            nodes_list.append(str(inst_comp.np))

            # increase the counter value by 1
            counter = counter + 1

        # check if there is a new node,
        # which is not in the node list
        if inst_comp.nn not in nodes_list:

            # then add a new element to the list with the same name of the node
            nodes_list.append(str(inst_comp.nn))

            # increase the counter value by 1
            counter = counter + 1

        # check if there is a voltage source
        if inst_comp.kind == 'V':

            # increase the counter value by 1
            counter = counter + 1

    # then we have to start defining our matrices
    # the first one is the Y matrix,
    # which is a square matrix with
    # the size of the number of nodes
    # an voltages sources in the circuit
    y_matrix = [['0' for row in range(0, counter)] for col in range(0, counter)]

    # then the second and third ones are the
    # V and J matrix nad they are
    # column matrices with the size of the
    # number of nodes an voltages sources in
    # the circuit
    v_matrix = ['0' for row in range(0, counter)]
    j_matrix = ['0' for row in range(0, counter)]

    # then we need to define a counter
    # that contains the index of the
    # node or the voltage sources we
    # are working in
    node_num = 0

    # then we have to start iterating
    # on every node in the node list,
    # but we skip the first one as it
    # is the zero or ground node and
    # it has no presence in the matrices
    for node in nodes_list[1:]:

        # then we have to add each node
        # to the V matrix list
        v_matrix[node_num] = node

        # then increment the node counter by 1
        node_num = node_num + 1

    # then we have to start iterating
    # on every component in the component list
    for inst_comp in comp_list:

        # if the component is a voltage source
        if inst_comp.kind == 'V':

            # then we have to add each
            # voltage source to the V matrix list
            # as it represents the current passing
            # threw this voltage source
            v_matrix[node_num] = inst_comp.name

            # then we have to add each
            # voltage source to the J matrix list
            j_matrix[node_num] = inst_comp.name

            # then increment the node counter by 1
            node_num = node_num + 1

        # if the component is a current source
        if inst_comp.kind == 'I':

            # to handle the current source case
            # we have to see first if it is
            # going into the node or out
            if inst_comp.np != '0':

                # if the node is connected to the
                # positive node of the source then
                # assign to it the negative value of the current source

                j_matrix[v_matrix.index(inst_comp.np)] = '-' + inst_comp.name

            if inst_comp.nn != '0':

                # if the node is connected to the
                # negative node of the source then
                # assign to it the value of the current source
                j_matrix[v_matrix.index(inst_comp.nn)] = inst_comp.name

    # then we will start the hardest part,
    # which is the fill of the Y matrix
    for inst_comp in comp_list:

        # if the component is a resistor
        if inst_comp.kind == 'R':

            # then we have to check if positive node is not ground
            if inst_comp.np != '0':

                # then save its G value in its place
                # where the row and column value are
                # equal to each other and equal to
                # the index of this node in the V matrix
                y_matrix[v_matrix.index(inst_comp.np)][v_matrix.index(inst_comp.np)] += ("+(1/" + inst_comp.name + ")")

            # then we have to check if negative node is not ground
            if inst_comp.nn != '0':

                # then save its G value in its place
                # where the row and column value are
                # equal to each other and equal to
                # the index of this node in the V matrix
                y_matrix[v_matrix.index(inst_comp.nn)][v_matrix.index(inst_comp.nn)] += ("+(1/" + inst_comp.name + ")")

            # then we have to check if positive and negative nodes are not ground
            if (inst_comp.nn != '0') and (inst_comp.np != '0'):

                # then save its G value in 2 more places
                # where the row and column values are
                # the intersections of the indices of the
                # positive and negative nodes in the V matrix
                y_matrix[v_matrix.index(inst_comp.nn)][v_matrix.index(inst_comp.np)] += ("+(-1/" + inst_comp.name + ")")
                y_matrix[v_matrix.index(inst_comp.np)][v_matrix.index(inst_comp.nn)] += ("+(-1/" + inst_comp.name + ")")

        # if the component is a voltage source
        if inst_comp.kind == 'V':

            # then we have to check if positive node is not ground
            if inst_comp.np != '0':

                # then we have to put "1" in the places of
                # intersection between the voltage source
                # and positive node indices
                y_matrix[v_matrix.index(inst_comp.np)][v_matrix.index(inst_comp.name)] += '+1'
                y_matrix[v_matrix.index(inst_comp.name)][v_matrix.index(inst_comp.np)] += '+1'

            # then we have to check if negative node is not ground
            if inst_comp.nn != '0':

                # then we have to put "1" in the places of
                # intersection between the voltage source
                # and negative node indices
                y_matrix[v_matrix.index(inst_comp.nn)][v_matrix.index(inst_comp.name)] += '-1'
                y_matrix[v_matrix.index(inst_comp.name)][v_matrix.index(inst_comp.nn)] += '-1'

    # then to enhance the readability of the
    # output, we have to put 'V' before
    # each node indicating that this is a voltage
    # of a certain node, and we have to put
    # "I(" before the voltage source and ")"
    # after it indicating that this is the value
    # of the current passing threw it

    # so we will make a loop iterating on every element in the V matrix
    # then we have to define a counter for the loop
    v_counter = 0

    for v_counter in range(counter):

        # check if this a node element
        if v_matrix[v_counter] in nodes_list:

            # then add "V"
            v_matrix[v_counter] = 'V' + v_matrix[v_counter]

        # else it must be a voltage source
        else:

            # the add "I(" and ")"
            v_matrix[v_counter] = 'I(' + v_matrix[v_counter] + ')'

    # then we have to convert the Y and J matrices
    # to symbolic matrices as to be able to
    # make some symbolic operations on them
    y_matrix = Matrix(y_matrix)
    j_matrix = Matrix(j_matrix)

    # then we have to creat a symbolic and
    # numerical representation for every unknown
    res_sym = j_matrix.transpose()*(y_matrix.inv())
    res_num = res_sym

    # then we have to replace in the numerical one
    # each component name with its value
    for comp1 in comp_list:

        res_num = res_num.subs(comp1.name, comp1.value)

    # and finally we print the answers
    print('y matrix = ')
    print(y_matrix)
    print('j matrix = ')
    print(j_matrix)
    for values in range(counter):

        print(v_matrix[values] + ' = ' + str(res_sym[values]))
        print(v_matrix[values] + ' = ' + str(res_num[values]))


if __name__ == "__main__":

    file_name = "New Text Document.txt"
    parse(file_name)

    compute_circuit()

