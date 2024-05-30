import streamlit as st
import random
import networkx as nx

from utils import generate_n_node_flat_data_in_range, generate_adjancency_matrix_with_none, adjacency_matrices_to_dataframe

edge_determination_options = [
            "random",
            "criticality based",
            "community based",
        ]

class DynamicHeterogenous:
    
    def input():
        num_records = st.number_input(label="Number of records for each node", min_value=100, step=10)
        
        num_nodes = st.number_input(label="Number of Nodes in Graph", min_value=1, step=1)
        lower_num_prop = st.number_input(label="Lower range for number of properties for each node", min_value=1, step=1)
        upper_num_prop = st.number_input(label="Upper range for number of properties for each node", min_value=lower_num_prop+1, step=1)
        
        num_edge_features = st.number_input(label="Number of properties for each edge", min_value=1, step=1)
        edge_density = st.number_input(label="Edge Density in Adjacency Matrix", min_value=0.0, max_value=1.0, step=0.05)
        new_edge_likelihood = st.number_input(label="Probabilty of new edge creation", min_value=0.0, max_value=1.0, step=0.05)
        delete_edge_likelihood = st.number_input(label="Probability of edge deletion", min_value=0.0, max_value=1.0, step=0.05)
        
        edge_determination = st.selectbox(label="Algorithm for determining edge changes", options=edge_determination_options)
        
        
        num_control_points = st.number_input(label="Number of Control Points in Generation", min_value=2, step=1)
        noise = st.number_input(label="Maximum Noise in Values", min_value=0.0, max_value=1.0, step=0.05)
        
        return num_nodes, num_records, lower_num_prop, upper_num_prop, num_edge_features, edge_density, new_edge_likelihood, delete_edge_likelihood, edge_determination, noise, num_control_points
    
    def generate_node_data(num_records, num_nodes, num_control_points, noise, lower_num_prop, upper_num_prop):
        merged_data = generate_n_node_flat_data_in_range(num_nodes=num_nodes, num_records=num_records, num_control_points=num_control_points, lower_num_properties=lower_num_prop, upper_num_properties=upper_num_prop, noise=noise)
        return merged_data
    
    def generate_edge_data(num_nodes, num_records, edge_density, new_edge_likelihood, delete_edge_likelihood, edge_determination, num_edge_features):
        main = []
        
        while len(main) < num_edge_features:
            
            adjacency_matrix = generate_adjancency_matrix_with_none(num_nodes=num_nodes, density=edge_density)
            
            results = [adjacency_matrix]
            
            while len(results) < num_records:
                new_state = DynamicHeterogenous.apply_variation(results[-1], new_edge_likelihood=new_edge_likelihood, delete_edge_likelihood=delete_edge_likelihood, edge_determination=edge_determination)
                results.append(new_state)

            main.append(results)
        
        df = adjacency_matrices_to_dataframe(adjacency_matrices=main)
        
        return df
    
    def apply_variation(graph_state, new_edge_likelihood, delete_edge_likelihood, edge_determination):
        new_state = None
        
        # Code goes here
        if edge_determination == edge_determination_options[0]:
            new_state = DynamicHeterogenous.random_change(graph_state=graph_state, add_prob=new_edge_likelihood, del_prob=delete_edge_likelihood)
        elif edge_determination == edge_determination_options[1]:
            new_state = DynamicHeterogenous.criticality_change(graph_state=graph_state, add_prob=new_edge_likelihood, del_prob=delete_edge_likelihood)
        elif edge_determination == edge_determination_options[2]:
            new_state = DynamicHeterogenous.communities_change(graph_state=graph_state, add_prob=new_edge_likelihood, del_prob=delete_edge_likelihood)
        
        return new_state
    
    def random_change(graph_state, add_prob, del_prob):
        n = len(graph_state)
        new_state = [row[:] for row in graph_state]

        for i in range(n):
            for j in range(n): 
                if i != j:
                    if graph_state[i][j] is None:
                        if random.random() < add_prob:
                            new_state[i][j] = 1
                    else:
                        if random.random() < del_prob:
                            new_state[i][j] = None

        return new_state
    
    def compute_node_degrees(graph_state):
        n = len(graph_state)
        in_degrees = [0] * n
        out_degrees = [0] * n
        
        for i in range(n):
            for j in range(n):
                if i != j:
                    if graph_state[i][j] is not None:
                        out_degrees[i] += 1
                        in_degrees[j] += 1
                    
        return in_degrees, out_degrees

    def criticality_change(graph_state, add_prob, del_prob):
        n = len(graph_state)
        new_state = [row[:] for row in graph_state]
        
        in_degrees, out_degrees = DynamicHeterogenous.compute_node_degrees(graph_state)
        
        for i in range(n):
            for j in range(n):
                if i != j:
                    if graph_state[i][j] is None:
                        prob = add_prob * (1 - (out_degrees[i] / n)) * (1 - (in_degrees[j] / n))
                        if random.random() < prob:
                            new_state[i][j] = 1 
                    else:
                        prob = del_prob * (out_degrees[i] / n) * (in_degrees[j] / n)
                        if random.random() < prob:
                            new_state[i][j] = None 

        return new_state
    
    def detect_communities(graph_state):
        G = nx.DiGraph()
        n = len(graph_state)
        
        # Build the graph
        for i in range(n):
            for j in range(n):
                if graph_state[i][j] is not None:
                    G.add_edge(i, j)
        
        # Detect communities
        communities = list(nx.community.greedy_modularity_communities(G))
        node_to_community = {}
        
        # Assign nodes to communities
        for i, community in enumerate(communities):
            for node in community:
                node_to_community[node] = i
                
        # Ensure all nodes are assigned to a community
        for node in range(n):
            if node not in node_to_community:
                node_to_community[node] = len(communities)  # Assign to a new community
        
        return node_to_community

    def communities_change(graph_state, add_prob, del_prob):
        n = len(graph_state)
        new_state = [row[:] for row in graph_state]
        
        node_to_community = DynamicHeterogenous.detect_communities(graph_state)
        
        for i in range(n):
            for j in range(n):
                if i != j:
                    if graph_state[i][j] is None:
                        if node_to_community[i] == node_to_community[j]:
                            prob = add_prob * 1.5  # Higher probability for intra-community edges
                        else:
                            prob = add_prob * 0.5  # Lower probability for inter-community edges
                        
                        if random.random() < prob:
                            new_state[i][j] = 1  # Add a directed edge
                    else:
                        if node_to_community[i] == node_to_community[j]:
                            prob = del_prob * 0.5  # Lower probability for intra-community edges
                        else:
                            prob = del_prob * 1.5  # Higher probability for inter-community edges
                        
                        if random.random() < prob:
                            new_state[i][j] = None  # Remove the directed edge

        return new_state