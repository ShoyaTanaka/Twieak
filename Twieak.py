import os.path
import subprocess
import tweepy
from os import path
import socket
import platform

class Twieak:
    consumer_key = ""
    consumer_secret = ""
    access_token_secret = ""
    access_token = ""
    auth = ""
    whoami = ""
    whoami_status = ""
    url = "http://127.0.0.1:60020"  #現段階ではcallbackurlとしてループバックアドレスを指定しなければ動作しない。ここは後日修正する。
    def __init__(self, silent_init=False,callback_port=999999,file_dir="", access_token="", access_token_secret="",
                 information_accept=False,consumer_key="",consumer_key_secret=""):
        if not consumer_key_secret or not consumer_key:
            raise Exception("consumer_key or consumer_key_secret is not configured.")
        else:
            self.consumer_key = consumer_key
            self.consumer_secret = consumer_key_secret
        if callback_port == 999999:
            raise Exception("callback_port is not configured.")
        at_ats_array = ""
        if not silent_init:
            if file_dir == "":
                file_dir = "tokens.txt"
            if path.exists(file_dir):
                f = open(file_dir,mode="r",encoding="utf-8")
                at_ats_array = f.readlines()
                f.close()
            auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret, self.url)
            i = 0
            while i < len(at_ats_array):
                if at_ats_array[i] == "\n":
                    del at_ats_array[i]
                else:
                    i += 1
            print(at_ats_array)
            if len(at_ats_array) == 0 and not silent_init:
                [access_token,access_token_secret] = self.fetch_authorization(portnumber=callback_port)
                auth.set_access_token(access_token,access_token_secret)
                self.api = tweepy.API(auth,wait_on_rate_limit=True)
                with open(file_dir, mode="w", encoding="utf-8") as f:
                    print(access_token,end=",", file=f)
                    print(access_token_secret, file=f)
                    try:
                        self.whoami = self.api.user_timeline(count=1)[0].user.screen_name
                        self.whoami_status = self.api.get_user(screen_name=self.whoami)
                    except IndexError:
                        self.api.update_status("@tos au")
                        self.whoami = self.api.user_timeline(count=1)[0].user.screen_name
                        self.api.destroy_status(self.api.user_timeline(count=1)[0].id)
            else:
                print("アカウントを選択")
                for x in range(0,len(at_ats_array)):
                    auth.set_access_token(at_ats_array[x].replace("\n","").split(",")[0], at_ats_array[x].replace("\n","").split(",")[1])
                    api = tweepy.API(auth)
                    try:
                        self.whoami = api.user_timeline(count=1)[0].user.screen_name
                    except IndexError:
                        api.update_status("@tos au")
                        self.whoami = api.user_timeline(count=1)[0].user.screen_name
                        api.destroy_status(api.user_timeline(count=1)[0].id)
                    print(str(x+1)+":"+self.whoami)
                print(str(len(at_ats_array)+1)+":アカウントを追加する")
                print(str(len(at_ats_array)+2)+":終了")
                while True:
                    while True:
                        try:
                            select = int(input("数字で入力してください:"))
                            break
                        except ValueError:
                            print("数字で入力してください")
                    if select == len(at_ats_array)+1:
                        [self.access_token,self.access_token_secret] = self.fetch_authorization(portnumber=callback_port)
                        auth.set_access_token(self.access_token,self.access_token_secret)
                        self.api = tweepy.API(auth,wait_on_rate_limit=True)
                        try:
                            self.whoami = api.user_timeline(count=1)[0].user.screen_name
                        except IndexError:
                            api.update_status("@tos au")
                            self.whoami = api.user_timeline(count=1)[0].user.screen_name
                            api.destroy_status(api.user_timeline(count=1)[0].id)
                        with open(file_dir,mode="a+",encoding="utf-8") as f:
                            print(self.access_token,end=",",file=f)
                            print(self.access_token_secret,end="",file=f)
                        break
                    elif select == len(at_ats_array)+2:
                        print("終了します")
                        exit(0)
                    elif not 0 < select <= len(at_ats_array):
                        print("範囲外の数字です。選び直してください。")
                    else:
                        auth.set_access_token(at_ats_array[select-1].replace("\n", "").split(",")[0],
                                                   at_ats_array[select-1].replace("\n", "").split(",")[1])
                        self.api = tweepy.API(auth,wait_on_rate_limit=True)
                        self.whoami_status = self.api.get_user(screen_name=self.whoami)
                        print("選択したアカウント:@"+self.whoami)
                        break
        else:
            if not information_accept:
                print("""information:Twieak is configured to silent initialize.If you don't make OAuth methods,
            it may cause some Errors so I recommend you enable interactive init.
            This information can be ignored by enabling information_accept in argument.""")
            if (not access_token or not access_token_secret):
                raise Exception("Twieak Error:Cannot initialize because silent_init is enable but access_token or secret is blank.")
            else:
                try:
                    auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret, self.url)
                    auth.set_access_token(access_token,access_token_secret)
                    #######API導通テスト############
                    test_api = tweepy.API(auth,wait_on_rate_limit=True)
                    test_api.user_timeline()
                    self.api = test_api
                except tweepy.errors.Unauthorized:
                    if not consumer_key:
                        raise Exception("Twieak Error:Maybe invalid access token or secret.")
                    else:
                        raise Exception("Twieak Error:Confirm consumer_key,Secret,or access_token(and secret).")
        return
    #########コンストラクタ終わり

    def gen_only_follow_follower_list(self,screenname=False) -> [{int}]:
        #[フォローのみ,フォローされているのみ、フォロー/フォロワー]のリストで返す。screen_name=Trueにした場合は@以降のIDを返す。
        followers = []
        follows = []
        followers_ids = tweepy.Cursor(self.api.get_followers, id=self.whoami, cursor=-1).items()
        for followers_id in followers_ids:
            followers.append(followers_id)
        follows_ids = tweepy.Cursor(self.api.get_friends, id=self.whoami, cursor=-1).items()
        for follows_id in follows_ids:
            follows.append(follows_id)
        if screenname:
            for i,value in enumerate(followers):
                followers[i] = value.screen_name
            for i,value in enumerate(follows):
                follows[i] = value.screen_name
        else:
            for i,value in enumerate(followers):
                followers[i] = value.id
            for i,value in enumerate(follows):
                follows[i] = value.id
        followers = set(followers)
        follows = set(follows)
        follow_follower = follows & followers
        only_follower = followers - follow_follower
        only_follow = follows - follow_follower
        follow_follower = list(follow_follower)
        only_follower = list(only_follower)
        only_follow = list(only_follow)
        return [only_follow, only_follower, follow_follower]

    def terminate_only_follows_followers(self) -> [int,str]:
        [only_follow,only_follower,follow_follower] = self.gen_only_follow_follower_list()
        try:
            for follow in only_follow:
                print(follow)
                self.api.destroy_friendship(user_id=follow)
            for follower in only_follower:
                self.api.create_block(user_id=follower)
                self.api.destroy_block(user_id=follower)
            return [0,"OK"]
        except tweepy.TweepyException as e:
            return [1,str(e)]
        except Exception as e:
            return [2,str(e)]
    def terminate_all_follow_followers(self) -> [int,str]:
        [only_follow,only_follower,follow_follower] = self.gen_only_follow_follower_list()
        try:
            for follow in only_follow:
                self.api.destroy_friendship(user_id=follow)
            for follower in only_follower:
                self.api.create_block(user_id=follower)
                self.api.destroy_block(user_id=follower)
            for common in follow_follower:
                self.api.create_block(user_id=common)
                self.api.destroy_block(user_id=common)
            return [0,"OK"]
        except tweepy.TweepyException as e:
            return [1,e]
        except Exception as e:
            return [2,e]

    def destroy_favorites(self,limit=200) -> [int,int,str]: #成功失敗,api制限で止まっている場合はfavの消去数を、それ以外で停止した場合はエラーコードをstrで返す
        target = self.api.get_favorites()
        success_delete = 0
        goal = limit
        if limit == "ALL":
            goal = self.whoami_status.favourites_count
        try:
            while success_delete < goal:
                target = self.api.get_favorites()
                for x in target:
                    self.api.destroy_favorite(x.id)
                    success_delete += 1
            return [0,success_delete,"OK."]
        except tweepy.TweepyException as e:
            return [1,success_delete,str(e)]
        except Exception as e:
            return [2,success_delete,str(e)]

    def terminate_tweets(self,jsf=None,limit=3000,since=0,until=0) -> [int,int,str]:
        #####ツイート数が多すぎてそのままでは削除できない場合1を、正常に成功すれば0を、API制限に引っ掛かれば2を返す。何らかの異常が起きれば3,errorコードを返す
        goal = limit
        i = 0
        flag = 0
        bef = 0
        print(self.whoami_status)
        if limit == "ALL":
            goal = self.whoami_status.statuses_count
        elif limit > self.whoami_status.statuses_count:
            goal = self.whoami_status.statuses_count
        if (goal > 3000) and not zip:
            return [1,0,"too many tweets without using zip."]
        elif jsf and path.exists(jsf):
            try:
                f = open(jsf,mode="r",encoding="utf-8")
                f.close()
            except:
                return [3,0,"cannot open file."]
            with open(jsf,mode="r",encoding="utf-8") as f:

                target = []
                with open("tweet.json", "r") as f:
                    data = f.readline()
                    while data:
                        if (data[0:12] == "      \"id\" :"):
                            target.append(data[14:].replace("\",\n", ""))
                        data = f.readline()

                for twid in target:
                    if until == 0:
                        until = self.api.user_timeline(self.whoami)[0].id
                    try:
                        if since < int(twid) < until:
                            self.api.destroy_status(id=int(twid))
                        i += 1
                    except tweepy.errors.Forbidden:
                        self.api.unretweet(id=twid)
                    except tweepy.TweepyException as e:
                        return [1,i,str(e)]
                    except Exception as e:
                        return [2,i,str(e)]
            return [0,i,"all tweets deleted."]
        elif jsf and not path.exists(jsf):
            return [3,0,"no such file."]
        else:
            i = 0
            print(goal)
            try:
                while i < goal-1:

                    print("loop")
                    """                  if flag == 1:
                                          break
                                      if not bef == i:
                                          bef = i
                                          flag = 0
                                      else:
                                          flag = 1"""
                    tweets = self.api.user_timeline(count=200)
                    for text in tweets:
                        i += 1
                        self.api.destroy_status(text.id)
                return [0, i, "OK"]
            except tweepy.TweepyException as e:
                return [1, i, str(e)]
            except Exception as e:
                return [2, i, str(e)]

    def goodbye_all_activities(self) -> [int]:
        #全ての履歴を抹消します。
        print("いいねを削除中...")
        fav_st = self.destroy_favorites(limit="ALL")
        print("終了:status"+str(fav_st[0]))
        print("ツイートを削除中...")
        tw_st = self.terminate_tweets(limit="ALL")
        print("ffを削除中...")
        ff_st = self.terminate_all_follow_followers()
        return [fav_st,ff_st,tw_st]
    def extract_raw_tweep_api(self):
        return self.api
    def fetch_authorization(self,portnumber) ->[str]:
        #return [access_token,access_token_secret]
        #class内にあるconsumer_key,consumer_secret,urlを用いて認証し認証後のaccess token,access token secretを返します。
        if not -1 < portnumber < 65536:
            raise Exception("Port Error:invalid port number.")
        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret, self.url)
        auth_url = auth.get_authorization_url()
        port = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        flag = False
        while True:
            try:
                port.bind(("127.0.0.1", portnumber))
                break
            except socket.error as e:
                if not flag:
                    print("少しお待ちを...")
                    flag = True
        if (platform.platform().split("-")[0] != "Windows"):
            browse = subprocess.Popen("exec python3 openbrowser.py " + auth_url,shell=True)
        else:
            browse = subprocess.Popen("python3 "+os.path.dirname(__file__)+"/openbrowser.py "+auth_url)
        port.listen()
        client, client_address = port.accept()
        browse.terminate()
        st = str(client.recv(8192), encoding="utf-8")
        client.close()
        oauth_token = st.split()[1].split("=")[1].split("&")[0]
        oauth_verifer = st.split()[1].split("=")[2]
        auth.request_token['oauth_token'] = oauth_token
        auth.request_token['oauth_token_secret'] = oauth_verifer
        auth.get_access_token(oauth_verifer)
        return [auth.access_token,auth.access_token_secret]
