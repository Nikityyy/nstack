---
name: resume-live-work
description: Recover the active task and any running job after a cold pickup, provider change, interruption, or planned pause. Use when the next action depends on live state or on decisions made outside the current context.
---

# Resume live work

Start with the latest user direction and the current handoff or runbook. Recover the active project, goal, constraints, last verified result, and next useful action. When the note leaves a gap, read the relevant prior turns. In T3 Code, a known thread link and its activity can recover the decision and tool result. Worktree status can locate the checkout. Verify the live checkout or run separately.

- **On pickup.** Check the actual branch, dirty files, build, job, or checkpoint that matters. If there is a long-running job, establish its identity and state before issuing a start, resume, or stop command. A past report, process name, or stale PID file alone is insufficient. Carry forward explicit limits such as watcher-only work or a user-owned release step.
- **While the job runs.** If the user asked you to monitor, identify the next event, the source that proves it happened, and what you will do when it arrives. Keep one owner and one wake path. Re-arm a missing watcher when needed and supported. T3's pull request watcher applies to pull requests. A training run or local process needs the project's run-control or a suitable monitor. Report when you can observe the job now but cannot reliably wake on its result.
- **At pause or handoff.** Use the project's graceful stop path when authorized. Read back the actual saved state and check that the process, watcher, or ownership is where the user expects. Leave the next concrete action and any command the user needs to see progress. Use the existing runbook when it already keeps those facts current.

Continue directly when the current thread already has the goal and state. When the user has clearly switched projects, use the newer brief. Keep earlier work resumable on its own terms.
