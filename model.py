

# Implementation of all the structures used


###################################################################################################

class Problem():
    def __init__(self, nodes, messages, computers, links):
        self.computers = computers
        self.links = links
        self.nodes = nodes
        self.messages = messages

    def __str__(self):
        res = describe('Nodes', self.nodes)
        res += describe('Messages', self.messages)
        res += describe('Computers', self.computers)
        res += describe('Links', self.links)
        return res
    

###################################################################################################

class Allocation():
    def __init__(self):
        self.mapping = {}    

    def __str__(self):
        solution = []
        for (setting, computer) in self.mapping.items():
            solution.append((str(setting), computer.id))
        sorted_solution = sorted(solution, key=lambda tup: tup[0])
        return str(sorted_solution)   
    
    def clone(self):
        a = Allocation()
        for (setting, computer) in self.mapping.items():
            a.assign(setting, computer)
        return a

    def assign(self, setting, computer):
        self.mapping[setting] = computer   

    def computer_util(self, computer):
        util = 0
        for (setting, p) in self.mapping.items():
            if p == computer:
                util += setting.size
        return util

    def perf(self):
        Perf = 0
	for setting in self.mapping:
	    #print setting, setting.perf
            Perf += setting.perf
        return Perf               

    def which_setting(self, n):
        for (s, _) in self.mapping.items():
            if s.node == n:
                return s
        return None

    def computer_for_node(self, n):		
        s = self.which_setting(n)        
        return self.mapping[s]

    def bandwidth_util(self, link):
        total = 0
        (c1, c2) = link.computers
        c1_nodes = []
        c2_nodes = []
        for setting, allocated_computer in self.mapping.items():
            if allocated_computer == c1:
                c1_nodes.append(setting.node)
            if allocated_computer == c2:
                c2_nodes.append(setting.node)
        for node in c1_nodes:
            for message in node.from_messages:
                if message.to_node in c2_nodes:
                    total += message.size
            for message in node.to_messages:
                if message.from_node in c2_nodes:
                    total += message.size
        return total


###################################################################################################

class Computer():
    def __init__(self, id, capacity):
        self.id = id
        self.capacity = capacity
        self.links = []
        self.type=''

    def __str__(self):
        return self.id + ' (' + str(self.capacity) + ')'

    def add_link(self, link):
        self.links.append(link)


###################################################################################################

class Node():
    def __init__(self, id, coresidence, settings):
        self.id = id
        self.coresidence = coresidence
        self.from_messages = []
        self.to_messages = []
        self.settings = settings
        self.formula=''
        self.ratio=0        

    def __str__(self):
        setting_desc = map(str, self.settings)
        if self.coresidence != []:
            coresidency_desc = ' Coresidency: ' + '/'.join([node.id for node in self.coresidence])
        else:
            coresidency_desc = ''
        return "Node " + str(self.id) + coresidency_desc + ' Settings: ' + str(setting_desc)

    def add_msg_source(self, msg):
        self.from_messages.append(msg)

    def add_msg_sink(self, msg):
        self.to_messages.append(msg)
        

###################################################################################################

class Setting():
    def __init__(self, node, size, perf, residency, v_index):
        self.node = node
        self.size = size
        self.perf = perf
        self.residency = residency
        self.v_index = v_index

    def __str__(self):
        return str(self.node.id) + '-P' + str(self.perf) + '-U' + str(self.size) + '-R:' + ':'.join( [x.id for x in self.residency])


###################################################################################################

class Message():
    def __init__(self, id, node1, node2, size):
        self.id = id
        self.from_node = node1
        self.to_node = node2
        self.size = size

    def __str__(self):
        return "Message " + str(self.id) + " " + str(self.from_node.id) + " -> " + str(self.to_node.id) + ' [' + str(self.size) + ']'


###################################################################################################

class Link():
    def __init__(self, id, c1, c2, bandwidth):
        self.id = id
        self.computers = [c1, c2]
        self.bandwidth = bandwidth

    def __str__(self):
        proc_desc = [str(p.id) for p in self.computers]
        return "Link " + str(self.id) + ' ' + str(proc_desc) + ' (' + str(self.bandwidth) + ')'


###################################################################################################

def describe(header, dict):
    sorted_keys = sorted(dict)
    dict_desc = [str(dict[k]) for k in sorted_keys]
    return header + '\n' + '\n'.join(dict_desc) + '\n'





