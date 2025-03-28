# scraper-demo Project

This project is a web scraper that extracts product information from a website using Selenium and BeautifulSoup. The extracted data is saved to a mongo db

## Requirements

- Python 3.x
- Docker (for running MongoDB)
- A node package manager (pnpm)

## Project Structure

```
scraper-demo
├── backend
    ├── scaper_*.py         # Web scraping logic
    ├── docker-compose.yml  # Docker setup for mongo and standalone chrome
├── frontend                
    ├──  Vue app            # Frontend Client App
└── README.md               # Project documentation
```

## Setup Instructions

1. **Clone the repository:**

   ```bash
   git clone <repository-url>
   cd scraper-demo
   ```

2. **Create a virtual environment:**

   It is recommended to use a virtual environment to manage dependencies. Run the following commands:

   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Python dependencies:**

   Make sure you have `pip` installed, then run:

   ```bash
   pip install -r requirements.txt
   ```

   Note: Create a `requirements.txt` file with the necessary dependencies if it doesn't exist.

4. **Rename the `.env.example` file:**

   In the project directory, rename the `.env.example` file to `.env`:

   ```bash
   mv .env.example .env
   ```

5. **Run MongoDB using Docker:**

   Ensure you have Docker installed and running. Then, in the project directory, run:

   ```bash
   docker-compose up -d
   ```

   This command will start the MongoDB service defined in `docker-compose.yml`.

6. **Run the fast api server:**

   ```bash
   fastapi dev
   ```

   This command will start the  fast api server which will be used to communicate with the web client

7. **Run the scraper:**

   After the MongoDB service is up, you can run the scraper:

   ```bash
   python scraper_superc.py
   ```

   The scraped data will be saved to the mongo database in the `products` collection

8. **Compile and create the frontend app:**

   ```bash
   cd ../frontend
   ```

  follow the steps in the `README.md` file 


9. **(Optional) Test the chat bot:**

   Add an OpenAI key to your .env file in the `backend` folder. If you don't have one, visit [OpenAI](https://platform.openai.com/docs/overview) and create an account. Then navigate to [API Keys](https://platform.openai.com/settings/organization/api-keys) and create a key.
   Once there is enough data in the database, you can try playing around with the chatbot

   Visit [localhost:5173](http://localhost:5173/) and follow type in your grocery list...

## Notes

- The MongoDB service can be accessed at `localhost:27017` by default. Adjust the connection settings in your application if necessary.
- [Download MongoDB Compass](https://www.mongodb.com/try/download/compass) as a GUI to easily view the database entries
- To see what is happening in the container, paste this `http://localhost:7900/?autoconnect=1&resize=scale&password=secret⁠` in your browser



