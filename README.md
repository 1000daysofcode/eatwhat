# EatWhat?

#### Video Demo: [EatWhat? Video Demo](https://youtu.be/8dbePBUvVkE) <https://youtu.be/8dbePBUvVkE>

#### Description:

##### Summary

EatWhat? is a web application with a single, simple purpose: help you decide what to eat when you can't mack a choice. The use case that inspired me to create this was that often my fiance is unsure of what she wants to eat... yet she knows the basic tastes she wants, whether it's hot and whether it's a solid (like steak) food or soft (like soup).

Therefore, the app requires little input by nature and once it receives that input will return options that the received conditions. Options are ideally returned five at a time and include

- Name of the food
- Where the food is from,
- Main flavors,
- Main ingredients,
- A description,
- A picture, and *conveniently*
- A link to search for that food nearby

The website also features a brief About Us section that summarizes the app's purpose and use, as well as a Contact Us form that automatically sends formatted contact emails from the website.



##### How it Works

###### Main Application

The default web application serves an HTML page "choose.html" the accepts as input 1-3 selections of taste, 1 choice of solidity, 1 choice of temperature, the address of user and when food is desired. All information is checked for errors (both in Python and HTML) to ensure that information is correctly entered. Any error leads to an error page that details the reason for the error; these will eventually be JavaScript pop-up errors that don't allow form progress to the next page.

Once the form is successfully submitted, Flask will query a SQLite3 database of foods with the following schema:

- Unique ID
- Food name
- Country
- Continent
- Tastes(s)
- Ingredients
- Temperature
- Solidity
- Description
- Image link

If there are no results, the web application will note this to the user on the next page instead of displaying results.

If there *are* results, a blank list for results is initiated. Then a for loop manipulates each row within the SQL query, dynamically creates a Google search link for the user based on the name of the food, their location and duration they entered:

- *Ice Cream would become* **'ice+cream'** (link_name)
- *123 Main St NYC would become* **'123+main+st+nyc'** (link_add + link city)
- *< 30 Min. (duration) would become* **'5+kilometers' **(distance)

This is all added to a maps link as such: https://www.google.com/maps/search/{link_name}+within+{distance}+of+{link_add}+{link_city}/'

The above link is then assigned to a 'Restaurants' button under each food for the user's convenience.

Other food details are added, with this to a temporary dictionary which is then appended to the list for results. The list of dictionaries is then passed to the "options.HTML" template, which uses a Jinja for loop to display all results in the page. That's it!



###### About and Contact Pages

The <u>about page</u> requires little explanation; it only accepts GET requests and always renders the same about page.

The <u>contact page</u>'s HTML template accepts the user's email address, name, a subject line and a message as input.

Flask's Python will check to make sure all information has inputs and that they are nominal lengths. The HTML only accepts specific types, which ensures, for example, that only an email are entered into the email bar.

Once the form is successfully submitted, flask_mail will use the inputted information along with the other variables initialized at the top of the application to create and send an email to the website owner that looks similar to the below:

> EatWhat contact request. Zach: "Testing the contact success page "
>
> Hello Zach,
>
> You have received an email from *Zach* on 2021-09-06 at 15:14:19 UTC.
>
> The subject is **"Testing the contact success page ."** Content below:
> *"Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."*
>
> In order to respond to this inquiry, please email [test@test.com](mailto:test@test.com).
>
> *This was an automatic message from EatWhat.app*

Within the next few months, I will improve the the contact page so that the email sends as "EatWhat Support" (or something along those lines) and also sends an email to address of the person that sent the contact request.



###### Future Improvements

I plan to improve this project even after CS50.

**Within the next 1-2 months:**

1. Replace CS50 library for SQL, upload to self-hosted location
2. Add continent option
3. Add country option
4. Input errors block form submission via JavaScript instead of continuing to the next page and displaying errors.
5. Add spiciness option
6. Connect to food API **or** increase database size otherwise
7. Improve contact form functionality
   1. Add confirmation email
   2. Customize sending email address

**Within the next 3-6 months:**

1. Update tastes to include two taste options: simple or complex.
   1. Simple would be the five main tastes
   2. Complex would feature flavors like "nutty," "earthy," etc.
2. Include option for in-app display of top 5-10 restaurants by rating.
3. Create option for users to sign up and create an account to save foods they enjoyed to personal list of saved restaurants.
4. Create an option to use location based on GPS information.

**After 6 months minimum:**

Add option for cooking within user accounts. A direct prerequisite is the user log-in functionality. What else this would require:

1. A list of ingredients user currently has; this may work with some API
2. Updates to the database items:
   1. Food item table column addition:
      1. Cooking difficulty (low, medium, high)
      2. Total cooking time (short, medium, long)
   2. New table for ingredients: ingredient availability
   3. User table addition: user cooking ability
3. This would also require a new form to choose foods from within the user menu while logged in.