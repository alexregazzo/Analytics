from flask import Flask, render_template, request, Response
import json
import hashlib
import settings
import time
from database import Database

app = Flask(__name__)
logger = settings.logmaker(__name__)
logger.debug("Init")


@app.route('/tracker')
def tracker():
    with open("static/js/tracker.js") as f:
        return f.read()


@app.route('/tester')
def tracker():
    with open("static/js/tester.js") as f:
        return f.read()


@app.route('/test')
def test():
    return "Hi, its working"


@app.route('/')
def hello_world():
    return render_template("test.html")


@app.route("/track/", methods=["GET", "POST"])
def track_save():
    logger.debug("New request")
    start_request_time = time.time()
    try:
        logger.debug("Try decode data")
        data = json.loads(request.get_data().decode("UTF8"))
    except Exception as e:
        logger.info(f"Error reading data: {e}")
        logger.debug(request.get_data().decode("UTF8"))
    else:
        logger.debug("Data decoded")
        try:
            logger.debug("Getting hash from request")
            user_hash = request.args.get("hash", "")
            logger.debug(f"User: {user_hash}")
            logger.debug("Getting data from json")
            attempt = data["attempt"]
            location = data["location"]
            date = data["date"]
            ip = data["ip"]
            logger.debug("Request DB lock try")
            lock_start_request = time.time()
            with Database() as db:
                logger.debug("Request DB lock success")
                logger.debug(f"Lock timed: {time.time() - lock_start_request}")
                if user_hash == "":
                    # new user
                    logger.info("New user")
                    # get hash
                    logger.debug("Get new hash")
                    user_hash = get_new_hash(db)
                    logger.debug("Got new hash")
                    logger.debug("Insert on tables")
                    logger.debug("First start")
                    db.insert(
                        f"""INSERT INTO `track`(`tra_hash`, `tra_total_tries`, `tra_first_time`, `tra_last_time`, `tra_origin`, `tra_user_agent`, `tra_ip`) VALUES ('{user_hash}', '{attempt}', '{date}', '{date}', '{request.origin}', '{request.user_agent}', '{ip}');""")
                    logger.debug("First done")
                    logger.debug("Second start")
                    path_id = db.insert(f"""INSERT INTO `path`(`tra_hash`, `pat_href`, `pat_first_time`, `pat_last_time`) VALUES ('{user_hash}', '{location}', '{date}', '{date}');""")
                    logger.debug("Second done")
                    logger.debug("Third start")
                    db.update(f"""UPDATE `track` SET `pat_id_last`='{path_id}' WHERE `tra_hash` = '{user_hash}';""")
                    logger.debug("Third done")
                else:
                    # old user
                    logger.debug("Old user")
                    logger.debug("Select last hash and path")
                    tracks = db.select(f"""SELECT * FROM `track` WHERE `tra_hash`='{user_hash}';""")
                    if len(tracks) == 0:
                        # user does not exist
                        # user will reset and try again
                        logger.info("User tried, but wasn't found!")
                        return Response("", status=401)
                    track = tracks[0]
                    path = db.select(f"""SELECT * FROM `path` WHERE `pat_id`='{track["pat_id_last"]}';""")[0]
                    logger.debug("Select success")
                    if path["pat_href"] == location:
                        # same place as before
                        logger.debug("Same place start update")
                        db.update(f"""UPDATE `path` SET `pat_last_time`='{date}' WHERE `pat_id`='{path["pat_id"]}';""")
                        db.update(f"""UPDATE `track` SET `tra_total_tries`='{attempt}',`tra_last_time`='{date}', `tra_ip`='{ip}'  WHERE `tra_hash`='{user_hash}';""")
                        logger.debug("Same place finish update")
                    else:
                        # other location
                        logger.debug("Other place start update")
                        path_id = db.insert(f"""INSERT INTO `path`(`tra_hash`, `pat_href`, `pat_first_time`, `pat_last_time`) VALUES ('{user_hash}', '{location}', '{date}', '{date}');""")
                        db.update(f"""UPDATE `track` SET `tra_total_tries`='{attempt}',`tra_last_time`='{date}', `tra_ip`='{ip}', `pat_id_last`='{path_id}' WHERE `tra_hash`='{user_hash}';""")
                        logger.debug("Other place finish update")
        except Exception as e:
            logger.exception(e)
    finish_request_time = time.time()
    logger.debug(f"Responding request: {start_request_time} {finish_request_time} => {finish_request_time - start_request_time}")
    return Response(user_hash, status=200)


def get_new_hash(db: Database) -> str:
    new_hash = hashlib.sha256(bytes(str(time.time()), 'utf8')).hexdigest()
    results = db.select("SELECT * FROM `track`;")
    while any([new_hash == result["tra_hash"] for result in results]):
        new_hash = hashlib.sha256(bytes(str(time.time()), 'utf8')).hexdigest()
    return new_hash


@app.after_request
def apply_caching(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response


if __name__ == '__main__':
    if __name__ == "__main__":
        import platform

        if platform.system() == "Windows":
            app.run("127.0.0.1", port=5000, debug=True, ssl_context="adhoc")
            # app.run("127.0.0.4", port=5478, debug=True)
        elif platform.system() == "Linux":
            app.run(host='0.0.0.0', port=8888, ssl_context="adhoc")
