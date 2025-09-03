# Assorted Dataset Creation Code

This folder includes code for making datasets I used throughout classes. Some of them are listed below:

- Street Names in the bay area (small list)
- Street Names in the UK (medium-large list)
- Works of Shakespeare (medium-large list)
- Transcripts from Trump Speeches (large list)
- Mispelled Words (medium-large list)
    - this last one is pretty cool in my opinion, mispellings are made based off of keys that are adjacent on a keyboard, not nearby letters of the alphabet. Reflecting upon this, I could have done this in a more sophisticated manner in a couple ways:
        - Using a probability distribution for each letter, where the probability of replacing this letter with a different letter is inversely proportional to the distance between these letters on the keyboard, not just the boolean of their adjacency.  (I hope that makes sense).
        - swapping adjacent letters (when typing fast, one often types letters in the wrong order)