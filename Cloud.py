import requests
from flask import Flask, Request, jsonify

URL = "https://events.fredonia.edu/api/2/events?type=105813&pp=100&page=1&days=200"
AthleticURL = "https://events.fredonia.edu/api/2/events?type=105880&pp=100&page=1&days=1"

Send={
  "payload": {
    "google": {
      "expectUserResponse": 'false',
      "richResponse": {
        "items": [
          {
            "simpleResponse": {
              "textToSpeech": "Error!"
            }
          }
        ]
      }
    }
  }
}



def hello_world(request):
	response = requests.get(url = URL)
	responseJson=response.json()
	results=responseJson["events"]
	test=request.get_json(force=True)

	AthleticResponse=requests.get(url = AthleticURL)
	AthResponseJson=AthleticResponse.json()
	AthResults=AthResponseJson["events"]


	if(test["queryResult"]["parameters"].get('AthleticCalendar')):
		subscript="AthleticCalendar"
	else:
		subscript="ScheduleAnswer"


	if("SPRING SEMESTER" in test["queryResult"]["parameters"][subscript].upper()):
		for x in results:
			if("FIRST DAY OF CLASSES" in x["event"]["title"].upper()):
				Send["payload"]["google"]["richResponse"]["items"][0]["simpleResponse"]["textToSpeech"]="The Spring Semester starts "+x["event"]["first_date"]
				return jsonify(Send)
	if("FINAL" in test["queryResult"]["parameters"][subscript].upper()):
		for x in results:
			if("FINAL EXAM" in x["event"]["title"].upper()):
				Send["payload"]["google"]["richResponse"]["items"][0]["simpleResponse"]["textToSpeech"]="Final exams are "+x["event"]["first_date"]+" to "+x["event"]["last_date"]
				return jsonify(Send)
	if("GYM" in test["queryResult"]["parameters"][subscript].upper()):
		for x in AthResults:
			if("FITNESS CENTER" in x["event"]["title"].upper()):
				Send["payload"]["google"]["richResponse"]["items"][0]["simpleResponse"]["textToSpeech"]="The gym is open from " + x["event"]["event_instances"][0]["event_instance"]["start"][11:16]+ " AM to "+x["event"]["event_instances"][0]["event_instance"]["end"][11:16]+" PM "
				return jsonify(Send)

	return jsonify(Send)
