# Verify Availability of Volunteer

import flet as ft
import requests

API_URL = "http://localhost:8000/volunteer/availability"  

def main(page: ft.Page):
    page.title = "Volunteer Availability"
    page.window_width = 400
    page.window_height = 350
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"

    email = ft.TextField(label="Volunteer Email", width=350)
    password = ft.TextField(label="Password", password=True, width=350)
    availability = ft.Dropdown(
        label="Are you available?",
        options=[
            ft.dropdown.Option("Yes"),
            ft.dropdown.Option("No")
        ],
        width=350
    )
    status = ft.Text("")

    def submit_availability(e):
        data = {
            "email": email.value,
            "password": password.value,
            "available": availability.value == "Yes"
        }
        try:
            resp = requests.post(API_URL, json=data)
            if resp.status_code == 200:
                status.value = "Availability updated successfully!"
                status.color = "green"
            else:
                status.value = f"Error: {resp.json().get('detail', 'Update failed')}"
                status.color = "red"
        except Exception as ex:
            status.value = f"Error: {ex}"
            status.color = "red"
        page.update()

    page.add(
        ft.Column([
            ft.Text("Verify Volunteer Availability", size=20, weight="bold"),
            email,
            password,
            availability,
            ft.ElevatedButton("Submit Availability", on_click=submit_availability),
            status,
        ], alignment="center", horizontal_alignment="center")
    )

if __name__ == "__main__":
    ft.app(target=main)

