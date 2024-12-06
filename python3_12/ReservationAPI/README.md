# Henry Meds Reservation API Take-Home
### Richard Thomas [thomas.richard.l@gmail.com](mailto:thomas.richard.l@gmail.com)

## Contents
- [Summary](#summary)
- [Instructions](#instructions)
- [Assumptions](#assumptions)
- [Trade-offs](#trade-offs)

## Summary
This is an implementation of an API that meets the following specified requirements (See [requirements](https://henrymeds.notion.site/Reservation-Backend-v3-1e5c24f700b846f19b173f5e18c4ebc5)):
- Allows providers to submit times they are available for appointments
    - e.g. On Friday the 13th of August, Dr. Jekyll wants to work between 8am and 3pm
- Allows a client to retrieve a list of available appointment slots
    - Appointment slots are 15 minutes long
- Allows clients to reserve an available appointment slot
- Allows clients to confirm their reservation
- Reservations expire after 30 minutes if not confirmed and are again available for other clients to reserve that appointment slot
- Reservations must be made at least 24 hours in advance

For this implementation, I used Python 3.12, FastAPI 0.115.6, and PostgreSQL 16.6 hosted in Aiven

## Instructions

To run:
- Ensure Python 3.12 is installed
  - (Optional, but recommended) create a [virtual environment](https://docs.python.org/3/library/venv.html) in the project directory
- Ensure .env file is in ReservationAPI directory (provided separately)
- Install dependencies with command `pip install -r requirements.txt`
- In any terminal/shell, navigate to the ReservationAPI directory, and run the command `fastapi dev main.py`
- By default, the application server for the API should now be running on http://127.0.0.1:8000

For API documentation:
- For Swagger/OpenAPI docs, go to http://127.0.0.1:8000/docs
- For alternative docs by ReDoc, go to http://127.0.0.1:8000/redoc

## Assumptions/Experiences

As far as I can tell from my testing, the API does meet all the stated requirements. For data persistence, I leveraged a hosted database. The API has absolutely no authentication, and any user can add clients/providers, set availability for any provider, and reserve/confirm appointments for any client/provider. The requirments did not state anything about this, but it would probably be a consideration if this was to be used in a production environment.

I was instructed to spend no more than ~3 hours on this - I did end up spending a bit more (probably closer to 6 hours total), but that was largely due to troubleshooting issues I had working with the ORM and handling some of the relationships between the data. That aside, the actual work on implementing the API took probably close to 2-3 hours, if I had to estimate.

## Trade-offs

If I had more time/was writing this to be used in an actual production environment, I would definitely focus more on authentication/security to ensure that clients and providers can only access/modify their own data.

From a code quality/structure perspective, I would have spent more time to split out the client and provider models into separate create/read/update models to do things like prevent users from providing their own id when creating a client or provider, obfuscating certain fields depending on context, etc.

In a production environment, I would use a proper production-ready application server, focus more on leveraging Alembic to generate DB migrations (it is being used now, but I basically just installed the package and did the most basic configuration to get it working), and include unit tests. Unit tests are definitely lacking here, but FastAPI's use of Pydantic models and built-in validation does provide some comfort over data integrity.

In terms of requirements/features, I would have liked to make the appointment/availability handling a bit more robust, like automatically cleaning up unconfirmed appointments after 30 minutes, and added update/delete endpoints to modify clients, providers, and appointments after being created. I would probably also like to make data entry/querying a bit more robust, particularly around datetime handling and being able to query clients/providers by name or appointments/availability by day. I also probably would have added more validation to guarantee that availability works out with the 15 minute intervals outlined in the requirements (e.g. if a provider sets their availability from 9:34am to 5:00pm instead of something round like 9:00-5:00).

Another thing I did not get around to implementing was enforcing uniqueness/idempotency, particularly around provider availability. For example, a provider can submit the same availability multiple times, and duplicates will appear when you view their availability; however, if an appointment is made and confirmed for one of the duplicate times, all instances are removed from the availability.