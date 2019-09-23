from requests import request
import os

API_TEST_HOST = os.getenv("API_TEST_HOST", "")
API_TEST_COOKIES = os.getenv("API_TEST_COOKIES","")


class ApiTest:
    def __init__(self, apis):
        self.cookies = {"BrainAuth": API_TEST_COOKIES}
        self.apis = apis

    def datasets_search(self):
        url = self.apis["dataset_search"][1]
        response = request(self.apis["dataset_search"][0],
                           url, cookies=self.cookies)
        res = self.verify_response(url, response)
        if res:
            assert res["dataset_name"] != ""
            print("API: %s pass" % url)
        else:
            print("response is None")

    def dataset_detail(self):
        url = self.apis["dataset_detail"][1]
        response = request(self.apis["dataset_detail"][0],
                           url, cookies=self.cookies)
        res = self.verify_response(url, response)
        if res:
            assert len(res["data"]) >= 2
            print("API: %s pass" % url)
        else:
            print("response is None")
    def get_accesskey(self):
        url = self.apis["get_accesskey"][1]
        response = request(self.apis["get_accesskey"][0],
                           url, cookies=self.cookies)
        res = self.verify_response(url, response)
        if res:
            assert res["access_key_secret"] == ""
            print("API: %s pass" % url)
        else:
            print("response is None")

    def reset_accesskey(self):
        url = self.apis["reset_accesskey"][1]
        response = request(self.apis["reset_accesskey"][0],
                           url, cookies=self.cookies)
        res = self.verify_response(url, response)
        if res:
            assert res["access_key_secret"] != ""
            print("API: %s pass" % url)
        else:
            print("response is None")

    def get_tag_tree(self):
        url = self.apis["get_tag_tree"][1]
        response = request(self.apis["get_tag_tree"][0],
                           url, cookies=self.cookies)
        res = self.verify_response(url, response)
        if res:
            assert len(res["tag_trees"]) > 0
            print("API: %s pass" % url)
        else:
            print("response is None")

    def get_dataset_versions(self):
        url = self.apis["get_dataset_versions"][1]
        response = request(self.apis["get_dataset_versions"][0],
                           url, cookies=self.cookies)
        res = self.verify_response(url, response)
        if res:
            assert res["pagination"].get("total") > 0
            print("API: %s pass" % url)
        else:
            print("response is None")

    def get_rawdataset_paths(self):
        url = self.apis["get_rawdataset_paths"][1]
        response = request(self.apis["get_rawdataset_paths"][0],
                           url, cookies=self.cookies)
        res = self.verify_response(url, response)
        if res:
            assert res["pagination"].get("total") == 0
            print("API: %s pass" % url)
        else:
            print("response is None")

    def get_rawdatasets(self):
        url = self.apis["get_rawdatasets"][1]
        response = request(self.apis["get_rawdatasets"][0],
                           url, cookies=self.cookies)
        res = self.verify_response(url, response)
        if res:
            assert res["pagination"].get("total") > 0
            print("API: %s pass" % url)
        else:
            print("response is None")

    def verify_response(self, api, response):
        if "身份认证" in response.text:
            print("需要身份认证！！！")
            return
        res = None
        try:
            res = response.json()
            if "error" in res.keys():
                print("response error in api: %s" % api)
            # print(res)
        except Exception as e:
            print("failed req URL: %s, error:" % api, e)
        finally:
            return res

    def test_run(self):
        self.datasets_search()
        self.dataset_detail()
        self.reset_accesskey()
        self.get_accesskey()

        self.get_tag_tree()
        self.get_dataset_versions()
        self.get_rawdataset_paths()
        self.get_rawdatasets()


if __name__ == '__main__':
    apis = {"dataset_search": ["GET", API_TEST_HOST + "/api/v1/datasets/1"],
            "dataset_detail": ["GET",
                               API_TEST_HOST + "/api/v1/datasets?offset=0&limit=10&tags=2&category=-1&sorts"],
            "reset_accesskey": ["POST",
                                API_TEST_HOST + "/api/v1/users/current/accesskey/_reset"],
            "get_accesskey": ["GET", API_TEST_HOST + "/api/v1/users/current/accesskey"],
            "get_app_version": ["GET", API_TEST_HOST + "/api/v1/version"],
            "get_tag_tree": ["GET", API_TEST_HOST + "/api/v1/tags-tree?&offset=0&limit=20"],
            "get_dataset_versions": ["GET", API_TEST_HOST + "/api/v1/datasets/1/versions?&offset=0&limit=20"],
            "get_rawdataset_paths": ["GET", API_TEST_HOST + "/api/v1/versions/860/rawdataset-paths?offset=0&limit=20"],
            "get_rawdatasets": ["GET", API_TEST_HOST + "/api/v1/raw-datasets"],
            }

    t = ApiTest(apis)
    t.test_run()