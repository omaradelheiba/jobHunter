from flask import Flask, request, jsonify
from jobspy import scrape_jobs

app = Flask(__name__)

@app.route('/api/jobs', methods=['GET'])
def get_jobs():
    title = request.args.get('title')
    location = request.args.get('location')
    country = request.args.get('country')
    
    try:
        jobs = scrape_jobs(
            site_name=["linkedin", "indeed", "glassdoor", "google"],
            search_term=title,
            location=location,
            results_wanted=15,
            hours_old=720,
            country_indeed=country
        )
        
        if not jobs.empty:
            jobs_list = jobs.fillna("غير محدد").to_dict('records')
            return jsonify({'status': 'success', 'jobs': jobs_list})
        else:
            return jsonify({'status': 'success', 'jobs': []})
            
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})