\COPY public.conn(mno, "RSRQ", "RSRP", "SINR", type, tijd,  lat, long  ) FROM '/home/cfns/systemtest/modem.csv' DELIMITERS ',' CSV HEADER NULL AS ' ';
UPDATE public.conn set coordinates = ST_GeogFromText('POINT(' || long || ' ' || lat ||')');
