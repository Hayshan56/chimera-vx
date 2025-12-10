CHIMERA-VX DEPLOYMENT GUIDE
## From Termux to Production Cluster

---

## 🚀 QUICK START DEPLOYMENT

### **Termux (Android) - 5 Minutes:**
```bash
# 1. Clone repository
cd ~
git clone https://github.com/Hayshan56/chimera-vx
cd chimera-vx

# 2. Run setup script
chmod +x setup.sh
./setup.sh

# 3. Start server
python3 server/main_server.py

# 4. In another terminal, run client
python3 client/player_client.py
```

Linux Desktop - 10 Minutes:

```bash
# 1. Clone and setup
git clone https://github.com/Hayshan56/chimera-vx
cd chimera-vx
chmod +x setup.sh
sudo ./setup.sh

# 2. Start services
./deployment/start_all.sh

# 3. Access web interface
# Open browser to http://localhost:8080
```

📋 SYSTEM REQUIREMENTS

Minimum (Testing):

· CPU: 2 cores @ 2.0GHz
· RAM: 4GB
· Storage: 20GB
· OS: Android (Termux) or Linux
· Network: Basic internet connection

Recommended (Development):

· CPU: 4 cores @ 3.0GHz
· RAM: 8GB
· Storage: 100GB SSD
· OS: Ubuntu 22.04 LTS
· Network: 100Mbps connection

Production (Large Scale):

· CPU: 8+ cores @ 3.5GHz
· RAM: 32GB+
· Storage: 1TB NVMe SSD
· OS: Ubuntu Server 22.04 LTS
· Network: 1Gbps+ with DDoS protection
· CDN: Cloudflare or equivalent
· Database: PostgreSQL cluster
· Cache: Redis cluster

---

🔧 TERMUX DEPLOYMENT (DETAILED)

Step 1: Termux Setup

```bash
# Update Termux
pkg update -y && pkg upgrade -y

# Install basic tools
pkg install -y git python python-pip nodejs clang make cmake
pkg install -y proot-distro wget curl nano vim tree htop

# Install puzzle-specific tools
pkg install -y rtl-sdr hackrf gnuroadio
pkg install -y tshark wireshark nmap
pkg install -y imagemagick ffmpeg sox
pkg install -y sqlite mariadb
pkg install -y binutils radare2 gdb
pkg install -y qemu-system-x86_64
pkg install -y z3 yices
pkg install -y verilog gtkwave

# Install Ubuntu inside Termux (optional)
proot-distro install ubuntu
proot-distro login ubuntu -- apt update
proot-distro login ubuntu -- apt install python3 python3-pip
```
Step 2: Clone and Setup

```bash
# Clone repository
cd ~
git clone https://github.com/Haysha56/chimera-vx
cd chimera-vx

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Generate encryption keys
python3 -c "
import secrets
import base64
import os

os.makedirs('keys', exist_ok=True)

# Server key
with open('keys/server.key', 'w') as f:
    f.write(base64.b64encode(secrets.token_bytes(256)).decode())

# Session secret
with open('keys/session.secret', 'w') as f:
    f.write(base64.b64encode(secrets.token_bytes(32)).decode())

print('Keys generated in keys/ directory')
"

# Initialize database
sqlite3 chimera.db < server/schema.sql
```

Step 3: Configuration

```bash
# Create config file
cat > server/config.py << 'EOF'
import os

class Config:
    # Server settings
    SECRET_KEY = open('keys/session.secret').read().strip()
    SERVER_HOST = '0.0.0.0'
    SERVER_PORT = 8080
    DEBUG = False
    
    # Database
    DATABASE_PATH = 'chimera.db'
    
    # Security
    SALT_ROUNDS = 12
    SESSION_TIMEOUT = 86400  # 24 hours
    
    # Puzzle settings
    MAX_ATTEMPTS_PER_PUZZLE = 10
    PUZZLE_TIMEOUT = 86400  # 24 hours per puzzle
    
    # Paths
    LOG_DIR = 'logs'
    DATA_DIR = 'data'
    TEMP_DIR = 'temp'
    
    # External APIs (optional)
    WEATHER_API_KEY = ''
    GEOCODE_API_KEY = ''
    BLOCKCHAIN_API_URL = 'https://blockchain.info'
EOF
```

Step 4: Start Services

```bash
# Start server (background)
nohup python3 server/main_server.py > logs/server.log 2>&1 &
SERVER_PID=$!
echo "Server started with PID: $SERVER_PID"

# Start monitoring
nohup python3 server/monitor.py > logs/monitor.log 2>&1 &
MONITOR_PID=$!
echo "Monitor started with PID: $MONITOR_PID"

# Check if running
sleep 2
curl -s http://localhost:8080/api/v1/status | python3 -m json.tool
```

Step 5: Client Setup

```bash
# In another Termux session
cd ~/chimera-vx
source venv/bin/activate

# Run client
python3 client/player_client.py

# Or use CLI
python3 client/cli.py --register --username "testplayer"
```

---

🐳 DOCKER DEPLOYMENT

Docker Compose Setup:

```yaml
# docker-compose.yml
version: '3.8'

services:
  # Main server
  chimera-server:
    build: ./server
    ports:
      - "8080:8080"
      - "8081:8081"  # Monitoring
    environment:
      - DATABASE_URL=postgresql://chimera:password@db/chimera
      - REDIS_URL=redis://redis:6379
      - SECRET_KEY=${SECRET_KEY}
    volumes:
      - ./data:/data
      - ./logs:/logs
    depends_on:
      - db
      - redis
    restart: unless-stopped

  # Database
  db:
    image: postgres:15
    environment:
      - POSTGRES_USER=chimera
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=chimera
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./server/schema.sql:/docker-entrypoint-initdb.d/init.sql
    restart: unless-stopped

  # Redis cache
  redis:
    image: redis:7-alpine
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data
    restart: unless-stopped

  # Puzzle generator
  puzzle-gen:
    build: ./generation
    environment:
      - SERVER_URL=http://chimera-server:8080
      - GENERATOR_KEY=${GENERATOR_KEY}
    volumes:
      - ./puzzles:/puzzles
    restart: unless-stopped

  # Monitoring
  monitor:
    build: ./monitoring
    ports:
      - "9090:9090"  # Prometheus
      - "3000:3000"  # Grafana
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml
      - ./monitoring/grafana:/etc/grafana
    restart: unless-stopped

  # Reverse proxy (optional)
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./deployment/nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - chimera-server
    restart: unless-stopped

volumes:
  postgres_data:
  redis_data:
```

Dockerfile for Server:

```dockerfile
# server/Dockerfile
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc g++ make cmake \
    sqlite3 libsqlite3-dev \
    libssl-dev libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Create user
RUN useradd -m -u 1000 chimera
USER chimera
WORKDIR /home/chimera/app

# Copy requirements
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create directories
RUN mkdir -p logs data temp keys

# Expose port
EXPOSE 8080

# Start server
CMD ["python", "main_server.py"]
```

Deploy with Docker:

```bash
# 1. Build and start
docker-compose up -d --build

# 2. Check logs
docker-compose logs -f

# 3. Stop services
docker-compose down

# 4. With data persistence
docker-compose down -v  # Removes volumes too
```

---

☁️ CLOUD DEPLOYMENT

AWS Deployment (EC2 + RDS + ElastiCache):

```bash
#!/bin/bash
# deploy-aws.sh

# Variables
STACK_NAME="chimera-vx"
REGION="us-east-1"
KEY_NAME="chimera-key"
INSTANCE_TYPE="t3.large"

# Create CloudFormation stack
aws cloudformation create-stack \
  --stack-name $STACK_NAME \
  --template-body file://deployment/aws-cloudformation.yml \
  --parameters \
    ParameterKey=InstanceType,ParameterValue=$INSTANCE_TYPE \
    ParameterKey=KeyName,ParameterValue=$KEY_NAME \
  --capabilities CAPABILITY_IAM \
  --region $REGION

# Wait for completion
aws cloudformation wait stack-create-complete \
  --stack-name $STACK_NAME \
  --region $REGION

# Get public IP
INSTANCE_IP=$(aws cloudformation describe-stacks \
  --stack-name $STACK_NAME \
  --region $REGION \
  --query "Stacks[0].Outputs[?OutputKey=='PublicIP'].OutputValue" \
  --output text)

echo "Deployment complete! Access at: http://$INSTANCE_IP:8080"
```

CloudFormation Template:

```yaml
# deployment/aws-cloudformation.yml
AWSTemplateFormatVersion: '2010-09-09'
Description: Chimera-VX CTF Platform

Parameters:
  InstanceType:
    Type: String
    Default: t3.large
    AllowedValues:
      - t3.medium
      - t3.large
      - t3.xlarge
      - m5.large
      - m5.xlarge
  
  KeyName:
    Type: AWS::EC2::KeyPair::KeyName
    Description: SSH key pair

Resources:
  # EC2 Instance
  ChimeraInstance:
    Type: AWS::EC2::Instance
    Properties:
      InstanceType: !Ref InstanceType
      ImageId: ami-0c55b159cbfafe1f0  # Ubuntu 22.04
      KeyName: !Ref KeyName
      SecurityGroups:
        - !Ref SecurityGroup
      UserData:
        Fn::Base64: |
          #!/bin/bash
          apt-get update
          apt-get install -y git docker.io docker-compose
          git clone https://github.com/Hayshan56/chimera-vx
          cd chimera-vx
          docker-compose up -d
# Security Group
  SecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupDescription: Chimera-VX security group
      SecurityGroupIngress:
        - IpProtocol: tcp
          FromPort: 22
          ToPort: 22
          CidrIp: 0.0.0.0/0
        - IpProtocol: tcp
          FromPort: 80
          ToPort: 80
          CidrIp: 0.0.0.0/0
        - IpProtocol: tcp
          FromPort: 443
          ToPort: 443
          CidrIp: 0.0.0.0/0
        - IpProtocol: tcp
          FromPort: 8080
          ToPort: 8080
          CidrIp: 0.0.0.0/0

Outputs:
  PublicIP:
    Description: Public IP address
    Value: !GetAtt ChimeraInstance.PublicIp
  SSHCommand:
    Description: SSH command
    Value: !Sub 'ssh -i ${KeyName}.pem ubuntu@${ChimeraInstance.PublicIp}'
```

---

🚢 KUBERNETES DEPLOYMENT

Kubernetes Manifests:

```yaml
# deployment/k8s/chimera-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: chimera-server
  namespace: chimera
spec:
  replicas: 3
  selector:
    matchLabels:
      app: chimera-server
  template:
    metadata:
      labels:
        app: chimera-server
    spec:
      containers:
      - name: server
        image: Hayshan56/chimera-vx:latest
        ports:
   - containerPort: 8080
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: chimera-secrets
              key: database-url
        - name: REDIS_URL
          value: "redis://chimera-redis:6379"
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /api/v1/health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /api/v1/ready
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: chimera-service
  namespace: chimera
spec:
  selector:
    app: chimera-server
  ports:
  - port: 80
    targetPort: 8080
  type: LoadBalancer
```

Deploy to Kubernetes:

```bash
# 1. Create namespace
kubectl create namespace chimera

# 2. Create secrets
kubectl create secret generic chimera-secrets \
  --namespace=chimera \
  --from-literal=database-url='postgresql://user:pass@host/db' \
  --from-literal=secret-key='your-secret-key-here'

# 3. Deploy applications
kubectl apply -f deployment/k8s/

# 4. Check status
kubectl get all -n chimera

# 5. Access service
kubectl get service chimera-service -n chimera -o jsonpath='{.status.loadBalancer.ingress[0].ip}'
```

---

🔐 SECURITY DEPLOYMENT CHECKLIST

Pre-Deployment:

· Generate new encryption keys
· Update all passwords and secrets
· Review firewall rules
· Configure SSL certificates
· Set up monitoring and alerts
· Backup existing data

Network Security:

```bash
# Configure firewall (UFW example)
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw allow 8080/tcp  # Chimera API
sudo ufw enable
```

SSL Configuration (Let's Encrypt):

```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d chimera.yourdomain.com

# Auto-renewal
sudo certbot renew --dry-run
```

Database Security:

```sql
-- PostgreSQL security settings
ALTER USER chimera WITH PASSWORD 'strong-password-here';
REVOKE ALL ON DATABASE chimera FROM PUBLIC;
GRANT CONNECT ON DATABASE chimera TO chimera;

-- Enable SSL
ALTER SYSTEM SET ssl = 'on';
ALTER SYSTEM SET ssl_cert_file = '/etc/ssl/certs/ssl-cert-snakeoil.pem';
ALTER SYSTEM SET ssl_key_file = '/etc/ssl/private/ssl-cert-snakeoil.key';
```

---

📊 MONITORING DEPLOYMENT

Prometheus Configuration:

```yaml
# monitoring/prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

alerting:
  alertmanagers:
    - static_configs:
        - targets: ['alertmanager:9093']

rule_files:
  - "alerts/*.yml"

scrape_configs:
  - job_name: 'chimera-server'
    static_configs:
      - targets: ['chimera-server:8080']
    
  - job_name: 'node-exporter'
    static_configs:
      - targets: ['node-exporter:9100']
    
  - job_name: 'postgres-exporter'
    static_configs:
      - targets: ['postgres-exporter:9187']
```

Grafana Dashboard Import:

```json
{
  "dashboard": {
    "title": "Chimera-VX Monitoring",
    "panels": [
      {
        "title": "Active Players",
        "targets": [{
          "expr": "chimera_players_active",
          "legendFormat": "Active Players"
        }]
      },
      {
        "title": "Puzzle Submissions",
        "targets": [{
          "expr": "rate(chimera_submissions_total[5m])",
          "legendFormat": "Submissions/sec"
        }]
      }
    ]
  }
}
```
Alert Rules:

```yaml
# monitoring/alerts/chimera-alerts.yml
groups:
  - name: chimera-alerts
    rules:
      - alert: HighErrorRate
        expr: rate(chimera_http_errors_total[5m]) > 0.1
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "High error rate detected"
          description: "Error rate is {{ $value }} per second"
      
      - alert: DatabaseDown
        expr: up{job="postgres-exporter"} == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Database is down"
          description: "PostgreSQL exporter is not responding"
```

---

🗃️ DATA MIGRATION

SQLite to PostgreSQL Migration:

```bash
# Export from SQLite
sqlite3 chimera.db .dump > chimera.sql

# Convert for PostgreSQL
sed -i 's/INTEGER PRIMARY KEY/SERIAL PRIMARY KEY/g' chimera.sql
sed -i 's/DATETIME/TIMESTAMP/g' chimera.sql
sed -i '/^PRAGMA/d' chimera.sql
sed -i '/^BEGIN/d' chimera.sql
sed -i '/^COMMIT/d' chimera.sql

# Import to PostgreSQL
psql -U chimera -d chimera -f chimera.sql
```

Backup Strategy:

```bash
#!/bin/bash
# backup.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups/chimera"

# Create backup directory
mkdir -p $BACKUP_DIR

# Backup database
pg_dump -U chimera chimera > $BACKUP_DIR/chimera_db_$DATE.sql

# Backup puzzle assets
tar -czf $BACKUP_DIR/puzzles_$DATE.tar.gz puzzles/

# Backup logs
tar -czf $BACKUP_DIR/logs_$DATE.tar.gz logs/

# Upload to S3 (optional)
aws s3 cp $BACKUP_DIR/chimera_db_$DATE.sql s3://chimera-backups/
aws s3 cp $BACKUP_DIR/puzzles_$DATE.tar.gz s3://chimera-backups/
aws s3 cp $BACKUP_DIR/logs_$DATE.tar.gz s3://chimera-backups/

# Clean old backups (keep 30 days)
find $BACKUP_DIR -type f -mtime +30 -delete
```

---

🧪 TESTING DEPLOYMENT

Health Check Script:

```python
# tests/health_check.py
import requests
import json
import sys

ENDPOINTS = [
    ("http://localhost:8080/api/v1/status", "GET"),
    ("http://localhost:8080/api/v1/health", "GET"),
    ("http://localhost:8080/api/v1/ready", "GET"),
]

def check_endpoint(url, method):
    try:
        if method == "GET":
            response = requests.get(url, timeout=5)
        elif method == "POST":
            response = requests.post(url, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            return True, data.get("status", "unknown")
        else:
            return False, f"HTTP {response.status_code}"
    except Exception as e:
        return False, str(e)

def main():
    print("🧪 Chimera-VX Health Check")
    print("=" * 50)
    
    all_ok = True
    for url, method in ENDPOINTS:
        ok, status = check_endpoint(url, method)
        icon = "✅" if ok else "❌"
        print(f"{icon} {method} {url}: {status}")
        if not ok:
            all_ok = False
    
    print("=" * 50)
    if all_ok:
        print("✅ All services healthy!")
        sys.exit(0)
    else:
        print("❌ Some services are down!")
        sys.exit(1)

if __name__ == "__main__":
    main()
```

Load Testing:

```bash
# Install k6
curl https://github.com/grafana/k6/releases/download/v0.43.1/k6-v0.43.1-linux-amd64.tar.gz | tar xz
sudo mv k6-v0.43.1-linux-amd64/k6 /usr/local/bin/

# Run load test
k6 run --vus 10 --duration 30s deployment/load-test.js
```

Load Test Script:

```javascript
// deployment/load-test.js
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '30s', target: 10 },   // Ramp up to 10 users
    { duration: '1m', target: 10 },    // Stay at 10 users
    { duration: '30s', target: 50 },   // Ramp up to 50 users
    { duration: '2m', target: 50 },    // Stay at 50 users
    { duration: '30s', target: 0 },    // Ramp down
  ],
};

export default function () {
  // Test status endpoint
  const statusRes = http.get('http://localhost:8080/api/v1/status');
  check(statusRes, {
    'status is 200': (r) => r.status === 200,
    'response time < 500ms': (r) => r.timings.duration < 500,
  });

  // Test puzzle endpoint
  const puzzleRes = http.get('http://localhost:8080/api/v1/challenge');
  check(puzzleRes, {
    'puzzle status is 200': (r) => r.status === 200,
  });

  sleep(1);
}
```

---

🆘 TROUBLESHOOTING

Common Issues and Solutions:

1. Port already in use:

```bash
# Find process using port 8080
sudo lsof -i :8080
# Kill process
sudo kill -9 <PID>
```

1. Database connection issues:

```bash
# Check if database is running
sudo systemctl status postgresql
# Check connection
psql -U chimera -d chimera -c "SELECT 1;"
```

1. Memory issues:

```bash
# Check memory usage
free -h
# Clear cache
sudo sync && echo 3 | sudo tee /proc/sys/vm/drop_caches
```

1. Firewall blocking:

```bash
# Check firewall status
sudo ufw status
# Allow port
sudo ufw allow 8080/tcp
```

1. SSL certificate issues:

```bash
# Check certificate
openssl s_client -connect chimera.yourdomain.com:443
# Renew certificate
sudo certbot renew --force-renewal
```

---

📈 SCALING GUIDE

Vertical Scaling (Bigger Machine):

```bash
# Upgrade instance type (AWS)
aws ec2 modify-instance-attribute \
  --instance-id i-1234567890abcdef0 \
  --instance-type t3.xlarge
```

Horizontal Scaling (More Machines):

```bash
# Auto Scaling Group (AWS)
aws autoscaling create-auto-scaling-group \
  --auto-scaling-group-name chimera-asg \
  --launch-template LaunchTemplateName=chimera-launch-template \
  --min-size 2 \
  --max-size 10 \
  --desired-capacity 2 \
  --vpc-zone-identifier "subnet-123,subnet-456"
```

Database Scaling:

```sql
-- Add read replica
CREATE SUBSCRIPTION chimera_replica
CONNECTION 'host=replica-server user=replicator password=secret'
PUBLICATION chimera_publication;

-- Sharding
CREATE TABLE submissions_2024_01 PARTITION OF submissions
FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');
```

---

🎯 DEPLOYMENT CHECKLIST

Pre-Flight Checklist:

· All tests passing
· Security scan completed
· Backup strategy in place
· Monitoring configured
· Alerting configured
· Documentation updated
· Rollback plan ready

Deployment Day:

· Notify team
· Start backup
· Deploy to staging
· Run smoke tests
· Deploy to production
· Monitor metrics
· Verify functionality
· Update DNS (if needed)

Post-Deployment:

· Monitor for 24 hours
· Check error rates
· Verify backups
· Update documentation
· Schedule next review

---

🏁 CONCLUSION

Chimera-VX can be deployed anywhere from a single Android phone to a global Kubernetes cluster. The architecture is designed to scale with your needs while maintaining security and performance.

Remember: Start small, monitor everything, and scale as needed. The most important deployment is the one that works for your specific use case.

Happy deploying! 🚀


