# Solution: Regression suites

Under the lowered threshold mutant, r04 and r05 both fail, but they pin different facts: r04 pins the lowest WARM score, r05 pins the highest score that must not be WARM under the real thresholds, one point below the line. Deleting r05 removes the only pin on the 64 side of the WARM boundary, so a future change that moved the WARM threshold to 64 would pass the whole regression set while changing real routing. Boundary pins come in pairs, one on each side of every line, or they do not pin the line.
