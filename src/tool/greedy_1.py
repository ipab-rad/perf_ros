
import model as Model

import string
import math
import sys


###################################################################################################

def solve(problem):
    nodes = nodes_by_max_size(problem)
    computers = computers_by_capacity(problem)    
    allocation = Model.Allocation()        
          	     
    #--------------------------------------------------------------------------------------

    # First step: allocate weakest setting of nodes with residence constraint (otherwise I could allocate other nodes and not leave any space for res constraints)
    for node in nodes:
        settings = sorted(node.settings, key=lambda setting: setting.size, reverse=False)
        setting = settings[0]        		
       
	if setting.residency != []:	    
	    computer = setting.residency[0]	   
	    if feasible(setting, computer, allocation, problem):                              
		allocation.assign(setting,computer)       
	    else:
		print '\nTHERE IS NO SOLUTION,', node.id , 'cannot be allocated - residence\n'
		sys.exit(0)		

	
    # Second step: allocate weakest setting of nodes with coresidence constraint 
    # (if one node with cores is allocated in the robot, I could allocate other nodes and not leave any space for other nodes with cores)
    for node in nodes:
        if not allocation.which_setting(node):            
            settings = sorted(node.settings, key=lambda setting: setting.size, reverse=False)
            setting = settings[0]        				
            
	    if setting.node.coresidence != []:
		done= False
		for computer in computers:       	
		    if not allocation.which_setting(node):                                   			
			if feasible_coRes(setting, computer, allocation, problem):
			    allocation.assign(setting,computer)    
			    done= True
			    break			
		if done == False:
		    print '\nTHERE IS NO SOLUTION,', node.id , 'cannot be allocated - coresidence\n'
		    sys.exit(0)     					                   
  
   
    # Third step: allocate weakest setting of other nodes
    for node in nodes:
        if not allocation.which_setting(node):	    
            settings = sorted(node.settings, key=lambda setting: setting.size, reverse=False)
            setting = settings[0]      
            
            done= False         
            i=0
	    for computer in computers:
		i+=1
		if not allocation.which_setting(node):
		    if feasible(setting, computer, allocation, problem):			
			allocation.assign(setting,computer)    
			done= True
			break		   
	    if done == False:
		print '\nTHERE IS NO SOLUTION,', node.id , 'cannot be allocated - other\n'
		sys.exit(0)    
    
    #--------------------------------------------------------------------------------------	                       
    #Fourth step: replace allocated setting by a more powerful one, when possible (CPU increment = 1)
    
    gradients = {}    
    gradients_aux = {}    
           
    for node in nodes:						
	settings = sorted(node.settings, key=lambda setting: setting.size, reverse=False)		
	if len(settings) > 1 and settings[0].size < settings[1].size:
	    gradients[node.id] = node.ratio	    	
      	    
    # We increase nodes by ratio
    upgrade_nodes(allocation, problem, computers, gradients)        
    
    #--------------------------------------------------------------------------------------                          
    # Move nodes that didn'node reach their limit from full computers to others with space           
       
    for node in nodes:	
	settings = sorted(node.settings, key=lambda setting: setting.size, reverse=False)	
	
	computer = allocation.computer_for_node(node)		
	if allocation.computer_util(computer) == computer.capacity:		        
	    if len(settings) > 1 and settings[0].size < settings[1].size and settings[0].residency == []:
		gradients[node.id] = node.ratio		    
	 	    
    while len(gradients) > 0:    
                         
	max_node = max(gradients, key=gradients.get)
	node = problem.nodes[max_node]   
	computer = allocation.computer_for_node(node)       
		    
	settings = sorted(node.settings, key=lambda setting: setting.v_index, reverse=True)
		
	for computer_new in computers:		    	    
	    if computer != computer_new and feasible(settings[1], computer_new, allocation, problem):		
		allocation.assign(settings[0],computer_new)   	
				
		for tcr in node.coresidence:	    		    		    
		    if feasible(tcr.settings[0], computer_new, allocation, problem):		    
			allocation.assign(tcr.settings[0],computer_new)
		    else:
			print '\nTHERE IS NO SOLUTION,', node.id , 'cannot be allocated - coresidence server full B\n'
			sys.exit(0)			
	
		gradients_aux[node.id] = node.ratio		
		upgrade_nodes(allocation, problem, computers, gradients_aux)        							    
		break 
		
	del gradients[max_node]	   								   
                   
    #------------   
             	
    for node in nodes:						
	settings = sorted(node.settings, key=lambda setting: setting.size, reverse=False)		
	if len(settings) > 1 and settings[0].size < settings[1].size:	
	    gradients[node.id] = node.ratio	    		
    
    upgrade_nodes(allocation, problem, computers, gradients)         
	
    #--------------------------------------------------------------------------------------                          
    # Move any node without parameters nor coRes constraint from full computers to others with space           
        
    for node in nodes:		
	settings = sorted(node.settings, key=lambda setting: setting.size, reverse=False)
	    
	computer = allocation.computer_for_node(node)		
	if allocation.computer_util(computer) == computer.capacity:
	    
	    if len(settings) == 1 and settings[0].residency == [] and settings[0].node.coresidence == []:				   		    
		setting = settings[0]	    
			    
		for computer_new in computers:		    	    
		    if computer != computer_new and feasible(setting, computer_new, allocation, problem):		    
			allocation.assign(setting,computer_new)    		    		  		    
			break		
		    
		    
    for node in nodes:						
	settings = sorted(node.settings, key=lambda setting: setting.size, reverse=False)		
	if len(settings) > 1 and settings[0].size < settings[1].size:
	    gradients[node.id] = node.ratio	    	
    
    if gradients != {}:          	    
	upgrade_nodes(allocation, problem, computers, gradients)
		    
    #------------        
    # Move any node, reaching or not their limit, from full computers to others with space           
    
    for node in nodes:	
	settings = sorted(node.settings, key=lambda setting: setting.size, reverse=False)	
	
	computer = allocation.computer_for_node(node)		
	if allocation.computer_util(computer) == computer.capacity:		        
	    if len(settings) > 1 and settings[0].residency == []:
		gradients[node.id] = node.ratio		   
		        
    while len(gradients) > 0:    
                         
	max_node = min(gradients, key=gradients.get)
	node = problem.nodes[max_node]   
	computer = allocation.computer_for_node(node)     	    
	settings = sorted(node.settings, key=lambda setting: setting.v_index, reverse=True)
		
	for computer_new in computers:		    	    
	    if computer != computer_new and feasible(settings[0], computer_new, allocation, problem):		
		allocation.assign(settings[0],computer_new)   	
				
		for tcr in node.coresidence:	    		    		    
		    if feasible(tcr.settings[0], computer_new, allocation, problem):		    
			allocation.assign(tcr.settings[0],computer_new)
		    else:
			print '\nTHERE IS NO SOLUTION,', node.id , 'cannot be allocated - coresidence server full B\n'
			sys.exit(0)			
	
		gradients_aux[node.id] = node.ratio		
		upgrade_nodes(allocation, problem, computers, gradients_aux)        							    
		break 
		
	del gradients[max_node]	   				    
      	
    #------------   
		   
    for node in nodes:						
	settings = sorted(node.settings, key=lambda setting: setting.size, reverse=False)		
	if len(settings) > 1 and settings[0].size < settings[1].size:
	    #print node.id, node.ratio	
	    gradients[node.id] = node.ratio	    	
    #print gradients
    
    if gradients != {}:          	    
	upgrade_nodes(allocation, problem, computers, gradients)            		   
       
    #--------------------------------------------------------------------------------------	
      
    print
    for computer in computers:
	print 'Computer ', computer.id, ' (capacity, used):', computer.capacity, ',', allocation.computer_util(computer)
    print 'Performance:', allocation.perf()
    print
	
    return allocation


###################################################################################################
			
# Increments all the units possible per node by gradient value    
def upgrade_nodes(allocation, problem, computers, gradients):            
    
    while len(gradients)!=0:    	
	max_node = max(gradients, key=gradients.get)   
	node = problem.nodes[max_node]		
	settings = sorted(node.settings, key=lambda setting: setting.v_index, reverse=True)
	computer = allocation.computer_for_node(node)	
					
	if settings[0].size+1 <= settings[1].size:						
	    if allocation.computer_util(computer)+1 <= computer.capacity:		    
		
		old_perf = settings[0].perf		
		
		settings[0].size+=1			
		y=float(settings[0].size)/100		
		
		formula = string.replace(node.formula, 'x', 'y')		
		new_perf = round(eval(formula), 2)		
		settings[0].perf=new_perf
		
		node.ratio = round(new_perf-old_perf, 2)				    
		gradients[node.id] = node.ratio
		
	    else:			    
		del gradients[max_node]
	else:		
	    del gradients[max_node]		
    

###################################################################################################
    
def nodes_by_max_size(problem):
    return sorted(problem.nodes.values(), key=lambda node: max([setting.size for setting in node.settings]), reverse=True)


###################################################################################################

def computers_by_capacity(problem):
    return sorted(problem.computers.values(), key=lambda computer: computer.id, reverse=True)


###################################################################################################

def feasible(setting, computer, allocation, problem):    
   
    # Don't overload
    if setting.size + allocation.computer_util(computer) > computer.capacity:
        return False
   
    # Bandwidth
    tmp_allocation = allocation.clone()
    tmp_allocation.assign(setting, computer)
    for link in problem.links.values():
        if tmp_allocation.bandwidth_util(link) > link.bandwidth:
            return False

    return True


###################################################################################################

def feasible_coRes(setting, computer, allocation, problem):   
    
    # Coresidency
    for other_node in setting.node.coresidence:
        if allocation.which_setting(other_node):
            if allocation.computer_for_node(other_node) != computer:
                return False

    # Don't overload
    if setting.size + allocation.computer_util(computer) > computer.capacity:
        return False   
    
    # Bandwidth
    tmp_allocation = allocation.clone()
    tmp_allocation.assign(setting, computer)
    for link in problem.links.values():
        if tmp_allocation.bandwidth_util(link) > link.bandwidth:
            return False

    return True




