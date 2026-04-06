from sqlmodel import Field, SQLModel, Relationship
from typing import Optional
from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()


# =========================
# Section 3 — User Model (with relationships)
# =========================
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    email: str = Field(index=True, unique=True)
    password: str

    # Section 3.1 — Relationship field (User → many Todos)
    todos: list["Todo"] = Relationship(back_populates="user")

    def set_password(self, plaintext_password):
        self.password = password_hash.hash(plaintext_password)

    def __str__(self) -> str:
        return f"(User id={self.id}, username={self.username}, email={self.email})"


# =========================
# Section 5 — Bridge Table (Many-to-Many)
# =========================
class TodoCategory(SQLModel, table=True):
    todo_id: int | None = Field(primary_key=True, foreign_key="todo.id")
    category_id: int | None = Field(primary_key=True, foreign_key="category.id")


# =========================
# Section 2 — Todo Model
# =========================
class Todo(SQLModel, table=True):
    # Task 2.1 fields
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    text: str = Field(max_length=255)
    done: bool = Field(default=False)

    # Section 3.2 — Relationship (Todo → User)
    user: "User" = Relationship(back_populates="todos")

    # Section 5.2 — Many-to-Many relationship (Todo ↔ Category)
    categories: list["Category"] = Relationship(
        back_populates="todos",
        link_model=TodoCategory
    )

    # Section 3.4 — toggle function
    def toggle(self):
        self.done = not self.done


# =========================
# Section 5 — Category Model
# =========================
class Category(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    text: str = Field(max_length=255)

    # Many-to-Many relationship (Category ↔ Todo)
    todos: list["Todo"] = Relationship(
        back_populates="categories",
        link_model=TodoCategory
    )