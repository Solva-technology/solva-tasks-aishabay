--
-- PostgreSQL database dump
--

-- Dumped from database version 15.13
-- Dumped by pg_dump version 15.13

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.alembic_version (version_num) FROM stdin;
fcbd1710d04d
\.


--
-- Data for Name: user; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public."user" (email, hashed_password, is_active, is_superuser, is_verified, id, created_at, updated_at, telegram_id, username, full_name, role) FROM stdin;
manager@gmail.com	$argon2id$v=19$m=65536,t=3,p=4$ReyjLpvEcTQRQYiU15n2JA$nuCM9ENC/hBTo/Svr2/0ZL5cJe8JHA5TcMuPigO9TCw	t	f	f	1	2025-09-17 08:41:55.594171+00	2025-09-17 08:41:55.594171+00	2	manager	manager	manager
teacher@gmail.com	$argon2id$v=19$m=65536,t=3,p=4$Twvu+64RGo6OgVYx1ogszw$ie+RqGzVihlu7lFug2p+jyV/RxWk7gGuAmUmS3iHfEs	t	f	f	2	2025-09-17 08:43:00.846391+00	2025-09-17 08:43:00.846391+00	1	teacher	teacher	teacher
admin@gmail.com	$argon2id$v=19$m=65536,t=3,p=4$dX+sDU+owKlAl7pmYkMMgQ$Q0nzW3KfwwHsPJmy5qfmD6ol7I61VfzFE1e1XmVPt/E	t	f	f	3	2025-09-17 08:43:23.469521+00	2025-09-17 08:43:23.469521+00	0	admin	admin	admin
student1@gmail.com	$argon2id$v=19$m=65536,t=3,p=4$qHWuV8ewSxAB1iM5URyGuQ$e05eDBpyzzpHt2xgdNdJpz1/ArfttyMHm23VXVWmOwk	t	f	f	4	2025-09-17 08:44:09.569717+00	2025-09-17 08:44:09.569717+00	3	student1	student1	student
student2@gmail.com	$argon2id$v=19$m=65536,t=3,p=4$Qf/xxNxVtOA0khLyN48BcQ$jVpmEIWfveP0JQX2RoGN3Z2EdaKUfQYoN/1V2yXBcxQ	t	f	f	5	2025-09-17 08:44:28.847256+00	2025-09-17 08:44:28.847256+00	4	student2	student2	student
\.


--
-- Name: user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.user_id_seq', 5, true);


--
-- PostgreSQL database dump complete
--

