#cd /opt/llm-agent
source venv/bin/activate

celery -A agents.tasks worker -Q stl --concurrency=10
