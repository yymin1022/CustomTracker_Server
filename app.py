from datetime import datetime
from flask import Flask
from flask import request
from urllib.request import urlopen
from xml.etree import ElementTree

app = Flask(__name__)

apiKey = "d240g270y083v227e030m080h1"
defaultUrl = "https://unipass.customs.go.kr:38010" \
             "/ext/rest/cargCsclPrgsInfoQry/retrieveCargCsclPrgsInfo?" \
             "crkyCn={0}&blYy={2}&hblNo={1}"


@app.route('/getParcelInfo')
def getParcelInfo():
    parcelInfoResult = ""

    trackNum = request.args.get("trackNum", 00000000)
    parcelYear = request.args.get("parcelYear", datetime.today().year)
    unipassUrl = str.format(defaultUrl, apiKey, trackNum, parcelYear)

    unipassResponce = urlopen(unipassUrl).read()
    rootElement = ElementTree.fromstring(unipassResponce)

    parcelInfoElement = rootElement.iter(tag="cargCsclPrgsInfoQryVo")
    for parcelInfo in parcelInfoElement:
        parcelInfoStr = str(parcelInfo.find("prnm").text) + "\n" + \
                        str(parcelInfo.find("etprCstm").text) + "\n" + \
                        str(parcelInfo.find("ttwg").text)
        parcelInfoResult = parcelInfoStr

    return parcelInfoResult

@app.route('/getTrackInfo')
def hello_world():
    trackInfoResult = ""
    trackNum = request.args.get("trackNum", 00000000)
    parcelYear = request.args.get("parcelYear", datetime.today().year)
    unipassUrl = str.format(defaultUrl, apiKey, trackNum, parcelYear)

    unipassResponce = urlopen(unipassUrl).read()
    rootElement = ElementTree.fromstring(unipassResponce)

    trackInfoElement = rootElement.iter(tag="cargCsclPrgsInfoDtlQryVo")

    for trackInfo in trackInfoElement:
        trackInfoStr = str(trackInfo.find("prcsDttm").text) + " : " + \
                       str(trackInfo.find("cargTrcnRelaBsopTpcd").text)
        trackInfoResult = trackInfoResult + trackInfoStr + "\n"

    return trackInfoResult


if __name__ == '__main__':
    app.run()