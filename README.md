# Ontario Tech University CSCI4230 Final Project

This is a final project for Ontario Tech University's Advanced Web Development course (csci4230).

## Requirements

The core requirements for the final project are as follows.

### API & Project Evaluation Criteria

#### API Design and Integration (15%)

- Clear and well-structured API endpoints
- Proper use of HTTP methods (GET, POST, PUT, DELETE)
- Integration with at least one external API
- Documentation of the API endpoints

#### Architectural Design (15%)

- Implementation of chosen architecture (e.g., Microservices, Monolithic, MVC)
- Proper separation of concerns (frontend, backend, database)
- Diagram and explanation of the chosen architecture (UML package and class diagrams)

#### Authentication and Security (10%)

- Implementation of secure user authentication (e.g., OAuth, JWT, etc.)
- Protection of sensitive routes with proper authorization checks
- Handling of user sessions and secure storage of credentials

#### Database Design and ORM (10%)

- Database schema design
- Use of an ORM for database interactions (e.g., SQLAlchemy, Django ORM)
- Implementation of CRUD operations
- Use of relationships between data entities

#### Testing and Quality Assurance (10%)

- Unit tests covering core functionalities
- Integration tests for API endpoints
- End-to-end tests with Selenium

#### Deployment and DevOps (10%)

- Deployment to a cloud platform or a general-purpose server
- Use of Docker for deployment consistency
- Setup of a CI/CD pipeline
- Documentation of deployment process
- Use of HTTPS with either HTTP/2 or HTTP/3

#### Performance Optimization (5%)

- Analysis of application performance using <https://pagespeed.web.dev/>

#### Version Control and Collaboration (5%)

- Use of Git and GitHub/GitLab for version control
- Regular commits with clear messages
- Properly documented README file with project setup instructions

#### Code Quality and Documentation (5%)

- Proper use of comments and docstrings
- Adherence to coding standards and best practices (e.g., PEP 8 for Python)
- Comprehensive project documentation, including setup, usage, and architecture

#### Presentation and Demonstration (15%)

- Clear and organized presentation of the project
- Demonstration of key features
- Explanation of design decisions and challenges faced
- Q&A session to assess understanding and depth of knowledge

## Project Overview

Our project idea is to build a book club web application. The core concepts in the app will be to allow for the formulation of groups, discussion of topics in themes (think reddit but for book/theme discussion pages), and a meeting scheduler to allow users to schedule regular meeting times for their clubs.

If we can get ambitious we will attempt to implement WebRTC for real-time video streaming. We'll add some CI/CD pipelines to allow for the deployment of new versions and set automated deployment dependent on tests passing.

### Technologies

The stack will be the following:

- React/Shadcn frontend using TypeScript
- WebRTC for video streaming
- Python/FastAPI/Alembic backend
- PostgresSQL database
- GitHub Actions for CI/CD
- CodeQL SAST scanning
- Docker
- Selenium
- Google cloud for web hosting
- Radix for worker/queue service

### Quality Standards

- Adherence to defined code standards:
  - CodeQL security scanning.
  - PEP8.
  - ESLint for TypeScript rules.
