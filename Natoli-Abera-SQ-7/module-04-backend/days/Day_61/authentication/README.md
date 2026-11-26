# Authentication Flow

A lightweight NestJS authentication service using **Argon2** for password and token hashing, and **JWT** (Access + Refresh tokens) for session management.

---

## 🔐 Architecture Overview

- **Password Hashing**: Uses `argon2` for secure hashing.
- **Access Tokens**: Short-lived (15 minutes), signed with `JWT_ACCESS_SECRET`. Used in the `Authorization: Bearer <token>` header to access protected routes.
- **Refresh Tokens**: Long-lived (7 days), signed with `JWT_REFRESH_SECRET`. Stored as an Argon2 hash on the user record for rotation and secure verification.
- **Global Prefix**: All routes are mounted under `/api`.

---

## 🔄 Authentication Flows

### 1. Registration (`POST /api/auth/register`)
```text
Client                          Server
  |                               |
  |--- POST /api/auth/register -->|
  |    { email, password }        |-- Checks if email exists (409 on duplicate)
  |                               |-- Hashes password with Argon2
  |                               |-- Creates user with default role: ['customer']
  |<-- 201 Created ---------------|
       { id, email, roles }
```

### 2. Login (`POST /api/auth/login`)
```text
Client                          Server
  |                               |
  |--- POST /api/auth/login ----->|
  |    { email, password }        |-- Verifies user credentials with Argon2
  |                               |-- Generates Access Token (15m) & Refresh Token (7d)
  |                               |-- Hashes Refresh Token with Argon2 and saves to user
  |<-- 200 OK --------------------|
       { accessToken, refreshToken }
```

### 3. Access Protected Route (`GET /api/auth/me`)
```text
Client                          Server
  |                               |
  |--- GET /api/auth/me --------->|
  |    Header: Bearer <accessToken>-- JwtAuthGuard & JwtStrategy validate token
  |                               |-- Extracts user payload ({ id, email, roles })
  |<-- 200 OK --------------------|
       { id, email, roles }
```

### 4. Refresh Token Rotation (`POST /api/auth/refresh`)
```text
Client                          Server
  |                               |
  |--- POST /api/auth/refresh --->|
  |    { refreshToken }           |-- Verifies token signature & expiration
  |                               |-- Compares token against stored Argon2 hash
  |                               |-- Generates a NEW pair of access & refresh tokens
  |                               |-- Saves new hashed refresh token (rotation)
  |<-- 200 OK --------------------|
       { accessToken, refreshToken }
```

### 5. Logout (`POST /api/auth/logout`)
```text
Client                          Server
  |                               |
  |--- POST /api/auth/logout ---->|
  |    Header: Bearer <accessToken>-- Authenticates user via JwtAuthGuard
  |                               |-- Sets user's refreshTokenHash to null
  |<-- 200 OK --------------------|
       { message: "Logged out" }
```

---

## 📋 API Summary

| Endpoint | Method | Auth Required | Description |
| :--- | :--- | :--- | :--- |
| `/api/auth/register` | `POST` | No | Registers new user; returns user profile |
| `/api/auth/login` | `POST` | No | Validates credentials; returns access & refresh tokens |
| `/api/auth/me` | `GET` | Bearer Token | Returns current authenticated user details |
| `/api/auth/refresh` | `POST` | No | Exchanges valid refresh token for a new token pair |
| `/api/auth/logout` | `POST` | Bearer Token | Invalidates refresh token by setting hash to null |

---

## ⚙️ Environment Variables

Ensure the following are defined in your `.env`:

```env
PORT=3000
JWT_ACCESS_SECRET="your-access-secret"
JWT_REFRESH_SECRET="your-refresh-secret"
```

---

## 🧪 Testing

Requests are prepared in [`src/auth/auth.http`](file:///c:/Users/suraf/OneDrive/Documenten/IBT-sq1/module-04-backend/Days/Day_61/authentication/src/auth/auth.http) for testing via the REST Client extension.
