import math

# 计算包含n个结点的完全m叉树,第k个节点的子树的节点数


def subtree_node_num(n, m, k):
    """
    计算完全 m 叉树中第 k 个节点所在的子树的节点数
    """
    # 计算树的高度
    h = 0
    while m**(h+1)-1 <= n:
        h += 1
    # 计算第 k 个节点所在的层数
    l = 0
    while (m**(l+1)-1)//(m-1) < k:
        l += 1
    if l < h:
        return m**(h-l)
    else:
        p = k - (m**h-1)//(m-1)
        return min(n-(m**h-1)//(m-1), m**h - (p-1)*m**(h-1))

print(subtree_node_num(74, 5, 3))
