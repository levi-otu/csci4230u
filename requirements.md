# The Public Square

At the core of its functionality, The Public Square is an online community that allows for the free sharing of ideas. To enable this, Public Square revolves around the reading of books, sharing of ideas, and open discussion of any range of topics.

Core features the The Public Square includes are:

- Book clubs for users to read, study, and share ideas together.
  - Online video streaming using WebRTC.
  - Meeting scheduling and integration with ical calendars.
- Discussion boards where users can create discussion threads on common topics.
- Personal libraries and readings lists for users to track their readings.

## Technical

The csci4230u repository houses the application logic for The Public Square. It splits the web application into two primary directories for the frontend and backend systems. The technologies used in each are listed below:

Frontend:

- Vite + React TypeScript
- Radix/Shadcn for styling.
- Tailwind CSS
- ESLint as a linter.
-

Backend:

- Python FastAPI
- SQLAlchemy
- Alembic for data migrations
- Pydantic data models

## Style

The primary style in the Website will be an amber orange. Dark theme is encouraged but a light theme will also be available to users. All components will be fully customizable with shadcn.

## Pages

The following are pages included in our book club application.

- Login
  - Forgot Password
- Register
- Home
- Clubs
  - Join a club
  - Create a club
  - Club page
    - Club settings (RBAC restricted)
      - Schedule meetings
    - Meetings
      - Meet now
    - Discussions
- Pages (a topic/theme page such as "theology", "Dostoyevsky", in a reddit theme style)
  - Follow
  - View
  - Filter
- Library
  - Books
  - Register new book
  - Remove a book
