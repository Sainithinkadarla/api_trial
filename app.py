from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)


GITHUB_USERNAME = "Sainithinkadarla"
GITHUB_TOKEN = "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"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/repo_info', methods=['POST'])
def repo_info():
    repo_name = request.form['repo_name']
    url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{repo_name}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        repo_data = response.json()
        return jsonify({
            "name": repo_data['name'],
            "description": repo_data['description'],
            "stars": repo_data['stargazers_count'],
            "forks": repo_data['forks_count']
        })
    else:
        return jsonify({"error": f"Failed to fetch data: {response.status_code}"}), response.status_code

@app.route('/list_issues', methods=['POST'])
def list_issues():
    repo_name = request.form['repo_name']
    url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{repo_name}/issues"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        issues = response.json()
        issue_list = [{"title": issue['title'], "url": issue['html_url']} for issue in issues]
        return jsonify(issue_list)
    else:
        return jsonify({"error": f"Failed to fetch issues: {response.status_code}"}), response.status_code

if __name__ == '__main__':
    app.run(debug=True)
