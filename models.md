user

user_security

user_roles

user_groups

user_pages

user_clubs

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
