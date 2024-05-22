
# Rewardify Project

Rewardify is a web application designed to manage and distribute rewards. This project aims to simplify the process of reward allocation and tracking for organizations.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Pages Overview](#pages-overview)
- [Contributing](#contributing)
- [License](#license)

## Features

- User authentication and management
- Admin dashboard for reward management
- Responsive design
- Integration with external services

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/PriyabrataP00/rewardify_project.git
   cd rewardify_project
   ```

2. Create a virtual environment and activate it:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Apply migrations:

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. Create a superuser:

   ```bash
   python manage.py createsuperuser
   ```

6. **Add necessary environment variables.** Ensure you have set up all required environment variables, such as database settings, secret keys, etc.

7. Run the development server:

   ```bash
   python manage.py runserver
   ```

## Usage

1. Open your web browser and navigate to `http://127.0.0.1:8000/`.
2. Log in with the superuser credentials created earlier.
3. Use the "Create Admin" feature within the application to add new admins as needed.
4. Manage rewards and users through the provided interfaces.

## Project Structure

- `admin_component/` - Contains the admin-related functionalities.
- `user_component/` - Handles user-related operations.
- `rewardify_project/` - Main project settings and configurations.
- `app_images/` - Stores images used in the application.
- `media/` - Media files for the application.
- `requirements.txt` - List of dependencies.
- `manage.py` - Django's command-line utility.

## Pages Overview

### Admin Pages

1. **Home**: Overview of the added applications.
2. **Add Apps**: Functionality to add new applications.
3. **Settings**: Configure application settings such as creating, editing or deleting Categories and SubCategories .
4. **Create Admin**: Feature to create new admin users.

### User Pages

1. **Home**: User-specific dashboard showing completed tasks.
2. **Profile**: View  personal information and preferences.
3. **Points**: Track and view accumulated points alongwith a leaderboard.
4. **Tasks**: View and manage tasks assigned to the user.

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add new feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Open a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
