# scheduler/main.py
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.jobstores.memory import MemoryJobStore
from pytz import timezone
from scheduler.tasks import run_full_crawl_and_detect_changes

async def main():
    # Use Bangladesh Time (Asia/Dhaka)
    bd_tz = timezone("Asia/Dhaka")
    
    scheduler = AsyncIOScheduler(
        jobstores={"default": MemoryJobStore()},
        timezone=bd_tz
    )
    
    # Run daily at 2:00 AM Bangladesh Time
    scheduler.add_job(
        run_full_crawl_and_detect_changes,
        # CronTrigger(hour=2, minute=0, timezone=bd_tz),
        CronTrigger(minute="*", timezone=bd_tz),
        id="daily_crawl_bdt",
        replace_existing=True
    )
    
    scheduler.start()
    print("⏰ Scheduler started. Daily crawl at 02:00 AM .")

    try:
        while True:
            await asyncio.sleep(3600)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()

if __name__ == "__main__":
    asyncio.run(main())