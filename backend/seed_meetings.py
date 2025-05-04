# seed_meetings.py
import os, random
from datetime import datetime, timedelta
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()
client = MongoClient(os.getenv("MONGO_URI"))
col = client.get_default_database().meetings   # collection “meetings”

titles = [
    "Kick‑off", "Sprint Review", "Brainstorm", "Workshop", "Town Hall",
    "Retrospective", "One‑on‑One", "Stand‑up", "Demo", "Planning",
    "Onboarding", "Q&A", "Strategy", "Design Sync", "Bug Bash",
    "Tech Talk", "Lunch & Learn", "OKR Check", "Budget Review", "Roadmap"
]
clubs  = ["AI Club", "Robotics", "Design Guild", "Product Circle", "MLP"]
rooms  = ["101", "123", "201", "234", "443", "550"]

def rand_date(month_offset: int):
    # start at Jan 1 2025 and add month_offset
    base = datetime(2025, 1, 1, 9, 0)
    day  = random.randint(0, 27)               # keep inside month
    hour = random.choice([9,11,13,15,17])
    return base + timedelta(days=30*month_offset + day, hours=hour)

docs = []
for i in range(20):
    start = rand_date(i % 8)                   # months Jan‑Aug
    dur   = random.randint(30, 120)            # minutes
    end   = start + timedelta(minutes=dur)

    invited  = random.randint(3, 12)
    accepted = random.randint(0, invited)

    docs.append({
        "title"      : titles[i % len(titles)],
        "club"       : random.choice(clubs),
        "room"       : random.choice(rooms),
        "start_time" : start,
        "end_time"   : end,
        "invited"    : invited,
        "accepted"   : accepted
    })

result = col.insert_many(docs)
print(f"Inserted {len(result.inserted_ids)} meetings.")