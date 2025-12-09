# 🪝 SmarterOS Webhook Handler

[![Tests](https://github.com/SmarterCL/smarteros-webhook-handler/actions/workflows/test.yml/badge.svg)](https://github.com/SmarterCL/smarteros-webhook-handler/actions/workflows/test.yml)
[![Build](https://github.com/SmarterCL/smarteros-webhook-handler/actions/workflows/build.yml/badge.svg)](https://github.com/SmarterCL/smarteros-webhook-handler/actions/workflows/build.yml)
[![Deploy](https://github.com/SmarterCL/smarteros-webhook-handler/actions/workflows/deploy.yml/badge.svg)](https://github.com/SmarterCL/smarteros-webhook-handler/actions/workflows/deploy.yml)
[![codecov](https://codecov.io/gh/SmarterCL/smarteros-webhook-handler/branch/main/graph/badge.svg)](https://codecov.io/gh/SmarterCL/smarteros-webhook-handler)

Production-ready webhook handler for GitHub Marketplace with signature verification, structured logging, and persistent storage.

## ✨ Features

- ✅ **Signature Verification** - HMAC-SHA256 validation for webhook security
- 📝 **Structured Logging** - JSON-formatted logs for easy parsing
- 💾 **Persistent Storage** - SQLite database for event tracking
- 🧪 **Full Test Coverage** - Unit and integration tests with pytest
- 🐳 **Docker Ready** - Containerized deployment
- 🔄 **GitHub Codespaces** - Pre-configured devcontainer
- 🚀 **CI/CD Pipeline** - Automated testing and deployment

## 🚀 Quick Start

### Using GitHub Codespaces

1. Click "Code" → "Create codespace on main"
2. Wait for the environment to set up (automatic via devcontainer)
3. Run: `make dev`
4. Open browser to forwarded port 8000

### Local Development

```bash
# Clone repository
git clone https://github.com/SmarterCL/smarteros-webhook-handler.git
cd smarteros-webhook-handler

# Install dependencies
curl -LsSf https://astral.sh/uv/install.sh | sh
uv pip install -e ".[dev]"

# Start development server
make dev

# Run tests
make test

# Check coverage
make coverage
```

## 📦 Usage

### Sending a Webhook

```bash
# Without signature
curl -X POST http://localhost:8000/webhooks/test \
  -H "Content-Type: application/json" \
  -H "X-GitHub-Delivery: test-123" \
  -d '{"action": "test", "data": "hello"}'

# With signature
SECRET="your-secret"
PAYLOAD='{"action":"test","data":"hello"}'
SIGNATURE="sha256=$(echo -n "$PAYLOAD" | openssl dgst -sha256 -hmac "$SECRET" | cut -d' ' -f2)"

curl -X POST http://localhost:8000/webhooks/test \
  -H "Content-Type: application/json" \
  -H "X-Hub-Signature-256: $SIGNATURE" \
  -H "X-GitHub-Delivery: test-456" \
  -d "$PAYLOAD"
```

### Response

```json
{
  "status": "received",
  "event_id": 1,
  "delivery_id": "test-123",
  "message": "Webhook processed successfully"
}
```

## 🧪 Testing

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# Run specific test
pytest tests/test_webhook.py::test_webhook_with_valid_signature -v
```

## 📊 Test Coverage

Current coverage: **~85%**

- ✅ Webhook endpoint handling
- ✅ Signature verification
- ✅ JSON parsing
- ✅ Database persistence
- ✅ Error handling

## 🏗️ Architecture

```
src/
├── main.py                 # FastAPI application
├── webhooks/
│   ├── test.py            # Webhook endpoint handler
│   └── verify.py          # Signature verification
└── utils/
    ├── logger.py          # Structured logging
    └── storage.py         # SQLite persistence
```

## 🔐 Security

### Signature Verification

Set your webhook secret:

```bash
export WEBHOOK_SECRET="your-github-webhook-secret"
```

The handler will automatically verify the `X-Hub-Signature-256` header using HMAC-SHA256.

### Best Practices

- ✅ Always use HTTPS in production
- ✅ Validate webhook signatures
- ✅ Rate limit webhook endpoints
- ✅ Monitor for suspicious activity
- ✅ Rotate secrets periodically

## 🐳 Docker Deployment

```bash
# Build image
docker build -t smarteros-webhook-handler .

# Run container
docker run -p 8000:8000 \
  -e WEBHOOK_SECRET=your-secret \
  smarteros-webhook-handler
```

## 📈 Monitoring

### Logs

Structured JSON logs for easy parsing:

```json
{
  "timestamp": "2025-12-09T22:00:00.000Z",
  "level": "INFO",
  "logger": "src.webhooks.test",
  "message": "Webhook received",
  "delivery_id": "abc123",
  "event_type": "test"
}
```

### Health Check

```bash
curl http://localhost:8000/health
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

All PRs must:
- ✅ Pass all tests
- ✅ Maintain >80% coverage
- ✅ Follow code style (black + ruff)
- ✅ Include documentation

## 📝 License

MIT License - see [LICENSE](LICENSE) for details

## 🔗 Links

- **Documentation**: [docs.smarterbot.store](https://docs.smarterbot.store)
- **Production API**: [api.smarterbot.store](https://api.smarterbot.store)
- **GitHub Marketplace**: [GitHub](https://github.com/marketplace)

---

**Built with ❤️ by [SmarterOS](https://smarterbot.store)**
