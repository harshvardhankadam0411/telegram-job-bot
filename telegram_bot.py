import logging
import feedparser
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")

  # <-- तुमचा token टाका

RSS_FEEDS = [
    # "https://pythonjobs.github.io/feed.xml",                  # Global Python Jobs
    # "https://weworkremotely.com/categories/remote-programming-jobs.rss",  # Remote developer jobs
    # "https://remoteok.com/remote-dev-jobs.rss",               # Remote developer
    # "https://stackoverflow.com/jobs/feed",                    # StackOverflow Jobs
    "https://himalayas.app/jobs/rss"                          # India-friendly remote jobs
    "https://www.freejobalert.com/feed/",                  # Govt Jobs
    "https://govtjobguru.in/feed/",                        # Govt Job Guru 
    # "https://www.sarkariresult.com/rss/sarkariresult.xml", # Sarkari Result RSS
    # "https://www.employment-news.net/rss.xml",             # Employment News
    # "https://www.maharashtrasarkarinaukri.com/feed/",      # Maharashtra Govt Jobs
    # "https://maharashtranokri.in/feed/",                   # Maharashtra Sarkari Naukri
    # "https://www.isro.gov.in/hi/news.xml",                 # ISRO News
    # "https://www.drdo.gov.in/drdo-news-rss",               # DRDO News
    # AI / Machine Learning
    "https://ai-jobs.net/rss/",
    "https://remoteok.com/remote-ai-jobs.rss",
    "https://weworkremotely.com/categories/remote-machine-learning-jobs.rss",
    "https://remotive.com/remote-jobs/rss?category=software-dev&search=machine+learning",

    # Data Science / Data Analyst
    "https://remotive.com/remote-jobs/rss?category=data",
    "https://www.datasciencejobshub.com/feed/",
    "https://dataanalystjobs.beehiiv.com/feed"
]

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ---------------- FETCH JOBS ----------------
def fetch_jobs():
    jobs = []

    for feed in RSS_FEEDS:
        try:
            data = feedparser.parse(feed)
            for entry in data.entries[:5]:  # प्रत्येक feed मधून 5 jobs
                jobs.append({
                    "title": entry.get("title", "No Title"),
                    "link": entry.get("link", "")
                })
        except:
            continue

    return jobs

# ---------------- TELEGRAM COMMANDS ----------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Hi Harsh! Type /jobs to get latest job openings.")

async def jobs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔍 Fetching jobs... Wait 2 seconds...")

    job_list = fetch_jobs()

    if not job_list:
        await update.message.reply_text("❌ No jobs found currently. Try again later.")
        return

    for job in job_list:
        text = f"💼 {job['title']}\n🔗 {job['link']}"
        await update.message.reply_text(text)

    await update.message.reply_text("✅ Job list delivered!")

# ---------------- MAIN ----------------
def main():
    if BOT_TOKEN == "PUT_YOUR_TOKEN_HERE":
        raise RuntimeError("Please set your BOT_TOKEN!")

    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("jobs", jobs))

    logger.info("Bot Started Successfully!")
    app.run_polling()

if __name__ == "__main__":
    main()