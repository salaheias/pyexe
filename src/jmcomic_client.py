class JMComicClient:
    """一个安全包装器，尽量不对 jmcomic 的具体 API 做硬编码假设。

    使用示例：
        client = JMComicClient()
        client.list_comics()
        client.fetch_comic(comic_id)
    """

    def __init__(self):
        try:
            import jmcomic
        except Exception:
            jmcomic = None
        self._jm = jmcomic

    def _fn(self, *names):
        """查找第一个存在且可调用的属性名，返回函数或 None。"""
        if not self._jm:
            return None
        for n in names:
            fn = getattr(self._jm, n, None)
            if callable(fn):
                return fn
        return None

    def fetch_comic(self, comic_id):
        fn = self._fn("get_comic", "fetch_comic", "download")
        if not fn:
            raise RuntimeError("jmcomic 模块未提供已知的 fetch/get 函数")
        return fn(comic_id)

    def download_comic(self, comic_id, save_path):
        # 优先找直接下载函数，否则使用 fetch_comic 并尝试写入
        dl = self._fn("download_comic", "download", "save_comic")
        if dl:
            return dl(comic_id, save_path)

        comic = self.fetch_comic(comic_id)
        # 最保守的写法：若对象有 content 属性则写入，否则尝试将对象 bytes() 或 str()
        data = None
        if hasattr(comic, "content"):
            data = comic.content
        elif isinstance(comic, (bytes, bytearray)):
            data = comic
        else:
            try:
                data = bytes(comic)
            except Exception:
                data = str(comic).encode("utf-8")

        with open(save_path, "wb") as f:
            f.write(data)

    def list_comics(self):
        fn = self._fn("list_comics", "get_comics", "search", "list")
        if not fn:
            raise RuntimeError("jmcomic 模块未提供已知的列举函数")
        return fn()