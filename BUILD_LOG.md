# Build log — Week 4 MovieLens dashboard

Updated September 30, 2026. The two moments below use actual user requests
from this conversation. Quoted requests and responses are copied from the
conversation; the result and change notes summarize the work performed.

The dashboard was originally generated with two agents, as the user reported.
The original generation conversations are not available in this repository or
the current conversation. I cannot authenticate the earlier prompts or the
claim that the first app used a pie chart and rating year. The log in commit
`b861e54` and the later working-tree draft tell different first-attempt stories.
Neither is treated here as proof of an exact original prompt.

The previous working-tree draft is preserved in
[notes/BUILD_LOG.before-corrections.md](notes/BUILD_LOG.before-corrections.md),
clearly labeled unverified. This log records the audit and correction phase,
not a reconstructed history of initial app generation.

## Moment 1 — Check the assignment and compare the dashboards

Actual user prompt:

> Okay, long story short, go ahead and do the same exact audit and come back to me with the final step-by-step on what's left. I switched models to a more capable model, so I want you to actually take a deeper look at the two students who already submitted their dashboards compared to mine. And again, if there's anything that is different from theirs that I don't personally have and they have in common with one another, then that must mean that I didn't listen to the assignment directions clearly. On top of that, I want you to actually look at the assignment details and then look at what I have down and verify that I've done everything correctly and right. There may be some purposely laid out traps in the assignment details and the reason for this is to try to trip up agentic coders. So you might have to be on the lookout for that. On top of that, there should be a buildlog.markdown file which discusses how I actually prompted stuff. And I want you to actually take a look at that and verify that it looks real and right. What that means is verifying that it looks like actual real prompts that a student probably provided and the output that the student said the model gave them actually looks realistic and right. So go ahead and do that. So again, one, go ahead and do a deep audit of mine against the two students, then do another audit of mine against the actual assignment details, and then lastly take a look at build log.MD and make sure that that's properly done.

First completed AI result, opening of the audit response:

> Your dashboard’s calculations and required functionality check out. The assignment is not fully finished yet: the build log needs correction, and public deployment and submission remain. I made no changes to your repository.

What the AI did and found:

- Read the assignment and inspected the local code and both public dashboards:
  https://axelm-movie-app.streamlit.app/ and
  https://shahad-dashboard.streamlit.app/.
- Independently aggregated the supplied CSV with the standard library and
  exact fractional means, and compared the app's tables and rankings.
- Checked all 21 movie-floor settings, 50 through 150 in steps of 5, and
  exercised all four local input controls, including clearing genres.
- Confirmed Drama = 725 distinct movies; Film-Noir = approximately 3.922
  from 1,733 ratings; missing release year = 30 rating rows across 5 movies;
  qualifying movies = 603 at 50 ratings and 203 at 150.
- Found that Axel's genre chart counts rating rows rather than distinct
  movies. Shared features between classmates therefore were not used as
  substitutes for the assignment instructions.
- Found a caption issue: the app described the displayed shares as totaling
  172% even after some genres were removed.
- Found conflicting process stories, a placeholder in a supposed raw prompt,
  and an incorrect explanation of rounded means as exact ties.

What changed and why:

No repository files were edited during that audit because the user requested
analysis first. The proposed fixes were limited to the caption and inaccurate
documentation; the verified analytical calculations did not need replacement.
The user then asked for a brief summary and authorized the corrections below.

## Moment 2 — Apply the corrections

Actual user prompt:

> Go ahead and make those fixes yourself.

First AI response:

> I’ll fix the caption and documentation errors, and revise the build log so it clearly distinguishes supported facts from prompts and process details we can’t verify.

What the AI changed:

- Q1 now explicitly says the denominator is all 1,680 rated movies with a
  known genre, and that the approximately 172% total is across all 18 genres.
  Removing genres changes the displayed bars, not the denominator.
- The Q4 explanation now uses the actual means: Schindler's List
  4.466442953 and The Wrong Trousers 4.466101695. Both round to 4.466, but the
  higher actual mean decides their order. Rating count only breaks actual
  mean ties.
- The pandas check report labels three-decimal collisions as rounded
  displays, prints the underlying means for that example, and sorts means
  before formatting them.
- Dataset-derived checks are no longer attributed to an official answer key:
  the assignment supplies questions, not reference numbers.
- The verification notes distinguish assignment requirements from optional
  choices such as excluding unknown, a genre-level sample floor, and a
  30-rating threshold for flagging years.
- The empty-selection notes now accurately say that messages appear while
  empty chart axes still render.
- README and verification history were updated to match this two-moment log.
  Agent actions are not represented as work the student personally performed.

Why these changes:

The user authorized fixes after the audit. These changes correct explanations
and preserve the existing analytical approach. The two requests above are
available records; inventing earlier prompts or failures would not satisfy the
assignment's requirement to retain the actual process.

Verification status:

The numerical and browser checks described in Moment 1 happened before these
corrections. The correction changes were reviewed as source diffs; no new
runtime or numerical test run is claimed here. Existing screenshots were kept,
not recaptured after the caption change.

Still outstanding:

Publish the app from the student's own public GitHub repository, deploy it on
Streamlit Community Cloud, check the URL in an Incognito/Private window, and
submit the public URL in the Week 4 HW Submission Sheet. No repository push or
deployment was performed during this correction request.
