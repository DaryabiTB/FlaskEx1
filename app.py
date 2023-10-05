from flask import Flask, render_template, jsonify, abort, request
from sqlalchemy import text
from database import engine, load_jobs, get_job

app = Flask(__name__)


@app.route("/")
def hello_jovian():
    JOBS = load_jobs()
    return render_template('home.html',
                           jobs=JOBS,
                           company_name='Jovian')


@app.route("/api/jobs/<int:job_id>")
def job(job_id):
    job = get_job(job_id)
    if job is None:
        abort(404)
    else:
        return jsonify(job)

    # if job is None:
    #     abort(404)
    # else:
    #     return render_template('jobitem.html', job=job)


@app.route("/api/jobs")
def list_jobs():
    JOBS = load_jobs()
    return jsonify(JOBS)


@app.route("/job/<id>/apply", methods=['post'])
def apply_to_job(id):
    data = request.form
    job = get_job(id)
    add_application_to_db(id, data)
    return render_template('application_submitted.html',
                           application=data,
                           job=job)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
