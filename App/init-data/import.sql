COPY public.device_1(time_data, temp, compStat)
FROM '/var/lib/postgresql@17/ColdRoom_DataLogger.csv'
DELIMITER ','
CSV HEADER;

COPY public.device_2(time_data, temp, evapTemp, defroStat, compStat, evapStat)
FROM '/var/lib/postgresql@17/Freezer_DataLogger.csv'
DELIMITER ','
CSV HEADER;