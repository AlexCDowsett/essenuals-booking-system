# Essensuals Booking System

A professional hairdressing salon booking system developed as an A-Level project. This system provides a complete solution for managing appointments, clients, staff, and services at Essensuals hair salon.

## Features

- **Secure Login System**: Staff authentication with different access levels (Admin and Staff)
- **Appointment Management**:
  - View and manage appointments in a calendar interface
  - Book new appointments
  - Cancel existing appointments
  - Process payments
- **Client Management**:
  - Add new clients
  - Store client contact information
  - View client history
- **Staff Management**:
  - Manage staff accounts
  - Track staff performance
  - Set staff rates
- **Service Management**:
  - Configure different haircut services
  - Set prices and estimated durations
  - Track service history

## Technical Details

- Built with Python and Tkinter for the GUI
- SQLite database for data storage
- Configurable working hours and appointment intervals
- Customizable interface colors and fonts

## Installation

1. Ensure you have Python installed on your system
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the system:
   ```bash
   python system.py
   ```

## Default Login

For first-time use:
- Staff ID: 1
- Password: ess19

## Configuration

The system can be configured through the following parameters in `system.py`:

- Working hours (first and last appointment times)
- Appointment intervals
- Working days
- Interface colors and fonts
- Window settings

## Database Management

The system uses SQLite for data storage. To view or modify the database directly:

1. Download DB Browser for SQLite from [sqlitebrowser.org](https://sqlitebrowser.org/dl/)
2. Open the `bookings.db` file located in the `db` directory

## Project Structure

- `system.py`: Main application file
- `db/`: Database directory
- `resources/`: Application resources (images, icons)
- `requirements.txt`: Python dependencies

## Development

This project was developed as an A-Level project by Alex Dowsett. It demonstrates the implementation of:

- Object-oriented programming
- Database design and management
- GUI development
- User authentication and security
- Business logic implementation

## Support

For any issues or questions, please refer to the User Guide or contact the system administrator. 