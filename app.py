from flask import Flask,request,render_template,url_for,redirect
from config import client
from datetime import datetime
from flask_paginate import get_page_parameter,Pagination
app = Flask(__name__)


@app.route('/search/<keyword>/',methods=['GET'])
def search(keyword):
    page = request.args.get(get_page_parameter(), type=int, default=1)

    start_time = datetime.now()
    response = client.search(
        index="sgk",
        body={
            "query": {
                "multi_match": {
                    "query": keyword,
                    "fields": ["file", "data", "from"]
                }
            },
            "from": 1,
            "size": 1000,
            "highlight": {
                "pre_tags": ['<span class="keyword">'],
                "post_tags": ['/span'],
                "fields": {
                    "title": {},
                    "content": {},
                }
            }
        },
        request_timeout=360000
    )
    end_time = datetime.now()
    last_seconds = (end_time - start_time).total_seconds()
    total_nums = response["hits"]["total"]
    hit_list = []

    for hit in response["hits"]["hits"]:
        hit_dict = {}
        if "highlight" in hit:
            if "data" in hit["highlight"]:
                hit_dict["data"] = "".join(hit["highlight"]["data"])
            else:
                hit_dict["data"] = hit["_source"]["data"]
        else:
            hit_dict["data"] = hit["_source"]["data"]
            hit_dict["file"] = hit["_source"]["file"]
            hit_dict["from"] = hit["_source"]["from"]
            hit_dict["score"] = hit["_score"]
        hit_list.append(hit_dict)
    pagenation = Pagination(bs_version=3,page=page,total=total_nums,outer_window=1,inner_window=2)
    context = {
        'hit_list' : hit_list,
        'total_nums' : total_nums,
        'last_seconds' : last_seconds,
        'pagenation' : pagenation
    }
    return render_template("result.html", **context)


@app.route('/', methods=['GET', 'POST'])
def hello_world():

    if request.method == "POST":
        keyword = request.form['q']
        return redirect(url_for('search', keyword=keyword))
    else:
        return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
