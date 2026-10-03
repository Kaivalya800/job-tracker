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
for app in apps:
    print(app["company"], "-", app["status"])

print("--- interviews only ---")
for app in apps:
    if app["status"] == "interview":
        print(app["company"], "-", app["role"])

print("--- all apps ---")
for app in apps:
    print(app["company"], "-", app["status"])

company = input("Company: ")
role = input("Role: ")
status = input("Status: ")

new_app = {"company": company, "role": role, "status": status}
apps.append(new_app)
save_apps(apps)

print("--- after adding yours ---")
for app in apps:
    print(app["company"], "-", app["role"], "-", app["status"])