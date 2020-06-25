clear
capture log close
local root "D:\code\tt_no1\huizong_in_browser\data"
log using "`root'\\`1'.log", replace
display "hello tiaotiao!"
insheet using "`root'\\`1'.csv"
// describe
// summarize
// codebook
display "tiaotiao 要开始做LOS回归啦！"
local x_list "观看总人数 峰值人数 粉丝增量 点赞增量 评论增量 转发增量 关注增量 粉丝团增量 送礼UV"
local y_list "销量 销售额 粉丝总量 点赞总数 平均评论 平均转发 音浪收入"
foreach x of local x_list{
	foreach y of local y_list{
		display "tiaotiao 针对 `x', `y'" "做了LOS回归，如下："
		regress `x' `y'
	}
}
log close
exit