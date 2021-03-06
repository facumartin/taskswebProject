import pymysql
from app import app
from db_config import mysql
from flask import Flask, render_template
from flask import jsonify, session, redirect, url_for,escape,request
from flask import flash, request
from werkzeug import generate_password_hash, check_password_hash


# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'



@app.route('/add', methods=['POST'])
def add_user():
	try:
		_json = request.json
		_name = _json['name']
		_email = _json['email']
		_password = _json['pwd']
        #_name = request.form["name"]
    	#_email = request.form["email"]
    	#_password = request.form.get("pwd")

		# validate the received values
		if _name and _email and _password and request.method == 'POST':
			#do not save password as a plain text
			_hashed_password = generate_password_hash(_password)
			# save edits
			sql = "INSERT INTO tbl_user(user_name, user_email, user_password) VALUES(%s, %s, %s)"
			data = (_name, _email, _hashed_password)
			#data = (str(session['username']), _email, _hashed_password)
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute(sql, data)
			conn.commit()
			resp = jsonify('User added successfully!')
			resp.status_code = 200
			return resp
		else:
			return not_found()
	except Exception as e:
		print(e)
	finally:
		cursor.close()
		conn.close()

@app.route('/users')
def users():
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM tbl_user")
		rows = cursor.fetchall()
		resp = jsonify(rows)
		print(resp)
		resp.status_code = 200
		return resp
        #return render_template('index.html')
	except Exception as e:
		print(e)
	finally:
		cursor.close()
		conn.close()

@app.route('/kanban', methods=['GET'])
def kanbanBoard():
	"""Render Homepage/Kanban board"""
	tasks = db.session.query(Task).filter(Task.username==session.get('username'))
	to_do, doing, done = [],[],[]
	tasks=[]
	for task in tasks:
	    if task.status == 'to_do':
	        to_do.append(task)
	    elif task.status == 'doing':
	        doing.append(task)
	    elif task.status == 'done':
	        done.append(task)
	return render_template('kanban.html', to_do=to_do, doing=doing, done=done, user=session.get('username'))

@app.route('/user/<id>')
def user(id):
	try:
		print(id)
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM tbl_user WHERE user_id=%s", id)
		row = cursor.fetchone()
		resp = jsonify(row)
		resp.status_code = 200
		return resp
	except Exception as e:
		print(e)
	finally:
		cursor.close()
		conn.close()



@app.route('/update', methods=['POST'])
def update_user():
	try:
		_json = request.json
		_id = _json['id']
		_name = _json['name']
		_email = _json['email']
		_password = _json['pwd']
		# validate the received values
		if _name and _email and _password and _id and request.method == 'POST':
			#do not save password as a plain text
			_hashed_password = generate_password_hash(_password)
			# save edits
			sql = "UPDATE tbl_user SET user_name=%s, user_email=%s, user_password=%s WHERE user_id=%s"
			data = (_name, _email, _hashed_password, _id,)
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute(sql, data)
			conn.commit()
			resp = jsonify('User updated successfully!')
			resp.status_code = 200
			return resp
		else:
			return not_found()
	except Exception as e:
		print(e)
	finally:
		cursor.close()
		conn.close()

@app.route('/delete/<id>')
def delete_user(id):
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute("DELETE FROM tbl_user WHERE user_id=%s", (id,))
		conn.commit()
		resp = jsonify('User deleted successfully!')
		resp.status_code = 200
		return resp
	except Exception as e:
		print(e)
	finally:
		cursor.close()
		conn.close()

@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp

if __name__ == "__main__":
    app.run()
