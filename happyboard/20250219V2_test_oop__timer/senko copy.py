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

        if str(x) == str(y):
            return True #比對 SHA1 是否相同，如果不同代表程式碼有變更，需要更新
        else:
            return False

    def _get_file(self, url):
        # =======
        # 記憶體測試
        # =====
        gc.collect()
        micropython.mem_info()
        # 發送 HTTP GET 請求 下載 GitHub 上的最新版本程式碼
        payload = urequests.get(url, headers=self.headers)
        code = payload.status_code # 取的狀態碼
        #print("read ok  "+url)
        gc.collect()
        #print(gc.mem_free())
        if code == 200:
            return payload.text #回傳文字內容（程式碼）
        else:
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
        print('debug[senko._check_all] Start') 
        gc.collect()
        gc.mem_free()
        index_times = 0
        for file in self.files:
            # =====
            # 新版待測試 所以使用60000 總體記憶體為標準試看看
            # =====
            index_times += 1
            
            print(f'debug[senko._check_all loop]: {file},{index_times}')
            micropython.mem_info()
            while(gc.mem_free() < 60000): #確保記憶體夠用 (gc.mem_free() < 60000
                # =====
                # 打印整體記憶體資訊
                # =====
                gc.collect()
                micropython.mem_info()
                #print(gc.mem_free())
                print(f"記憶體不足，等待中... (可用記憶體: {gc.mem_free()})")
                sleep(1)
            latest_version = self._get_file(self.url + "/" + file)  # 調用方法發送請求 下載 GitHub 上的最新版本程式碼    
            if latest_version is None:
                continue

            try:
                with open(file, "r") as local_file: #讀取 ESP32 本地版本的相同檔案
                    local_version = local_file.read()
            except:
                local_version = ""

            if not self._check_hash(latest_version, local_version):
                changes.append(file) #如果 不同，代表有變更，加入 changes 清單
            # latest_version=""
            # local_version = ""
            # 釋放記憶體
            del latest_version, local_version
            gc.collect()
        return changes
    # def _check_all(self):
    #     changes = []
    #     print('debug[senko._check_all] memory_data') 
    #     gc.collect()
    #     gc.mem_free()
    #     index_times = 0
    #     for file in self.files:
    #         # =====
    #         # 新版待測試 所以使用60000 總體記憶體為標準試看看
    #         # =====
    #         index_times += 1
            
    #         print(f'debug[senko._check_all loop]: {file},{index_times}')
    #         micropython.mem_info()
    #         while(gc.mem_free() < 60000): #確保記憶體夠用 (gc.mem_free() < 60000
    #             # =====
    #             # 打印整體記憶體資訊
    #             # =====
    #             #gc.collect()
    #             #micropython.mem_info()
    #             #print(gc.mem_free())
    #             sleep(1)
    #         latest_version = self._get_file(self.url + "/" + file)  # 調用方法發送請求 下載 GitHub 上的最新版本程式碼    
    #         if latest_version is None:
    #             continue

    #         try:
    #             with open(file, "r") as local_file: #讀取 ESP32 本地版本的相同檔案
    #                 local_version = local_file.read()
    #         except:
    #             local_version = ""

    #         if not self._check_hash(latest_version, local_version):
    #             changes.append(file) #如果 不同，代表有變更，加入 changes 清單
    #         latest_version=""
    #         local_version = ""

    #     return changes

    # def fetch(self): # 沒有使用
    #     """Check if newer version is available.

    #     Returns:
    #         True - if is, False - if not.
    #     """
    #     if not self._check_all():
    #         return False
    #     else:
    #         return True
    # 執行 OTA 更新
    def update(self):
        """Replace all changed files with newer one.

        Returns:
            True - if changes were made, False - if not.
        """
        changes = self._check_all() #呼叫 _check_all() 找出需要更新的檔案
        gc.collect()
        # =======
        # 記憶體打印
        # =====
        print('debug[senko.update] memory_data') 
        micropython.mem_info()
        for file in changes: #逐一下載 GitHub 最新版本並覆蓋 ESP32 上的舊版本
            with open(file, "w") as local_file:
                local_file.write(self._get_file(self.url + "/" + file))
            

        if changes:
            return True
        else:
            return False
