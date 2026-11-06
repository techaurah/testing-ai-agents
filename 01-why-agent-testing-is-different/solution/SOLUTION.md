# Solution: Why agent testing is different

Any HOT scoring case behaves like s13: the band stays HOT, the stage drops from BOOKED to QUALIFIED, and `book_appointment` leaves the tool sequence, because the hours rule blocks the booking, not the qualification. WARM, NURTURE, and LOW cases are unchanged by the clock, because their routes never consult the calendar. The general law: the clock only matters to cases whose route crosses a time gated tool, which is exactly why the clock belongs in the fixture.
