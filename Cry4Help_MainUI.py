import flet as ft
import sqlite3

DB_PATH = "cry4help.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            email TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS user_activity (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT,
            action TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# --- Log Activity ---
def log_activity(email, action):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("INSERT INTO user_activity (email, action) VALUES (?, ?)", (email, action))
    conn.commit()
    conn.close()

session = {"is_logged_in": False, "user_email": None}

def main(page: ft.Page):
    init_db()

    page.title = "Cry4Help - Community Skill Sharing"
    page.window_width = 800
    page.window_height = 600
    page.bgcolor = ft.Colors.GREY_100

    def show_snack(message, color):
        page.snack_bar = ft.SnackBar(content=ft.Text(message), bgcolor=color)
        page.snack_bar.open = True
        page.update()

    # --- Welcome View ---
    def welcome_view():
        return ft.View(
            "/",
            controls=[
                ft.Column([
                    ft.Text("Welcome to Cry4Help", size=30, weight="bold", color=ft.Colors.BLUE),
                    ft.ElevatedButton("Login", on_click=lambda _: page.go("/login")),
                    ft.ElevatedButton("Register", on_click=lambda _: page.go("/register")),
                ], horizontal_alignment="center", spacing=20)
            ],
            vertical_alignment="center",
            horizontal_alignment="center",
            padding=20
        )

    # --- Registration View ---
    def registration_view():
        email = ft.TextField(label="Email", width=300)
        password = ft.TextField(label="Password", password=True, width=300)
        message = ft.Text("")

        def register_clicked(e):
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            cur.execute("SELECT * FROM users WHERE email=?", (email.value,))
            if cur.fetchone():
                message.value = "Email already registered."
                message.color = ft.Colors.RED
            else:
                cur.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email.value, password.value))
                conn.commit()
                session["is_logged_in"] = True
                session["user_email"] = email.value
                log_activity(email.value, "Registered")
                message.value = "Registered and logged in successfully!"
                message.color = ft.Colors.GREEN
                show_snack("Welcome, you are now logged in!", ft.Colors.GREEN)
                page.go("/main")
            conn.close()
            page.update()

        return ft.View(
            "/register",
            controls=[
                ft.Column([
                    ft.Text("Register", size=25, weight="bold", color=ft.Colors.BLUE_900),
                    email,
                    password,
                    ft.ElevatedButton("Register", on_click=register_clicked),
                    message,
                    ft.TextButton("Back to Home", on_click=lambda _: page.go("/"))
                ], spacing=20, horizontal_alignment="center")
            ],
            vertical_alignment="center",
            horizontal_alignment="center"
        )

    # --- Login View ---
    def login_view():
        email = ft.TextField(label="Email", width=300)
        password = ft.TextField(label="Password", password=True, width=300)
        message = ft.Text("")

        def login_clicked(e):
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            cur.execute("SELECT * FROM users WHERE email=? AND password=?", (email.value, password.value))
            result = cur.fetchone()
            conn.close()
            if result:
                session["is_logged_in"] = True
                session["user_email"] = email.value
                log_activity(email.value, "Logged In")
                message.value = "Login successful!"
                message.color = ft.Colors.GREEN
                show_snack("Welcome back!", ft.Colors.GREEN)
                page.go("/main")
            else:
                message.value = "Invalid credentials."
                message.color = ft.Colors.RED
            page.update()

        return ft.View(
            "/login",
            controls=[
                ft.Column([
                    ft.Text("Login", size=25, weight="bold", color=ft.Colors.BLUE_900),
                    email,
                    password,
                    ft.ElevatedButton("Login", on_click=login_clicked),
                    message,
                    ft.TextButton("Back to Home", on_click=lambda _: page.go("/"))
                ], spacing=20, horizontal_alignment="center")
            ],
            vertical_alignment="center",
            horizontal_alignment="center"
        )

    # --- Main View with UC Tabs ---
    def main_view():
        if not session["is_logged_in"]:
            return ft.View(
                "/main",
                controls=[
                    ft.Text("Unauthorized. Please login or register first.", color=ft.Colors.RED),
                    ft.ElevatedButton("Go to Login", on_click=lambda _: page.go("/login"))
                ]
            )

        def logout_click(e):
            log_activity(session["user_email"], "Logged Out")
            session["is_logged_in"] = False
            session["user_email"] = None
            show_snack("Logged out successfully.", ft.Colors.BLUE)
            page.go("/")

        tabs = ft.Tabs(
            selected_index=0,
            animation_duration=200,
            expand=1,
            tabs=[
                ft.Tab(
                    text="UC1 - RegistrationUI",
                    icon=ft.Icons.PERSON_ADD,
                    content=ft.Text("UC1_1 Registration UI Placeholder")
                ),
                ft.Tab(
                    text="UC2 - LoginUI",
                    icon=ft.Icons.LOGIN,
                    content=ft.Text("UC2_1 Login UI Placeholder")
                ),
                ft.Tab(
                    text="UC3 - Request Help",
                    icon=ft.Icons.HELP,
                    content=ft.Text("UC3 Request Help Placeholder")
                ),
                ft.Tab(
                    text="UC4 - Matchmaking",
                    icon=ft.Icons.GROUP,
                    content=ft.Text("UC4 Matchmaking Placeholder")
                ),
                ft.Tab(
                    text="UC5 - Match Results",
                    icon=ft.Icons.CHECK,
                    content=ft.Text("UC5 Match Results Placeholder")
                ),
                ft.Tab(
                    text="UC6 - Match History",
                    icon=ft.Icons.HISTORY,
                    content=ft.Text("UC6 Match History Placeholder")
                ),
            ]
        )

        return ft.View(
            "/main",
            controls=[
                ft.Column([
                    ft.Text(f"Welcome, {session['user_email']}!", size=22, weight="bold", color=ft.Colors.GREEN),
                    tabs,
                    ft.ElevatedButton("Logout", on_click=logout_click, bgcolor=ft.Colors.BLUE, color=ft.Colors.WHITE)
                ], spacing=20, expand=True)
            ]
        )

    def route_change(e):
        page.views.clear()
        routes = {
            "/": welcome_view,
            "/login": login_view,
            "/register": registration_view,
            "/main": main_view
        }
        page.views.append(routes.get(page.route, welcome_view)())
        page.update()

    page.on_route_change = route_change
    page.go("/")

ft.app(target=main)
