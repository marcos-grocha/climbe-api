# Delta for servicos

## ADDED Requirements

### Requirement: List servicos

The system SHALL expose `GET /servicos` to any authenticated user (needed for the empresa form).

#### Scenario: Authenticated user lists servicos

- GIVEN an authenticated user
- WHEN `GET /servicos` is requested
- THEN the response is 200 with the 5 seeded Climbe services
