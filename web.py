import asyncio
import websockets
import json
import flet as ft
import pandas as pd
import folium
from folium.plugins import HeatMap
import threading
import http.server
import socketserver
import os
from sklearn.cluster import DBSCAN
from folium.plugins import MarkerCluster
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
from sklearn.metrics import silhouette_score as ss
import itertools

# Function to generate heatmap and save it as an HTML file
def generate_heatmap():
    csv_file = os.path.join(os.path.dirname(__file__), "sample_addresses.csv")  # Get the current directory
    if not os.path.exists(csv_file):
        print(f"File not found: {csv_file}")
        return
    
    df = pd.read_csv(csv_file)
    print(f"CSV File Loaded: {csv_file}")

    df_counts = df.groupby(['Latitude', 'Longitude']).size().reset_index(name='count')

    min_value = df_counts['count'].min()
    max_value = df_counts['count'].max()

    df_counts['normalized_intensity'] = df_counts['count'].apply(
        lambda x: (x - min_value) / (max_value - min_value) if max_value > min_value else 1
    )

    heatmap_data = df_counts[['Latitude', 'Longitude', 'normalized_intensity']].values.tolist()

    mapObj = folium.Map([10.3157, 123.8854], zoom_start=10)
    HeatMap(heatmap_data).add_to(mapObj)

    # Save the heatmap in a folder named "static"
    os.makedirs("static", exist_ok=True)
    heatmap_path = os.path.join("static", "heatmap.html")
    if os.path.exists(heatmap_path):
        os.remove(heatmap_path) 

    mapObj.save(heatmap_path)

    return heatmap_path  # Return the file path

# Start a local HTTP server in the background
def start_http_server():
    PORT = 8000
    os.chdir("static")  # Serve files from the "static" directory
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        print(f"Serving at http://127.0.0.1:{PORT}/heatmap.html")
        httpd.serve_forever()

threading.Thread(target=start_http_server, daemon=True).start()  # ✅ Run HTTP server in background

def apply_dbscan():
    csv_file = os.path.join(os.path.dirname(__file__), "sample_addresses.csv")  # Get the current directory
    if not os.path.exists(csv_file):
        print(f"File not found: {csv_file}")
        return
    
    df = pd.read_csv(csv_file)
    print(f"CSV File Loaded: {csv_file}")
    # Extract Latitude and Longitude
    lat_long = df[['Latitude', 'Longitude']]
    lat, long = df.Latitude, df.Longitude
    X = np.radians(lat_long.to_numpy())  # Convert to radians for Haversine

    # Apply DBSCAN Clustering
    epsilons = np.linspace(1/6371, 5/6371, num = 15)
    min_samples = np.arange(2, 20, step = 3)
    combinations = list(itertools.product(epsilons, min_samples))
    N = len(combinations)
    def get_scores_and_labels(combinations, X):
        scores = []
        all_labels_list = []

        for i, (eps, num_samples) in enumerate(combinations):
            dbscan_cluster_model = DBSCAN(eps=eps, min_samples=num_samples, algorithm="ball_tree", metric='haversine').fit(X)
            labels = dbscan_cluster_model.labels_
            labels_set = set(labels)
            num_clusters = len(labels_set)
            if -1 in labels_set:
                num_clusters -= 1
            
            if (num_clusters < 2):
                scores.append(-10)
                all_labels_list.append('bad')
                c = (eps, num_samples)
                continue
            
            scores.append(ss(X, labels))
            all_labels_list.append(labels)

        best_index = np.argmax(scores)
        best_parameters = combinations[best_index]
        best_labels = all_labels_list[best_index]
        best_score = scores[best_index]
        print(f"best score: {best_score}")

        return{'best_epsilon': best_parameters[0],
            'best_min_samples': best_parameters[1],
            'best_labels': best_labels,
            'best_score': best_score}

    best_dict = get_scores_and_labels(combinations, X)
    df['cluster'] = best_dict['best_labels']
    print(df['cluster'].value_counts())

    cluster_counts = df['cluster'].value_counts()
    total_points = len(df)
    heavy_threshold = total_points * 0.3  # Define what percentage is considered heavy
    moderate_threshold = total_points * 0.1  # Define what percentage is considered moderate

    def classify_cluster(count, label):
        if label == -1:  # Cluster -1 represents noise
            return 'Unclassified'
        elif count >= heavy_threshold:
            return 'Heavy'
        elif count >= moderate_threshold:
            return 'Moderate'
        else:
            return 'Light'

    # Create a new column for classification based on cluster size
    df['classification'] = df['cluster'].map(lambda x: classify_cluster(cluster_counts.get(x, 0), x))

    # Scatter Plot with Classification
    fig = px.scatter(df, x='Longitude', y='Latitude', color='classification', 
                    color_discrete_map={'Heavy': 'red', 'Moderate': 'yellow', 'Light': 'green', 'Unclassified': 'black'}, title="PWD Density Cluster",
                    labels={'classification': 'Cluster Classification'},
                    category_orders={'classification': ['Heavy', 'Moderate', 'Light', 'Unclassified']})

    fig.update_layout(
        title_text="PWD Density Cluster",
        title_x=0.5  # Center align title
    )
    # Save plot as HTML
    os.makedirs("static", exist_ok=True)  # Ensure "static" folder exists
    plot_path = os.path.join("static", "dbscan_plot.html")
    
    if os.path.exists(plot_path):
        os.remove(plot_path)  # Delete old file before writing new one

    fig.write_html(plot_path)


    print(f"DBSCAN plot saved: {plot_path}")

async def main(page: ft.Page):
    page.title = "PWD Assistance Receiver"
    page.bgcolor = "white"
    page.scroll = "auto"

    alert_column = ft.Column([], scroll="auto")

    def show_alert(data):
        page.controls.clear()  # Remove everything
        page.open(alert_dialog)  # Only show the alert
        
        alert_dialog.content.value = (
            f"{data['full_name']} needs help at {data['location']}\n\n\n"
            f"Date of Birth: {data['dob']}\n"
            f"Gender: {data['gender']}\n"
            f"Contact Number: {data['contact_number']}\n"
            f"Current Address: {data['current_address']}\n"
            f"Emergency Contact: {data['emergency_contact']['name']} "
            f"({data['emergency_contact']['relationship']}) - {data['emergency_contact']['contact_number']}\n"
            f"Disability Type: {data['disability_type']}\n"
            f"Severity Level: {data['severity_level']}\n"
            f"Assistive Devices: {data['assistive_devices']}\n"
            f"Communication Preferences: {data['communication_prefs']}\n"
            f"Mobility Needs: {data['mobility_needs']}\n"
        )
        
        alert_dialog.open = True
        page.update()

    def close_alert(e):
        page.close(alert_dialog)
        page.controls.clear()  # Clear the page
        setup_ui()  # Rebuild the original UI
        page.update()

    def on_confirm_click(e):
        page.open(info_dialog)

    info_dialog = ft.AlertDialog(
        title=ft.Text("Assistance Dispatched"),
        content=ft.Text("The user has been informed and rescuer is on the way."),
        bgcolor="#356D7C",
        on_dismiss=lambda e: setup_ui()
    )

    alert_dialog = ft.AlertDialog(
        title=ft.Text("🚨 Help Needed!", size=20, weight=ft.FontWeight.BOLD, color="red"),
        content=ft.Text(""),
        actions=[
            ft.TextButton("Pass to Next Rescuer", on_click=close_alert),
            ft.TextButton("Send Help", on_click=on_confirm_click)
        ],
        modal=True,
        actions_alignment=ft.MainAxisAlignment.END,
        bgcolor="#356D7C",
    )
    

    
    # ✅ WebSocket listener
    async def listen_websocket():
        uri = "ws://localhost:6789"
        while True:
            try:
                async with websockets.connect(uri) as websocket:
                    while True:
                        message = await websocket.recv()
                        data = json.loads(message)
                        print("Received data:", data)
                        page.pubsub.send_all(json.dumps(data))
            except websockets.exceptions.ConnectionClosedError as e:
                print(f"WebSocket closed: {e}. Reconnecting in 3 seconds...")
                await asyncio.sleep(3)
            except Exception as e:
                print(f"Unexpected error: {e}. Retrying in 5 seconds...")
                await asyncio.sleep(5)

    # ✅ Subscribe to WebSocket messages

    page.pubsub.subscribe(lambda data: show_alert(json.loads(data)))

    # ✅ Start WebSocket listener in the background
    asyncio.create_task(listen_websocket())

    # ✅ Generate heatmap and get URL
    generate_heatmap() 
    apply_dbscan()

    heatmap_url = "http://127.0.0.1:8000/heatmap.html"
    dbscan_url = "http://127.0.0.1:8000/dbscan_plot.html"

    def setup_ui():
        heatmap_view = ft.WebView(url=heatmap_url, width=800, height=400)
        dbscan_view = ft.WebView(url=dbscan_url, width=800, height=800)

        page.add(
            ft.Column(
                [
                    ft.Container(
                        content=alert_column,
                        padding=10,
                        expand=True
                    ),
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Text("Display of PWDs in the Area", size=20, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER, color="#356D7C"),
                                ft.Container(heatmap_view, alignment=ft.alignment.center)
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            expand=True
                        ),
                        padding=10,
                        expand=True
                    ),
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Container(dbscan_view, alignment=ft.alignment.center)
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            expand=True
                        ),
                        padding=10,
                        expand=True
                    )
                ],
                scroll="auto",
                expand=True
            ),
    )

    setup_ui()

ft.app(target=main, view=ft.WEB_BROWSER)
