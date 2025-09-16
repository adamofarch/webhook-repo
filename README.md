## Installation 

  - Create a new virtual environment 
  ```bash
  python -m venv venv
  ```

  - Activate the virtual env
  ```bash
  cd venv
  source venv/bin/activate
  ```

  - Install requirements
  ```bash
  pip install -r requirements.txt
  ```

## Usage

  - Ngrok free tunnel for port forwarding (If in a development environment)
  ```bash
  paru -S ngrok
  ngrok config add-authtoken <your_authtoken_here>
  ngrok http 5000
  ```
  Note: This installation for ngrok is for Arch Linux, for other distributions refer to [Ngrok Dashboard](https://dashboard.ngrok.com/get-started/setup/), Enter the https://<your_ngrok_url>/webhook/receiver while setting up webhooks at your Github Repo


  - Setup .env
  ```bash
  cp .env.example .env
  ```
  Note: Change the Connection string if you're not using the default one
  

  - Run the flask application (Use Gunicorn in production)
  ```bash
  python run.py
  ```

  - Endpoints
    - '/' - Homepage(UI)
    - '/webhook/receiver' - Receives the webhooks payload from github actions
    - '/webhook/events' - Keep polling the database and updates UI every 15 seconds

  
  
