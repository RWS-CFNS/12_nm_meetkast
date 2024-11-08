<<<<<<< HEAD
\COPY public.conn(mno, "RSRQ", "RSRP", "SINR", type, tijd,  lat, long  ) FROM '/home/cfns/systemtest/modem.csv' DELIMITERS ',' CSV HEADER NULL AS ' ';
=======
\COPY public.conn(mno, rsrq, rsrp, sinr, type, tijd, lat, long, cell_plmn, tac_lac, cell_utran_id) FROM '/home/cfns/systemtest/modem.csv' DELIMITERS ',' CSV HEADER NULL AS ' ';
>>>>>>> 0c5826d (bewerkte meetkast script, nu met; GPS coordinaten, cell tower informatie.)
UPDATE public.conn set coordinates = ST_GeogFromText('POINT(' || long || ' ' || lat ||')');
