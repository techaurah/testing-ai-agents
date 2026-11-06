# Lesson 21: The seeded stand-in

Time: ~40 min | Difficulty: Intermediate | Prerequisites: Lesson 20

A deterministic twin cannot teach nondeterminism, so the course ships a labelled stand-in (`agent/standin.py`) that injects controlled wobble into the twin: band thresholds jitter by a seeded amount in [-4, +4], booking phrases are sometimes swapped for synonyms the parser does not know, and replies sometimes gain a courtesy suffix. It is a stand-in, not a model simulation, and it says so on its label: the mechanisms are chosen to be instructive, and every trial is reproducible from its seed.

The lab's first result rearranges a comfortable assumption. Stability is a property of the case, not of the system, and no watched case is fully stable.

## Run it

```bash
python3 standin_lab.py
```

Over 30 trials each: s01 passes 28, s03 passes 19, s05 passes 19, s07 passes 12, s10 passes 14. The boundary cases (scores 80, 65, 50, 49, sitting on the band edges) fail mostly to threshold jitter, as expected. But s01, score 93 and far from every edge the jitter can reach, still drops 2 trials, both through the wording channel, when a phrasing swap hides its booking phrase. And the same seed reproduces a trial exactly, result and variance record alike, which is what makes any of this debuggable.

## Common failures

- Treating the stand-in's rates as predictions about a real model. They are properties of this stand-in and these cases; the transferable skill is the measurement method, not the numbers.
- Running trials without recording seeds. An unreproducible failure in a stochastic suite is a rumour.
- Averaging stability across cases into one system score. 28 of 30 and 12 of 30 are different engineering situations; the average is neither.

## Recap checklist

- [ ] Pass counts: s01 28, s03 19, s05 19, s07 12, s10 14 of 30
- [ ] You can name the stand-in's three wobble mechanisms and which channel explains s01's failures
- [ ] You know why every trial carries its seed

## Resources

- [agent/standin.py](../../agent/standin.py): the stand-in, labelled and seeded
- [Lesson 22](../22-pass-at-k-and-pass-pow-k/): what to compute from these pass counts
