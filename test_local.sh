curl localhost:8000 \
  -X POST \
  -H "Content-Type: application/json" \
  -H "ce-id: 123451234512345" \
  -H "ce-specversion: 1.0" \
  -H "ce-time: 2024-01-05T16:08:15.789Z" \
  -H "ce-type: google.cloud.pubsub.topic.v1.messagePublished" \
  -H "ce-source: //pubsub.googleapis.com/projects/MY-PROJECT/topics/MY-TOPIC" \
  -d '{
      "message": {
        "data":"eyJjYV91dWlkIjogIjRiMjMyNDJhLTExNjEtNDZjMy1hZjg0LTVlMzVkYzgwMWM0MyIsICJwYXRyb2xfcmVxdWVzdHMiOiBbXSwgIndheXBvaW50X3JlcXVlc3RzIjogW3sidHlwZSI6ICJGZWF0dXJlIiwgImdlb21ldHJ5IjogeyJjb29yZGluYXRlcyI6IFstNzIuNzA0NDI1LCAtNTEuNjg4NjQ1XX0sICJwcm9wZXJ0aWVzIjogeyJkYXRlVGltZSI6ICIyMDI0LTAxLTA1VDE5OjAzOjAwIiwgInNtYXJ0RGF0YVR5cGUiOiAiaW5jaWRlbnQiLCAic21hcnRGZWF0dXJlVHlwZSI6ICJ3YXlwb2ludC9uZXciLCAic21hcnRBdHRyaWJ1dGVzIjogeyJvYnNlcnZhdGlvbkdyb3VwcyI6IFt7Im9ic2VydmF0aW9ucyI6IFt7Im9ic2VydmF0aW9uVXVpZCI6ICIzYWZhNmIxYi0wOGIyLTRlYzgtODQxYi1iODkwODFmMDI0ZjgiLCAiY2F0ZWdvcnkiOiAiYW5pbWFscy5zaWduIiwgImF0dHJpYnV0ZXMiOiB7InNwZWNpZXMiOiAibGlvbiIsICJhZ2VvZnNpZ24iOiAiZGF5cyJ9fV19XSwgInBhdHJvbFV1aWQiOiBudWxsLCAicGF0cm9sTGVnVXVpZCI6IG51bGwsICJwYXRyb2xJZCI6IG51bGwsICJpbmNpZGVudElkIjogImd1bmRpX2V2XzNhZmE2YjFiLTA4YjItNGVjOC04NDFiLWI4OTA4MWYwMjRmOCIsICJpbmNpZGVudFV1aWQiOiAiM2FmYTZiMWItMDhiMi00ZWM4LTg0MWItYjg5MDgxZjAyNGY4IiwgInRlYW0iOiBudWxsLCAib2JqZWN0aXZlIjogbnVsbCwgImNvbW1lbnQiOiAiUmVwb3J0OiBBbmltYWxzIFNpZ25cbkltcG9ydGVkOiAyMDI0LTAxLTA1VDE5OjA1OjIyLjU2MjE4MS0wMzowMCIsICJpc0FybWVkIjogbnVsbCwgInRyYW5zcG9ydFR5cGUiOiBudWxsLCAibWFuZGF0ZSI6IG51bGwsICJudW1iZXIiOiBudWxsLCAibWVtYmVycyI6IG51bGwsICJsZWFkZXIiOiBudWxsLCAiYXR0YWNobWVudHMiOiBudWxsfX19XSwgInRyYWNrX3BvaW50X3JlcXVlc3RzIjogW119",
        "attributes":{
          "gundi_version":"v2",
          "provider_key":"gundi_trap_tagger_d88ac520-2bf6-4e6b-ab09-38ed1ec6947a",
          "gundi_id":"3a09e9c8-525a-4431-a43e-12a9830f688e",
          "related_to": "None",
          "stream_type":"ev",
          "source_id":"393daf82-822a-4953-bfda-049587261076",
          "external_source_id":"Xyz123",
          "destination_id":"b42c9205-5228-49e0-a75b-ebe5b6a9f78e",
          "data_provider_id":"d88ac520-2bf6-4e6b-ab09-38ed1ec6947a",
          "annotations":"{}",
          "tracing_context":"{}"
        }
      },
      "subscription": "projects/MY-PROJECT/subscriptions/MY-SUB"
    }'
# Gundi v2 Event
#  -d '{
#      "message": {
#        "data":"eyJ0aXRsZSI6ICJBbmltYWwgRGV0ZWN0ZWQiLCAiZXZlbnRfdHlwZSI6ICJsZW9wYXJkX3NpZ2h0aW5nIiwgImV2ZW50X2RldGFpbHMiOiB7InNpdGVfbmFtZSI6ICJDYW1lcmEyQSIsICJzcGVjaWVzIjogIkxlb3BhcmQiLCAidGFncyI6IFsiYWR1bHQiLCAibWFsZSJdLCAiYW5pbWFsX2NvdW50IjogMn0sICJ0aW1lIjogIjIwMjMtMDYtMjMgMDA6NTE6MDArMDA6MDAiLCAibG9jYXRpb24iOiB7ImxvbmdpdHVkZSI6IDIwLjgwNjc4NSwgImxhdGl0dWRlIjogLTU1Ljc4NDk5OH19",
#        "attributes":{
#          "gundi_version":"v2",
#          "provider_key":"awt",
#          "gundi_id":"23ca4b15-18b6-4cf4-9da6-36dd69c6f638",
#          "related_to":"None",
#          "stream_type":"ev",
#          "source_id":"ea2d5fca-752a-4a44-b170-668d780db85e",
#          "external_source_id":"Xyz123",
#          "destination_id":"a9aa0990-2674-4ff4-8ba2-f9b9a613d7c0",
#          "data_provider_id":"d88ac520-2bf6-4e6b-ab09-38ed1ec6947a",
#          "annotations":"{}",
#          "tracing_context":"{\"x-cloud-trace-context\": \"95f36c1f22b1cb599efc28243a631f7d/15139689239813763386;o=1\"}"
#        }
#      },
#      "subscription": "projects/MY-PROJECT/subscriptions/MY-SUB"
#    }'
# Gundi v2 Attachment
#  -d '{
#      "message": {
#        "data":"eyJmaWxlX3BhdGgiOiAiYXR0YWNobWVudHMvZjFhODg5NGItZmYyZS00Mjg2LTkwYTAtOGYxNzMwM2U5MWRmXzIwMjMtMDYtMjYtMTA1M19sZW9wYXJkLmpwZyJ9",
#        "attributes":{
#          "gundi_version":"v2",
#          "provider_key":"d88ac520-2bf6-4e6b-ab09-38ed1ec6947a",
#          "gundi_id":"e6795790-4a5f-4d47-ac93-de7d7713698b",
#          "related_to":"13632f77-6858-4721-8603-64138a9f38aa",
#          "stream_type":"att",
#          "source_id":"None",
#          "external_source_id":"None",
#          "destination_id":"a9aa0990-2674-4ff4-8ba2-f9b9a613d7c0",
#          "data_provider_id":"d88ac520-2bf6-4e6b-ab09-38ed1ec6947a",
#          "annotations":"null",
#          "tracing_context":"{}"
#        }
#      },
#      "subscription": "projects/MY-PROJECT/subscriptions/MY-SUB"
#    }'
# Gundi v1
#  -d '{
#        "message": {
#          "data":"eyJtYW51ZmFjdHVyZXJfaWQiOiAiMDE4OTEwOTgwIiwgInNvdXJjZV90eXBlIjogInRyYWNraW5nLWRldmljZSIsICJzdWJqZWN0X25hbWUiOiAiTG9naXN0aWNzIFRydWNrIEEiLCAicmVjb3JkZWRfYXQiOiAiMjAyMy0wMy0wNyAwODo1OTowMC0wMzowMCIsICJsb2NhdGlvbiI6IHsibG9uIjogMzUuNDM5MTIsICJsYXQiOiAtMS41OTA4M30sICJhZGRpdGlvbmFsIjogeyJ2b2x0YWdlIjogIjcuNCIsICJmdWVsX2xldmVsIjogNzEsICJzcGVlZCI6ICI0MSBrcGgifX0=",
#          "attributes":{
#             "observation_type":"ps",
#             "device_id":"018910980",
#             "outbound_config_id":"1c19dc7e-73e2-4af3-93f5-a1cb322e5add",
#             "integration_id":"36485b4f-88cd-49c4-a723-0ddff1f580c4",
#             "tracing_context":"{}"
#          }
#        },
#        "subscription": "projects/MY-PROJECT/subscriptions/MY-SUB"
#      }'
# CemeraTrap
#  -d '{
#      "message": {
#        "data":"eyJmaWxlIjogImNhbWVyYXRyYXAuanBnIiwgImNhbWVyYV9uYW1lIjogIk1hcmlhbm8ncyBDYW1lcmEiLCAiY2FtZXJhX2Rlc2NyaXB0aW9uIjogInRlc3QgY2FtZXJhIiwgInRpbWUiOiAiMjAyMy0wMy0wNyAxMTo1MTowMC0wMzowMCIsICJsb2NhdGlvbiI6ICJ7XCJsb25naXR1ZGVcIjogLTEyMi41LCBcImxhdGl0dWRlXCI6IDQ4LjY1fSJ9",
#        "attributes":{
#          "observation_type":"ct",
#          "device_id":"Mariano Camera",
#          "outbound_config_id":"5f658487-67f7-43f1-8896-d78778e49c30",
#          "integration_id":"a244fddd-3f64-4298-81ed-b6fccc60cef8",
#          "tracing_context":"{}"
#        }
#      },
#      "subscription": "projects/MY-PROJECT/subscriptions/MY-SUB"
#    }'
# GeoEvent
#  -d '{
#      "message": {
#        "data":"eyJ0aXRsZSI6ICJSYWluZmFsbCIsICJldmVudF90eXBlIjogInJhaW5mYWxsX3JlcCIsICJldmVudF9kZXRhaWxzIjogeyJhbW91bnRfbW0iOiA2LCAiaGVpZ2h0X20iOiAzfSwgInRpbWUiOiAiMjAyMy0wMy0wNyAxMToyNDowMi0wNzowMCIsICJsb2NhdGlvbiI6IHsibG9uZ2l0dWRlIjogLTU1Ljc4NDk4LCAibGF0aXR1ZGUiOiAyMC44MDY3ODV9fQ==",
#        "attributes":{
#          "observation_type":"ge",
#          "device_id":"003",
#          "outbound_config_id":"9243a5e3-b16a-4dbd-ad32-197c58aeef59",
#          "integration_id":"8311c4a5-ddab-4743-b8ab-d3d57a7c8212",
#          "tracing_context":"{}"
#        }
#      },
#      "subscription": "projects/MY-PROJECT/subscriptions/MY-SUB"
#    }'
