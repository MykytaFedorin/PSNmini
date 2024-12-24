# How to deploy PSNmini on Linux

## 1. Install Docker

### 1.1 Uninstall Conflicting Versions
First, remove any conflicting versions of Docker or container tools that might already be installed:

```bash
for pkg in docker.io docker-doc docker-compose docker-compose-v2 podman-docker containerd runc; do
    sudo apt-get remove $pkg;
done
```

### 1.2 Add Docker's Official GPG Key
To verify the authenticity of the Docker packages, add Docker's official GPG key:

```bash
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc
```

### 1.3 Add the Docker Repository to Apt Sources
Now, add the Docker repository to your Apt sources:

```bash
echo   "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu   $(. /etc/os-release && echo "$VERSION_CODENAME") stable" |   sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

### 1.4 Update Apt Package Index
Update the package index:

```bash
sudo apt-get update
```

### 1.5 Install Docker Packages
Install the required Docker packages:

```bash
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

### 1.6 Verify Installation
Finally, verify the installation by running the `hello-world` container:

```bash
sudo docker run hello-world
```

## 2. Download the project
```bash
cd ~
git clone git@github.com:MykytaFedorin/PSNmini.git
cd PSNmini
```

## 3. Get Ngrok key
1. Go to the https://dashboard.ngrok.com  and sign up
2. Claim a static domain on https://dashboard.ngrok.com/get-started/setup/linux in Static Domain section.
3. Below Static Domain section you are able to find your auth-key. Copy it and go to the project root folder
```bash

cd ~/PSNmini
touch bot/data/.env.sh
echo "export NGROK_URL=https://your_ngrok_static_domain" >> bot/data/.env.sh
echo "export NGROK_TOKEN=your_ngrok_token" >> bot/data/.env.sh
echo "export BOT_TOKEN=your_tg_bot_token" >> bot/data/.env.sh

```
## 4. Start the project
```bash

cd ~/PSNmini
docker compose up -d --build

```
