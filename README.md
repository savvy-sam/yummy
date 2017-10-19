# yummy

<img src='https://img.shields.io/coveralls/jekyll/jekyll/master.svg'>

<img src= 'https://travis-ci.org/savvy-sam/Yummy-Recipes.svg?branch=master'>
<img src= 'https://opensource.org/licenses/MIT' >
< img src='https://img.shields.io/codeclimate/github/kabisaict/flow.svg'>


<strong>Introduction</strong>
<p>
Yummy is an app where users manage recipes. 
It allows users to create,edit, view and delete recipes
</p>
<strong>Installation</strong>
<p>
To run the app on your local machine:
</p>
Clone this repository
<p><code> git clone</code></p>



<strong>Introduction</strong>
<p>
Yummy is an app where users manage recipes. 
It allows users to create,edit, view and delete recipes
</p>
<strong>Installation</strong>
<p>
To run the app on your local machine:
</p>
Clone this repository
<p><code> git clone</code></p>

<p>Assuming you have python running on your computer,install pipenv</p>

<p><code> pip install pipenv</code><p>
    
 <p>Install virtualenv</p>
 
 <p><code>pipenv install virtualenv</code></p>
 
 <p>Create a virtual environment</p>
 <p><code>cd your_project_folder</code></p>
 <p><code>virtualenv your_virtual_env</code></p>
  
  Install Flask
  <p><code>pip install flask</code></p>
  
  <p>Install requirements.txt</p>
  <p><code>pip freeze > requirementstxt </code></p>
  
  
  To run the server, 
  <p><code>flask run</code></p>
  
  
  <strong >Routes</strong>
  
  1. GET yummy/- Landing page with links to other pages
  
  2. GET yummy/login -Renders the Login page
  
  3. POST yummy/login- Creates a user session
  
  4. GET yummy/signup- Renders the sign up form
  
  5. POST yummy/signup- Creates a user
  
  6. GET yummy/recipes- Lists all recipes belonging to user
  
  7. GET yummy/recipes/create - Renders form to creates a new recipe
  
  8. POST yummy/recipes/create- Creates a new recipe
  
  9. PUT yummy/recipes/update- Updates an existing recipe
  
  10. DELETE yummy/recipes/destroy- Destroys an existing recipe

<strong>Testing<strong>
    
    <p>The tests are are based on the python unittest library, you can run them using pytest</p> 
    
    
 <strong>Uses</strong>
 
 <ol>
    <li>Flask</li>
    <li>HTML</li>
    <li>Bootstrap</li>
 
 </ol>
 <strong>Author</strong>
 
 Samson Chege- Andela Fellowship Applicant

