from django.core.urlresolvers import reverse_lazy
from django.test import TestCase

class TestCalls(TestCase):
    def setUp(self):
        self.index_url = 'index'
        self.alarm_url = 'alarm'
    def test_call_index_loads(self):
        path = str(reverse_lazy(self.index_url))
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,'form.html')
    def test_call_alarm_error(self):
        path = str(reverse_lazy(self.alarm_url))
        value = '110011'
        params = {
            'func' : value
            }
        response = self.client.post(path, params)
        txt = "Too short input! Must me 7!"
        self.assertEqual(response.content, txt)
    def test_call_alarm_succeed(self):
        path = str(reverse_lazy(self.alarm_url))
        value = '11001100'
        params = {
            'func' : value
            }
        response = self.client.post(path, params)
        txt = "Diods alarmed! (" + value + ")"
        self.assertEqual(txt, response.content)

        
