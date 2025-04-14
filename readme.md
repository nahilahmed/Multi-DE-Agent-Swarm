
# Multi-Agent Data Engineering Swarm 🐝🚀

> Fully autonomous AI agents executing Python code within your environment to ingest, clean, and load messy data into Postgres.

---

## Demo

<!-- Drop your gif here -->
<p align="center">
  <img src="demo.gif" alt="AutoGen Multi-Agent Swarm Demo" width="700">
</p>

---

## What makes this cool?

→ Agents don't just chat — *they execute real code.*

→ Powered by Microsoft AutoGen's `LocalCommandLineCodeExecutor` → letting agents:
- Access your local environment
- Run Python scripts dynamically
- Handle pandas, SQLAlchemy, Postgres, file ops... like a real engineer would.

All happening in your current virtual environment.

---

## How does it work?

You simply say:
> *"Ingest messy_sales.csv into Postgres after cleaning it properly."*

→ That's it.

Behind the scenes, your agent swarm self-organizes into:

| Agent            | Role | Powers |
|-----------------|------|--------------------------------|
| FinderAgent      | Data explorer | Reads messy data, summarizes it |
| TransformerAgent | Data cleaner  | Handles nulls, type errors, formatting |
| LoaderAgent      | Data loader   | Pushes data into Postgres with ingestion_ts, fixes column names |

And they figure out everything else.  
Fully autonomous. No micro-managing.

---

## Tech Stack 🛠️

- Python 3.x
- AutoGen (Microsoft)
- pandas
- SQLAlchemy
- psycopg2
- PostgreSQL
- dotenv
- LocalCommandLineCodeExecutor (AutoGen Magic ✨)

---

## Project Structure

```
.
├── data/
│   ├── messy_sales.csv
│   ├── temp_clean_input.csv
│   └── final_clean.csv
│
├── agents/
│   ├── finder_agent.py
│   ├── transformer_agent.py
│   └── loader_agent.py
│
├── main.py
├── .env.example
├── requirements.txt
└── README.md
```

---

## Setup & Run locally

```bash
git clone https://github.com/nahilahmed/Multi-DE-Agent-Swarm.git
cd Multi-DE-Agent-Swarm

cp .env.example .env
# Fill your postgres creds in .env

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt

python main.py
```

---

## .env.example

```env
OPENAI_API_KEY=sk-...
POSTGRES_CONN_STR=postgresql+psycopg2://username:password@localhost:5432/db_name
```

---

## Credits & Inspiration

Big love to:
- Microsoft AutoGen → https://microsoft.github.io/autogen

---

*This is just the beginning of Multi-Agent Engineering Automation.*
