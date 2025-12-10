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

