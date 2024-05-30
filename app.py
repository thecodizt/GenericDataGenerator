import streamlit as st

from variants import StaticHomogenous, DynamicHomogenous
from utils import visualize_node_data, visualize_edge_data

def main():
    st.title("LAM - Generic Graph Time Series Data Generator")
    
    graph_types = [
        "Static",
        "Dynamic"
    ]
    
    node_types = [
        "Homogenous",
        "Heterogenous"
    ]
    
    graph_type = st.selectbox("Graph Type", options=graph_types)
    node_type = st.selectbox("Node Type", options=node_types)
    
    st.header("Inputs")
    
    if graph_type == graph_types[0]:
        if node_type == node_types[0]:
            num_nodes, num_records, num_prop, num_edge_features, edge_density, noise, num_control_points = StaticHomogenous.input()
            
            node_data = StaticHomogenous.generate_node_data(
                num_nodes=num_nodes, 
                num_records=num_records, 
                num_prop=num_prop, 
                noise=noise, 
                num_control_points=num_control_points
            )
            
            edge_data = StaticHomogenous.generate_edge_data(
                edge_density=edge_density,
                num_nodes=num_nodes,
                num_edge_features=num_edge_features
            )
            
            st.header("Generated Data")
            
            if len(node_data):
                st.subheader("Node Data")
                st.dataframe(node_data)
                
                st.download_button("Download Node Data", data=node_data.to_csv(), file_name='nodes.csv')
                
            if len(edge_data):
                st.subheader("Edge Data")
                st.dataframe(edge_data)

                st.download_button("Download Edge Data", data=edge_data.to_csv(), file_name='edges.csv')
                
        else:
            pass
    else:
        if node_type == node_types[0]:
            num_nodes, num_records, num_prop, num_edge_features, edge_density, new_edge_likelihood, delete_edge_likelihood, edge_determination, noise, num_control_points = DynamicHomogenous.input()
            
            node_data = DynamicHomogenous.generate_node_data(
                num_nodes=num_nodes, 
                num_records=num_records,
                num_prop=num_prop, 
                noise=noise, 
                num_control_points=num_control_points
            )
            
            edge_data = DynamicHomogenous.generate_edge_data(
               num_nodes = num_nodes, 
               num_records = num_records, 
               edge_density = edge_density, 
               new_edge_likelihood = new_edge_likelihood, 
               delete_edge_likelihood = delete_edge_likelihood, 
               edge_determination = edge_determination,
               num_edge_features=num_edge_features
            )
            
            st.header("Generated Data")
            
            if len(node_data):
                st.subheader("Node Data")
                st.dataframe(node_data)
                
                st.download_button("Download Node Data", data=node_data.to_csv(), file_name='nodes.csv')
                
            if len(edge_data):
                st.subheader("Edge Data")
                st.dataframe(edge_data)

                st.download_button("Download Edge Data", data=edge_data.to_csv(), file_name='edges.csv')
        else:
            pass

if __name__ == "__main__":
    main()