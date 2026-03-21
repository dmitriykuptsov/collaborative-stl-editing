#cd /opt/llm-agent
source venv/bin/activate

celery -A agents.worker.celery worker -Q stl --concurrency=10
