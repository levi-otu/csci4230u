# Models

This documents lays out the data models that will be used to create the book club system.

## User

user

user_security

- id
- user_id
- email
- password
- old_password

user_roles

- user_id
- role_id

user_groups

- user_id
- group_id

user_pages

- user_id
- page_id
- join_date

user_clubs

- user_id
- club_id
- join_date

// User meetings are for individually scheduled meetings between users.
user_meetings

## Groups

The groups will allow for the grouping of users. This can be under interests, clubs, boards, etc.

groups

## Pages

Pages represent a specific theme or topic. These are used in a similar fashion to reddit pages.

pages:

- id

## Clubs

Clubs represent book clubs that users can join in together.

clubs

- id
- name
- description
- topic

// Club meetings are for reoccuring meetings for a club.
club_meetings

- id
- club_id
- start_date
- end_date
- frequency

## Meetings

meetings:

- id
- name
- description
- status
- scheduled_start
- scheduled_end
- actual_start
- actual_end
- duration

## Books

books

- id
- name
- author
- date_of_first_publish

book_versions

- id
- publisher
- isbn
- publish_date
- editors
- editor_info

## publishers
