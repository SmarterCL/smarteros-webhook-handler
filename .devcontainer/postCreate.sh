#!/bin/bash
set -e

echo "🚀 Setting up SmarterOS Webhook Handler environment..."

# Install UV (fast Python package manager)
echo "📦 Installing uv..."
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.cargo/bin:$PATH"

# Install pnpm
echo "📦 Installing pnpm..."
npm install -g pnpm

# Install Supabase CLI
echo "📦 Installing Supabase CLI..."
npm install -g supabase

# Install Python dependencies with uv
echo "🐍 Installing Python dependencies..."
uv pip install --system -e ".[dev]"

# Setup pre-commit hooks
echo "🪝 Setting up git hooks..."
if [ -f ".git/hooks/pre-commit" ]; then
    echo "Git hooks already configured"
else
    mkdir -p .git/hooks
    cat > .git/hooks/pre-commit << 'HOOK'
#!/bin/bash
pytest tests/ -v --tb=short
if [ $? -ne 0 ]; then
    echo "❌ Tests failed. Commit aborted."
    exit 1
fi
echo "✅ Tests passed."
HOOK
    chmod +x .git/hooks/pre-commit
fi

# Initialize database
echo "🗄️  Initializing database..."
python -c "from src.utils.storage import init_db; init_db()" || echo "⚠️  Will create on first run"

# Create .env if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env from example..."
    cp .env.example .env
fi

echo "✅ Setup complete!"
