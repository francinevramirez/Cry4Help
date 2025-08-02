# Identify Distance between Requester and Volunteer

import flet as ft
import requests

API_URL = "http://localhost:8000/distance" 

def main(page: ft.Page):
    page.title = "Requester-Volunteer Distance"
    page.window_width = 400
    page.window_height = 400
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"

    requester_email = ft.TextField(label="Requester Email", width=350)
    volunteer_email = ft.TextField(label="Volunteer Email", width=350)
    status = ft.Text("")
    distance_result = ft.Text("", size=16, weight="bold")

    def get_distance(e):
        data = {
            "requester_email": requester_email.value,
            "volunteer_email": volunteer_email.value
        }
        try:
            resp = requests.post(API_URL, json=data)
            if resp.status_code == 200:
                dist = resp.json().get("distance_km")
                if dist is not None:
                    distance_result.value = f"Distance: {dist:.2f} km"
                    status.value = "Distance calculated successfully!"
                    status.color = "green"
                else:
                    distance_result.value = ""
                    status.value = "Could not calculate distance."
                    status.color = "red"
            else:
                distance_result.value = ""
                status.value = f"Error: {resp.json().get('detail', 'Calculation failed')}"
                status.color = "red"
        except Exception as ex:
            distance_result.value = ""
            status.value = f"Error: {ex}"
            status.color = "red"
        page.update()

    page.add(
        ft.Column([
            ft.Text("Identify Distance", size=20, weight="bold"),
            requester_email,
            volunteer_email,
            ft.ElevatedButton("Get Distance", on_click=get_distance),
            status,
            distance_result,
        ], alignment="center", horizontal_alignment="center")
    )

if __name__ == "__main__":
    ft.app(target=main)

