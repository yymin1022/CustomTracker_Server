from datetime import datetime
from flask import Flask
from flask import request
from urllib.request import urlopen
from xml.etree import ElementTree

app = Flask(__name__)

apiKey = "d240g270y083v227e030m080h1"
defaultUrl = "https://unipass.customs.go.kr:38010/ext/rest/cargCsclPrgsInfoQry/retrieveCargCsclPrgsInfo?crkyCn={0}&blYy={2}&hblNo={1}"


@app.route('/getTrackInfo')
def hello_world():
    customTrackResult = []

    trackNum = request.args.get("trackNum", 00000000)
    parcelYear = request.args.get("parcelYear", datetime.today().year)
    unipassUrl = str.format(defaultUrl, apiKey, trackNum, parcelYear)

    unipassResponce = urlopen(unipassUrl).read()
    rootElement = ElementTree.fromstring(unipassResponce)

    customSimpleProcessElement = rootElement.iter(tag="cargCsclPrgsInfoQryVo")
    for currentProcess in customSimpleProcessElement:
        currentProcessInfo = {}
        currentProcessInfo["Name"] = currentProcess.find("prnm").text
        currentProcessInfo["Location"] = currentProcess.find("etprCstm").text
        currentProcessInfo["Weight"] = currentProcess.find("ttwg").text
        customTrackResult.append(currentProcessInfo)

    customDetailProcessElement = rootElement.iter(tag="cargCsclPrgsInfoDtlQryVo")

    for currentProcess in customDetailProcessElement:
        currentProcessDict = {}
        currentProcessDict["Step"] = currentProcess.find("cargTrcnRelaBsopTpcd").text
        currentProcessDict["Date"] = currentProcess.find("prcsDttm").text
        customTrackResult.append(currentProcessDict)

    return str(customTrackResult)


if __name__ == '__main__':
    app.run()