#!/bin/bash
echo "🚀 Building Career Up Platform..."
python3.9 -m pip install -r requirements.txt
python3.9 manage.py migrate --noinput
python3.9 manage.py shell -c "import add_courses"
echo "✅ Build Complete!"
