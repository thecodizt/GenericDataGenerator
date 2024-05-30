import streamlit as st

from utils import generate_n_node_flat_data_in_range, generate_adjancency_matrix_with_none, adjacency_matrices_to_dataframe

class StaticHeterogenous:
    def input():
        num_records = st.number_input(label="Number of records for each node", min_value=100, step=10)
        
        num_nodes = st.number_input(label="Number of Nodes in Graph", min_value=1, step=1)
        lower_num_prop = st.number_input(label="Lower range for number of properties for each node", min_value=1, step=1)
        upper_num_prop = st.number_input(label="Upper range for number of properties for each node", min_value=1, step=1)
        
        num_edge_features = st.number_input(label="Number of properties for each edge", min_value=1, step=1)
        edge_density = st.number_input(label="Edge Density in Adjacency Matrix", min_value=0.0, max_value=1.0, step=0.05)
        
        num_control_points = st.number_input(label="Number of Control Points in Generation", min_value=2, step=1)
        noise = st.number_input(label="Maximum Noise in Values", min_value=0.0, max_value=1.0, step=0.05)
        
        return num_nodes, num_records, lower_num_prop, upper_num_prop, num_edge_features, edge_density, noise, num_control_points
    
    def generate_node_data(num_records, num_nodes, lower_num_prop, upper_num_prop, num_control_points, noise):
        merged_data = generate_n_node_flat_data_in_range(num_nodes=num_nodes, num_records=num_records, num_control_points=num_control_points, lower_num_properties=lower_num_prop, upper_num_properties=upper_num_prop, noise=noise)
        return merged_data
    
    def generate_edge_data(num_nodes, num_edge_features, edge_density):
        main = []
        
        for i in range(num_edge_features):
            adjacency_matrix = generate_adjancency_matrix_with_none(num_nodes=num_nodes, density=edge_density)
            main.append([adjacency_matrix])
            
        df = adjacency_matrices_to_dataframe(adjacency_matrices=main)
        
        return df