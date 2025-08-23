# ImageAnalyzer

Image analyzer using Python and Django framework.

## Deployment

This project is containerized using Docker and managed with Docker Compose. Follow these steps to deploy and run the services.

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Running the Application

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd ImageAnalyzer
    ```

2.  **Navigate to the deploy directory:**
    ```bash
    cd deploy
    ```

3.  **Build and start the services:**
    Use Docker Compose to build the images and start the containers for both the Django and TensorFlow services.
    ```bash
    docker-compose up --build
    ```

    - The Django application will be available at `http://localhost:8001`.
    - The TensorFlow Jupyter server will be available at `http://localhost:8888`.

### Stopping the Application

To stop and remove the containers, press `Ctrl + C` in the terminal where the services are running, and then run:

```bash
docker-compose down
```

## Manual Deployment

If you prefer to run the services individually without Docker Compose, you can follow these manual steps.

1.  **Pull the TensorFlow Image:**
    ```bash
    docker pull tensorflow/tensorflow:latest-jupyter
    ```

2.  **Run the TensorFlow Container:**
    ```bash
    docker run -it -p 8888:8888 tensorflow/tensorflow:latest-jupyter
    ```

3.  **Build the Django Application Image:**
    From the project's root directory, run:
    ```bash
    docker build -t image-analyzer .
    ```

4.  **Run the Django Application Container:**
    ```bash
    docker run -p 8001:8001 image-analyzer
    ```
