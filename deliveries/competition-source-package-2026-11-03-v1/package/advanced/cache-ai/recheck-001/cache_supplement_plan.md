# Frozen targeted supplement v1

After initial 40-config PASS, review found byte-mask reads occurred only after all
masks, so intermediate lane errors could be hidden by a later full write. Preserve
original plan/vectors/results. Add a read after EVERY mask, for both cache hit writes
and no-allocate miss writes (distinct cold lines). Expected values supplied by the
same independent byte memory, not RTL. Execute D cached/bypass x delays 0/3.

Add protocol MODE=2: keep qvalid asserted continuously across two acceptances of
identical side-effect reads. Assert no third acceptance while valid held under response
backpressure, change input payload only after acceptance to prove latching, and expect
exactly counters 0 then 1, two backend commands and two responses. Then reset and check
no ghost output. Hold a second request behind a pending first response.

Negative control: flip first expected word in a derived (separately identified) vector;
simulation must fail with data mismatch, not pass. Original frozen vectors untouched.
