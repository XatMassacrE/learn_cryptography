# 使用 Python 学习和破解古典密码

之前在研究一些数字货币的时候有一个概念深深的吸引了我，那就是**零知识证明**，它指的是**证明者能够在不向验证者提供任何有用的信息的情况下，使验证者相信某个论断是正确的**。通俗的讲就是我有一个 secret_key，但是我不会把这个 secret_key 提供给验证者，而让验证者相信我知道这个 secret_key。很神奇吧，但是我们今天并不是要说零知识证明，而是从密码学最基础的地方说起。对零知识证明感兴趣的同学可以去看看 [zkSNARKs in a nutshell](https://blog.ethereum.org/2016/12/05/zksnarks-in-a-nutshell/)。

古典密码学虽然在现在看起来非常简单，但是对于构建密码的原理和一些解决问题的方法上仍然值得我们学习。今天我们就使用 Python 来对两个著名的加密算法进行加解密和破解。本文源码在[这里](https://github.com/XatMassacrE/learn_cryptography)获取。

## 凯撒密码（Caesar Cipher）

### 介绍

凯撒密码属于替换密码的一种，替换密码就是指用一个别的字母来替换当前的字母。比如我和对方约定一个替换表： l -> h，o -> a，v -> t，然后我发送`love`给对方，对方按照对照表就知道我发送的其实是`hate`。凯撒密码使用的是将正常的 26 个英文字母进行移位替换，通常设定 shift 值为 3，相当于 a -> d，b -> e，c -> f... 

### 加解密方法（encrypt，decrypt）

下面给出加解密实现：

```
import string

lowercase = string.ascii_lowercase

def substitution(text, key_table):
    text = text.lower()
    result = ''
    for l in text:
        i = lowercase.find(l)
        if i < 0:
            result += l
        else:
            result += key_table[i]
    return result

def caesar_cypher_encrypt(text, shift):
    key_table = lowercase[shift:] + lowercase[:shift]
    return substitution(text, key_table)

def caesar_cypher_decrypt(text, shift):
    return caesar_cypher_encrypt(text, -shift)
    
```

为了看起来比较容易，所以在方法中把密文的空格和标点符号都保留了下来。

今天的两个例子都会使用下面这段经典密文（德国在一战期间邀请墨西哥进攻美国的密文，源自[齐默尔曼电报事件](https://en.wikipedia.org/wiki/Zimmermann_Telegram)）进行演示：

> We intend to begin on the first of February unrestricted submarine warfare. We shall endeavor in spite of this to keep the United States of America neutral. In the event of this not succeeding, we make Mexico a proposal of alliance on the following basis: make war together, make peace together, generous financial support and an understanding on our part that Mexico is to reconquer the lost territory in Texas, New Mexico, and Arizona. The settlement in detail is left to you. You will inform the President of the above most secretly as soon as the outbreak of war with the United States of America is certain and add the suggestion that he should, on his own initiative, invite Japan to immediate adherence and at the same time mediate between Japan and ourselves. Please call the President's attention to the fact that the ruthless employment of our submarines now offers the prospect of compelling England in a few months to make peace.

使用`caesar_cypher_encrypt(text, shift)`我们会得到：

> zh lqwhqg wr ehjlq rq wkh iluvw ri iheuxdub xquhvwulfwhg vxepdulqh zduiduh. zh vkdoo hqghdyru lq vslwh ri wklv wr nhhs wkh xqlwhg vwdwhv ri dphulfd qhxwudo. lq wkh hyhqw ri wklv qrw vxffhhglqj, zh pdnh phalfr d sursrvdo ri dooldqfh rq wkh iroorzlqj edvlv: pdnh zdu wrjhwkhu, pdnh shdfh wrjhwkhu, jhqhurxv ilqdqfldo vxssruw dqg dq xqghuvwdqglqj rq rxu sduw wkdw phalfr lv wr uhfrqtxhu wkh orvw whuulwrub lq whadv, qhz phalfr, dqg dulcrqd. wkh vhwwohphqw lq ghwdlo lv ohiw wr brx. brx zloo lqirup wkh suhvlghqw ri wkh deryh prvw vhfuhwob dv vrrq dv wkh rxweuhdn ri zdu zlwk wkh xqlwhg vwdwhv ri dphulfd lv fhuwdlq dqg dgg wkh vxjjhvwlrq wkdw kh vkrxog, rq klv rzq lqlwldwlyh, lqylwh mdsdq wr lpphgldwh dgkhuhqfh dqg dw wkh vdph wlph phgldwh ehwzhhq mdsdq dqg rxuvhoyhv. sohdvh fdoo wkh suhvlghqwv dwwhqwlrq wr wkh idfw wkdw wkh uxwkohvv hpsorbphqw ri rxu vxepdulqhv qrz riihuv wkh survshfw ri frpshoolqj hqjodqg lq d ihz prqwkv wr pdnh shdfh.

> 注：英国情报局截获的密文并不是这样使用凯撒密码加密的

### 破解

如果当时你截获到这样一份电报你会怎么想？在短暂的一面懵逼之后，显然要想办法破解出正常的意思才行。破解的思路其实也非常简单：因为加密时可以人为设定 shift 值，那么我们就从 0-25 循环来一遍看看哪个是有意义的就行了：

```
def crack_caesar_cypher(text):
    for i in range(26):
        key_table = lowercase[-i:] + lowercase[:-i]
        print(substitution(text, key_table)[:12], '| shift is ', i, )
```

看看结果：

![](https://user-gold-cdn.xitu.io/2017/9/23/b623844c68bbe7da4211904a25f38a7d)

哪一行是有意义的呢？

## 维吉尼亚密码（Vigener cipher）

### 介绍

凯撒密码显然无法阻挡人类的智慧，其实正常的替换密码的空间大小为 26!，这个数字非常大，相当于 2 的 88 次方，就是随机替换字母表生成加密表，然后按照加密表进行加密和解密，但是在字频分析下也败下阵来。然后就出现了维吉尼亚密码。维吉尼亚密码的加密方式也非常简单，先设定一个`key = 'crypto'`，然后将key循环排列与原信息按照字母一一对应，然后将字母在字母表中的所在位置进行相加得到一个index，然后将 index 模 26，得到加密后的字母在字母表中的位置。例如：

we intend to 
**cr yptocr yp**

相当于：

22 4 8 13 19 4 13 3 19 14
**2 17 24 15 19 14 2 17 24 15**

上下相加我们就得到：

24 21 32 28 38 18 15 20 43 29 再模 26 得到：
24 21 6 2 12 18 15 20 17 3

然后对应字母表我们得到：

yv gcmspu rd

### 加解密方法（encrypt，decrypt）

下面给出加解密实现：

```
def insert_letter(text, i, l):
    return text[:i] + l + text[i:]

def get_blank_record(text):
    text = text.lower()
    blank_record = []
    for i in range(len(text)):
        l = text[i]
        item = []
        if lowercase.find(l) < 0:
            item.append(i)
            item.append(l)
            blank_record.append(item)
    return blank_record

def restore_blank_record(text, blank_record):
    for i in blank_record:
        text = insert_letter(text, i[0], i[1])
    return text

def get_vigener_key_table(text, key):
    text = text.lower()
    trim_text = ''
    for l in text:
        if lowercase.find(l) >= 0:
            trim_text += l

    total_length = len(trim_text)
    key_length = len(key)
    quotient = total_length // key_length
    reminder = total_length % key_length
    key_table = quotient * key + key[:reminder]
    
    return trim_text, key_table

def vigener_cypher_encrypt(text, key, is_encrypt=True):
    blank_record = get_blank_record(text)
    trim_text, key_table = get_vigener_key_table(text, key)

    result = ''
    for i in range(len(trim_text)):
        l = trim_text[i]
        index_lowercase = lowercase.find(l)
        index_key_table = lowercase.find(key_table[i])
        if not is_encrypt:
            index_key_table = -index_key_table
        result += lowercase[(index_lowercase + index_key_table) % 26]

    return restore_blank_record(result, blank_record)

def vigener_cypher_decrypt(text, key):
    return vigener_cypher_encrypt(text, key, False)
    
```

使用`vigener_cypher_encrypt(text, key)`我们会得到：

> yv gcmspu rd usizl dg hjv dxkgv fd uxptlygr ipichmfktrtw gwskpkwpv upktcic. lx gjrja xbfvykhf ke qebhg fd iawu km zxsr kft nbkkcs lhckch ht cdcgbqc ecjmfcc. gc mvg vttgh qw rwbg pfr hnqevcsbbi, nc btyg dcmbqq r nghdqjya ht ccjxtbev mc mvg wmaecyzlv uouzq: btyg nyg mcivrwxf, orit isctc ihugkftk, ugecghiu wgctbezya lirgmgm opu yc nbfvphmopugcz cp fsg iotk rwth ovvxvc kj rd kseflfnst kft ecuk rtkfkkmgr wp kcmtg, pvu bxlktm, pgr cigohbc. kft lsvkjtfspk gc wsvrga bg nvdi mc afs. nhi yzja bbhfpb mvg gptlwfvli ht vyc pucxv kdlh uvagxhnp yh lcqe yh mvg fsiufgri dy kci uxmv vyc jgwvvb hmovvq dy oovpxvo kj atkhczl pgr cub ias ulevxgvzmc mvck ft lvqljs, hb jzq dpb kegibovztt, bbxzrt corrl ih wodcsbovv ysastvlrx opu yi mvg jybx hkdc bxrkrrt usvnctg xcgyc tbf fsglsnmch. izgrqt vonc rwx dtvqxwspkq pmhgerxhb vf rwx tctr iaov kft kivyjtlg gdnahmovli ht qlp hnporpxgsu eml hthvph mvg gpdldgtr dy qqdntezkee tgunrls bb c wcl fcpkfh mc orit isctc.

为了看起来比较容易，所以在方法中把密文的空格和标点符号都保留了下来。

上面的密文看起来似乎与凯撒密码差不多，但是这种加密方法在当时很难被破解。

### 破解

这种加密特点在于同样的字母加密之后并不会指向同样的密文，比如前3个单词`we intent to`中的 t，在凯撒密码或者常规的替换密码的下都会对应一个特定的字母，但是在这里我们可以看到`intent`中的`t`加密为`m`，`to`中的`t`加密为`r`。这样的话，**字频分析**也不起作用了。

但是道高一尺魔高一丈，这个号称不能被破解的密码还是迎来了被破解的命运：

假设我知道这个 key 的长度为 6。那么我们把密文以 6 个一组进行切割，那么一组中每个字母对应的原字母出现的的频率就是符合字频分析的，所谓的字频分析就是：**26 个英文字母在句子中出现的频率**。

![](https://user-gold-cdn.xitu.io/2017/9/24/fba9443be7d90d1e5baa7107e80be04a)

然后我们开始对每组的字频进行统计：

> group 0 : [{'c': 17}, {'g': 16}, {'v': 14}, {'p': 13}, {'k': 11}, {'o': 7}, {'q': 7}]
group 1 : [{'v': 23}, {'k': 17}, {'r': 11}, {'f': 10}, {'z': 10}, {'e': 8}, {'d': 6}]
group 2 : [{'c': 20}, {'r': 15}, {'y': 12}, {'l': 9}, {'g': 8}, {'m': 8}, {'p': 8}]
group 3 : [{'t': 22}, {'h': 11}, {'i': 11}, {'g': 10}, {'c': 9}, {'d': 9}, {'x': 8}]
group 4 : [{'m': 18}, {'h': 15}, {'x': 13}, {'b': 11}, {'l': 10}, {'g': 8}, {'k': 8}]
group 5 : [{'s': 16}, {'b': 14}, {'o': 13}, {'c': 10}, {'h': 10}, {'v': 9}, {'g': 8}]

根据字母频率表我们发现，字母`e`出现的频率超过了 12%，所以我们假设每组中至少有一个是字母`e`对应的密文，然后遍历出现次数超过10次的字母，并对另外两个出现频率最高的的字符数组`['t', 'a']`进行检测记分，然后得出最可能的的`key`。

下面是代码：

```
def get_trim_text(text):
    text = text.lower()
    trim_text = ''
    for l in text:
        if lowercase.find(l) >= 0:
            trim_text += l
    return trim_text
    
def crack_vigener_cypher(text, key_length):
    blank_record = get_blank_record(text)
    trim_text = get_trim_text(text)
    group = ['' for i in range(key_length)]
    for i in range(len(trim_text)):
        l = trim_text[i]
        for j in range(key_length):
            if i % key_length == j:
                group[j] += l

    key = ''
    letter_stats_group = []
    for j in range(key_length):
        letter_stats = []
        for l in lowercase:
            lt = {}
            count = group[j].count(l)
            lt[l] = count
            letter_stats.append(lt)

        letter_stats = sorted(letter_stats, key=lambda x: list(x.values())[0], reverse=True)
        letter_stats_group.append(letter_stats)
        # print('group', j, ':', letter_stats[:8])

        # gvctxs
        score_list = []
        for i in range(3):
            current_letter = list(letter_stats[i].keys())[0]
            index = lowercase.find(current_letter)
            key_letter = lowercase[index - lowercase.find('e')]
            item = []
            item.append(key_letter)
            score = 0
            for k in range(3):
                vl = list(letter_stats[k].keys())[0]
                for fl in ['t', 'a']:
                    #if i == 1 and (k == 1 or k == 2) and j == 1:
                    if (lowercase.find(key_letter) + lowercase.find(fl)) % 26 == lowercase.find(vl):
                        score += 1
            item.append(score)
            score_list.append(item)
        score_list = sorted(score_list, key=lambda x: x[1], reverse=True)
        key += score_list[0][0]

    plain_text = vigener_cypher_decrypt(trim_text, key)
    return restore_blank_record(plain_text, blank_record)

```

然后我们通过运行`crack_vigener_cypher(cypher_text, 6)`就可以得到明文了。然而这个地方大家可以看到，我默认传了一个参数 6 进去，也就是 key 的长度。但是当我们截获到密文的时候连 key 都不知道，显然也不会知道 key 的长度了。所以如果我们可以确定 key 的长度，那么维吉尼亚密码在我们面前就是纸老虎了。

实际上，像凯撒密码一样，从 1 到 25 去试也是可以破解的，但是我们这里使用一个叫做**重合指数**的方法来帮助缩小范围（虽然实际效果并不好，但是还是要理解一下方法）。

> 重合指数法：由26个字母构成的一段有意义文字中，任取两个元素刚好相同的概率约为0.067，所以如果一段明文是用同一个字母加密的话，这个概率依然不会改变。

因此我们可以写个方法来计算重合指数：

```

def get_coincidence_index(text):
    trim_text = get_trim_text(text)
    length = len(trim_text)
    letter_stats = []
    for l in lowercase:
        lt = {}
        count = trim_text.count(l)
        lt[l] = count
        letter_stats.append(lt)

    index = 0
    for d in letter_stats:
        v = list(d.values())[0]
        index += (v/length) ** 2

    return index
```

然后我们假设不同的 key 的长度，对每组密文进行重合指数的计算，然后选出和0.067相比方差较小的一部分长度作为备选：

```
def get_var(data, mean=0.067):
    if not data:
        return 0
    var_sum = 0
    for d in data:
        var_sum += (d - mean) ** 2

    return var_sum / len(data)
    
def get_key_length(text):
    trim_text = get_trim_text(text)
    # assume text length less than 26
    group = []
    for n in range(1, 26):
        group_str = ['' for i in range(n)]
        for i in range(len(trim_text)):
            l = trim_text[i]
            for j in range(n):
                if i % n == j:
                    group_str[j] += l
        group.append(group_str)

    var_list = []
    length = 1
    for text in group:
        data = []
        for t in text:
            index = get_coincidence_index(t)
            data.append(index)
        var_list.append([length, get_var(data)])
        length += 1
    var_list = sorted(var_list, key=lambda x: x[1])
    return [v[0] for v in var_list[:12]]    

```
> [[16, 2.9408699990533694e-05], [9, 3.8755178005797864e-05], [10, 5.415541187702294e-05], [17, 5.5154370298645345e-05], [19, 6.055960902865477e-05], [13, 8.572621594737114e-05], [8, 8.734954157595401e-05], [14, 9.767402405996375e-05], [3, 0.00010208649957333127], [20, 0.00012009258116435503], [11, 0.0001230940714957638], [6, 0.00014687184215509398]]
正确长度在第12个，我也很绝望啊...

现在万事具备了，直接遍历备选的 key_length，然后看看解密之后的效果吧。


![](https://user-gold-cdn.xitu.io/2017/9/24/0b9bdd6b6b1c3604d6c55134e4efde7f)

12 行，应该一眼就可以看到答案了吧。

本文到此结束，欢迎批评指正。


