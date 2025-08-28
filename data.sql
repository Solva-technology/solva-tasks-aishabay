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
1437758de114
\.


--
-- Data for Name: user; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public."user" (email, hashed_password, is_active, is_superuser, is_verified, id, created_at, updated_at) FROM stdin;
root@gmail.com	$argon2id$v=19$m=65536,t=3,p=4$MWiv/rHJQFNHMzdXJXvZLg$Epb8YKQEzzqrFFTXELsGG6jCeynKLQ56pBdstv5T9eY	t	t	t	1	2025-08-28 08:25:57.375682+00	2025-08-28 08:28:50.691585+00
\.


--
-- Name: user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.user_id_seq', 1, true);


--
-- PostgreSQL database dump complete
--

