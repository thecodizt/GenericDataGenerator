import streamlit as st

from utils import generate_n_node_flat_data_in_range, generate_adjancency_matrix_with_none, adjacency_matrices_to_dataframe
from input import node_heterogeneous, edge_static

class StaticHeterogenous:
    def input():
        num_records = st.number_input(label="Number of records for each node", min_value=100, step=10)
        
        num_nodes, node_lower_range, node_upper_range, lower_num_prop, upper_num_prop, node_feature_names, num_control_points, noise  = node_heterogeneous()
                    
        num_edge_features, edge_density, edge_feature_names= edge_static()
        
        return num_nodes, node_lower_range, node_upper_range, num_records, lower_num_prop, upper_num_prop, node_feature_names, num_edge_features, edge_density, edge_feature_names, noise, num_control_points
    
    def generate_node_data(num_records, num_nodes, lower_num_prop, upper_num_prop, num_control_points, noise, features=None, node_lower_range = 0, node_upper_range = 1):
        merged_data = generate_n_node_flat_data_in_range(
            num_nodes=num_nodes, 
            num_records=num_records, 
            num_control_points=num_control_points, 
            lower_num_properties=lower_num_prop, 
            upper_num_properties=upper_num_prop, 
            noise=noise, 
            features=features,
            node_lower_range = node_lower_range, 
            node_upper_range = node_upper_range, 
        )
        return merged_data
    
    def generate_edge_data(num_nodes, num_edge_features, edge_density, features=None):
        main = []
        
        for i in range(num_edge_features):
            adjacency_matrix = generate_adjancency_matrix_with_none(num_nodes=num_nodes, density=edge_density)
            main.append([adjacency_matrix])
            
        df = adjacency_matrices_to_dataframe(adjacency_matrices=main, features=features)
        
        return df