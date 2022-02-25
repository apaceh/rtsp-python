from flask import Flask, render_template, Response, request, redirect, url_for, session
import cv2 as cv
from flask_mysqldb import MySQL
import MySQLdb.cursors
import bcrypt
import time

app = Flask(__name__)

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = '1a2b3c4d5e'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'kamera'

mysql = MySQL(app)

cameras = []


def connect_camera():
    mycursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    mycursor.execute("SELECT * FROM cctv LIMIT 2")
    myresult = mycursor.fetchall()

    index = []
    cam = []
    for row in myresult:
        source = "rtsp://" + row['username'] + ":" + row['password'] + "@" + \
            row['ip_address'] + ":" + row['port'] + "/mode=real&idc=1&ids=1"
        arr = {}

        arr['status'] = True
        arr['source'] = source
        arr['lokasi'] = row['lokasi_kamera']
        arr['is_webcame'] = row['is_webcame']
        cam.append(arr)
        index.append(row['no'])

    global cameras
    cameras = cam

    return index


def gen_frames(index):  # generate frame by frame from camera
    i = int(index)
    source = cameras[i]['source']
    lokasi = cameras[i]['lokasi']

    if cameras[i]['is_webcame'] == 1:
        cap = cv.VideoCapture(0)
    else:
        cap = cv.VideoCapture(source)

    # used to record the time when we processed last frame
    prev_frame_time = 0

    # used to record the time at which we processed current frame
    new_frame_time = 0

    while(cap.isOpened()):
        # Capture frame-by-frame
        # read the camera frame
        success, frame = cap.read()
        if not success:
            break
        else:
            # fps = cap.get(cv.CAP_PROP_FPS)

            cap_width = cap.get(cv.CAP_PROP_FRAME_WIDTH)
            cap_height = cap.get(cv.CAP_PROP_FRAME_HEIGHT)
            cv.putText(frame, lokasi + ' (' + str(cap_width) + 'x' + str(cap_height) + ')', (10, 30),
                       cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2, cv.LINE_AA)

            # time when we finish processing for this frame
            new_frame_time = time.time()
            fps = 1 / (new_frame_time-prev_frame_time)
            prev_frame_time = new_frame_time

            # converting the fps into integer
            fps = int(fps)
            cv.putText(frame, 'FPS : ' + str(fps), (10, 60),
                       cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2, cv.LINE_AA)

            ret, buffer = cv.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result

            key = cv.waitKey(1)
            if (key == 27):
                break

    # When everything done, release the capture
    cap.release()
    cv.destroyAllWindows()


@app.route('/video_feed/<string:index>/', methods=["GET"])
def video_feed(index):
    return Response(gen_frames(index), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if 'loggedin' not in session:
        # Output message if something goes wrong...
        msg = ''
        # Check if "username" and "password" POST requests exist (user submitted form)
        if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
            # Create variables for easy access
            username = request.form['username']
            password = request.form['password']
            # Check if account exists using MySQL
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(
                "SELECT * FROM user WHERE username = '" + username + "'")
            # Fetch one record and return result
            account = cursor.fetchone()
            # If account exists in accounts table in out database
            if account:
                cekPassword = bcrypt.checkpw(password.encode('utf8'),
                                             account['password'].encode('utf8'))

                if cekPassword:
                    # Create session data, we can access this data in other routes
                    session['loggedin'] = True
                    session['id'] = str(account['id'])
                    session['username'] = account['username']
                    session['level'] = str(account['level'])
                    # Redirect to home page
                    return redirect(url_for('home'))
                else:
                    msg = 'Salah password!'
            else:
                # Account doesnt exist or username incorrect
                msg = 'Salah username!'
        return render_template('index.html', msg=msg)
    else:
        return redirect(url_for('home'))


@app.route('/logout')
def logout():
    session.pop('username')
    session.pop('loggedin')
    session.pop('id')
    return redirect(url_for('login'))


@app.route('/list_kamera')
def list_kamera():
    if 'loggedin' in session:
        mycursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        mycursor.execute("SELECT * FROM cctv")
        list_kamera = mycursor.fetchall()

        return render_template('list_kamera.html', list_kamera=list_kamera, level=session['level'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@app.route('/tambah_kamera', methods=["POST"])
def tambah_kamera():
    lokasi_kamera = request.form['lokasi_kamera']
    ip_address = request.form['ip_address']
    username = request.form['username']
    password = request.form['password']
    port = request.form['port']

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO `cctv` (`lokasi_kamera`, `ip_address`, `username`, `password`, `port`) VALUES ('" +
                lokasi_kamera + "', '" + ip_address + "', '" + username + "', '" + password + "', '" + port + "') ")
    mysql.connection.commit()
    return redirect(url_for('list_kamera'))


@app.route('/edit_kamera/<string:id_kamera>/', methods=["GET"])
def edit_kamera(id_kamera):
    if 'loggedin' in session:
        mycursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        mycursor.execute("SELECT * FROM cctv WHERE no = '" + id_kamera + "'")
        kamera = mycursor.fetchone()

        return render_template('edit_kamera.html', kamera=kamera, level=session['level'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@app.route('/update_kamera', methods=["POST"])
def update_kamera():
    no = request.form['no']
    lokasi_kamera = request.form['lokasi_kamera']
    ip_address = request.form['ip_address']
    username = request.form['username']
    password = request.form['password']
    port = request.form['port']

    cur = mysql.connection.cursor()
    cur.execute("UPDATE `cctv` SET `lokasi_kamera`='" + lokasi_kamera + "',`ip_address`='" + ip_address +
                "',`username`='" + username + "',`password`='" + password + "',`port`='" + port + "' WHERE no = '" + no + "'")
    mysql.connection.commit()
    return redirect(url_for('list_kamera'))


@app.route('/hapus_kamera/<string:id_kamera>', methods=["GET"])
def hapus_kamera(id_kamera):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM cctv WHERE no=%s", (id_kamera,))
    mysql.connection.commit()
    return redirect(url_for('list_kamera'))


@app.route('/users')
def users():
    if 'loggedin' in session:
        mycursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        mycursor.execute("SELECT * FROM user")
        users = mycursor.fetchall()

        return render_template('users.html', users=users, level=session['level'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@app.route('/tambah_user', methods=["POST"])
def tambah_user():
    username = str(request.form['username'])
    password = str(request.form['password'])
    level = str(request.form['level'])

    salt = bcrypt.gensalt()
    pass_hashed = bcrypt.hashpw(password.encode('utf-8'), salt)

    cur = mysql.connection.cursor()
    sql = "INSERT INTO `user` (`username`, `password`, `level`) VALUES ('" + \
        username + "', '" + pass_hashed.decode('utf-8') + "', '" + level + "')"
    cur.execute(sql)
    mysql.connection.commit()
    return redirect(url_for('users'))


@app.route('/edit_user/<string:id_user>/', methods=["GET"])
def edit_user(id_user):
    if 'loggedin' in session:
        mycursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        mycursor.execute("SELECT * FROM user WHERE id = '" + id_user + "'")
        user = mycursor.fetchone()

        return render_template('users_edit.html', user=user, level=session['level'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@app.route('/update_user', methods=["POST"])
def update_user():
    id_user = request.form['id_user']
    username = request.form['username']
    password = request.form['password']
    level = request.form['level']

    cur = mysql.connection.cursor()

    if(password == ""):
        cur.execute("UPDATE `user` SET `username`='" + username +
                    "', `level`='" + level + "' WHERE id = '" + id_user + "'")
    else:
        salt = bcrypt.gensalt()
        pass_hashed = bcrypt.hashpw(password.encode('utf-8'), salt)

        cur.execute("UPDATE `user` SET `username`='" + username + "', `password`='" +
                    pass_hashed.decode('utf-8') + "', `level`='" + level + "' WHERE id = '" + id_user + "'")

    mysql.connection.commit()
    return redirect(url_for('users'))


@app.route('/hapus_user/<string:id_user>', methods=["GET"])
def hapus_user(id_user):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM user WHERE id=%s", (id_user))
    mysql.connection.commit()
    return redirect(url_for('users'))


@app.route('/home')
def home():
    # Check if user is loggedin
    if 'loggedin' in session:
        list_camera = connect_camera()

        # User is loggedin show them the home page
        return render_template('home.html', camera_list=len(list_camera), cameras=cameras, level=session['level'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    # app.run(host='0.0.0.0')
    app.run(debug=True)
