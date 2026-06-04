# DSA Study Tracker

A full-stack, data-driven study application designed to track Data Structures and Algorithms (DSA) progress, automate data entry via LeetCode's GraphQL API, and optimize learning using Machine Learning and Spaced Repetition algorithms.

##  The "Why"
Most LeetCode trackers only record *if* a problem was solved. This system tracks the **human element**—time spent, mental friction, and topic weaknesses—to act as an AI study coach rather than just a database.

## Core Architecture & Features

* **Automated LeetCode Sync (GraphQL):** Integrates directly with LeetCode's undocumented GraphQL API to fetch recent accepted submissions, parse difficulty and topic tags, and seamlessly merge them into the local database without duplication.
* **AI Smart Coach (Pandas):** An analytical engine that processes study session data to calculate a custom "Weakness Score." It identifies high-friction topics based on time spent vs. success rate to recommend targeted practice.
* **Spaced Repetition Engine (SM-2 Inspired):** Implements an active recall scheduling algorithm. Based on user feedback (e.g., "Needed Hints" vs. "Solved Smoothly"), the backend calculates dynamic `next_review_date` intervals to optimize memory retention.
* **Triage Queue:** A rapid-fire UI component that identifies synced problems missing study data and prompts the user to quickly log their performance metrics.
* **Rock-Solid Backend:** Built with FastAPI and Pydantic for strict data validation, paired with a fully relational SQLite database mapped via SQLAlchemy ORM.

## Tech Stack

**Frontend:**
* [Streamlit](https://streamlit.io/) (Pure Python UI generation)
* `requests` (Client-side API consumption)

**Backend:**
* [FastAPI](https://fastapi.tiangolo.com/) (High-performance API framework)
* [Pydantic](https://docs.pydantic.dev/) (Data validation and serialization)
* [Uvicorn](https://www.uvicorn.org/) (ASGI Web Server)

**Database & Data Science:**
* [SQLite](https://www.sqlite.org/) (Lightweight relational database)
* [SQLAlchemy](https://www.sqlalchemy.org/) (Python SQL Toolkit and ORM)
* [Pandas](https://pandas.pydata.org/) (Data manipulation and ML feature engineering)

---

## Local Setup & Installation

**1. Clone the repository and navigate to the directory:**

```
git clone https://github.com/yourusername/dsa-tracker.git
cd dsa-tracker

```

**2. Create and activate a virtual environment:**

```
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate

```

**3. Install dependencies:**

```bash
pip install fastapi uvicorn sqlalchemy pydantic streamlit requests pandas

```

**4. Run the Backend API (Terminal 1):**

```
uvicorn main:app --reload

```

The FastAPI server will start on `http://localhost:8000` and auto-generate the SQLite database.

**5. Run the Frontend Dashboard (Terminal 2):**

```bash
streamlit run app.py

```

The Streamlit dashboard will open in your browser at `http://localhost:8501`.

## Database Schema

The application utilizes a relational data model:

* **Problem Table:** Stores immutable problem data (`id`, `title`, `difficulty`, `topic`, `url`, `is_solved`, `next_review_date`).
* **Session Table:** Stores individual study attempts (`id`, `problem_id (FK)`, `duration_minutes`, `status`, `timestamp`).
* **Relationship:** One-to-Many (One Problem can have multiple Study Sessions).