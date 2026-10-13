from flask import Flask, render_template, request, redirect, url_for, session
import os 
import mysql.connector

from werkzeug.security import generate_password_hash, check_password_hash





app = Flask(__name__)



# Secret key for session

app.secret_key = os.environ.get("SECRET_KEY")





# ============================================================

# DATABASE CONNECTION

# ============================================================




import os
import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv(
            "DB_NAME",
            "airport_ground_management"
        ),
        port=int(os.getenv("DB_PORT", "3306"))
    )





# ============================================================

# LOGIN

# ============================================================



# 👇 YAHAN SIGNUP ROUTE PASTE KARO



@app.route("/signup", methods=["GET", "POST"])

def signup():



    if request.method == "POST":



        employee_id = request.form["employee_id"].strip()

        full_name = request.form["full_name"].strip()

        department = request.form["department"].strip()

        email = request.form["email"].strip().lower()

        password = request.form["password"]

        confirm_password = request.form["confirm_password"]



        if password != confirm_password:

            return render_template(

                "signup.html",

                error="Passwords do not match."

            )



        if len(password) < 6:

            return render_template(

                "signup.html",

                error="Password must contain at least 6 characters."

            )



        try:

            conn = get_db_connection()

            cursor = conn.cursor(dictionary=True)



            cursor.execute(

                """

                SELECT user_id

                FROM users

                WHERE employee_id = %s OR email = %s

                """,

                (employee_id, email)

            )



            existing_user = cursor.fetchone()



            if existing_user:

                cursor.close()

                conn.close()



                return render_template(

                    "signup.html",

                    error="Employee ID or Email is already registered."

                )



            hashed_password = generate_password_hash(password)



            cursor.execute(

                """

                INSERT INTO users

                (employee_id, full_name, department, email, password, role)

                VALUES (%s, %s, %s, %s, %s, %s)

                """,

                (

                    employee_id,

                    full_name,

                    department,

                    email,

                    hashed_password,

                    "Ground Staff"

                )

            )



            conn.commit()



            cursor.close()

            conn.close()



            return redirect(url_for("login"))



        except Exception as e:



            return render_template(

                "signup.html",

                error=f"Registration failed: {e}"

            )



    return render_template("signup.html")





@app.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        connection = None
        cursor = None

        try:
            connection = get_db_connection()
            cursor = connection.cursor(dictionary=True)

            cursor.execute(
                """
                SELECT *
                FROM users
                WHERE email = %s
                """,
                (email,)
            )

            user = cursor.fetchone()

            if user:
                stored_password = user["password"]

                # Secure password verification for new accounts.
                password_valid = False

                try:
                    password_valid = check_password_hash(
                        stored_password,
                        password
                    )
                except (ValueError, TypeError):
                    password_valid = False

                # Upgrade the old plaintext password automatically.
                if not password_valid and stored_password == password:
                    password_valid = True

                    new_hash = generate_password_hash(password)

                    cursor.execute(
                        """
                        UPDATE users
                        SET password = %s
                        WHERE user_id = %s
                        """,
                        (new_hash, user["user_id"])
                    )

                if password_valid:

                    cursor.execute(
                        """
                        INSERT INTO login_history
                        (user_id, login_status, ip_address)
                        VALUES (%s, %s, %s)
                        """,
                        (
                            user["user_id"],
                            "SUCCESS",
                            request.remote_addr
                        )
                    )

                    login_history_id = cursor.lastrowid
                    connection.commit()

                    session["user_id"] = user["user_id"]
                    session["full_name"] = user["full_name"]
                    session["role"] = user["role"]
                    session["login_history_id"] = login_history_id

                    return redirect(url_for("dashboard"))

                # Known account + wrong password
                cursor.execute(
                    """
                    INSERT INTO login_history
                    (user_id, login_status, ip_address)
                    VALUES (%s, %s, %s)
                    """,
                    (
                        user["user_id"],
                        "FAILED",
                        request.remote_addr
                    )
                )

                connection.commit()

                return render_template(
                    "index.html",
                    error="Invalid email or password."
                )

            # Unknown email cannot currently be inserted into
            # login_history because user_id is NOT NULL.
            return render_template(
                "index.html",
                error="Invalid email or password."
            )

        except mysql.connector.Error as error:

            if connection:
                connection.rollback()

            return f"Database Error: {error}"

        finally:

            if cursor:
                cursor.close()

            if connection:
                connection.close()

    return render_template("index.html")


# ============================================================

# DASHBOARD

# ============================================================



@app.route("/dashboard")

def dashboard():



    if "user_id" not in session:

        return redirect(url_for("login"))



    return render_template("dashboard.html")





# ============================================================

# FLIGHT MANAGEMENT

# ============================================================



@app.route("/flights", methods=["GET", "POST"])

def flights():



    connection = None

    cursor = None



    try:



        connection = get_db_connection()

        cursor = connection.cursor(dictionary=True)



        # ----------------------------

        # ADD FLIGHT

        # ----------------------------



        if request.method == "POST":



            flight_number = request.form.get("flight_number")

            airline = request.form.get("airline")

            origin_airport = request.form.get("origin_airport")

            destination_airport = request.form.get("destination_airport")

            flight_date = request.form.get("flight_date")

            arrival_time = request.form.get("arrival_time")

            departure_time = request.form.get("departure_time")

            terminal = request.form.get("terminal")

            gate_number = request.form.get("gate_number")

            status = request.form.get("status")



            query = """

                INSERT INTO flights

                (

                    flight_number,

                    airline,

                    origin_airport,

                    destination_airport,

                    flight_date,

                    arrival_time,

                    departure_time,

                    terminal,

                    gate_number,

                    status

                )

                VALUES

                (%s, %s, %s, %s, %s,

                 %s, %s, %s, %s, %s)

            """



            values = (

                flight_number,

                airline,

                origin_airport,

                destination_airport,

                flight_date,

                arrival_time,

                departure_time,

                terminal,

                gate_number,

                status

            )



            cursor.execute(query, values)

            connection.commit()



            return redirect(url_for("flights"))



        # ----------------------------

        # DISPLAY FLIGHTS

        # ----------------------------



        cursor.execute("""

            SELECT *

            FROM flights

            ORDER BY flight_date, departure_time

        """)



        flight_data = cursor.fetchall()



        return render_template(

            "flights.html",

            flights=flight_data

        )



    except mysql.connector.Error as error:



        if connection:

            connection.rollback()



        return f"Database Error: {error}"



    finally:



        if cursor:

            cursor.close()



        if connection:

            connection.close()





# ============================================================

# EDIT FLIGHT

# ============================================================



@app.route("/edit-flight/<int:flight_id>", methods=["GET", "POST"])

def edit_flight(flight_id):



    connection = None

    cursor = None



    try:



        connection = get_db_connection()

        cursor = connection.cursor(dictionary=True)



        if request.method == "POST":



            flight_number = request.form.get("flight_number")

            airline = request.form.get("airline")

            origin_airport = request.form.get("origin_airport")

            destination_airport = request.form.get("destination_airport")

            flight_date = request.form.get("flight_date")

            arrival_time = request.form.get("arrival_time")

            departure_time = request.form.get("departure_time")

            terminal = request.form.get("terminal")

            gate_number = request.form.get("gate_number")

            status = request.form.get("status")



            query = """

                UPDATE flights

                SET

                    flight_number = %s,

                    airline = %s,

                    origin_airport = %s,

                    destination_airport = %s,

                    flight_date = %s,

                    arrival_time = %s,

                    departure_time = %s,

                    terminal = %s,

                    gate_number = %s,

                    status = %s

                WHERE flight_id = %s

            """



            values = (

                flight_number,

                airline,

                origin_airport,

                destination_airport,

                flight_date,

                arrival_time,

                departure_time,

                terminal,

                gate_number,

                status,

                flight_id

            )



            cursor.execute(query, values)

            connection.commit()



            return redirect(url_for("flights"))



        cursor.execute("""

            SELECT *

            FROM flights

            WHERE flight_id = %s

        """, (flight_id,))



        flight = cursor.fetchone()



        if not flight:

            return "Flight not found."



        return render_template(

            "edit_flight.html",

            flight=flight

        )



    except mysql.connector.Error as error:



        if connection:

            connection.rollback()



        return f"Database Error: {error}"



    finally:



        if cursor:

            cursor.close()



        if connection:

            connection.close()





# ============================================================

# DELETE FLIGHT

# ============================================================



@app.route("/delete-flight/<int:flight_id>", methods=["POST"])

def delete_flight(flight_id):



    connection = None

    cursor = None



    try:



        connection = get_db_connection()

        cursor = connection.cursor()



        # Delete related gate allocations first

        cursor.execute("""

            DELETE FROM gate_allocations

            WHERE flight_id = %s

        """, (flight_id,))



        # Delete flight

        cursor.execute("""

            DELETE FROM flights

            WHERE flight_id = %s

        """, (flight_id,))



        connection.commit()



        return redirect(url_for("flights"))



    except mysql.connector.Error as error:



        if connection:

            connection.rollback()



        return f"Database Error: {error}"



    finally:



        if cursor:

            cursor.close()



        if connection:

            connection.close()





# ============================================================

# GATE ALLOCATION

# ============================================================



@app.route("/gate-allocation", methods=["GET", "POST"])

def gate_allocation():



    connection = None

    cursor = None



    try:



        connection = get_db_connection()

        cursor = connection.cursor(dictionary=True)



        # ----------------------------

        # ADD ALLOCATION

        # ----------------------------



        if request.method == "POST":



            flight_id = request.form.get("flight_id")

            gate_id = request.form.get("gate_id")

            allocation_status = request.form.get("allocation_status")



            # Check flight already allocated

            cursor.execute("""

                SELECT allocation_id

                FROM gate_allocations

                WHERE flight_id = %s

                AND allocation_status = 'Active'

            """, (flight_id,))



            existing_flight = cursor.fetchone()



            if existing_flight:



                return "This flight already has an active gate allocation."



            # Check gate already allocated

            cursor.execute("""

                SELECT allocation_id

                FROM gate_allocations

                WHERE gate_id = %s

                AND allocation_status = 'Active'

            """, (gate_id,))



            existing_gate = cursor.fetchone()



            if existing_gate:



                return "This gate is already allocated to another flight."



            query = """

                INSERT INTO gate_allocations

                (

                    flight_id,

                    gate_id,

                    assigned_by,

                    allocation_status

                )

                VALUES

                (%s, %s, %s, %s)

            """



            values = (

                flight_id,

                gate_id,

                1,

                allocation_status

            )



            cursor.execute(query, values)

            connection.commit()



            return redirect(url_for("gate_allocation"))



        # ----------------------------

        # DISPLAY ALLOCATIONS

        # ----------------------------



        cursor.execute("""

            SELECT

                ga.allocation_id,

                ga.flight_id,

                ga.gate_id,

                f.flight_number,

                f.airline,

                g.gate_number,

                g.terminal,

                g.gate_type,

                ga.allocation_status,

                ga.assigned_at

            FROM gate_allocations ga

            JOIN flights f

                ON ga.flight_id = f.flight_id

            JOIN gates g

                ON ga.gate_id = g.gate_id

            ORDER BY ga.assigned_at DESC

        """)



        allocation_data = cursor.fetchall()



        # Flights

        cursor.execute("""

            SELECT

                flight_id,

                flight_number,

                airline

            FROM flights

            ORDER BY flight_number

        """)



        flight_data = cursor.fetchall()



        # Gates

        cursor.execute("""

            SELECT

                gate_id,

                gate_number,

                terminal,

                gate_type,

                status

            FROM gates

            ORDER BY gate_number

        """)



        gate_data = cursor.fetchall()



        return render_template(

            "gate_allocation.html",

            allocations=allocation_data,

            flights=flight_data,

            gates=gate_data

        )



    except mysql.connector.Error as error:



        if connection:

            connection.rollback()



        return f"Database Error: {error}"



    finally:



        if cursor:

            cursor.close()



        if connection:

            connection.close()





# ============================================================

# EDIT GATE ALLOCATION

# ============================================================



@app.route(

    "/edit-gate-allocation/<int:allocation_id>",

    methods=["GET", "POST"]

)

def edit_gate_allocation(allocation_id):



    connection = None

    cursor = None



    try:



        connection = get_db_connection()

        cursor = connection.cursor(dictionary=True)



        if request.method == "POST":



            flight_id = request.form.get("flight_id")

            gate_id = request.form.get("gate_id")

            allocation_status = request.form.get("allocation_status")



            # Check flight

            cursor.execute("""

                SELECT allocation_id

                FROM gate_allocations

                WHERE flight_id = %s

                AND allocation_status = 'Active'

                AND allocation_id != %s

            """, (flight_id, allocation_id))



            existing_flight = cursor.fetchone()



            if existing_flight:



                return "This flight already has another active gate allocation."



            # Check gate

            cursor.execute("""

                SELECT allocation_id

                FROM gate_allocations

                WHERE gate_id = %s

                AND allocation_status = 'Active'

                AND allocation_id != %s

            """, (gate_id, allocation_id))



            existing_gate = cursor.fetchone()



            if existing_gate:



                return "This gate is already allocated to another flight."



            query = """

                UPDATE gate_allocations

                SET

                    flight_id = %s,

                    gate_id = %s,

                    allocation_status = %s

                WHERE allocation_id = %s

            """



            values = (

                flight_id,

                gate_id,

                allocation_status,

                allocation_id

            )



            cursor.execute(query, values)

            connection.commit()



            return redirect(url_for("gate_allocation"))



        cursor.execute("""

            SELECT *

            FROM gate_allocations

            WHERE allocation_id = %s

        """, (allocation_id,))



        allocation = cursor.fetchone()



        if not allocation:

            return "Gate allocation not found."



        cursor.execute("""

            SELECT

                flight_id,

                flight_number,

                airline

            FROM flights

            ORDER BY flight_number

        """)



        flight_data = cursor.fetchall()



        cursor.execute("""

            SELECT

                gate_id,

                gate_number,

                terminal,

                gate_type

            FROM gates

            ORDER BY gate_number

        """)



        gate_data = cursor.fetchall()



        return render_template(

            "edit_gate_allocation.html",

            allocation=allocation,

            flights=flight_data,

            gates=gate_data

        )



    except mysql.connector.Error as error:



        if connection:

            connection.rollback()



        return f"Database Error: {error}"



    finally:



        if cursor:

            cursor.close()



        if connection:

            connection.close()





# ============================================================

# DELETE GATE ALLOCATION

# ============================================================



@app.route(

    "/delete-gate-allocation/<int:allocation_id>",

    methods=["POST"]

)

def delete_gate_allocation(allocation_id):



    connection = None

    cursor = None



    try:



        connection = get_db_connection()

        cursor = connection.cursor()



        cursor.execute("""

            DELETE FROM gate_allocations

            WHERE allocation_id = %s

        """, (allocation_id,))



        connection.commit()



        return redirect(url_for("gate_allocation"))



    except mysql.connector.Error as error:



        if connection:

            connection.rollback()



        return f"Database Error: {error}"



    finally:



        if cursor:

            cursor.close()



        if connection:

            connection.close()





# ============================================================

# GROUND STAFF

# ============================================================



@app.route("/ground-staff", methods=["GET", "POST"])

def ground_staff():



    connection = None

    cursor = None



    try:



        connection = get_db_connection()

        cursor = connection.cursor(dictionary=True)



        if request.method == "POST":



            employee_id = request.form.get("employee_id")

            staff_name = request.form.get("staff_name")

            department = request.form.get("department")

            role = request.form.get("role")

            contact_number = request.form.get("contact_number")

            availability_status = request.form.get("availability_status")



            cursor.execute("""

                SELECT staff_id

                FROM ground_staff

                WHERE employee_id = %s

            """, (employee_id,))



            existing_staff = cursor.fetchone()



            if existing_staff:

                return "Employee ID already exists."



            query = """

                INSERT INTO ground_staff

                (

                    employee_id,

                    staff_name,

                    department,

                    role,

                    contact_number,

                    availability_status

                )

                VALUES

                (%s, %s, %s, %s, %s, %s)

            """



            values = (

                employee_id,

                staff_name,

                department,

                role,

                contact_number,

                availability_status

            )



            cursor.execute(query, values)

            connection.commit()



            return redirect(url_for("ground_staff"))



        cursor.execute("""

            SELECT *

            FROM ground_staff

            ORDER BY staff_id DESC

        """)



        staff_data = cursor.fetchall()



        return render_template(

            "ground_staff.html",

            staff=staff_data

        )



    except mysql.connector.Error as error:



        if connection:

            connection.rollback()



        return f"Database Error: {error}"



    finally:



        if cursor:

            cursor.close()



        if connection:

            connection.close()





# ============================================================

# EDIT GROUND STAFF

# ============================================================



@app.route(

    "/edit-ground-staff/<int:staff_id>",

    methods=["GET", "POST"]

)

def edit_ground_staff(staff_id):



    connection = None

    cursor = None



    try:



        connection = get_db_connection()

        cursor = connection.cursor(dictionary=True)



        if request.method == "POST":



            employee_id = request.form.get("employee_id")

            staff_name = request.form.get("staff_name")

            department = request.form.get("department")

            role = request.form.get("role")

            contact_number = request.form.get("contact_number")

            availability_status = request.form.get("availability_status")



            cursor.execute("""

                SELECT staff_id

                FROM ground_staff

                WHERE employee_id = %s

                AND staff_id != %s

            """, (employee_id, staff_id))



            existing_staff = cursor.fetchone()



            if existing_staff:

                return "Employee ID already exists."



            query = """

                UPDATE ground_staff

                SET

                    employee_id = %s,

                    staff_name = %s,

                    department = %s,

                    role = %s,

                    contact_number = %s,

                    availability_status = %s

                WHERE staff_id = %s

            """



            values = (

                employee_id,

                staff_name,

                department,

                role,

                contact_number,

                availability_status,

                staff_id

            )



            cursor.execute(query, values)

            connection.commit()



            return redirect(url_for("ground_staff"))



        cursor.execute("""

            SELECT *

            FROM ground_staff

            WHERE staff_id = %s

        """, (staff_id,))



        staff_member = cursor.fetchone()



        if not staff_member:

            return "Ground staff member not found."



        return render_template(

            "edit_ground_staff.html",

            staff=staff_member

        )



    except mysql.connector.Error as error:



        if connection:

            connection.rollback()



        return f"Database Error: {error}"



    finally:



        if cursor:

            cursor.close()



        if connection:

            connection.close()





# ============================================================

# DELETE GROUND STAFF

# ============================================================



@app.route(

    "/delete-ground-staff/<int:staff_id>",

    methods=["POST"]

)

def delete_ground_staff(staff_id):



    connection = None

    cursor = None



    try:



        connection = get_db_connection()

        cursor = connection.cursor()



        # Check baggage usage

        cursor.execute("""

            SELECT COUNT(*) AS total

            FROM baggage

            WHERE handled_by = %s

        """, (staff_id,))



        baggage_usage = cursor.fetchone()[0]



        # Check fuel usage

        cursor.execute("""

            SELECT COUNT(*) AS total

            FROM fuel_operations

            WHERE handled_by = %s

        """, (staff_id,))



        fuel_usage = cursor.fetchone()[0]



        if baggage_usage > 0 or fuel_usage > 0:



            return (

                "This staff member is assigned to existing "

                "baggage or fuel operations and cannot be deleted."

            )



        cursor.execute("""

            DELETE FROM ground_staff

            WHERE staff_id = %s

        """, (staff_id,))



        connection.commit()



        return redirect(url_for("ground_staff"))



    except mysql.connector.Error as error:



        if connection:

            connection.rollback()



        return f"Database Error: {error}"



    finally:



        if cursor:

            cursor.close()



        if connection:

            connection.close()





# ============================================================

# BAGGAGE MANAGEMENT

# ============================================================



@app.route("/baggage", methods=["GET", "POST"])

def baggage():



    connection = None

    cursor = None



    try:



        connection = get_db_connection()

        cursor = connection.cursor(dictionary=True)



        # ----------------------------

        # ADD BAGGAGE

        # ----------------------------



        if request.method == "POST":



            flight_number = request.form.get("flight_number")

            baggage_count = request.form.get("baggage_count")

            baggage_weight = request.form.get("baggage_weight")

            handling_status = request.form.get("handling_status")

            handled_by = request.form.get("handled_by")



            query = """

                INSERT INTO baggage

                (

                    flight_number,

                    baggage_count,

                    baggage_weight,

                    handling_status,

                    handled_by

                )

                VALUES

                (%s, %s, %s, %s, %s)

            """



            values = (

                flight_number,

                baggage_count,

                baggage_weight,

                handling_status,

                handled_by if handled_by else None

            )



            cursor.execute(query, values)

            connection.commit()



            return redirect(url_for("baggage"))



        # ----------------------------

        # DISPLAY BAGGAGE

        # ----------------------------



        cursor.execute("""

            SELECT

                b.baggage_id,

                b.flight_number,

                b.baggage_count,

                b.baggage_weight,

                b.handling_status,

                b.handled_by,

                gs.staff_name

            FROM baggage b

            LEFT JOIN ground_staff gs

                ON b.handled_by = gs.staff_id

            ORDER BY b.baggage_id DESC

        """)



        baggage_data = cursor.fetchall()



        # Ground staff

        cursor.execute("""

            SELECT

                staff_id,

                staff_name,

                employee_id

            FROM ground_staff

            ORDER BY staff_name

        """)



        staff_data = cursor.fetchall()



        # Flights

        cursor.execute("""

            SELECT DISTINCT flight_number

            FROM flights

            ORDER BY flight_number

        """)



        flight_data = cursor.fetchall()



        return render_template(

            "baggage.html",

            baggage=baggage_data,

            staff=staff_data,

            flights=flight_data

        )



    except mysql.connector.Error as error:



        if connection:

            connection.rollback()



        return f"Database Error: {error}"



    finally:



        if cursor:

            cursor.close()



        if connection:

            connection.close()





# ============================================================

# EDIT BAGGAGE

# ============================================================



@app.route(

    "/edit-baggage/<int:baggage_id>",

    methods=["GET", "POST"]

)

def edit_baggage(baggage_id):



    connection = None

    cursor = None



    try:



        connection = get_db_connection()

        cursor = connection.cursor(dictionary=True)



        if request.method == "POST":



            flight_number = request.form.get("flight_number")

            baggage_count = request.form.get("baggage_count")

            baggage_weight = request.form.get("baggage_weight")

            handling_status = request.form.get("handling_status")

            handled_by = request.form.get("handled_by")



            query = """

                UPDATE baggage

                SET

                    flight_number = %s,

                    baggage_count = %s,

                    baggage_weight = %s,

                    handling_status = %s,

                    handled_by = %s

                WHERE baggage_id = %s

            """



            values = (

                flight_number,

                baggage_count,

                baggage_weight,

                handling_status,

                handled_by if handled_by else None,

                baggage_id

            )



            cursor.execute(query, values)

            connection.commit()



            return redirect(url_for("baggage"))



        cursor.execute("""

            SELECT *

            FROM baggage

            WHERE baggage_id = %s

        """, (baggage_id,))



        baggage_record = cursor.fetchone()



        if not baggage_record:

            return "Baggage record not found."



        cursor.execute("""

            SELECT DISTINCT flight_number

            FROM flights

            ORDER BY flight_number

        """)



        flight_data = cursor.fetchall()



        cursor.execute("""

            SELECT

                staff_id,

                staff_name,

                employee_id

            FROM ground_staff

            ORDER BY staff_name

        """)



        staff_data = cursor.fetchall()



        return render_template(

            "edit_baggage.html",

            baggage=baggage_record,

            flights=flight_data,

            staff=staff_data

        )



    except mysql.connector.Error as error:



        if connection:

            connection.rollback()



        return f"Database Error: {error}"



    finally:



        if cursor:

            cursor.close()



        if connection:

            connection.close()





# ============================================================

# DELETE BAGGAGE

# ============================================================



@app.route(

    "/delete-baggage/<int:baggage_id>",

    methods=["POST"]

)

def delete_baggage(baggage_id):



    connection = None

    cursor = None



    try:



        connection = get_db_connection()

        cursor = connection.cursor()



        cursor.execute("""

            DELETE FROM baggage

            WHERE baggage_id = %s

        """, (baggage_id,))



        connection.commit()



        return redirect(url_for("baggage"))



    except mysql.connector.Error as error:



        if connection:

            connection.rollback()



        return f"Database Error: {error}"



    finally:



        if cursor:

            cursor.close()



        if connection:

            connection.close()





# ============================================================

# FUEL MANAGEMENT

# ============================================================



@app.route("/fuel-management", methods=["GET", "POST"])

def fuel_management():



    connection = None

    cursor = None



    try:



        connection = get_db_connection()

        cursor = connection.cursor(dictionary=True)



        # ----------------------------

        # ADD FUEL OPERATION

        # ----------------------------



        if request.method == "POST":



            flight_number = request.form.get("flight_number")

            fuel_type = request.form.get("fuel_type")

            fuel_quantity = request.form.get("fuel_quantity")

            fueling_time = request.form.get("fueling_time")

            fuel_status = request.form.get("fuel_status")

            handled_by = request.form.get("handled_by")



            query = """

                INSERT INTO fuel_operations

                (

                    flight_number,

                    fuel_type,

                    fuel_quantity,

                    fueling_time,

                    fuel_status,

                    handled_by

                )

                VALUES

                (%s, %s, %s, %s, %s, %s)

            """



            values = (

                flight_number,

                fuel_type,

                fuel_quantity,

                fueling_time if fueling_time else None,

                fuel_status,

                handled_by if handled_by else None

            )



            cursor.execute(query, values)

            connection.commit()



            return redirect(url_for("fuel_management"))



        # ----------------------------

        # DISPLAY FUEL OPERATIONS

        # ----------------------------



        cursor.execute("""

            SELECT

                fo.fuel_id,

                fo.flight_number,

                fo.fuel_type,

                fo.fuel_quantity,

                fo.fueling_time,

                fo.fuel_status,

                fo.handled_by,

                gs.staff_name

            FROM fuel_operations fo

            LEFT JOIN ground_staff gs

                ON fo.handled_by = gs.staff_id

            ORDER BY fo.fuel_id DESC

        """)



        fuel_data = cursor.fetchall()



        # Flights

        cursor.execute("""

            SELECT DISTINCT flight_number

            FROM flights

            ORDER BY flight_number

        """)



        flight_data = cursor.fetchall()



        # Ground staff

        cursor.execute("""

            SELECT

                staff_id,

                staff_name,

                employee_id

            FROM ground_staff

            ORDER BY staff_name

        """)



        staff_data = cursor.fetchall()



        return render_template(

            "fuel_management.html",

            fuel=fuel_data,

            flights=flight_data,

            staff=staff_data

        )



    except mysql.connector.Error as error:



        if connection:

            connection.rollback()



        return f"Database Error: {error}"



    finally:



        if cursor:

            cursor.close()



        if connection:

            connection.close()





# ============================================================

# EDIT FUEL

# ============================================================



@app.route(

    "/edit-fuel/<int:fuel_id>",

    methods=["GET", "POST"]

)

def edit_fuel(fuel_id):



    connection = None

    cursor = None



    try:



        connection = get_db_connection()

        cursor = connection.cursor(dictionary=True)



        if request.method == "POST":



            flight_number = request.form.get("flight_number")

            fuel_type = request.form.get("fuel_type")

            fuel_quantity = request.form.get("fuel_quantity")

            fueling_time = request.form.get("fueling_time")

            fuel_status = request.form.get("fuel_status")

            handled_by = request.form.get("handled_by")



            query = """

                UPDATE fuel_operations

                SET

                    flight_number = %s,

                    fuel_type = %s,

                    fuel_quantity = %s,

                    fueling_time = %s,

                    fuel_status = %s,

                    handled_by = %s

                WHERE fuel_id = %s

            """



            values = (

                flight_number,

                fuel_type,

                fuel_quantity,

                fueling_time if fueling_time else None,

                fuel_status,

                handled_by if handled_by else None,

                fuel_id

            )



            cursor.execute(query, values)

            connection.commit()



            return redirect(url_for("fuel_management"))



        # Existing fuel record

        cursor.execute("""

            SELECT *

            FROM fuel_operations

            WHERE fuel_id = %s

        """, (fuel_id,))



        fuel_record = cursor.fetchone()



        if not fuel_record:

            return "Fuel operation record not found."



        # Flights

        cursor.execute("""

            SELECT DISTINCT flight_number

            FROM flights

            ORDER BY flight_number

        """)



        flight_data = cursor.fetchall()



        # Ground staff

        cursor.execute("""

            SELECT

                staff_id,

                staff_name,

                employee_id

            FROM ground_staff

            ORDER BY staff_name

        """)



        staff_data = cursor.fetchall()



        return render_template(

            "edit_fuel.html",

            fuel=fuel_record,

            flights=flight_data,

            staff=staff_data

        )



    except mysql.connector.Error as error:



        if connection:

            connection.rollback()



        return f"Database Error: {error}"



    finally:



        if cursor:

            cursor.close()



        if connection:

            connection.close()





# ============================================================

# DELETE FUEL

# ============================================================



@app.route(

    "/delete-fuel/<int:fuel_id>",

    methods=["POST"]

)

def delete_fuel(fuel_id):



    connection = None

    cursor = None



    try:



        connection = get_db_connection()

        cursor = connection.cursor()



        cursor.execute("""

            DELETE FROM fuel_operations

            WHERE fuel_id = %s

        """, (fuel_id,))



        connection.commit()



        return redirect(url_for("fuel_management"))



    except mysql.connector.Error as error:



        if connection:

            connection.rollback()



        return f"Database Error: {error}"



    finally:



        if cursor:

            cursor.close()



        if connection:

            connection.close()





# ============================================================

# REPORTS

# ============================================================



@app.route("/reports")

def reports():



    connection = None

    cursor = None



    try:



        connection = get_db_connection()

        cursor = connection.cursor(dictionary=True)



        # Total flights

        cursor.execute("""

            SELECT COUNT(*) AS total

            FROM flights

        """)



        total_flights = cursor.fetchone()["total"]



        # Total gates

        cursor.execute("""

            SELECT COUNT(*) AS total

            FROM gates

        """)



        total_gates = cursor.fetchone()["total"]



        # Total staff

        cursor.execute("""

            SELECT COUNT(*) AS total

            FROM ground_staff

        """)



        total_staff = cursor.fetchone()["total"]



        # Total baggage

        cursor.execute("""

            SELECT COALESCE(SUM(baggage_count), 0) AS total

            FROM baggage

        """)



        total_baggage = cursor.fetchone()["total"]



        # Total fuel

        cursor.execute("""

            SELECT COALESCE(SUM(fuel_quantity), 0) AS total

            FROM fuel_operations

        """)



        total_fuel = cursor.fetchone()["total"]



        # Active allocations

        cursor.execute("""

            SELECT COUNT(*) AS total

            FROM gate_allocations

            WHERE allocation_status = 'Active'

        """)



        active_allocations = cursor.fetchone()["total"]



        # Flight status

        cursor.execute("""

            SELECT

                status,

                COUNT(*) AS total

            FROM flights

            GROUP BY status

        """)



        flight_status = cursor.fetchall()



        # Baggage status

        cursor.execute("""

            SELECT

                handling_status,

                COUNT(*) AS total

            FROM baggage

            GROUP BY handling_status

        """)



        baggage_status = cursor.fetchall()



        # Fuel status

        cursor.execute("""

            SELECT

                fuel_status,

                COUNT(*) AS total

            FROM fuel_operations

            GROUP BY fuel_status

        """)



        fuel_status = cursor.fetchall()



        return render_template(

            "reports.html",

            total_flights=total_flights,

            total_gates=total_gates,

            total_staff=total_staff,

            total_baggage=total_baggage,

            total_fuel=total_fuel,

            active_allocations=active_allocations,

            flight_status=flight_status,

            baggage_status=baggage_status,

            fuel_status=fuel_status

        )



    except mysql.connector.Error as error:



        return f"Database Error: {error}"



    finally:



        if cursor:

            cursor.close()



        if connection:

            connection.close()





# ============================================================

# LOGOUT

# ============================================================


@app.route("/logout")
def logout():

    connection = None
    cursor = None

    try:
        login_history_id = session.get("login_history_id")
        user_id = session.get("user_id")

        # Debug messages to check session values
        print("Logout session:", dict(session))
        print("Logout IDs:", login_history_id, user_id)

        if login_history_id and user_id:
            connection = get_db_connection()
            cursor = connection.cursor()

            cursor.execute(
                """
                UPDATE login_history
                SET logout_time = NOW()
                WHERE login_id = %s
                  AND user_id = %s
                  AND logout_time IS NULL
                """,
                (login_history_id, user_id)
            )

            connection.commit()

            print("Logout rows updated:", cursor.rowcount)

    except mysql.connector.Error as error:
        print("Logout database error:", error)

        if connection:
            connection.rollback()

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()

    session.clear()

    return redirect(url_for("login"))

# ============================================================

# RUN APPLICATION

# ============================================================



if __name__ == "__main__":



    app.run(

        debug=True,

        host="127.0.0.1",

        port=5000

    )