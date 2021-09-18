# Testing

The following describes the testing steps taken during the development of [Above Board](http://above-board.herokuapp.com/).

Full details ofthe site can be found in the [README](README.md).

# Table of Contents
> 1.  [Validators](#validation)
> 2.  [User Stories](#user-stories)
> 3.  [Manual Testing](#manual-testing)
> 4.  [Automated Testing](#automated-testing)
> 5.  [Bugs](#bugs)

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
1. As a new user, I want to be able to register an account, so I can fully utilize the site.
2. As a returning user, I want to be able to log in easily, so I can access the site’s features.
3. As a boardgame fan, I want to be able to view, search and filter a database of games, so I can find one to play.
4. As a boardgame fan, I want to add my games to the database, so I can curate my collection.
5. As a boardgame fan, I want to view my collection of games to the database, so I can see all the games I have added.
6. As a boardgame fan, I want rate games in the database, so I can provide guidance to other users.
7. As a site user, I want to be able to delete my posts, so I can remove any games I have posted.
8. As a site administrator, I want to be able to delete any user’s games, so I can remove any potentially inappropriate content.
9. As a site administrator, I want to be able to add new genres and mechanics, so I can expand the database content in line with user demands.

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


# Bugs

## Fixed
**Login not working:**

Issue: 
- Login user method does not throw an error, redirects to homepage and creates a session cookie as intended, but the current_user.is_authenticated still comes back as false.
- When printing current_user after leaving the original route, get `flask_login.mixins.AnonymousUserMixin`
- Judicious use of print statements showed the load_user function was passing in the email address correctly, but then returning None rather than the User object.
- Investigation highlighted a typo in load_user, “mongo.db.User” vs. “mongo.db.users”.

Fix:
- Typo has been corrected and login now functions correctly.

**Login route fails with a 500 error if email provided is not in the database**

Issue:
- Login route was failing if the email provided was not in the database.
- The function to check the password hash was expecting a result fromthe find_user method, and was causing an error if find_user returned None.

Fix:
- The check passwrod has function is now wrapped in an if statement,and only fires if the find_user method returns a result (i.e., is not None). If not, the Login page will be refeshed and a flashed message displayed.

**View Game route crashing if given an invalid/wrong length game id:**

Issue:
- The View Games route was unable to handle being passed an invalid game id, and was causing 500 errors.
- An invalid id could be one that is manually inputted by a user and could be the wrong length or could point to a game that is no longer in the database.

Fix:
- Wrapped the route in a try/except block. In the event the route fails, will redirect the user to the All Games route and flash a message to explain rather than throwing an error.

**An error displaying in the console for the star ratings JavaScript function, only on pages where it is unused.**

Issue:
- The function gets the average rating from a div with the id of 'rating-avg'.
- On pages where this div did not exist, the function would fail with a syntax error.

Fix:
- Wrapped the function in an if statement, so it only fires on pages where the '#ratings-avg' div exists.

## Remaining
- At the time of submission, no outstanding bugs were identified.