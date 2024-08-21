import os
import paho.mqtt.client as mqtt
from paho.mqtt.client import MQTTMessage
import psycopg
from datetime import datetime
import time

# Get configuration from environment variables
mqtt_broker = os.environ["MQTT_BROKER"]
mqtt_port = int(os.environ["MQTT_PORT"])
mqtt_username = os.environ["MQTT_USERNAME"]
mqtt_password = os.environ["MQTT_PASSWORD"]

pg_host = os.environ["PG_HOST"]
pg_database = os.environ["PG_DATABASE"]
pg_user = os.environ["PG_USER"]
pg_password = os.environ["PG_PASSWORD"]


def create_pg_connection():
    return psycopg.connect(
        f"postgresql://{pg_user}:{pg_password}@{pg_host}/{pg_database}"
    )


def create_table_if_not_exists(conn):
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS shelly_sensor_data (
                timestamp TIMESTAMPTZ PRIMARY KEY,
                device_id VARCHAR(50) NOT NULL,
                temperature NUMERIC(5,2),
                humidity NUMERIC(5,2),
                battery INTEGER,
                error INTEGER
            );

            CREATE INDEX IF NOT EXISTS idx_device_id ON shelly_sensor_data(device_id);

            COMMENT ON TABLE shelly_sensor_data IS 'Stores sensor data from Shelly HT devices';
        """)
    conn.commit()


def insert_data(conn, table, timestamp, device_id, column, value):
    print(f"Now inserting {value} into {column}")
    with conn.cursor() as cur:
        cur.execute(
            f"""
            INSERT INTO {table} (timestamp, device_id, {column})
            VALUES (%s, %s, %s)
            ON CONFLICT (timestamp) DO UPDATE
            SET {column} = EXCLUDED.{column}
        """,
            (timestamp, device_id, value),
        )
    conn.commit()


def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code.is_failure:
        print(f"Failed to connect: {reason_code}. loop_forever() will retry connection")
    else:
        client.subscribe("shellies/shellyht-746CEB/sensor/temperature")
        client.subscribe("shellies/shellyht-746CEB/sensor/humidity")
        client.subscribe("shellies/shellyht-746CEB/sensor/battery")
        client.subscribe("shellies/shellyht-746CEB/sensor/error")


def on_message(_client: mqtt.Client, _userdata, msg: MQTTMessage) -> None:
    try:
        timestamp = datetime.now()
        topic_parts = msg.topic.split("/")
        device_id = topic_parts[1]
        table = "shelly_sensor_data"
        column = topic_parts[3]
        print(f"Received: {timestamp}, {device_id}, {table}, {msg.payload.decode()}")
        value = msg.payload.decode()
        insert_data(pg_conn, table, timestamp, device_id, column, value)
    except Exception as e:
        print(f"Error processing message: {e}")


mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqtt_client.username_pw_set(mqtt_username, mqtt_password)
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

pg_conn = create_pg_connection()
create_table_if_not_exists(pg_conn)


def main():
    while True:
        try:
            mqtt_client.connect(mqtt_broker, mqtt_port)
            mqtt_client.loop_forever()
        except Exception as e:
            print(f"Connection to MQTT broker failed: {e}")
            print("Retrying in 10 seconds...")
            time.sleep(10)


if __name__ == "__main__":
    main()
