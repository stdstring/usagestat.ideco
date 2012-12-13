#!/bin/bash
curl --dump-header - -H "Content-Type: application/xml" -X POST --data '{"source_id": "iddqd", "items": [{"category": "cat1", "data": "data1"}, {"category": "cat2", "data": "data2"}]}' http://localhost:8888/collect/
