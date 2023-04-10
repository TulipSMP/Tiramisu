# Contributing
We will always appreciate contributions to Tiramisu! If you are outside of our organization, all you need to do is read the *Pull Requests* section below. Developers within the RoseSMP organization should read the subsequent sections.

## Pull Requests
Pull Requests are how you add to Tiramisu. Below are a few guidelines to help you in your creation of a PR:

* Must commit to the `main` branch
* If it fixes an issue, that issue must be linked in the PR description, so github will close those issues on merge.
  - "Fixes #00"
* You **MUST** explain *why* you are making changes, regardless of how obvious it may seem to you.

In your changes you must:

* Follow style according to how the code around you does
* Make use of logging where necessary

Pull Requests must meet these requirements to be merged.

## Internal Development Guidelines

* Minor changes *may* be made directly to `main`
* For any other change, make a branch starting with `dev-`, with words after that separated by underscores (`_`)
* You may **NOT** push directly to `prod` under ANY circumstances
