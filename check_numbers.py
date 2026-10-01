"""Second-way number checks for the Week 4 MovieLens dashboard.

Run:  uv run --with pandas python check_numbers.py
Computes the main quantities in verification.md directly from
data/movie_ratings.csv using pandas. check_stdlib.py computes the same core
quantities separately with the csv module. The assignment supplies questions,
not numerical reference answers. Compare corresponding values in the two
reports; their output formats and extra diagnostics differ.
"""

import pandas as pd

CSV = "data/movie_ratings.csv"
df = pd.read_csv(CSV)

print("== shape and keys ==")
print("rows", len(df))
print("unique user/movie pairs", df.groupby(["user_id", "movie_id"]).ngroups)
print("distinct movies", df["movie_id"].nunique())
print("distinct users", df["user_id"].nunique())

genres = df["genres"].str.split("|")
all_tokens = sorted({g for row in genres for g in row})
print("genre tokens", len(all_tokens), all_tokens)

print("\n== blank release year ==")
blank_year = df["year"].isna()
print("blank year rows", int(blank_year.sum()))
print("blank year movies", df.loc[blank_year, "movie_id"].nunique())
print("blank year titles", sorted(df.loc[blank_year, "title"].unique()))

print("\n== release-year points (Q3) ==")
print("distinct non-blank years", df["year"].nunique())
print("year min/max", df["year"].min(), df["year"].max())
print("distinct rating_year", sorted(int(v) for v in df["rating_year"].unique()))
by_year = df.dropna(subset=["year"]).groupby("year")["rating"].agg(["mean", "size"])
print("thin years (<30 ratings):", {int(y): int(n) for y, n in by_year.loc[by_year["size"] < 30, "size"].items()})

print("\n== Q1 movies per genre (distinct movie_id), including unknown for comparison ==")
movie_genres = df[["movie_id", "genres"]].drop_duplicates("movie_id")
exploded = movie_genres.assign(genre=movie_genres["genres"].str.split("|")).explode("genre")
counts = exploded["genre"].value_counts()
print(counts.to_string())
print("movies carrying 1..6 genres:")
print(exploded.groupby("movie_id").size().value_counts().sort_index().to_string())
known_movies = movie_genres.loc[movie_genres["genres"] != "unknown", "movie_id"].nunique()
known_counts = counts.drop("unknown", errors="ignore")
print("known-genre movies", known_movies)
print("share-of-movies sum, % (excl unknown)", round(100 * known_counts.sum() / known_movies, 2))

print("\n== Q2 mean rating per genre (rating rows exploded), including unknown for comparison ==")
exp_ratings = df.assign(genre=df["genres"].str.split("|")).explode("genre")
gen = exp_ratings.groupby("genre")["rating"].agg(["mean", "count"])
print(gen.sort_values("mean", ascending=False).to_string(float_format=lambda x: f"{x:.3f}"))
print("incl unknown lowest:", gen.sort_values("mean").head(3).to_string(float_format=lambda x: f"{x:.3f}"))

print("\n== unknown genre sample ==")
unk = exp_ratings[exp_ratings["genre"] == "unknown"]
print("rows", len(unk), "movies", unk["movie_id"].nunique(), "mean", round(unk["rating"].mean(), 3))

print("\n== Q4 top 5 with rating floor ==")
movie_stats = df.groupby(["movie_id", "title"]).agg(
    mean=("rating", "mean"), n=("rating", "size")).reset_index()
for floor in (50, 150):
    sub = movie_stats[movie_stats["n"] >= floor]
    top = sub.sort_values(["mean", "n", "title"], ascending=[False, False, True]).head(5)
    print(f"-- floor {floor}: qualifying movies {len(sub)}")
    for _, r in top.iterrows():
        print(f"   {r['title'][:40]:42s} {r['mean']:.3f}  n={r['n']}")

print("\n== rounded-display collisions at floor 50 (not exact ties) ==")
sub = movie_stats[movie_stats["n"] >= 50]
vc = sub["mean"].round(3).value_counts()
tied = vc[vc > 1]
print("three-decimal displays shared by more than one movie:", len(tied), "distinct values,",
      int(tied.sum()), "movies")
print(tied.sort_index().head(8).to_string())
print("movies displayed as 4.466; full means determine their order:")
print(sub[sub["mean"].round(3) == 4.466].sort_values(
    ["mean", "n", "title"], ascending=[False, False, True]
).to_string(index=False, float_format=lambda x: f"{x:.9f}"))

print("\n== genre count on movies-per-genre multi-label shape ==")
print("movies with >1 genre:", int((exploded.groupby("movie_id").size() > 1).sum()))
