import re


def autoWrap(text: str, maxCharactersNum: int) -> tuple:
    """ 自动给字符串换行, maxCharactersNum是text换算为1个宽度字符的总长度 """
    # 换行符个数
    lineBreaksNum = 0
    # 设置换行标志位
    text_list = list(text)
    # 字母或类字母字符的个数
    alpha_num = 0
    # 非字母字符的个数
    not_alpha_num = 0
    for index, i in enumerate(text):
        Match = re.match(r'[0-9A-Za-z:\+\-\{\}\d\(\)\*\.\s]', i)
        if Match:
            alpha_num += 1
        else:
            not_alpha_num += 1
        totalNum = not_alpha_num * 2 + alpha_num
        if totalNum % maxCharactersNum == 0:
            text_list.insert(index + 1+lineBreaksNum, '\n')
            lineBreaksNum += 1
        elif totalNum > maxCharactersNum and totalNum % maxCharactersNum == 1 and text_list[index] != '\n':
            text_list.insert(index + lineBreaksNum, '\n')
            lineBreaksNum += 1

    newText = ''.join(text_list)

    return newText,lineBreaksNum


if __name__ == "__main__":
    text = '哈哈哈哈哈哈哈哈哈哈或或或或或或或hhhhhhhhhhhhhhhhhhhhh或或或或或或或或或或或或或或或或或或或或或或哈哈哈哈哈哈哈哈哈哈或或或或或或或或或或或或或或或或或或或或或或或或'
    newText = autoWrap(text, 50)
    print(newText)
