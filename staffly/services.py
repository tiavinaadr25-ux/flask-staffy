from __future__ import annotations

import json
import re
from datetime import UTC, date, datetime
from urllib import error as urllib_error
from urllib import request as urllib_request

from flask import Flask
from typing_extensions import Any

from .extensions import bcrypt, db
from .models import Employee, LeaveRequest, Manager, Task
from .repositories import get_manager_by_email

try:
    from pymongo import MongoClient
    from pymongo.errors import PyMongoError
except ImportError:  # pragma: no cover - optional dependency in local dev
    MongoClient = None

    class PyMongoError(Exception):
        """Fallback error type used when pymongo is unavailable."""


def parse_optional_date(raw_value: str) -> date | None:
    """Convert an ISO date string into a date object when present."""
    if not raw_value.strip():
        return None
    return date.fromisoformat(raw_value)


def create_manager_account(
    full_name: str,
    restaurant_name: str,
    email: str,
    password: str,
) -> Manager:
    """Create a manager account and persist it."""
    manager = Manager(
        full_name=full_name,
        restaurant_name=restaurant_name,
        email=email,
    )
    manager.password_hash = bcrypt.generate_password_hash(password).decode("utf-8")
    db.session.add(manager)
    db.session.commit()
    return manager


def authenticate_manager(email: str, password: str) -> Manager | None:
    """Authenticate a manager by email and password."""
    manager = get_manager_by_email(email)
    if manager is None:
        return None
    if not bcrypt.check_password_hash(manager.password_hash, password):
        return None
    return manager


def seed_demo_records() -> bool:
    """Create demo data only once for product demonstrations."""
    if get_manager_by_email("manager@staffly.com") is not None:
        return False

    manager = Manager(
        full_name="Tia Manager",
        restaurant_name="Staffly Bistro",
        email="manager@staffly.com",
    )
    manager.password_hash = bcrypt.generate_password_hash("Staffly123!").decode("utf-8")
    db.session.add(manager)
    db.session.flush()

    employee_one = Employee(
        manager_id=manager.id,
        full_name="Aina Rakoto",
        role_title="Chef de rang",
        email="aina@staffly.com",
        phone="+33 6 11 22 33 44",
    )
    employee_two = Employee(
        manager_id=manager.id,
        full_name="Mickael Rabe",
        role_title="Commis de cuisine",
        email="mickael@staffly.com",
        phone="+33 6 55 44 33 22",
    )
    db.session.add_all([employee_one, employee_two])
    db.session.flush()

    task = Task(
        manager_id=manager.id,
        employee_id=employee_one.id,
        title="Prepare the lunch service checklist",
        description="Check tables, booking notes, and stock for lunch.",
        status="in_progress",
        due_date=date.today(),
    )
    leave_request = LeaveRequest(
        manager_id=manager.id,
        employee_id=employee_two.id,
        start_date=date.today(),
        end_date=date.today(),
        reason="Medical appointment",
        status="pending",
    )

    db.session.add_all([task, leave_request])
    db.session.commit()
    return True


def get_mongo_collection(app: Flask) -> Any | None:
    """Return the MongoDB collection used for AI suggestion history."""
    mongo_uri = app.config.get("MONGO_URI", "")

    if MongoClient is None or not isinstance(mongo_uri, str) or not mongo_uri:
        return None

    mongo_client = app.extensions.get("mongo_client")
    if mongo_client is None:
        mongo_client = MongoClient(mongo_uri, serverSelectionTimeoutMS=1000)
        app.extensions["mongo_client"] = mongo_client

    database_name = app.config.get("MONGO_DB_NAME", "staffly_ai")
    collection_name = app.config.get("MONGO_COLLECTION_NAME", "ai_suggestions")
    return mongo_client[database_name][collection_name]


def parse_suggestion_items(raw_text: str) -> list[str]:
    """Convert raw generated text into a clean list of suggestions."""
    normalized_lines = [line.strip(" -*0123456789.") for line in raw_text.splitlines()]
    suggestions = [line.strip() for line in normalized_lines if line.strip()]

    if suggestions:
        return suggestions[:5]

    sentence_candidates = [
        sentence.strip()
        for sentence in raw_text.replace("!", ".").split(".")
        if sentence.strip()
    ]
    return sentence_candidates[:5]


def normalize_matching_text(text: str) -> str:
    """Normalize a text so repeated phrases can be detected more reliably."""
    lowered_text = text.lower().strip()
    compact_text = re.sub(r"\s+", " ", lowered_text)
    return re.sub(r"[^\w\sàâçéèêëîïôöùûüÿœæ-]", "", compact_text)


def build_fallback_suggestions(prompt: str) -> list[str]:
    """Return action-oriented task suggestions when the AI API is unavailable."""
    normalized_prompt = normalize_matching_text(prompt)
    suggestions: list[str] = []

    def add_suggestion(item: str) -> None:
        if item not in suggestions:
            suggestions.append(item)

    if any(
        keyword in normalized_prompt
        for keyword in ("midi", "dejeuner", "déjeuner", "lunch")
    ):
        add_suggestion(
            "Lancer la mise en place et vérifier que chaque poste est"
            " prêt avant l'ouverture du midi."
        )

    if any(
        keyword in normalized_prompt for keyword in ("soir", "diner", "dîner", "dinner")
    ):
        add_suggestion(
            "Valider la mise en place du soir et confirmer la répartition"
            " entre la salle et la cuisine."
        )

    if "terrasse" in normalized_prompt:
        add_suggestion(
            "Préparer la terrasse et répartir les zones entre les membres de l'équipe."
        )

    if any(
        keyword in normalized_prompt
        for keyword in ("absence", "absences", "absent", "manque", "sous-effectif")
    ):
        add_suggestion(
            "Réorganiser les postes pour couvrir les absences sans ralentir le service."
        )

    if any(
        keyword in normalized_prompt
        for keyword in (
            "reservation",
            "reservations",
            "réservation",
            "réservations",
            "reservent",
            "réservent",
        )
    ):
        add_suggestion(
            "Faire un point sur les réservations et ajuster le plan de"
            " salle selon le flux attendu."
        )

    if any(
        keyword in normalized_prompt
        for keyword in ("stock", "rupture", "livraison", "produit")
    ):
        add_suggestion(
            "Contrôler les stocks critiques et signaler les manques"
            " avant le lancement du service."
        )

    add_suggestion(
        "Faire un briefing rapide avec l'équipe sur les priorités du" " service."
    )
    add_suggestion(
        "Vérifier la salle, le matériel et les postes de travail avant le coup de feu."
    )
    add_suggestion(
        "Suivre l'avancement des tâches critiques et réajuster la"
        " répartition si besoin."
    )

    return suggestions[:3]


def clean_generated_suggestions(
    suggestions: list[str],
    prompt: str,
    restaurant_name: str,
) -> list[str]:
    """Remove repetitive or low-value suggestions from generated content."""
    normalized_prompt = normalize_matching_text(prompt)
    normalized_restaurant = normalize_matching_text(restaurant_name)
    cleaned_suggestions: list[str] = []

    for suggestion in suggestions:
        clean_text = " ".join(suggestion.split()).strip(" -•")
        if not clean_text:
            continue

        normalized_suggestion = normalize_matching_text(clean_text)
        if normalized_prompt and normalized_prompt in normalized_suggestion:
            continue
        if normalized_restaurant and normalized_restaurant in normalized_suggestion:
            continue

        if clean_text[-1] not in ".!?":
            clean_text = f"{clean_text}."

        if clean_text not in cleaned_suggestions:
            cleaned_suggestions.append(clean_text)

    return cleaned_suggestions


def generate_ai_task_suggestions(
    app: Flask, manager: Manager, prompt: str
) -> tuple[list[str], str]:
    """Generate task suggestions with Hugging Face when configured."""
    token = app.config.get("HUGGING_FACE_API_TOKEN", "")
    model_url = app.config.get("HUGGING_FACE_MODEL_URL", "")
    fallback_suggestions = build_fallback_suggestions(prompt)

    if not isinstance(token, str) or not isinstance(model_url, str):
        return fallback_suggestions, "fallback"

    if not token or not model_url:
        return fallback_suggestions, "fallback"

    payload = {
        "inputs": (
            "Generate exactly 3 short and actionable task suggestions in"
            " French for a restaurant manager. "
            "Each suggestion must start with a verb. "
            "Do not repeat the manager request verbatim. "
            "Do not mention the restaurant name. "
            "Return only the task suggestions. "
            f"Manager request: {prompt}"
        ),
        "parameters": {
            "max_new_tokens": 120,
            "return_full_text": False,
        },
    }
    request_headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    api_request = urllib_request.Request(
        model_url,
        data=json.dumps(payload).encode("utf-8"),
        headers=request_headers,
        method="POST",
    )

    try:
        with urllib_request.urlopen(api_request, timeout=10) as response:
            response_payload = json.loads(response.read().decode("utf-8"))
    except (
        TimeoutError,
        urllib_error.URLError,
        urllib_error.HTTPError,
        json.JSONDecodeError,
    ):
        return fallback_suggestions, "fallback"

    if isinstance(response_payload, list) and response_payload:
        generated_text = str(response_payload[0].get("generated_text", "")).strip()
    elif isinstance(response_payload, dict):
        generated_text = str(response_payload.get("generated_text", "")).strip()
    else:
        generated_text = ""

    parsed_items = parse_suggestion_items(generated_text)
    cleaned_items = clean_generated_suggestions(
        parsed_items,
        prompt,
        manager.restaurant_name,
    )
    if cleaned_items:
        for fallback_suggestion in fallback_suggestions:
            if fallback_suggestion not in cleaned_items:
                cleaned_items.append(fallback_suggestion)
            if len(cleaned_items) == 3:
                break
        return cleaned_items[:3], "hugging_face"

    return fallback_suggestions, "fallback"


def save_ai_suggestion_history(
    app: Flask,
    manager: Manager,
    prompt: str,
    suggestions: list[str],
    source: str,
) -> bool:
    """Save AI suggestion history into MongoDB when available."""
    collection = get_mongo_collection(app)
    if collection is None:
        return False

    document = {
        "manager_email": manager.email,
        "manager_name": manager.full_name,
        "restaurant_name": manager.restaurant_name,
        "prompt": prompt,
        "suggestions": suggestions,
        "source": source,
        "created_at": datetime.now(UTC).isoformat(),
    }

    try:
        collection.insert_one(document)
    except PyMongoError:
        return False

    return True


def format_history_datetime(raw_value: Any) -> str:
    """Format a stored datetime value into a short French display string."""
    if isinstance(raw_value, datetime):
        parsed_datetime = raw_value.astimezone()
    else:
        raw_text = str(raw_value).strip()
        if not raw_text:
            return ""

        try:
            parsed_datetime = datetime.fromisoformat(raw_text.replace("Z", "+00:00"))
        except ValueError:
            return raw_text

    return parsed_datetime.astimezone().strftime("%d/%m/%Y à %H:%M")


def load_ai_suggestion_history(
    app: Flask,
    manager: Manager,
    limit: int = 5,
) -> list[dict[str, Any]]:
    """Load the latest AI suggestion history for the connected manager."""
    collection = get_mongo_collection(app)
    if collection is None:
        return []

    try:
        documents = (
            collection.find({"manager_email": manager.email})
            .sort(
                "created_at",
                -1,
            )
            .limit(limit)
        )
    except PyMongoError:
        return []

    history: list[dict[str, Any]] = []
    for document in documents:
        history.append(
            {
                "prompt": str(document.get("prompt", "")),
                "suggestions": list(document.get("suggestions", [])),
                "source": str(document.get("source", "fallback")),
                "created_at": format_history_datetime(document.get("created_at", "")),
            }
        )

    return history
