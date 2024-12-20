import os
import pandas as pd
import plotly.graph_objects as go

def load_data(software_file, units_file, processes_file, links_file):
    """
    Load data from CSV files and return dataframes.
    """
    # Verify that all required files exist
    for file in [software_file, units_file, processes_file, links_file]:
        if not os.path.exists(file):
            raise FileNotFoundError(f"Required file '{file}' is missing.")
    
    # Load data from CSV
    software_df = pd.read_csv(software_file)
    units_df = pd.read_csv(units_file)
    processes_df = pd.read_csv(processes_file)
    links_df = pd.read_csv(links_file)

    return software_df, units_df, processes_df, links_df


def generate_hover_text(software_row):
    """
    Generate hover text for a software entry as key-value pairs (excluding ID).
    """
    return "<br>".join([f"<b>{key}:</b> {value}" 
                        for key, value in software_row.items() if key != "ID"])


def create_heatmap_data(software_df, units_df, processes_df, links_df, status_mapping):
    """
    Create z_matrix (color mapping), text_matrix (cell text), and hover_matrix.
    """
    # Initialize matrices
    num_units = len(units_df)
    num_processes = len(processes_df)
    z_matrix = [[None for _ in range(num_processes)] for _ in range(num_units)]
    text_matrix = [["" for _ in range(num_processes)] for _ in range(num_units)]
    hover_matrix = [["" for _ in range(num_processes)] for _ in range(num_units)]

    # Fill matrices based on links
    for _, link in links_df.iterrows():
        process_id = link["Process ID"]
        unit_id = link["Organizational Unit ID"]
        software_id = link["Software ID"]

        process_idx = processes_df[processes_df["ID"] == process_id].index[0]
        unit_idx = units_df[units_df["ID"] == unit_id].index[0]
        software_row = software_df[software_df["ID"] == software_id].iloc[0]

        status = software_row["Status"].lower()
        software_name = software_row["Software Name"]

        # Map status to color
        z_matrix[unit_idx][process_idx] = status_mapping.get(status, None)

        # Add software name to cell
        text_matrix[unit_idx][process_idx] = software_name

        # Add detailed hover text
        hover_matrix[unit_idx][process_idx] = generate_hover_text(software_row)

    return z_matrix, text_matrix, hover_matrix


def create_process_support_map(
    software_file="csv/software.csv",
    units_file="csv/organizational_units.csv",
    processes_file="csv/processes.csv",
    links_file="csv/links.csv",
    output_file="dist/process_support_map.html"
):
    """
    Create a process support map as an interactive heatmap with hover information.
    """
    # Load data
    software_df, units_df, processes_df, links_df = load_data(
        software_file, units_file, processes_file, links_file
    )

    # Define status mapping and colorscale
    status_mapping = {
        "development": 1,
        "production": 2,
        "maintenance": 3,
        "decommissioned": 4
    }
    status_colorscale = [
        [0, "rgba(255, 255, 0, 0.6)"],    # Development, yellow
        [0.33, "rgba(0, 255, 0, 0.6)"],      # Production, green
        [0.66, "rgba(0, 123, 255, 0.6)"],     # Maintenance, blue
        [1, "rgba(169, 169, 169, 0.6)"]          # Decommissioned, gray
    ]

    # Generate data for the heatmap
    z_matrix, text_matrix, hover_matrix = create_heatmap_data(
        software_df, units_df, processes_df, links_df, status_mapping
    )

    # Create heatmap
    fig = go.Figure(data=go.Heatmap(
        z=z_matrix,
        x=processes_df["Process Name"].tolist(),
        y=units_df["Organizational Unit Name"].tolist(),
        colorscale=status_colorscale,
        colorbar=dict(
            title="Status",
            tickvals=[1, 2, 3, 4],
            ticktext=["Development", "Production", "Maintenance", "Decommissioned"]
        ),
        text=text_matrix,  # Add software name as cell text
        texttemplate="%{text}",  # Show software name in cells
        hovertemplate="%{text}<br>%{customdata}<extra></extra>",  # Add hover text
        customdata=hover_matrix  # Pass hover text
    ))

    # Update layout
    fig.update_layout(
        title="Process Support Map",
        xaxis=dict(title="Processes"),
        yaxis=dict(title="Organizational Units"),
        width=800,
        height=600,
        template="plotly_white"
    )

    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # Save the heatmap to an HTML file
    fig.write_html(output_file)
    print(f"Process support map saved to '{output_file}'.")


# Allow both module import and standalone execution
if __name__ == "__main__":
    create_process_support_map()
