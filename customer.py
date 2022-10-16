from arin import *


class Customer(Arin):
    def _init__(self):
        super().__init__()

    def create_recipient_customer(
            self,
            parent_net_handle: str,
            customer_payload: dict,
    ):
        """
        https://www.arin.net/resources/manage/regrws/methods/#create-recipient-customer

        :param parent_net_handle:
        :param customer_payload:
        :return:
        """
        url = f"{self.url}/net/{parent_net_handle}/customer?apikey={self.api_key}"
        template = self.env.get_template('customer_payload.jinja2')
        rendered_payload = template.render(**customer_payload)
        print(url)
        print(rendered_payload)
        r = requests.post(
            url=url,
            headers=self.headers,
            data=rendered_payload
        )
        doc = xmltodict.parse(r.text)
        print(doc)
        return r.status_code, json.dumps(doc)
