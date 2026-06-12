# Snippet-Hub

![Python](https://img.shields.io/badge/Python-3.12+-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?logo=postgresql&logoColor=white)
![Alembic](https://img.shields.io/badge/Alembic-DDD?logo=alembic&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-DC382D?logo=redis&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)

![Vue.js](https://img.shields.io/badge/Vue.js-3.5-4FC08D?logo=vue.js&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?logo=typescript&logoColor=white)
![Nuxt UI](https://img.shields.io/badge/Nuxt%20UI-v4-00DC82?logo=nuxt.js&logoColor=white)
![Pinia](https://img.shields.io/badge/Pinia-B7B0FF?logo=pinia&logoColor=white)


## Сервис для хранения сниппетов и полезностей

Идея в том, чтобы структурировать и собрать в одном месте полезный код, шпаргалки, полезные утилиты и тд.

## Превью

[<img width="1916" height="944" alt="Image" src="https://github.com/user-attachments/assets/5a618475-c3df-4d2e-ab15-584cc05e69fc" />](https://github.com/user-attachments/assets/8f00381d-ecd0-4f7a-b85c-6cf3da04215e)

## Возможности

- Создание, редактирование и удаление сниппетов с поддержкой подсветки синтаксиса для популярных языков программирования.
- Система тегов и категорий для удобной навигации и организации кодовой базы.
- Адаптивный пользовательский интерфейс, построенный библиотеке компонентов на Nuxt UI.
- 420+ иконок для разделов, все самые популярные технологии.
- Полноценный REST API с автоматической генерацией интерактивной документации.

## Запуск через Docker

1. Клонируйте репозиторий и перейдите в папку проекта:
   ```bash
   git clone https://github.com/PurpleSwtr/Snippet-Hub.git
   cd Snippet-Hub
   ```
   
2. Отредактируйте файл `compose.yaml`, указав необходимые параметры подключения к базе данных.
   

3. Соберите и запустите контейнеры в фоновом режиме:
   ```bash
   docker-compose up -d --build
   ```

4. После запуска приложения будут доступны по следующим адресам:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000/docs
