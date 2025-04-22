def store():
    logger = system.util.getLogger("ImageStore")
    base64_data = system.tag.readBlocking(["[MQTT Engine]images/defect"])[0].value
    document = {"timestamp": system.date.now(),
        		"tagName": "ImageBase64",
        		"base64Data": base64_data}
    try:
        result = system.mongodb.insertOne(connector="mongodb",collection="images",document=document)
        logger.info("Insert result: %s" % str(result))
    except Exception as e:
        logger.error("MongoDB insert failed: %s" % str(e))