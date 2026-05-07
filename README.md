# Stockholms Puls 🎭
A multi-page interactive dashboard for exploring live events across Stockholm and Sweden — built with **Streamlit**, **Plotly**, **Pandas** and **DuckDB**.
Browse concerts, theatre shows, nightlife, sports, and more. Filter by date, segment, event name, or venue. View event images, buy tickets, and locate venues on a live map.
---
## Features
- **KPI cards** — total events, on-sale count, upcoming events, unique venues, and a per-segment breakdown at a glance
- **Interactive charts** — pie charts for segment and genre share, a trend line with value markers for monthly activity, and a colour-coded horizontal bar for top venues (🟢 highest · 🔵 middle · 🔴 lowest)
- **Four filters** — date range, segment, event name search, and venue
- **Event cards** — each filtered result shows the event image, date, venue, category, status badge, and a direct link to buy tickets or learn more
- **Venue map** — every filtered event plotted on an interactive map using latitude and longitude
- **Raw data page** — full sortable table of all 1 200+ events

---

## Folder structure

```
streamlit_test_dennis/
│
├── pyproject.toml              # project config and dependencies
├── uv.lock                     
├── README.md                   
│
└── src/
    └── events/
        ├── app.py              # entry point — defines the 3-page navigation
        ├── __init__.py
        │
        ├── assets/
        │   ├── data/
        │   │   └── events_combined.csv   # the data
            │   ├── image/                    # home page banner image
            │   ├── markdown/
            │   │   ├── intro_events.md       # home page intro text
            │   │   └── dashboard_description.md
            │   └── style/
            │       └── dashboard.css         # custom styles (metric cards, buttons)
            │
            ├── pages/
            │   ├── home.py         # Home page — banner image + project description
            │   ├── dashboard.py    # Dashboard page — charts, filters, cards, map
            │   └── raw_data.py     # Raw Data page — full scrollable data table
            │
            ├── components/
            │   ├── kpis.py         # metric card functions (one per KPI)
            │   ├── charts.py       # all Plotly chart functions
            │   └── filters.py      # all filter widget functions
            │
            └── utils/
                ├── constants.py    # file path constants (DATA_PATH, MARKDOWN_PATH …)
                └── helpers.py      # read_textfile, read_css, get_events_df
```
       
    

    
--- 
## Prerequisites

       
- **Python 3.12 or newer**
- **uv** — a fast Python package and project manager
       
Install `uv` if you do not have it yet:

    
```bash  

```

---

## Installation and running
    
**1. Navigate to the project folder**
    
```bash
cd streamlit_test_dennis
```

**2. Install all dependencies**

```bash
uv sync
```
This reads `pyproject.toml`, creates a virtual environment automatically, and installs Streamlit, Plotly, and DuckDB. You only need to do this once (or again after adding new packages).

**3. Launch the dashboard**
```bash
uv run streamlit run src/events/app.py
```

Streamlit will print a local URL — open it in your browser:

```
Local URL:  http://localhost:8501
```
Press `Ctrl + C` in the terminal to stop the server.

---

## How to use the dashboard
### Home page
A welcome page with a banner image and an overview of the dataset — what it covers, where the data comes from, and what you can explore.

### Dashboard page
The main analytics page. Scroll down through the sections:

| Section | What it shows |
|---|---|
| **Segment KPIs** | Event count for each of the 5 segments |
| **Overview KPIs** | Total events, on-sale, upcoming, and unique venues |
| **Segment pie chart** | Proportional share of events across segments |
| **Monthly trend line** | Events per month from January to December, with a value label at every data point |
| **Genre pie + Venues bar** | Genre share (top 8) and top 8 venues by event count, colour-coded |
| **Breakdown tables** | Value counts for status, day of week, source, and segment |
| **Explore Events** | Four filters + event cards with images and ticket links + live venue map |
#### Using the four filters
| Filter | How it works |
|---|---|
| **Date range** | Pick a start and end date — only events within that window appear |
| **Segment** | Choose a category (e.g. Music) or leave on *All* |
| **Search event name** | Type any keyword to match against event titles (case-insensitive) |
| **Venue** | Pick a specific venue or leave on *All* |

All four filters work together and update the event cards and map instantly.

#### Event cards
Each card shows the event poster image, full date and time, venue and city, category, status badge, and a **Get Tickets /
More Info** button that opens the original event page.

#### Venue map
All filtered venues are plotted on an interactive map. Zoom, pan, and hover to explore the locations.

### Raw Data page
A full interactive table of every event in the dataset. Click any column header to sort ascending or descending.
---

## Dependencies

| Package | Purpose |
|---|---|
| `streamlit` | Web framework — builds the entire UI |
| `plotly` | Interactive charts (pie, line, bar) |
| `duckdb` | SQL queries run directly on Pandas DataFrames |
| `pandas` | Data loading and manipulation (installed automatically with Streamlit) |

---

## Data sources

Events are sourced from public listings on:

- [Ticketmaster Sweden](https://www.ticketmaster.se)
- [Visit Stockholm](https://www.visitstockholm.com)
- [Fasching](https://www.fasching.se)
- [Berns](https://www.berns.se)

---
*Built by Dennis Chinecherem(Data engineer), and Mossad Hagos(Data engineer)*