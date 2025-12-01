# Models

This document lays out the data models used to create the book club system.

## User

**users**
- id (UUID, primary key)
- username (string, unique, indexed)
- email (string, unique, indexed)
- full_name (string, nullable)
- is_active (boolean, default: true)
- created_at (datetime)
- updated_at (datetime)

**user_security**
- user_id (UUID, foreign key to users.id)
- email (string, unique, indexed)
- password (string)
- old_password (string, nullable)
- password_changed_at (datetime, nullable)
- created_at (datetime)
- updated_at (datetime)

**user_roles** (association table)
- user_id (UUID, foreign key to users.id)
- role_id (UUID, foreign key to roles.id)
- assigned_at (datetime)

**user_groups** (association table)
- user_id (UUID, foreign key to users.id)
- group_id (UUID, foreign key to groups.id)
- joined_at (datetime)

**user_pages** (association table)
- user_id (UUID, foreign key to users.id)
- page_id (UUID, foreign key to pages.id)
- join_date (datetime)

**user_clubs** (association table)
- user_id (UUID, foreign key to users.id)
- club_id (UUID, foreign key to clubs.id)
- join_date (datetime)
- role (string, default: "member")

**refresh_tokens**
- id (UUID, primary key)
- user_id (UUID, foreign key to users.id)
- token_hash (string, unique, indexed)
- expires_at (datetime, indexed)
- created_at (datetime)
- revoked (boolean, default: false)
- replaced_by_token_id (UUID, foreign key to refresh_tokens.id, nullable)
- device_info (string, nullable)
- ip_address (string, nullable)

## Roles

**roles**
- id (UUID, primary key)
- name (string, unique, indexed)
- description (string, nullable)
- created_at (datetime)
- updated_at (datetime)

## Groups

**groups**
- id (UUID, primary key)
- name (string, indexed)
- description (string, nullable)
- created_by (UUID, foreign key to users.id)
- created_at (datetime)
- updated_at (datetime)

## Pages

Pages represent a specific theme or topic, used in a similar fashion to Reddit pages.

**pages**
- id (UUID, primary key)
- name (string, unique, indexed)
- description (string, nullable)
- topic (string, indexed, nullable)
- created_by (UUID, foreign key to users.id)
- is_active (boolean, default: true)
- created_at (datetime)
- updated_at (datetime)

## Clubs

Clubs represent book clubs that users can join together.

**clubs**
- id (UUID, primary key)
- name (string, indexed)
- description (string, nullable)
- topic (string, indexed, nullable)
- created_by (UUID, foreign key to users.id)
- is_active (boolean, default: true)
- max_members (integer, nullable)
- created_at (datetime)
- updated_at (datetime)

**club_meetings**
- id (UUID, primary key)
- club_id (UUID, foreign key to clubs.id, indexed)
- meeting_id (UUID, foreign key to meetings.id, indexed)
- start_date (datetime)
- end_date (datetime, nullable)
- frequency (string, default: "once") - Options: once, daily, weekly, monthly
- recurrence_rule (string, nullable) - iCal RRULE format
- created_at (datetime)
- updated_at (datetime)

## Meetings

**meetings**
- id (UUID, primary key)
- name (string)
- description (string, nullable)
- status (string, default: "scheduled") - Options: scheduled, in_progress, completed, cancelled
- scheduled_start (datetime)
- scheduled_end (datetime)
- actual_start (datetime, nullable)
- actual_end (datetime, nullable)
- duration (integer) - Duration in minutes
- created_by (UUID, foreign key to users.id)
- club_id (UUID, foreign key to clubs.id, nullable)
- created_at (datetime)
- updated_at (datetime)

## Books

**publishers**
- id (UUID, primary key)
- name (string, unique, indexed)
- country (string, nullable)
- website (string, nullable)
- created_at (datetime)
- updated_at (datetime)

**books**
- id (UUID, primary key)
- title (string, indexed)
- author (string, indexed)
- date_of_first_publish (date, nullable)
- genre (string, indexed, nullable)
- description (text, nullable)
- cover_image_url (string, nullable)
- series_title (string, nullable)
- volume_number (integer, nullable)
- volume_title (string, nullable)
- created_at (datetime)
- updated_at (datetime)

**book_versions**
- id (UUID, primary key)
- book_id (UUID, foreign key to books.id, indexed)
- publisher_id (UUID, foreign key to publishers.id, indexed, nullable)
- isbn (string, unique, indexed)
- publish_date (date, nullable)
- edition (string, nullable)
- editors (string, nullable)
- editor_info (text, nullable)
- created_at (datetime)
- updated_at (datetime)

**user_books**
- id (UUID, primary key)
- user_id (UUID, foreign key to users.id, indexed)
- book_id (UUID, foreign key to books.id, indexed)
- book_version_id (UUID, foreign key to book_versions.id, indexed, nullable)
- added_date (datetime)
- is_read (boolean, default: false)
- read_date (datetime, nullable)
- reading_status (string, default: "unread") - Options: unread, reading, finished
- rating (float, nullable) - Range: 0.0 to 5.0
- review (text, nullable)
- notes (text, nullable)
- is_favorite (boolean, default: false)
- created_at (datetime)
- updated_at (datetime)

**reading_lists**
- id (UUID, primary key)
- user_id (UUID, foreign key to users.id, indexed)
- name (string)
- description (text, nullable)
- created_date (datetime)
- is_default (boolean, default: false)
- created_at (datetime)
- updated_at (datetime)

**reading_list_items**
- id (UUID, primary key)
- reading_list_id (UUID, foreign key to reading_lists.id, indexed)
- user_book_id (UUID, foreign key to user_books.id, indexed)
- order_index (integer)
- added_date (datetime)
- created_at (datetime)
- updated_at (datetime)
