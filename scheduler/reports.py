# scheduler/reports.py
import json
from datetime import datetime, timezone
from crawler.storage import db
import os

async def generate_daily_report():
    today = datetime.now(timezone.utc).date()
    start_of_day = datetime.combine(today, datetime.min.time(), tzinfo=timezone.utc)

    changes = await db.change_log.find(
        {"detected_at": {"$gte": start_of_day}}
    ).to_list(length=None)

    report = {
        "report_date": today.isoformat(),
        "total_changes": len(changes),
        "new_books": len([c for c in changes if c["change_type"] == "new"]),
        "updated_books": len([c for c in changes if c["change_type"] == "updated"]),
        "changes": changes
    }

    os.makedirs("reports", exist_ok=True)
    filename = f"reports/change_report_{today}.json"
    with open(filename, "w") as f:
        json.dump(report, f, indent=2, default=str)
    print(f"📄 Daily report saved: {filename}")