\COPY public.conn(mno, rsrq, rsrp, sinr, type, tijd, lat, long, cell_plmn, tac_lac, cell_utran_id) FROM '/home/cfns/systemtest/modem.csv' DELIMITERS ',' CSV HEADER NULL AS ' ';
UPDATE public.conn set coordinates = ST_GeogFromText('POINT(' || long || ' ' || lat ||')');
