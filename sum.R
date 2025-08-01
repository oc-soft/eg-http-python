# stdinは標準入力
# ターミナルでRを起動した場合のデフォルトはターミナルからの入力
# 標準入力から空白区切りのデータを'charater'として読み取る
inp <- scan("stdin", what = 'character')
# inpには"a" "2" "5,62"のようなデータが格納されている

tmp_data <- list()
for (item in inp) {
    # ','も区切り文字として認識したいのでinpの各要素をさらに分割する
    tmp_items <- scan(text = item, sep = ',', what = 'character') 
    for (tmp_item in tmp_items) {
        # tmp_itemは'character'なので、数値に変換する。
        tmp_num = as.numeric(tmp_item)
        # a のようなデータはNAとなるので、NAではないデータを抽出する 
        if (!is.na(tmp_num)) {
            tmp_data[[length(tmp_data) + 1]] = tmp_num
        }
    }
}
# tmp_dataの総和を計算する
# printを使用すると[x] 6のような出力になる。
# sumはsum(2, 3, 4, 5)のように全てのデータを渡す必要がある。
# tmp_dataが (2, 3, 4)のようなリストの時、
# unlink(tmp_data) は 2 , 3, 4のようにtmp_dataの中身を展開する。
cat(sum(unlist(tmp_data)), "\n")

# vi: se ts=4 sw=4 et:
