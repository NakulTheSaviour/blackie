from flask import Flask, jsonify, request
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# MySQL connection details
db_config = {
    'host': 'localhost',
    'database': 'nakuldb1',
    'user': 'root',
    'password': 'nakul'
}

def execute_query(query, data=None, fetch_all=False):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)

        if data:
            cursor.execute(query, data)
        else:
            cursor.execute(query)

        if fetch_all:
            result = cursor.fetchall()
        else:
            result = cursor.fetchone()

        return result

    except Error as e:
        print(f"Error: {e}")
        return None

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

@app.route('/current-week-leaderboard', methods=['GET'])
def current_week_leaderboard():
    print("Received request for current week leaderboard")
    query = "SELECT * FROM Player ORDER BY Score DESC LIMIT 200;"
    result = execute_query(query, fetch_all=True)
    print("Result:", result)
    return jsonify(result)

@app.route('/last-week-leaderboard/<country_code>', methods=['GET'])
def last_week_leaderboard(country_code):
    print("Received request for last week leaderboard")
    # country_code = request.args.get('country_code')

    # if not country_code:
    #     return jsonify({'error': 'Country code is required'}), 400

    query = f"SELECT * FROM Player WHERE Country = '{country_code}' ORDER BY Score DESC LIMIT 200;"
    result = execute_query(query, fetch_all=True)
    print("Result:", result)
    return jsonify(result)

@app.route('/user-rank/<user_id>', methods=['GET'])
# def user_rank(user_id):
#     # print("Received request for user rank")
#     # user_id = request.args.get('user_id')

#     # if not user_id:
#     #     return jsonify({'error': 'User ID is required'}), 400

#     query = f"SELECT UID, Name, Score, Country, TimeStamp, FIND_IN_SET(Score, (SELECT GROUP_CONCAT(Score ORDER BY Score DESC) FROM Player)) AS Rank FROM Player WHERE UID = '{user_id}';"
#     result = execute_query(query)
#     print("Result:", result)
#     return jsonify(result)

def user_rank(user_id):
    query = f"""
        SELECT
            UID,
            Name,
            Score,
            Country,
            TimeStamp,
            (SELECT COUNT(*) + 1 FROM Player AS p2 WHERE p2.Score > p1.Score) AS `Rank`
        FROM
            Player AS p1
        WHERE
            UID = '{user_id}';
    """
    result = execute_query(query)
    print("Result:", result)
    return jsonify(result)



if __name__ == '__main__':
    app.run(debug=True)
