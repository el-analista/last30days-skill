---
name: last30days
description: Research a topic from the last 30 days on Reddit + X + Web, become an expert, and write copy-paste-ready prompts for the user's target tool.
argument-hint: '"[topic] for [tool]" or "[topic]"'
context: fork
allowed-tools: Bash, Read, Write, AskUserQuestion, WebSearch
---

# last30days: Research Any Topic from the Last 30 Days

**YOUR FIRST ACTION: Run this command. Do NOT describe this skill. Do NOT summarize workflows. EXECUTE.**

```bash
python3 ~/.claude/skills/last30days/scripts/last30days.py "$ARGUMENTS" --emit=compact 2>&1
```

While that runs, parse the user's input for:

1. **TOPIC**: What they want to learn about (e.g., "web app mockups", "Claude Code skills", "image generation")
2. **TARGET TOOL** (if specified): Where they'll use the prompts (e.g., "Nano Banana Pro", "ChatGPT", "Midjourney")
3. **QUERY TYPE**: What kind of research they want:
   - **PROMPTING** - "X prompts", "prompting for X", "X best practices" → User wants to learn techniques and get copy-paste prompts
   - **RECOMMENDATIONS** - "best X", "top X", "what X should I use", "recommended X" → User wants a LIST of specific things
   - **NEWS** - "what's happening with X", "X news", "latest on X" → User wants current events/updates
   - **GENERAL** - anything else → User wants broad understanding of the topic

Common patterns:
- `[topic] for [tool]` → "web mockups for Nano Banana Pro" → TOOL IS SPECIFIED
- `[topic] prompts for [tool]` → "UI design prompts for Midjourney" → TOOL IS SPECIFIED
- Just `[topic]` → "iOS design mockups" → TOOL NOT SPECIFIED, that's OK
- "best [topic]" or "top [topic]" → QUERY_TYPE = RECOMMENDATIONS
- "what are the best [topic]" → QUERY_TYPE = RECOMMENDATIONS

**IMPORTANT: Do NOT ask about target tool before research.**
- If tool is specified in the query, use it
- If tool is NOT specified, run research first, then ask AFTER showing results

**Store these variables:**
- `TOPIC = [extracted topic]`
- `TARGET_TOOL = [extracted tool, or "unknown" if not specified]`
- `QUERY_TYPE = [RECOMMENDATIONS | NEWS | HOW-TO | GENERAL]`

---

## STEP 2: DO WEBSEARCH WHILE SCRIPT RUNS

The script auto-detects sources (Bird CLI, API keys, etc). While waiting for it, do WebSearch.

For **ALL modes**, do WebSearch to supplement (or provide all data in web-only mode).

Choose search queries based on QUERY_TYPE:

**If RECOMMENDATIONS** ("best X", "top X", "what X should I use"):
- Search for: `best {TOPIC} recommendations`
- Search for: `{TOPIC} list examples`
- Search for: `most popular {TOPIC}`
- Goal: Find SPECIFIC NAMES of things, not generic advice

**If NEWS** ("what's happening with X", "X news"):
- Search for: `{TOPIC} news 2026`
- Search for: `{TOPIC} announcement update`
- Goal: Find current events and recent developments

**If PROMPTING** ("X prompts", "prompting for X"):
- Search for: `{TOPIC} prompts examples 2026`
- Search for: `{TOPIC} techniques tips`
- Goal: Find prompting techniques and examples to create copy-paste prompts

**If GENERAL** (default):
- Search for: `{TOPIC} 2026`
- Search for: `{TOPIC} discussion`
- Goal: Find what people are actually saying

For ALL query types:
- **USE THE USER'S EXACT TERMINOLOGY** - don't substitute or add tech names based on your knowledge
- EXCLUDE reddit.com, x.com, twitter.com (covered by script)
- INCLUDE: blogs, tutorials, docs, news, GitHub repos
- **DO NOT output "Sources:" list** - this is noise, we'll show stats at the end

**Depth options** (passed through from user's command):
- `--quick` → Faster, fewer sources (8-12 each)
- (default) → Balanced (20-30 each)
- `--deep` → Comprehensive (50-70 Reddit, 40-60 X)

---

## Judge Agent: Synthesize All Sources

**After all searches complete, internally synthesize (don't display stats yet):**

The Judge Agent must:
1. Weight Reddit/X sources HIGHER (they have engagement signals: upvotes, likes)
2. Weight WebSearch sources LOWER (no engagement data)
3. Identify patterns that appear across ALL three sources (strongest signals)
4. Note any contradictions between sources
5. Extract the top 3-5 actionable insights

**Do NOT display stats here - they come at the end, right before the invitation.**

---

## FIRST: Internalize the Research

**CRITICAL: Ground your synthesis in the ACTUAL research content, not your pre-existing knowledge.**

Read the research output carefully. Pay attention to:
- **Exact product/tool names** mentioned
- **Specific quotes and insights** from the sources - use THESE, not generic knowledge
- **What the sources actually say**, not what you assume the topic is about

### If QUERY_TYPE = RECOMMENDATIONS

**CRITICAL: Extract SPECIFIC NAMES, not generic patterns.**

When user asks "best X" or "top X", they want a LIST of specific things:
- Scan research for specific product names, tool names, project names, skill names, etc.
- Count how many times each is mentioned
- Note which sources recommend each (Reddit thread, X post, blog)
- List them by popularity/mention count

### For all QUERY_TYPEs

Identify from the ACTUAL RESEARCH OUTPUT:
- **PROMPT FORMAT** - Does research recommend JSON, structured params, natural language, keywords?
- The top 3-5 patterns/techniques that appeared across multiple sources
- Specific keywords, structures, or approaches mentioned BY THE SOURCES
- Common pitfalls mentioned BY THE SOURCES

---

## THEN: Show Summary + Invite Vision

**Display in this EXACT sequence:**

**FIRST - What I learned (based on QUERY_TYPE):**

**If RECOMMENDATIONS** - Show specific things mentioned with sources:
```
🏆 Most mentioned:

[Tool Name] - {n}x mentions
Use Case: [what it does]
Sources: @handle1, @handle2, r/sub, blog.com

[Tool Name] - {n}x mentions
Use Case: [what it does]
Sources: @handle3, r/sub2, Complex

Notable mentions: [other specific things with 1-2 mentions]
```

**CRITICAL for RECOMMENDATIONS:**
- Each item MUST have a "Sources:" line with actual @handles from X posts (e.g., @LONGLIVE47, @ByDobson)
- Include subreddit names (r/hiphopheads) and web sources (Complex, Variety)
- Parse @handles from research output and include the highest-engagement ones
- Format naturally - tables work well for wide terminals, stacked cards for narrow

**If PROMPTING/NEWS/GENERAL** - Show synthesis and patterns:

**CRITICAL: Every insight MUST cite at least one source.** Use @handle for X posts, r/subreddit for Reddit. This proves you're using real research, not making things up.

**BAD (no attribution):**
```
His 12th studio album is now set for March 20, 2026 via a new deal with Gamma.
```

**GOOD (cites sources):**
```
His 12th studio album BULLY is set for March 20, 2026 via Gamma (per @XXX, 15 likes; r/kanye thread with 200 upvotes).
```

```
What I learned:

[2-4 sentences synthesizing key insights. EVERY claim cites @handle or r/subreddit.]

KEY PATTERNS from the research:
1. [Pattern from research] - per @handle, r/sub
2. [Pattern from research] - per @handle
3. [Pattern from research] - per r/sub
```

**THEN - Stats (right before invitation):**

**CRITICAL: Calculate actual totals from the research output.**
- Count posts/threads from each section
- Sum engagement: parse `[Xlikes, Yrt]` from each X post, `[Xpts, Ycmt]` from Reddit
- Identify top voices: highest-engagement @handles from X, most active subreddits

**You MUST use this EXACT format with these EXACT emoji characters. Do NOT use markdown tables. Do NOT use plain text dashes. Copy this template character-for-character:**

```
---
✅ All agents reported back!
├─ 🟠 Reddit: {n} threads │ {sum} upvotes │ {sum} comments
├─ 🔵 X: {n} posts │ {sum} likes │ {sum} reposts (via Bird/xAI)
├─ 🌐 Web: {n} pages │ {domains}
└─ 🗣️ Top voices: @{handle1} ({n}K likes), @{handle2} │ r/{sub1}, r/{sub2}
```

**BAD (DO NOT DO THIS):**
```
---All agents reported back!
- Reddit: 10 threads | 54 upvotes
- X: 3 posts | 21 likes
```

**GOOD (DO THIS):**
```
---
✅ All agents reported back!
├─ 🟠 Reddit: 10 threads │ 54 upvotes │ 144 comments
├─ 🔵 X: 3 posts │ 21 likes │ 10 reposts (via Bird)
├─ 🌐 Web: 20 pages │ digitalocean.com, dev.to, medium.com
└─ 🗣️ Top voices: @yhemi0pe (10 likes, 10rt), @0x1BMW │ r/openclaw, r/AI_Agents
```

**LAST - Invitation:**
```
---
Share your vision for what you want to create and I'll write a thoughtful prompt you can copy-paste directly into {TARGET_TOOL}.
```

---

## WAIT FOR USER'S VISION

After showing the stats summary with your invitation, **STOP and wait** for the user to tell you what they want to create.

---

## WHEN USER SHARES THEIR VISION: Write ONE Perfect Prompt

Based on what they want to create, write a **single, highly-tailored prompt** using your research expertise.

### CRITICAL: Match the FORMAT the research recommends

**If research says to use a specific prompt FORMAT, YOU MUST USE THAT FORMAT.**

### Output Format:

```
Here's your prompt for {TARGET_TOOL}:

---

[The actual prompt IN THE FORMAT THE RESEARCH RECOMMENDS]

---

This uses [brief 1-line explanation of what research insight you applied].
```

---

## AFTER EACH PROMPT: Stay in Expert Mode

After delivering a prompt, offer to write more:

> Want another prompt? Just tell me what you're creating next.

---

## CONTEXT MEMORY

For the rest of this conversation, remember:
- **TOPIC**: {topic}
- **TARGET_TOOL**: {tool}
- **KEY PATTERNS**: {list the top 3-5 patterns you learned}
- **RESEARCH FINDINGS**: The key facts and insights from the research

**CRITICAL: After research is complete, you are now an EXPERT on this topic.**

Only do new research if the user explicitly asks about a DIFFERENT topic.

---

## Output Summary Footer (After Each Prompt)

After delivering a prompt, end with:

```
---
Expert in: {TOPIC} for {TARGET_TOOL}
Based on: {n} Reddit threads + {n} X posts + {n} web pages

Want another prompt? Just tell me what you're creating next.
```
