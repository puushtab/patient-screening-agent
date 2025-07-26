# CuraMe - AI-Powered Patient Screening System

CuraMe is an intelligent patient screening system that leverages multiple Model Context Protocol (MCP) servers to provide comprehensive healthcare data analysis and screening capabilities.

## 🏥 Overview

CuraMe integrates with multiple specialized MCP servers to create a powerful patient screening workflow:

- **📊 MongoDB MCP Server** - Patient data storage and retrieval
- **🧠 NLX MCP Server** - Natural language processing for medical text analysis
- **⏱️ Temporal** - Workflow orchestration and scheduling
- **🔒 Wiz** - Security and compliance scanning
- **☁️ AWS** - Cloud infrastructure and MongoDB hosting

## 🎯 Key Features

- **Intelligent Patient Screening** - AI-powered analysis of patient data
- **Multi-Modal Data Processing** - Text, structured data, and medical records
- **Workflow Orchestration** - Automated screening pipelines with Temporal
- **Secure Data Handling** - Enterprise-grade security with Wiz integration
- **Scalable Architecture** - AWS-hosted MongoDB for high availability
- **Real-time Analysis** - Instant patient risk assessment and recommendations

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Cursor IDE    │    │   CuraMe App    │    │  AWS MongoDB    │
│   (Frontend)    │◄──►│   (Core Logic)  │◄──►│   (Database)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         ▲                       ▲                       ▲
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  MCP Servers    │    │    Temporal     │    │      Wiz        │
│  - MongoDB MCP  │    │  (Workflows)    │    │  (Security)     │
│  - NLX MCP      │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+** - `python3 --version`
- **Node.js 16+** - For Temporal (optional)
- **MongoDB Atlas Account** - [Sign up free](https://www.mongodb.com/atlas)
- **AWS Account** - For advanced MongoDB hosting
- **Cursor IDE** - [Download here](https://cursor.sh/)

### 1. Clone and Setup

```bash
git clone <repository-url>
cd CuraMe
python3 quickstart.py
```

### 2. Configure Environment

Edit `.env` with your credentials:
```bash
# MongoDB Atlas
MONGODB_CONNECTION_STRING=mongodb+srv://user:pass@cluster.mongodb.net/curame?retryWrites=true&w=majority
MONGODB_DATABASE_NAME=curame

# NLX Configuration
NLX_API_KEY=your_nlx_api_key
NLX_ENDPOINT=https://api.nlx.com/v1

# AWS Configuration (Optional)
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_REGION=us-east-1

# Temporal Configuration (Optional)
TEMPORAL_HOST=localhost:7233
TEMPORAL_NAMESPACE=curame

# Wiz Configuration (Optional)
WIZ_API_KEY=your_wiz_api_key
WIZ_ENDPOINT=https://api.wiz.io
```

### 3. Start All Services

```bash
# Start MongoDB MCP Server
python3 mongo_mcp_server.py &

# Start NLX MCP Server (if available)
python3 nlx_mcp_server.py &

# Start Temporal (optional)
temporal server start-dev &

# Start main application
python3 curame_app.py
```

## 🔧 MCP Servers Setup

### MongoDB MCP Server Setup

#### Step 1: MongoDB Atlas Configuration

1. **Create Atlas Account**
   - Visit [MongoDB Atlas](https://www.mongodb.com/atlas)
   - Sign up for free account
   - Create new project: "CuraMe"

2. **Create Cluster**
   - Choose **M0 Sandbox** (Free tier)
   - Select region closest to you
   - Name: "curame-cluster"
   - Wait 3-5 minutes for deployment

3. **Database User Setup**
   - Go to **Database Access**
   - Click **"Add New Database User"**
   - Username: `curame_user`
   - Generate secure password
   - Role: **"Read and write to any database"**

4. **Network Access**
   - Go to **Network Access**
   - Click **"Add IP Address"**
   - For development: **"Allow Access from Anywhere"** (0.0.0.0/0)
   - For production: Add specific IP addresses

5. **Get Connection String**
   - Go to **Database** → Your cluster
   - Click **"Connect"** → **"Connect your application"**
   - Copy connection string
   - Replace `<password>` with your user password

#### Step 2: AWS MongoDB Hosting (Advanced)

For production deployments with AWS:

1. **Setup AWS DocumentDB**
   ```bash
   aws docdb create-db-cluster \
     --db-cluster-identifier curame-cluster \
     --engine docdb \
     --master-username curame_admin \
     --master-user-password <secure-password>
   ```

2. **Configure VPC and Security Groups**
   ```bash
   # Create security group
   aws ec2 create-security-group \
     --group-name curame-docdb-sg \
     --description "CuraMe DocumentDB Security Group"
   
   # Allow MongoDB port
   aws ec2 authorize-security-group-ingress \
     --group-name curame-docdb-sg \
     --protocol tcp \
     --port 27017 \
     --cidr 0.0.0.0/0
   ```

3. **Update Connection String**
   ```bash
   MONGODB_CONNECTION_STRING=mongodb://curame_admin:password@curame-cluster.cluster-xyz.us-east-1.docdb.amazonaws.com:27017/curame?ssl=true&replicaSet=rs0&readPreference=secondaryPreferred&retryWrites=false
   ```

#### Step 3: Test MongoDB Connection

```bash
python3 test_atlas_connection.py
```

Expected output:
```
🔌 Testing MongoDB Atlas Connection...
✅ Successfully connected to MongoDB Atlas!
📊 Server Version: 6.0.8
📂 Database 'curame' accessible
📋 Collections found: 3
   Collections: patients, screenings, reports
✅ Write test successful
🧹 Test document cleaned up
```

### NLX MCP Server Setup

#### Step 1: NLX Account Setup

1. **Create NLX Account**
   - Visit [NLX Platform](https://nlx.com)
   - Sign up for developer account
   - Create new workspace: "CuraMe"

2. **Get API Credentials**
   - Go to **API Keys** section
   - Generate new API key
   - Copy key and endpoint URL

3. **Configure Models**
   - Enable medical text analysis models
   - Configure healthcare-specific NLP pipelines
   - Set up entity extraction for medical terms

#### Step 2: Test NLX Integration

```bash
python3 test_nlx_connection.py
```

### Temporal Setup (Workflow Orchestration)

#### Step 1: Install Temporal

```bash
# Install Temporal CLI
curl -sSf https://temporal.download/cli.sh | sh

# Start development server
temporal server start-dev
```

#### Step 2: Configure Workflows

```bash
# Create workflow namespace
temporal namespace create curame

# Deploy workflows
python3 temporal_workflows.py
```

### Wiz Security Setup

#### Step 1: Wiz Integration

1. **Setup Wiz Account**
   - Contact Wiz for healthcare compliance setup
   - Configure HIPAA compliance scanning
   - Set up data classification rules

2. **Configure Security Policies**
   ```bash
   # Install Wiz CLI
   pip install wiz-cli
   
   # Configure policies
   wiz configure --api-key YOUR_WIZ_API_KEY
   ```

## 💻 Using CuraMe in Cursor IDE

### Setup Cursor for CuraMe

1. **Install Cursor**
   - Download from [cursor.sh](https://cursor.sh/)
   - Install and open the CuraMe project

2. **Configure MCP in Cursor**
   
   Edit your Cursor settings (`~/.cursor/mcp.json`):
   ```json
   {
     "mcp": {
       "servers": {
         "mongodb": {
           "command": "python3",
           "args": ["mongo_mcp_server.py"],
           "cwd": "/path/to/curame"
         },
         "nlx": {
           "command": "python3",
           "args": ["nlx_mcp_server.py"],
           "cwd": "/path/to/curame"
         }
       }
     }
   }
   ```

3. **Restart Cursor** to load MCP servers

### Example Prompts and Workflows

#### 🏥 Patient Data Analysis

**Prompt:**
```
Analyze the patient data for John Doe (ID: P12345). Check his recent vitals, medical history, and run a cardiovascular risk assessment. Use the MongoDB MCP server to fetch his records and NLX to analyze any clinical notes.
```

**Expected Workflow:**
1. Cursor connects to MongoDB MCP server
2. Fetches patient P12345 data
3. Extracts clinical notes and vitals
4. Uses NLX MCP to analyze medical text
5. Generates risk assessment report

#### 🔍 Batch Patient Screening

**Prompt:**
```
Screen all patients admitted in the last 24 hours for diabetes risk factors. For each patient:
1. Get their demographics and vitals from MongoDB
2. Analyze their admission notes using NLX
3. Calculate diabetes risk score
4. Generate screening report
5. Flag high-risk patients for immediate review
```

**Expected Workflow:**
1. Query MongoDB for recent admissions
2. Iterate through patient list
3. Extract and analyze medical data
4. Apply ML models for risk scoring
5. Generate batch screening report

#### 📊 Clinical Data Mining

**Prompt:**
```
Find patterns in patient outcomes for hypertension treatments over the last 6 months. Use MongoDB to query treatment data and NLX to analyze physician notes for treatment effectiveness mentions.
```

**Expected Workflow:**
1. Complex MongoDB aggregation queries
2. Text analysis of clinical notes
3. Statistical analysis of outcomes
4. Pattern recognition and reporting

#### 🚨 Real-time Alert System

**Prompt:**
```
Set up a real-time monitoring system that:
1. Watches for new patient vitals in MongoDB
2. Analyzes critical values using business rules
3. Uses NLX to check if physician notes mention concerns
4. Triggers alerts for immediate intervention needed
```

**Expected Workflow:**
1. MongoDB change streams monitoring
2. Real-time data processing
3. Rule-based alert generation
4. Integration with notification systems

### Advanced Cursor Integrations

#### Custom MCP Commands

You can create custom commands in Cursor:

```javascript
// .cursor/commands.json
{
  "commands": [
    {
      "name": "Screen Patient",
      "description": "Run comprehensive patient screening",
      "prompt": "Screen patient {{patientId}} using all available data sources and generate a comprehensive risk assessment report"
    },
    {
      "name": "Analyze Cohort",
      "description": "Analyze patient cohort",
      "prompt": "Analyze the patient cohort with condition {{condition}} over the last {{timeframe}} and identify trends, outcomes, and recommendations"
    }
  ]
}
```

#### Workflow Templates

Create reusable workflow templates:

```python
# cursor_workflows.py
SCREENING_WORKFLOW = """
1. Connect to MongoDB MCP server
2. Fetch patient data for {patient_id}
3. Extract demographics, vitals, medical history
4. Use NLX MCP to analyze clinical notes
5. Apply screening algorithms
6. Generate risk assessment
7. Create actionable recommendations
8. Store results in MongoDB
"""

BATCH_ANALYSIS = """
1. Query MongoDB for patient cohort: {criteria}
2. For each patient:
   - Extract relevant data
   - Run NLX analysis on text fields
   - Apply ML models
   - Calculate risk scores
3. Aggregate results
4. Generate population health insights
5. Export findings to dashboard
"""
```

## 🔒 Security and Compliance

### HIPAA Compliance

- **Data Encryption**: All data encrypted in transit and at rest
- **Access Controls**: Role-based access with audit logging
- **Wiz Integration**: Continuous security monitoring
- **AWS Security**: VPC isolation and security groups

### Data Privacy

- **Anonymization**: PII removal for analytics
- **Consent Management**: Patient consent tracking
- **Data Retention**: Automated data lifecycle management
- **Audit Trails**: Complete action logging

## 📈 Monitoring and Analytics

### Health Metrics Dashboard

Access at `http://localhost:8080/dashboard`:

- **Patient Screening Metrics**
- **System Performance**
- **Data Quality Indicators**
- **Alert Statistics**
- **User Activity Logs**

### Performance Monitoring

```bash
# Check MCP server status
curl http://localhost:8000/health

# MongoDB connection status
python3 -c "from mongo_mcp_server import test_connection; test_connection()"

# NLX service status
python3 -c "from nlx_mcp_server import test_nlx; test_nlx()"
```

## 🚨 Troubleshooting

### Common Issues

#### MongoDB Connection Failed
```bash
# Check connection string
python3 test_atlas_connection.py

# Verify IP whitelist in Atlas
# Check username/password
# Ensure database exists
```

#### NLX API Errors
```bash
# Verify API key
export NLX_API_KEY=your_key
python3 test_nlx_connection.py

# Check rate limits
# Verify endpoint URL
```

#### Cursor MCP Not Working
```bash
# Check MCP configuration
cat ~/.cursor/mcp.json

# Restart Cursor
# Check server logs
tail -f mcp_server.log
```

### Getting Help

- **Documentation**: Check `/docs` folder
- **Logs**: All logs in `/logs` directory  
- **Support**: Create issue in repository
- **Community**: Join our Discord server

## 🚀 Deployment

### Development Environment
```bash
# Start all services
./start_dev.sh

# Run tests
python3 -m pytest tests/

# Check health
./health_check.sh
```

### Production Deployment
```bash
# Deploy to AWS
./deploy_aws.sh

# Configure load balancer
# Set up monitoring
# Enable backup systems
```

## 📚 API Reference

### MongoDB MCP Server Tools

- `connect_to_mongodb_atlas()` - Connect to Atlas cluster
- `list_collections()` - List all collections  
- `find_documents()` - Query with filtering
- `insert_document()` - Insert new documents
- `update_documents()` - Update existing documents
- `delete_documents()` - Delete documents
- `get_collection_stats()` - Collection statistics

### NLX MCP Server Tools

- `analyze_medical_text()` - Extract medical entities
- `classify_clinical_notes()` - Classify note types
- `extract_symptoms()` - Identify symptoms
- `risk_assessment()` - Calculate risk scores
- `generate_summary()` - Create clinical summaries

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **MongoDB Atlas** - Database hosting
- **NLX Platform** - NLP capabilities  
- **Temporal** - Workflow orchestration
- **Wiz** - Security and compliance
- **AWS** - Cloud infrastructure
- **Cursor** - AI-powered development environment

---

**CuraMe** - Transforming healthcare through intelligent patient screening 🏥✨ 