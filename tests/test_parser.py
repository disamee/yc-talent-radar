from src.parser import extract_inertia_props, parse_company_details, extract_jobs_from_company

SAMPLE_HTML = '''
<!DOCTYPE html>
<html>
<body>
<div id="app" data-page="{&quot;component&quot;:&quot;jobs/public/pages/CompanyPage&quot;,&quot;props&quot;:{&quot;company&quot;:{&quot;name&quot;:&quot;Mason&quot;,&quot;slug&quot;:&quot;mason&quot;,&quot;batch&quot;:&quot;W16&quot;,&quot;url&quot;:&quot;http://www.bymason.com&quot;,&quot;founders&quot;:[{&quot;name&quot;:&quot;Jim Xiao&quot;}],&quot;jobs&quot;:[{&quot;id&quot;:13302,&quot;title&quot;:&quot;Software Engineer&quot;,&quot;roleType&quot;:&quot;Backend&quot;,&quot;jobType&quot;:&quot;Fulltime&quot;,&quot;location&quot;:&quot;Seattle, WA&quot;,&quot;salary&quot;:&quot;$80K - $140K&quot;}]}}}">
</div>
</body>
</html>
'''

def test_extract_inertia_props():
    props = extract_inertia_props(SAMPLE_HTML)
    assert "company" in props
    assert props["company"]["name"] == "Mason"

def test_parse_company_details():
    props = extract_inertia_props(SAMPLE_HTML)
    details = parse_company_details(props)
    assert details["name"] == "Mason"
    assert details["website"] == "http://www.bymason.com"
    assert len(details["founders"]) == 1
    assert details["founders"][0]["name"] == "Jim Xiao"

def test_extract_jobs_from_company():
    props = extract_inertia_props(SAMPLE_HTML)
    details = parse_company_details(props)
    jobs = extract_jobs_from_company(details, {"batch": "W16"})
    assert len(jobs) == 1
    assert jobs[0]["jobId"] == 13302
    assert jobs[0]["jobTitle"] == "Software Engineer"
    assert jobs[0]["company"]["name"] == "Mason"
    assert jobs[0]["salaryRange"] == "$80K - $140K"
