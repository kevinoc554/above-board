# Above Board

Above Board is a user-centered boardgame database that aims to provide boardgamers a place to catalogue, rate and research games.

View the live site [here](http://above-board.herokuapp.com/home).

# Table of Contents

> 1.  [Project Goals](#project-goals)
> 2.  [UX](#ux)
> 3.  [Features](#features)
> 4.  [Technologies Used](#technologies-used)
> 5.  [Testing](#testing)
> 6.  [Bugs](#bugs)
> 7.  [Deployment](#deployment)
> 8.  [Credits](#credits)
> 9.  [Acknowledgements](#acknowledgements)

# **Project Goals**

Above Board is a place for boardgame fans to browse an extensive database of games, add and rate games, and ultimately find something fun to play. Above Board is aimed at boardgamers new and old, allowing users to log their collections, rate games and explore the database by filtering by genre and game mechanics.

**User Goals:**

- A place to log their collection, see what games other people are playing, and find something to play.

**Site Owner Goal:**

- Utilize the site's functionality themselves.
- Promote boardgaming as a hobby.
- Potentially generate income via affiliate links.

![Home page viewed on different screen sizes](docs/screenshots/responsive-index.PNG)

*A screenshot of the Home page as viewed on different screen sizes, generated on [ami.responsivedesign.is](http://ami.responsivedesign.is/). An interactive scrollable version is available [here](http://ami.responsivedesign.is/?url=http://above-board.herokuapp.com/home).*

# **UX**

## **User Stories**

1. As a new user, I want to be able to register an account, so I can fully utilize the site.
2. As a returning user, I want to be able to log in easily, so I can access the site’s features.
3. As a boardgame fan, I want to be able to view, search and filter a database of games, so I can find one to play.
4. As a boardgame fan, I want to add my games to the database, so I can curate my collection.
5. As a boardgame fan, I want to view my collection of games to the database, so I can see all the games I have added.
6. As a boardgame fan, I want rate games in the database, so I can provide guidance to other users.
7. As a site user, I want to be able to delete my posts, so I can remove any games I have posted.
8. As a site administrator, I want to be able to delete any user’s games, so I can remove any potentially inappropriate content.
9. As a site administrator, I want to be able to add new genres and mechanics, so I can expand the database content in line with user demands.

## **Design**

### Database Schema

Based on the above, the following schema was mapped out:

![Database Schema](docs/screenshots/database-schema.jpg)

### Initial Wireframes

Based on the above, the following wireframes were mocked up:

- [Index](docs/wireframes/index.pdf)
- [Login](docs/wireframes/login.pdf)
- [Register](docs/wireframes/register.pdf)
- [Profile Page](docs/wireframes/profile.pdf)
- [All Games & My Games](docs/wireframes/all-games.pdf) 
- [Add Game & Edit Game](docs/wireframes/add-game.pdf) 
- [View Game](docs/wireframes/game-info.pdf)
- [Admin Area](docs/wireframes/admin-area.pdf)

### Colour Scheme

The color palette chosen for this project is below.

![Color Palette](docs/screenshots/color-palette.PNG)

- The yellow was chosen for the navigation bar and some UI elements, as it is warm and bright and can quickly grab the users attention. Care was given to not overuse it, as it could lead to visual fatigue.
- The greys and lilac were chosen as background colors as they are muted and would not divert the users attention away from the content of the site.
- Black font is used throughout the site, to ensure readability. The contrast of the black text against the various background colors was checked with this [contrast checker](https://coolors.co/contrast-checker/000000-ffff00).


### Fonts

The fonts chosen for this project were:
1. [Scramble](https://www.fontspace.com/scramble-font-f2476)
2. [Inter](https://fonts.google.com/?query=inter)

#### Scramble
![Scramble Font Sample](docs/screenshots/scramble-font-sample.png)

Scramble was chosen as the font for the main headers of the site. This font was chosen as visual reference to the boardgame 'Scrabble', with which many of the users of the site would already be familiar, in the hopes of eliciting a positive emotional response from them.

#### Inter
![Inter Font Sample](docs/screenshots/inter-font-sample.PNG)

Inter is a a variable font family specifically designed to be legible on computer screens. This font was chosen to prioritize readability, particularly when database entries could have variable amounts of text.

# Features

## Existing Features

### Users

Users of the site are able to register accounts, log in and out, edit their account info and reset their password via email.

#### Users - Register
- Users can register for an account using the form on the Register page, which can be accessed via the navigation bar at any time, or via the prominent call to action button on the homepage.
- Users must provide their first and last names, their desired usernames, their emails and a secure password.
- This form, created with `flask-wtforms`, has extensive validation checks that ensure the password provided is sufficiently secure, and the username and email do not already exist in the database. If there are any issues, this is fed back to the user on the front-end and the form is not submitted.
- Upon successfully submitting and validating the form, the user's account is registered to the database and they are invited to log in.

#### Users - Login/Logout
- Once a user has an account, they can log in. This is accessed via the navigation bar, or if a user attempts to reach a page they can only access while logged in.
- To login, a user must provide an email address and a password. This is compared against the email in the database and the secure hash of the password. Passwords are never stored as plaintext.
- If the information does not match, the user is given feedback and encouraged to try again.
- If the information matches, `flask-login` is used to log the user in.
- A logged in user can log out at any time by clicking the relevant link in the navigation bar.

#### Users - Edit Account Info
- While logged in a user can navigate to their Profile page, where they can see and edit their account information.
- Users can update their first and last names, and their email address.
- Users cannot change their usernames as these are essential to the site's functionality.

#### Users - Password Reset
- When logging in, a user who has forgotten their password can requesta password reset.
- The user is asked to provide the email address associated with the account, and provided it exists in the database an email is sent to this address.
- This email contains a link, the URL of which is created with a secure token unique to that account. Following that link will allow the user to set a new password. The token will expire if not used in time.
- A user who did not request a reset, or changes their mind, can safely ignore the email. 

## Features To Be Implemented

# Technologies Used

- HTML5 - the pages of this site were designed using HTML.
- CSS3 - the pages of this site were styled using CSS.
- JavaScript - the interactive elements of this site were implemented using JavaScript.
- Python - back-end functionality of the site was written in Python
- [Flask](https://flask.palletsprojects.com/en/2.0.x/#) - The Flask micro-framework - including the [Jinja](https://jinja.palletsprojects.com/) template engine and [Werkzeug](https://werkzeug.palletsprojects.com/) toolkit - was used to develop this site.
- [MongoDB](https://www.mongodb.com/) - the site's uses MongoDB as it's database platform.
- [Gitpod](https://www.gitpod.io/) - the site was developed using Gitpod as the development environment.
- [Materialize](https://materializecss.com/) - the site was styled using the Materialize front-end framework.
- [jQuery](https://jquery.com/) - jQuery was used to simplify and condense JavaScript, particularly for interacting with, and writing to, the DOM.
- [Font Awesome](https://fontawesome.com/) - Font Awesome icons were used for the social media links in the footer.
- [Google Fonts](https://fonts.google.com/) - Google Fonts were used throughout the project.
- [Coolor Contrast Checker](https://coolors.co/contrast-checker/000000-ffff00) - Contrast Checker was used to ensure there was sufficient contrast between foreground and background colours.
- [Free Logo Design](https://www.freelogodesign.org/) - The site's brand logo was created using Free Logo Design.
- [Favicon Generator](https://www.favicongenerator.com/) - Favicon Generator was used to create and size the favicon for the site, using the logo created above.
- [Random Keygen](https://randomkeygen.com/) - Used to generate the site's SECRET_KEY

## Packages
Some of the key packages used in this project include:
- [Flask-Login](https://flask-login.readthedocs.io/en/latest/) - Used to manage user logins, and for keeping track of the current user
- [Flask-WTForms](https://flask-wtf.readthedocs.io/en/0.15.x/) - Used to create and validate all forms in the project.
- [Flask-Mail](https://flask-mail.readthedocs.io/en/latest/) - Used to send the password reset email

*A full list of the packages can be found in the requirements.txt*

# Testing

*Full details of testing can be found [here](docs/TESTING.md).*

# Deployment

- This site was developed in [Gitpod](https://www.gitpod.io/), committed and pushed to [Github](https://github.com/), and deployed on [Heroku](https://www.heroku.com/).
- At the time of submission, there are no differences between the development version and deployed version of the site.

## The following steps were taken to deploy this site:
Initial steps:
1. Navigate to [Heroku](https://www.heroku.com/), and log in/sign up.
2. Once logged in, click on '**New**', and then '**Create New App**'.
3. Enter a suitable App Name, and choose the region from the dropdown menu.
4. Click on **Create App**.
5. Click on the '**Deploy**' tab.
6. Next to '**Deployment Method**', click on '**GitHub**'.
7. If prompted, enter GitHub login details.
8. Next to '**Connect to Github**', find the repository by typing the name in the search box.
9. Click '**Connect**'.

Enable Autmotaic deploys:
1. Within the Heroku app, navigate to the '**Deploy**' tab as above.
2. Navigate to '**Autmomatic deploys**', and select the branch fromwhich to deploy,in this case `main`.
3. Click '**Enable Automatic Deploys**'

Set Environment Variables:
1. Within the Heroku app, navigate to the '**Settings**' tab.
2. Click on '**Reveal Config Vars**'.
3. Add the following Config Variables:
    - **IP** : 0.0.0.0
    - **PORT** : 5000
    - **MONGO_URI** : The unique address of the mongoDB collection, which will include the database name and password. Can be found by logging in to [MongoDB](https://www.mongodb.com/), navigating to the Cluster in question and clicking on '**Connect**'.
    - **MONGO_DBNAME** : The name of the database on mongoDB
    - **SECRET_KEY** : A string of random characters, used by Flask to maintain security. Can be created using a key generator like the one above, [Random Keygen](https://randomkeygen.com/).
    - **MAIL_USERNAME** : The email address to be used to send email via Flask-Mail
    - **MAIL_PASSWORD**' : The app password for the email in the **MAIL_USERNAME**.


## To run and edit the code for this site locally, follow these steps:

# Credits

## Code

## Content

# Acknowledgements
