<a id="top"></a>
# 🚀 Yatube — Social Blogging Platform

[![Python](https://img.shields.io/badge/Python-3.8.3-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-2.2.16-green.svg)](https://www.djangoproject.com/)

> **A modern social blogging platform built with Django** ✨

## 📖 Description

**Yatube** is a feature-rich social blogging platform that allows users to share posts, connect with others, and engage in meaningful discussions. Built with Django, it provides a robust and secure environment for content creators and readers alike.

### ✨ Key Features

- 📝 **Rich Post Creation** - Create posts with images and text
- 👥 **User Groups** - Join communities and share content within groups
- 💬 **Comments System** - Engage with posts through comments
- 👤 **User Profiles** - Personal profiles with post history
- 🔔 **Follow System** - Follow your favorite authors
- 🔒 **Secure Authentication** - CSRF protection and email verification
- 📱 **Responsive Design** - Works on all devices
- ⚡ **Performance Optimized** - Caching for better performance
- 🧪 **Fully Tested** - Comprehensive test coverage

### 🛡️ Security Features

- CSRF protection enabled
- Email verification for new registrations
- Secure user authentication
- Admin panel for database management

---

## 🛠️ Technology Stack

- **Backend**: Python 3.8.3, Django 2.2.16
- **Database**: SQLite
- **Frontend**: HTML, CSS, JavaScript
- **Testing**: pytest
- **Other**: See `requirements.txt` for complete dependencies

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Git
- pip

### Installation

1. **Clone the repository**
   ```bash
   git clone git@github.com:andrei-kolesnik-california/Yatube.git
   cd Yatube
   ```

2. **Create and activate virtual environment**
   
   **For Windows:**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```
   
   **For macOS/Linux:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run database migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create superuser (admin)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Start the development server**
   ```bash
   python manage.py runserver
   ```

7. **Open your browser**
   
   Navigate to `http://127.0.0.1:8000/` to see the application!

---

## 📍 API Endpoints

| Endpoint | Description | Access |
|----------|-------------|---------|
| `/` | Home page | Public |
| `/about/author/` | About the author | Public |
| `/about/tech/` | Technologies used | Public |
| `/auth/signup/` | User registration | Public |
| `/auth/login/` | User login | Public |
| `/profile/<username>/` | User profile | Public |
| `/create/` | Create new post | Authenticated |
| `/posts/<post_id>/edit/` | Edit post | Author only |
| `/group/<group_name>/` | Group posts | Public |
| `/profile/<username>/follow/` | Follow user | Authenticated |
| `/posts/<post_id>/` | Post details & comments | Public |
| `/admin/` | Admin panel | Admin only |

---

## 🧪 Testing

The project includes comprehensive unit tests covering all major functionality:

```bash
# Run all tests
python manage.py test

# Run tests with coverage
coverage run --source='.' manage.py test
coverage report
```

---

## 📁 Project Structure

```
Yatube/
├── yatube/                 # Main Django project
│   ├── posts/             # Posts app
│   ├── users/             # Users app
│   ├── about/             # About pages
│   └── core/              # Core functionality
├── templates/             # HTML templates
├── static/                # Static files
├── tests/                 # Test files
└── requirements.txt       # Dependencies
```

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 👨‍💻 Author

**Andrei Kolesnik** - [GitHub Profile](https://github.com/andrei-kolesnik-california)

---

<div align="center">

⭐ **Star this repository if you found it helpful!** ⭐

</div>

---

<div align="center">

[⬆️ Back to Top](#top)

</div>
