import json
import re
import secrets

from helpers.headers_helper import UA

import httpx

response_javascript = """throw 'allowScriptTagRemoting is false.';
//#DWR-INSERT
//#DWR-REPLY
//#DWR-START#
(function() {
    if (!window.dwr)
        return;
    var dwr = window.dwr._[0];
    dwr.engine.remote.handleCallback("9", "0", "{\"data\":[{\"eventLocationName\":\"\u570B\u7ACB\u6545\u5BAE\u535A\u7269\u9662\",\"eventTime\":\"2025\/09\/12~2025\/09\/12\",\"eventType\":\"1\",\"idVal\":\"685dcbb326b324199c8d5112\",\"timeLeft\":\"4\",\"title\":\"\u300C\u7B56\u5C55\u4EBA\u966A\u6211\u770B\u5C55\u89BD\u300D\u6545\u5BAE\u5C08\u984C\u5C0E\u89BD\uFF1A\u7B46\u58A8\u898B\u771F\u7AE0\u2014\u6545\u5BAE\u66F8\u6CD5\u5C0E\u8CDE(2025-III)(\u7B2C3\u5834)\"},{\"eventLocationName\":\"\u570B\u7ACB\u6545\u5BAE\u535A\u7269\u9662\",\"eventTime\":\"2025\/09\/19~2025\/09\/19\",\"eventType\":\"1\",\"idVal\":\"685dcbb326b324199c8d5113\",\"timeLeft\":\"11\",\"title\":\"\u300C\u7B56\u5C55\u4EBA\u966A\u6211\u770B\u5C55\u89BD\u300D\u6545\u5BAE\u5C08\u984C\u5C0E\u89BD\uFF1A\u7881\u4EBA\u5F08\u4E8B\uFF0D\u53E4\u4EE3\u570D\u68CB\u6587\u5316(\u7B2C4\u5834)\"},{\"eventLocationName\":\"\u570B\u7ACB\u81FA\u7063\u6587\u5B78\u9928\u4E8C\u6A13\u7B2C\u4E8C\u6703\u8B70\u5BA4\",\"eventTime\":\"2025\/09\/13~2025\/09\/20\",\"eventType\":\"1\",\"idVal\":\"688d237a26b324477c8a1197\",\"timeLeft\":\"12\",\"title\":\"\u6587\u5B78\u597D\u5BA2\uFF1A\u5BA2\u8A9E\u66F8\u5BEB\u5DE5\u4F5C\u574A\"},{\"eventLocationName\":\"\u81FA\u7063\u6587\u5B78\u57FA\u5730 \u6085\u8B80\u9928\",\"eventTime\":\"2025\/09\/20~2025\/09\/20\",\"eventType\":\"1\",\"idVal\":\"68bca94426b32440a896442b\",\"timeLeft\":\"12\",\"title\":\"\u3010\u81FA\u7063\u6587\u5B78\u8655\u65B9\u7B8B\u2014\u5F15\u9304\u5287\u5834\u8AB2\u7A0B\u3011\u6210\u679C\u5C55\u6F14\"},{\"eventLocationName\":\"\u7B2C3\u5C55\u89BD\u5EF3\",\"eventTime\":\"2025\/09\/10~2025\/09\/21\",\"eventType\":\"1\",\"idVal\":\"68acf59d26b32415881739a0\",\"imgUrl\":\"\/e_new_upload\/task\/97b68b43-4653-4595-b7a0-a816818be7c5\/5358982abf714a3b0384bc9d2233ea7e72134596ae79696a96aabab5bcfec8e406d7a6fe696f0dc9aba1b41114ccab7fbe8379cf910b7c8c70d27885803beb9e\/8517cf196d82a3279849b7d35e1f6d0933a1f6d1.jpg\",\"timeLeft\":\"13\",\"title\":\"2025\u8F49\u5316\/\u7FFB\u8F49\u610F\u8C61\u806F\u5C55\"},{\"eventLocationName\":\"\u7F8E\u5B78\u7A7A\u9593\",\"eventTime\":\"2025\/09\/10~2025\/09\/21\",\"eventType\":\"1\",\"idVal\":\"68acf59d26b324158817399f\",\"imgUrl\":\"\/e_new_upload\/task\/97b68b43-4653-4595-b7a0-a816818be7c5\/1bf0090ae5b2100a4f4b7f3f57ae6c76cbff323598b5c24e1583ccea08d487944ae452618d862e43d9d918ce124e7c75c1776c17e3b18fa1d819d46af6bfafcb\/c4e552e26f14108f41407cb85192fd665acd0b34.jpg\",\"timeLeft\":\"13\",\"title\":\"\u6642\u5149\u6DEC\u934A,\u85DD\u5FC3\u7DBB\u653E\"},{\"eventLocationName\":\"\u81FA\u5317\u5E02\u4E2D\u5C71\u5802\",\"eventTime\":\"2025\/09\/13~2025\/09\/23\",\"eventType\":\"1\",\"idVal\":\"68af881226b32440a896409e\",\"timeLeft\":\"15\",\"title\":\"\u300C\u821E\u8E48\u5178\u7BC4\uFF0D\u5289\u9CF3\u5B78\u7684\u958B\u5275\u8207\u50B3\u627F\u300D- \u767E\u5E74\u7D00\u5FF5\u5C55:\u300C\u821E\u8E48\u5178\u7BC4\uFF0E\u8EAB\u97FB\u518D\u73FE\u300D\"},{\"eventLocationName\":\"\u5B5F\u7126\u756B\u574A\",\"eventTime\":\"2025\/09\/17~2025\/09\/28\",\"eventType\":\"1\",\"idVal\":\"6893b81a26b324477c8a1384\",\"imgUrl\":\"\/e_new_upload\/task\/6a4137d4-aae7-4e6d-838b-aaf069042338\/M9900418859\/0a04b2d475b67bf553086e9372f3f312e74e89e5.jpg\",\"timeLeft\":\"20\",\"title\":\"\u5200\u85DD\u96D9\u99A8 \u5B8B\u5D172025\u66F8\u9215\u7BC6\u500B\u5C55\"},{\"eventLocationName\":\"\u7F8E\u5B78\u7A7A\u9593\",\"eventTime\":\"2025\/09\/24~2025\/10\/06\",\"eventType\":\"1\",\"idVal\":\"68acf59d26b32415881739a2\",\"imgUrl\":\"\/e_new_upload\/task\/97b68b43-4653-4595-b7a0-a816818be7c5\/9a6f8ee006df95da6930007af379229093f6bad0933d0c1a531b86348a6f2c6ee622e2e25b0254316bcbe3a6c1f07fbb29ffd8ae109bd4bfff5f701d9a41b94c\/90a4ecc0e27fe979baf82cd7c8db102b70eb44ae.jpg\",\"timeLeft\":\"28\",\"title\":\"\u6232 \u5F69\"},{\"eventLocationName\":\"4\u5C55\u5EF3\",\"eventTime\":\"2025\/09\/18~2025\/10\/06\",\"eventType\":\"1\",\"idVal\":\"6893b71926b324477c8a1337\",\"timeLeft\":\"28\",\"title\":\"114\u5E74\u300C\u749E\u7389\u767C\u5149 \u5168\u570B\u85DD\u8853\u884C\u92B7\u6D3B\u52D5\u300D\u5F97\u734E\u4F5C\u54C1\u806F\u5C55(\u514D\u8CBB\u53C3\u89C0)\"},{\"eventLocationName\":\"3\u5C55\u5EF3\",\"eventTime\":\"2025\/09\/20~2025\/10\/06\",\"eventType\":\"1\",\"idVal\":\"68ba083826b32440a8964335\",\"timeLeft\":\"28\",\"title\":\"\u5982\u662F\u4E4B\u9593 \u30FB \u4E00\u5FC3\u5F18\u9AD4\u66F8\u6CD5\u85DD\u8853\u5C55(\u514D\u8CBB\u53C3\u89C0)\"},{\"eventLocationName\":\"\u81FA\u7063\u7576\u4EE3\u6587\u5316\u5BE6\u9A57\u5834 C-LA...\",\"eventTime\":\"2025\/09\/09~2025\/10\/06\",\"eventType\":\"1\",\"idVal\":\"688a564826b324477c8a1047\",\"timeLeft\":\"28\",\"title\":\"2025 TIPF \u53F0\u7063\u570B\u969B\u651D\u5F71\u7BC0\u2014\u2014\u96D9\u5C55\u5957\u7968\"}],\"pageLevel\":1}");
}
)();
//#DWR-END#"""


def test_get_raw_response():
    with httpx.Client() as client:
        headers = {
            "user-agent": UA.random,
            "referer": "https://cloud.culture.tw/frontsite/inquiry/eventInquiryAction.do?method=showEventList",
            "origin": "https://cloud.culture.tw",
            "host": "cloud.culture.tw",
            "content-type": "text/plain",
        }
        payload = {
            "callCount": "1",
            "nextReverseAjaxIndex": "0",
            "c0-scriptName": "eventInquiryAction",
            "c0-methodName": "doSearchEvent",
            "c0-id": "0",
            "c0-param0": "number:12",
            "c0-param1": "number:4",  # 頁數
            "c0-param2": "string:",
            "c0-param3": "number:6",  # 類別
            "c0-param4": "string:%E8%87%BA%E5%8C%97%E5%B8%82",  # 縣市
            "c0-param5": "string:2025%2F09%2F09",  # 不限 (填當下日期)
            "c0-param6": "string:",
            "c0-param7": "string:0",
            "c0-param8": "number:0",
            "c0-param9": "null:null",
            "c0-param10": "null:null",
            "batchId": "10",
            "instanceId": "0",
            "page": "/frontsite/inquiry/eventInquiryAction.do?method=showEventList",
            "scriptSessionId": secrets.token_hex(16),
        }
        response = client.post(
            "https://cloud.culture.tw/dwr/call/plaincall/eventInquiryAction.doSearchEvent.dwr",
            headers=headers,
            data=payload,
        )
    match_value = re.search(
        r'handleCallback\("[^"]+", "[^"]+", "(.*?)"\);', response.text, re.S
    )
    if match_value:
        json_str = match_value.group(1)
        json_unescaped_str = json_str.replace("\\\\", "\\").replace('\\"', '"')
        data = json.loads(json_unescaped_str)
        with open("qaq.json", "w+", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    else:
        print("QAQ re")
