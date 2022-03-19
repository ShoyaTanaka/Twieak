import sys
import webbrowser
while True:
    print(sys.argv)
    webbrowser.open(sys.argv[1])
    a = input("ブラウザのタブを閉じてしまった場合はなんらかのキーを押すと再度開きます。")