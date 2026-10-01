# CUNY Tech Prep (CTP) — Week 4, Vibe Coding 101: MovieLens Dashboard

A Streamlit dashboard over the MovieLens ratings file
(100,000 ratings, 943 users, 1,682 movies) that answers the four questions
from the Week 4 assignment with one chart each:

1. Genre breakdown — sorted horizontal bar, distinct movies per genre
2. Genre satisfaction — sorted horizontal bar, mean rating per genre with a
   minimum-ratings floor
3. Ratings over time — line chart by **release year** (not rating year)
4. Best movies with a floor — top 5 at 50+ ratings, slider up to 150, plus a
   side-by-side comparison of both floors

## Run it

```
uv run --with pandas --with streamlit --with plotly streamlit run app.py
```

or, with a plain environment:

```
pip install -r requirements.txt
streamlit run app.py
```

Then open http://localhost:8501. `app.py` reads `data/movie_ratings.csv`
relative to its own file, so run it from this folder.

## Files

| File | What it is |
|---|---|
| `app.py` | the dashboard |
| `data/movie_ratings.csv` | the dataset, copied in |
| `requirements.txt` | streamlit, pandas, plotly |
| `BUILD_LOG.md` | two actual audit/correction requests, AI results, and decisions |
| `verification.md` | dataset checks, chart decisions, and verification history |
| `check_numbers.py` | number checks with pandas |
| `check_stdlib.py` | the same checks with the standard library only |
| `screenshots/` | the app running, and the widgets being driven |
| `notes/BUILD_LOG.before-corrections.md` | preserved earlier draft, explicitly unverified |

## Decisions worth knowing

- **Counted movies, not ratings, for the genre breakdown.** A movie with three
  genre tags counts once in each, so shares across all 18 genres add to about 172%.
  Said on the chart, not buried here.
- **`unknown` is excluded from both genre charts.** 2 movies, 10 ratings, and
  its 3.20 average would rank last on a sample that small.
- **Release year, not rating year,** for the time chart. `rating_year` only
  has 1997 and 1998. 30 rows with no release year are dropped and disclosed,
  and years with under 30 ratings are marked off the line instead of being
  joined into the trend.
- **Question 2 has a floor slider** (default 100 ratings per genre) to disclose
  and filter the number of ratings behind each genre mean. This is an optional
  control; at the default, all 18 known genres remain visible.
- **Question 4 sorts by the unrounded mean, then rating count, then title.**
  Schindler's List (4.466442953) ranks above The Wrong Trousers (4.466101695)
  because its actual mean is higher. Both display as 4.466; that rounding is
  not an exact tie. Rating count and title only resolve equal actual means.

`verification.md` records the independent dataset audit. `BUILD_LOG.md` uses
actual requests from the audit/correction conversation and identifies gaps in
the original generation history; it does not reconstruct earlier prompts.

## Deploy and submit

1. Create your own public GitHub repository and commit the dashboard files,
   including `requirements.txt` and `data/movie_ratings.csv`. The existing
   course-repository remote is not the deployment destination.
2. In Streamlit Community Cloud, select your repository, `main`, and `app.py`
   if these files are at the repository root. If you keep the entire course
   repository structure, use `Week-04-Vibe-Coding-101/dashboard/app.py` instead.
   Use Python 3.12 to match the audited local environment.
3. Open the deployed URL in an Incognito/Private window. Check all four charts
   and controls, including 603 qualifying movies at 50 ratings and 203 at 150.
4. Submit the public Streamlit URL in the Week 4 HW Submission Sheet. The
   dashboard assignment does not require a dashboard-code PR to the class repo.

See the [Streamlit deployment instructions](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy).
