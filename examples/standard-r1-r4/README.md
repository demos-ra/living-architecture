# standard-r1-r4: Standard Living Architecture

**Active Layers:** R1, R2, R3, R4  
**Timeline:** 6 months - 2 years  
**Team:** 2-5 people  
**Complexity:** Medium

---

## Overview

Standard four-layer architecture. Business rules extracted to DOMAIN, workflows to APPLICATION.

- R1 (DOMAIN) - Business entities and rules
- R2 (APPLICATION) - Workflows and use cases
- R3 (INTERFACE) - API boundaries
- R4 (INFRASTRUCTURE) - External systems

---

## When to Use

✓ Standard web applications  
✓ SaaS products  
✓ E-commerce platforms  
✓ Business software  
✓ Most production systems

---

## Structure

```
standard-r1-r4/
├── domain/            # R1 - Business rules (10-50 rules)
│   ├── User.py
│   ├── Order.py
│   └── Payment.py
├── application/       # R2 - Workflows (5-20 workflows)
│   ├── CreateOrder.py
│   ├── ProcessPayment.py
│   └── CancelOrder.py
├── interface/         # R3 - API contracts
│   ├── rest/
│   └── graphql/
└── infrastructure/    # R4 - Persistence, integrations
    ├── database/
    └── stripe_client/
```

---

## Dependency Rules

Four layers with clean separation:

```
R4 → R2 → R1
     ↓
     R3
```

✅ **Allowed:**
- R1 → nothing
- R2 → R1
- R3 → R1, R2
- R4 → R1, R2

❌ **Forbidden:**
- R1 → R2, R3, R4 (domain is pure)
- R2 → R3, R4 (application doesn't know about interfaces or infrastructure)
- R3 → R4 (interface doesn't depend on infrastructure)
- R4 → R3 (infrastructure doesn't depend on interfaces)

---

## Example: Order System

**domain/order.py** (R1):
```python
class Order:
    def __init__(self, user, items):
        self.user = user
        self.items = items
        self.total = sum(item.price for item in items)
    
    def can_be_placed(self):
        # Pure business rule
        return (
            len(self.items) > 0 and
            self.user.has_sufficient_credit(self.total)
        )
    
    def validate(self):
        if not self.can_be_placed():
            raise InvalidOrderError()
```

**application/create_order.py** (R2):
```python
from domain.order import Order

class CreateOrderWorkflow:
    def __init__(self, order_repo, payment_service):
        self.order_repo = order_repo
        self.payment_service = payment_service
    
    def execute(self, user, items):
        # Orchestrate the workflow
        order = Order(user, items)
        order.validate()
        
        # Save order
        saved_order = self.order_repo.save(order)
        
        # Process payment
        self.payment_service.charge(user, order.total)
        
        return saved_order
```

**interface/order_routes.py** (R3):
```python
from application.create_order import CreateOrderWorkflow

class OrderRoutes:
    def __init__(self, workflow):
        self.workflow = workflow
    
    def post_order(self, request):
        # HTTP layer
        user = request.current_user
        items = [Item.from_dict(i) for i in request.json['items']]
        
        order = self.workflow.execute(user, items)
        
        return {"order_id": order.id}, 201
```

**infrastructure/order_repository.py** (R4):
```python
from domain.order import Order

class OrderRepository:
    def __init__(self, db):
        self.db = db
    
    def save(self, order: Order):
        # Database persistence
        return self.db.insert('orders', {
            'user_id': order.user.id,
            'total': order.total,
            'items': json.dumps(order.items)
        })
```

---

## Benefits Over Minimal

✓ **Business rules isolated:** Easy to test, easy to change  
✓ **Workflows explicit:** Clear what happens when  
✓ **Easy to swap infrastructure:** Change database without touching business logic  
✓ **Multiple interfaces:** Can add GraphQL, CLI, etc. using same workflows  
✓ **Better testing:** Unit test domain, integration test workflows

---

## When to Expand

### Add R0 (CONFIG) when:
- Feature flagging needed
- Multi-tenant configuration
- Complex deployment topology
- Regional settings

### Add R5 (PRESENTATION) when:
- Second frontend (mobile app)
- Multiple UI frameworks
- Separate UI state management

---

## Common Patterns

### Repository Pattern
**Interface in R1, implementation in R4:**

```python
# R1: domain/order_repository_interface.py
class OrderRepository(ABC):
    @abstractmethod
    def save(self, order: Order): pass

# R4: infrastructure/postgres_order_repository.py
class PostgresOrderRepository(OrderRepository):
    def save(self, order: Order):
        # Postgres implementation
```

### Dependency Injection
**R2 receives dependencies, not concrete implementations:**

```python
# R2: application/create_order.py
class CreateOrderWorkflow:
    def __init__(
        self, 
        order_repo: OrderRepository,  # Interface from R1
        payment: PaymentService        # Interface from R1
    ):
        self.order_repo = order_repo
        self.payment = payment
```

---

## Migration Paths

### From minimal-r3-r4:

```bash
# Create domain layer
mkdir domain
mv interface/business_rules.py domain/

# Create application layer
mkdir application
mv interface/workflows.py application/

# Update imports and test
python3 ../../tools/validate-dependencies.py --root .
```

### To full-r0-r5:

Add CONFIG and PRESENTATION when needed.

---

See also:
- [minimal-r3-r4](../minimal-r3-r4/) - Simpler starting point
- [full-r0-r5](../full-r0-r5/) - Enterprise evolution
- [../starter/](../starter/) - Working code example
