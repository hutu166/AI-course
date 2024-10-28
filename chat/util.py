from flask import jsonify
import markdown
import time


def md_to_html(md_content):
    html_content = markdown.markdown(md_content)
    return html_content


def parse_csv_dataset(input):
    find_csv = False
    csv_filename = "./static/dataset-"+str(time.time()).replace(".", "") + ".csv"

    result = []
    dataset = []
    for row in input.split("\n"):
        if "Sample Dataset".lower() in row.lower():
            result.append(f"**Sample Dataset ({csv_filename})**\n")
            find_csv = True
        elif row.strip() == "```csv":
            result.append("==========================\n\n")
        elif row.strip() == "```":
            find_csv = False
            result.append("==========================\n")
        elif find_csv:
            result.append(row.strip() + "\n\n")
            if row.strip() != '':
                dataset.append(row.strip() + "\n")
        else:
            result.append(row+"\n")
    return (''.join(result), ''.join(dataset), csv_filename)


def success(data=''):
    return jsonify({
        "code": 0,
        "data": data
    })


def error(data=''):
    return jsonify({
        "code": -1,
        "data": data
    })
