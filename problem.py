
import model as Model

NODES_PER_ROBOT = 6
ROBOT_CPU_CAPACITY = 100
SERVER_CAPACITY = 400		# for greedy_2 the value must be 0

ALGORITHM = 'greedy_1'	# greedy_2


###################################################################################################

def generate(num_computers, num_robots, num_cameras):
    msgs_robot = 0
    for x in range(1, num_robots + 1):
        msgs_robot += 8 + num_robots - x

    # Computers for each robot
    computers = {}
    
    for x in range(1, num_robots+1):
        computer = Model.Computer('C' + str(x), ROBOT_CPU_CAPACITY)
        computer.type = 'robot'
        computers[computer.id] = computer
           
    # Computers for servers
    for x in range(num_robots+1, num_computers+1):
        computer = Model.Computer('C' + str(x), SERVER_CAPACITY)
        computer.type = 'server'
        computers[computer.id] = computer
        
    #-----------------------------------------------------------------------------------------------------------      
    # Links
    num_wireless_links = 0
    for x in range(1, num_robots+1):
        num_wireless_links += num_computers - x

    num_link=1
    links = {}

    # wireless links
    for x in range(1, num_robots+1):
        for y in range(x+1, num_computers+1):
            bandwidth = 54000/num_wireless_links 
            link = Model.Link('L' + str(num_link), computers['C'+str(x)], computers['C' + str(y)], bandwidth)
            links[link.id] = link
            computers['C'+str(x)].add_link(link)
            computers['C'+str(y)].add_link(link)
            num_link+=1

    # wired links
    for x in range(num_robots+1, num_computers+1):
        for y in range(x+1, num_computers+1):
            bandwidth = 100000
            link = Model.Link('L' + str(num_link), computers['C'+str(x)], computers['C'+str(y)], bandwidth)
            links[link.id] = link
            computers['C'+str(x)].add_link(link)
            computers['C'+str(y)].add_link(link)
            num_link+=1

    #-----------------------------------------------------------------------------------------------------------      
    # Nodes    
    #
    # Experiment, N1
    # Tracker (one per camera), N2..N(1+camera_no)
    # Then for each robot:
    # 	Environment (1+cameras) + (robot-1)*6
    #   Model,
    #   Planner,
    #   AMCL,
    #   Navigation,
    #   Youbot_core

    if num_computers - num_robots > 1:
        servers_residence = []
        for n in range(num_robots+1, num_computers+1):
            servers_residence.append(computers['C' + str(n)])
    else:
        servers_residence = [computers['C' + str(num_computers)]]

    num_node = 1
    nodes = {}

    # Experiment node
    id = 'N' + str(num_node)
    node = Model.Node(id, [], None)
    setting = Model.Setting(node, 1, 1, servers_residence, 'S1')
    node.settings = [setting]
    nodes[node.id] = node
    node.formula = 'x'
    node.ratio = 0.01
    num_node += 1


    # Nodes for cameras
    for x in range(1, num_cameras+1):
        # Tracker
        id = 'N' + str(num_node)
        node = Model.Node(id, [], None)       
        
        if ALGORITHM == 'greedy_1':                      
	    setting_min = Model.Setting(node, 200, 100, servers_residence, 'S1')
	    setting_max = Model.Setting(node, 80, 40, servers_residence, 'S2')                      
	    node.settings = [setting_min, setting_max]        
	elif ALGORITHM == 'greedy_2':                
	    setting = Model.Setting(node, 120, 70, servers_residence, 'S1')        
	    node.settings = [setting]
        
        nodes[node.id] = node
        node.formula = '66.62*math.log(x)+56.308'        
        node.ratio = 0.83
        num_node += 1


    # Nodes for robots
    for x in range(1, num_robots+1):
        robot_residence = []
        robot_residence.append(computers['C' + str(x)])
    
        # Environment
        id = 'N' + str(num_node)
        node = Model.Node(id, [], None)
        setting = Model.Setting(node, 1, 1, [], 'S1')
        node.settings = [setting]
        nodes[node.id] = node
        node.formula = 'x'
        node.ratio = 0.01
        num_node += 1

        # Model
        id = 'N' + str(num_node)
        node = Model.Node(id, [], None)               
               
        if ALGORITHM == 'greedy_1':
	    setting_min = Model.Setting(node, 59, 100, [], 'S1')
	    setting_max = Model.Setting(node, 17, 20, [], 'S2')        
	    node.settings = [setting_min, setting_max]        
        elif ALGORITHM == 'greedy_2':        		
	    setting = Model.Setting(node, 39, 70, [], 'S1')        
	    node.settings = [setting]
        
        nodes[node.id] = node
        node.formula = '63.707*math.log(x)+132.16'
        node.ratio = 3.64
        num_node += 1
      
        # Planner
        id = 'N' + str(num_node)
        planner_node = Model.Node(id, [], None)
        setting = Model.Setting(planner_node, 1, 1, [], 'S1')
        planner_node.settings = [setting]
        nodes[planner_node.id] = planner_node
        planner_node.formula = 'x'
        planner_node.ratio = 0.01
        num_node += 1     

        # AMCL
        id = 'N' + str(num_node)
        node = Model.Node(id, [], None)               
              
        if ALGORITHM == 'greedy_1':
	    setting_min = Model.Setting(node, 66, 100, [], 'S1')
	    setting_max = Model.Setting(node, 19, 20, [], 'S2')        
	    node.settings = [setting_min, setting_max]        
	elif ALGORITHM == 'greedy_2':                	    
	    setting = Model.Setting(node, 41, 50, [], 'S1')        
	    node.settings = [setting] 
        
        nodes[node.id] = node
        node.formula = '135.4*(x**2) + 55.126*(x)+4.6383'
        node.ratio = 1.33
        num_node += 1

        # Navigation
        id = 'N' + str(num_node)
        navigation_node = Model.Node(id, [], None)               
              
        if ALGORITHM == 'greedy_1':
	    setting_min = Model.Setting(navigation_node, 50, 100, [], 'S1')
	    setting_max = Model.Setting(navigation_node, 25, 10, [], 'S2')        
	    navigation_node.settings = [setting_min, setting_max]
	elif ALGORITHM == 'greedy_2':                
	    setting = Model.Setting(navigation_node, 39, 65, [], 'S1')        
	    navigation_node.settings = [setting]
                
        nodes[navigation_node.id] = navigation_node
        navigation_node.formula = '129.12*math.log(x)+188.36'
        navigation_node.ratio = 5.06
        num_node += 1
        
        # Youbot_core
        id = 'N' + str(num_node)
        youbot_node = Model.Node(id, [], None)
        setting = Model.Setting(youbot_node, 16, 1, robot_residence, 'S1')
        youbot_node.settings = [setting]
        nodes[youbot_node.id] = youbot_node
        youbot_node.formula = 'x'
        youbot_node.ratio = 0.01
        num_node += 1

        # two coresidence constraints
        # Planner with Navigation
        planner_coresidence = nodes['N' + str(1+num_cameras+((x-1)*NODES_PER_ROBOT)+5)]
        planner_node.coresidence = [planner_coresidence]
        # Navigation with planner
        navigation_coresidence = nodes['N' + str(1+num_cameras+(x-1)*NODES_PER_ROBOT+3)]
        navigation_node.coresidence = [navigation_coresidence]
        
    #-----------------------------------------------------------------------------------------------------------      
    # Messages

    num_mess=1
    messages = {}

    # Messages from Experiment (Experiment - Environment)
    for x in range(1, num_robots+1):
        msg_id = 'M' + str(num_mess)
        source = nodes['N1']
        target = nodes['N' + str(1+num_cameras+(x-1)*NODES_PER_ROBOT+1)]
        size = 1
        message = Model.Message(msg_id, source, target, size)
        source.add_msg_source(message)
        target.add_msg_sink(message)
        num_mess += 1
        messages[message.id] = message

    # Messages from cameras (Tracker - Environment)
    for x in range(1, num_cameras+1):
        msg_id = 'M' + str(num_mess)
        source = nodes['N' + str(1+x)]
        target = nodes['N' + str(2+num_cameras)]
        size = 3
        message = Model.Message(msg_id, source, target, size)
        source.add_msg_source(message)
        target.add_msg_sink(message)
        num_mess += 1
        messages[message.id] = message

    # Messages from robots
    for x in range(1, num_robots+1):
        # (Environment - Model)
        msg_id = 'M' + str(num_mess)
        source = nodes['N' + str(1+num_cameras+(x-1)*NODES_PER_ROBOT+1)]
        target = nodes['N' + str(1+num_cameras+(x-1)*NODES_PER_ROBOT+2)]
        size = 1
        message = Model.Message(msg_id, source, target, size)
        source.add_msg_source(message)
        target.add_msg_sink(message)
        num_mess += 1
        messages[message.id] = message

        # (Environment - Planner)
        msg_id = 'M' + str(num_mess)
        source = nodes['N' + str(1+num_cameras+(x-1)*NODES_PER_ROBOT+1)]
        target = nodes['N' + str(1+num_cameras+(x-1)*NODES_PER_ROBOT+3)]
        size = 1
        message = Model.Message(msg_id, source, target, size)
        source.add_msg_source(message)
        target.add_msg_sink(message)
        num_mess += 1
        messages[message.id] = message

        # (Environment - Youbot_core)
        msg_id = 'M' + str(num_mess)
        source = nodes['N' + str(1+num_cameras+(x-1)*NODES_PER_ROBOT+1)]
        target = nodes['N' + str(1+num_cameras+(x-1)*NODES_PER_ROBOT+6)]
        size = 1
        message = Model.Message(msg_id, source, target, size)
        source.add_msg_source(message)
        target.add_msg_sink(message)
        num_mess += 1
        messages[message.id] = message

        # Between robots (Environment - Environment)
        for y in range(x+1, num_robots+1):
            msg_id = 'M' + str(num_mess)
            source = nodes['N' + str(1+(num_cameras)+(x-1)*NODES_PER_ROBOT+1)]
            target = nodes['N' + str(1+(num_cameras)+(y-1)*NODES_PER_ROBOT+1)]
            size = 1
            message = Model.Message(msg_id, source, target, size)
            source.add_msg_source(message)
            target.add_msg_sink(message)
            num_mess += 1
            messages[message.id] = message

        ##
       
        # (Planner - Navigation)
        msg_id = 'M' + str(num_mess)
        source = nodes['N' + str(1+num_cameras+(x-1)*NODES_PER_ROBOT+3)]
        target = nodes['N' + str(1+num_cameras+(x-1)*NODES_PER_ROBOT+5)]
        size = 1
        message = Model.Message(msg_id, source, target, size)
        source.add_msg_source(message)
        target.add_msg_sink(message)
        num_mess += 1
        messages[message.id] = message

        # (Navigation - Environment)
        msg_id = 'M' + str(num_mess)
        source = nodes['N' + str(1+num_cameras+(x-1)*NODES_PER_ROBOT+5)]
        target = nodes['N' + str(1+num_cameras+(x-1)*NODES_PER_ROBOT+1)]
        size = 1
        message = Model.Message(msg_id, source, target, size)
        source.add_msg_source(message)
        target.add_msg_sink(message)
        num_mess += 1
        messages[message.id] = message

        # (Youbot_core - Navigation)
        msg_id = 'M' + str(num_mess)
        source = nodes['N' + str(1+num_cameras+(x-1)*NODES_PER_ROBOT+6)]
        target = nodes['N' + str(1+num_cameras+(x-1)*NODES_PER_ROBOT+5)]
        size = 1
        message = Model.Message(msg_id, source, target, size)
        source.add_msg_source(message)
        target.add_msg_sink(message)
        num_mess += 1
        messages[message.id] = message

        # (Youbot_core - AMCL)
        msg_id = 'M' + str(num_mess)
        source = nodes['N' + str(1+num_cameras+(x-1)*NODES_PER_ROBOT+6)]
        target = nodes['N' + str(1+num_cameras+(x-1)*NODES_PER_ROBOT+4)]
        size = 1
        message = Model.Message(msg_id, source, target, size)
        source.add_msg_source(message)
        target.add_msg_sink(message)
        num_mess += 1
        messages[message.id] = message

        # (AMCL - Environment)
        msg_id = 'M' + str(num_mess)
        source = nodes['N' + str(1+(num_cameras)+(x-1)*NODES_PER_ROBOT+4)]
        target = nodes['N' + str(1+(num_cameras)+(x-1)*NODES_PER_ROBOT+1)]
        size = 1
        message = Model.Message(msg_id, source, target, size)
        source.add_msg_source(message)
        target.add_msg_sink(message)
        num_mess += 1
        messages[message.id] = message
              

    problem = Model.Problem(nodes=nodes, messages=messages, computers=computers, links=links)
    return problem




