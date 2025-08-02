# File: request_app.py
import flet as ft
import sqlite3

# --- 1. Request Validation Logic (from UC3_2) ---
def validate_request_form(name, title, description, category, location):
    errors = []
    if not name.strip() or not name.strip().isalpha():
        errors.append("Username must be letters only and not empty.")
    if len(title.strip()) < 5:
        errors.append("Title must be at least 5 characters.")
    if len(description.strip()) < 10:
        errors.append("Description must be at least 10 characters.")
    if not category:
        errors.append("You must select a category.")
    if not location.strip():
        errors.append("Location cannot be empty.")
    return errors

# --- 2. Backend Logic for "History Log Request" ---

DB_NAME = "cry4help.db"

def get_user_id_by_username(username):
    """A helper function to find a user's ID by their name."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def log_request_to_db(requester_id, title, description, category, location):
    """
    THIS IS THE CORE FUNCTION FOR YOUR "History Log Request" TASK.
    It saves the validated request data into the 'requests' table.
    """
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        # The initial status for any new request is 'Open'
        cursor.execute(
            """
            INSERT INTO requests (requesterID, title, description, category, location, status) 
            VALUES (?, ?, ?, ?, ?, 'Open')
            """,
            (requester_id, title, description, category, location)
        )
        conn.commit()
        conn.close()
        # On success, return a success message
        return True, "✅ Request has been successfully logged to the history!"
    except Exception as e:
        # On failure, return the error message
        return False, f"❌ A database error occurred: {e}"

# --- 3. Flet User Interface ---

def main(page: ft.Page):
    page.title = "Cry4Help - Submit Request"
    page.scroll = ft.ScrollMode.AUTO
    page.window_width = 500
    page.window_height = 650
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    name = ft.TextField(label="Your Username", width=400, hint_text="Try: jasmine, garcia, or ramirez")
    title = ft.TextField(label="Request Title", width=400)
    description = ft.TextField(label="Request Description", multiline=True, min_lines=3, width=400)
    category = ft.Dropdown(
        label="Category",
        width=400,
        options=[ft.dropdown.Option(opt) for opt in ['tutoring', 'repair', 'transport', 'tech', 'other']]
    )
    location = ft.TextField(label="Location", width=400)
    feedback_text = ft.Text(value="", size=14, width=400, text_align=ft.TextAlign.CENTER)

    def handle_submit(e):
        # 1. Validate the form fields
        errors = validate_request_form(
            name.value, title.value, description.value, category.value, location.value
        )
        if errors:
            feedback_text.color = ft.colors.RED_600
            feedback_text.value = "\n".join(errors)
            page.update()
            return
            
        # 2. Get the user's ID from the database
        user_id = get_user_id_by_username(name.value.strip())
        if not user_id:
            feedback_text.color = ft.colors.RED_600
            feedback_text.value = f"User '{name.value}' not found. Please use a registered username."
            page.update()
            return

        # 3. Call your function to log the request to the database
        success, message = log_request_to_db(
            requester_id=user_id,
            title=title.value.strip(),
            description=description.value.strip(),
            category=category.value,
            location=location.value.strip()
        )
        
        # 4. Display the result from the database operation
        feedback_text.value = message
        feedback_text.color = ft.colors.GREEN_700 if success else ft.colors.RED_600
        page.update()

    page.add(
        ft.Column(
            [
                ft.Text("Submit a Help Request", size=26, weight="bold"),
                ft.Text("Your request will be saved to the system history."),
                ft.Divider(height=15),
                name, title, description, category, location,
                ft.ElevatedButton("Log My Request", on_click=handle_submit, width=400, height=45, icon=ft.icons.HISTORY_EDU),
                feedback_text
            ],
            spacing=15,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )

if __name__ == "__main__":
    ft.app(target=main)