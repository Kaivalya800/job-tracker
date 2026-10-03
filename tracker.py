apps = [
    {"company": "Google", "role": "SWE Intern", "status": "applied"},
    {"company": "Stripe", "role": "PM Intern", "status": "rejected"},
    {"company": "Facebook", "role": "SWE Intern", "status": "interview"}
]

for app in apps:
    print(app["company"], "-", app["status"])

print("--- interviews only ---")
for app in apps:
    if app["status"] == "interview":
        print(app["company"], "-", app["role"])

new_app = {"company": "Amazon", "role": "SWE Intern", "status": "applied"}
apps.append(new_app)

print("--- all apps ---")
for app in apps:
    print(app["company"], "-", app["status"])