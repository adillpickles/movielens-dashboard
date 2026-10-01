"""Second-way check with the standard library only — no pandas.

Computes the same core quantities as check_numbers.py using a separate CSV
loop. Compare corresponding values; the reports have different formats and
extra diagnostics, so they are not intended to match line by line.

Run:  uv run --with pandas python check_stdlib.py   (pandas is not imported;
        plain `python3 check_stdlib.py` works too)
"""

import csv
from collections import Counter, defaultdict

CSV = "data/movie_ratings.csv"

rows = 0
pairs = set()
movies = {}
users = set()
genre_movie_counts = Counter()      # distinct movies per genre
movie_genre_n = {}                  # movie_id -> genre token count
genre_rating_sum = Counter()        # sum of ratings per genre (exploded)
genre_rating_n = Counter()          # rating rows per genre (exploded)
year_rating_sum = defaultdict(float)
year_rating_n = Counter()
movie_rating_sum = defaultdict(float)
movie_rating_n = Counter()
blank_year_rows = 0
blank_year_movies = set()
tokens = set()

with open(CSV, newline="", encoding="utf-8") as fh:
    for rec in csv.DictReader(fh):
        rows += 1
        uid, mid = rec["user_id"], rec["movie_id"]
        pairs.add((uid, mid))
        users.add(uid)
        rating = float(rec["rating"])
        title = rec["title"]
        year = rec["year"].strip()
        if year:
            y = int(float(year))
            year_rating_sum[y] += rating
            year_rating_n[y] += 1
        else:
            blank_year_rows += 1
            blank_year_movies.add(mid)
        gs = [g for g in rec["genres"].split("|") if g]
        tokens.update(gs)
        # movie-level facts are repeated on every row; first write wins
        if mid not in movies:
            movies[mid] = title
            movie_genre_n[mid] = len(gs)
            seen = set()
            for g in gs:
                if g not in seen:
                    genre_movie_counts[g] += 1
                    seen.add(g)
        for g in gs:
            genre_rating_sum[g] += rating
            genre_rating_n[g] += 1
        movie_rating_sum[mid] += rating
        movie_rating_n[mid] += 1

print("== shape and keys ==")
print("rows", rows)
print("unique user/movie pairs", len(pairs))
print("distinct movies", len(movies))
print("distinct users", len(users))
print("genre tokens", len(tokens))

print("\n== blank release year ==")
print("blank year rows", blank_year_rows)
print("blank year movies", len(blank_year_movies))

print("\n== release-year points (Q3) ==")
print("distinct non-blank years", len(year_rating_n))
print("year min/max", min(year_rating_n), max(year_rating_n))
print("ratings in 1926", year_rating_n[1926])
print("thin years (<30 ratings):",
      {y: n for y, n in sorted(year_rating_n.items()) if n < 30})

print("\n== Q1 movies per genre (distinct movie_id) ==")
for g, c in genre_movie_counts.most_common():
    print(f"{g:12s} {c}")
print("movies carrying N genres:",
      dict(sorted(Counter(movie_genre_n.values()).items())))
# both 'unknown' movies carry that tag alone, so this is the known-genre count
known_movies = len(movies) - genre_movie_counts["unknown"]
known_tags = sum(c for g, c in genre_movie_counts.items() if g != "unknown")
print("known-genre movies", known_movies)
print("share-of-movies sum, % (excl unknown)", round(100 * known_tags / known_movies, 2))

print("\n== Q2 mean rating per genre (exploded rows) ==")
means = {g: genre_rating_sum[g] / genre_rating_n[g] for g in genre_rating_n}
for g in sorted(means, key=lambda k: means[k], reverse=True):
    print(f"{g:12s} {means[g]:.3f}  n={genre_rating_n[g]}")

print("\n== Q4 top 5 with floor ==")
stats = [(movies[m], movie_rating_sum[m] / movie_rating_n[m], movie_rating_n[m])
         for m in movies]
for floor in (50, 150):
    sub = [s for s in stats if s[2] >= floor]
    sub.sort(key=lambda s: (-s[1], -s[2], s[0]))
    print(f"-- floor {floor}: qualifying movies {len(sub)}")
    for t, m, n in sub[:5]:
        print(f"   {t[:40]:42s} {m:.3f}  n={n}")
