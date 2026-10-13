# Database Design

## Table 1 : Users

| Column | Data Type | Description |
|---------|-----------|-------------|
| user_id | INT | Primary Key |
| username | VARCHAR(50) | User Name |
| password | VARCHAR(255) | Password |
| role | VARCHAR(20) | Admin / Staff / Manager |

---

## Table 2 : Flights

| Column | Data Type |
|---------|-----------|
| flight_id | INT |
| flight_number | VARCHAR(20) |
| airline | VARCHAR(50) |
| origin | VARCHAR(50) |
| destination | VARCHAR(50) |
| scheduled_arrival | DATETIME |
| actual_arrival | DATETIME |
| scheduled_departure | DATETIME |
| actual_departure | DATETIME |
| status | VARCHAR(20) |

---

## Table 3 : Gates

| Column | Data Type |
|---------|-----------|
| gate_id | INT |
| gate_number | VARCHAR(10) |
| terminal | VARCHAR(20) |
| gate_status | VARCHAR(20) |

---

## Table 4 : Ground Staff

| Column | Data Type |
|---------|-----------|
| staff_id | INT |
| staff_name | VARCHAR(100) |
| department | VARCHAR(50) |
| shift | VARCHAR(20) |

---

## Table 5 : Baggage

| Column | Data Type |
|---------|-----------|
| baggage_id | INT |
| flight_number | VARCHAR(20) |
| baggage_count | INT |
| baggage_weight | DECIMAL |

---

## Table 6 : Fuel

| Column | Data Type |
|---------|-----------|
| fuel_id | INT |
| flight_number | VARCHAR(20) |
| fuel_loaded | DECIMAL |
| fuel_status | VARCHAR(20) |