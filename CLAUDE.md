# AmazonManager - Claude Memory

## Project Overview
AmazonManager is a Django-based Amazon business management application designed to help users manage their Amazon business operations effectively.

## Technology Stack

### Backend Framework
- **Django**: Web framework for Python providing rapid development capabilities
- **Wagtail CMS**: Powerful, flexible content management system built on Django
  - Installation: `pip install wagtail`
  - Getting started: `wagtail start mysite`
  - Features: Page management, admin interface, rich content editing

### Frontend Technologies
- **HTMX**: High-power tools for HTML enabling modern web interactions without complex JavaScript
  - Installation via CDN: `<script src="https://unpkg.com/htmx.org@2.0.5/dist/htmx.min.js"></script>`
  - Key attributes: `hx-get`, `hx-post`, `hx-swap`, `hx-target`
  - Django integration: Works seamlessly with Django templates and views
  - Best practices: Use relative URLs, implement CSRF protection

- **Alpine.js**: Rugged, minimal framework for composing JavaScript behavior in markup
  - Installation via CDN: `<script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>`
  - Installation via NPM: `npm install alpinejs`
  - Key directives: `x-data`, `x-text`, `x-show`, `x-on`, `x-model`, `x-init`
  - Perfect for reactive components and state management

### Architecture Pattern
This project follows a modern "hypermedia-driven" approach:
- **HTMX** handles server-side rendering and dynamic content updates
- **Alpine.js** provides client-side interactivity and component state
- **Wagtail** manages content and provides admin capabilities
- **Django** serves as the robust backend framework

### Key Integration Points
1. **Django + HTMX**: Server-side templates with dynamic partial updates
2. **HTMX + Alpine.js**: Server-driven content with client-side enhancements
3. **Wagtail + Django**: CMS functionality integrated with custom business logic

### Development Setup
1. Create virtual environment
2. Install Django and Wagtail: `pip install django wagtail`
3. Create project: `wagtail start amazonmanager`
4. Install dependencies: `pip install -r requirements.txt`
5. Run migrations: `python manage.py migrate`
6. Create superuser: `python manage.py createsuperuser`
7. Start server: `python manage.py runserver`

### Frontend Asset Management
- Include HTMX and Alpine.js via CDN for rapid development
- Consider NPM installation for production builds
- HTMX should be loaded before Alpine.js
- Use `defer` attribute for script loading

## Repository Information
- **GitHub URL**: https://github.com/peerjakobsen/AmazonManager
- **Initial commit**: Comprehensive Django .gitignore file
- **Branch**: main