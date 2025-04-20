# Social Media Database Project

## Project Description
This project involves the design and implementation of a relational database for a social media platform. The database is structured to handle user profiles, posts, comments, likes, and connections between users. It aims to provide efficient data storage, retrieval, and management for a scalable social media application.

The project focuses on creating a robust schema that ensures data integrity, supports complex queries, and optimizes performance for common social media functionalities.

## Approach
1. **Requirements Analysis**  
    - Identified key entities such as Users, Posts, Comments, Likes, and Friendships.
    - Defined relationships and constraints to model real-world interactions.

2. **Database Design**  
    - Created an Entity-Relationship Diagram (ERD) to visualize the schema.
    - Translated the ERD into a normalized relational schema to eliminate redundancy.

3. **Implementation**  
    - Used SQL Server to define tables, relationships, and constraints.
    - Populated the database with sample data for testing.

4. **Query Development**  
    - Wrote SQL queries to handle common operations like user registration, posting content, liking posts, and retrieving user feeds.
    - Developed queries in `#file:usedQueries.sql`.

5. **Backend Development**  
    - Implemented backend logic using Python in `#file:backend.py` to interact with the database.
    - Integrated SQL queries with Python for seamless data operations.

6. **Frontend Integration**  
    - Built a user interface using Streamlit in `#file:streamlitapp.py` and `#file:userapp.py` to provide a functional application for user interaction.

7. **Testing**  
    - Conducted functional testing to ensure all operations work as expected.
    - Performed stress testing to evaluate scalability under high loads.

## Features
- User registration and profile management.
- Posting, commenting, and liking functionality.
- Friend request and connection management.
- Newsfeed generation based on user activity and connections.

## Tools and Technologies
- **Database Management System**: SQL Server
- **Programming Language**: Python
- **Backend**: `#file:backend.py`
- **Frontend**: Streamlit (`#file:streamlitapp.py`, `#file:userapp.py`)
- **Database Schema**: `#file:databasecreation.sql`
- **Query Scripts**: `#file:usedQueries.sql`

## Future Enhancements
- Implement advanced features like hashtags, direct messaging, and notifications.
- Integrate with a front-end application for a complete user experience.
- Explore additional database optimization techniques for large-scale data.

## How to Use
1. Clone the repository.
2. Import the SQL schema from `#file:databasecreation.sql` into your SQL Server database.
3. Populate the database with sample data or use the provided scripts in `#file:usedQueries.sql`.
4. Run the Streamlit applications (`#file:streamlitapp.py` and `#file:userapp.py`) to interact with the database.

