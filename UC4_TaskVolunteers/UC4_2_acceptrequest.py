# accept request

import flet as ft
import requests

API_URL = "http://localhost:8000/requests/accept"  

def main(page: ft.Page):
    page.title = "Accept Help Request"
    page.window_width = 400
    page.window_height = 350
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"

    email = ft.TextField(label="Volunteer Email", width=350)
    password = ft.TextField(label="Password", password=True, width=350)
    request_id = ft.TextField(label="Request ID to Accept", width=350)
    status = ft.Text("")

    def accept_request(e):
        data = {
            "email": email.value,
            "password": password.value,
            "request_id": request_id.value,
        }
        try:
            resp = requests.post(API_URL, json=data)
            if resp.status_code == 200:
                status.value = "Request accepted successfully!"
                status.color = "green"
            else:
                status.value = f"Error: {resp.json().get('detail', 'Could not accept request')}"
                status.color = "red"
        except Exception as ex:
            status.value = f"Error: {ex}"
            status.color = "red"
        page.update()

    page.add(
        ft.Column([
            ft.Text("Accept a Help Request", size=20, weight="bold"),
            email,
            password,
            request_id,
            ft.ElevatedButton("Accept Request", on_click=accept_request),
            status,
        ], alignment="center", horizontal_alignment="center")
    )

if __name__ == "__main__":
    ft.app(target=main)

