import os
import logging
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import HTTPException

# 1. Structured Telemetry Configuration
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# 2. Resilient Environment Isolation (Render Persistent Storage vs. Local Testing)
if os.environ.get('RENDER'):
    db_path = '/var/data/tasks.db'
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
else:
    db_path = 'tasks.db'

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# 3. Data Model Boundary
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False, nullable=False)

    def to_dict(self):
        return {"id": self.id, "title": self.title, "completed": self.completed}

# Defensive Initialization
with app.app_context():
    try:
        db.create_all()
        logger.info("Database storage layers synchronized successfully.")
    except Exception as e:
        logger.critical(f"Critical Database Initialization Failure: {str(e)}")

# --- GLOBAL SYSTEM ERROR CATCHMENTS ---

@app.errorhandler(HTTPException)
def handle_http_exception(e):
    """Intercept standard HTTP failures cleanly based on request routing context."""
    logger.warning(f"HTTP Boundary Trap: {e.code} - {e.description} on route {request.path}")
    if request.path.startswith('/api/'):
        return jsonify({"error": e.description}), e.code
    return render_template('index.html', tasks=[], initial_error=e.description), e.code

@app.errorhandler(SQLAlchemyError)
def handle_database_error(e):
    """Intercept database locking or transaction corruption without revealing schema structures."""
    logger.error(f"SQLAlchemy Operational Exception: {str(e)} during {request.method} {request.path}")
    db.session.rollback()  # Safeguards database integrity state
    return jsonify({"error": "Data tier processing error. Please try again or verify system constraints."}), 500

@app.errorhandler(Exception)
def handle_unhandled_exception(e):
    """Catch-all root boundary to prevent unhandled panics or stack traces leaking to client."""
    logger.critical(f"Unhandled Kernel Level Panic: {str(e)}", exc_info=True)
    return jsonify({"error": "An internal framework error occurred."}), 500


# --- REST CORE API INTERFACES ---

@app.route('/')
def index():
    try:
        tasks = Task.query.all()
        return render_template('index.html', tasks=tasks)
    except Exception as e:
        logger.error(f"Render Template Injection Interrupted: {str(e)}")
        return render_template('index.html', tasks=[], initial_error="Data pipeline currently offline.")

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([t.to_dict() for t in tasks])

@app.route('/api/tasks', methods=['POST'])
def add_task():
    if not request.is_json:
        return jsonify({"error": "Payload validation failed. Content-Type must be application/json."}), 415
        
    data = request.get_json() or {}
    title = data.get('title', '').strip()
    
    # Assertive Defenses (Completeness List Boundary)
    if not title:
        return jsonify({"error": "Task schema requirement violation: Title cannot be empty."}), 400
    if len(title) > 200:
        return jsonify({"error": "Task schema requirement violation: Title exceeds maximum length of 200 characters."}), 400
    
    new_task = Task(title=title)
    db.session.add(new_task)
    db.session.commit()
    logger.info(f"Task Transaction Complete: ID {new_task.id} appended.")
    return jsonify(new_task.to_dict()), 201

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({"error": f"Resource not found: Task ID {task_id} does not exist."}), 404
        
    data = request.get_json() or {}
    if 'completed' in data:
        task.completed = bool(data['completed'])
    if 'title' in data:
        title = data['title'].strip()
        if not title:
            return jsonify({"error": "Updates cannot mutate schema state to an empty string."}), 400
        task.title = title
        
    db.session.commit()
    return jsonify(task.to_dict())

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({"error": f"Resource not found: Task ID {task_id} already purge state or nonexistent."}), 404
        
    db.session.delete(task)
    db.session.commit()
    logger.info(f"Task Transaction Complete: ID {task_id} purged.")
    return jsonify({"success": True})

# --- OPERATIONAL TELEMETRY ---
@app.route('/health', methods=['GET'])
def health():
    """Automated operational diagnostic probe for Render engine orchestration."""
    try:
        db.session.execute(db.select(1))
        return jsonify({"status": "healthy", "storage_tier": "connected"}), 200
    except Exception as e:
        logger.critical(f"System Node Probing Failure: {str(e)}")
        return jsonify({"status": "unhealthy", "reason": "Data processing engine connection dropped."}), 500

if __name__ == '__main__':
    app.run(debug=True)
