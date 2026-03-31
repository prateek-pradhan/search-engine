# Wikipedia Search Engine

A Django-based Wikipedia search engine using a custom inverted index with token-based ranking. Data is sourced from a 41GB MediaWiki XML dump, parsed and indexed into PostgreSQL.

## Architecture

Two Django apps under the `backend` project:

- **scraper** — Data ingestion. `WikiData` model (title, content, created_at). Management commands parse Wikipedia XML and populate the database.
- **search** — Search logic. `InvertedIndex` model stores `token -> {wiki_id: rank_score}` as JSON. Services handle token normalization and wiki markup cleaning. Views handle query parsing, index lookup, score accumulation, and ranked result display.

### Ranking

Title token matches score **10 points**, content token matches score **1 point**. Scores accumulate across query tokens per document, and results are returned in descending score order.

### Project Structure

```
backend/            # Django project settings, root URL config
scraper/
  management/commands/
    populatedata.py         # Streaming XML parser, batch inserts WikiData
    createinvertedindex.py  # Builds inverted index with rank scoring
  assets/
    wikipedia_dump.xml      # MediaWiki XML dump (gitignored, ~41GB)
    stopwords.txt           # Stopword list (available, not yet integrated)
search/
  models.py                 # InvertedIndex model
  services.py               # normalize_token(), clean_content()
  views.py                  # tokenized_query, get_wiki views
  templates/search_page.html
  urls.py
manage.py
pyproject.toml
```

## Getting Started

### Prerequisites

- Python 3.10
- [uv](https://docs.astral.sh/uv/) (package manager)
- PostgreSQL

### Database Setup

Create a PostgreSQL database and user for local development:

```sql
CREATE USER dev WITH PASSWORD 'dev';
CREATE DATABASE "search-engine" OWNER dev;
```

### Installation

```bash
# Install dependencies
uv sync

# Run migrations
python manage.py migrate
```

### Loading Data

1. Download a MediaWiki XML dump from [Wikimedia Downloads](https://dumps.wikimedia.org/) and place it at `scraper/assets/wikipedia_dump.xml`.
2. Populate the database (streams the file, batch inserts of 1000):

```bash
python manage.py populatedata
```

3. Build the inverted index:

```bash
python manage.py createinvertedindex
```

### Running the Server

```bash
python manage.py runserver
```

## URL Routes

| Route | Description |
|---|---|
| `GET /search/` | Search landing page |
| `GET /search/?query=<term>` | Tokenized search with ranked results |
| `GET /search/wiki/<id>/` | Wiki article detail page |
| `/admin/` | Django admin |

## Commands

```bash
python manage.py runserver             # Dev server
python manage.py migrate               # Run migrations
python manage.py populatedata          # Populate DB from XML dump
python manage.py createinvertedindex   # Build inverted index
python manage.py test                  # Run all tests
python manage.py test search           # Run search app tests
python manage.py test scraper          # Run scraper app tests
```

## Dependencies

Managed with [uv](https://docs.astral.sh/uv/). Key packages: Django, djangorestframework, psycopg2-binary, requests, beautifulsoup4.

## Known Limitations

- Stopwords file (`scraper/assets/stopwords.txt`) exists but is not yet integrated into tokenization
- Test files exist but have no test cases yet
