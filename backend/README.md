# Eligify Backend

AI-powered Employability Operating System backend built with Python, FastAPI, and AWS serverless services.

## Architecture

- **Runtime**: Python 3.11+
- **Framework**: FastAPI on AWS Lambda
- **Database**: DynamoDB
- **Storage**: S3
- **Authentication**: Amazon Cognito + JWT
- **AI**: AWS Bedrock (Claude 3 Sonnet) with OpenAI fallback
- **Deployment**: Serverless Framework

## Project Structure

```
backend/
├── src/
│   ├── handlers/          # Lambda function handlers
│   ├── services/          # Business logic services
│   │   ├── ai_service.py           # AI abstraction layer
│   │   ├── eligibility_service.py  # Deterministic eligibility engine
│   │   ├── profile_service.py      # Profile management
│   │   ├── skill_service.py        # Skill graph operations
│   │   └── project_service.py      # Project management
│   ├── models/            # Pydantic models and types
│   ├── middleware/        # FastAPI middleware (auth, validation, error)
│   ├── config/            # Configuration and environment
│   └── utils/             # Helper functions (DynamoDB, S3, JWT)
├── serverless.yml         # Serverless Framework configuration
├── requirements.txt       # Python dependencies
└── pyproject.toml         # Python project configuration
```

## Setup

1. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Copy environment variables:
```bash
cp .env.example .env
```

4. Configure AWS credentials:
```bash
aws configure
```

5. Deploy infrastructure:
```bash
serverless deploy
```

## Development

Run locally with uvicorn:
```bash
uvicorn src.main:app --reload --port 8000
```

Or with serverless-offline:
```bash
serverless offline
```

## Testing

Run tests:
```bash
pytest
```

## Deployment

Deploy to AWS:
```bash
serverless deploy
```

## API Endpoints

### Authentication
- `POST /auth/signup` - Create new account
- `POST /auth/signin` - Login
- `POST /auth/refresh` - Refresh access token
- `POST /auth/signout` - Logout

### Profile
- `GET /profile` - Get current user profile
- `PUT /profile` - Update profile
- `POST /profile/upload-resume` - Upload resume

### Skills
- `GET /skills` - Get skill graph
- `POST /skills` - Add skill manually

### Internships
- `GET /internships` - List all internships
- `GET /internships/classify` - Get classified internships

### Projects
- `POST /projects/generate` - Generate AI project
- `GET /projects` - List user projects
- `GET /projects/:id` - Get project details
- `PUT /projects/:id/complete` - Mark project complete

## Environment Variables

See `.env.example` for required configuration.

## License

MIT
