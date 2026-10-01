# Verification — Week 4 MovieLens Dashboard

This record separates the September 30, 2026 independent audit from earlier
agent-reported setup history. Results come from `data/movie_ratings.csv`;
the assignment supplies questions, not an official numerical answer key.
`check_numbers.py` uses pandas and `check_stdlib.py` uses a separate CSV loop
to reproduce the main quantities. Their output formats and extra diagnostics
differ, so compare corresponding values rather than a line-by-line diff.

The September 30 audit independently aggregated the CSV with the standard
library and exact fractional means, compared the current app's tables and
rankings, checked all 21 movie floors from 50 through 150 in steps of 5, and
exercised all four local controls. These were AI-agent actions, not a claim
that the student personally performed each check.

---

## 1. How it was run

The earlier log in commit `b861e54` reports the following setup and results.
The original generation conversation and server logs are unavailable; the
first-run history is reported, not authenticated. These WSL commands are
examples, not a transcript of student actions:

```
cd Week-04-Vibe-Coding-101/dashboard
uv run --with pandas --with streamlit --with plotly streamlit run app.py \
    --server.headless true --server.port 8501 \
    > streamlit.log 2>&1 &                              # background
curl -s -o /dev/null -w '%{http_code}' http://localhost:8501   ->  200
grep -Ein "warn|error|traceback|exception" streamlit.log        ->  none
```

- The server output goes to `streamlit.log` in this folder, so the grep runs
  against a file that lives with the code instead of somewhere outside the
  project. The command above regenerates it every run; it is a runtime
  artifact and is listed in `.gitignore`, so it is not committed.
- HTTP status: **200**
- Server log: clean, no traceback, no warnings (the first run did log five
  `use_container_width` deprecation warnings; that argument was replaced with
  `width="stretch"` and the server restarted from an empty log, according to
  the earlier record. This chronology was not reproduced in the audit).
- Streamlit 1.64.0, pandas 3.0.6, plotly 7.1.0 (what `uv run --with ...`
  resolved on 2026-09-26).
- `requirements.txt` declares a minimum of `streamlit>=1.51`, not an exact
  version pin. The documented 1.51 signature supports `width="stretch"`;
  the 1.50 signature lacks that argument. See
  [Streamlit 1.51](https://docs.streamlit.io/1.51.0/develop/api-reference/charts/st.plotly_chart)
  and [Streamlit 1.50](https://docs.streamlit.io/1.50.0/develop/api-reference/charts/st.plotly_chart).
- Screenshots `screenshots/01` … `screenshots/07` are retained from the earlier
  working tree. They were not recaptured after the latest caption correction.
- The September 30 audit inspected the existing localhost app. No application
  exception was observed while exercising its controls. These documentation
  corrections did not start or stop the server.
- The latest caption and documentation changes were reviewed as source diffs.
  No new runtime or numerical test run is claimed for the correction request.

## 2. Dataset-derived number checks

The table retains the earlier reports' corresponding script values. Its
comparison values were computed from the CSV, not supplied by the assignment.
The September 30 independent audit confirmed the app's chart aggregates and
movie-floor rankings.

| Quantity | Dataset-derived comparison value | pandas (`check_numbers.py`) | stdlib (`check_stdlib.py`) | Agree |
|---|---|---|---|---|
| rows | 100,000 | 100,000 | 100,000 | yes |
| unique user/movie pairs | 100,000 | 100,000 | 100,000 | yes |
| distinct movies | 1,682 | 1,682 | 1,682 | yes |
| distinct users | 943 | 943 | 943 | yes |
| genre tokens (incl. `unknown`) | 19 | 19 | 19 | yes |
| movies with 1/2/3/4/5/6 genres | 833/569/215/51/11/3 | same | same | yes |
| Drama / Comedy / Thriller / Action / Romance (distinct movies) | 725 / 505 / 251 / 251 / 247 | same | same | yes |
| Film-Noir mean (n) | 3.922 (1,733) | 3.922 (1,733) | 3.922 (1,733) | yes |
| War mean (n) | 3.816 (9,398) | 3.816 (9,398) | 3.816 (9,398) | yes |
| Drama mean (n) | 3.687 (39,895) | 3.687 (39,895) | 3.687 (39,895) | yes |
| lowest incl. unknown | unknown 3.200 (10), Fantasy 3.215 (1,352), Horror 3.290 (5,317) | same | same | yes |
| release-year points | 71 (1922–1998) | 71 (1922–1998) | 71 (1922–1998) | yes |
| blank release-year rows / movies | 30 / 5 | 30 / 5 | 30 / 5 | yes |
| qualifying movies at ≥50 / ≥150 | 603 / 203 | 603 / 203 | 603 / 203 | yes |
| Q4 top 5 at ≥50 | 4.491 / 4.466 / 4.466 / 4.457 / 4.448 | same | same | yes |
| Q4 top 5 at ≥150 | 4.466 / 4.457 / 4.445 / 4.388 / 4.386 | same | same | yes |
| thin release years (<30 ratings) | — | 1926:2, 1930:18, 1932:12, 1943:24 | same | yes |
| Q1 share-of-movies sum (1,680 known-genre movies) | — | 172.08% | 172.08% | yes |

**No disagreement in chart aggregates or movie-floor rankings.** This does
not authenticate the earlier build narrative.

The current aggregates live in one cached `build_tables()` function, with
widget filtering applied afterward. The latest correction changes caption
wording, not the aggregation logic. The September 30 browser audit confirmed
that a fresh page returns to defaults: sliders 100 / 1922–1998 / 50, 18 genres
selected, and "At 50 ratings: 603 movies qualify". It did not establish that
every earlier edit had been followed by a complete numerical rerun.

## 3. Seven chart decisions

Release-year semantics, distinct-movie counting, the movie floors, and sorted
category charts follow the assignment's questions and toolkit. Unknown-genre
exclusion, the genre sample floor, and the 30-rating year threshold are
disclosed implementation choices, not additional mandated traps.

**Decision 1 — release year vs rating year (required by Q3).**
Decision: Question 3 uses `year`. The `rating_year` column holds only 1997 and
1998, so plotting it would produce a two-point line answering a different question.
The 30 rows with a blank release year (5 movies, including the row literally
titled `unknown`) are dropped in `build_tables()` with
`df.dropna(subset=["year"])` and the drop is stated in the chart caption:
"30 rating rows (5 movies) have a blank release year and were dropped before
this chart." Missing-year rows remain eligible for the other questions.
Thin years are not smoothed over: years with under 30 ratings
(4 of the 71 shown: 1926 n=2, 1930 n=18, 1932 n=12, 1943 n=24) are drawn as
red x markers off the line and counted in the caption. The line itself only
joins years with 30+ ratings and breaks at years with no ratings (1923–25,
1927–29), so no straight segment implies data that isn't there.

**Decision 2 — bar instead of a many-slice pie (toolkit guidance).**
Decision: sorted horizontal bar chart for Question 1, descending. 19 genre
tokens do not belong in a pie. The chart carries an explicit sort order
(`yaxis categoryorder: total ascending` plus a pre-sorted frame) so nothing
falls back to alphabetical or pandas default order.

**Decision 3 — what "counted" means in Q1 (required by Q1).**
Decision: distinct movies per genre. A movie with three genre tags is counted
once under each tag, so one movie appears in up to 6 bars. This is explained
in the caption before the chart. Each percentage uses all 1,680 rated movies with a known
genre as its denominator. Across all 18 genres, shares total 172.08%; a
filtered selection can total less. The corrected caption explicitly qualifies
the total as applying to all genres. The current Q1 counts `movie_id` after
`drop_duplicates`, Q2 counts rating rows, and the two are computed in separate
blocks so they can't be confused.

**Decision 4 — the `unknown` genre (optional exclusion).**
Decision: excluded from Q1 and Q2, disclosed in both captions ("2 movies
tagged 'unknown' are excluded: 10 ratings, and unknown is not a genre" /
"'unknown' excluded: its 3.20 average rests on 10 ratings"). The exclusion is
a filter on `genre != "unknown"` in both tables, not a post-hoc crop of the
chart. Both `unknown`-tagged movies were checked to be tagged `unknown` alone
(`Good Morning (1971)` and the row titled `unknown`), so excluding on exact
match does not discard any known-genre tags. The assignment does not require
this exclusion; including unknown with a clear explanation is also defensible.

**Decision 5 — Q2 genre sample floor (optional extra control).**
Decision: a genre-level minimum-ratings slider, default 100, labelled in the
chart title ("Average rating by genre, sorted, minimum 100 ratings per genre")
and in the caption ("at least 100 ratings behind the average (18 of 18 genres
shown)"). Semantics: a genre must have at least N rating rows behind its mean.
Default 100 excludes nothing (smallest non-unknown genre is Documentary,
758 ratings), so the default view reproduces the full-data genre means. It
is a live control — moved to 10,000 in the browser it shows 7 of 18 genres
(screenshot `07-widget-q2-genre-floor-10000.png`). The 7 that survive are the
genres with at least 10,000 rating rows: Drama, Comedy, Action, Thriller,
Romance, Adventure, Sci-Fi. War (9,398 rows) is the first one out. The
assignment requires working widgets, but does not prescribe this genre floor.

**Decision 6 — Q4 movie floors and full-precision ranking (required by Q4).**
Decision: the floor is the number of rating rows for that movie. All 100,000
user/movie pairs are unique, so row count equals distinct raters — stated in
the caption. Sorting uses the unrounded mean descending, then rating count
descending, then title. Schindler's List (4.466442953, n=298) ranks above The
Wrong Trousers (4.466101695, n=118) because its actual mean is higher. Both
display as 4.466, but they are not tied; rating count does not decide this order.
The 80 shared values involving 181 movies in the old diagnostic are collisions
after rounding to three decimals, not exact ties. The independent audit found
26 exact-mean groups shared by multiple movies at the 50 floor. The pandas
report now labels its rounded-display diagnostic and prints the underlying
means for the 4.466 example. Both floors are shown: a slider from 50 to 150
drives the chart,
and a fixed side-by-side table answers "what changes" without touching the
slider — at 50 the list is Close Shave, Schindler's List, Wrong Trousers,
Casablanca, Wallace & Gromit; at 150 the three thinnest drop (112, 118, 67
ratings) and Shawshank, Rear Window and The Usual Suspects come in.

**Decision 7 — sorted category charts (toolkit guidance).**
Decision: Q1, Q2 and Q4 are all sorted explicitly before they hit the chart
and all three also set an explicit `categoryorder`, so neither pandas' default
order nor alphabetical order can leak in. Verified visually in screenshots
01, 02, 04: 725 → 505 → 251 → 251 → 247 in Q1, 3.922 down to 3.215 in Q2
(all 18 bars in frame),
4.491 down to 4.448 in Q4.

## 4. Widget checks (AI-agent actions in the September 30 browser audit)

| Widget | Action | Observed result | Evidence |
|---|---|---|---|
| Q4 rating floor | slider 50 → 150 | caption "At 150 ratings: 203 movies qualify", title "Top 5 movies with at least 150 ratings", bars become Schindler's List 4.466, Casablanca 4.457, Shawshank 4.445, Rear Window 4.388, Usual Suspects 4.386 | `06-widget-q4-floor-150.png` |
| Q2 genre floor | slider 100 → 10,000 | caption "at least 10,000 ratings behind the average (7 of 18 genres shown)", 7 bars remain (Drama, Romance, Sci-Fi, Thriller, Adventure, Action, Comedy) | `07-widget-q2-genre-floor-10000.png` |
| genre multiselect | removed Drama while the genre floor was 10,000 | the 725 bar left Q1; Q2 showed 6 of 18 genres | read back from the live page |
| genre multiselect | cleared all genres | explanatory messages appeared, with empty chart axes still rendered; no application exception | read back from the live page |
| Q3 year range | narrowed to 1998, then on a fresh page to 1922 | single-year values approximately 3.297297 and 3.555556 | read back from the live page |

Four widgets, assignment asked for at least one or two. Existing screenshots
are earlier visual records, not evidence that the student personally drove
the controls. At the default range, all 71 populated-year means are represented
as 67 ordinary points plus four red crosses, not one continuous 71-point line.

## 5. Chart type against the assignment's toolkit

| Question | Chart used | Why (against the toolkit table) |
|---|---|---|
| Q1 genre breakdown | horizontal bar, sorted desc | many categories and long labels; the current chart follows the toolkit warning against a many-slice pie, without claiming an authenticated first-attempt history |
| Q2 genre satisfaction | horizontal bar, sorted desc, values and n on the bars | comparing averages across categories; sorting is asked for explicitly |
| Q3 ratings over time | line with markers, thin-sample points overlaid as red x | trend over time; the toolkit's warning is confusing year released with year rated, avoided and disclosed |
| Q4 top movies with a floor | horizontal bar of the top 5, plus a two-column comparison table | comparing 5 categories with long titles; the floor change is a comparison, so it gets its own side-by-side view |

## 6. Scope checks

- Four charts, one per required question, questions not substituted.
- No embedded write-up or audit section in the app — methodology lives in
  short chart captions, the audit lives in this file.
- `data/movie_ratings.csv` is a copy (10,878,734 bytes) of the class dataset;
  the original under `/mnt/d/projects/ds-dev-fall-2026` was read only.
- No push, pull request, or Streamlit deployment was performed during this
  audit or correction request. The repository has local commit `b861e54` plus
  uncommitted dashboard changes. Its `origin` is `CUNYTechPrep/ds-dev-fall-2026`,
  the class repository. Deployment needs the student's own public repository.
- Deployment and submission remain: publish on Streamlit Community Cloud,
  check the URL in an Incognito/Private window, and submit the public URL in
  the Week 4 HW Submission Sheet. README.md records the entrypoint choices.

## 7. Known limits

- The Q2 floor is on genres, not on individual movies. Averages over movies
  with very few ratings still enter a genre's mean; the control says which
  genres are too thin to rank, not which movies are.
- Q3's thin-sample threshold is 30 ratings, an implementation choice, not one
  the assignment specified. It is labelled wherever it appears.
- The Q1 percentage denominator is the 1,680 rated movies that carry a real
  genre label, so it excludes the 2 `unknown`-tagged movies on top of the
  disclosure above. Filtering genres does not change that denominator.
- Empty genre selections display explanatory messages alongside empty charts.
- The original generation conversations remain unavailable. BUILD_LOG.md uses
  two actual requests from the audit/correction phase, with the previous draft
  preserved separately and labeled unverified.
