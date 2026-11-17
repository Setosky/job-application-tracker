
from flask import Flask, render_template, request, redirect, url_for
from database import get_db
import json

app = Flask(__name__)


# DASHBOARD

@app.route("/")
def dashboard():
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT COUNT(*) AS total FROM companies")
    company_count = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) AS total FROM jobs")
    job_count = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) AS total FROM applications")
    application_count = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) AS total FROM contacts")
    contact_count = cursor.fetchone()["total"]

    cursor.close()
    db.close()

    return render_template(
        "dashboard.html",
        company_count=company_count,
        job_count=job_count,
        application_count=application_count,
        contact_count=contact_count
    )



# DISPLAY COMPANIES
@app.route("/companies")
def companies():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM companies ORDER BY company_name")
    company_list = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("companies.html", companies=company_list)


# ADD COMPANY
@app.route("/companies/new", methods=["GET", "POST"])
def add_company():
    if request.method == "POST":
        company_name = request.form["company_name"].strip()

        if not company_name:
            return "Company name is required.", 400

        conn = get_db()
        cursor = conn.cursor()

        sql = """
            INSERT INTO companies
            (company_name, industry, website, city, state, notes)
            VALUES (%s, %s, %s, %s, %s, %s)
        """

        values = (
            company_name,
            request.form.get("industry") or None,
            request.form.get("website") or None,
            request.form.get("city") or None,
            request.form.get("state") or None,
            request.form.get("notes") or None
        )

        cursor.execute(sql, values)
        conn.commit()

        cursor.close()
        conn.close()

        return redirect(url_for("companies"))

    return render_template("company_form.html", company=None, action="Add")


# EDIT COMPANY
@app.route("/companies/edit/<int:company_id>", methods=["GET", "POST"])
def edit_company(company_id):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":
        company_name = request.form["company_name"].strip()

        if not company_name:
            cursor.close()
            conn.close()
            return "Company name is required.", 400

        sql = """
            UPDATE companies
            SET company_name=%s, industry=%s, website=%s,
                city=%s, state=%s, notes=%s
            WHERE company_id=%s
        """

        values = (
            company_name,
            request.form.get("industry") or None,
            request.form.get("website") or None,
            request.form.get("city") or None,
            request.form.get("state") or None,
            request.form.get("notes") or None,
            company_id
        )

        cursor.execute(sql, values)
        conn.commit()

        cursor.close()
        conn.close()

        return redirect(url_for("companies"))

    cursor.execute(
        "SELECT * FROM companies WHERE company_id = %s",
        (company_id,)
    )
    company = cursor.fetchone()

    cursor.close()
    conn.close()

    if not company:
        return "Company not found.", 404

    return render_template(
        "company_form.html",
        company=company,
        action="Edit"
    )


# DELETE COMPANY
@app.route("/companies/delete/<int:company_id>", methods=["POST"])
def delete_company(company_id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM companies WHERE company_id = %s",
        (company_id,)
    )

    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for("companies"))


# DISPLAY JOBS
@app.route("/jobs")
def jobs():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT jobs.*, companies.company_name
        FROM jobs
        JOIN companies ON jobs.company_id = companies.company_id
    """)

    job_list = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("jobs.html", jobs=job_list)


# ADD JOB
@app.route("/jobs/new", methods=["GET", "POST"])
def add_job():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":
        requirements = request.form.get("requirements", "")
        requirements_json = json.dumps(
            [s.strip() for s in requirements.split(",") if s.strip()]
        )

        cursor.execute("""
            INSERT INTO jobs
            (company_id, job_title, job_type, salary_min, salary_max,
             job_url, date_posted, requirements)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            request.form["company_id"],
            request.form["job_title"],
            request.form["job_type"],
            request.form.get("salary_min") or None,
            request.form.get("salary_max") or None,
            request.form.get("job_url") or None,
            request.form.get("date_posted") or None,
            requirements_json
        ))

        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for("jobs"))

    cursor.execute("SELECT * FROM companies")
    company_list = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "job_form.html",
        job=None,
        companies=company_list
    )


# EDIT JOB
@app.route("/jobs/edit/<int:job_id>", methods=["GET", "POST"])
def edit_job(job_id):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":
        requirements = request.form.get("requirements", "")
        requirements_json = json.dumps(
            [s.strip() for s in requirements.split(",") if s.strip()]
        )

        cursor.execute("""
            UPDATE jobs
            SET company_id=%s, job_title=%s, job_type=%s,
                salary_min=%s, salary_max=%s, job_url=%s,
                date_posted=%s, requirements=%s
            WHERE job_id=%s
        """, (
            request.form["company_id"],
            request.form["job_title"],
            request.form["job_type"],
            request.form.get("salary_min") or None,
            request.form.get("salary_max") or None,
            request.form.get("job_url") or None,
            request.form.get("date_posted") or None,
            requirements_json,
            job_id
        ))

        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for("jobs"))

    cursor.execute(
        "SELECT * FROM jobs WHERE job_id=%s",
        (job_id,)
    )
    job = cursor.fetchone()

    cursor.execute("SELECT * FROM companies")
    company_list = cursor.fetchall()

    if job and isinstance(job["requirements"], (dict, list)):
        job["requirements"] = ", ".join(job["requirements"])

    cursor.close()
    conn.close()

    return render_template(
        "job_form.html",
        job=job,
        companies=company_list
    )


# DELETE JOB
@app.route("/jobs/delete/<int:job_id>", methods=["POST"])
def delete_job(job_id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM jobs WHERE job_id=%s",
        (job_id,)
    )

    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for("jobs"))


# DISPLAY APPLICATIONS
@app.route("/applications")
def applications():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT applications.*, jobs.job_title, companies.company_name
        FROM applications
        JOIN jobs ON applications.job_id = jobs.job_id
        JOIN companies ON jobs.company_id = companies.company_id
        ORDER BY applications.application_date DESC
    """)

    application_list = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("applications.html", applications=application_list)


# ADD APPLICATION
@app.route("/applications/new", methods=["GET", "POST"])
def add_application():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":
        interview_data = request.form.get("interview_data", "")

        cursor.execute("""
            INSERT INTO applications
            (job_id, application_date, status, resume_version,
             cover_letter_sent, interview_data)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            request.form["job_id"],
            request.form["application_date"],
            request.form["status"],
            request.form.get("resume_version") or None,
            request.form["cover_letter_sent"],
            json.dumps({"notes": interview_data})
        ))

        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for("applications"))

    cursor.execute("""
        SELECT jobs.job_id, jobs.job_title, companies.company_name
        FROM jobs
        JOIN companies ON jobs.company_id = companies.company_id
    """)

    job_list = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "application_form.html",
        application=None,
        jobs=job_list
    )


# EDIT APPLICATION
@app.route("/applications/edit/<int:application_id>", methods=["GET", "POST"])
def edit_application(application_id):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":
        interview_data = request.form.get("interview_data", "")

        cursor.execute("""
            UPDATE applications
            SET job_id=%s, application_date=%s, status=%s,
                resume_version=%s, cover_letter_sent=%s, interview_data=%s
            WHERE application_id=%s
        """, (
            request.form["job_id"],
            request.form["application_date"],
            request.form["status"],
            request.form.get("resume_version") or None,
            request.form["cover_letter_sent"],
            json.dumps({"notes": interview_data}),
            application_id
        ))

        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for("applications"))

    cursor.execute(
        "SELECT * FROM applications WHERE application_id=%s",
        (application_id,)
    )
    application = cursor.fetchone()

    cursor.execute("""
        SELECT jobs.job_id, jobs.job_title, companies.company_name
        FROM jobs
        JOIN companies ON jobs.company_id = companies.company_id
    """)

    job_list = cursor.fetchall()

    if application and application["interview_data"]:
        data = application["interview_data"]

        if isinstance(data, str):
            data = json.loads(data)

        application["interview_data"] = data.get("notes", "")

    cursor.close()
    conn.close()

    return render_template(
        "application_form.html",
        application=application,
        jobs=job_list
    )


# DELETE APPLICATION
@app.route("/applications/delete/<int:application_id>", methods=["POST"])
def delete_application(application_id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM applications WHERE application_id=%s",
        (application_id,)
    )

    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for("applications"))



@app.route("/contacts")
def contacts():
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT contacts.*, companies.company_name
        FROM contacts
        JOIN companies ON contacts.company_id = companies.company_id
        ORDER BY contacts.contact_id DESC
    """)

    contacts_list = cursor.fetchall()
    cursor.close()
    db.close()

    return render_template("contacts.html", contacts=contacts_list)


@app.route("/contacts/new", methods=["GET", "POST"])
def new_contact():
    db = get_db()
    cursor = db.cursor(dictionary=True)

    if request.method == "POST":
        cursor.execute("""
            INSERT INTO contacts
            (company_id, contact_name, title, email, phone, linkedin_url, notes)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            request.form["company_id"],
            request.form["contact_name"],
            request.form["title"],
            request.form["email"],
            request.form["phone"],
            request.form["linkedin_url"],
            request.form["notes"]
        ))

        db.commit()
        cursor.close()
        db.close()
        return redirect(url_for("contacts"))

    cursor.execute("SELECT * FROM companies ORDER BY company_name")
    companies = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template("contact_form.html", companies=companies, contact=None)


@app.route("/contacts/edit/<int:contact_id>", methods=["GET", "POST"])
def edit_contact(contact_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)

    if request.method == "POST":
        cursor.execute("""
            UPDATE contacts
            SET company_id=%s, contact_name=%s, title=%s, email=%s,
                phone=%s, linkedin_url=%s, notes=%s
            WHERE contact_id=%s
        """, (
            request.form["company_id"],
            request.form["contact_name"],
            request.form["title"],
            request.form["email"],
            request.form["phone"],
            request.form["linkedin_url"],
            request.form["notes"],
            contact_id
        ))

        db.commit()
        cursor.close()
        db.close()
        return redirect(url_for("contacts"))

    cursor.execute(
        "SELECT * FROM contacts WHERE contact_id = %s",
        (contact_id,)
    )
    contact = cursor.fetchone()

    cursor.execute("SELECT * FROM companies ORDER BY company_name")
    companies = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template(
        "contact_form.html",
        companies=companies,
        contact=contact
    )


@app.route("/contacts/delete/<int:contact_id>")
def delete_contact(contact_id):
    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        "DELETE FROM contacts WHERE contact_id = %s",
        (contact_id,)
    )

    db.commit()
    cursor.close()
    db.close()

    return redirect(url_for("contacts"))


@app.route("/job-match", methods=["GET", "POST"])
def job_match():
    results = []
    skills_text = ""
    searched = False

    if request.method == "POST":
        skills_text = request.form.get("skills", "")
        searched = True

        user_skills = [
            skill.strip().lower()
            for skill in skills_text.split(",")
            if skill.strip()
        ]

        db = get_db()
        cursor = db.cursor(dictionary=True)

        cursor.execute("""
            SELECT jobs.job_id, jobs.job_title, jobs.requirements,
                   companies.company_name
            FROM jobs
            JOIN companies ON jobs.company_id = companies.company_id
        """)

        jobs = cursor.fetchall()

        for job in jobs:
            requirements = job["requirements"]

            if isinstance(requirements, str):
                requirements = json.loads(requirements)

            if isinstance(requirements, dict):
                required_skills = requirements.get("skills", [])
            elif isinstance(requirements, list):
                required_skills = requirements
            else:
                required_skills = []

            required_skills = [
                skill.strip().lower()
                for skill in required_skills
                if isinstance(skill, str)
            ]

            if required_skills:
                matched = [
                    skill for skill in required_skills
                    if any(
                        skill in user_skill or user_skill in skill
                        for user_skill in user_skills
                    )
                ]

                percentage = round(
                    len(matched) / len(required_skills) * 100
                )

                results.append({
                    "job_title": job["job_title"],
                    "company_name": job["company_name"],
                    "match_percentage": percentage,
                    "matched_skills": ", ".join(matched) if matched else "None"
                })

        cursor.close()
        db.close()

        results.sort(
            key=lambda job: job["match_percentage"],
            reverse=True
        )

    return render_template(
        "job_match.html",
        results=results,
        skills_text=skills_text,
        searched=searched
    )


if __name__ == "__main__":
    app.run(debug=True)
