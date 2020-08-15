import  numpy as np
from collections import deque

# 木探索基本クラス
class TreeSearch(object):

    # 初期化
    def __init__(self, start_node_number, finish_node_number):

        # ノードの名前のリスト(ノードiの名前はname[i])
        self.name =  np.array(['A','D','E','F','I','J','L','M','P','Q','U','V','W','Y'])
        
        # ノードの位置のx座標(ノードiのx座標はx[i])
        self.x = np.array([1,4,5,1,4,5,2,3,1,2,1,2,3,5])

        # ノードの位置のy座標(ノードiのy座標はy[i])
        self.y = np.array([5,5,5,4,4,4,3,3,2,2,1,1,1,1])
        
        # 隣接行列
             #                 A D E F I J L M P Q U V W Y
        self.link = np.array([[0,1,0,1,0,0,0,0,0,0,0,0,0,0],   # A
                              [0,0,1,0,1,0,0,0,0,0,0,0,0,0],   # D
                              [0,0,0,0,0,0,0,0,0,0,0,0,0,0],   # E
                              [0,0,0,0,0,0,0,1,1,0,0,0,0,0],   # F
                              [0,0,0,0,0,0,0,0,0,0,0,0,0,0],   # I
                              [0,0,0,0,0,0,0,0,0,0,0,0,0,0],   # J
                              [0,0,0,0,0,0,0,0,0,0,0,0,0,0],   # L
                              [0,0,0,0,0,1,1,0,0,0,0,0,1,0],   # M
                              [0,0,0,0,0,0,0,0,0,1,1,0,0,0],   # P
                              [0,0,0,0,0,0,0,0,0,0,0,0,0,0],   # Q
                              [0,0,0,0,0,0,0,0,0,0,0,0,0,0],   # U
                              [0,0,0,0,0,0,0,0,0,0,0,0,0,0],   # V
                              [0,0,0,0,0,0,0,0,0,0,0,1,0,1],   # W
                              [0,0,0,0,0,0,0,0,0,0,0,0,0,0],]) # Y

        # 開始・終了ノード番号のセット
        self.start_node_number, self.finish_node_number = start_node_number, finish_node_number

    # リスト操作
    # --------------------------------------------------------------------------------------------------------------------
    # リストの後ろに値を追加する
    def enqueue(self, List, extend_list):
        List.extend(extend_list)
    
    # リストの先頭の値を取り出す
    def dequeue(self, List):
        return List.popleft()

    # リストの先頭に値を追加する
    def push(self, List, extend_list):
        return List.extendleft(extend_list[::-1])

    # リストの後ろの値を取り出す
    def pop(self, List):
        return List.pop()
    # --------------------------------------------------------------------------------------------------------------------
    
    # その他操作

    # OpenListの初期化
    def init_open_list(self):
        self.open_list = deque([])
        self.push(self.open_list, [self.name[self.start_node_number]])

    # CloseListの初期化
    def init_close_list(self):
        self.close_list = deque([])

    # OpenListが空かを判定
    def judgment_open_list_empty(self):
        return len(self.open_list) == 0 

    # 取り出したノードが目標ノードか確認
    def judgment_finish_node(self, top_node):
        return self.finish_node_number == np.where(self.name == top_node)[0]

    # 親ノードから子ノードを取得
    def get_child_node(self, parent_node_name):

        # 親ノード名から親ノード番号を取得
        parent_node_number = np.where(self.name == parent_node_name)[0]
        
        # 親ノード番号から子ノード番号を取得
        child_node_rocation = self.link[parent_node_number,:][0]
        
        # 親ノード番号から子ノード名前リストを返す
        return np.take(self.name, child_node_rocation.nonzero())[0]

    # 子ノードで, OpenListにもCloseListにも含まれないものを返す
    def judgment_child_node(self, child_node_name_list):
        # OpenListとCloseListの和集合を計算する
        union_open_close_list = np.array(np.union1d(self.open_list, self.close_list))
        
        # 子ノードと先の和集合の差集合を計算する
        return np.setdiff1d(child_node_name_list, union_open_close_list)

    # x, y座標からnameのインデックスを取得
    def get_index_from_coord(coord_x, coord_y):
        return np.intersect1d(np.where(x == coord_x), np.where(y == coord_y))[0]

# 横型探索クラス
class DepthFirstSearch(TreeSearch):

    # 深さ優先探索
    def depth_first_search(self):
        print("-----------------------Start depth-first-search-----------------------")
        # 初期ノードをOpenListにいれる, CloseListを空にする(Step 1)
        self.init_open_list()
        self.init_close_list()

        print("Start search ", end="→")
        while True:

            # OpenListが空なら解なしで終了(Step 2)
            if self.judgment_open_list_empty():
                print("Empty OpenList no answer")
                return
            
            # OpenListから先頭の要素nを取り出し, CloseListにnを追加する(Step 3)
            top_node = self.dequeue(self.open_list)
            self.enqueue(self.close_list, top_node)
            print("{}".format(top_node[0]), end="→")

            # ノードnが目標であれば, nを解として終了
            if self.judgment_finish_node(top_node):
                print(" Finish search")
                return
            
            # nから1ステップでたどれる子ノードの中で, OpenListにもCloseListにも含まれていないものはすべてOpenListの先頭に移動する
            self.push(self.open_list, self.judgment_child_node(self.get_child_node(top_node)))

# 縦型探索クラス
class BreadthFirstSearch(TreeSearch):

    # 深さ優先探索
    def breadth_first_search(self):
        print("-----------------------Start breadt-first-search-----------------------")
        # 初期ノードをOpenListにいれる, CloseListを空にする(Step 1)
        self.init_open_list()
        self.init_close_list()

        print("Start search ", end="→")
        while True:

            # OpenListが空なら解なしで終了(Step 2)
            if self.judgment_open_list_empty():
                print("Empty OpenList no answer")
                return
            
            # OpenListから先頭の要素nを取り出し, CloseListにnを追加する(Step 3)
            top_node = self.dequeue(self.open_list)
            self.enqueue(self.close_list, top_node)
            print("{}".format(top_node[0]), end="→")

            # ノードnが目標であれば, nを解として終了
            if self.judgment_finish_node(top_node):
                print(" Finish search")
                return
            
            # nから1ステップでたどれる子ノードの中で, OpenListにもCloseListにも含まれていないものはすべてOpenListの先頭に移動する
            self.enqueue(self.open_list, self.judgment_child_node(self.get_child_node(top_node)))

# A*探索クラス
class AStarSearch(TreeSearch):
    
    def __init__(self, start_node_number, finish_node_number):
        super(AStarSearch, self).__init__(start_node_number, finish_node_number)
        
        # 推定コストの初期化
        self.cost_list = np.zeros(self.name.shape[0])

    # 始めのノードのコスト設定
    def init_cost_list(self):
        # 目標ノードのx, y座標を取得
        finish_coord_x, finish_coord_y = self.x[self.finish_node_number], self.y[self.finish_node_number]        

        # 開始ノードのx, y座標を取得
        start_coord_x, start_coord_y = self.x[self.start_node_number], self.y[self.start_node_number]

        self.cost_list[self.start_node_number] = abs(finish_coord_x - start_coord_x) + abs(finish_coord_y - start_coord_y)

    # 推定コスト計算
    def estimate_cost_sort(self, now_node_name):
        # 目標ノードのx, y座標を取得
        finish_coord_x, finish_coord_y = self.x[self.finish_node_number], self.y[self.finish_node_number]
        
        # 計算した推定コストを保持する配列
        cost_cache = np.zeros(len(self.open_list))

        # OpenList内のそれぞれのノードについて考える
        for cost_cache_number, open_list_node in enumerate(self.open_list):
            # 始点ノードからノードnまでのコストg(n)を見つける
            open_list_node_number = np.where(self.name == open_list_node)[0]
            parent_node_number = np.where(self.link[:, open_list_node_number] == 1)[0]
            parent_cost = self.cost_list[parent_node_number]
            
            # ノードのx, y座標を取得
            n_coord_x, n_coord_y = self.x[np.where(self.name == open_list_node)][0], self.y[np.where(self.name == open_list_node)][0]
            
            # マンハッタン距離を計算して保存する
            cost_cache[cost_cache_number] = (abs(finish_coord_x - n_coord_x) + abs(finish_coord_y - n_coord_y)) + parent_cost

        # 計算したコストからOpenListをソートする
        choice_node_name = np.array(self.open_list)[np.argsort(cost_cache, axis=0) == 0][0]
        self.cost_list[np.where(self.name == choice_node_name)[0]] = min(cost_cache)
        self.open_list = deque(np.array(self.open_list)[np.argsort(cost_cache, axis=0)])

    # A*探索
    def a_star_search(self):
        print("-----------------------Start A-star-search-----------------------")
        # 初期ノードをOpenListにいれる, CloseListを空にする(Step 1)
        self.init_open_list()
        self.init_close_list()

        # 初期ノードのコストを設定しておく
        self.init_cost_list()

        print("Start search ", end="→")
        while True:

            # OpenListが空なら解なしで終了(Step 2)
            if self.judgment_open_list_empty():
                print("Empty OpenList no answer")
                return
            
            # OpenListから先頭の要素nを取り出し, CloseListにnを追加する(Step 3)
            top_node = self.dequeue(self.open_list)
            self.enqueue(self.close_list, top_node)
            print("{}".format(top_node[0]), end="→")

            
            # ノードnが目標であれば, nを解として終了
            if self.judgment_finish_node(top_node):
                print(" Finish search")
                return
            
            # nから1ステップでたどれる子ノードの中で, OpenListにもCloseListにも含まれていないものはすべてOpenListの先頭に移動する(Step 5-1)
            self.enqueue(self.open_list, self.judgment_child_node(self.get_child_node(top_node)))

            # OpenList内のノードの推定コストを計算して, コストの小さく順にソートする(Step 5-2)
            self.estimate_cost_sort(top_node[0])

print("\n=========Start script=========\n")

depth = DepthFirstSearch(0,13)
depth.depth_first_search()
print("\n")
bread = BreadthFirstSearch(0,13)
bread.breadth_first_search()
print("\n")
a_star = AStarSearch(0,13)
a_star.a_star_search()

print("\n=========Finish script=========\n")
