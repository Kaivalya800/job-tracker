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

company = input("Company: ")
role = input("Role: ")
status = input("Status: ")

new_app = {"company": company, "role": role, "status": status}
apps.append(new_app)

print("--- after adding yours ---")
for app in apps:
    print(app["company"], "-", app["role"], "-", app["status"])