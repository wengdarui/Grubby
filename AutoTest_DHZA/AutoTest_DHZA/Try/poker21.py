"""
游戏规则
1. 玩家：两个角色 （电脑/人类） 电脑是庄家
2. 游戏开始的时,电脑和玩家分别获取两张底牌,庄家暴露一张牌
3. 人类玩家优先根据自己手上的牌决定是否继续要牌， 如果要，则在牌堆中抽取一张牌。此时判断胜负。超过21点就输了
4. 如果人类玩家不要牌了，那么电脑要牌
    4.1 电脑一直要牌，直到比玩家大则停止
    4.2 设置阀值，超过阀值就要，低于就不要
5. 循环3、4
6、完成一轮游戏时，人类玩家决定是否继续下一轮
7、牌堆中的牌不够一轮时，则自动结束

计算规则
2、3、4、5、6、7、8、、9、10 是正常点数，J Q K 都算10点
A 先当做11计算，如果总分大于21，则当做1计算，如果总分小于21，则当做11点计算
"""
"""
程序的功能模块
洗牌： 随机排序
发牌： 初始化：一下两张
        要牌，一下一张
计分： A 特殊
胜负判断： 比较大小
是否要牌
继续还是退出，是否玩下一轮
"""
# shuffle 的作用是随机打乱列表
from random import shuffle
import random
# nump的作用记录分数
import  numpy
from sys import exit

#扑克牌列表
playing_cards = {
    "♥A": 1,"♥2": 2,"♥3": 3,"♥4": 4,"♥5": 5,"♥6": 6,"♥7": 7,"♥8": 8,"♥9": 9,"♥10": 10,
    "♥J": 10,"♥Q": 10,"♥K": 10,
    "♠A": 1,"♠2": 2,"♠3": 3,"♠4": 4,"♠5": 5,"♠6": 6,"♠7": 7,"♠8": 8,"♠9": 9,"♠10": 10,
    "♠J": 10,"♠Q": 10,"♠K": 10,
    "♦A": 1,"♦2": 2,"♦3": 3,"♦4": 4,"♦5": 5,"♦6": 6,"♦7": 7,"♦8": 8,"♦9": 9,"♦10": 10,
    "♦J": 10,"♦Q": 10,"♦K": 10,
    "♣A": 1,"♣2": 2,"♣3": 3,"♣4": 4,"♣5": 5,"♣6": 6,"♣7": 7,"♣8": 8,"♣9": 9,"♣10": 10,
    "♣J": 10,"♣Q": 10,"♣K": 10,
}
#扑克牌名字
poker_name = list(playing_cards.keys())
#有几副扑克牌
poker_count = 1
#扑克牌总数
poker_list = poker_name * poker_count
#特殊分数扑克的列表
four_A = {"♥A","♠A","♦A","♣A"}
#计分器
total_score = numpy.array([0,0])
#游戏回合数
game_round = 1


def random_card(poker_list):
    """
    洗牌函数
    """
    shuffle(poker_list)


def start_init_two_poker(poker_list):
    """
    游戏初始化，电脑和玩家分别获取两张底牌
    :return:
    """
    return [poker_list.pop(random.randint(0,len(poker_list)-1)),
            poker_list.pop(random.randint(0,len(poker_list)-1))]


def if_get_next_poker():
    """
    是否继续要牌
    :return:
    """
    if_continue = input("是否继续要牌？（Y/N）#######：")
    if if_continue.upper() == "Y":
        return get_one_poker()
    elif if_continue.upper() == "N":
        print("玩家停止要牌")
        return False
    else:
        print("输入非法参数，请重新输入")
        return if_get_next_poker()


def get_one_poker():
    """
    发牌
    :return:
    """
    return poker_list.pop(random.randint(0,len(poker_list)-1))


def score_count(hand_poker):
    """
    计算手中的牌有多少分；poker_score为总分初始化变量；have_a 判断手中的牌是否包含A
    """
    poker_score = 0
    have_a = False

    #判断手中的牌是否有A，根据不同情况分别计算分数
    for poker in hand_poker:
        if poker in four_A:
            have_a = True
            break
        else:
            continue
    if have_a == False:
        for poker in hand_poker:
            poker_score += playing_cards[poker]
    elif have_a == True:
        for poker in hand_poker:
            poker_score += playing_cards[poker]
        if poker_score + 10 <= 21:
            poker_score = poker_score +10

    return poker_score


def who_win(you_score,pc_score):
    """
    判断输赢
    :param you_score:我的分数
    :param pc_score:电脑的分数
    :return:
    """
    if you_score > 21 and pc_score > 21 :
        print("平局了")
        return numpy.array([0,0])
    elif you_score > 21 and pc_score <= 21 :
        print("玩家输了，电脑赢了")
        return numpy.array([0,1])
    elif you_score <= 21 and pc_score > 21 :
        print("电脑输了，玩家赢了")
        return numpy.array([1, 0])
    elif you_score <= 21 and pc_score <= 21 :
        if you_score > pc_score:
            print("电脑输了，玩家赢了")
            return numpy.array([1, 0])
        elif you_score < pc_score:
            print("玩家输了，电脑赢了")
            return numpy.array([0, 1])
        else:
            print("平局了")
            return numpy.array([0, 0])


def continue_or_quit():
    """
    是否继续下一轮游戏
    :return:
    """
    if_next_round = input("还想要玩下一局么？（Y/N）#######：")
    if if_next_round.upper() == "Y":
        if len(poker_list) < 10 :
            print("剩余扑克少于10张，游戏结束")
            exit(1)
        else:
            return True
    elif if_next_round.upper() == "N":
        print("玩家不想玩了，游戏结束")
        exit(1)
    else:
        print("输入非法参数，请重新输入")
        return continue_or_quit()


def gogogo(poker_list):
    """
    游戏流程
    :param poker_list:
    :return:
    your_hand_poker 玩家手中的扑克
    computer_hand_poker 电脑手中的扑克
    """
    your_hand_poker = []
    computer_hand_poker = []
    # 初始化牌面
    your_init_poker = start_init_two_poker(poker_list)
    computer_init_poker = start_init_two_poker(poker_list)

    # 展示获得的扑克
    print("玩家获得是poker是{}和{}".format(your_init_poker[0],your_init_poker[1]))
    print("电脑获得是poker是？和{}".format(computer_init_poker[1]))

    # 荷官发牌
    your_hand_poker.extend(your_init_poker)
    computer_hand_poker.extend(computer_init_poker)

    # 计算初始化牌面分数
    score = numpy.array([score_count(your_hand_poker),score_count(computer_hand_poker)])

    # 根据初始化分数判断输赢，以及是否要牌
    if score[0] == 21 or score[1] == 21 :
        print("初始化出现21点")
        return who_win(score[0],score[1])
    else:
        while score[0] <= 21:
            get_new_poker = if_get_next_poker()
            if get_new_poker != False:
                #新发的牌拿到手里
                your_hand_poker.append(get_new_poker)
                print("目前手里的扑克牌是{}".format(your_hand_poker))
                score[0] = score_count(your_hand_poker)
                #判断分数大小
                if score[0] > 21 :
                    print("分数爆炸超过21点，电脑获胜")
                    return who_win(score[0],score[1])
                elif score[0] == 21 :
                    print("分数刚好21点，玩家获胜")
                    return who_win(score[0],score[1])
            #玩家不要牌了
            elif get_new_poker == False:
                #电脑一直要牌，直到比玩家大则停止
                while score[1] < score[0]:
                    computer_new_poker = get_one_poker()
                    computer_hand_poker.append(computer_new_poker)
                    score[1] = score_count(computer_hand_poker)

                print("电脑手里的牌是{}".format(computer_hand_poker))
                return who_win(score[0],score[1])
            else:
                continue



while True:
    input("请安任意键开始游戏~~~~~")
    print("目前是第{}轮游戏".format(game_round))
    #洗牌
    random_card(poker_list)
    # 开始游戏
    score = gogogo(poker_list)
    # 计算分数
    total_score = numpy.add (total_score,score)
    print("本轮游戏结束，总比分是玩家{} ： 电脑{}".format(total_score[0],total_score[1]))
    game_round +=1
    continue_or_quit()


