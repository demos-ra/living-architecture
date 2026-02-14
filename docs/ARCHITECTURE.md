# Architecture

Living Architecture R0-R5 pluggable framework.

> **AI:** Read this file before generating code in Living Architecture projects.

---

## Overview

Living Architecture is a dependency-based code organization system. Code is organized into layers based on dependency weight - components with zero dependencies sink to the core, components with maximum dependencies float to the periphery.

The system uses up to 6 layers (R0-R5). Projects start minimal with 2 required layers and add optional layers as complexity grows.

---

## The Framework

### Core Principle

**Dependency Gravity**

Dependencies create weight. Heavy components (many dependencies) belong at the periphery. Light components (zero dependencies) belong at the core.

This creates a natural stability gradient:
- Core (R0-R1): Heavy, stable, rarely changes
- Middle (R2-R3): Moderate weight, changes with features
- Periphery (R4-R5): Light, volatile, frequently replaced

---

## The Six Layers (R0-R5)

### Required Layers (Always Present)

Every system must have these two layers:

#### R3 • INTERFACE

**Purpose:** API boundaries and contracts

**When to add:** Always present (every system has boundaries)

**Contains:**
- REST endpoints
- GraphQL resolvers
- CLI handlers
- DTO mapping
- Input validation
- Output formatting

**Dependencies:** Can import from R0, R1, R2

**Cannot import from:** R4 (infrastructure), R5 (presentation)

**Example:**
```python
# src/interface/user_routes.py
from application.create_user import CreateUserWorkflow  # R2
from domain.user import User  # R1

class UserRoutes:
    def post_user(self, request):
        workflow = CreateUserWorkflow()
        user = workflow.execute(request.data)
        return {"id": user.id, "email": user.email}
```

**Changes when:** API contracts change, client needs evolve

---

#### R4 • INFRASTRUCTURE

**Purpose:** External world interactions

**When to add:** Always present (every system executes somewhere)

**Contains:**
- Database repositories
- Message queues
- Cache clients
- External API clients
- File system access
- Email services
- Payment gateways

**Dependencies:** Can import from R0, R1, R2

**Cannot import from:** R3 (interface), R5 (presentation)

**Note:** Infrastructure and Interface are peers. Neither should depend on the other.

**Example:**
```python
# src/infrastructure/user_repository.py
from domain.user import User  # R1
import psycopg2

class UserRepository:
    def __init__(self, connection):
        self.db = connection
    
    def save(self, user: User):
        self.db.execute(
            "INSERT INTO users VALUES (%s, %s)",
            (user.id, user.email)
        )
```

**Changes when:** External systems change, persistence needs evolve

---

### Optional Layers (Add When Needed)

#### R0 • CONFIG

**Purpose:** Environment and deployment configuration

**When to add:** When you have >5 configuration concerns

**Contains:**
- Environment variables
- Feature flags
- Deployment parameters
- Multi-tenant configuration
- Regional settings
- Service discovery

**Dependencies:** None (root layer)

**Example:**
```python
# src/config/settings.py
class Settings:
    DATABASE_URL = os.getenv("DATABASE_URL")
    STRIPE_API_KEY = os.getenv("STRIPE_API_KEY")
    FEATURE_NEW_CHECKOUT = os.getenv("FEATURE_NEW_CHECKOUT", "false")
```

**Changes when:** Deployment topology changes, features toggle

**Skip if:** All configuration fits in a single environment file

---

#### R1 • DOMAIN

**Purpose:** Business entities and invariants

**When to add:** When you have >10 business rules

**Contains:**
- Entities (User, Order, Product)
- Value objects (Email, Money, Address)
- Business invariants
- Domain services (pure business logic)
- Domain events
- Interfaces (contracts for other layers)

**Dependencies:** R0 (config) if it exists

**Cannot import from:** R2, R3, R4, R5

**Rules:**
- No framework dependencies
- No I/O operations
- Pure functions only
- Business logic belongs here

**Example:**
```python
# src/domain/user.py
class User:
    def __init__(self, id, email, name):
        self.id = id
        self.email = email
        self.name = name
    
    def is_valid_email(self):
        # Pure business logic
        return '@' in self.email and '.' in self.email.split('@')[1]
    
    def can_purchase(self, amount):
        # Business rule
        return amount <= self.credit_limit
```

**Changes when:** Business rules change, domain model evolves

**Skip if:** Business logic is simple enough to live in application layer

---

#### R2 • APPLICATION

**Purpose:** Use cases, workflows, and orchestration

**When to add:** When you have >3 workflows or need state machines

**Contains:**
- Use cases (CreateOrder, RegisterUser)
- Workflows and sagas
- Business process coordination
- State machines
- Application services
- Orchestration logic

**Dependencies:** R0, R1 (if they exist)

**Cannot import from:** R3, R4, R5

**Example:**
```python
# src/application/create_order.py
from domain.order import Order  # R1
from domain.user import User  # R1

class CreateOrderWorkflow:
    def execute(self, user: User, items):
        # Orchestrate business logic
        if not user.can_purchase(total):
            raise InsufficientCredit()
        
        order = Order(user, items)
        order.validate()
        
        return order
```

**Changes when:** Business processes change, workflows evolve

**Skip if:** 
- You only have simple CRUD operations
- You're using pure CQRS (queries bypass this layer)
- Business logic fits directly in interface handlers

---

#### R5 • PRESENTATION

**Purpose:** UI and rendering

**When to add:** When you have >1 frontend

**Contains:**
- React components
- Vue pages
- Mobile app screens
- Desktop UI
- Templates
- Client-side state management

**Dependencies:** R0 (config), R3 (interface) only

**Cannot import from:** R1, R2, R4

**Note:** Presentation talks to Interface only. It never reaches into domain or infrastructure.

**Example:**
```javascript
// src/presentation/web/UserProfile.jsx
import { getUserAPI } from 'interface/api_client';  // R3

function UserProfile({ userId }) {
    const [user, setUser] = useState(null);
    
    useEffect(() => {
        getUserAPI(userId).then(setUser);
    }, [userId]);
    
    return <div>{user?.name}</div>;
}
```

**Changes when:** UI requirements change, new frontends added

**Skip if:** You only have one frontend (can live in R3/interface)

---

## Dependency Rules

### Allowed Dependencies

```
R0 ← R1 ← R2 ← R3
 ↑    ↑    ↑    
 └────┴────┴──── R4

R0 ← R3 ← R5
```

**In plain language:**
- R0 depends on nothing (root)
- R1 can depend on R0
- R2 can depend on R0, R1
- R3 can depend on R0, R1, R2
- R4 can depend on R0, R1, R2 (NOT R3 or R5)
- R5 can depend on R0, R3 (NOT R1, R2, R4)

### Forbidden Dependencies

```
R0 → anything          ❌ Config never depends outward
R1 → R2, R3, R4, R5   ❌ Domain is pure
R2 → R3, R4, R5       ❌ Application doesn't know about interfaces or infrastructure
R3 → R4, R5           ❌ Interface doesn't depend on infrastructure or UI
R4 → R3, R5           ❌ Infrastructure doesn't depend on interfaces or UI
R5 → R1, R2, R4       ❌ Presentation only talks to interface
```

### Why These Rules?

**R3 cannot depend on R4:** Interface defines contracts, infrastructure implements them. Reversing this creates tight coupling.

**R4 cannot depend on R3:** Infrastructure is about "how", interface is about "what". Infrastructure shouldn't know about API shapes.

**R5 depends only on R3:** UI should only talk through defined interfaces, never reach into business logic or infrastructure.

---

## When to Add Each Layer

| Layer | Add When | Skip If |
|-------|----------|---------|
| R0 CONFIG | >5 config concerns | All config in .env |
| R1 DOMAIN | >10 business rules | Simple CRUD app |
| R2 APPLICATION | >3 workflows | Direct handlers work |
| R3 INTERFACE | Always | Never skip |
| R4 INFRASTRUCTURE | Always | Never skip |
| R5 PRESENTATION | >1 frontend | Single frontend in R3 |

---

## Project Evolution

### Tiny (MVP, Week 1)

**Active layers:** R3, R4

**Example:** Startup prototype

```
src/
  interface/         # R3 - API handlers
  infrastructure/    # R4 - Database, external APIs
```

**Validators:** Check 2-layer dependencies only

**When to evolve:** When business logic needs extraction

---

### Small (6 months)

**Active layers:** R1, R2, R3, R4

**Example:** Business rules emerge

```
src/
  domain/           # R1 - User, Order entities
  application/      # R2 - CreateOrder workflow
  interface/        # R3 - REST endpoints
  infrastructure/   # R4 - Postgres, Redis
```

**Validators:** Check 4-layer dependencies

**When to evolve:** When adding second frontend

---

### Growing (2 years)

**Active layers:** R1, R2, R3, R4, R5

**Example:** Multiple frontends (web + mobile)

```
src/
  domain/           # R1 - Business entities
  application/      # R2 - Workflows
  interface/        # R3 - REST + GraphQL
  infrastructure/   # R4 - Database, queues
  presentation/     # R5 - Web app, mobile app
```

**Validators:** Check 5-layer dependencies

**When to evolve:** When config becomes complex

---

### Enterprise (5+ years)

**Active layers:** R0, R1, R2, R3, R4, R5

**Example:** Multi-tenant, multi-region

```
src/
  config/           # R0 - Feature flags, regional settings
  domain/           # R1 - Complex business rules
  application/      # R2 - Sagas, compensation
  interface/        # R3 - Multiple API styles
  infrastructure/   # R4 - Multiple backends
  presentation/     # R5 - Multiple platforms
```

**Validators:** Check all 6 layers

---

## Benefits

### Swap Layers Independently

**Change database?** Only R4 affected
**Change UI framework?** Only R5 affected
**Add GraphQL?** Only R3 affected
**Change business rules?** Only R1 affected

Core logic never touched.

---

### Predictable Change Impact

Every change has a clear scope:

| Change Type | Affected Layers |
|-------------|-----------------|
| Business rule | R1 |
| Workflow | R2 |
| API contract | R3 |
| Database schema | R4 |
| UI redesign | R5 |
| Feature flag | R0 |

---

### Natural Testing Boundaries

Each layer has different testing needs:

- **R0:** Config validation tests
- **R1:** Pure unit tests (no mocks)
- **R2:** Workflow integration tests
- **R3:** API contract tests
- **R4:** Repository integration tests
- **R5:** UI component tests

---

### Clear AI Collaboration

When prompting AI:

```
"Add user verification"
```

AI knows:
- R1: User entity needs `verified` field
- R2: VerifyEmailWorkflow
- R3: POST /verify-email endpoint
- R4: EmailService integration
- R5: Verification UI component

Each layer generated in correct location.

---

## Common Patterns

### Pattern: Repository Pattern

**Interface defined in:** R1 (domain)  
**Implementation in:** R4 (infrastructure)

```python
# R1: domain/user_repository.py
class UserRepository(ABC):
    @abstractmethod
    def save(self, user: User): pass
    
    @abstractmethod
    def find_by_email(self, email: str): pass

# R4: infrastructure/postgres_user_repository.py
class PostgresUserRepository(UserRepository):
    def save(self, user: User):
        self.db.execute(...)
```

---

### Pattern: Dependency Inversion

**Problem:** R2 (application) needs to call R4 (infrastructure)

**Solution:** Define interface in R1, implement in R4, inject into R2

```python
# R1: domain/email_sender.py
class EmailSender(ABC):
    @abstractmethod
    def send(self, to: str, subject: str, body: str): pass

# R4: infrastructure/smtp_email_sender.py
class SMTPEmailSender(EmailSender):
    def send(self, to, subject, body):
        # SMTP implementation

# R2: application/user_registration.py
class UserRegistration:
    def __init__(self, email_sender: EmailSender):
        self.email_sender = email_sender
    
    def execute(self, user):
        user.register()
        self.email_sender.send(user.email, "Welcome", "...")
```

---

### Pattern: DTO Mapping

**Problem:** Domain entities shouldn't leak to API

**Solution:** Map in R3 (interface)

```python
# R1: domain/user.py
class User:
    def __init__(self, id, email, password_hash):
        self.id = id
        self.email = email
        self.password_hash = password_hash  # Internal

# R3: interface/user_dto.py
class UserDTO:
    def __init__(self, id, email):
        self.id = id
        self.email = email  # No password

    @staticmethod
    def from_domain(user: User):
        return UserDTO(user.id, user.email)
```

---

## Validation

### Automatic Validation

Git hooks validate every commit:

```bash
git commit -m "Domain: Add user verification [R1/C2]"
```

Pre-commit hook checks:
1. Dependency direction (D2)
2. Layer boundaries
3. No forbidden imports

Violations block the commit.

---

### Manual Validation

Run validators manually:

```bash
# Check dependency flow
python3 tools/validate-dependencies.py --root .

# Check all rules
bash tools/validate-all.sh
```

---

## Migration Guide

### From Flat Structure

**Before:**
```
src/
  models/
  services/
  controllers/
  utils/
```

**After (minimal R3-R4):**
```
src/
  interface/       # controllers
  infrastructure/  # models, services, utils
```

**After (standard R1-R4):**
```
src/
  domain/          # pure models
  application/     # services
  interface/       # controllers
  infrastructure/  # database, external APIs
```

---

### From MVC

**Before:**
```
src/
  models/
  views/
  controllers/
```

**After:**
```
src/
  domain/          # models (business logic only)
  application/     # controllers (business processes)
  interface/       # API layer
  infrastructure/  # data access
  presentation/    # views
```

---

## FAQs

**Q: Where do utilities go?**  
A: Depends on dependencies:
- Pure utilities (no dependencies): R1
- Application utilities: R2
- Infrastructure utilities: R4

**Q: Where does authentication go?**  
A: Split across layers:
- R1: User entity, permission rules
- R2: Authentication workflow
- R3: Auth middleware, JWT handling
- R4: Password hashing, token storage

**Q: Can I skip R2 (application)?**  
A: Yes, if:
- Simple CRUD operations
- Pure CQRS architecture
- Workflows fit in R3 handlers

**Q: When should I add R0 (config)?**  
A: When you have:
- Feature flags
- Multi-tenant configuration
- Complex deployment parameters
- Regional settings

**Q: What if a layer is empty?**  
A: That's fine. Validators detect active layers automatically.

**Q: Can I rename layers?**  
A: Validators use directory names. Keep standard names:
- `config/`, `domain/`, `application/`, `interface/`, `infrastructure/`, `presentation/`

---

## See Also

- [COMMIT_FORMAT.md](COMMIT_FORMAT.md) - How to format commits
- [specs/00-framework.md](specs/00-framework.md) - Formal framework specification
- [CONSTITUTION.md](CONSTITUTION.md) - Design philosophy
- [../examples/](../examples/) - Example projects
