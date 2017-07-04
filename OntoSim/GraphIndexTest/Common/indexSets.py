###############################################################################
#	 Purpose: Prepare the index sets
#	 Author:  Arne Tobias Elve
#	 Date:    Tue Jul  4 10:52:05 2017
#	 Why:     To make the index sets with correct names
###############################################################################
N = IndexSet(indices["node"])
A = IndexSet(indices["arc"])
R = IndexSet(indices["conversion"])
N_x_R = IndexSet(indices["node & conversion"])
N_R = IndexSet(indices["node_conversion"])
N_R_x_R = IndexSet(indices["node_conversion & conversion"])
N_R_x_S = IndexSet(indices["node_conversion & species"])
R_x_S = IndexSet(indices["conversion & species"])
N_x_S = IndexSet(indices["node & species"])
A_x_S = IndexSet(indices["arc & species"])
S = IndexSet(indices["species"])
N_d = IndexSet(indices["node_d"])
N_d_x_S = IndexSet(indices["node_d & species"])
N_v = IndexSet(indices["node_v"])
N_v_x_S = IndexSet(indices["node_v & species"])
N_w = IndexSet(indices["node_w"])
N_c = IndexSet(indices["node_c"])
N_r = IndexSet(indices["node_r"])
A_d = IndexSet(indices["arc_d"])
A_d_x_S = IndexSet(indices["arc_d & species"])
A_v = IndexSet(indices["arc_v"])
A_v_x_S = IndexSet(indices["arc_v & species"])
A_w = IndexSet(indices["arc_w"])
A_c = IndexSet(indices["arc_c"])
A_r = IndexSet(indices["arc_r"])
