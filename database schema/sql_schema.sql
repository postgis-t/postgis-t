CREATE TABLE buoy_data_buoy(
	buoy_id INTEGER PRIMARY KEY,
	buoy_wmo INTEGER,
	buoy_expno VARCHAR(15),
	buoy_type_buoy VARCHAR(15),
	buoy_deploy_date TIMESTAMP,
	buoy_deploy_location GEOMETRY(POINT, 4326),
	buoy_end_date TIMESTAMP,
	buoy_end_location GEOMETRY(POINT, 4326),
	buoy_lost_date TIMESTAMP,
	buoy_type_death NUMERIC
);

CREATE INDEX IX_buoy_id ON  buoy_data_buoy(buoy_id);
CREATE INDEX IX_buoy_deploy_date ON  buoy_data_buoy(buoy_deploy_date);
CREATE INDEX IX_buoy_deploy_location ON buoy_data_buoy USING GIST(buoy_deploy_location);

CREATE TABLE traj_buoy_trajectory(
	traj_id SERIAL PRIMARY KEY,
	traj_buoy_id INTEGER,
	traj_position_time NUMERIC,
	traj_date DATE,
	traj_location GEOMETRY(POINT, 4326),
	traj_celsius_temperature NUMERIC,
	traj_east_velocity NUMERIC,
	traj_north_velocity NUMERIC,
	traj_speed_velocity NUMERIC,
	traj_variance_location GEOMETRY(POINT, 4326),
	traj_variance_temp VARCHAR(15),
	CONSTRAINT FK_traj_buoy_id FOREIGN KEY(traj_buoy_id) REFERENCES buoy_data_buoy(buoy_id)
);

CREATE INDEX IX_traj_buoy_id ON traj_buoy_trajectory(traj_buoy_id);
CREATE INDEX IX_traj_date ON traj_buoy_trajectory(traj_date);
CREATE INDEX IX_traj_location ON traj_buoy_trajectory USING GIST(traj_location);
CREATE INDEX IX_traj_speed_velocity ON traj_buoy_trajectory(traj_speed_velocity);
CREATE INDEX IX_traj_variance_location ON traj_buoy_trajectory USING GIST(traj_variance_location);


