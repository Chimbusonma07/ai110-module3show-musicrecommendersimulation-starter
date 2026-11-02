# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**TuneScout 1.0**

---

## 2. Intended Use  

**What it does**

- TuneScout suggests 5 songs from a small catalog.
- You tell it your favorite genre and mood, plus how loud, fast, happy, danceable and acoustic you like your music.
- It scores every song against that taste and shows the 5 best, with a reason for each one.

**What it assumes**

- It assumes you have one favorite genre and one favorite mood.
- It assumes your taste stays the same. It doesn't learn from what you skip or replay.

**What it's for**

- Classroom exploration: learning how a simple recommender works and where it goes wrong.
- Trying out "what if" taste profiles and seeing how the picks change.

**What it's not for**

- Real users or a real music app. The catalog is only 20 songs.
- Judging what music is "good." It only measures how close a song is to what you asked for.
- Anyone whose taste mixes several genres or moods. It can only hold one of each.

---

## 3. How the Model Works  

Every song gets points. The songs with the most points are recommended.

- **Genre:** An exact match earns 2 points, the biggest single reward. A related name, like "indie pop" for a pop fan, earns 1 point.
- **Mood:** An exact match earns 1 point. A similar mood, like "relaxed" for a "chill" fan, earns half a point.
- **Numbers:** Each song has energy, tempo, happiness (valence), danceability and acousticness. The closer a song is to your target, the more points it gets.
- **Energy matters most** among the numbers (up to 1.5 points). Happiness is next (0.75). The rest are worth up to 0.5 each.
- **Ties:** If two songs score the same, the one closer to your energy target wins.
- **Changes from the starter:** The starter just returned the first 5 songs in the file. I added the scoring, the half-credit for related genres and similar moods, and the reasons shown next to each pick.

---

## 4. Data  

- The catalog has **20 songs**, stored in `data/songs.csv`.
- Each song has a title, artist, genre, mood, and five number features: energy, tempo, valence, danceability and acousticness.
- There are **17 genres**, but most have just one song. Lofi has 3 and pop has 2.
- There are **16 moods**. "Chill" is the most common, with 3 songs.
- Energy is spread out, but there's a gap: no song falls between 0.58 and 0.75.
- I didn't add or remove any songs.
- **What's missing:** lyrics, language, release year, artist popularity, and anything about what real listeners actually played. Big genres like K-pop, gospel and punk aren't there at all.

---

## 5. Strengths  

- It works well for listeners whose taste the catalog covers. High-Energy Pop, Chill Lofi and Deep Intense Rock each got a near-perfect #1 (above 6.6 out of 6.75).
- Opposite tastes get opposite results. The pop and lofi lists share no songs.
- Half-credit for similar moods helps. A "chill" fan still gets "relaxed" jazz instead of nothing.
- Every pick comes with reasons, so you can see exactly why a song was chosen.
- It's predictable. The same profile always gets the same list.  

---

## 6. Limitations and Bias 

- The genre and mood labels together are worth 3 points, so a song with the "right" labels beats songs whose actual sound fits the user far better.
- In the "Sad Banger" test (sad mood, energy 0.9), the slow blues song Crossroads Whiskey (energy 0.45) ranked #1, and it stayed #1 even after doubling the energy weight and halving the genre weight.
- That weight shift changed only 11 of 50 top-5 slots across ten profiles, and the #1 pick changed for just one profile, so the label bias is built into how the scoring is structured, not just into the exact weight values.
- The bias is worse for niche listeners: 15 of the 17 genres have only one song, so a rock or jazz fan gets one genre match and then filler, while a lofi fan gets three matches.  

---

## 7. Evaluation  

I ran 10 user profiles through the recommender and read each top-5 list to check whether the picks matched what that listener asked for.

**Profiles tested**

- Three "normal" listeners: High-Energy Pop, Chill Lofi, and Deep Intense Rock.
- Seven tricky ones, built to find weak spots:
  - Sad Banger: sad mood but very high energy.
  - Empty Genre: no genre given.
  - K-Pop Fan: a genre the catalog doesn't have.
  - Sloppy Input: `"  Rock "` with extra spaces and capital letters.
  - Out of Range: impossible numbers, like energy 1.8.
  - Romantic Only: a mood with no "similar" moods.
  - Fence Sitter: nothing matches and every number is set to the middle.

**Comparing pairs of profiles**

- **High-Energy Pop vs. Chill Lofi:** The two lists share no songs at all. Pop gets loud, danceable tracks (energy 0.76–0.95), and Lofi gets quiet, acoustic ones (energy 0.28–0.42). That makes sense: they asked for opposite things on almost every number.
- **High-Energy Pop vs. Deep Intense Rock:** "Gym Hero" comes 2nd in both lists, for different reasons. For the pop fan, it's labeled "pop," and a genre match is the biggest single reward (2 points). For the rock fan, it's labeled "intense" and is just as loud as rock.
- **Why "Gym Hero" keeps showing up for Happy Pop fans:** The system sees "pop" on the label and hands out its biggest reward before it looks at mood. Gym Hero is a workout song, not a happy one, but it only loses the 1 mood point. That's less than the genre point "Rooftop Lights" misses for being labeled "indie pop" instead of plain "pop."
- **Chill Lofi vs. Deep Intense Rock:** Lofi's top 3 are all lofi songs with scores above 5.6. Rock has one strong match (Storm Runner, 6.71), then drops to 4.27. The catalog has three lofi songs but only one rock song, so the rock fan runs out of real matches after the first pick.
- **Deep Intense Rock vs. Sad Banger:** Both asked for energy 0.9, so loud songs like Storm Runner, Iron Furnace and Gym Hero appear in both lists. But Sad Banger's #1 is a slow blues song (energy 0.45), because its "blues" and "sad" labels outweigh the energy the user actually asked for.
- **Deep Intense Rock vs. Sloppy Input:** Both lists start with Storm Runner, but its score falls from 6.71 to 3.48. The extra spaces in `"  Rock "` stop it from counting as an exact genre match, and the sloppy profile set fewer numbers, so there were fewer points to win.
- **High-Energy Pop vs. K-Pop Fan:** Sunrise City is #1 in both lists. "Rooftop Lights" gets no genre credit for the K-Pop fan, though, because the system only compares spelling and "k-pop" isn't spelled inside "indie pop." It has no idea the two genres sound alike.
- **Chill Lofi vs. Empty Genre:** The songs are mostly the same calm tracks, but with no genre given, every song in the catalog got a "related genre" bonus. The genre check stopped meaning anything, so mood and energy alone decided the order.
- **Deep Intense Rock vs. Out of Range:** The metal song Iron Furnace wins easily (3.46), and every other song scores under 1 point. No song can be as loud as 1.8, so the number scores collapse to almost zero and only the labels count.
- **Romantic Only vs. Fence Sitter:** "Velvet Hours" appears in both lists. The romantic listener only gets it at #2, even though its mood is an exact "romantic" match, because a jazz-labeled song wins on genre. For the Fence Sitter, it comes #1 just because its energy is exactly 0.5, and the whole top 5 sits within 0.14 points, so the order is close to random.

**What surprised me**

- The recommender never says "nothing fits." Even when nothing matched (Fence Sitter, K-Pop Fan), it still showed five confident-looking picks.
- I tested a weight change: doubling the weight on energy and halving the weight on genre. Only 11 of the 50 top-5 slots changed, and only one profile got a new #1. The labels still dominated, which shows the bias comes from how the score is built, not just from the exact numbers.

---

## 8. Future Work  

- **Let the sound count more than the labels.** Right now a matching genre or mood label can beat a song that actually sounds right. I'd lower the label points, or only give them when the numbers are also close.
- **Say when nothing fits.** If no song scores above a minimum, the system should say "no good match" instead of showing 5 weak picks as if they were good.
- **Clean up the input and add variety.** Trim spaces, skip the genre check when it's empty, and reject impossible numbers like energy 1.8. I'd also stop the top 5 from being five songs of the same genre or artist.

---

## 9. Personal Reflection  

**Biggest learning moment**

- The weight-shift test. I doubled the weight on energy and halved the weight on genre, expecting big changes.
- Almost nothing moved. The #1 pick stayed the same for 9 of 10 profiles.
- That taught me the problem wasn't the exact numbers. It was the design: labels hand out big flat rewards that the numbers can't catch up to.

**How AI tools helped, and when I double-checked**

- AI helped me come up with tricky test profiles I wouldn't have thought of, like a blank genre or impossible numbers.
- It also helped me write a quick script to compare rankings before and after the weight change.
- I still had to check its claims by running the code. Once it said the "  Rock " profile would never match rock. When I ran it, the song still got partial credit, so the comment was wrong and had to be fixed.
- I also checked the numbers it quoted in this card against the real output, not just trusted them.

**What surprised me**

- A few lines of adding up points already feel like a real recommender. The lofi fan gets calm study music. The rock fan gets loud, fast songs.
- The "why" list makes it feel smart, even though it's just showing the math.
- But it never says "I don't know." It gives five confident picks even when nothing fits, and that looks just as convincing as a good list.

**What I'd try next**

- Make the score depend more on how a song sounds and less on its label.
- Add a "no good match" message when every score is low.
- Grow the catalog so each genre has more than one song, then test whether the bias toward lofi fans goes away.
- Let the user give feedback (like or skip) and adjust their profile over time.  

---

## 10 Output
```
Loaded songs: 20

============================================================
 High-Energy Pop: top 5 picks for 'pop' / happy / energy 0.85
============================================================

 1. Sunrise City  by Neon Echo
    pop | happy | Score: 6.61 / 6.75
    Why:
      - genre match (+2.0)
      - mood match (+1.0)
      - energy close to target (+1.46)
      - valence close to target (+0.74)
      - danceability close to target (+0.47)
      - acousticness close to target (+0.46)
      - tempo_bpm close to target (+0.48)

 2. Gym Hero  by Max Pulse
    pop | intense | Score: 5.48 / 6.75
    Why:
      - genre match (+2.0)
      - energy close to target (+1.38)
      - valence close to target (+0.69)
      - danceability close to target (+0.48)
      - acousticness close to target (+0.47)
      - tempo_bpm close to target (+0.45)

 3. Rooftop Lights  by Indigo Parade
    indie pop | happy | Score: 5.44 / 6.75
    Why:
      - related genre: indie pop (+1.0)
      - mood match (+1.0)
      - energy close to target (+1.36)
      - valence close to target (+0.72)
      - danceability close to target (+0.48)
      - acousticness close to target (+0.38)
      - tempo_bpm close to target (+0.49)

 4. Drop Zone  by Pulse Theory
    edm | euphoric | Score: 3.92 / 6.75
    Why:
      - similar mood: euphoric (+0.5)
      - energy close to target (+1.35)
      - valence close to target (+0.67)
      - danceability close to target (+0.47)
      - acousticness close to target (+0.46)
      - tempo_bpm close to target (+0.47)

 5. Concrete Crown  by Kilo Verse
    hip hop | confident | Score: 3.82 / 6.75
    Why:
      - similar mood: confident (+0.5)
      - energy close to target (+1.40)
      - valence close to target (+0.58)
      - danceability close to target (+0.49)
      - acousticness close to target (+0.49)
      - tempo_bpm close to target (+0.36)

------------------------------------------------------------

============================================================
 Chill Lofi: top 5 picks for 'lofi' / chill / energy 0.38
============================================================

 1. Library Rain  by Paper Lanterns
    lofi | chill | Score: 6.63 / 6.75
    Why:
      - genre match (+2.0)
      - mood match (+1.0)
      - energy close to target (+1.46)
      - valence close to target (+0.73)
      - danceability close to target (+0.49)
      - acousticness close to target (+0.47)
      - tempo_bpm close to target (+0.48)

 2. Midnight Coding  by LoRoom
    lofi | chill | Score: 6.61 / 6.75
    Why:
      - genre match (+2.0)
      - mood match (+1.0)
      - energy close to target (+1.44)
      - valence close to target (+0.74)
      - danceability close to target (+0.49)
      - acousticness close to target (+0.45)
      - tempo_bpm close to target (+0.49)

 3. Focus Flow  by LoRoom
    lofi | focused | Score: 5.68 / 6.75
    Why:
      - genre match (+2.0)
      - energy close to target (+1.47)
      - valence close to target (+0.74)
      - danceability close to target (+0.50)
      - acousticness close to target (+0.49)
      - tempo_bpm close to target (+0.48)

 4. Spacewalk Thoughts  by Orbit Bloom
    ambient | chill | Score: 4.31 / 6.75
    Why:
      - mood match (+1.0)
      - energy close to target (+1.35)
      - valence close to target (+0.70)
      - danceability close to target (+0.41)
      - acousticness close to target (+0.44)
      - tempo_bpm close to target (+0.42)

 5. Coffee Shop Stories  by Slow Stereo
    jazz | relaxed | Score: 3.99 / 6.75
    Why:
      - similar mood: relaxed (+0.5)
      - energy close to target (+1.48)
      - valence close to target (+0.65)
      - danceability close to target (+0.47)
      - acousticness close to target (+0.46)
      - tempo_bpm close to target (+0.43)

------------------------------------------------------------

============================================================
 Deep Intense Rock: top 5 picks for 'rock' / intense / energy 0.90
============================================================

 1. Storm Runner  by Voltline
    rock | intense | Score: 6.71 / 6.75
    Why:
      - genre match (+2.0)
      - mood match (+1.0)
      - energy close to target (+1.48)
      - valence close to target (+0.73)
      - danceability close to target (+0.49)
      - acousticness close to target (+0.50)
      - tempo_bpm close to target (+0.49)

 2. Gym Hero  by Max Pulse
    pop | intense | Score: 4.27 / 6.75
    Why:
      - mood match (+1.0)
      - energy close to target (+1.46)
      - valence close to target (+0.55)
      - danceability close to target (+0.39)
      - acousticness close to target (+0.47)
      - tempo_bpm close to target (+0.41)

 3. Iron Furnace  by Grave Engine
    metal | angry | Score: 3.71 / 6.75
    Why:
      - similar mood: angry (+0.5)
      - energy close to target (+1.40)
      - valence close to target (+0.54)
      - danceability close to target (+0.40)
      - acousticness close to target (+0.46)
      - tempo_bpm close to target (+0.41)

 4. Fuego Lento  by Los Brisas
    latin | energetic | Score: 3.43 / 6.75
    Why:
      - similar mood: energetic (+0.5)
      - energy close to target (+1.41)
      - valence close to target (+0.46)
      - danceability close to target (+0.38)
      - acousticness close to target (+0.42)
      - tempo_bpm close to target (+0.25)

 5. Night Drive Loop  by Neon Echo
    synthwave | moody | Score: 3.22 / 6.75
    Why:
      - energy close to target (+1.27)
      - valence close to target (+0.74)
      - danceability close to target (+0.46)
      - acousticness close to target (+0.44)
      - tempo_bpm close to target (+0.30)

------------------------------------------------------------

============================================================
 Sad Banger: top 5 picks for 'blues' / sad / energy 0.90
============================================================

 1. Crossroads Whiskey  by Delta Moan
    blues | sad | Score: 5.19 / 6.75
    Why:
      - genre match (+2.0)
      - mood match (+1.0)
      - energy close to target (+0.83)
      - valence close to target (+0.68)
      - danceability close to target (+0.34)
      - acousticness close to target (+0.17)
      - tempo_bpm close to target (+0.18)

 2. Night Drive Loop  by Neon Echo
    synthwave | moody | Score: 3.56 / 6.75
    Why:
      - similar mood: moody (+0.5)
      - energy close to target (+1.27)
      - valence close to target (+0.53)
      - danceability close to target (+0.46)
      - acousticness close to target (+0.44)
      - tempo_bpm close to target (+0.35)

 3. Storm Runner  by Voltline
    rock | intense | Score: 3.40 / 6.75
    Why:
      - energy close to target (+1.48)
      - valence close to target (+0.54)
      - danceability close to target (+0.43)
      - acousticness close to target (+0.50)
      - tempo_bpm close to target (+0.44)

 4. Iron Furnace  by Grave Engine
    metal | angry | Score: 3.28 / 6.75
    Why:
      - energy close to target (+1.40)
      - valence close to target (+0.73)
      - danceability close to target (+0.32)
      - acousticness close to target (+0.46)
      - tempo_bpm close to target (+0.36)

 5. Gym Hero  by Max Pulse
    pop | intense | Score: 3.17 / 6.75
    Why:
      - energy close to target (+1.46)
      - valence close to target (+0.32)
      - danceability close to target (+0.46)
      - acousticness close to target (+0.47)
      - tempo_bpm close to target (+0.46)

------------------------------------------------------------

============================================================
 Empty Genre: top 5 picks for '' / chill / energy 0.40
============================================================

 1. Midnight Coding  by LoRoom
    lofi | chill | Score: 3.47 / 6.75
    Why:
      - related genre: lofi (+1.0)
      - mood match (+1.0)
      - energy close to target (+1.47)

 2. Library Rain  by Paper Lanterns
    lofi | chill | Score: 3.42 / 6.75
    Why:
      - related genre: lofi (+1.0)
      - mood match (+1.0)
      - energy close to target (+1.42)

 3. Spacewalk Thoughts  by Orbit Bloom
    ambient | chill | Score: 3.32 / 6.75
    Why:
      - related genre: ambient (+1.0)
      - mood match (+1.0)
      - energy close to target (+1.32)

 4. Coffee Shop Stories  by Slow Stereo
    jazz | relaxed | Score: 2.96 / 6.75
    Why:
      - related genre: jazz (+1.0)
      - similar mood: relaxed (+0.5)
      - energy close to target (+1.46)

 5. Mountain Letters  by Fern & Hollow
    folk | peaceful | Score: 2.85 / 6.75
    Why:
      - related genre: folk (+1.0)
      - similar mood: peaceful (+0.5)
      - energy close to target (+1.35)

------------------------------------------------------------

============================================================
 K-Pop Fan: top 5 picks for 'k-pop' / happy / energy 0.80
============================================================

 1. Sunrise City  by Neon Echo
    pop | happy | Score: 3.47 / 6.75
    Why:
      - related genre: pop (+1.0)
      - mood match (+1.0)
      - energy close to target (+1.47)

 2. Rooftop Lights  by Indigo Parade
    indie pop | happy | Score: 2.44 / 6.75
    Why:
      - mood match (+1.0)
      - energy close to target (+1.44)

 3. Gym Hero  by Max Pulse
    pop | intense | Score: 2.30 / 6.75
    Why:
      - related genre: pop (+1.0)
      - energy close to target (+1.30)

 4. Concrete Crown  by Kilo Verse
    hip hop | confident | Score: 1.97 / 6.75
    Why:
      - similar mood: confident (+0.5)
      - energy close to target (+1.47)

 5. Drop Zone  by Pulse Theory
    edm | euphoric | Score: 1.78 / 6.75
    Why:
      - similar mood: euphoric (+0.5)
      - energy close to target (+1.28)

------------------------------------------------------------

============================================================
 Sloppy Input: top 5 picks for '  Rock ' / INTENSE / energy 0.90
============================================================

 1. Storm Runner  by Voltline
    rock | intense | Score: 3.48 / 6.75
    Why:
      - related genre: rock (+1.0)
      - mood match (+1.0)
      - energy close to target (+1.48)

 2. Gym Hero  by Max Pulse
    pop | intense | Score: 2.46 / 6.75
    Why:
      - mood match (+1.0)
      - energy close to target (+1.46)

 3. Fuego Lento  by Los Brisas
    latin | energetic | Score: 1.91 / 6.75
    Why:
      - similar mood: energetic (+0.5)
      - energy close to target (+1.41)

 4. Iron Furnace  by Grave Engine
    metal | angry | Score: 1.90 / 6.75
    Why:
      - similar mood: angry (+0.5)
      - energy close to target (+1.40)

 5. Drop Zone  by Pulse Theory
    edm | euphoric | Score: 1.43 / 6.75
    Why:
      - energy close to target (+1.43)

------------------------------------------------------------

============================================================
 Out of Range: top 5 picks for 'metal' / angry / energy 1.80
============================================================

 1. Iron Furnace  by Grave Engine
    metal | angry | Score: 3.46 / 6.75
    Why:
      - genre match (+2.0)
      - mood match (+1.0)
      - energy close to target (+0.25)
      - valence close to target (+0.21)
      - tempo_bpm close to target (+0.00)

 2. Gym Hero  by Max Pulse
    pop | intense | Score: 0.70 / 6.75
    Why:
      - similar mood: intense (+0.5)
      - energy close to target (+0.20)
      - valence close to target (+0.00)
      - tempo_bpm close to target (+0.00)

 3. Storm Runner  by Voltline
    rock | intense | Score: 0.68 / 6.75
    Why:
      - similar mood: intense (+0.5)
      - energy close to target (+0.16)
      - valence close to target (+0.02)
      - tempo_bpm close to target (+0.00)

 4. Fuego Lento  by Los Brisas
    latin | energetic | Score: 0.56 / 6.75
    Why:
      - similar mood: energetic (+0.5)
      - energy close to target (+0.06)
      - valence close to target (+0.00)
      - tempo_bpm close to target (+0.00)

 5. Drop Zone  by Pulse Theory
    edm | euphoric | Score: 0.22 / 6.75
    Why:
      - energy close to target (+0.22)
      - valence close to target (+0.00)
      - tempo_bpm close to target (+0.00)

------------------------------------------------------------

============================================================
 Romantic Only: top 5 picks for 'jazz' / romantic / energy 0.50
============================================================

 1. Coffee Shop Stories  by Slow Stereo
    jazz | relaxed | Score: 3.30 / 6.75
    Why:
      - genre match (+2.0)
      - energy close to target (+1.30)

 2. Velvet Hours  by Sienna Rae
    r&b | romantic | Score: 2.50 / 6.75
    Why:
      - mood match (+1.0)
      - energy close to target (+1.50)

 3. Crossroads Whiskey  by Delta Moan
    blues | sad | Score: 1.42 / 6.75
    Why:
      - energy close to target (+1.42)

 4. Dusty Porch Swing  by Willow Creek Band
    country | nostalgic | Score: 1.42 / 6.75
    Why:
      - energy close to target (+1.42)

 5. Island Time  by Roots Harbor
    reggae | laid-back | Score: 1.38 / 6.75
    Why:
      - energy close to target (+1.38)

------------------------------------------------------------

============================================================
 Fence Sitter: top 5 picks for 'polka' / curious / energy 0.50
============================================================

 1. Velvet Hours  by Sienna Rae
    r&b | romantic | Score: 3.38 / 6.75
    Why:
      - energy close to target (+1.50)
      - valence close to target (+0.65)
      - danceability close to target (+0.39)
      - acousticness close to target (+0.40)
      - tempo_bpm close to target (+0.44)

 2. Dusty Porch Swing  by Willow Creek Band
    country | nostalgic | Score: 3.35 / 6.75
    Why:
      - energy close to target (+1.42)
      - valence close to target (+0.60)
      - danceability close to target (+0.43)
      - acousticness close to target (+0.41)
      - tempo_bpm close to target (+0.48)

 3. Midnight Coding  by LoRoom
    lofi | chill | Score: 3.31 / 6.75
    Why:
      - energy close to target (+1.38)
      - valence close to target (+0.70)
      - danceability close to target (+0.44)
      - acousticness close to target (+0.40)
      - tempo_bpm close to target (+0.39)

 4. Crossroads Whiskey  by Delta Moan
    blues | sad | Score: 3.27 / 6.75
    Why:
      - energy close to target (+1.42)
      - valence close to target (+0.60)
      - danceability close to target (+0.49)
      - acousticness close to target (+0.38)
      - tempo_bpm close to target (+0.38)

 5. Focus Flow  by LoRoom
    lofi | focused | Score: 3.24 / 6.75
    Why:
      - energy close to target (+1.35)
      - valence close to target (+0.68)
      - danceability close to target (+0.45)
      - acousticness close to target (+0.36)
      - tempo_bpm close to target (+0.40)

------------------------------------------------------------
```
