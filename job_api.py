import traceback
import json
from flask import Flask, request, Response

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return "Job Hunter API is Running successfully for ALL Countries!"

@app.route('/api/jobs', methods=['GET'])
def get_jobs():
    try:
        from jobspy import scrape_jobs
        import pandas as pd
        
        title = request.args.get('title', 'Engineer')
        location = request.args.get('location', 'Saudi Arabia')
        
        loc_lower = location.lower()
        
        # ================= خوارزمية تحديد الدولة بناءً على المدينة =================
        egypt_cities = ['egypt', 'مصر', 'cairo', 'alexandria', 'giza', 'qalyubia', 'sharqia', 'dakahlia', 'gharbia', 'monufia', 'kafr el sheikh', 'beheira', 'damietta', 'ismailia', 'port said', 'suez', 'matrouh', 'sinai', 'red sea', 'new valley', 'faiyum', 'beni suef', 'minya', 'asyut', 'sohag', 'qena', 'luxor', 'aswan']
        
        uae_cities = ['united arab emirates', 'uae', 'الإمارات', 'abu dhabi', 'dubai', 'sharjah', 'ajman', 'umm al quwain', 'ras al khaimah', 'fujairah', 'al ain', 'al dhafra']
        
        kuwait_cities = ['kuwait', 'الكويت', 'al asimah', 'hawalli', 'al farwaniyah', 'mubarak al-kabeer', 'al ahmadi', 'al jahra']
        
        qatar_cities = ['qatar', 'قطر', 'doha', 'al rayyan', 'al wakrah', 'umm salal', 'al khor', 'al shamal', 'al daayen', 'al-shahaniya']
        
        iraq_cities = ['iraq', 'العراق', 'baghdad', 'basra', 'nineveh', 'erbil', 'sulaymaniyah', 'duhok', 'kirkuk', 'diyala', 'al anbar', 'babil', 'karbala', 'najaf', 'al-qādisiyyah', 'muthanna', 'dhi قار', 'maysan', 'wasit', 'saladin']

        if any(city in loc_lower for city in egypt_cities):
            country_val = 'egypt'
        elif any(city in loc_lower for city in uae_cities):
            country_val = 'united arab emirates'
        elif any(city in loc_lower for city in kuwait_cities):
            country_val = 'kuwait'
        elif any(city in loc_lower for city in qatar_cities):
            country_val = 'qatar'
        elif any(city in loc_lower for city in iraq_cities):
            country_val = 'iraq'
        else:
            country_val = 'saudi arabia'
        # =========================================================================

        jobs = scrape_jobs(
            site_name=["indeed"],
            search_term=title,
            location=location,
            results_wanted=80,
            hours_old=720,
            country_indeed=country_val
        )
        
        jobs_list = []
        if jobs is not None and type(jobs) == pd.DataFrame and not jobs.empty:
            jobs = jobs.fillna("غير محدد")
            for _, row in jobs.iterrows():
                jobs_list.append({
                    "title": str(row.get("title", "وظيفة")),
                    "company": str(row.get("company", "جهة عمل")),
                    "location": str(row.get("location", location)),
                    "site": str(row.get("site", "منصة")),
                    "date_posted": str(row.get("date_posted", "حديث")),
                    "job_url": str(row.get("job_url", ""))
                })
                
        resp_json = json.dumps({"status": "success", "jobs": jobs_list, "total": len(jobs_list)}, ensure_ascii=False)
        return Response(resp_json, mimetype='application/json; charset=utf-8')

    except Exception as e:
        error_json = json.dumps({"status": "error", "message": str(e), "trace": traceback.format_exc()}, ensure_ascii=False)
        return Response(error_json, mimetype='application/json; charset=utf-8')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
