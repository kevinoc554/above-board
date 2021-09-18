# Testing

The following describes the testing steps taken during the development of [Above Board](http://above-board.herokuapp.com/).

Full details ofthe site can be found in the [README](README.md).

# Table of Contents
> 1.  [Validators](#validation)
> 2.  [User Stories](#user-stories)
> 3.  [Manual Testing](#manual-testing)
> 4.  [Automated Testing](#automated-testing)

# Validation:

### HTML

- The HTML for the site's four pages was passed through the W3C Markup Validation Service.
- The validator flagged `Bad value true for attribute readonly on element input`, however this was unavoidable due to how Materialize handles select elements.

### CSS

- The site's CSS was passed through the W3C CSS Validation Service, and no errors were found.
- The validation tool highlighted some vendor prefixes which were added by [Autoprefixer](http://autoprefixer.github.io/) to ensure cross-browser support.

### JS

- The site's JavaScript was validated using JSHint.

### Python

- The Python code was written in an attempt to comply with PEP-8 standards, with the following exceptions:
    - games/forms.py - error: line too long: The variable in question is a URL, and was left intact to ensure readability.
    - games/utils.py - warning: possible unbalanced tuple - The implementation of pagination (based on [this](https://gist.github.com/mozillazg/69fb40067ae6d80386e10e105e6803c9) guide) requires the tuple to be unbalanced to function.
    - aboveboard/config.py - warning: 'env' imported but unused: This is used solely to set environment variables locally,isnot pushed to githud/heroku.

# User Stories

# Manual Testing

## Testing Environments

Development and initial testing took place on a HP 250 G6 Laptop (Windows 10) in Chrome. Subsequent testing took place across the following devices, operating systems and browsers:

- Devices:

  - HP 250 G6 Laptop (Windows 10)
  - MacBook Pro 2013 (MacOS)
  - OnePlus 6T (Oxygen OS)
  - Samsung Galaxy S9 (Android)
  - Apple iPad (iPadOS 14)
- Browsers:

  - Chrome
  - Firefox
  - Edge
  - Safari

*All testing steps were taken on all devices and browsers, unless otherwise stated.*

# Automated Testing
