# GitMatched

GitMatched is a dating app specifically designed for UIUC computer science students who are interested in finding love and coding partners. The app allows users to create a profile and post code snippets instead of pictures of themselves. Users can then browse other profiles and click left or right to reject or match with potential partners. Once two users match, they can communicate with each other outside of gitmatched via email.

## Installation

To run GitMatched on your local machine, you can follow these steps:

1.  Create a virtual environment and activate it.

`python3 -m venv venv . venv/bin/activate`

2.  Set the Flask app variable.

`export FLASK_APP=gitmatched.py`

3.  Install the required dependencies.

`pip3 install -r requirements.txt`

4.  Generate the CSS files.

`cd ./app/static npx tailwindcss -i ./src/style.css -o ./css/main.css `
`cd .. `
`cd ..`

5.  Run the Flask app.

`flask run`


Or, you can utilize our bash file and run `bash run.bash`  to execute all the above steps at once.

## Functionality

### Profile Creation

Users can create a profile on GitMatched by signing up with their illinois email address and a password. Instead of uploading a photo, users can upload code snippets that showcase their coding skills and style.

### Matching System

After creating a profile, users can browse through other profiles using a Tinder-style matching system. Users can click to reject a profile or right to match with a profile. When two users match, they both recieve an email (using flask mail) and can communicate off the platform in order to share more information about each other.

### Technologies Used

GitMatched is built using the Flask web framework for Python. The frontend is built using HTML, CSS, and JavaScript, with Tailwind CSS for styling. We used. SQL database that works within flask to store data and accounts (we used standard privacy features to secure account information and encrypt data like passwords). 

GitMatched also uses the OpenAI GPT API (we used davinci-003) to generate similarity scores for code snippets. This helps us match users based on their coding style, making it easier for them to find coding partners and love.

## Team Collaboration

**Group members: Salar Cheema, Saurav Kumar, and Raj Patel**

All of us contributed equally, but we did have main roles in completing the construction of GitMatched. Salar contributed heavily to the backend development of the authentication with flask, and wrote some of the structural HTML to integrate the backend into our frontend. Saurav worked on the matching algorithm and styled the frontend. Raj worked on writing integration and unit tests for all the algorithms and also helped with the emailing function.
