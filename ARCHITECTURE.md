# Architecture

Four-layer structure based on dependency weight.

> AI: Read this file before generating code in this project.

---

## Layers

### R1 • Domain

**Purpose:** Core business logic

**Dependencies:** Zero external dependencies

**Contains:**
- Entities (User, Order, Product)
- Value objects (Email, Money, Address)
- Domain services (pure business logic)
- Interfaces (contracts for R2 to implement)

**Rules:**
- Cannot import from R2, R3, or R4
- No framework dependencies
- No I/O operations
- Pure functions only

**Example:**

```python
# src/domain/user.py
class User:
    def __init__(self, id, email, name):
        self.id = id
        self.email = email
        self.name = name
    
    def is_valid_email(self):
        return '@' in self.email
```

**Changes when:**
Business rules change

---

### R2 • Database

**Purpose:** Persistence layer

**Dependencies:** Domain only (R1)

**Contains:**
- Repositories (implement domain interfaces)
- Database connections
- Query builders
- Migrations
- Data mappers

**Rules:**
- Can import from R1
- Cannot import from R3 or R4
- Implements interfaces defined in R1
- All database-specific logic here

**Example:**

```python
# src/database/user_repository.py
from domain.user import User

class UserRepository:
    def __init__(self, connection):
        self.db = connection
    
    def save(self, user: User):
        self.db.execute(
            "INSERT INTO users VALUES (?, ?, ?)",
            (user.id, user.email, user.name)
        )
    
    def find_by_id(self, user_id):
        row = self.db.query("SELECT * FROM users WHERE id = ?", user_id)
        return User(row['id'], row['email'], row['name'])
```

**Changes when:**
Data model evolves

---

### R3 • API

**Purpose:** Orchestration layer

**Dependencies:** Domain (R1) + Database (R2)

**Contains:**
- HTTP routes
- Request handlers
- Response formatters
- Authentication middleware
- Validation

**Rules:**
- Can import from R1 and R2
- Cannot import from R4
- Orchestrates domain + database operations
- Translates HTTP ↔ domain concepts

**Example:**

```python
# src/api/user_routes.py
from domain.user import User
from database.user_repository import UserRepository

def register_user(request):
    # Extract from HTTP
    data = request.json
    
    # Create domain entity
    user = User(
        id=generate_id(),
        email=data['email'],
        name=data['name']
    )
    
    # Validate
    if not user.is_valid_email():
        return {"error": "Invalid email"}, 400
    
    # Persist
    repo = UserRepository(db_connection)
    repo.save(user)
    
    # Return HTTP response
    return {"user_id": user.id}, 201
```

**Changes when:**
Client needs change

---

### R4 • Integrations

**Purpose:** External world adapters

**Dependencies:** All layers (R1, R2, R3)

**Contains:**
- Payment gateways (Stripe, PayPal)
- Email services (SendGrid, Mailgun)
- Authentication providers (Auth0, OAuth)
- UI components (React, Vue)
- Third-party APIs

**Rules:**
- Can import from all layers
- Adapts external systems to domain
- All external I/O here
- Most volatile layer

**Example:**

```python
# src/integrations/email_service.py
import sendgrid
from domain.user import User

class EmailService:
    def __init__(self, api_key):
        self.client = sendgrid.SendGridAPIClient(api_key)
    
    def send_verification_email(self, user: User):
        message = {
            "to": user.email,
            "from": "noreply@example.com",
            "subject": "Verify your email",
            "body": f"Hi {user.name}, please verify..."
        }
        self.client.send(message)
```

**Changes when:**
External systems change

---

## Dependency Flow

```
        ┌─────────────┐
        │   Domain    │  R1 (zero dependencies)
        │   (R1)      │
        └─────────────┘
              ▲
              │
        ┌─────────────┐
        │  Database   │  R2 (depends on R1)
        │   (R2)      │
        └─────────────┘
              ▲
              │
        ┌─────────────┐
        │     API     │  R3 (depends on R1 + R2)
        │   (R3)      │
        └─────────────┘
              ▲
              │
        ┌─────────────┐
        │Integrations │  R4 (depends on all)
        │   (R4)      │
        └─────────────┘
```

**Key principles:**

1. **Arrows point up** - Dependencies flow toward core
2. **Core is stable** - Domain changes least frequently
3. **Periphery is volatile** - Integrations change most frequently
4. **Layers are isolated** - Each can be tested independently

---

## Examples

### Feature: User Registration

**Files created:**

```
src/domain/user.py                    [R1/C2]
src/database/user_repository.py       [R2/C2]
src/api/registration_routes.py        [R3/C2]
src/integrations/email_service.py     [R4/C2]
```

**Dependency flow:**

```
email_service.py (R4)
    ↓ imports
registration_routes.py (R3)
    ↓ imports
user_repository.py (R2)
    ↓ imports
user.py (R1)
```

All dependencies flow toward R1. Validated automatically.

---

### Feature: Payment Processing

**Files created:**

```
src/domain/payment.py                 [R1/C2]
src/database/payment_repository.py    [R2/C2]
src/api/payment_routes.py             [R3/C2]
src/integrations/stripe_gateway.py    [R4/C2]
```

**Dependency flow:**

```
stripe_gateway.py (R4)
    ↓ imports
payment_routes.py (R3)
    ↓ imports
payment_repository.py (R2)
    ↓ imports
payment.py (R1)
```

Stripe is isolated in R4. Can swap for PayPal without touching R1-R3.

---

## Anti-patterns

### ❌ Domain importing Database

```python
# src/domain/user.py
from database.user_repository import UserRepository  # BLOCKED

class User:
    def save(self):
        repo = UserRepository()  # Domain should not know about persistence
        repo.save(self)
```

**Why blocked:**
Domain becomes coupled to database implementation.

**Fix:**
API orchestrates:

```python
# src/api/user_routes.py
from domain.user import User
from database.user_repository import UserRepository

def create_user(request):
    user = User(...)  # Domain
    repo = UserRepository()  # Database
    repo.save(user)  # API orchestrates
```

---

### ❌ Database importing API

```python
# src/database/user_repository.py
from api.authentication import get_current_user  # BLOCKED

class UserRepository:
    def save(self, user):
        current_user = get_current_user()  # Wrong layer
```

**Why blocked:**
Database should not know about HTTP context.

**Fix:**
Pass user explicitly:

```python
# src/api/user_routes.py
def update_user(request):
    current_user = get_current_user()  # API knows about auth
    repo = UserRepository()
    repo.save(user, updated_by=current_user)
```

---

### ❌ API importing Integrations

```python
# src/api/user_routes.py
from integrations.stripe import StripeClient  # BLOCKED

def create_user(request):
    stripe = StripeClient()  # API should not know about Stripe
```

**Why blocked:**
API becomes coupled to specific payment provider.

**Fix:**
Integration calls API:

```python
# src/integrations/stripe_webhook.py
from api.payment_routes import process_payment

def handle_webhook(event):
    process_payment(event.data)  # Integration → API
```

---

## Testing

Each layer can be tested independently:

**R1 • Domain:**
```python
def test_user_validation():
    user = User(1, "invalid", "Test")
    assert not user.is_valid_email()
```

**R2 • Database:**
```python
def test_user_repository():
    repo = UserRepository(mock_connection)
    user = User(1, "test@example.com", "Test")
    repo.save(user)
    assert repo.find_by_id(1).email == "test@example.com"
```

**R3 • API:**
```python
def test_registration():
    response = register_user(mock_request)
    assert response.status_code == 201
```

**R4 • Integrations:**
```python
def test_email_service():
    service = EmailService(mock_api_key)
    user = User(1, "test@example.com", "Test")
    service.send_verification_email(user)
    assert mock_client.send_called
```

---

## Migration Guide

### From existing codebase:

1. **Identify domain logic**
   Move to `src/domain/`

2. **Identify persistence**
   Move to `src/database/`

3. **Identify HTTP handlers**
   Move to `src/api/`

4. **Identify external services**
   Move to `src/integrations/`

5. **Run validators**
   ```
   .living-arch/tools/validate-all.sh
   ```

6. **Fix violations**
   Validators will identify illegal imports

---

## Version

1.0.0

Dependencies flow toward core.
Validators enforce automatically.
Structure remains consistent.
