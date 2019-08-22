class Login(Base):
    def test_login(self):
        url = self.RC.BASE_URL + "/collect/v1/login"
        data = {"next_url": "/account/v2/login".format(self.RC.LOGIN_URL)}
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        rv = self.session.get(url, params=data, allow_redirects=False, verify=False)
        url = self.RC.LOGIN_URL + "/account/v2/login"
        data = {"client_id": self.RC.CLIENT_ID, "next": rv.next.url, "type": 3}
        data1 = {"username": "13011112222", "password": "dev"}
        self.session.post(url, data=data1, params=data)
        url2 = self.RC.LOGIN_URL + "/account/v2/authorize"
        params = {"client_name": "采集数据平台",
                  "client_id": self.RC.CLIENT_ID,
                  "client_secret": self.RC.CLIENT_SECRET,
                  "redirect_uri": "{}/collect/v1/login/callback".format(self.RC.BASE_URL),
                  "response_type": "code",
                  "scope": "default",
                  "state": "aHR0cHM6Ly9iZWVoaXZlLXRlc3Quenpjcm93ZC5jb20uY24vIy9sb2dpbg==",
                  "confirm": "yes"}
        rv2 = self.session.get(url2, params=params, allow_redirects=False)
        url3 = rv2.headers["location"]
        rv3 = self.session.get(url3, verify=False)
        if rv3.status_code == 200:
            if self.session.get(
                    self.RC.BASE_URL + "/collect/v1/jobs?page=1&per_page=15&operation=0&ride=0&over=1").status_code == 200:
                flag = True
                msg = "登录成功"
            else:
                flag = False
                msg = "登录失败"
        else:
            flag = False
            msg = "登录失败"
        self.log.info(msg)
        self.assertTrue(flag, msg)
