# minimal-r3-r4: Minimal Living Architecture

**Active Layers:** R3 (INTERFACE), R4 (INFRASTRUCTURE)  
**Skipped:** R0 (CONFIG), R1 (DOMAIN), R2 (APPLICATION), R5 (PRESENTATION)  
**Timeline:** MVP, < 3 months  
**Team:** 1-2 people  
**Complexity:** Minimal

---

## Overview

The smallest possible Living Architecture system. Just two required layers:
- R3 (INTERFACE) - API boundaries
- R4 (INFRASTRUCTURE) - External systems

Business logic lives directly in R3 handlers. No separate domain layer.

---

## When to Use

✓ Weekend hackathons  
✓ MVPs and prototypes  
✓ Simple CRUD applications  
✓ Microservices with thin logic  
✓ Learning the system

---

## Structure

```
minimal-r3-r4/
├── interface/         # R3 - API handlers, HTTP layer
│   └── todo_handler.py
└── infrastructure/    # R4 - Database, external services
    └── todo_repository.py
```

No domain layer - business logic embedded in handlers.  
No application layer - workflows are simple enough.  
No presentation layer - single web app served by interface.  
No config layer - environment variables sufficient.

---

## Dependency Rules

Only 2 layers means simple rules:

✅ **Allowed:**
- R3 (interface) → R4 (infrastructure)

❌ **Forbidden:**
- R4 (infrastructure) → R3 (interface)

That's it!

---

## Example: Todo API

**interface/todo_handler.py** (R3):
```python
from infrastructure.todo_repository import TodoRepository

class TodoHandler:
    def __init__(self):
        self.repo = TodoRepository()
    
    def create_todo(self, request):
        # Business logic embedded here (simple enough)
        if not request.title or len(request.title) < 3:
            return {"error": "Title too short"}, 400
        
        todo = {
            'title': request.title,
            'done': False
        }
        saved = self.repo.save(todo)
        return {"id": saved['id'], "title": saved['title']}, 201
```

**infrastructure/todo_repository.py** (R4):
```python
import sqlite3

class TodoRepository:
    def __init__(self):
        self.db = sqlite3.connect('todos.db')
    
    def save(self, todo):
        cursor = self.db.cursor()
        cursor.execute(
            "INSERT INTO todos (title, done) VALUES (?, ?)",
            (todo['title'], todo['done'])
        )
        self.db.commit()
        todo['id'] = cursor.lastrowid
        return todo
```

---

## When to Expand

### Add R1 (DOMAIN) when:
- Business rules > 10
- Rules changing frequently
- Need to share rules across services
- Testing business logic separately becomes important

**Example:** Todo validation rules become complex (due dates, priorities, categories)

### Add R2 (APPLICATION) when:
- Workflows involve >3 steps
- Need state machines
- Orchestrating multiple domain objects
- Implementing sagas or compensation logic

**Example:** CreateTodo workflow needs to: validate, save, send notification, update statistics

### Add R5 (PRESENTATION) when:
- Second frontend appears (mobile app)
- Multiple UI frameworks (React + Vue)
- Need separate UI state management

---

## Benefits of Starting Minimal

✓ **Fast to build:** Just two directories  
✓ **Easy to understand:** Minimal moving parts  
✓ **Quick to validate:** Simple dependency rules  
✓ **Perfect for learning:** Understand core concepts first  
✓ **Grow when needed:** Add layers as complexity emerges

---

## Evolution Path

```
minimal-r3-r4 (Week 1)
     ↓
     Business rules extracted
     ↓
standard-r1-r4 (6 months)
     ↓
     Multiple frontends
     ↓
full-r0-r5 (2+ years)
```

---

## Validation

Validators automatically detect only 2 active layers:

```bash
python3 ../../tools/detect-active-layers.py --root .
# Output:
# {"config": false, "domain": false, "application": false, 
#  "interface": true, "infrastructure": true, "presentation": false}

python3 ../../tools/validate-dependencies.py --root .
# Output:
# ✅ No dependency violations found (checking R3 → R4 only)
```

---

## Common Mistakes

❌ **Don't create empty layer directories**  
If you don't need R1 (domain), don't create a `domain/` folder.

❌ **Don't over-engineer**  
Resist the urge to add layers "for future use". Add them when you actually need them.

❌ **Don't bypass validators**  
Even with 2 layers, dependency flow matters.

---

## Migration to Standard

When your minimal system grows:

```bash
# Add domain layer
mkdir domain
mv interface/validation_logic.py domain/todo.py

# Add application layer
mkdir application
mv interface/complex_workflow.py application/create_todo_workflow.py

# Update imports
# Update validators
python3 ../../tools/validate-dependencies.py --root .
```

---

See also:
- [standard-r1-r4](../standard-r1-r4/) - Next evolution step
- [../starter/](../starter/) - Working code example with R1-R4
