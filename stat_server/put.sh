#!/bin/bash
curl --dump-header - -H "Content-Type: application/xml" -X PUT --data '<objects user_id="83cf01c6-2284-11e2-9494-08002703af71"><object><source>source1</source><category>cat1</category><timemarker>2012-12-21 23:59:59</timemarker><data>IDDQD</data></object><object><source>source666</source><category>cat999</category><timemarker>2012-12-21 23:59:59</timemarker><data>IDKFA</data></object></objects>' http://127.0.0.1:8000/statserver/api/v1/collect/
