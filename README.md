# swapi_assesment# Project Name

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
4. Verify installation again by typing the following
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
In the macOS terminal or Windows Command Prompt, run the following command:
```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
```

### 2. Set up environment variables

Copy the example env file:

For macOS or Linux 
```bash
cp .env.example .env.docker
```

For windows
```cmd
copy .env.example .env.docker
```
---

### 3. Build and run with Docker Compose

You can use one of the two following commands to build the application and run it:

```bash
docker compose up --build
```

Normally, the API will be available at: **http://localhost:8000** (or whichever port you configured)

Moreover, to run the application in detached mode, i.e. in the background of your terminal, not receiving any input or displaying output:

```bash
docker compose up --build -d
```

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
