# My Weblog v2

A personal blog and portfolio website built with Django, targeting a Persian-speaking (Farsi/RTL) audience.

## Features

- **Blog** - Markdown-based posts with YAML front matter, categories, tags, threaded comments, FAQs, featured posts, and automatic syntax highlighting.
- **Projects** - Portfolio showcase with employer, date, technologies, and category filtering.
- **Resume** - Profile, work experience, skills, education, expertise scores, and social links with a superuser-only dashboard for management.
- **Contact** - Contact form with reCAPTCHA v3 spam protection.
- **Image Processing** - Automatic WebP conversion for all uploaded images (avatar, blog, project).
- **RTL Support** - Full right-to-left layout with automatic language detection in markdown content.
- **Jalali Dates** - Persian calendar date display throughout the site.
- **Dark Theme** - Toggle between light and dark modes.

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Django 5.2, Python |
| Database | MySQL |
| Frontend | Bootstrap 5 (RTL), jQuery, Font Awesome, Animate.css |
| Content | Markdown rendering (Pygments, BeautifulSoup, Bleach) |
| Media | Pillow (WebP conversion) |
| Security | django-recaptcha v3 |
| Environment | django-environ |

## Project Structure

```
My_weblog_v2/
├── README.md
├── requirements.txt
├── .gitignore
└── config/                    # Django project root
    ├── .env                   # Environment variables (not committed)
    ├── manage.py
    ├── config/                # Settings module
    │   ├── settings.py
    │   ├── urls.py
    │   ├── wsgi.py
    │   └── asgi.py
    ├── home/                  # Landing page and contact form
    ├── blog/                  # Blog engine (posts, comments, FAQs)
    ├── project/               # Project portfolio
    ├── resume/                # Resume/CV and dashboard
    ├── templates/             # Shared HTML templates
    ├── static/                # CSS, JS, fonts, images
    └── media/                 # User uploads
```

## Prerequisites

- Python 3.10+
- MySQL 8.0+
- pip

## Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your-username/My_weblog_v2.git
   cd My_weblog_v2
   ```

2. **Create and activate a virtual environment:**

   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**

   Copy the example environment file and fill in your values:

   ```bash
   cp config/.env.example config/.env
   ```

   Edit `config/.env` with your database credentials, Django secret key, and reCAPTCHA keys.

5. **Create the MySQL database:**

   ```sql
   CREATE DATABASE your_db_name CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```

6. **Run migrations:**

   ```bash
   cd config
   python manage.py migrate
   ```

7. **Create a superuser:**

   ```bash
   python manage.py createsuperuser
   ```

8. **Run the development server:**

   ```bash
   python manage.py runserver
   ```

   The site will be available at `http://127.0.0.1:8000/`.

## Environment Variables

Create `config/.env` based on the following template:

```
SECRET_KEY=your-django-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_HOST=localhost
DB_PORT=3306
RECAPTCHA_PUBLIC_KEY=your-recaptcha-public-key
RECAPTCHA_PRIVATE_KEY=your-recaptcha-private-key
RECAPTCHA_REQUIRED_SCORE=0.5
```

## URL Structure

| URL | App | Description |
|-----|-----|-------------|
| `/` | home | Landing page with profile and contact form |
| `/blog/` | blog | Blog listing |
| `/blog/<slug>/` | blog | Blog post detail |
| `/project/` | project | Project portfolio listing |
| `/project/<slug>/` | project | Project detail |
| `/resume/` | resume | Public resume page |
| `/resume/dashboard/` | resume | Superuser dashboard for resume management |
| `/admin/` | Django admin | Administration panel |

## License

This project is for personal use. Contact the author for licensing information.
