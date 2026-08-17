# Lesson 2: State and Transitions

## Core Idea

State defines what is true in the environment. Transitions define how actions change what is true.

## State Should Include

- employees
- managers
- policies
- trips
- receipts
- reimbursement drafts
- approvals
- action history

## Transition Design

Every action should specify:

- preconditions
- inputs
- state changes
- observation returned
- possible errors
- whether the episode terminates

## Checkpoint

You are ready to move on when every simulated action changes state in a predictable and inspectable way.

