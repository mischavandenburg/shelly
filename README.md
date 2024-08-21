# MQTT to PostgreSQL Logger

This Python script listens to MQTT messages from a Shelly HT device and logs the sensor data into a PostgreSQL database. The application is containerized using Docker for easy deployment and management.

## Features

- Connects to an MQTT broker and subscribes to Shelly HT sensor topics
- Stores received sensor data (temperature, humidity, battery level, and error status) in a PostgreSQL database
- Automatically creates the necessary database table if it doesn't exist
- Implements error handling and automatic reconnection for MQTT broker
- Uses environment variables for configuration
- Containerized using Docker for easy deployment

## Prerequisites

- Docker
- Docker Compose

## Project Structure

```bash
.
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── src/
│   └── main.py
└── .env
```

## Deployment on Kubernetes

See the GitOps configuration in my [homelab repo](https://github.com/mischavandenburg/homelab/tree/main/apps/production/shelly) to see how I've deployed it.

## Local Installation and Setup

1. Clone this repository

2. Create a `.env` file in the project root with the following variables:

   ```bash
   MQTT_BROKER=<your-mqtt-broker-address>
   MQTT_PORT=<your-mqtt-broker-port>
   MQTT_USERNAME=<your-mqtt-username>
   MQTT_PASSWORD=<your-mqtt-password>
   PG_HOST=db
   PG_DATABASE=<your-postgresql-database>
   PG_USER=<your-postgresql-username>
   PG_PASSWORD=<your-postgresql-password>
   ```

   Note: Set `PG_HOST=db` to use the database service defined in the Docker Compose file.

## Usage

To run the application using Docker Compose:

```bash
docker-compose up --build
```

This command will:

1. Build the Docker image for the MQTT client application
2. Start a PostgreSQL container
3. Start the MQTT client container
4. Connect the MQTT client to the specified MQTT broker
5. Begin logging data to the PostgreSQL database

To stop the application:

```bash
docker-compose down
```

To stop the application and remove the volumes (this will delete the database data):

```bash
docker-compose down -v
```

## Docker Configuration

### Dockerfile

The Dockerfile sets up the Python environment and installs the necessary dependencies:

```dockerfile
FROM python:3.12.5-alpine3.20
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src/ .
CMD ["python", "main.py"]
```

### Docker Compose

The `docker-compose.yml` file defines two services:

1. `mqtt-client`: The main application
2. `db`: The PostgreSQL database

It also sets up volume persistence for the database and defines a health check for the database service.

## Database Schema

The script creates a table named `shelly_sensor_data` with the following schema:

```sql
CREATE TABLE shelly_sensor_data (
    timestamp TIMESTAMPTZ PRIMARY KEY,
    device_id VARCHAR(50) NOT NULL,
    temperature NUMERIC(5,2),
    humidity NUMERIC(5,2),
    battery INTEGER,
    error INTEGER
);
```

An index on `device_id` is also created for improved query performance.

These are for all the topics I wanted. You can adjust the schema and topics as you see fit.

## Error Handling

The script implements error handling for both MQTT connection and database operations. If the MQTT connection fails, it will retry every 10 seconds. Database errors are logged but don't stop the script's execution.

## Logging

The script uses Python's built-in logging module to provide informative logs about its operation. Logs are printed to the console with timestamps and can be viewed using `docker-compose logs mqtt-client`.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
