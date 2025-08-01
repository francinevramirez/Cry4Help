from UC3_2_request_validation import validate_request_form
import flet as ft

# Simulate backend function
def send_request(name, title, description, category, location):
    return f"""✅ Request Submitted:

👤 Name     : {name}
📝 Title    : {title}
🔧 Category : {category}
📍 Location : {location}
📄 Details  : {description}
"""

# Flet UI Version of the Form
def main(page: ft.Page):
    page.title = "Cry4Help - Submit Request"
    page.scroll = ft.ScrollMode.AUTO
    page.window_width = 500
    page.window_height = 600
    page.bgcolor = ft.Colors.GREY_100

    # NEW: Ensure the database table exists when the app starts
    setup_requests_table()

    name = ft.TextField(label="Your Name", width=400)
    title = ft.TextField(label="Request Title", width=400)
    description = ft.TextField(label="Request Description", multiline=True, min_lines=3, max_lines=5, width=400)
    category = ft.Dropdown(
        label="Category",
        width=400,
        options=[ft.dropdown.Option(opt) for opt in ['tutoring', 'repair', 'transport', 'tech', 'other']]
    )
    location = ft.TextField(label="Location", width=400)
    result_output = ft.Text(value="", size=14, color=ft.colors.RED_600, width=400, text_align=ft.TextAlign.CENTER)

    # MODIFIED: The handle_submit function
    def handle_submit(e):
        errors = validate_request_form(
            name.value,
            title.value,
            description.value,
            category.value or "",
            location.value
        )

        if errors:
            result_output.color = ft.colors.RED_600
            result_output.value = "\n".join(["❌ " + err for err in errors])
        else:
            # THIS IS WHERE YOU LOG THE REQUEST
            # Instead of the simulated send_request, call the database function
            success, message = log_request_to_db(
                name.value,
                title.value,
                description.value,
                category.value,
                location.value
            )

            # Update the UI based on whether the database save was successful
            if success:
                result_output.color = ft.colors.GREEN_700
            else:
                result_output.color = ft.colors.RED_600
            
            result_output.value = message

        page.update()

    submit_button = ft.ElevatedButton(text="Submit Request", on_click=handle_submit, width=200)

    page.add(
        ft.Column(
            [
                ft.Text("Cry4Help - Request Form", size=26, weight="bold", color=ft.colors.BLUE_900),
                name,
                title,
                description,
                category,
                location,
                submit_button,
                result_output
            ],
            spacing=15,
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )

ft.app(target=main)
