'''Dubug 版本的Senko.py'''
import urequests
import uhashlib
import gc
from time import sleep
import micropython

class Senko:
    raw = "https://raw.githubusercontent.com"
    github = "https://github.com"

    def __init__(self, user, repo, url=None, branch="master", working_dir="app", files=["boot.py", "main.py"], headers={}):
        """Senko OTA agent class.

        Args:
            user (str): GitHub user.
            repo (str): GitHub repo to fetch.
            branch (str): GitHub repo branch. (master)
            working_dir (str): Directory inside GitHub repo where the micropython app is.
            url (str): URL to root directory.
            files (list): Files included in OTA update.
            headers (list, optional): Headers for urequests.
        """
        self.base_url = "{}/{}/{}".format(self.raw, user, repo) if user else url.replace(self.github, self.raw)
        self.url = url if url is not None else "{}/{}/{}".format(self.base_url, branch, working_dir)
        self.headers = headers
        self.files = files
    # 比對檔案內容
    def _check_hash(self, x, y):
        #計算 x（GitHub 版本）與 y（本地版本）的 SHA1 雜湊
        x_hash = uhashlib.sha1(x.encode())
        y_hash = uhashlib.sha1(y.encode())

        x = x_hash.digest()
        y = y_hash.digest()

        ## 取的比對結果
        result = (str(x) == str(y))
        # if str(x) == str(y):
        #     return True #比對 SHA1 是否相同，如果不同代表程式碼有變更，需要更新
        # else:
        #     return False
        print(f"Debugger:[_check_hash] x,y哈希值:{x_hash}，記憶體:{gc.mem_free()}")
        #回收哈希值
        del x_hash, y_hash, x, y
        gc.collect()
        print(f"Debugger:[_check_hash] 刪除x,y哈希值{result}，記憶體:{gc.mem_free()}")
        return result


        # 這裡的x, y在實際調用時，會傳參 latest_version 和 local_version
        # 函式裡面又對這兩個參數做x_hash  y_hash 
        # 但這個.check_hash()函式 我們只需要知道TURE OR FALSE 因此要刪除 x_hash 和y_hash
        # 後續的gc.collect()才有效果
        # if str(x) == str(y):
        #     return True #比對 SHA1 是否相同，如果不同代表程式碼有變更，需要更新
        # else:
        #     return False

    def _get_file(self, url):
        # =======
        # 記憶體測試
        # =====
        gc.collect()
        micropython.mem_info()
        # 發送 HTTP GET 請求 下載 GitHub 上的最新版本程式碼
        print(f"Debugger:[_get_file] 這裡執行.get(): {url}")  # 🔍 加入 URL 印出來檢查
        payload = urequests.get(url, headers=self.headers)
        code = payload.status_code # 取的狀態碼
        print(f"Debugger:[_get_file] HTTP 狀態碼: {code}") 
        #print("read ok  "+url)
        gc.collect()
        #print(gc.mem_free())
        if code == 200:
            data = payload.text
            print(f"Debugger:[_get_file] status(200)")
            return data #回傳文字內容（程式碼）
        else:
            print(f"Debugger:[_get_file] 無法取得 {url}，回傳 None")
            return None
    # def _get_file(self, url):
    #     """ 以 chunked 方式下載檔案，避免記憶體爆滿 """
    #     import urequests
        
    #     gc.collect()
    #     micropython.mem_info()
        
    #     try:
    #         response = urequests.get(url, headers=self.headers, stream=True)  # 以串流模式下載
    #         if response.status_code == 200:
    #             file_name = url.split("/")[-1]  # 取得檔案名稱
    #             with open(file_name, "w") as f:
    #                 while True:
    #                     chunk = response.raw.read(512)  # 每次讀取 512 bytes
    #                     if not chunk:
    #                         break
    #                     f.write(chunk.decode())  # 逐行寫入檔案
    #             response.close()
    #             return True
    #         else:
    #             print(f"無法下載 {file_name}, 狀態碼: {response.status_code}")
    #     except Exception as e:
    #         print(f"下載 {file_name} 失敗: {e}")
    #     return False


    ## 檢查哪些檔案需要更新(微調版)
    def _check_all(self):
        changes = []
        print('Debugger:[senko._check_all] 開始') 
        gc.collect()
        index_times = 0
        print(f"Debugger:[senko._check_all] 進入files迴圈前:{gc.mem_free()}") 
        for file in self.files:
            # =====
            # 新版待測試 所以使用60000 總體記憶體為標準試看看
            # =====
            index_times += 1
            
            print(f'Debugger:[senko._check_all 迴圈跑到{file}]  第: {index_times} 檔案，記憶體為：')
            micropython.mem_info()
            ## 記憶體不夠用才會跑這裡 但即使gc後沒有60000 還是出不了這個while??
            while(gc.mem_free() < 60000): #確保記憶體夠用 (gc.mem_free() < 60000
                # =====
                # 打印整體記憶體資訊
                # =====
                gc.collect()
                print(f'Debugger:[while內] 釋放記憶體：')
                micropython.mem_info()
                sleep(1)
                
            print(f'Debugger:[senko._check_all] 準備下載 {file} 的latest_version，記憶體:')
            micropython.mem_info()
            latest_version = self._get_file(self.url + "/" + file)  # 調用方法發送請求 下載 GitHub 上的最新版本程式碼    
            if latest_version is None:
                print(f'Debugger:[senko._check_all]  {file} 沒有 latest_version')
                continue

            print(f'Debugger:[senko._check_all] 準備下載 {file} 的local_version，記憶體:')
            micropython.mem_info()
            try:
                with open(file, "r") as local_file: #讀取 ESP32 本地版本的相同檔案
                    local_version = local_file.read()
                    print(f'Debugger:[senko._check_all]  讀取 {file} 的local_version')
            except:
                local_version = ""
                print(f'Debugger:[senko._check_all] {file} 目前local_version為空')

            #### 這裡調用了._check_hash(latest_version, local_version)
            if not self._check_hash(latest_version, local_version):
                changes.append(file) #如果 不同，代表有變更，加入 changes 清單
                print(f'Debugger:[senko._check_all] 目前已加入changes清單，有 {changes} ')
            else:
                 # **清空 latest_version 和 local_version**
                print(f"Debugger:[latest_version與local_version & gc以前] 遠端和本地檔案內容一致，記憶體:{gc.mem_free()}")
                del latest_version, local_version
                gc.collect()
                print(f"Debugger:[latest_version與local_version& gc以後] 遠端和本地檔案內容一致，無須更新，不用重啟，記憶體:{gc.mem_free()}")
            # 釋放記憶體
            gc.collect()
            print(f"Debugger:[gc後]:{gc.mem_free()}")
        return changes

    # 執行 OTA 更新
    def update(self):
        changes = self._check_all() #呼叫 _check_all() 找出需要更新的檔案
        gc.collect()
        print(f'Debugger[senko.update] memory_data: {gc.mem_free()}') 

        #這裡指的是 如果有changes回傳 沒有就代表無須更新 遠端檔案 與本地檔案一致
        for file in changes: #逐一下載 GitHub 最新版本並覆蓋 ESP32 上的舊版本
            with open(file, "w") as local_file:
                local_file.write(self._get_file(self.url + "/" + file))
            

        if changes:
            return True
        else:
            print(f'Debugger[senko.update] 遠端檔案 和本地檔案 一致 無須更新') 
            return False
