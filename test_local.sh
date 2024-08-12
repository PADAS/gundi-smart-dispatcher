curl localhost:8383 \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{
      "message": {
        "data":"eyJldmVudF9pZCI6ICJiOGRlZjIzNS0yYzdhLTQ1ZDAtODNhMi1kOWFkMTQ1ZDU1MDciLCAidGltZXN0YW1wIjogIjIwMjQtMDgtMDIgMTQ6MjI6MTMuMTg3MTQ0KzAwOjAwIiwgInNjaGVtYV92ZXJzaW9uIjogInYxIiwgInBheWxvYWQiOiB7ImNhX3V1aWQiOiAiMTY5MzYxZDAtNjJiOC00MTFkLWE4ZTYtMDE5ODIzODA1MDE2IiwgIndheXBvaW50X3JlcXVlc3RzIjogW3sidHlwZSI6ICJGZWF0dXJlIiwgImdlb21ldHJ5IjogeyJjb29yZGluYXRlcyI6IFsxMy4xMjM0NTYsIDEzLjEyMzQ1Nl19LCAicHJvcGVydGllcyI6IHsiZGF0ZVRpbWUiOiAiMjAyNC0wOC0wMiAxMTo0NjoxMCIsICJzbWFydERhdGFUeXBlIjogImluY2lkZW50IiwgInNtYXJ0RmVhdHVyZVR5cGUiOiAid2F5cG9pbnQiLCAic21hcnRBdHRyaWJ1dGVzIjogeyJpbmNpZGVudElkIjogImd1bmRpX2V2XzU0NmI5MjdiLTU3OGMtNDUwNC05OWNlLWE0Mjg5NTI4NDk0MSIsICJpbmNpZGVudFV1aWQiOiAiNTQ2YjkyN2ItNTc4Yy00NTA0LTk5Y2UtYTQyODk1Mjg0OTQxIiwgImNvbW1lbnQiOiAiUmVwb3J0OiBBbmltYWxzIDEwIEVkaXRlZCBkZXRhaWxzIFxuVXBkYXRlZDogMjAyNC0wOC0wMlQxNDoyMTozMS4zMDU4ODArMDA6MDAifX19LCB7InR5cGUiOiAiRmVhdHVyZSIsICJwcm9wZXJ0aWVzIjogeyJzbWFydERhdGFUeXBlIjogImluY2lkZW50IiwgInNtYXJ0RmVhdHVyZVR5cGUiOiAid2F5cG9pbnQvb2JzZXJ2YXRpb24iLCAic21hcnRBdHRyaWJ1dGVzIjogeyJvYnNlcnZhdGlvblV1aWQiOiAiNTQ2YjkyN2ItNTc4Yy00NTA0LTk5Y2UtYTQyODk1Mjg0OTQxIiwgImNhdGVnb3J5IjogImFuaW1hbHMiLCAiYXR0cmlidXRlcyI6IHsidGFyZ2V0c3BlY2llcyI6ICJyZXB0aWxlcy5weXRob25zcHAiLCAid2lsZGxpZmVvYnNlcnZhdGlvbnR5cGUiOiAiZGlyZWN0b2JzZXJ2YXRpb24iLCAiYWdlb2ZzaWduYW5pbWFsIjogImZyZXNoIiwgIm51bWJlcm9mYW5pbWFsIjogNX19fX1dfSwgImV2ZW50X3R5cGUiOiAiRXZlbnRVcGRhdGVUcmFuc2Zvcm1lZFNNQVJUIn0=", # pragma: allowlist secret
        "attributes":{
          "gundi_version":"v2",
          "provider_key":"gundi_trap_tagger_d88ac520-2bf6-4e6b-ab09-38ed1ec6947a",
          "gundi_id":"546b927b-578c-4504-99ce-a42895284941",
          "related_to": "None",
          "stream_type":"evu",
          "source_id":"29669b17-c888-4c6d-87b5-d8b9e14e342d",
          "external_source_id":"default-source",
          "destination_id":"b42c9205-5228-49e0-a75b-ebe5b6a9f78e",
          "data_provider_id":"d88ac520-2bf6-4e6b-ab09-38ed1ec6947a",
          "annotations":"{}",
          "tracing_context":"{}"
        },
        "messageId": "9155786613739819",
        "message_id": "9155786613739819",
        "publishTime": "2024-08-02T16:08:15.789Z",
        "publish_time": "2024-08-02T16:08:15.789Z",
        "orderingKey": "546b927b-578c-4504-99ce-a42895284941"
      },
      "subscription": "projects/MY-PROJECT/subscriptions/MY-SUB"
    }'  # pragma: allowlist secret
# Gundi v2 Event Update for SMART - Full
#  -d '{
#      "message": {
#        "data":"eyJldmVudF9pZCI6ICJiOGRlZjIzNS0yYzdhLTQ1ZDAtODNhMi1kOWFkMTQ1ZDU1MDciLCAidGltZXN0YW1wIjogIjIwMjQtMDgtMDIgMTQ6MjI6MTMuMTg3MTQ0KzAwOjAwIiwgInNjaGVtYV92ZXJzaW9uIjogInYxIiwgInBheWxvYWQiOiB7ImNhX3V1aWQiOiAiMTY5MzYxZDAtNjJiOC00MTFkLWE4ZTYtMDE5ODIzODA1MDE2IiwgIndheXBvaW50X3JlcXVlc3RzIjogW3sidHlwZSI6ICJGZWF0dXJlIiwgImdlb21ldHJ5IjogeyJjb29yZGluYXRlcyI6IFsxMy4xMjM0NTYsIDEzLjEyMzQ1Nl19LCAicHJvcGVydGllcyI6IHsiZGF0ZVRpbWUiOiAiMjAyNC0wOC0wMiAxMTo0NjoxMCIsICJzbWFydERhdGFUeXBlIjogImluY2lkZW50IiwgInNtYXJ0RmVhdHVyZVR5cGUiOiAid2F5cG9pbnQiLCAic21hcnRBdHRyaWJ1dGVzIjogeyJpbmNpZGVudElkIjogImd1bmRpX2V2XzU0NmI5MjdiLTU3OGMtNDUwNC05OWNlLWE0Mjg5NTI4NDk0MSIsICJpbmNpZGVudFV1aWQiOiAiNTQ2YjkyN2ItNTc4Yy00NTA0LTk5Y2UtYTQyODk1Mjg0OTQxIiwgImNvbW1lbnQiOiAiUmVwb3J0OiBBbmltYWxzIDEwIEVkaXRlZCBkZXRhaWxzIFxuVXBkYXRlZDogMjAyNC0wOC0wMlQxNDoyMTozMS4zMDU4ODArMDA6MDAifX19LCB7InR5cGUiOiAiRmVhdHVyZSIsICJwcm9wZXJ0aWVzIjogeyJzbWFydERhdGFUeXBlIjogImluY2lkZW50IiwgInNtYXJ0RmVhdHVyZVR5cGUiOiAid2F5cG9pbnQvb2JzZXJ2YXRpb24iLCAic21hcnRBdHRyaWJ1dGVzIjogeyJvYnNlcnZhdGlvblV1aWQiOiAiNTQ2YjkyN2ItNTc4Yy00NTA0LTk5Y2UtYTQyODk1Mjg0OTQxIiwgImNhdGVnb3J5IjogImFuaW1hbHMiLCAiYXR0cmlidXRlcyI6IHsidGFyZ2V0c3BlY2llcyI6ICJyZXB0aWxlcy5weXRob25zcHAiLCAid2lsZGxpZmVvYnNlcnZhdGlvbnR5cGUiOiAiZGlyZWN0b2JzZXJ2YXRpb24iLCAiYWdlb2ZzaWduYW5pbWFsIjogImZyZXNoIiwgIm51bWJlcm9mYW5pbWFsIjogNX19fX1dfSwgImV2ZW50X3R5cGUiOiAiRXZlbnRVcGRhdGVUcmFuc2Zvcm1lZFNNQVJUIn0=", # pragma: allowlist secret
#        "attributes":{
#          "gundi_version":"v2",
#          "provider_key":"gundi_trap_tagger_d88ac520-2bf6-4e6b-ab09-38ed1ec6947a",
#          "gundi_id":"546b927b-578c-4504-99ce-a42895284941",
#          "related_to": "None",
#          "stream_type":"evu",
#          "source_id":"29669b17-c888-4c6d-87b5-d8b9e14e342d",
#          "external_source_id":"default-source",
#          "destination_id":"b42c9205-5228-49e0-a75b-ebe5b6a9f78e",
#          "data_provider_id":"d88ac520-2bf6-4e6b-ab09-38ed1ec6947a",
#          "annotations":"{}",
#          "tracing_context":"{}"
#        },
#        "messageId": "9155786613739819",
#        "message_id": "9155786613739819",
#        "publishTime": "2024-08-02T16:08:15.789Z",
#        "publish_time": "2024-08-02T16:08:15.789Z",
#        "orderingKey": "546b927b-578c-4504-99ce-a42895284941"
#      },
#      "subscription": "projects/MY-PROJECT/subscriptions/MY-SUB"
#    }'
# Gundi v2 Event Update for SMART - Partial
#  -d '{
#      "message": {
#        "data":"eyJldmVudF9pZCI6ICJhNjZiNWUzZS01YjlmLTQ0MDItYmM4ZC0xYTZiNTk3OTFmNzYiLCAidGltZXN0YW1wIjogIjIwMjQtMDgtMDIgMTI6MTg6MjQuNjUwNTk4KzAwOjAwIiwgInNjaGVtYV92ZXJzaW9uIjogInYxIiwgInBheWxvYWQiOiB7ImNhX3V1aWQiOiAiMTY5MzYxZDAtNjJiOC00MTFkLWE4ZTYtMDE5ODIzODA1MDE2IiwgIndheXBvaW50X3JlcXVlc3RzIjogW3sidHlwZSI6ICJGZWF0dXJlIiwgImdlb21ldHJ5IjogeyJjb29yZGluYXRlcyI6IFsxMy4xMjM0NTYsIDEzLjEyMzQ1Nl19LCAicHJvcGVydGllcyI6IHsiZGF0ZVRpbWUiOiAiMjAyNC0wOC0wMiAxMTo0NjoxMCIsICJzbWFydERhdGFUeXBlIjogImluY2lkZW50IiwgInNtYXJ0RmVhdHVyZVR5cGUiOiAid2F5cG9pbnQiLCAic21hcnRBdHRyaWJ1dGVzIjogeyJpbmNpZGVudElkIjogImd1bmRpX2V2XzU0NmI5MjdiLTU3OGMtNDUwNC05OWNlLWE0Mjg5NTI4NDk0MSIsICJpbmNpZGVudFV1aWQiOiAiNTQ2YjkyN2ItNTc4Yy00NTA0LTk5Y2UtYTQyODk1Mjg0OTQxIiwgImNvbW1lbnQiOiAiUmVwb3J0OiBBbmltYWxzIDA0IEVkaXRlZCAoVGVzdCBNYXJpYW5vKSBcblVwZGF0ZWQ6IDIwMjQtMDgtMDJUMTI6NTg6MDcuOTk3OTY5KzAwOjAwIn19fV19LCAiZXZlbnRfdHlwZSI6ICJFdmVudFVwZGF0ZVRyYW5zZm9ybWVkU01BUlQifQ==", # pragma: allowlist secret
#        "attributes":{
#          "gundi_version":"v2",
#          "provider_key":"gundi_trap_tagger_d88ac520-2bf6-4e6b-ab09-38ed1ec6947a",
#          "gundi_id":"546b927b-578c-4504-99ce-a42895284941",
#          "related_to": "None",
#          "stream_type":"evu",
#          "source_id":"29669b17-c888-4c6d-87b5-d8b9e14e342d",
#          "external_source_id":"default-source",
#          "destination_id":"b42c9205-5228-49e0-a75b-ebe5b6a9f78e",
#          "data_provider_id":"d88ac520-2bf6-4e6b-ab09-38ed1ec6947a",
#          "annotations":"{}",
#          "tracing_context":"{}"
#        },
#        "messageId": "9155786613739819",
#        "message_id": "9155786613739819",
#        "publishTime": "2024-08-02T16:08:15.789Z",
#        "publish_time": "2024-08-02T16:08:15.789Z",
#        "orderingKey": "546b927b-578c-4504-99ce-a42895284941"
#      },
#      "subscription": "projects/MY-PROJECT/subscriptions/MY-SUB"
#    }'
# Gundi v2 Event for SMART
#  -d '{
#      "message": {
#        "data":"eyJldmVudF9pZCI6ICI5ODZkMzQwYi02ZThiLTQ3MTctOTMwZS1kZWUwOWYzY2Y0OGUiLCAidGltZXN0YW1wIjogIjIwMjQtMDgtMDIgMTA6NTU6NDcuOTAyMTcxKzAwOjAwIiwgInNjaGVtYV92ZXJzaW9uIjogInYxIiwgInBheWxvYWQiOiB7ImNhX3V1aWQiOiAiMTY5MzYxZDAtNjJiOC00MTFkLWE4ZTYtMDE5ODIzODA1MDE2IiwgInBhdHJvbF9yZXF1ZXN0cyI6IFtdLCAid2F5cG9pbnRfcmVxdWVzdHMiOiBbeyJ0eXBlIjogIkZlYXR1cmUiLCAiZ2VvbWV0cnkiOiB7ImNvb3JkaW5hdGVzIjogWzEzLjc4MzA2NywgMTMuNjg4NjM0XX0sICJwcm9wZXJ0aWVzIjogeyJkYXRlVGltZSI6ICIyMDI0LTA4LTAyIDExOjQ2OjEwIiwgInNtYXJ0RGF0YVR5cGUiOiAiaW5jaWRlbnQiLCAic21hcnRGZWF0dXJlVHlwZSI6ICJ3YXlwb2ludC9uZXciLCAic21hcnRBdHRyaWJ1dGVzIjogeyJvYnNlcnZhdGlvbkdyb3VwcyI6IFt7Im9ic2VydmF0aW9ucyI6IFt7Im9ic2VydmF0aW9uVXVpZCI6ICI1NDZiOTI3Yi01NzhjLTQ1MDQtOTljZS1hNDI4OTUyODQ5NDEiLCAiY2F0ZWdvcnkiOiAiYW5pbWFscyIsICJhdHRyaWJ1dGVzIjogeyJ0YXJnZXRzcGVjaWVzIjogInJlcHRpbGVzLnB5dGhvbnNwcCIsICJ3aWxkbGlmZW9ic2VydmF0aW9udHlwZSI6ICJkaXJlY3RvYnNlcnZhdGlvbiIsICJhZ2VvZnNpZ25hbmltYWwiOiAiZnJlc2giLCAibnVtYmVyb2ZhbmltYWwiOiAxfX1dfV0sICJpbmNpZGVudElkIjogImd1bmRpX2V2XzU0NmI5MjdiLTU3OGMtNDUwNC05OWNlLWE0Mjg5NTI4NDk0MSIsICJpbmNpZGVudFV1aWQiOiAiNTQ2YjkyN2ItNTc4Yy00NTA0LTk5Y2UtYTQyODk1Mjg0OTQxIiwgImNvbW1lbnQiOiAiUmVwb3J0OiBBbmltYWxzIDAyIChUZXN0IE1hcmlhbm8pXG5JbXBvcnRlZDogMjAyNC0wOC0wMlQxMTo1MzoxOC4yNzI5NDQrMDE6MDAifX19XSwgInRyYWNrX3BvaW50X3JlcXVlc3RzIjogW119LCAiZXZlbnRfdHlwZSI6ICJFdmVudFRyYW5zZm9ybWVkU01BUlQifQ==", # pragma: allowlist secret
#        "attributes":{
#          "gundi_version":"v2",
#          "provider_key":"gundi_trap_tagger_d88ac520-2bf6-4e6b-ab09-38ed1ec6947a",
#          "gundi_id":"546b927b-578c-4504-99ce-a42895284941",
#          "related_to": "None",
#          "stream_type":"ev",
#          "source_id":"29669b17-c888-4c6d-87b5-d8b9e14e342d",
#          "external_source_id":"default-source",
#          "destination_id":"b42c9205-5228-49e0-a75b-ebe5b6a9f78e",
#          "data_provider_id":"d88ac520-2bf6-4e6b-ab09-38ed1ec6947a",
#          "annotations":"{}",
#          "tracing_context":"{}"
#        },
#        "messageId": "9155786613739819",
#        "message_id": "9155786613739819",
#        "publishTime": "2024-08-02T16:08:15.789Z",
#        "publish_time": "2024-08-02T16:08:15.789Z"
#      },
#      "subscription": "projects/MY-PROJECT/subscriptions/MY-SUB"
#    }'
# Gundi v2 Event for ER
#  -d '{
#      "message": {
#        "data":"eyJ0aXRsZSI6ICJBbmltYWwgRGV0ZWN0ZWQiLCAiZXZlbnRfdHlwZSI6ICJsZW9wYXJkX3NpZ2h0aW5nIiwgImV2ZW50X2RldGFpbHMiOiB7InNpdGVfbmFtZSI6ICJDYW1lcmEyQSIsICJzcGVjaWVzIjogIkxlb3BhcmQiLCAidGFncyI6IFsiYWR1bHQiLCAibWFsZSJdLCAiYW5pbWFsX2NvdW50IjogMn0sICJ0aW1lIjogIjIwMjMtMDYtMjMgMDA6NTE6MDArMDA6MDAiLCAibG9jYXRpb24iOiB7ImxvbmdpdHVkZSI6IDIwLjgwNjc4NSwgImxhdGl0dWRlIjogLTU1Ljc4NDk5OH19", # pragma: allowlist secret
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
#        },
#        "messageId": "9155786613739819",
#        "message_id": "9155786613739819",
#        "publishTime": "2024-08-02T16:08:15.789Z",
#        "publish_time": "2024-08-02T16:08:15.789Z"
#      },
#      "subscription": "projects/MY-PROJECT/subscriptions/MY-SUB"
#    }'
# Gundi v2 Attachment
#  -d '{
#      "message": {
#        "data":"eyJmaWxlX3BhdGgiOiAiYXR0YWNobWVudHMvZjFhODg5NGItZmYyZS00Mjg2LTkwYTAtOGYxNzMwM2U5MWRmXzIwMjMtMDYtMjYtMTA1M19sZW9wYXJkLmpwZyJ9", # pragma: allowlist secret
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
#        },
#        "messageId": "9155786613739819",
#        "message_id": "9155786613739819",
#        "publishTime": "2024-08-02T16:08:15.789Z",
#        "publish_time": "2024-08-02T16:08:15.789Z"
#      },
#      "subscription": "projects/MY-PROJECT/subscriptions/MY-SUB"
#    }'
# Gundi v1
#  -d '{
#        "message": {
#          "data":"eyJtYW51ZmFjdHVyZXJfaWQiOiAiMDE4OTEwOTgwIiwgInNvdXJjZV90eXBlIjogInRyYWNraW5nLWRldmljZSIsICJzdWJqZWN0X25hbWUiOiAiTG9naXN0aWNzIFRydWNrIEEiLCAicmVjb3JkZWRfYXQiOiAiMjAyMy0wMy0wNyAwODo1OTowMC0wMzowMCIsICJsb2NhdGlvbiI6IHsibG9uIjogMzUuNDM5MTIsICJsYXQiOiAtMS41OTA4M30sICJhZGRpdGlvbmFsIjogeyJ2b2x0YWdlIjogIjcuNCIsICJmdWVsX2xldmVsIjogNzEsICJzcGVlZCI6ICI0MSBrcGgifX0=", # pragma: allowlist secret
#          "attributes":{
#             "observation_type":"ps",
#             "device_id":"018910980",
#             "outbound_config_id":"1c19dc7e-73e2-4af3-93f5-a1cb322e5add",
#             "integration_id":"36485b4f-88cd-49c4-a723-0ddff1f580c4",
#             "tracing_context":"{}"
#        },
#          "messageId": "9155786613739819",
#          "message_id": "9155786613739819",
#          "publishTime": "2024-08-02T16:08:15.789Z",
#          "publish_time": "2024-08-02T16:08:15.789Z"
#        },
#        "subscription": "projects/MY-PROJECT/subscriptions/MY-SUB"
#      }'
# CemeraTrap
#  -d '{
#      "message": {
#        "data":"eyJmaWxlIjogImNhbWVyYXRyYXAuanBnIiwgImNhbWVyYV9uYW1lIjogIk1hcmlhbm8ncyBDYW1lcmEiLCAiY2FtZXJhX2Rlc2NyaXB0aW9uIjogInRlc3QgY2FtZXJhIiwgInRpbWUiOiAiMjAyMy0wMy0wNyAxMTo1MTowMC0wMzowMCIsICJsb2NhdGlvbiI6ICJ7XCJsb25naXR1ZGVcIjogLTEyMi41LCBcImxhdGl0dWRlXCI6IDQ4LjY1fSJ9", # pragma: allowlist secret
#        "attributes":{
#          "observation_type":"ct",
#          "device_id":"Mariano Camera",
#          "outbound_config_id":"5f658487-67f7-43f1-8896-d78778e49c30",
#          "integration_id":"a244fddd-3f64-4298-81ed-b6fccc60cef8",
#          "tracing_context":"{}"
#        },
#          "messageId": "9155786613739819",
#          "message_id": "9155786613739819",
#          "publishTime": "2024-08-02T16:08:15.789Z",
#          "publish_time": "2024-08-02T16:08:15.789Z"
#        },
#      "subscription": "projects/MY-PROJECT/subscriptions/MY-SUB"
#    }'
# GeoEvent
#  -d '{
#      "message": {
#        "data":"eyJ0aXRsZSI6ICJSYWluZmFsbCIsICJldmVudF90eXBlIjogInJhaW5mYWxsX3JlcCIsICJldmVudF9kZXRhaWxzIjogeyJhbW91bnRfbW0iOiA2LCAiaGVpZ2h0X20iOiAzfSwgInRpbWUiOiAiMjAyMy0wMy0wNyAxMToyNDowMi0wNzowMCIsICJsb2NhdGlvbiI6IHsibG9uZ2l0dWRlIjogLTU1Ljc4NDk4LCAibGF0aXR1ZGUiOiAyMC44MDY3ODV9fQ==", # pragma: allowlist secret
#        "attributes":{
#          "observation_type":"ge",
#          "device_id":"003",
#          "outbound_config_id":"9243a5e3-b16a-4dbd-ad32-197c58aeef59",
#          "integration_id":"8311c4a5-ddab-4743-b8ab-d3d57a7c8212",
#          "tracing_context":"{}"
#        },
#          "messageId": "9155786613739819",
#          "message_id": "9155786613739819",
#          "publishTime": "2024-08-02T16:08:15.789Z",
#          "publish_time": "2024-08-02T16:08:15.789Z"
#        },
#      "subscription": "projects/MY-PROJECT/subscriptions/MY-SUB"
#    }'
