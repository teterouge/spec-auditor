  SPEC AUDIT REPORT                                                                                                                                                                                                                                Snake Game (MS-DOS Style / Nibbles Recreation)                                                                                                                                                                                                 
  Audit date: 2026-03-10                                                                                                                                                                                                                         

  ---
  SPRINT READINESS VERDICT

  🚫 Not ready — 2 blockers must be resolved. Sprint start not recommended.

  Top blocker: Section 9 lists five edge cases to handle but specifies the required behavior for none of them — engineers will implement divergent solutions, and at least one (apple spawning with no empty spaces) risks an infinite loop in   
  production.

  ---
  PASS 1: COMPLETENESS

  ┌────────────────────┬───────────┬───────────┬────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐    
  │       Field        │  Status   │ Severity  │                                                                                      Issue / Question                                                                                      │    
  ├────────────────────┼───────────┼───────────┼────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤    
  │ Success metrics    │ ❌        │ 🔴        │ All 8 success criteria in Section 11 are qualitative and untestable (see Pass 2). QA cannot produce a deterministic pass/fail result for any of them. What does "runs smoothly without     │    
  │                    │ Missing   │ Blocker   │ lag" mean in measurable terms?                                                                                                                                                             │    
  ├────────────────────┼───────────┼───────────┼────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤    
  │ Edge case          │ ❌        │ 🔴        │ Section 9 lists 5 edge cases as "to handle" but specifies no expected behavior for any of them. Engineering will make 5 independent implementation decisions. What is the specified        │    
  │ behaviors          │ Missing   │ Blocker   │ behavior for each?                                                                                                                                                                         │    
  ├────────────────────┼───────────┼───────────┼────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤    
  │ Error states       │ ❌        │ 🟡        │ No error states defined. At minimum: what happens if localStorage is unavailable (private browsing, storage quota exceeded, security policy)? Does the game still run? Does the high score │    
  │                    │ Missing   │ Warning   │  silently not persist?                                                                                                                                                                     │    
  ├────────────────────┼───────────┼───────────┼────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤    
  │ Initial game state │ ❌        │ 🟡        │ Snake starting position, starting direction, and starting speed are not defined. Where does the snake start? Which direction is it moving at game start?                                   │    
  │                    │ Missing   │ Warning   │                                                                                                                                                                                            │    
  ├────────────────────┼───────────┼───────────┼────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤    
  │ Actor/device       │ ⚠️        │ 🔵 Note   │ Section 7.4 rules out mobile, but no minimum viewport/resolution is defined. The 40×25 grid needs a minimum screen size to render legibly.                                                 │    
  │ context            │ Partial   │           │                                                                                                                                                                                            │    
  ├────────────────────┼───────────┼───────────┼────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤    
  │ Build tooling      │ ❌        │ 🔵 Note   │ "React" is specified but no build tooling (Vite, CRA, etc.) or React version is mentioned. React 18 StrictMode double-invokes effects — this will cause a duplicate game loop with         │    
  │                    │ Missing   │           │ setInterval unless explicitly handled.                                                                                                                                                     │    
  └────────────────────┴───────────┴───────────┴────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘    

  ---
  PASS 2: TESTABILITY

  ---
  Finding 1
  - Location: Section 11, Success Criterion 1
  - Original: "The game is playable from start to finish"
  - Issue: No definition of what constitutes a valid "start to finish" playthrough. Not deterministic — QA cannot reproduce a pass/fail result.
  - Rewritten: "A new game can be started from the Title screen, a snake of at least 5 segments can be grown by eating apples, and a Game Over screen is reached via wall or self-collision — all within a single uninterrupted session."        

  ---
  Finding 2
  - Location: Section 11, Success Criterion 2
  - Original: "All controls work as expected"
  - Issue: "As expected" by whom? Against what specification? This is circular.
  - Rewritten: "Arrow keys change snake direction per Section 3.2. Spacebar toggles Paused/Playing state. Enter key triggers a new game from the Game Over screen and navigates to the Title screen from the Title screen."

  ---
  Finding 3
  - Location: Section 11, Success Criterion 7
  - Original: "Game runs smoothly without lag or glitches"
  - Issue: "Smoothly," "lag," and "glitches" are undefined. Also contradicts Section 7.3 which specifies 60fps — a game ticking 10 times per second has no visible frames between ticks, making 60fps a meaningless target for this architecture.
  - Rewritten: "Game tick executes within ±5ms of the configured interval (default 100ms) as measured in Chrome DevTools Performance panel on a mid-range device. No frame is skipped during normal gameplay. The 60fps spec in Section 7.3
  should be removed or replaced with a tick-accuracy metric."

  ---
  Finding 4
  - Location: Section 11, Success Criterion 6
  - Original: "Visual design matches MS-DOS aesthetic"
  - Issue: Completely subjective. Two reviewers will disagree.
  - Rewritten: "All visual elements use only the specified CGA/EGA colors from Section 5.1. Box-drawing characters are used for all borders per Section 5.3. All text is rendered in a monospace font. Snake segments use █ or equivalent block  
  character. Apple uses ● or ◉."

  ---
  Finding 5
  - Location: Section 3.2, Movement
  - Original: "Movement speed: approximately 10 tiles per second (adjust for playability)"
  - Issue: "Approximately" and "adjust for playability" give developer complete discretion. QA cannot test against this.
  - Rewritten: "Movement speed defaults to 100ms per tick (10 tiles/second). This value is a named constant (TICK_INTERVAL_MS) in the codebase. No runtime speed adjustment is in scope for MVP."

  ---
  Finding 6
  - Location: Section 3.3, Apple Appearance
  - Original: "Apples should be visually distinct from the snake (different color/character)"
  - Issue: "Should" and "visually distinct" are subjective. The spec already defines specific colors in Section 5.1 — this AC is redundant and weaker than the actual spec.
  - Rewritten: "Apple is rendered using ● or ◉ in #FF0000. Snake segments are rendered in #00FF00. No snake segment or border character shares the apple's character or color."

  ---
  Finding 7
  - Location: Section 7.3
  - Original: "Optimize rendering to avoid unnecessary re-renders"
  - Issue: "Unnecessary" is undefined. This is an implementation suggestion, not a testable requirement.
  - Rewritten: Remove as an AC. If performance is a concern, specify: "The React component tree does not re-render components outside the GameBoard on each game tick, verified via React DevTools Profiler."

  ---
  Finding 8
  - Location: Section 5.2
  - Original: "All text should have the pixelated, retro feel"
  - Issue: "Pixelated, retro feel" is subjective and untestable.
  - Rewritten: "All text uses a CSS font-family stack of 'Courier New', Courier, monospace. No anti-aliasing CSS properties are applied to text elements. No serif or sans-serif fonts appear anywhere in the UI."

  ---
  PASS 3: AMBIGUITY

  ---
  Ambiguity 1
  - Location: Section 9, Edge Case 1 — "Rapid key presses that might reverse direction through intermediate states"
  - Ambiguity: Two standard implementations exist: (a) accept only the first direction change per tick, ignoring subsequent inputs until the tick fires; (b) queue the last valid direction input, processing one per tick. These produce        
  observably different gameplay feel.
  - Clarifying question: Should the input handler accept only one direction change per game tick (first wins), or should it queue the most recent valid direction change and apply it on the next tick?

  ---
  Ambiguity 2
  - Location: Section 9, Edge Case 5 — "Multiple key presses during a single game tick"
  - Ambiguity: This overlaps with Edge Case 1 but isn't identical. Could mean: holding a key vs. rapidly tapping. "Handle" is unspecified. Same two approaches apply, but the interaction with Edge Case 1 is unclear.
  - Clarifying question: Is this a duplicate of Edge Case 1, or is there a distinct scenario (e.g., holding down a key triggers key-repeat events)? If distinct, what is the expected behavior?

  ---
  Ambiguity 3
  - Location: Section 9, Edge Case 2 — "Apple spawning when snake is very long (limited empty spaces)"
  - Ambiguity: Three possible behaviors: (a) loop until a free cell is found (infinite loop risk when snake fills >95% of grid), (b) pick a pre-computed list of free cells, (c) trigger a win condition if no empty space exists.
  - Clarifying question: What is the expected behavior when no valid apple spawn position exists? Is there a win condition, or does the game continue without an apple?

  ---
  Ambiguity 4
  - Location: Section 6.2, Technical Requirements
  - Original: "Recommended approach: Use setInterval or requestAnimationFrame for the game loop"
  - Ambiguity: These two approaches have fundamentally different behavior when the browser tab is backgrounded. setInterval continues firing (game state advances while invisible). rAF pauses (game freezes while tab is hidden). Neither       
  behavior is specified as correct.
  - Clarifying question: Should the game pause automatically when the tab is backgrounded, or continue running?

  ---
  Ambiguity 5
  - Location: Section 4.1
  - Original: "40 columns × 25 rows (adjustable for screen size considerations)"
  - Ambiguity: Who adjusts this, under what conditions, and within what range? Two engineers will interpret this as either (a) a fixed constant they can tweak pre-launch, or (b) a responsive layout that recalculates at runtime.
  - Clarifying question: Is the grid size a fixed build-time constant for MVP, or should it respond dynamically to viewport size? If responsive, what are the minimum and maximum dimensions?

  ---
  Ambiguity 6
  - Location: Section 8 / Section 3.5
  - Ambiguity: The localStorage key name for the high score is not specified. Two engineers or two future iterations could write to different keys, silently breaking persistence.
  - Clarifying question: What is the exact localStorage key to use for the high score? (e.g., "snakeHighScore", "nibbles_high_score", etc.)

  ---
  Ambiguity 7
  - Location: Section 5.3, Snake Rendering
  - Original: "Snake head can optionally be distinguished from body segments"
  - Ambiguity: "Optionally" means this is not a requirement. But it's in the spec under Visual Elements, implying it might be expected. Engineers will disagree on whether to implement it.
  - Clarifying question: Is distinguishing the snake head from the body a requirement or explicitly out of scope for MVP? If in scope, what character or color distinguishes it?

  ---
  PASS 4: ASSUMPTIONS

  ---
  - Assumption: localStorage is available and writable in the user's browser environment.
  - Category: System behavior
  - Action required: Document fallback behavior. The game must still be playable if localStorage throws. Confirm: is a silent no-op (no high score persists) acceptable, or should the user see an error?

  ---
  - Assumption: The user's browser renders Unicode block characters (█, ●, ◉, ╔, ╝, etc.) correctly using the specified monospace font stack.
  - Category: Platform
  - Action required: Confirm. Misrendering of box-drawing characters is common on Windows with certain font fallbacks. Validate visually across Chrome, Firefox, Safari, Edge on both Windows and macOS.

  ---
  - Assumption: The viewport is large enough to display a 40×25 character grid at a legible size without scrolling.
  - Category: Platform
  - Action required: Define the minimum supported viewport width and height. Specify behavior if the viewport is too small (scale down? scroll? show a message?).

  ---
  - Assumption: React version is current enough to support all hooks used, but no specific version is pinned.
  - Category: System behavior
  - Action required: Pin a minimum React version. If React 18, note that StrictMode double-invokes useEffect in development — a bare setInterval in useEffect will create two game loops. This needs an explicit cleanup return or a guard.      

  ---
  - Assumption: The snake always begins at a fixed or predictable position and direction at game start.
  - Category: Sequence/state
  - Action required: Add to spec: starting position (e.g., center of grid), starting direction (e.g., moving right), starting length (Section 3.2 says 3 — confirmed).

  ---
  - Assumption: There is no win condition. The game only ends via collision.
  - Category: System behavior
  - Action required: Confirm explicitly. Edge Case 2 (apple spawning with no room) suggests a scenario where the snake fills the board — is that a win? The spec doesn't say.

  ---
  PASS 5: SCOPE RISKS

  ---
  Risk 1
  - Original: "approximately 10 tiles per second (adjust for playability)"
  - Risk: Minimum: one hardcoded constant, never touched. Maximum: developer implements a tunable speed system, playtests multiple values, potentially adds difficulty ramping not in scope.
  - Bounded rewrite: "Default tick interval is 100ms (10 tiles/second), defined as a single named constant TICK_INTERVAL_MS = 100. This value is not adjusted at runtime and not exposed as a user setting in MVP."

  ---
  Risk 2
  - Original: "40 columns × 25 rows (adjustable for screen size considerations)"
  - Risk: Minimum: fixed 40×25 grid, no responsive behavior. Maximum: fully responsive layout recalculating grid dimensions on resize, multiple breakpoints, CSS media queries.
  - Bounded rewrite: "Grid is fixed at 40 columns × 25 rows for MVP. No responsive resizing is implemented. If the viewport is narrower than the minimum required width, the game renders at its fixed size and the page scrolls horizontally."  

  ---
  Risk 3
  - Original: "Optimize rendering to avoid unnecessary re-renders"
  - Risk: Minimum: no optimization, rely on React's default behavior. Maximum: full profiling session, canvas migration, virtualization of unchanged cells.
  - Bounded rewrite: Remove from spec. If a rendering performance requirement exists, specify it measurably (e.g., "no re-render of components outside GameBoard on each tick, confirmed via React DevTools"). Otherwise, treat performance as a 
  post-MVP concern.

  ---
  Risk 4
  - Original: "Must work in modern browsers (Chrome, Firefox, Safari, Edge)"
  - Risk: Minimum: latest stable version of each. Maximum: N years of version support for all four browsers, including testing matrix.
  - Bounded rewrite: "Must work in the current stable release of Chrome, Firefox, Safari, and Edge at time of delivery. No support for previous versions is required."

  ---
  Risk 5
  - Original: "Optional: Brief instructions" (on Title Screen)
  - Risk: Minimum: no instructions at all (it's optional). Maximum: full help screen with control diagram, rules explanation, and scoring guide.
  - Bounded rewrite: Either remove "Optional: Brief instructions" entirely, or specify: "Title screen displays one line of control instructions: ARROW KEYS: Move  |  SPACE: Pause  |  ENTER: Start."

  ---
  Risk 6
  - Original: "All text should have the pixelated, retro feel"
  - Risk: Minimum: monospace font, done. Maximum: custom pixel/bitmap font loaded via @font-face, CSS image-rendering: pixelated, scanline overlay effects, CRT shader.
  - Bounded rewrite: "All text uses font-family: 'Courier New', Courier, monospace. No custom font loading, CSS filter effects, or canvas post-processing is in scope for MVP."

  ---
  SUMMARY

  ┌────────────────┬───────┐
  │    Severity    │ Count │
  ├────────────────┼───────┤
  │ 🔴 Blockers    │ 2     │
  ├────────────────┼───────┤
  │ 🟡 Warnings    │ 5     │
  ├────────────────┼───────┤
  │ 🔵 Notes       │ 3     │
  ├────────────────┼───────┤
  │ Total findings │ 10    │
  └────────────────┴───────┘

  Recommended next action: Before anything else, answer the five edge case behaviors in Section 9 — especially the input queue strategy (Edge Case 1/5) and the apple exhaustion scenario (Edge Case 2) — because those two will drive divergent 
  architecture decisions on day one of the sprint.

  ---
  Bottom line for the PM: This spec is well-structured and covers the happy path thoroughly. The visual design and out-of-scope sections are strong. What's missing is the behavior under failure/edge conditions and measurable done criteria.  
  Fix those two areas and this is ready.