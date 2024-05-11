import json
import logging


class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def append(self, data):
        if len(data.keys()) == 1 and self.tail:
            self.tail.data['written'] += data['written']
        else:
            new_node = Node(data)
            if not self.head:
                self.head = new_node
                self.tail = new_node
            else:
                self.tail.next = new_node
                self.tail = new_node

    def print_list(self):
        current_node = self.head
        while current_node:
            print(current_node.data)
            current_node = current_node.next

    def get_all_tokens(self):
        token_list = []
        current_node = self.head
        while current_node:
            token_list.append(current_node.data)
            current_node = current_node.next
        return token_list

    def get_continues_tokens(self, node=None):
        if not node:
            node = self.head
        try:
            current_node = node
            tokens = []
            while current_node:
                tokens.append(current_node.data)
                if not current_node.next:
                    break
                if current_node.data['endtime'] != current_node.next.data['starttime']:
                    break
                current_node = current_node.next
        except Exception as e:
            logging.error(e)
            logging.info('current_node', node)
        return tokens, current_node.next if current_node else None


def json_to_linkedlist(data):
    json_data = json.loads(data)
    tokens = json_data['results'][0]['tokens']

    linked_list = LinkedList()
    for token in tokens:
        linked_list.append(token)

    return linked_list


def calculate_total_weighted_confidence(tokens):
    try:
        total_weighted_confidence = sum(
            (token['endtime'] - token['starttime']) * token['confidence'] for token in tokens)
    except Exception as e:
        logging.error('calculate_total_weighted_confidence error', e)
    return total_weighted_confidence


def compare_segments(linked_list1, linked_list2):
    result = []
    node1, node2 = linked_list1.head, linked_list2.head

    while node1 and node2:
        segment1, next1 = linked_list1.get_continues_tokens(node1)
        segment2, next2 = linked_list2.get_continues_tokens(node2)

        if segment1[0]['starttime'] - segment2[0]['starttime'] > 200:
            segment2, next2 = linked_list2.get_continues_tokens(next2)
        elif segment2[0]['starttime'] - segment1[0]['starttime'] > 200:
            segment1, next1 = linked_list1.get_continues_tokens(next1)

        conf1 = calculate_total_weighted_confidence(segment1)
        conf2 = calculate_total_weighted_confidence(segment2)

        if conf1 > conf2:
            result.append(segment1)
        else:
            result.append(segment2)

        node1, node2 = next1, next2

        if node1 is None and node2 is None:
            break
        elif node1 is None or node2 is None:
            break

    return result


def get_final_result(result1, result2) -> dict:
    model1_token_linklist = json_to_linkedlist(result1)
    model2_token_linklist = json_to_linkedlist(result2)

    result = compare_segments(model1_token_linklist, model2_token_linklist)

    result_format = {}
    result_format['text'] = ''
    result_format['results'] = [{}]
    result_format['results'][0]['tokens'] = []

    for segment in result:
        for token in segment:
            result_format['results'][0]['tokens'].append(token)
            result_format['text'] += token.get('written', '') + ' '

    result_format['results'][0]['confidence'] = 0.0

    return result_format


if __name__ == '__main__':
    result1 = {
        "code": "",
        "message": "",
        "results": [
            {
                "confidence": 0.99975,
                "endtime": 12100,
                "rulename": "",
                "starttime": 0,
                "tags": [],
                "text": "No. 11.How often do you play tennis?A.I took a train.B.once a month.See.in a park.",
                "tokens": [
                    {
                        "confidence": 0.95,
                        "endtime": 660,
                        "spoken": "No.",
                        "starttime": 320,
                        "written": "No."
                    },
                    {
                        "confidence": 1,
                        "endtime": 1280,
                        "spoken": "eleven",
                        "starttime": 660,
                        "written": "11"
                    },
                    {
                        "written": "."
                    },
                    {
                        "confidence": 0.95,
                        "endtime": 2150,
                        "spoken": "How",
                        "starttime": 1930,
                        "written": "How"
                    },
                    {
                        "confidence": 1,
                        "endtime": 2390,
                        "spoken": "often",
                        "starttime": 2150,
                        "written": "often"
                    },
                    {
                        "confidence": 1,
                        "endtime": 2490,
                        "spoken": "do",
                        "starttime": 2390,
                        "written": "do"
                    },
                    {
                        "confidence": 1,
                        "endtime": 2590,
                        "spoken": "you",
                        "starttime": 2490,
                        "written": "you"
                    },
                    {
                        "confidence": 1,
                        "endtime": 2830,
                        "spoken": "play",
                        "starttime": 2590,
                        "written": "play"
                    },
                    {
                        "confidence": 1,
                        "endtime": 3470,
                        "spoken": "tennis",
                        "starttime": 2830,
                        "written": "tennis"
                    },
                    {
                        "written": "?"
                    },
                    {
                        "confidence": 0.79,
                        "endtime": 4840,
                        "spoken": "A",
                        "starttime": 4280,
                        "written": "A"
                    },
                    {
                        "written": "."
                    },
                    {
                        "confidence": 1,
                        "endtime": 5560,
                        "spoken": "I",
                        "starttime": 5360,
                        "written": "I"
                    },
                    {
                        "confidence": 1,
                        "endtime": 5780,
                        "spoken": "took",
                        "starttime": 5560,
                        "written": "took"
                    },
                    {
                        "confidence": 1,
                        "endtime": 5820,
                        "spoken": "a",
                        "starttime": 5780,
                        "written": "a"
                    },
                    {
                        "confidence": 1,
                        "endtime": 6440,
                        "spoken": "train",
                        "starttime": 5820,
                        "written": "train"
                    },
                    {
                        "written": "."
                    },
                    {
                        "confidence": 0.72,
                        "endtime": 7770,
                        "spoken": "B",
                        "starttime": 7130,
                        "written": "B"
                    },
                    {
                        "written": "."
                    },
                    {
                        "confidence": 0.58,
                        "endtime": 8650,
                        "spoken": "once",
                        "starttime": 8270,
                        "written": "once"
                    },
                    {
                        "confidence": 1,
                        "endtime": 8690,
                        "spoken": "a",
                        "starttime": 8650,
                        "written": "a"
                    },
                    {
                        "confidence": 0.99,
                        "endtime": 9390,
                        "spoken": "month",
                        "starttime": 8690,
                        "written": "month"
                    },
                    {
                        "written": "."
                    },
                    {
                        "confidence": 0.55,
                        "endtime": 10630,
                        "spoken": "See",
                        "starttime": 9930,
                        "written": "See"
                    },
                    {
                        "written": "."
                    },
                    {
                        "confidence": 0.62,
                        "endtime": 11340,
                        "spoken": "in",
                        "starttime": 11180,
                        "written": "in"
                    },
                    {
                        "confidence": 1,
                        "endtime": 11420,
                        "spoken": "a",
                        "starttime": 11340,
                        "written": "a"
                    },
                    {
                        "confidence": 0.95,
                        "endtime": 12000,
                        "spoken": "park",
                        "starttime": 11420,
                        "written": "park"
                    },
                    {
                        "written": "."
                    }
                ]
            }
        ],
        "text": "No. 11.How often do you play tennis?A.I took a train.B.once a month.See.in a park.",
        "utteranceid": "20240501/21/018f3423547d0a30369794c1_20240501_213121"
    }

    result2 = {
        "code": "",
        "message": "",
        "results": [
            {
                "confidence": 0.931,
                "endtime": 12084,
                "rulename": "",
                "starttime": 0,
                "tags": [],
                "text": "ナンプラーパン葉を煎じたピチャイ氏ちょっとB星へのパーク",
                "tokens": [
                    {
                        "confidence": 0.63,
                        "endtime": 896,
                        "spoken": "なんぷらー",
                        "starttime": 336,
                        "written": "ナンプラー"
                    },
                    {
                        "confidence": 0.68,
                        "endtime": 1280,
                        "spoken": "ぱん",
                        "starttime": 896,
                        "written": "パン"
                    },
                    {
                        "confidence": 0.42,
                        "endtime": 2114,
                        "spoken": "は",
                        "starttime": 1938,
                        "written": "葉"
                    },
                    {
                        "confidence": 0.33,
                        "endtime": 2274,
                        "spoken": "を",
                        "starttime": 2114,
                        "written": "を"
                    },
                    {
                        "confidence": 0.22,
                        "endtime": 2626,
                        "spoken": "せんじ",
                        "starttime": 2274,
                        "written": "煎じ"
                    },
                    {
                        "confidence": 0.01,
                        "endtime": 2738,
                        "spoken": "た",
                        "starttime": 2674,
                        "written": "た"
                    },
                    {
                        "confidence": 0.12,
                        "endtime": 3170,
                        "spoken": "ぴちゃい",
                        "starttime": 2738,
                        "written": "ピチャイ"
                    },
                    {
                        "confidence": 0.4,
                        "endtime": 3474,
                        "spoken": "し",
                        "starttime": 3170,
                        "written": "氏"
                    },
                    {
                        "confidence": 0.41,
                        "endtime": 6044,
                        "spoken": "ちょっと",
                        "starttime": 5612,
                        "written": "ちょっと"
                    },
                    {
                        "confidence": 0.94,
                        "endtime": 7746,
                        "spoken": "びー",
                        "starttime": 6850,
                        "written": "B"
                    },
                    {
                        "confidence": 0.61,
                        "endtime": 10594,
                        "spoken": "せい",
                        "starttime": 9938,
                        "written": "星"
                    },
                    {
                        "confidence": 0.49,
                        "endtime": 11412,
                        "spoken": "への",
                        "starttime": 11172,
                        "written": "への"
                    },
                    {
                        "confidence": 0.94,
                        "endtime": 11940,
                        "spoken": "ぱーく",
                        "starttime": 11412,
                        "written": "パーク"
                    }
                ]
            }
        ],
        "text": "ナンプラーパン葉を煎じたピチャイ氏ちょっとB星へのパーク",
        "utteranceid": "20240501/21/018f342354820a30343894c8_20240501_213121"
    }
    final_result = get_final_result(result1, result2)
    print(json.dumps(final_result))
