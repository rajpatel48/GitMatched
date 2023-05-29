python3 -m venv venv
. venv/bin/activate
export FLASK_APP=gitmatched.py
pip3 install -r requirements.txt
cd ./app/static
npx tailwindcss -i ./src/style.css -o ./css/main.css
cd ..
cd ..
flask run