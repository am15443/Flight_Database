from flask import Flask, render_template, request, jsonify
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

def get_db():
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )

@app.route("/", methods=["GET", "POST"])
def index():
    flights = []
    searched = False
    if request.method == "POST":
        orig = request.form["origin"].strip().upper()
        dest = request.form["dest"].strip().upper()
        date_from = request.form["date_from"].strip()
        date_to = request.form["date_to"].strip()
        try:
            conn = get_db()
            cur = conn.cursor()
            cur.execute("""
                SELECT f.flight_number, f.departure_date, fs.origin_code,
                       fs.dest_code, fs.departure_time, fs.airline_name, f.plane_type
                FROM Flight f
                JOIN FlightService fs USING (flight_number)
                WHERE TRIM(fs.origin_code) = %s AND TRIM(fs.dest_code) = %s
                  AND f.departure_date BETWEEN %s AND %s
                ORDER BY f.departure_date, f.flight_number
            """, (orig, dest, date_from, date_to))
            flights = cur.fetchall()
            conn.close()
        except Exception as e:
            print(f"DB ERROR: {e}")
        searched = True
    return render_template("index.html", flights=flights, searched=searched)

@app.route("/flight/<fn>/<date>")
def flight_detail(fn, date):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT ac.capacity,
               COUNT(b.pid) AS booked,
               ac.capacity - COUNT(b.pid) AS available
        FROM Flight f
        JOIN Aircraft ac USING (plane_type)
        LEFT JOIN Booking b USING (flight_number, departure_date)
        WHERE f.flight_number = %s AND f.departure_date = %s
        GROUP BY ac.capacity
    """, (fn, date))
    row = cur.fetchone()
    conn.close()
    return jsonify(capacity=row[0], booked=int(row[1]), available=int(row[2]))

if __name__ == "__main__":
    app.run(debug=True)
