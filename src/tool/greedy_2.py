
import model as Model
import sys

###################################################################################################

def solve(problem):
    nodes = nodes_by_max_size(problem)    
    computers = computers_by_capacity(problem)
    computers2 = computers_by_capacity2(problem)
    allocation = Model.Allocation()
      
    assigned=0        
                   
    #--------------------------------------------------------------------------------------
        
    # First step: allocate nodes with residence constraint (since the robot capacity cannot be increased, I could allocate other nodes and not leave any space for res constraints)
    for node in nodes:			
	setting = node.settings[0]
	
	if setting.residency != []:		    
	    computer = setting.residency[0]	    
	    
	    if feasible(setting, computer, allocation, problem): 
		allocation.assign(setting,computer)
		assigned+=1			    
	    elif computer.type == 'server':
		if allocation.computer_util(computer) < computer.capacity:		    
		    increment = setting.size + allocation.computer_util(computer) - computer.capacity	
		    computer.capacity= int(computer.capacity + increment)										    				    
		else:				    
		    computer.capacity= int(computer.capacity + setting.size)
		    
		allocation.assign(setting,computer)				
		assigned+=1		
	    else:
		print '\nTHERE IS NO SOLUTION,', node.id , 'cannot be allocated - residence\n'
		sys.exit(0)					   			  	    						   
			    
    # Second/third step: allocate other nodes
    for node in nodes:
	if not allocation.which_setting(node):	
	    setting = node.settings[0]
	    
	    for computer in computers:       	
		if not allocation.which_setting(node):                                   			
		    if feasible_coRes(setting, computer, allocation, problem):			    
			if feasible(setting, computer, allocation, problem):
			    allocation.assign(setting,computer)    
			    assigned+=1    
			    done= True
			    break			    
			elif computer.type in 'server':			    			    
			    if allocation.computer_util(computer) < computer.capacity:	
				increment = setting.size + allocation.computer_util(computer) - computer.capacity			    
				computer.capacity= int(computer.capacity + increment)
			    else:			    
				computer.capacity= int(computer.capacity + setting.size)
									    
			    allocation.assign(setting,computer)				
			    assigned+=1			    
			    done= True
			    break			    		    			  			    			    
	    if done == False:		    		    		    
		print '\nTHERE IS NO SOLUTION,', node.id , 'cannot be allocated - coresidence\n'
		sys.exit(0)				   	  
	   	        
    #--------------------------------------------------------------------------------------	
        
    if assigned < len(nodes):
        print 'THERE IS NO SOLUTION\n'
        sys.exit(0)
    else:		
	print
	sum=0
	for computer in computers2:
	    print 'Computer ', computer.id, ' (capacity, used):', computer.capacity, ',', allocation.computer_util(computer)
	    sum+=allocation.computer_util(computer)
	print 'Utilisation:', sum
	print 'Performance:', allocation.perf()
	print
	    
	return allocation


##########################################################################################################################


def nodes_by_max_size(problem):
    return sorted(problem.nodes.values(), key=lambda node: max([setting.size for setting in node.settings]), reverse=True)
        
        
##########################################################################################################################


def computers_by_capacity(problem):
    return sorted(problem.computers.values(), key=lambda computer: computer.capacity, reverse=True)
    
def computers_by_capacity2(problem):
    return sorted(problem.computers.values(), key=lambda computer: computer.id, reverse=True)


##########################################################################################################################

def feasible(setting, computer, allocation, problem):            	       
   
    # Bandwidth
    tmp_allocation = allocation.clone()
    tmp_allocation.assign(setting, computer)
    for link in problem.links.values():
        if tmp_allocation.bandwidth_util(link) > link.bandwidth:
            return False
	
    # Don't overload
    if setting.size + allocation.computer_util(computer) > computer.capacity:
        return False
   
    return True


##########################################################################################################################

def feasible_coRes(setting, computer, allocation, problem):      
           
    # Coresidency
    for other_node in setting.node.coresidence:
        if allocation.which_setting(other_node):
            if allocation.computer_for_node(other_node) != computer:
                return False	                
	    
    return True




