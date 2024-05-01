# 💾 Database

## Why PostgreSQL?

PostgreSQL is chosen as the database solution for this project due to its robust performance in handling large datasets. As an open-source RDBMS, PostgreSQL offers advanced indexing, efficient query optimization, and support for complex data types, ensuring scalability and optimal data management. Its ACID compliance guarantees data integrity, making it a secure and reliable choice for applications dealing with substantial amounts of information. With PostgreSQL, the project can efficiently store, retrieve, and manipulate extensive data sets, meeting the technical requirements for handling significant data loads.

## Schemama Overview

### Table structure

- **users** table used for storing user data

  ```sql
  CREATE TABLE "users" (
  "is_administrator" boolean,
  "id" bigint PRIMARY KEY NOT NULL,
  "email" varchar(255),
  "name" varchar(255),
  "surname" varchar(255),
  "uid" varchar(255)
  );
  ```

- **panda_device** table storing data acording Panda devices

  ```sql
  CREATE TABLE "panda_device" (
  "status" boolean,
  "id" bigint PRIMARY KEY NOT NULL,
  "owner" bigint,
  "api_key" varchar(255),
  "location" varchar(255),
  "name" varchar(255),
  "uuid" varchar(255)
  );
  ```

- **api_keys** table used for storing api keys that are then being used to give Panda devides access to Bamboo API

  ```sql
  CREATE TABLE "api_keys" (
  "active" boolean,
  "created" timestamp(6),
  "id" bigint PRIMARY KEY NOT NULL,
  "owner" bigint,
  "panda" bigint,
  "key" varchar(255)
  );
  ```

- **panda_status** used for allowing Panda owner to verify panda status

  ```sql
  CREATE TABLE "panda_status" (
  "status" smallint,
  "id" bigint PRIMARY KEY NOT NULL,
  "last_connection" timestamp(6),
  "uuid" varchar(255)
  );
  ```

- **data_packets** table is storing data collected by Panda devies that will further be analysed

  ```sql
  CREATE TABLE "data_packets" (
  "date" date,
  "people_count" integer NOT NULL,
  "time" time(6),
  "id" bigint PRIMARY KEY NOT NULL,
  "panda_id" bigint,
  "day_of_week" varchar(255)
  );
  ```

### Database diagram

![DB diagram](https://i.imgur.com/OeMf4E6.png)
