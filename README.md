## swapi_assesment

The curernt API interfaces with the [Star Wars API](https://swapi.py4e.com/), to fetch, store, search and retrieve, characters, films and starships drawn from the star wars movies. The project is built using python and fastapi, and deployed using docker. Although, the project is containerised with  docker, it has only been tested that it works properly on macOs 26.2 and Windows 11.

---

## Prerequisites

Make sure you have the following installed before running the project:

- [Docker](https://www.docker.com/get-started) (v20+)
- [Docker Compose](https://docs.docker.com/compose/install/) (v2+)
- You can use the following commands 
```bash
   docker --version
   docker compose version
   ```

If not, continue reading the instructions. If yes you can jump directly to the [Getting Started](#getting-started) section.

---

## Installing Docker

### macOS

1. Download [Docker Desktop for Mac](https://www.docker.com/products/docker-desktop/)
2. Open the `.dmg` file and drag Docker to your Applications folder
3. Launch Docker from Applications and follow the setup wizard
4. Verify installation again by typing
   ```bash
   docker --version
   docker compose version
   ```

### Windows

1. Download [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop/)
2. Run the installer and follow the setup wizard
3. Enable **WSL 2** when prompted (recommended) — if not installed, follow [Microsoft's WSL guide](https://learn.microsoft.com/en-us/windows/wsl/install)
4. You will probably be asked to do so, but restart your machine after installation
5. Verify installation in PowerShell or Command Prompt:
   ```bash
   docker --version
   docker compose version
   ```
---

## Getting Started

### 1. Clone the repository

Note: Having git installed is highly recommended. In case you don't, you can download the project from the [GitHub](https://github.com/pantelous/swapi_assesment) repository.

If git is already installed on your machine,  run the following command on the macOS terminal or Windows Command Prompt,:
```bash
git clone https://github.com/pantelous/swapi_assesment.git
cd swapi_assesment
```

### 2. Set up environment variables

Copy the example .env.example file by doing:

For macOS or Linux 
```bash
cp .env.example .env.docker
```

For windows
```cmd
copy .env.example .env.docker
```
---

### 3. Start Docker desktop

Start the Docker Desktop application you downloaded before in the section [Installing Docker](#installing-docker).

---

### 4. Build and run with Docker Compose

You can use one of the two following commands to build the application and run it:

```bash
docker compose up --build
```

Normally, the API will be available at: **http://localhost:8000** (or whichever port you configured)

Moreover, to run the application in detached mode, i.e. in the background of your terminal, not receiving any input or displaying output (recommened):
```bash
docker compose up --build -d
```

---

## Populate the database with data

Before starting to interact with the API, you need to populate the database with data. 
To do so, you'll need to try the store related endpoints in the API Docs at
- Swagger UI: `http://localhost:8000/docs`
  
## Important: Please, you'll need to populate `characters` first, then `starships` and then `films`, otherwise you'll get errors.

You can vote for your favourite movie by just typing the name of the movie on the `vote-film` endpoint.

---

## Stopping the Application

```bash
docker compose down
```

## Restart the application

```bash
docker compose up -d
```
---

## API Documentation

Once the app is running, you can access the API docs at:

- Swagger UI: `http://localhost:8000/docs`

---
