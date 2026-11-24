---
name: verify-real-path
description: Verify a user-facing change, a reported runtime failure, or a fix tied to a specific build, device, editor, or CI environment. Use when the path the user relies on can behave differently from a demo, static check, or local substitute.
---

# Verify the real path

Find the action, environment, and observation that distinguish the reported failure from success. For example, if the user says text arrives only when processing finishes, observe text arriving **before** completion. A spinner proves activity only.

1. Use the project's existing verification recipe when it covers that path. When practical, reproduce the issue or capture the current behavior before editing. For visual or motion changes, preserve the accepted baseline and match the scene, view, inputs, and build settings for the comparison.
2. Run the same check on the artifact the user will receive. Include a nearby path the change could break when there is a concrete risk. A focused regression is enough when it exercises the reported failure at the right boundary.
3. Verify the target identity before relying on the result. For a CI failure, use the CI SDK and command. For a desktop shortcut, invoke it from a real target app. For a device-specific issue, use the relevant device or record exactly which part the available environment can verify.

In T3 Code, use browser preview for browser work the user requests when the target tab is reachable. Use the device tools when they are enabled and the matching simulator or emulator can exercise the failure. For native desktop behavior and hardware-only issues, use the project's existing driver or the supported local tools. Showing a screenshot or recording helps when the behavior is visible, especially when you can capture the interaction rather than only its final frame.

Report the path you ran and the observation. If the target is unavailable, report the closest executable check and the claim that remains open. Keep routine copy edits and read-only explanations out of this workflow.
