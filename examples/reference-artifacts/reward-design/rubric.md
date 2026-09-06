# Reward Design Rubric

## High

A high-quality reward design decomposes success into measurable components and
names the behavior it could accidentally incentivize.

Required anchors:

- Task success is checked by verifiers, not vibes.
- Positive components map to desired workflow behavior.
- Negative components catch unsafe or invalid behavior.
- Component weights are visible.
- Reward-hacking traps are named.

Example: [`good.md`](good.md) earns high because it separates task success,
policy grounding, approval behavior, tool validity, and fabrication penalties.

## Medium

A medium reward design has useful components but leaves key checks subjective
or omits anti-hacking analysis.

## Low

A low reward design is a single opaque score or rewards surface properties such
as length.

Example: [`weak.md`](weak.md) is low because it rewards answer detail without
checking whether the workflow was actually completed.
