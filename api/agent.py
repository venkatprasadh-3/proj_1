import os
import requests
import json
import sqlite3
from datetime import datetime
from openai import OpenAI

AIPROXY_TOKEN = os.getenv("AIPROXY_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def process_task(task):
    if "install uv" in task:
        return install_uv_and_run_datagen()
    elif "format markdown" in task:
        return format_markdown()
    elif "count wednesdays" in task:
        return count_wednesdays()
    elif "sort contacts" in task:
        return sort_contacts()
    elif "get recent logs" in task:
        return get_recent_logs()
    elif "extract email" in task:
        return extract_email()
    elif "total sales of gold" in task:
        return calculate_gold_sales()
    else:
        raise ValueError("Unsupported task")

def install_uv_and_run_datagen():
    os.system("pip install uv")
    os.system(f"python3 -m uv https://raw.githubusercontent.com/sanand0/tools-in-data-science-public/tds-2025-01/project-1/datagen.py {os.getenv('USER_EMAIL')}")
    return "Data generation complete"

def format_markdown():
    os.system("npx prettier --write /data/format.md")
    return "Markdown formatted"

def count_wednesdays():
    with open("/data/dates.txt", "r") as f:
        dates = [line.strip() for line in f.readlines()]
    count = sum(1 for date in dates if datetime.strptime(date, "%Y-%m-%d").weekday() == 2)
    with open("/data/dates-wednesdays.txt", "w") as f:
        f.write(str(count))
    return f"Counted {count} Wednesdays"

def sort_contacts():
    with open("/data/contacts.json", "r") as f:
        contacts = json.load(f)
    sorted_contacts = sorted(contacts, key=lambda x: (x["last_name"], x["first_name"]))
    with open("/data/contacts-sorted.json", "w") as f:
        json.dump(sorted_contacts, f, indent=4)
    return "Contacts sorted"

def get_recent_logs():
    logs = sorted([f for f in os.listdir("/data/logs") if f.endswith(".log")], key=os.path.getmtime, reverse=True)[:10]
    with open("/data/logs-recent.txt", "w") as f:
        for log in logs:
            with open(f"/data/logs/{log}", "r") as log_file:
                f.write(log_file.readline())
    return "Recent logs saved"

def extract_email():
    with open("/data/email.txt", "r") as f:
        email_content = f.read()
    response = OpenAI().ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": "Extract the sender’s email address"}, {"role": "user", "content": email_content}],
        api_key=OPENAI_API_KEY
    )
    email_address = response["choices"][0]["message"]["content"].strip()
    with open("/data/email-sender.txt", "w") as f:
        f.write(email_address)
    return f"Extracted email: {email_address}"

def calculate_gold_sales():
    conn = sqlite3.connect("/data/ticket-sales.db")
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(units * price) FROM tickets WHERE type='Gold'")
    total_sales = cursor.fetchone()[0]
    with open("/data/ticket-sales-gold.txt", "w") as f:
        f.write(str(total_sales))
    conn.close()
    return f"Total Gold ticket sales: {total_sales}"

def read_file(path):
    try:
        with open(path, "r") as f:
            return f.read()
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")
