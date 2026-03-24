# Language Style Fingerprint Analyzer - Test Cases

Use these test cases to demonstrate the analyzer's capabilities across different writing styles and edge cases.

---

## 1. Academic Style

**Expected:** High academic score, complex vocabulary, long sentences, noun-heavy

```
The epistemological foundations of contemporary cognitive science necessitate a thorough examination of the relationship between neural substrates and phenomenological experience. Furthermore, the integration of computational models with empirical neuroscientific data has yielded unprecedented insights into the mechanisms underlying human cognition. These interdisciplinary approaches have fundamentally transformed our understanding of consciousness and its neural correlates, establishing new paradigms for investigating the mind-brain relationship.
```

---

## 2. Conversational Style

**Expected:** High conversational score, short sentences, informal tone

```
Hey, so I was thinking about this the other day. You know how it goes, right? Things just happen sometimes. I mean, we can't really control everything. That's just life. Anyway, I wanted to tell you about this cool thing I found. It's pretty amazing actually. You should totally check it out when you get a chance.
```

---

## 3. Descriptive Style

**Expected:** High descriptive score, rich in adjectives and adverbs

```
The ancient, weathered lighthouse stood majestically atop the rugged, wind-swept cliff. Its brilliant, golden beam swept slowly across the dark, turbulent waters below. The salty, crisp air carried the hauntingly beautiful sound of crashing waves against the jagged, moss-covered rocks. Delicate, white seabirds circled gracefully overhead, their melodic cries echoing through the misty, grey evening sky.
```

---

## 4. Narrative Style

**Expected:** High narrative score, verb-heavy, pronoun usage, story-telling

```
She walked into the room and immediately noticed something was wrong. The furniture had been moved, and papers were scattered everywhere. She picked up a torn photograph from the floor and examined it closely. Her heart began to race as she recognized the faces. Without hesitation, she grabbed her phone and called her brother. He answered on the second ring, and she told him everything she had discovered.
```

---

## 5. Technical Style

**Expected:** High technical score, jargon-heavy, specific terminology

```
The API endpoint accepts POST requests with JSON payloads containing authentication tokens. Server-side validation ensures data integrity through SHA-256 hashing algorithms. The microservices architecture utilizes containerized deployment via Kubernetes orchestration. Database transactions implement ACID compliance through PostgreSQL's native support for serializable isolation levels. Load balancing distributes traffic across multiple replicated instances.
```

---

## 6. Persuasive Style

**Expected:** High persuasive score, action verbs, direct address

```
You deserve better than what you're settling for right now. Think about it. Every day you wait is another day wasted. Take action today and transform your life completely. Don't let fear hold you back any longer. Join thousands of others who have already made the leap. Your future self will thank you for making this decision. Act now before this opportunity disappears forever.
```

---

## 7. Journalistic Style

**Expected:** High journalistic score, balanced structure, factual tone

```
Local authorities announced yesterday that the new community center will open next month. The facility, which cost approximately three million dollars to construct, will offer various programs for residents of all ages. Mayor Johnson stated that the project represents a significant investment in the community's future. Construction began eighteen months ago following years of planning and public consultation. Officials expect the center to serve over two thousand residents annually.
```

---

## 8. Creative Style

**Expected:** High creative score, varied sentence lengths, high lexical diversity

```
Whispers. The clock struck midnight and everything changed. She remembered blue skies and forgotten promises, tangled together like autumn leaves dancing in a hurricane. Time folded in on itself. Perhaps reality was merely a suggestion, a half-remembered dream slipping through consciousness like water through cupped hands. The universe winked, and suddenly nothing mattered except the extraordinary ordinariness of breathing.
```

---

## 9. Mixed Style (Academic + Technical)

**Expected:** Mixed or Varied classification showing multiple high scores

```
The implementation of machine learning algorithms in bioinformatics has revolutionized genomic sequence analysis. Convolutional neural networks, particularly those utilizing residual connections, demonstrate superior performance in protein structure prediction tasks. The computational complexity of these models necessitates distributed processing architectures, typically leveraging GPU clusters for parallel computation. Recent publications in Nature have validated these methodological approaches through extensive empirical evaluation.
```

---

## 10. Mixed Style (Narrative + Descriptive)

**Expected:** Mixed classification with narrative and descriptive elements

```
He stepped into the magnificent, sunlit garden and immediately felt the warm, gentle breeze caress his weathered face. Ancient, towering oak trees swayed peacefully overhead as he walked slowly along the winding, cobblestone path. He remembered coming here as a child, running through these same beautiful, fragrant flowerbeds. Now everything seemed smaller, yet somehow more precious and wonderfully nostalgic than before.
```

---

## Edge Cases

### 11. Insufficient Text (< 10 words)

**Expected:** "Insufficient Text" error message

```
Hello world.
```

```
This is short.
```

```
Testing the analyzer.
```

---

### 12. Low Confidence (10-30 words)

**Expected:** Analysis with "Low Confidence" warning

```
The quick brown fox jumps over the lazy dog. It runs fast through the green meadow.
```

```
Technology changes everything. We must adapt quickly to survive in the modern digital world today.
```

---

### 13. Indeterminate Style (Neutral text)

**Expected:** Low scores across all categories, possibly "Indeterminate"

```
Items are on the table. The door is open. Water is in the glass. Books are on the shelf. The light is on. Papers are in the folder. Keys are in the drawer. Food is in the fridge.
```

---

## Quick Reference: Expected Dominant Styles

| Test Case | Primary Style | Secondary Style |
|-----------|--------------|-----------------|
| 1 | Academic | Technical |
| 2 | Conversational | - |
| 3 | Descriptive | Creative |
| 4 | Narrative | - |
| 5 | Technical | Academic |
| 6 | Persuasive | Conversational |
| 7 | Journalistic | - |
| 8 | Creative | Descriptive |
| 9 | Mixed/Varied | Academic + Technical |
| 10 | Mixed/Varied | Narrative + Descriptive |
| 11 | Insufficient Text | N/A |
| 12 | Varies | Low Confidence Warning |
| 13 | Indeterminate | N/A |

---

## Running the Demo

1. Start the application:
   ```bash
   cd /home/james-murithi/Downloads/projects/language_style_analyser/Language-Style-Analyser
   source .venv/bin/activate
   streamlit run app.py
   ```

2. Copy and paste each test case into the text input area

3. Click "Analyze" to see the linguistic fingerprint

4. Compare the results with expected outcomes listed above
