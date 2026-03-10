● ---                                                                                                                                                                                                                                            
  SPEC AUDIT REPORT     
  Snake Game (MS-DOS Style) — Nibbles PRD                                                                                                                                                                                                        
  Audit date: 2026-03-10                                                                                                                                                                                                                                                                                                                                                                                                                                                                          
  ---                                                                                                                                                                                                                                            
  SPRINT READINESS VERDICT

  ⚠️ Ready with fixes — 1 blocker and 5 warnings require PM response before sprint start. Core mechanics are well-defined, but edge case behaviors are listed without specified resolutions and success criteria are almost entirely untestable. 

  Top blocker: Apple spawn exhaustion (edge case #2) is acknowledged but left completely unresolved — the game will exhibit undefined or broken behavior when the snake fills the grid.

  ---
  PASS 1: COMPLETENESS

  ┌────────────────────┬─────────────────────┬───────────┬──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐    
  │       Field        │       Status        │ Severity  │                                                                                 Issue / Question                                                                                 │    
  ├────────────────────┼─────────────────────┼───────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤    
  │ Problem statement  │ Missing             │ 🔵 Note   │ No user problem defined — spec goes straight to solution. Acceptable for an internal game build, but worth a one-liner.                                                          │    
  ├────────────────────┼─────────────────────┼───────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤    
  │ Success metrics    │ Vague/circular      │ 🟡        │ Section 11 lists acceptance criteria disguised as success metrics. None are measurable. QA will have no basis for sign-off. See Pass 2 for full breakdown.                       │    
  │                    │                     │ Warning   │                                                                                                                                                                                  │    
  ├────────────────────┼─────────────────────┼───────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤    
  │ Edge case          │ Defined but         │ 🔴        │ Section 9 lists 5 edge cases but specifies handling for none of them. Engineers will invent independent solutions. Input handling in particular (items 1 and 5) is a core        │    
  │ behaviors          │ unresolved          │ Blocker   │ gameplay mechanic decision that can't be left to individual judgment.                                                                                                            │    
  ├────────────────────┼─────────────────────┼───────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤    
  │ Error states       │ Missing             │ 🟡        │ No behavior specified for: localStorage unavailable (private browsing, quota exceeded), apple spawn with zero remaining empty cells, or game loop failure.                       │    
  │                    │                     │ Warning   │                                                                                                                                                                                  │    
  ├────────────────────┼─────────────────────┼───────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤    
  │ Rollback / kill    │ N/A                 │ —         │ Static client-side app — not applicable.                                                                                                                                         │    
  │ switch             │                     │           │                                                                                                                                                                                  │    
  └────────────────────┴─────────────────────┴───────────┴──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘    

  ---
  PASS 2: TESTABILITY

  Success Criteria (Section 11) — 7 of 8 items are untestable as written.

  ---
  - Location: Section 11, criterion 1
  - Original: "The game is playable from start to finish"
  - Issue: "Playable" is undefined. A game that crashes 50% of the time could technically be "playable."
  - Rewritten: "A player can complete a full game session: Title → Playing (eating ≥1 apple) → Game Over → Restart → Playing, without errors or unresponsive states."

  ---
  - Location: Section 11, criterion 2
  - Original: "All controls work as expected"
  - Issue: "As expected" is circular — it references no defined behavior.
  - Rewritten: "Arrow keys change snake direction per Section 3.2. Spacebar toggles Paused/Playing state. Enter transitions Title→Playing and GameOver→Title. No other keys affect game state."

  ---
  - Location: Section 11, criterion 3
  - Original: "Collision detection is accurate"
  - Issue: No definition of accuracy. Accurate to the pixel? To the grid cell?
  - Rewritten: "Game Over is triggered on the tick where the snake's head position (grid coordinates) matches any wall boundary cell or any occupied snake body cell. No false positives (game over without collision) or false negatives        
  (collision without game over) occur in a 10-minute play session."

  ---
  - Location: Section 11, criterion 6
  - Original: "Visual design matches MS-DOS aesthetic"
  - Issue: Purely subjective. QA cannot test this without a reference image or explicit checklist.
  - Rewritten: "Visual design uses the color values in Section 5.1, box-drawing characters in Section 5.3, and Courier New (or equivalent monospace). A side-by-side comparison with the UI layout wireframe in Section 5.3 is the acceptance    
  standard."

  ---
  - Location: Section 11, criterion 7
  - Original: "Game runs smoothly without lag or glitches"
  - Issue: No performance threshold, hardware baseline, or definition of "glitch."
  - Rewritten: "Game maintains a consistent 100ms tick interval (±10ms) for the duration of a session, measured in Chrome on a mid-range laptop (e.g., 4-core, 8GB RAM). No dropped frames observable to the naked eye during snake movement."

  ---
  - Location: Section 3.2, Movement
  - Original: "Movement speed: approximately 10 tiles per second (adjust for playability)"
  - Issue: "Approximately" and "adjust for playability" give no fixed target. Engineers will each pick a different number.
  - Rewritten: "Default tick interval: 100ms (10 tiles/second). Speed is fixed for MVP — no in-game speed changes."

  ---
  - Location: Section 5.2, Typography
  - Original: "All text should have the pixelated, retro feel"
  - Issue: Unmeasurable aesthetic outcome.
  - Rewritten: "All text uses Courier New at sizes specified per UI element (see Section 5.3). No additional CSS effects (filters, shadows, transforms) are required for MVP."

  ---
  PASS 3: AMBIGUITY

  ---
  - Location: Section 9, items 1 and 5
  - Ambiguity: "Rapid key presses that might reverse direction" and "Multiple key presses during a single game tick" — two divergent implementations: (A) queue the last valid key press and apply it on the next tick, or (B) discard all but   
  the most recent input per tick.
  - Clarifying question: When two direction keys are pressed within the same 100ms tick, which input wins? Should the game maintain an input queue across ticks, or process only the last key received before each tick executes?

  ---
  - Location: Section 9, item 2
  - Ambiguity: "Apple spawning when snake is very long (limited empty spaces)" — two interpretations: (A) the game gracefully handles this and continues, or (B) this is implicitly a win condition / edge case that can be deferred.
  - Clarifying question: What is the expected behavior if the snake occupies all 1,000 grid cells and there is no valid spawn position for the apple? Does the player win, does the game freeze, or is this out of scope for MVP?

  ---
  - Location: Section 3.4, Collision Detection
  - Ambiguity: "Snake head collides with any part of its own body" — the segment immediately behind the head moves away on the same tick the head advances. Some implementations allow this (neck is vacated before collision check); others     
  treat it as a collision.
  - Clarifying question: Is moving the snake's head into the cell previously occupied by segment 2 (the neck) a game-over collision?

  ---
  - Location: Section 4.1
  - Ambiguity: "40 columns × 25 rows (adjustable for screen size considerations)" — "adjustable" could mean (A) fixed at 40×25 with CSS scaling, or (B) a responsive grid that recalculates tile count on viewport resize.
  - Clarifying question: Is the grid always 40×25 tiles regardless of screen size (with CSS scaling the tile size), or should the grid dimensions change based on the viewport?

  ---
  - Location: Section 5.1, Color Palette
  - Ambiguity: "Blue or cyan" and "Light gray or white" have no hex values. "Bright green or lime" provides #00FF00 but the "or" implies optionality. Engineer will make an arbitrary color choice.
  - Clarifying question: Should exact hex values be specified for all UI colors? At minimum, which should it be for boundaries: blue (#0000FF, #0000AA) or cyan (#00FFFF)?

  ---
  - Location: Section 7.4 vs. Section 10
  - Ambiguity: Section 7.4 says "Must work in modern browsers (Chrome, Firefox, Safari, Edge)." Section 10 says "No mobile support required for MVP." Mobile Safari is a modern browser. If someone opens the game on an iPhone, is broken       
  rendering acceptable?
  - Clarifying question: Is mobile Safari in scope for browser compatibility? If not, should the page display a "desktop only" message on mobile viewports?

  ---
  PASS 4: ASSUMPTIONS

  ---
  - Assumption: localStorage is available and writable in all target browser sessions.
  - Category: System behavior
  - Action required: Confirm — specify fallback behavior. Private browsing on Safari throws a SecurityError on localStorage access. Minimum: wrap in try/catch and silently skip high score persistence. This needs to be an explicit decision,  
  not left to the engineer.

  ---
  - Assumption: Arrow keys will be captured by the game and not intercepted by the browser (e.g., page scrolling).
  - Category: Platform
  - Action required: Document — event.preventDefault() on arrow key events is required to prevent page scroll. This is a known gotcha that should be called out explicitly rather than discovered in QA.

  ---
  - Assumption: The tab/window will remain focused during gameplay; background tab behavior is unspecified.
  - Category: System behavior
  - Action required: Confirm — setInterval degrades when the tab is backgrounded (Chrome throttles to ~1/second). requestAnimationFrame pauses entirely. The spec recommends both without distinguishing them. Should the game auto-pause when   
  the tab loses focus? This is distinct from the Spacebar pause mechanic.

  ---
  - Assumption: Unicode box-drawing characters (╔, ═, ║, etc.) render consistently in the target font.
  - Category: Platform
  - Action required: Document — Courier New on Windows renders these correctly; on macOS the rendering varies. If cross-platform visual consistency matters, call out a specific fallback or use CSS borders instead.

  ---
  - Assumption: React version is unspecified; hooks availability assumed.
  - Category: System behavior
  - Action required: Document — Pin to React 18+ (or minimum 16.8) in the tech stack section. This prevents an engineer from picking up an older project boilerplate.

  ---
  PASS 5: SCOPE RISKS

  ---
  - Original: "Optimize rendering to avoid unnecessary re-renders" (Section 7.3)
  - Risk: Minimum = don't do obviously wasteful full-page re-renders. Maximum = full profiling pass, React.memo everywhere, useMemo on every derived value, potential canvas migration.
  - Bounded rewrite: "The game board component re-renders only when snake position, apple position, or score changes. No performance profiling or memoization beyond this is required for MVP."

  ---
  - Original: "40 columns × 25 rows (adjustable for screen size considerations)" (Section 4.1)
  - Risk: Minimum = fixed 40×25 with no adjustment. Maximum = fully responsive grid that recalculates dimensions on every resize event, with new collision boundaries and apple repositioning logic.
  - Bounded rewrite: "Grid is fixed at 40×25 tiles. Tile size is fixed at [N]px. No responsive resizing logic required for MVP. On viewports smaller than the game's rendered width, the game may be partially clipped — no overflow handling    
  required."

  ---
  - Original: "Use a monospace font that resembles MS-DOS system font" (Section 5.2)
  - Risk: Minimum = Courier New, which ships with all target browsers. Maximum = loading a custom pixel/bitmap font (e.g., Perfect DOS VGA, Press Start 2P), adding a @font-face declaration, handling font load states.
  - Bounded rewrite: "Use Courier New. No custom font loading is required. Do not use Google Fonts or any external font CDN for MVP."

  ---
  - Original: "Implement a game loop that... Redraws the game screen" with "Recommended approach: Use setInterval or requestAnimationFrame" (Section 6.2)
  - Risk: These two have fundamentally different behaviors: rAF pauses in background tabs; setInterval is throttled. Leaving the choice open means inconsistent behavior across environments and potential conflict with the 60fps target in     
  Section 7.3.
  - Bounded rewrite: "Implement the game loop using setInterval at a 100ms interval. Do not use requestAnimationFrame. The game does not need to maintain frame rate when the tab is backgrounded."

  ---
  SUMMARY

  - 🔴 Blockers: 1
  - 🟡 Warnings: 5
  - 🔵 Notes: 1
  - Total findings: 19

  Recommended next actions (ranked by severity):

  1. Structural — Resolve all Section 9 edge case behaviors before sprint start. The spec names 5 edge cases but specifies handling for zero of them. Input queuing behavior and apple spawn exhaustion are core mechanic decisions that
  different engineers will implement incompatibly; these must be resolved, not left as implementation detail.
  2. Sprint Risk — Rewrite Section 11 Success Criteria as testable acceptance criteria. 7 of 8 items are untestable as written. QA will have no objective basis for sprint sign-off, which means sign-off becomes a subjective negotiation at the
   end of the sprint rather than a checklist.
  3. Scope — Bound the grid sizing and rendering optimization requirements explicitly. "Adjustable for screen size" and "optimize rendering" are the two highest-risk scope-expansion phrases in the spec. Both need a ceiling added before the  
  engineer starts, or they will either under-deliver or over-engineer.

    ---
  Bottom line for the PM: This spec is well-structured and covers the happy path thoroughly. The visual design and out-of-scope sections are strong. What's missing is the behavior under failure/edge conditions and measurable done criteria.  
  Fix those two areas and this is ready.

    ---
  Bottom line for the PM: This is a strong architecture document and a useful team-alignment artifact. But it's not a PRD engineering can act on. The gap between "here are the services and tech stack" and "here is what done looks like for   
  each feature" is where this spec currently lives. The three things that will unblock sprint start fastest: (1) a bounded MVP scope, (2) ACs for Phase 1 deliverables only, and (3) legal review of the voice cloning feature before a single   
  line of that service is written.