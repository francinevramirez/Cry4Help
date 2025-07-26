import re
import flet as ft

# ----------------------
# Validators
# ----------------------

def validate_name(name):
    return name.strip().isalpha()

def validate_title(title):
    return len(title.strip()) >= 5

def validate_description(desc):
    return len(desc.strip()) >= 10

def validate_category(category):
    allowed_categories = ['tutoring', 'repair', 'transport', 'tech', 'other']
    return category.lower() in allowed_categories

def validate_location(location):
    return len(location.strip()) > 0

def validate_request_form(name, title, description, category, location):
    errors = []
    if not validate_name(name):
        errors.append("Name must be letters only and not empty.")
    if not validate_title(title):
        errors.append("Title must be at least 5 characters.")
    if not validate_description(description):
        errors.append("Description must be at least 10 characters.")
    if not validate_category(category):
        errors.append(f"Invalid category: {category}. Choose from tutoring, repair, transport, tech, or other.")
    if not validate_location(location):
        errors.append("Location must not be empty.")
    return errors

# ----------------------
# Flet App
# ----------------------

def main(page: ft.Page):
    page.title = "Cry4Help - Submit Request"
    page.window_width = 500
    page.window_height = 550
    page.scroll = ft.ScrollMode.AUTO
    page.bgcolor = ft.Colors.GREY_100

    name = ft.TextField(label="Name", width=400)
    title = ft.TextField(label="Title of Request", width=400)
    description = ft.TextField(label="Description", multiline=True, min_lines=3, max_lines=5, width=400)
    category = ft.Dropdown(
        label="Category",
        width=400,
        options=[
            ft.dropdown.Option("tutoring"),
            ft.dropdown.Option("repair"),
            ft.dropdown.Option("transport"),
            ft.dropdown.Option("tech"),
            ft.dropdown.Option("other")
        ]
    )
    location = ft.TextField(label="Location", width=400)
    message = ft.Text(value="", color=ft.Colors.RED_600, size=14)

    def submit_request(e):
        errors = validate_request_form(
            name.value,
            title.value,
            description.value,
            category.value if category.value else "",
            location.value
        )

        if errors:
            message.value = "\n".join(["❌ " + error for error in errors])
            message.color = ft.Colors.RED_600
        else:
            message.value = "✅ Request submitted successfully!"
            message.color = ft.Colors.GREEN_700

        page.update()

    submit_btn = ft.ElevatedButton(text="Submit Request", on_click=submit_request, width=200)

    page.add(
        ft.Column(
            [
                ft.Text("Create a Help Request", size=24, weight="bold", color=ft.Colors.BLUE_900),
                name,
                title,
                description,
                category,
                location,
                submit_btn,
                message
            ],
            spacing=15,
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )

ft.app(target=main)
