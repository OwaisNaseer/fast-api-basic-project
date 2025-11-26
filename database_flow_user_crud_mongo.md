## Database Flow (MongoDB) – User CRUD Example

### 1. Environment and Connection

We use **MongoDB** as our database.  
The connection string is stored in `.env`:

```env
MONGODB_URL=mongodb://localhost:27017
```

In code, we load this URL and connect:

```python
# db.py
from motor.motor_asyncio import AsyncIOMotorClient
import os

MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
MONGODB_DB_NAME = "my_app_db"

client = AsyncIOMotorClient(MONGODB_URL)
db = client[MONGODB_DB_NAME]  # this is our database object

users_collection = db["users"]  # this is like a "table" for users
```

- **Database**: `my_app_db`
- **Collection**: `users` (similar to a table)
- **Document**: one user (similar to a row)

---

### 2. User Document Structure

A **document** in MongoDB is a JSON-like object.

Example user document:

```json
{
  "_id": "ObjectId(...)",
  "email": "john@example.com",
  "full_name": "John Doe",
  "hashed_password": "....",
  "created_at": "2025-11-26T12:00:00Z"
}
```

In our code, we usually define **schemas** for input and output:

```python
# schemas.py
from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None

class UserRead(BaseModel):
    id: str
    email: EmailStr
    full_name: Optional[str] = None
```

---

### 3. Create User (INSERT a Document)

**HTTP**: `POST /users`  
**DB**: `insert_one` into `users` collection.

```python
# crud_user.py
from bson import ObjectId
from datetime import datetime
from .db import users_collection
from .schemas import UserCreate

async def create_user(user_in: UserCreate) -> dict:
    # 1. Prepare the document
    doc = {
        "email": user_in.email,
        "full_name": user_in.full_name,
        "hashed_password": hash_password(user_in.password),  # your hash function
        "created_at": datetime.utcnow(),
    }

    # 2. Insert into MongoDB
    result = await users_collection.insert_one(doc)

    # 3. Return created user with string id
    doc["_id"] = str(result.inserted_id)
    return {
        "id": doc["_id"],
        "email": doc["email"],
        "full_name": doc["full_name"],
    }
```

FastAPI endpoint:

```python
# routers/users.py
from fastapi import APIRouter
from .schemas import UserCreate, UserRead
from .crud_user import create_user

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserRead)
async def create_user_endpoint(user_in: UserCreate):
    return await create_user(user_in)
```

**Flow**:

1. Client sends JSON to `POST /users`.
2. FastAPI parses it into `UserCreate`.
3. `create_user()` builds a document and uses `insert_one`.
4. MongoDB stores the document; we return the created user.

---

### 4. Read Users (SELECT Documents)

#### 4.1 Get All Users

**HTTP**: `GET /users`  
**DB**: `find({})` on `users` collection.

```python
# crud_user.py
async def get_users(limit: int = 10, skip: int = 0) -> list[dict]:
    cursor = users_collection.find({}).skip(skip).limit(limit)
    users = []
    async for doc in cursor:
        users.append({
            "id": str(doc["_id"]),
            "email": doc["email"],
            "full_name": doc.get("full_name"),
        })
    return users
```

#### 4.2 Get One User by ID

**HTTP**: `GET /users/{user_id}`  
**DB**: `find_one({"_id": ObjectId(user_id)})`.

```python
from fastapi import HTTPException

async def get_user_by_id(user_id: str) -> dict:
    doc = await users_collection.find_one({"_id": ObjectId(user_id)})
    if not doc:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "id": str(doc["_id"]),
        "email": doc["email"],
        "full_name": doc.get("full_name"),
    }
```

---

### 5. Update User (UPDATE a Document)

**HTTP**: `PUT /users/{user_id}`  
**DB**: `update_one` with `$set`.

```python
# schemas.py
class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    password: Optional[str] = None
```

```python
# crud_user.py
async def update_user(user_id: str, user_in: UserUpdate) -> dict:
    update_data = {}

    if user_in.full_name is not None:
        update_data["full_name"] = user_in.full_name

    if user_in.password is not None:
        update_data["hashed_password"] = hash_password(user_in.password)

    if not update_data:
        # nothing to update
        return await get_user_by_id(user_id)

    result = await users_collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": update_data}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="User not found")

    return await get_user_by_id(user_id)
```

**Key idea**:  
We use `{"$set": update_data}` to only change specific fields.

---

### 6. Delete User (DELETE a Document)

**HTTP**: `DELETE /users/{user_id}`  
**DB**: `delete_one({"_id": ObjectId(user_id)})`.

```python
# crud_user.py
async def delete_user(user_id: str) -> None:
    result = await users_collection.delete_one({"_id": ObjectId(user_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
```

---

### 7. Conditions and Queries in MongoDB

**Examples**:

- Find by email:

  ```python
  await users_collection.find_one({"email": "john@example.com"})
  ```

- Users created after a date:

  ```python
  await users_collection.find({"created_at": {"$gt": some_date}})
  ```

- Combine conditions (`AND`):

  ```python
  await users_collection.find({
      "email": {"$regex": "@gmail.com$"},
      "created_at": {"$gt": some_date}
  })
  ```

**Concept to remember**:  
MongoDB uses JSON-like query objects instead of SQL `WHERE`.

---

### 8. Student Tasks

1. Trace the flow for each endpoint:
   - Endpoint → CRUD function → MongoDB operation.
2. Match MongoDB operations to SQL ideas:
   - `insert_one` → `INSERT`
   - `find` / `find_one` → `SELECT`
   - `update_one` (`$set`) → `UPDATE`
   - `delete_one` → `DELETE`
3. Implement the same pattern for another entity:
   - Example: `Product` collection with CRUD endpoints.


