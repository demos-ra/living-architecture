# full-r0-r5: Enterprise Living Architecture

**Active Layers:** All 6 (R0, R1, R2, R3, R4, R5)  
**Timeline:** 3+ years  
**Team:** 10+ people  
**Complexity:** Very High

---

## Overview

Complete six-layer architecture for enterprise systems.

- R0 (CONFIG) - Feature flags, multi-tenant config
- R1 (DOMAIN) - Complex business rules
- R2 (APPLICATION) - Sagas, compensation logic
- R3 (INTERFACE) - Multiple API styles
- R4 (INFRASTRUCTURE) - Multiple backends
- R5 (PRESENTATION) - Multiple platforms

---

## When to Use

✓ Multi-tenant SaaS  
✓ Enterprise applications  
✓ Systems with >2 frontends  
✓ Complex configuration needs  
✓ Feature flagging required  
✓ Multiple deployment regions

---

## Structure

```
full-r0-r5/
├── config/            # R0 - Environment, feature flags
│   ├── settings.py
│   └── features.yaml
├── domain/            # R1 - Business rules (50+ rules)
│   ├── Order.py
│   ├── Payment.py
│   └── Inventory.py
├── application/       # R2 - Complex workflows (20+ workflows)
│   ├── PlaceOrder.py
│   ├── ProcessPayment.py
│   └── compensating/
│       └── RefundOrder.py
├── interface/         # R3 - Multiple API types
│   ├── rest/
│   ├── graphql/
│   └── events/
├── infrastructure/    # R4 - Multiple backends
│   ├── postgres/
│   ├── redis/
│   ├── kafka/
│   └── stripe_client/
└── presentation/      # R5 - Multiple UIs
    ├── web/
    ├── mobile/
    └── admin_dashboard/
```

---

## Dependency Rules

All six layers with strict separation:

```
R0 (root, no dependencies)
  ↓
R1 → R0
  ↓
R2 → R0, R1
  ↓
R3 → R0, R1, R2
  ↓
R4 → R0, R1, R2  (NOT R3)

R5 → R0, R3  (NOT R1, R2, R4)
```

---

## Full Request Flow Example

```
1. Mobile app (R5) sends request
2. REST API receives (R3/rest)
3. Calls PlaceOrderWorkflow (R2)
4. PlaceOrderWorkflow uses Order business rules (R1)
5. Checks feature flag from CONFIG (R0)
6. Creates order using OrderRepository (R4)
7. Publishes OrderPlaced event (R4/kafka)
8. Web app receives update (R5/web)
9. Admin dashboard sees order (R5/admin)
```

---

## Layer Examples

### R0: CONFIG

```python
# config/settings.py
class Settings:
    def __init__(self, tenant_id):
        self.tenant_id = tenant_id
    
    def feature_enabled(self, feature):
        return FeatureFlags.enabled(feature, self.tenant_id)
    
    @property
    def payment_provider(self):
        if self.tenant_id in ['enterprise_tenants']:
            return 'stripe_enterprise'
        return 'stripe_standard'
```

### R1: DOMAIN

```python
# domain/order.py
from config.settings import Settings

class Order:
    def __init__(self, user, items, config: Settings):
        self.user = user
        self.items = items
        self.config = config
    
    def can_use_express_checkout(self):
        # Business rule using config
        return (
            self.config.feature_enabled('express_checkout') and
            self.user.is_premium and
            self.total < 1000
        )
```

### R2: APPLICATION

```python
# application/place_order.py
from domain.order import Order

class PlaceOrderWorkflow:
    def __init__(self, config, order_repo, payment, notifications):
        self.config = config
        self.order_repo = order_repo
        self.payment = payment
        self.notifications = notifications
    
    def execute(self, user, items):
        # Complex orchestration
        order = Order(user, items, self.config)
        
        if order.can_use_express_checkout():
            return self._express_flow(order)
        else:
            return self._standard_flow(order)
    
    def _express_flow(self, order):
        # Save, charge, notify in one transaction
        saved = self.order_repo.save(order)
        self.payment.charge_immediate(order.user, order.total)
        self.notifications.send_confirmation(order.user)
        return saved
    
    def _standard_flow(self, order):
        # Standard multi-step workflow
        saved = self.order_repo.save_pending(order)
        self.payment.authorize(order.user, order.total)
        return saved
```

### R3: INTERFACE

```python
# interface/rest/order_routes.py
from application.place_order import PlaceOrderWorkflow

class OrderRoutes:
    def __init__(self, workflow):
        self.workflow = workflow
    
    def post_order(self, request):
        user = request.current_user
        items = self._parse_items(request.json)
        order = self.workflow.execute(user, items)
        return self._format_response(order), 201

# interface/graphql/order_resolvers.py
class OrderResolver:
    def __init__(self, workflow):
        self.workflow = workflow
    
    def create_order(self, root, info, items):
        user = info.context.user
        return self.workflow.execute(user, items)
```

### R4: INFRASTRUCTURE

```python
# infrastructure/postgres/order_repository.py
class PostgresOrderRepository:
    def save(self, order):
        return self.db.execute(...)

# infrastructure/kafka/order_events.py
class OrderEventPublisher:
    def publish_order_created(self, order):
        self.kafka.send('order.created', order.to_dict())
```

### R5: PRESENTATION

```jsx
// presentation/web/OrderForm.jsx
import { createOrderAPI } from 'interface/api_client';

function OrderForm() {
    const handleSubmit = async (items) => {
        const order = await createOrderAPI(items);
        navigate(`/orders/${order.id}`);
    };
    return <form onSubmit={handleSubmit}>...</form>;
}

// presentation/mobile/OrderScreen.tsx
import { createOrderAPI } from 'interface/api_client';

function OrderScreen() {
    // Same API, different UI
}
```

---

## Why All 6 Layers Matter

### R0 (CONFIG)
- Feature flags for gradual rollouts
- Multi-tenant configuration
- Regional settings (EU vs US)
- A/B testing parameters

### R1 (DOMAIN)
- Business rules don't leak into workflows
- Rules are testable independently
- Domain events for event sourcing

### R2 (APPLICATION)
- Sagas for distributed transactions
- Compensating transactions for failures
- Complex state machines

### R3 (INTERFACE)
- REST for web clients
- GraphQL for mobile apps
- Event streams for real-time updates
- Multiple API versions

### R4 (INFRASTRUCTURE)
- PostgreSQL for transactions
- Redis for caching
- Kafka for events
- Stripe for payments
- SendGrid for emails

### R5 (PRESENTATION)
- Web app (React)
- Mobile app (React Native)
- Admin dashboard (Vue)
- All share same APIs from R3

---

## Benefits at Scale

✓ **Clear ownership:** Each team owns specific layers  
✓ **Parallel development:** Teams don't block each other  
✓ **Technology isolation:** Change Redis without touching domain  
✓ **Multiple frontends:** Add new UIs without backend changes  
✓ **Feature flags:** Deploy code, enable features gradually  
✓ **Multi-tenant:** Tenant-specific config without code changes

---

## Validation

All 6-layer dependencies enforced:

```bash
python3 ../../tools/detect-active-layers.py --root .
# Output:
# {"config": true, "domain": true, "application": true, 
#  "interface": true, "infrastructure": true, "presentation": true}

python3 ../../tools/validate-dependencies.py --root .
# Output:
# ✅ No dependency violations found (checking all 6-layer dependencies)
```

---

## Evolution from Standard

```bash
# Add config layer
mkdir config
mv hardcoded_settings.py config/settings.py

# Add presentation layer
mkdir presentation
mv interface/react_components/ presentation/web/

# Update validators
python3 ../../tools/validate-dependencies.py --root .
```

---

## Anti-Patterns to Avoid

❌ **R5 importing from R1:** UI should never reach into domain  
❌ **R3 depending on R4:** Interface shouldn't know about infrastructure  
❌ **R0 importing from anywhere:** Config is root, imports nothing  
❌ **Creating all 6 layers on day 1:** Start minimal, add when needed

---

At enterprise scale, strict boundaries prevent chaos.

See also:
- [standard-r1-r4](../standard-r1-r4/) - Simpler alternative
- [../starter/](../starter/) - Working code example with R1-R4
