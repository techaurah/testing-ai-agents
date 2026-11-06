# Solution: Property based assertions

The reference agent shows 0 violations (its routing honours the law by construction). With `booking_hours_guard` off the law still shows 0 violations, because the law's condition includes the working hours premise, which the fixed Monday 10:00 clock always satisfies; the mutant's damage appears on out of hours cases, which this law never generates. The lesson inside the exercise: a property only guards the input region its generator visits, so generator design is assertion design.
