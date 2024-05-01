# 🛠️ Installation Steps

1. **Clone the Project:**

```bash
git clone https://github.com/Olszewski-Jakub/Bamboo.git
```

2. **Download Docker**
   - [Download Docker](https://www.docker.com/products/docker-desktop)
3. **[Firebase configuration](https://firebase.google.com/)**
   1. Create Firebase project
   2. Turn on Firebase Authentication via **Email/Password**
   3. Go to project settings
   4. Then go to Service Accounts and generate new **Private Key**
4. **Setting up private key**
   - Copy private key to **'src/main/resources'** and rename it to **firebase_config.json**
5. **Start project**

```bash
docker-compose up
```

6. **Swagger documentation should be avaible at**

- ``` http://localhost:8080/swagger-ui/index.html#/```

