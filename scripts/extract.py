''' This code must be run directly in Nifi in an ExecuteScript processor
    If new fields are added, the avro schema must also be changed, otherwise the new fields will be ignored
    All the fields defined in the AVRO schema must also be defined here, otherwiese there will be an error '''

import time, json
from java.nio.charset import StandardCharsets
from org.apache.commons.io import IOUtils
from org.apache.nifi.processor.io import StreamCallback


class Event():

    def __init__(self, filename):
        self.data = {}
        self.data['time'] = self.actualUnixTime()
        self.data['filename'] = filename
        self.data['ip'] = None
        self.data['type'] = None
        
    def actualUnixTime(self):
        ''' return actual unixtime in milliseconds '''
        return int(time.time() * 1000.0)

    def toJson(self):
        # dict is need for JSON serialization. self.__dict__ will fail with Nifi
        return json.dumps(self.data)


class TransformCallback(StreamCallback):

    fileName = ""

    def __init__(self, fileName):
        self.fileName = fileName

    def process(self, inputStream, outputStream):

        # Read input FlowFile content
        input = IOUtils.toString(inputStream, StandardCharsets.UTF_8)

        lines = []
        for line in input.splitlines():

            event = Event(self.fileName)
            fields = line.split(" ")
            event.data['ip'] = fields[0]
            event.data['type'] = fields[1]

            lines.append(event.toJson())

        output = "\n".join([str(l) for l in lines])
        outputStream.write(output.encode('utf-8'))

        log.info("{} events successfully extracted from {}".format(len(lines), self.fileName))


flowFile = session.get()
if flowFile != None:

    session.putAttribute(flowFile, "content-type", "application/json")
    session.putAttribute(flowFile, "mime.type", "application/json")

    try:
        fileName = flowFile.getAttribute('filename')
        flowFile = session.write(flowFile, TransformCallback(fileName))
        session.transfer(flowFile, REL_SUCCESS)
    except Exception as e:
        log.error(str(e))
        session.transfer(flowFile, REL_FAILURE)