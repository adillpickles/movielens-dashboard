"""MovieLens dashboard — CUNY Tech Prep, Week 4 "Vibe Coding 101".

Answers the four assignment questions with one chart each. Every analytical
choice (multi-genre counting, the unknown genre, the rating floors, release
year vs rating year) is documented in verification.md.

Run:  streamlit run app.py
"""

from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="MovieLens Ratings", layout="wide")

DATA = Path(__file__).resolve().parent / "data" / "movie_ratings.csv"
UNKNOWN = "unknown"
THIN_SAMPLE = 30  # years with fewer ratings than this get flagged in Q3


# ---------------------------------------------------------------- data layer
@st.cache_data
def load_ratings(path: str) -> pd.DataFrame:
    return pd.read_csv(path)


@st.cache_data
def build_tables(df: pd.DataFrame) -> dict:
    """Everything the four charts need, computed once."""
    # Q1 - distinct movies carrying each genre. Movies are counted once per
    # genre tag they carry, so a 3-genre movie shows up under all three.
    movie_genres = df[["movie_id", "genres"]].drop_duplicates("movie_id")
    movies_exploded = movie_genres.assign(
        genre=movie_genres["genres"].str.split("|")
    ).explode("genre")
    known = movies_exploded[movies_exploded["genre"] != UNKNOWN]
    q1 = known["genre"].value_counts().rename_axis("genre").reset_index(name="movies")
    q1["pct"] = 100 * q1["movies"] / known["movie_id"].nunique()

    # Q2 - mean rating per genre over rating rows (a rating row enters every
    # genre its movie carries), unknown left out.
    ratings_exploded = df.assign(genre=df["genres"].str.split("|")).explode("genre")
    ratings_exploded = ratings_exploded[ratings_exploded["genre"] != UNKNOWN]
    q2 = (
        ratings_exploded.groupby("genre")["rating"]
        .agg(mean="mean", n="size")
        .reset_index()
        .rename(columns={"mean": "mean_rating", "n": "ratings"})
    )

    # Q3 - mean rating by RELEASE year. Blank release years are dropped here
    # on purpose: 30 rating rows across 5 movies have no year at all.
    rated = df.dropna(subset=["year"]).copy()
    rated["year"] = rated["year"].astype(int)
    q3 = (
        rated.groupby("year")["rating"]
        .agg(mean="mean", n="size")
        .reset_index()
        .rename(columns={"mean": "mean_rating", "n": "ratings"})
    )
    q3["thin"] = q3["ratings"] < THIN_SAMPLE

    # Q4 - per movie mean and rating count, for the floor filter.
    q4 = (
        df.groupby(["movie_id", "title"])
        .agg(mean_rating=("rating", "mean"), ratings=("rating", "size"))
        .reset_index()
    )

    return {
        "q1": q1,
        "q2": q2,
        "q3": q3,
        "q4": q4,
        "dropped_year_rows": int(df["year"].isna().sum()),
        "dropped_year_movies": int(df.loc[df["year"].isna(), "movie_id"].nunique()),
    }


def top_movies(q4: pd.DataFrame, floor: int, k: int = 5) -> pd.DataFrame:
    """Top k by mean, ties broken by rating count then title."""
    qualifying = q4[q4["ratings"] >= floor]
    return (
        qualifying.sort_values(
            ["mean_rating", "ratings", "title"], ascending=[False, False, True]
        )
        .head(k)
        .reset_index(drop=True)
    )


# ------------------------------------------------------------------ widgets
df = load_ratings(str(DATA))
tables = build_tables(df)

st.title("MovieLens: who watched what, and what did they think?")
st.caption(
    "100,000 ratings from 943 users on 1,682 movies. Four questions, four charts. "
    "The controls on the left change what each chart shows."
)

with st.sidebar:
    st.header("Controls")
    genre_options = list(tables["q1"]["genre"])
    picked_genres = st.multiselect(
        "Genres to include (Questions 1 and 2)",
        options=genre_options,
        default=genre_options,
        help="The 2 movies tagged 'unknown' are left out of both genre charts.",
    )
    min_ratings_genre = st.slider(
        "Minimum ratings behind a genre (Question 2)",
        min_value=100,
        max_value=10000,
        value=100,
        step=100,
        help="A genre average built on 10 ratings and one built on 39,895 are "
        "not the same kind of number. At the default of 100 every genre passes.",
    )
    year_lo, year_hi = st.slider(
        "Release year range (Question 3)",
        min_value=1922,
        max_value=1998,
        value=(1922, 1998),
        step=1,
    )
    movie_floor = st.slider(
        "Minimum ratings per movie (Question 4)",
        min_value=50,
        max_value=150,
        value=50,
        step=5,
        help="Assignment asks for at least 50. Slide to 150 to see what changes.",
    )

# ---------------------------------------------------------------- question 1
st.header("Question 1 — Genre breakdown: which genres do the rated movies carry?")
q1 = tables["q1"]
q1_sel = q1[q1["genre"].isin(picked_genres)].sort_values("movies", ascending=True)
known_movies = int(df.loc[df["genres"] != UNKNOWN, "movie_id"].nunique())

st.caption(
    f"How this was counted: distinct movies, not ratings. A movie with three genre tags "
    f"is counted once under each of its tags. Each percentage uses all "
    f"{known_movies:,} rated movies with a known genre as its denominator. "
    f"Across all {len(q1)} genres, the shares add up to "
    f"about {q1['pct'].sum():.0f}% because a movie can carry up to 6 genres. "
    "Selecting fewer genres changes the bars shown, not that denominator. "
    "2 movies tagged 'unknown' are excluded: 10 ratings, and unknown is not a genre."
)
if q1_sel.empty:
    st.info("No genres selected — pick at least one in the sidebar.")
fig1 = px.bar(
    q1_sel,
    x="movies",
    y="genre",
    orientation="h",
    text=q1_sel.apply(lambda r: f"{r['movies']}  ({r['pct']:.1f}%)", axis=1)
    if len(q1_sel)
    else None,
    labels={"movies": "distinct movies rated", "genre": "genre"},
    title="Distinct rated movies per genre (sorted, highest first)",
)
fig1.update_traces(marker_color="#4C78A8", textposition="outside", cliponaxis=False)
fig1.update_layout(
    yaxis={"categoryorder": "total ascending"},
    xaxis_range=[0, q1_sel["movies"].max() * 1.2] if len(q1_sel) else None,
    height=560,
    bargap=0.25,
)
st.plotly_chart(fig1, width="stretch")

# ---------------------------------------------------------------- question 2
st.header("Question 2 — Genre satisfaction: which genres rate highest and lowest?")
q2 = tables["q2"]
q2_sel = q2[
    q2["genre"].isin(picked_genres) & (q2["ratings"] >= min_ratings_genre)
].sort_values("mean_rating", ascending=True)

st.caption(
    f"Mean rating per genre over rating rows, sorted. Genre floor: at least "
    f"{min_ratings_genre:,} ratings behind the average "
    f"({len(q2_sel)} of {len(q2)} genres shown). "
    "'unknown' excluded: its 3.20 average rests on 10 ratings and would rank last "
    "on a sample that small."
)
if q2_sel.empty:
    st.info("No genre passes the current selection and floor — add genres or lower the floor.")
fig2 = px.bar(
    q2_sel,
    x="mean_rating",
    y="genre",
    orientation="h",
    text=q2_sel.apply(lambda r: f"{r['mean_rating']:.3f}  (n={r['ratings']:,})", axis=1),
    labels={"mean_rating": "mean rating (1-5)", "genre": "genre"},
    title=f"Average rating by genre, sorted, minimum {min_ratings_genre:,} ratings per genre",
)
fig2.update_traces(marker_color="#F58518", textposition="outside", cliponaxis=False)
fig2.update_layout(
    yaxis={"categoryorder": "total ascending"},
    xaxis_range=[0, 5],
    margin={"r": 140},
    height=max(420, 34 * len(q2_sel) + 160),
    bargap=0.25,
)
st.plotly_chart(fig2, width="stretch")

# ---------------------------------------------------------------- question 3
st.header("Question 3 — Ratings over time: has the mean rating drifted by release year?")
q3 = tables["q3"]
q3_sel = q3[(q3["year"] >= year_lo) & (q3["year"] <= year_hi)].sort_values("year")
thin = q3_sel[q3_sel["thin"]]

st.caption(
    f"Release year, not rating year — the file's rating_year column only has 1997 and "
    f"1998, which would give a two-point line. {tables['dropped_year_rows']} rating rows "
    f"({tables['dropped_year_movies']} movies) have a blank release year and were dropped "
    f"before this chart. Years with fewer than {THIN_SAMPLE} ratings are shown as a red x "
    f"off the line instead of being joined into the trend — {len(thin)} of the "
    f"{len(q3_sel)} years shown."
)
# Reindex over every year in range so years with no ratings (and thin years)
# become gaps in the line instead of being bridged by a straight segment.
q3_line = (
    q3_sel[~q3_sel["thin"]]
    .set_index("year")
    .reindex(range(year_lo, year_hi + 1))
    .rename_axis("year")
    .reset_index()
)
fig3 = px.line(
    q3_line,
    x="year",
    y="mean_rating",
    markers=True,
    hover_data={"ratings": True, "mean_rating": ":.3f", "year": True},
    labels={"mean_rating": "mean rating", "year": "release year", "ratings": "ratings"},
    title="Mean rating by movie release year",
)
fig3.update_traces(line_color="#4C78A8")
fig3.add_scatter(
    x=thin["year"],
    y=thin["mean_rating"],
    mode="markers",
    marker=dict(symbol="x-open", size=11, color="#E45756", line=dict(width=2)),
    name=f"under {THIN_SAMPLE} ratings",
    customdata=thin["ratings"],
    hovertemplate="year %{x}: %{y:.3f} on %{customdata} ratings (thin sample)<extra></extra>",
)
fig3.update_layout(height=460, xaxis_dtick=5)
st.plotly_chart(fig3, width="stretch")

# ---------------------------------------------------------------- question 4
st.header("Question 4 — Best movies, with a floor on how many ratings count")
q4 = tables["q4"]
top = top_movies(q4, movie_floor)
n_qual = int((q4["ratings"] >= movie_floor).sum())

st.caption(
    f"Floor = number of rating rows for the movie (all 100,000 user/movie pairs are "
    f"unique, so that equals the number of raters). At {movie_floor} ratings: "
    f"{n_qual} movies qualify. Sorted by mean, ties broken by rating count, then title."
)
fig4 = px.bar(
    top.sort_values("mean_rating", ascending=True),
    x="mean_rating",
    y="title",
    orientation="h",
    text=top.sort_values("mean_rating", ascending=True).apply(
        lambda r: f"{r['mean_rating']:.3f}  ({r['ratings']} ratings)", axis=1
    ),
    labels={"mean_rating": "mean rating", "title": "movie"},
    title=f"Top 5 movies with at least {movie_floor} ratings",
)
fig4.update_traces(marker_color="#54A24B", textposition="outside", cliponaxis=False)
fig4.update_layout(
    yaxis={"categoryorder": "total ascending"},
    xaxis_range=[0, 5],
    margin={"r": 150},
    height=360,
    bargap=0.3,
)
st.plotly_chart(fig4, width="stretch")

st.subheader("What changes when the floor goes from 50 to 150?")
top50, top150 = top_movies(q4, 50), top_movies(q4, 150)
compare = pd.DataFrame(
    {
        "Floor 50": top50.apply(
            lambda r: f"{r['title']} — {r['mean_rating']:.3f} ({r['ratings']})", axis=1
        ),
        "Floor 150": top150.apply(
            lambda r: f"{r['title']} — {r['mean_rating']:.3f} ({r['ratings']})", axis=1
        ),
    }
)
st.dataframe(compare, width="stretch", hide_index=True)
dropped = top50[~top50["movie_id"].isin(top150["movie_id"])]
added = top150[~top150["movie_id"].isin(top50["movie_id"])]
st.caption(
    f"Raising the floor to 150 drops {len(dropped)} of the 50-list, all under 150 ratings "
    f"({', '.join(f'{t} {n}' for t, n in zip(dropped['title'], dropped['ratings']))}), "
    f"and pulls in {', '.join(added['title'])}, each with {added['ratings'].min()}+ "
    "ratings behind it."
)
