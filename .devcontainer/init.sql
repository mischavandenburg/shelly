CREATE TABLE shelly_sensor_data (
    timestamp TIMESTAMPTZ PRIMARY KEY,
    device_id VARCHAR(50) NOT NULL,
    temperature NUMERIC(5,2),
    humidity NUMERIC(5,2),
    battery INTEGER,
    ext_power BOOLEAN,
    error INTEGER,
);
-- Create an index on the device_id for faster queries
CREATE INDEX idx_device_id ON shelly_sensor_data(device_id);

-- Add a comment to the table
COMMENT ON TABLE shelly_sensor_data IS 'Stores sensor data from Shelly HT devices';
