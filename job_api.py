from flask import Flask, request, jsonify
from jobspy import scrape_jobs
import traceback

app = Flask(__name__)

@app.route('/api/jobs', methods=['GET'])
def get_jobs():
    title = request.args.get('title', 'Engineer')
    location = request.args.get('location', 'Saudi Arabia')
    
    try:
        # حذفنا glassdoor من هنا عشان ميضربش السيرفر في الدول العربية
        # كده السيرفر هيسحب إنديد ولينكد إن بنجاح تام وبدون أي أخطاء
        jobs = scrape_jobs(
            site_name=["indeed", "linkedin"],
            search_term=title,
            location=location,
            results_wanted=50, # هيسحب 50 وظيفة من كل موقع
            country_indeed='Saudi Arabia' if 'Saudi Arabia' in location or 'السعودية' in location else 'Egypt'
        )
        
        jobs_list = []
        if not jobs.empty:
            for index, row in jobs.iterrows():
                jobs_list.append({
                    "title": str(row.get("title", "وظيفة")),
                    "company": str(row.get("company", "جهة غير محددة")),
                    "location": str(row.get("location", location)),
                    "site": str(row.get("site", "منصة عالمية")),
                    "date_posted": str(row.get("date_posted", "حديث")),
                    "job_url": str(row.get("job_url", ""))
                })
                
        return jsonify({"status": "success", "jobs": jobs_list, "total": len(jobs_list)})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e), "trace": traceback.format_exc()})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
