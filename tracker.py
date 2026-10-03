import json
import os

FILENAME = "apps.json"

def load_apps():
    if os.path.exists(FILENAME):
        with open(FILENAME, "r") as f:
            return json.load(f)
    return []

def save_apps(apps):
    with open(FILENAME, "w") as f:
        json.dump(apps, f, indent=2)

apps = load_apps()

while True:
    print("\n1. Add application")
    print("2. View all")
    print("3. Filter by status")
    print("4. Quit")
    choice = input("Choose: ")

    if choice == "1":
        company = input("Company: ")
        role = input("Role: ")
        status = input("Status: ")
        date_applied = input("Date applied (YYYY-MM-DD): ")
        referral = input("Referral (or leave blank): ")
        link = input("Link: ")
        apps.append({"company": company,
                      "role": role,
                      "status": status,
                      "date_applied": date_applied,
                      "referral": referral,
                      "link": link
        })
        save_apps(apps)
        print("Saved!")

    elif choice == "2":
        for app in apps:
            print(
                app["company"], "-",
                app["role"], "-",
                app["status"], "-",
                app.get("date_applied", "no date"), "-",
                app.get("referral", "none") or "none", "-",
                app.get("link", "no link")
            )

    elif choice == "3":
        wanted = input("Which status? ")
        found = False
        for app in apps:
            if app["status"].lower() == wanted.lower():
                print(app["company"], "-", app["role"])
                found = True
        if not found:
            print("No applications with that status.")
            
    elif choice == "4":
        break

    else:
        print("Invalid choice, try again.")