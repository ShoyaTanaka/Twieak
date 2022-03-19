##########ライブラリを使用したサンプル。

from Twieak import Twieak
search = Twieak(callback_port=60020,consumer_key_secret="bWrX5ecmyJu08p7jhyGYrMTAxSD7JLet0pqbk634SKot9lLhgH",consumer_key="5stJkr3agDoqK418ZfkFoZLeC")
while True:
    print("1:片思い/思われをブロ解")
    print("2:直近3000ツイを消去(時間経過させないとダメかも)")
    print("3:全てのfollower/followee/tweetを抹消")
    print("4:終了")
    try:
        select = int(input("どれにする？(数字で)"))
        if not 1 <= select <= 4:
            print("値が不適切")
        elif select == 1:
            status = search.terminate_only_follows_followers()
        elif select == 2:
            stat = search.terminate_tweets()
            print(stat)
            if stat[0] == 0:
                print("正常に削除できました。")
            elif stat[0] == 1:
                print("api制限に引っ掛かりました。時間を置いて再度試してみてください。")
            else:
                print("内部エラー:"+stat[2])
        elif select == 3:
            yn = input("全ツイート、フォロー/フォロワーが消えるけど本当にいい？[y/n]")
            if yn.lower() == "y":
                sign = input("今までのツイートが全て消え、そしてフォローしていた人、フォローされていた人も消えます。この操作は取り消せません。本当によろしいですか?[y/n]")
                if sign.lower() == "y":

                    [fav_st,tw_st,ff_st] = search.goodbye_all_activities()
                    if tw_st[0] == 1:
                        print("ツイートの数が多すぎます。直近3000ツイートであれば削除可能ですが、完全削除したい場合にはツイートアーカイブを用いる必要があります。どうしますか？")
                        while True:
                            try:
                                a = int(input("1:直近3000ツイートを削除,2:全ツイートを削除,3:ツイート削除をスキップ"))
                                assert 1 <= a <= 3
                                if a == 1:
                                    stat = search.terminate_tweets()
                                    if stat == 0:
                                        print("直近3000ツイートの削除に成功しました。")
                                    elif stat == 1:
                                        print("api制限に引っ掛かりました。")
                                elif a == 2:
                                    while True:
                                        direct = input("tweets.jsファイルを指定してください。(中断したい場合はabortと入力):")
                                        if direct == "abort":
                                            print("中止しました。")
                                        else:
                                            status = search.terminate_tweets(jsf=direct,limit="ALL")
                                            if status[0] == 3:
                                                print("ファイルを開けませんでした。中断します。")
                                                break
                                else:
                                    print("ツイート削除をスキップしました。")
                                break
                            except ValueError or AssertionError:
                                print("有効な数字を入力してください。")
                else:
                    print("中止しました。")
            else:
                print("中止しました。")
        elif select == 4:
            print("終了します...")
            break
    except ValueError:
        print("数字にしてください。")
