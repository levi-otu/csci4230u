When writing Backend Python code:

- Strictly follow PEP 8 style guide
- Always create test cases with pytest
- Minimum 80% code coverage requirement using selenium
- All new handlers must have unit tests.
- Run coverage reports after writing tests
- Use type hints for all function signatures
- API is split between handlers, transports, and api endpoints.
- Handlers handle business logic, transports handle data transportation, and endpoints handle routes.
- Storage handles data storage.
- All new api handlers must be written with test cases. A task is not complete until test coverage is complete with all tests passing.
