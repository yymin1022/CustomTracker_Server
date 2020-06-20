from flask import Flask

app = Flask(__name__)

apiKey = "d240g270y083v227e030m080h1"
unipassUrl = str.format("https://unipass.customs.go.kr:38010/ext/rest/cargCsclPrgsInfoQry/retrieveCargCsclPrgsInfo?crkyCn={0}&blYy=2020&hblNo=6077876695710", apiKey)


@app.route('/')
def hello_world():
    return unipassUrl


if __name__ == '__main__':
    app.run()