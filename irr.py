from arin import *


class IRR(Arin):
    def __init__(self):
        super().__init__()

    def create_route(self, prefix, asn, descr, admin_c, tech_c, mnt_by):
        body = f"""route6: {prefix}
origin: {asn}
descr: {descr}
admin-c: {admin_c}
tech-c: {tech_c}
mnt-by: {mnt_by}
source: ARIN"""
        req = requests.post(
            f'{self.url}/irr/route/{prefix}/{asn}?apikey={self.api_key}',
            headers=self.headers_rpsl,
            data=body,
        )
        return req

    def create_route6(self, prefix, asn, descr, admin_c, tech_c, mnt_by):
        body = f"""route6: {prefix}
origin: {asn}
descr: {descr}
admin-c: {admin_c}
tech-c: {tech_c}
mnt-by: {mnt_by}
source: ARIN"""
        req = requests.post(
            f'{self.url}/irr/route/{prefix}/{asn}?apikey={self.api_key}',
            headers=self.headers_rpsl,
            data=body,
        )
        return req

    def get_route_object(self, prefix, asn):
        get = requests.get(
            f'{self.url}/irr/route/{prefix}/{asn}?apikey={self.api_key}',
            headers=self.headers_rpsl
        )
        splitter = re.compile(r'^(\S+): +(.*)$')
        lines = get.text.split('\n')
        results = dict()
        for line in lines:
            match = splitter.findall(line)
            if match:
                results[match[0][0]] = match[0][1]
        return results

    def modify_route_object(self, prefix, asn, descr):
        existing = self.get_route_object(prefix, asn)
        body = f"""route: {prefix}
origin: {asn}
descr: {descr}
admin-c: {existing['admin-c']}
tech-c: {existing['tech-c']}
mnt-by: {existing['mnt-by']}
source: ARIN"""
        put = requests.put(
            f'{self.url}/irr/route/{prefix}/{asn}?apikey={self.api_key}',
            headers=self.headers_rpsl,
            data=body
        )
        return put

    def modify_route6_object(self, prefix, asn, descr):
        existing = self.get_route_object(prefix, asn)
        body = f"""route: {prefix}
origin: {asn}
descr: {descr}
admin-c: {existing['admin-c']}
tech-c: {existing['tech-c']}
mnt-by: {existing['mnt-by']}
source: ARIN"""
        put = requests.put(
            f"{self.url}/irr/route/{prefix}/{asn}?apikey={self.api_key}",
            headers=self.headers_rpsl,
            data=body
        )
        return put

    def delete_route_object(self, prefix, asn):
        delete = requests.delete(
            f"{self.url}/irr/route/{prefix}/{asn}?apikey={self.api_key}",
            headers=self.headers_rpsl
        )
        return delete
