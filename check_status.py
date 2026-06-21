import pymysql
import json

DB_HOST = "127.0.0.1"
DB_USER = "db_username"
DB_PASS = "db_password"
DB_NAME = "log4om2"

def check_status():
    conn = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )
    
    try:
        with conn.cursor() as cursor:
            print("\n--- Last 50 QSOs LOTW Status ---")
            
            # Fetch the last 50 entries
            sql = "SELECT qsoid, callsign, qsodate, qsoconfirmations FROM log ORDER BY qsodate DESC LIMIT 50"
            cursor.execute(sql)
            results = cursor.fetchall()
            
            if not results:
                print("No records found.")
                return

            table_data = []
            for row in results:
                call_val = row.get('callsign', '')
                date_val = row.get('qsodate', '')
                time_val = ''
                
                # Extract time from datetime if possible
                if date_val:
                    try:
                        time_val = date_val.strftime('%H:%M:%S')
                        date_val = date_val.strftime('%Y-%m-%d')
                    except AttributeError:
                        # Fallback if it's stored as a string
                        parts = str(date_val).split()
                        if len(parts) > 1:
                            date_val = parts[0]
                            time_val = parts[1]
                
                # Parse JSON to find LOTW status
                lotw_status = "Unknown"
                lotw_date = ""
                conf_str = row.get('qsoconfirmations')
                if conf_str:
                    try:
                        confs = json.loads(conf_str)
                        for c in confs:
                            if c.get("CT") == "LOTW":
                                lotw_status = c.get("S", "No")
                                lotw_date = c.get("SD", "")
                                break
                    except json.JSONDecodeError:
                        lotw_status = "Parse Error"
                
                table_data.append([
                    call_val,
                    date_val,
                    time_val,
                    lotw_status,
                    lotw_date
                ])
                
            headers = ["Callsign", "Date", "Time", "LOTW Sent", "Sent Date"]
            
            col_widths = [max(len(str(item)) for item in col) for col in zip(headers, *table_data)]
            format_str = " | ".join([f"{{:<{w}}}" for w in col_widths])
            
            print(format_str.format(*headers))
            print("-" * (sum(col_widths) + len(headers) * 3 - 1))
            for row in table_data:
                print(format_str.format(*[str(item) for item in row]))
                
    finally:
        conn.close()

if __name__ == "__main__":
    check_status()
