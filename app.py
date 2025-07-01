from flask import jsonify
from flask import Flask, request, render_template_string, redirect
import base64  # 使用 base64 作示範，base62 需要額外安裝或自訂

app = Flask(__name__)

# 模擬資料庫
urls = {}
short_url = None 

# 使用 base64 替代 base62 進行簡單編碼（你可以用真正的 base62）
def shorten_url(url):
    encoded = base64.urlsafe_b64encode(url.encode()).decode()
    return encoded[:8]  # 簡化

# 首頁
@app.route('/')
def home():
    return 'Hello, Flask!'


@app.route('/form')
def form():
    return render_template_string('''
        <h2>縮網址服務</h2>
        <form id="urlForm">
            原始網址：<input name="url" id="urlInput">
            <input type="submit" value="縮短">
        </form>

        <div id="resultArea" style="margin-top: 1em;"></div>

        <script>
            document.getElementById("urlForm").addEventListener("submit", function (e) {
                e.preventDefault();  // 阻止表單預設送出
                const urlValue = document.getElementById("urlInput").value;

                fetch("/add_url", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/x-www-form-urlencoded"
                    },
                    body: "url=" + encodeURIComponent(urlValue)
                })
                .then(response => response.json())
                .then(data => {
                    const shortUrl = data.short_url;
                    const result = document.getElementById("resultArea");
                    result.innerHTML = `
                        <p><input type="text" value="${shortUrl}" style="display :none;" id="shortLink" readonly></p>
                    `;
                    const input = document.getElementById("shortLink");
                    input.select();
                    navigator.clipboard.writeText(input.value).then(() => {
                        alert("已自動複製：" + input.value);
                    }).catch(err => {
                        alert("複製失敗：" + err);
                    });
                });
            });
        </script>
    ''')



@app.route('/add_url', methods=['POST'])
def add_url():
    url = request.form['url']
    short = shorten_url(url)
    urls[short] = url
    short_full = request.host_url + short
    return jsonify({'short_url': short_full})

# 查詢原網址（GET）

@app.route('/<short_code>')
def redirect_to_external(short_code):
    if short_code in urls:
        org_url = urls[short_code]
        return redirect(org_url)
    else:
        return "Short URL not found", 404

if __name__ == '__main__':
    app.run(debug=True)
