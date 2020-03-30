---
layout: default
title: Home
nav_order: 1
---
# Clean Actions

A Tool for generating Github Action Workflows following DRY principals.

Clean Actions adds support for utilising commands, to help deduplicate your workflows,
and make them declarative.


## Why we are here

Github Actions is great. It's simple to use, and has good support for writing custom actions
in Javascript and Docker.

However, there is a feature sorely lacking, and that is support for defining and using
commands with the native workflow syntax.

This results duplicated routines being created, whether it's installing dependencies
for your different test/lint suites, or deploying stages of a service out.

## What we do

It's pretty simple. We make this run on a Github Actions runner:

```yaml
runs-on: ubuntu-latest
jobs:
  job:
    steps:
      - command: say-hello
        with:
          name: World
commands:
  say-hello:
    inputs:
      name:
    steps:
      - run: echo 'Hello, ${{ inputs.name }}!'
```

For more, see the [Features][features]

## How it's done

Clean Actions is a pre-processor. We take what you write, and will give you the equivalent
Github Actions workflow.

This means you will need to store both copies in your repository..

To build the workflow, run:

```sh
clean_actions .github/src/workflows/workflow.yml .github/workflows/workflow.yml
```

[features]: ./features.md
