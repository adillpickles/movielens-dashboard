# Previous build-log draft — unverified

This is the working-tree draft preserved before the September 30, 2026
corrections. It is retained for provenance, not submitted as an authentic prompt
transcript. Its first-attempt history conflicts with the record in commit
`b861e54`; some quoted prompts and personal-action claims could not be verified.
It also contains the rounding and empty-chart inaccuracies identified in the
audit. Use `../BUILD_LOG.md` for the current record of verified requests and work.

---

# build log: week 4 vibe coding (movielens dashboard)

raw notes from building this. keeping the prompts and what came back from each
one, mostly so next week's report has the real thing and not my memory of it.
not cleaned up on purpose.

## prompt 1 - the four charts

first thing I did was write one prompt using the structure we went over in
class (context, task, constraints, format, check):

> Act as a data scientist helping me with a homework dashboard. Attached is
> movie_ratings.csv, 100,000 ratings. Columns: user_id, movie_id, rating,
> timestamp, age, gender, occupation, zip_code, title, year, decade, genres,
> rating_year. genres is pipe separated and one movie can have more than one.
>
> Don't write code yet. List your steps first and the assumptions you're making
> about the data, especially how you'd count movies by genre and which column
> you'd use for "over time".
>
> Then build it as one streamlit app (app.py) that answers these four questions
> exactly as written, one chart per question: [pasted all 4 questions from the
> assignment here]
>
> pandas and plotly, one file, no write up text inside the app, short captions
> are fine.
>
> For each chart tell me the type you picked and why, and give me the numbers
> behind it so I can check them before I trust anything.

what came back: a plan first, then a working app. all four questions had a
chart on the first run, but before I believed any of it I went through the
charts and found three problems:

- q1 was a pie chart. 18 genres in a pie is unreadable, and it counted ratings
  instead of movies. had it redone as a horizontal bar chart of distinct
  movies, sorted.
- q3 was using rating_year. that column only has 1997 and 1998 in this file,
  so the "trend" was a two point line. had it switch to release year.
- nothing explained what happens to a movie with 3 genres. the assignment says
  to get that explanation before it counts anything, so now the chart says it
  up front: a movie counts once under every genre it has, which is why the
  percentages add up to about 172% and not 100%.

## prompt 2 - floors and small samples

next prompt was about the parts I didn't trust yet:

> Keep the four questions as written. Two changes. For question 2, "unknown"
> isn't a genre and it only has 10 ratings behind it, leave it out and say so
> on the chart. Add a minimum ratings control so a genre average over a tiny
> sample can't sit next to one over 40,000 ratings. Default it so nothing
> disappears, but make it strong enough that pushing it actually changes the
> chart.
>
> For question 4, the 50 is a minimum on how many ratings a movie has, keep
> that exact, and add a way to raise it to 150 to see what changes. Ties
> matter, if two movies have the same average the one with more ratings should
> win.
>
> Print the numbers behind everything so I can check them a second way.

all of that came back. numbers I checked so far: 100,000 rows, 100,000 unique
user/movie pairs, 1,682 movies, 943 users, Drama 725 movies, Film-Noir highest
average at 3.922 (1,733 ratings), War 3.816, Drama 3.687, and 30 rating rows
with a blank release year across 5 movies (dropped before the year chart, and
the chart says so).

two things I did myself:

- my first check script printed every average that shows up more than once.
  180 lines of noise I couldn't read. rewrote it to print just the tie that
  decides q4: 4.466, Schindler's List (298 ratings) over The Wrong Trousers
  (118). wrote a second check script with only the csv module so the numbers
  get checked two ways.
- the question 2 floor is on the genre, not on movies: a genre needs at least
  N ratings behind its average to show. dropping movies instead would move
  every average I just checked. default 100 excludes nothing. pushed to
  10,000, 7 of 18 genres are left, which is the point of having the control.

q4 floors: 603 movies qualify at 50, 203 at 150. at 150, Close Shave (112),
Wrong Trousers (118) and Wallace & Gromit (67) drop off and Shawshank, Rear
Window and The Usual Suspects come in. added a small side by side table so
both floors show at once without touching the slider.

## prompt 3 - ran it, drove every control

then I actually ran it, moved every slider and the dropdown, wrote down what
looked off, and sent this:

> Ran it. 5 warnings in the server log about use_container_width. q4 value
> labels are cut off at the right edge ("4.491 (11"). The q3 line dives down
> to 1926, which has 2 ratings, and draws straight through years that have
> none. Clearing the genre dropdown leaves blank axes. Fix all of that, and if
> width needs a newer streamlit, put that in requirements.txt too.

what changed:

- use_container_width replaced with width="stretch" (5 spots) and
  requirements.txt now says streamlit>=1.51. that argument doesn't exist
  before 1.51.
- value labels not clipped anymore (q4 and q2).
- q3: years with under 30 ratings now show as red x marks off the line, and
  the line breaks where there's no data instead of pretending 1926 is part of
  a trend.
- clearing the genres shows a message instead of blank axes.
- q1 caption said the labels were "shares" when the bars showed counts. bars
  now show both: 725 (43.2%).
- my first screenshot of the genre floor had Drama also removed from the
  dropdown, so it showed two changes at once and read 6 of 18. retook it from
  a fresh page with only the floor moved, now reads 7 of 18.

after that: ran it again (no warnings), drove the widgets one more time to make
sure they still change things (150 -> "203 movies qualify", genre floor at
10,000 -> 7 of 18 genres, remove Drama -> the 725 bar goes), and retook all 7
screenshots.

still to do at this point: deploy on streamlit cloud, which needs a public
repo first.

