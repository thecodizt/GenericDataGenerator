import streamlit as st
import random

from utils import generate_n_node_flat_data, generate_adjancency_matrix_with_none, adjacency_matrices_to_dataframe

edge_determination_options = [
            "random"
        ]

class DynamicHomogenous:
    
    
    def input():
        num_records = st.number_input(label="Number of records for each node", min_value=100, step=10)
        
        num_nodes = st.number_input(label="Number of Nodes in Graph", min_value=1, step=1)
        num_prop = st.number_input(label="Number of properties for each node", min_value=1, step=1)
        
        edge_density = st.number_input(label="Edge Density in Adjacency Matrix", min_value=0.0, max_value=1.0, step=0.05)
        new_edge_likelihood = st.number_input(label="Probabilty of new edge creation", min_value=0.0, max_value=1.0, step=0.05)
        delete_edge_likelihood = st.number_input(label="Probability of edge deletion", min_value=0.0, max_value=1.0, step=0.05)
        
        
        edge_determination = st.selectbox(label="Algorithm for determining edge changes", options=edge_determination_options)
        
        
        num_control_points = st.number_input(label="Number of Control Points in Generation", min_value=2, step=1)
        noise = st.number_input(label="Maximum Noise in Values", min_value=0.0, max_value=1.0, step=0.05)
        
        return num_nodes, num_records, num_prop, edge_density, new_edge_likelihood, delete_edge_likelihood, edge_determination, noise, num_control_points
    
    def generate_node_data(num_records, num_nodes, num_prop, num_control_points, noise):
        merged_data = generate_n_node_flat_data(num_nodes=num_nodes, num_records=num_records, num_control_points=num_control_points, num_properties=num_prop, noise=noise)
        return merged_data
    
    def generate_edge_data(num_nodes, num_records, edge_density, new_edge_likelihood, delete_edge_likelihood, edge_determination):
        adjacency_matrix = generate_adjancency_matrix_with_none(num_nodes=num_nodes, density=edge_density)
        
        results = [adjacency_matrix]
        
        while len(results) < num_records:
            new_state = DynamicHomogenous.apply_variation(results[-1], new_edge_likelihood=new_edge_likelihood, delete_edge_likelihood=delete_edge_likelihood, edge_determination=edge_determination)
            results.append(new_state)
        
        df = adjacency_matrices_to_dataframe(adjacency_matrices=[results])
        
        return df
    
    def apply_variation(graph_state, new_edge_likelihood, delete_edge_likelihood, edge_determination):
        new_state = None
        
        # Code goes here
        if edge_determination == edge_determination_options[0]:
            new_state = DynamicHomogenous.random_change(graph_state=graph_state, add_prob=new_edge_likelihood, del_prob=delete_edge_likelihood)
        
        return new_state
    
    def random_change(graph_state, add_prob, del_prob):
        n = len(graph_state)
        new_state = [row[:] for row in graph_state]  # Create a deep copy of the graph state

        # Iterate through each possible edge in the adjacency matrix
        for i in range(n):
            for j in range(i + 1, n):  # Ensure we do not duplicate edges (i, j) and (j, i) and skip self-loops
                if graph_state[i][j] is None:  # No edge currently
                    if random.random() < add_prob:
                        new_state[i][j] = 1
                        new_state[j][i] = 1
                else:  # Edge exists
                    if random.random() < del_prob:
                        new_state[i][j] = None
                        new_state[j][i] = None

        return new_state